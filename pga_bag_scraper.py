from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import csv

base_url = "https://www.pgaclubtracker.com"

def get_all_player_slugs() -> list[str]:
    slugs = set()
    page = 1

    while True:
        page_url = f"{base_url}/players?page={page}"
        print(f"Fetching player list page: {page_url}")
        resp = requests.get(page_url, timeout=15)
        if resp.status_code != 200:
            print(f"Stopping: got status {resp.status_code} on page {page}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        table = soup.find("table")
        if not table:
            print("No table found on this page, stopping.")
            break

        for a in table.find_all("a", href=True):
            href = a["href"]
            if not href.startswith("/players/"):
                continue
            if not href.endswith("-witb-whats-in-the-bag"):
                continue

            player_part = href.split("/players/", 1)[1]
            slug = player_part.replace("-witb-whats-in-the-bag", "")
            slugs.add(slug)

        next_link = soup.find("a", string=lambda s: s and "Next" in s)
        if not next_link:
            print("No Next link found, reached last page.")
            break

        page += 1
        time.sleep(1)

    return sorted(slugs)


def make_driver() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def scrape_witb(player_slug: str, driver: webdriver.Chrome):

    witb_url = f"{base_url}/players/{player_slug}-witb-whats-in-the-bag"
    print(f"Fetching WITB for {player_slug}: {witb_url}")
    driver.get(witb_url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    witb_table = None
    for table in soup.find_all("table"):
        header = table.find("thead")
        if not header:
            continue
        header_cells = [th.get_text(strip=True) for th in header.find_all("th")]
        if header_cells and header_cells[0] == "Club":
            witb_table = table
            break

    if witb_table is None:
        print(f"Could not find WITB table for {player_slug}")
        return []

    tbody = witb_table.find("tbody")
    if not tbody:
        print(f"WITB table found but no <tbody> for {player_slug}")
        return []

    results = []
    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 5:
            continue
        results.append({
            "club": cols[0].get_text(strip=True),
            "brand": cols[1].get_text(strip=True),
            "model": cols[2].get_text(strip=True),
            "loft_no": cols[3].get_text(strip=True),
            "shaft": cols[4].get_text(strip=True)
        })

    return results

def scrape_all_players_to_csv(output_csv: str = "pgaclubtracker_witb_all_players.csv"):
    slugs = get_all_player_slugs()
    print(f"Found {len(slugs)} players")

    driver = make_driver()
    all_rows = []

    try:
        for slug in slugs:
            clubs = scrape_witb(slug, driver)
            for c in clubs:
                all_rows.append({
                    "player_slug": slug,
                    "club": c["club"],
                    "brand": c["brand"],
                    "model": c["model"],
                    "loft_no": c["loft_no"],
                    "shaft": c["shaft"],
                })
    finally:
        driver.quit()

    fieldnames = ["player_slug", "club", "brand", "model", "loft_no", "shaft"]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Wrote {len(all_rows)} rows to {output_csv}")


if __name__ == "__main__":
    scrape_all_players_to_csv()
