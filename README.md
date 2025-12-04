# DSCI 510 Final Project: Masters Performance Prediction & WITB Equipment Analysis

This project predicts professional golfers' performance at the **2026 Masters Tournament** using historical strokes-gained data and machine learning models. It also includes a full **What's-In-The-Bag (WITB)equipment scraping and analysis pipeline** to study brand and club trends across professional golfers.


## Project Components

-   **Masters Prediction Pipeline**
    -   Loads multi-year Masters tournament data (2021-2025)
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

**For Selenium:** - Google Chrome must be installed -
ChromeDriver must be available in your system PATH


## Running the Full Pipeline

From the **project root directory**, run:

    python -m src.main

This command will: 
1. Download all **Masters CSV files from Google Drive** 
2. Load **season strokes-gained data** 
3. Train **LASSO-Linear & XGBoost models** 
4. Generate prediction outputs: -
`masters_2026_predicted.csv` - `masters_2026_predicted_XGB.csv` 
5. Scrape **WITB equipment data** 
6. Run **SQLite equipment analysis** 
7. Print formatted tables to the terminal


## Running Unit Tests

To run all unit tests:

    python tests.py

This verifies: 
- Google Drive Masters data downloading 
- Utility function behavior 
- Basic model training


## Output Files

After execution, the following files are generated:

-   `masters_2026_predicted.csv` (LASSO-linear model predictions)
-   `masters_2026_predicted_XGB.csv` (XGBoost model predictions)
-   `pgaclubtracker_witb_all_players.csv` (WITB scraping output)


## Prediction Models (Simple Explanation)

This project produces **two independent prediction models**:

**1. LASSO-Linear Model (`masters_2026_predicted.csv`)**\
A LASSO regression is trained on historical Masters data to learn how each strokes-gained category affects scoring. The results are combined into a single skill score and calibrated with a simple linear model.
This calibrated model is applied to 2025 season statistics to generate 2026 predictions.\
This model is interpretable and explains how each skill impacts performance.

**2. XGBoost Model (`masters_2026_predicted_XGB.csv`)**\
A nonlinear XGBoost regression is trained directly on historical Masters data. It captures complex, non-linear relationships and is applieddirectly to season-long statistics.\
This model focuses on **maximum predictive accuracy**.

Both models use the same strokes-gained inputs, but the LASSO-linear model emphasizes **explainability**, while the XGBoost model emphasizes **prediction performance**.


## Environment Variables

This project does **not require any API keys or secrets**.\
Instead, a placeholder `.env.example` file is included to satisfy the project structure requirement.