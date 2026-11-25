import sqlite3
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "nba_fantasy.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def load_player_logs(df):
    """Load cleaned NBA data into a relational database."""

    print("\nStarting database load...")

    df = df.copy()

    # Convert dates into SQLite-compatible strings
    df["game_date"] = df["game_date"].dt.strftime("%Y-%m-%d")

    # Separate the dataset into four tables
    players = df[
        ["player_id", "player_name"]
    ].drop_duplicates(subset=["player_id"])

    teams = df[
        ["team_id", "team_abbreviation"]
    ].drop_duplicates(subset=["team_id"])

    games = df[
        ["game_id", "game_date", "season_year"]
    ].drop_duplicates(subset=["game_id"])

    game_logs = df.drop(columns=[
        "player_name",
        "team_abbreviation",
        "game_date",
        "season_year"
    ])

    tables = {
        "players": players,
        "teams": teams,
        "games": games,
        "player_game_logs": game_logs
    }

    conn = sqlite3.connect(DB_PATH)

    try:
        # Enable foreign key enforcement
        conn.execute("PRAGMA foreign_keys = ON")

        # Create database tables
        conn.executescript(SCHEMA_PATH.read_text())

        # Load all tables within one transaction
        with conn:

            for table_name, data in tables.items():

                columns = ", ".join(data.columns)
                placeholders = ", ".join(
                    ["?"] * len(data.columns)
                )

                query = (
                    f"INSERT OR REPLACE INTO {table_name} "
                    f"({columns}) VALUES ({placeholders})"
                )

                conn.executemany(
                    query,
                    data.itertuples(index=False, name=None)
                )

                print(f"Loaded {len(data):,} records into {table_name}")

        print("Database load completed.")

        # Verify database record counts
        for table_name in tables:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            print(f"{table_name}: {count:,} records")

    finally:
        conn.close()