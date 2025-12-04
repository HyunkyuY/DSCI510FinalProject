import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from src.config import (
    MASTERS_YEARS,
    MASTERS_FILE_TEMPLATE,
    SEASON_SG_CSV,
    LASSO_PREDICTIONS_CSV,
    XGB_PREDICTIONS_CSV,
    RANDOM_STATE,
    TEST_SIZE,
    LASSO_ALPHA,
    XGB_N_ESTIMATORS,
    XGB_LEARNING_RATE,
    XGB_MAX_DEPTH,
    XGB_SUBSAMPLE,
    XGB_COLSAMPLE_BYTREE,
    XGB_OBJECTIVE,
)

from src.utils import download_file_from_gdrive
from src.config import (
    MASTERS_GDRIVE_FILES,
    LOCAL_MASTERS_TEMPLATE,
    LOCAL_SEASON_SG_FILE,
)

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names: lowercase, underscores, no dashes."""
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def clean_player_name(name: str) -> str:
    """Normalize player names and handle 'Last, First' formats."""
    if pd.isna(name):
        return name
    name = str(name).strip()
    if "," in name:
        last, first = [x.strip() for x in name.split(",", 1)]
        return f"{first} {last}"
    return name


def main():
    # Load and clean Masters historical data (2021-2025)
    masters_paths = []

    for year, gdrive_url in MASTERS_GDRIVE_FILES.items():
        local_file = LOCAL_MASTERS_TEMPLATE.format(year=year)
        download_file_from_gdrive(gdrive_url, local_file)
        masters_paths.append(local_file)

    masters_list = []
    for path in masters_paths:
        year = int(os.path.basename(path)[:4])
        df = pd.read_csv(path)
        df = clean_columns(df)
        df["player"] = df["player_name"].apply(clean_player_name)
        df["year"] = year
        masters_list.append(df)

    masters_df = pd.concat(masters_list, ignore_index=True)

    masters_df = masters_df.drop(columns=["sg_t2g", "sg_total"], errors="ignore")

    # Handle missing values and define features
    feature_cols = ["sg_ott", "sg_app", "sg_arg", "sg_putt"]

    print("Missing values per column:")
    print(masters_df[feature_cols + ["total_score"]].isna().sum())

    masters_clean = masters_df.dropna(subset=feature_cols + ["total_score"]).copy()

    print("\nShape before cleaning:", masters_df.shape)
    print("Shape after cleaning:", masters_clean.shape)

    # Correlation between strokes gained and score at the Masters: heatmap
    plt.figure(figsize=(8, 6))
    corr = masters_clean[["total_score"] + feature_cols].corr()
    sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0)
    plt.title("Correlation Between Strokes Gained Metrics and Score at The Masters")
    plt.show()

    # Linear Regression (Direction and Magniture of Effects)
    X_event = masters_clean[feature_cols]
    y_event = masters_clean["total_score"]

    linreg = LinearRegression()
    linreg.fit(X_event, y_event)

    lin_coeffs = pd.DataFrame({
        "Feature": feature_cols,
        "Coefficient": linreg.coef_
    }).sort_values("Coefficient")
    print("Linear regression coefficients:\n", lin_coeffs)

    # LASSO to learn coefficients on SG weighting at the Masters
    X_train_e, X_test_e, y_train_e, y_test_e = train_test_split(
        X_event, y_event, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    lasso = Lasso(alpha=LASSO_ALPHA)
    lasso.fit(X_train_e, y_train_e)

    lasso_importance = pd.DataFrame({
        "Feature": feature_cols,
        "LASSO_Weight": lasso.coef_
    }).sort_values("LASSO_Weight")
    print("LASSO importance:\n", lasso_importance)

    plt.figure(figsize=(7, 5))
    sns.barplot(data=lasso_importance, x="LASSO_Weight", y="Feature")
    plt.title("LASSO Feature Importance - Masters Event-Level SG")
    plt.xlabel("Coefficient (more negative = lowers score more)")
    plt.show()

    y_pred_lasso_event = lasso.predict(X_test_e)

    plt.figure(figsize=(5, 5))
    plt.scatter(y_test_e, y_pred_lasso_event, alpha=0.7)
    plt.plot(
        [y_test_e.min(), y_test_e.max()],
        [y_test_e.min(), y_test_e.max()],
        linestyle="--",
    )
    plt.xlabel("Actual Score")
    plt.ylabel("Predicted Score")
    plt.title("LASSO: Predicted vs Actual at the Masters")
    plt.tight_layout()
    plt.show()

    # Predicting the 2026 Masters Using Season-Long SG Stats
    # Compute Augusta skill index for historical Masters players
    beta = lasso.coef_.copy()
    z_event = X_event.values @ beta

    # Fit calibration model: total_score ~ a + b * z_event
    calib_reg = LinearRegression()
    calib_reg.fit(z_event.reshape(-1, 1), y_event)

    a = calib_reg.intercept_
    b = calib_reg.coef_[0]
    print("Calibration parameters a, b:", a, b)

    # Load Season-Long Strokes Gained Data (PGA/LIV/EURO (DP World Tour)) ----------
    sg_df_raw = pd.read_csv(SEASON_SG_CSV)
    sg_df = sg_df_raw.copy()
    sg_df.columns = (
        sg_df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Standardize player names
    sg_df["player"] = sg_df["player"].apply(clean_player_name)

    print("Season SG columns after cleaning:")
    print(sg_df.columns.tolist())

    # Standardize SG column names
    rename_map = {
        "ott": "sg_ott",
        "app": "sg_app",
        "arg": "sg_arg",
        "putt": "sg_putt"
    }
    sg_df = sg_df.rename(columns=rename_map)
    season_feature_cols = ["sg_ott", "sg_app", "sg_arg", "sg_putt"]
    # Keep only players with complete SG data for these four categories
    sg_clean = sg_df.dropna(subset=season_feature_cols).copy()
    print("\nShape before cleaning:", sg_df.shape)
    print("Shape after cleaning:", sg_clean.shape)

    # Apply the Augusta Model to Season SG Data
    X_season = sg_clean[season_feature_cols].values
    z_season = X_season @ beta

    # Predicted Masters total score relative to par
    yhat_season = calib_reg.predict(z_season.reshape(-1, 1))
    pred_df = sg_clean.copy()
    pred_df["PredictedScore"] = yhat_season

    # Lower score = better performance
    leaderboard = pred_df[["player", "PredictedScore"]].sort_values("PredictedScore")
    print("Top 15 LASSO+Linear-based predictions:")
    print(leaderboard.head(15))

    # Output: Predicted 2026 Masters Tournament Leaderboard
    leaderboard.to_csv(LASSO_PREDICTIONS_CSV, index=False)
    print("Saved LASSO+Linear-based predictions to:", LASSO_PREDICTIONS_CSV)

    # Train XGBoost on the same event-level features used for LASSO
    xgb = XGBRegressor(
        n_estimators=XGB_N_ESTIMATORS,
        learning_rate=XGB_LEARNING_RATE,
        max_depth=XGB_MAX_DEPTH,
        subsample=XGB_SUBSAMPLE,
        colsample_bytree=XGB_COLSAMPLE_BYTREE,
        objective=XGB_OBJECTIVE,
        random_state=RANDOM_STATE,
    )

    xgb.fit(X_train_e, y_train_e)

    # Evaluate on held-out Masters data
    y_pred_xgb_event = xgb.predict(X_test_e)
    mae_xgb = mean_absolute_error(y_test_e, y_pred_xgb_event)
    rmse_xgb = root_mean_squared_error(y_test_e, y_pred_xgb_event)
    print("XGBoost MAE, RMSE:", mae_xgb, rmse_xgb)

    plt.figure(figsize=(5, 5))
    plt.scatter(y_test_e, y_pred_xgb_event, alpha=0.7)
    plt.plot(
        [y_test_e.min(), y_test_e.max()],
        [y_test_e.min(), y_test_e.max()],
        linestyle="--"
    )
    plt.xlabel("Actual Scores")
    plt.ylabel("Predicted Scores")
    plt.title("XGBoost: Predicted vs Actual Scores at the Masters")
    plt.tight_layout()
    plt.show()

    # Use season-long SG features for 2025 to predict 2026 Masters scores with XGBoost
    X_season_xgb = sg_clean[season_feature_cols].values
    yhat_season_xgb = xgb.predict(X_season_xgb)

    leaderboard_xgb = sg_clean.copy()
    leaderboard_xgb["PredictedScore_XGB"] = yhat_season_xgb
    leaderboard_xgb = leaderboard_xgb[["player", "PredictedScore_XGB"]].sort_values(
        "PredictedScore_XGB"
    )

    print("Top 15 XGBoost-based predictions:")
    print(leaderboard_xgb.head(15))

    leaderboard_xgb.to_csv(XGB_PREDICTIONS_CSV, index=False)
    print("Saved XGBoost-based predictions to:", XGB_PREDICTIONS_CSV)


if __name__ == "__main__":
    main()
