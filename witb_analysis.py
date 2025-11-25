import sqlite3
import csv
from tabulate import tabulate

CSV_PATH = "pgaclubtracker_witb_all_players.csv"

def load_csv_to_db(conn):
    cur = conn.cursor()

    # Drop & create table
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

    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
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
        "INSERT INTO witb (player_slug, club, brand, model, loft_no, shaft) VALUES (?, ?, ?, ?, ?, ?);",
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

    # Most common brands across the entire bag
    print_section(
        "Most Common Brands Across Entire Bag",
        conn,
        """
        SELECT brand, COUNT(*) AS count
        FROM witb
        WHERE brand <> ''
        GROUP BY brand
        ORDER BY count DESC
        LIMIT 20;
        """
    )

    # Brand dominance by category (Driver/Wood/Hybrid/Iron/Wedge/Putter)
    print_section(
        "Brand Dominance by Category",
        conn,
        """
        WITH categorized AS (
            SELECT
                brand,
                CASE
                    WHEN LOWER(club) LIKE '%driver%' THEN 'Driver'
                    WHEN LOWER(club) LIKE '%wood%' OR LOWER(club) LIKE '%fw%' THEN 'Wood'
                    WHEN LOWER(club) LIKE '%hybrid%' OR LOWER(club) LIKE '%rescue%' THEN 'Hybrid'
                    WHEN LOWER(club) LIKE '%iron%' THEN 'Iron'
                    WHEN LOWER(club) LIKE '%wedge%' THEN 'Wedge'
                    WHEN LOWER(club) LIKE '%putter%' THEN 'Putter'
                    ELSE 'Other'
                END AS category
            FROM witb
            WHERE brand <> ''
        )
        SELECT category, brand, COUNT(*) AS count
        FROM categorized
        WHERE category <> 'Other'
        GROUP BY category, brand
        ORDER BY category, count DESC;
        """
    )

    # Most popular driver models
    print_section(
        "Most Popular Driver Models",
        conn,
        """
        SELECT brand, model, COUNT(*) AS count
        FROM witb
        WHERE LOWER(club) LIKE '%driver%'
        GROUP BY brand, model
        ORDER BY count DESC, brand, model
        LIMIT 20;
        """
    )

    # Most common shaft brands
    print_section(
        "Most Common Shaft Brands",
        conn,
        """
        WITH shaft_brand AS (
        SELECT
            CASE
                WHEN shaft = '' THEN ''
                WHEN INSTR(shaft, ' ') = 0 THEN shaft
                ELSE SUBSTR(shaft, 1, INSTR(shaft, ' ') - 1)
            END AS shaft_brand
        FROM witb
        )
        SELECT shaft_brand, COUNT(*) AS count
        FROM shaft_brand
        WHERE shaft_brand <> ''
        GROUP BY shaft_brand
        ORDER BY count DESC
        LIMIT 20;
        """
    )

    # Most common wedge models
    print_section(
        "Most Common Wedge Models",
        conn,
        """
        SELECT brand, model, COUNT(*) AS count
        FROM witb
        WHERE LOWER(club) LIKE '%wedge%'
        GROUP BY brand, model
        ORDER BY count DESC
        LIMIT 20;
        """
    )

    # Players with a single-brand bag
    print_section(
        "Players With Single-Brand Bags",
        conn,
        """
        WITH per_player AS (
            SELECT player_slug, COUNT(DISTINCT brand) AS n_brands
            FROM witb
            WHERE brand <> ''
            GROUP BY player_slug
        )
        SELECT player_slug
        FROM per_player
        WHERE n_brands = 1
        ORDER BY player_slug;
        """
    )

    conn.close()


if __name__ == "__main__":
    main()
