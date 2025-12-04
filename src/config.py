# Masters Tournament historical data
MASTERS_YEARS = [2021, 2022, 2023, 2024, 2025]
MASTERS_FILE_TEMPLATE = "{year}_masters_tournament_event_values.csv"

# Season strokes-gained data
SEASON_YEAR = 2025
DATAGOLF_BASE_URL = "https://datagolf.com/get-tour-lists"
SEASON_SG_CSV = f"pga_liv_euro_{SEASON_YEAR}_strokes_gained_combined.csv"

# WITB (What's In The Bag) scraper
PGACT_BASE_URL = "https://www.pgaclubtracker.com"
WITB_CSV = "pgaclubtracker_witb_all_players.csv"

# Masters Prediction output files
LASSO_PREDICTIONS_CSV = "masters_2026_predicted.csv"
XGB_PREDICTIONS_CSV = "masters_2026_predicted_XGB.csv"

# Google Drive data sources (these are available from Datagolf, but only with paid subscription)
MASTERS_GDRIVE_FILES = {
    2021: "https://drive.google.com/file/d/1tjp0oDdD7gJvocQZo4QiB45itDnDZavX/view?usp=sharing",
    2022: "https://drive.google.com/file/d/11T_bn_fCw_lzkC_XoWQ7pj1M81tuJttK/view?usp=sharing",
    2023: "https://drive.google.com/file/d/168RjJ682RQx9grBJoai02tHwVa5bGor1/view?usp=sharing",
    2024: "https://drive.google.com/file/d/1O9rV6YdAjr6fYjtMdscb0T-dnO6J1TNW/view?usp=sharing",
    2025: "https://drive.google.com/file/d/1zU4Jb3ma4SSUQng2cIU4ktpUsnVrh39s/view?usp=sharing",
}

# Local filenames after download
LOCAL_MASTERS_TEMPLATE = "{year}_masters_tournament_event_values.csv"
LOCAL_SEASON_SG_FILE = "pga_liv_euro_2025_strokes_gained_combined.csv"

# Predictrion Modeling Parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
LASSO_ALPHA = 0.05
XGB_N_ESTIMATORS = 400
XGB_LEARNING_RATE = 0.05
XGB_MAX_DEPTH = 3
XGB_SUBSAMPLE = 0.9
XGB_COLSAMPLE_BYTREE = 0.9
XGB_OBJECTIVE = "reg:squarederror"
