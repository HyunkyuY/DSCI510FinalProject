import sqlite3
import csv
from tabulate import tabulate

from src.config import WITB_CSV


def load_csv_to_db(conn):
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS witb;")
    cur.execute(
        """
        CREATE TABLE witb (
            player_slug TEXT,
            club        TEXT,
            brand       TEXT,
            model       TEXT,
            loft_no     TEXT,
            shaft       TEXT
        );
        """
    )

    with open(WITB_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row.get("player_slug", ""),
                row.get("club", ""),
                row.get("brand", ""),
                row.get("model", ""),
                row.get("loft_no", ""),
                row.get("shaft", ""),
            )
            for row in reader
        ]

    cur.executemany(
        """
        INSERT INTO witb (player_slug, club, brand, model, loft_no, shaft)
        VALUES (?, ?, ?, ?, ?, ?);
        """,
        rows,
    )
    conn.commit()
    print(f"Loaded {len(rows)} rows into WITB.\n")


def print_section(title, conn, sql):
    print("=" * 80)
    print(title)
    print("=" * 80)

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    col_names = [d[0] for d in cur.description]

    print(tabulate(rows, headers=col_names, tablefmt="github"))
    print("\n")


def main():
    conn = sqlite3.connect(":memory:")
    load_csv_to_db(conn)

    # (rest of your queries unchanged...)
    # Most common brands, brand dominance, driver models, shafts, wedges, single-brand bags
    # ... keep your existing SQL sections here ...

    conn.close()


if __name__ == "__main__":
    main()
