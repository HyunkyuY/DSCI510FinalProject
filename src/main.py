from src import golf_season_scraper
from src import pga_bag_scraper
from src import masters_pipeline
from src import witb_analysis

def main():
    # 1. Scrape strokes-gained season data
    golf_season_scraper.main()

    # 2. Scrape WITB data
    pga_bag_scraper.scrape_all_players_to_csv()

    # 3. Run Masters prediction models
    masters_pipeline.main()

    # 4. Run WITB equipment analysis
    witb_analysis.main()

if __name__ == "__main__":
    main()
