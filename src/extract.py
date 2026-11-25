from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import playergamelogs

RAW_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def extract_player_logs(season="2025-26", refresh=False):
    """Extract NBA data or reuse previously downloaded data."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = RAW_DATA_DIR / f"player_logs_{season}.csv"

    # Reuse existing data unless a refresh is requested
    if file_path.exists() and not refresh:
        print("Loading cached NBA data...")
        return pd.read_csv(file_path, dtype={"GAME_ID": str})

    print(f"Extracting NBA data for the {season} season...")

    # Request data from the NBA API
    response = playergamelogs.PlayerGameLogs(
        season_nullable=season,
        season_type_nullable="Regular Season",
        timeout=60
    )

    df = response.get_data_frames()[0]

    # Prevent an empty response from overwriting cached data
    if df.empty:
        raise ValueError("NBA API returned no records.")

    # Save the raw data locally
    df.to_csv(file_path, index=False)

    print(f"Successfully extracted {len(df):,} records.")
    print(f"Data saved to: {file_path}")

    return df