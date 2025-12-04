# DSCI 510 Final Project: Masters Performance Prediction & WITB Equipment Analysis

This project predicts professional golfers' performance at the **2026 Masters Tournament** using historical strokes-gained data and machine learning models. It also includes a full **What's-In-The-Bag (WITB)Analysis** to study brand and club trends across professional golfers.

## Introduction

This project focuses on using historical **Masters Tournament performance data** and **season-long strokes-gained statistics** to predict player performance at the 2026 Masters Tournament. Two independent machine learning models are built: a LASSO-linear regression model for interpretability and an XGBoost model for high predictive accuracy. In addition, the project scrapes and analyzes **professional golf equipment (WITB)** data to study brand dominance and equipment trends.


## Data Sources

  --------------------------------------------------------------------------------
  Dataset          Source           Description          Access Method
  ---------------- ---------------- -------------------- -------------------------
  Masters          Google Drive     Historical Masters   Downloaded automatically
  Tournament       (Datagolf.com)   strokes-gained and   at runtime
  Results                           scoring data         
  (2021-2025)                                           

  Season           Datagolf.com     Season-long player   Loaded locally after
  Strokes-Gained                    performance metrics  scraping
  Data (PGA/LIV/DP                            
  World Tour)                                            

  WITB Equipment   PGAClubTracker   Professional golf    Web scraping with
  Data             Website          bag equipment data   Selenium + BeautifulSoup
  --------------------------------------------------------------------------------


## Analysis

The project contains the following:

-   **Predictive Modeling**
    -   LASSO-linear regression for interpretable performance prediction
    -   XGBoost regression for nonlinear, high-accuracy prediction
-   **Feature Engineering**
    -   Cleaning and standardizing strokes-gained metrics
    -   Creating calibrated skill indices for Augusta National
-   **Model Evaluation**
    -   Train/test splitting
    -   Error metrics including MAE and RMSE
-   **Web Scraping & Equipment Analysis**
    -   Scraping club, shaft, and brand data from professional golfers
    -   SQLite-based analytical queries on equipment usage trends


## Summary of the Results

The results of the project show a strong and intuitive picture of what drives success at Augusta National and who is most likely to contend in the future. From the LASSO-Linear Regression model, short-game and approach play clearly emerged as the most important skills for Masters performance. When this model was used to generate a prediction for the 2026 leaderboard, Scottie Scheffler came out as the top projected finisher, followed by Rory McIlroy and Tommy Fleetwood. The XGBoost model produced a slightly different forecast, placing Scottie Scheffler at the top again but with Tommy Fleetwood and Russell Henley rounding out the top three. The consistency of Scheffler and Fleetwood across both models highlights the stability of the models, while the differences in rankings reflect how performance at the Masters can shift depending on nonlinear factors like form, volatility, and interaction between skills. Overall, these outputs show that the models not only capture real golf behavior, but also produce exciting future tournament projections.


## Project Components

-   **Masters Prediction Pipeline**
    -   Loads multi-year Masters tournament data (2021--2025)
    -   Trains LASSO and XGBoost regression models
    -   Generates predicted 2026 Masters scores
-   **Season Strokes-Gained Data**
    -   Uses combined PGA / LIV / European Tour season statistics
-   **WITB Equipment Scraper**
    -   Scrapes professional golf bag data using Selenium +
        BeautifulSoup
    -   Stores results in CSV format
-   **Equipment Analysis**
    -   Brand dominance
    -   Driver arms race
    -   Wedge distributions
    -   Shaft and club trends using SQLite
-   **Unit Tests**
    -   Includes real data-loading verification


## Installation

Install all required dependencies:

    pip install -r requirements.txt

**For Selenium (WITB scraping):** 
- Google Chrome must be installed 
-ChromeDriver must be available in your system PATH


## How to Run

From the **project root directory**, run:

    python -m src.main

This command will:

1.  Download all **Masters CSV files from Google Drive**
2.  Load **season strokes-gained data**
3.  Train **LASSO & XGBoost models**
4.  Generate prediction outputs:
    -   `masters_2026_predicted.csv`
    -   `masters_2026_predicted_XGB.csv`
5.  Scrape **WITB equipment data**
6.  Run **SQLite equipment analysis**
7.  Print formatted tables to the terminal

### Running Unit Tests

    python tests.py

This verifies:
- Google Drive Downloading 
- Utility function behavior 
- Basic model training

## Output Files

After running, the following files are generated:

-   `masters_2026_predicted.csv` (LASSO-linear model predictions)
-   `masters_2026_predicted_XGB.csv` (XGBoost model predictions)
-   `pgaclubtracker_witb_all_players.csv` (WITB scraping output)