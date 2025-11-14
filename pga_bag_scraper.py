from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def scrape_witb(player_slug: str):
    url = f"https://www.pgaclubtracker.com/players/{player_slug}-witb-whats-in-the-bag"
    print(f"Fetching URL: {url}")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(2)  # small delay to ensure page fully loads

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # Find the WITB table by looking for a table whose header starts with "Club"
        witb_table = None
        tables = soup.find_all("table")
        for table in tables:
            thead = table.find("thead")
            if not thead:
                continue
            header_row = thead.find("tr")
            if not header_row:
                continue
            header_cells = [th.get_text(strip=True) for th in header_row.find_all("th")]
            if header_cells and header_cells[0] == "Club":
                witb_table = table
                break
        if witb_table is None:
            print("Could not find WITB table (no header starting with 'Club').")
            return []
        tbody = witb_table.find("tbody")
        if not tbody:
            print("WITB table found, but no <tbody> present.")
            return []
        results = []
        for row in tbody.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 5:
                continue
            club = cols[0].get_text(strip=True)
            brand = cols[1].get_text(strip=True)
            model = cols[2].get_text(strip=True)
            loft_no = cols[3].get_text(strip=True)
            shaft = cols[4].get_text(strip=True)
            if not club:
                continue
            results.append(
                {
                    "club": club,
                    "brand": brand,
                    "model": model,
                    "loft_no": loft_no,
                    "shaft": shaft,
                }
            )
        return results
    finally:
        driver.quit()


if __name__ == "__main__":
    name = "max-homa"
    clubs = scrape_witb(name)

    print(f"\nClubs for {name}:\n")
    for c in clubs:
        print(
            f"{c['club']}: {c['brand']} {c['model']} "
            f"({c['loft_no']}) – Shaft: {c['shaft']}"
        )
