import csv
import requests
from src.config import SEASON_YEAR, DATAGOLF_BASE_URL, SEASON_SG_CSV

def fetch_tour_list(tour: str, year: int) -> dict:
    url = f"{DATAGOLF_BASE_URL}/{tour.upper()}_{year}"
    resp = requests.put(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

def make_row(d, tour):
    name = f"{d['first']} {d['last']}".strip()
    return name, {
        "Player": name,
        "Rounds": d["rounds"],
        "Putt": d["putt"],
        "Arg": d["arg"],
        "App": d["app"],
        "OTT": d["ott"],
        "BS": d["bs"],
        "T2G": d["t2g"],
        "Tour": tour,
    }

def main():
    year = SEASON_YEAR
    combined = {}
    pga_players = set()
    liv_players = set()

    pga_data = fetch_tour_list("PGA", year)
    for d in pga_data["data"]:
        name, row = make_row(d, "PGA")
        combined[name] = row
        pga_players.add(name)

    liv_data = fetch_tour_list("LIV", year)
    for d in liv_data["data"]:
        name, row = make_row(d, "LIV")
        if name not in pga_players:
            combined[name] = row
            liv_players.add(name)

    euro_data = fetch_tour_list("EURO", year)
    euro_skipped = 0
    for d in euro_data["data"]:
        name, row = make_row(d, "EURO")
        if name in pga_players or name in liv_players:
            euro_skipped += 1
            continue
        combined[name] = row

    fieldnames = ["Player", "Rounds", "Putt", "Arg", "App", "OTT", "BS", "T2G", "Tour"]

    with open(SEASON_SG_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined.values())

    print(f"Saved {len(combined)} unique players to {SEASON_SG_CSV}")

if __name__ == "__main__":
    main()
