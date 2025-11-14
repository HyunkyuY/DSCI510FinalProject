# DSCI 510 Final Project: Masters Prediction & WITB Scraper

- A Jupyter notebook for predicting players' performance at the Masters tournament.
- A Python script (`pga_bag_scraper.py`) that scrapes WITB golf club data using Selenium + BeautifulSoup.

## Installation
Install all dependencies:
```
pip install -r requirements.txt
```
- Chrome + ChromeDriver are required for Selenium.

## Running the Notebook
```
jupyter notebook
```

## Running the Scraper
```
python scripts/pga_bag_scraper.py
```

To change the golfer being scraped, edit inside the script:
```
name = "max-homa"
```

