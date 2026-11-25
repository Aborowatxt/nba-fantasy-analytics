from pathlib import Path

import pandas as pd

PROCESSED_DATA_DIR = (
    Path(__file__).resolve().parents[1] / "data" / "processed"
)


def transform_player_logs(df):
    """Clean and validate NBA player game logs."""

    print("\nStarting data transformation...")
    original_count = len(df)

    # Select columns relevant to fantasy basketball
    columns = [
        "SEASON_YEAR",
        "PLAYER_ID",
        "PLAYER_NAME",
        "TEAM_ID",
        "TEAM_ABBREVIATION",
        "GAME_ID",
        "GAME_DATE",
        "MATCHUP",
        "MIN",
        "PTS",
        "REB",
        "AST",
        "STL",
        "BLK",
        "TOV",
        "FGM",
        "FGA",
        "FTM",
        "FTA",
        "FG3M"
    ]

    # Verify that all required columns exist
    missing_columns = set(columns) - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    df = df[columns].copy()

    # Standardize column names
    df.columns = df.columns.str.lower()

    # Standardize game dates and identifiers
    df["game_date"] = pd.to_datetime(
        df["game_date"], errors="coerce"
    )

    df["game_id"] = df["game_id"].astype("string")

    # Convert statistical columns to numeric values
    numeric_columns = [
        "min", "pts", "reb", "ast", "stl",
        "blk", "tov", "fgm", "fga",
        "ftm", "fta", "fg3m"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # Remove records with missing required values
    df = df.dropna()

    # Remove invalid negative statistics
    df = df[(df[numeric_columns] >= 0).all(axis=1)]

    # Ensure one record per player per game
    df = df.drop_duplicates(
        subset=["player_id", "game_id"]
    )

    # Sort records chronologically for each player
    df = df.sort_values(
        ["player_id", "game_date"]
    ).reset_index(drop=True)

    # Save cleaned data
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        PROCESSED_DATA_DIR / "cleaned_player_logs.csv",
        index=False
    )

    print(f"Original records: {original_count:,}")
    print(f"Cleaned records: {len(df):,}")
    print(f"Removed records: {original_count - len(df):,}")
    print(f"Final columns: {len(df.columns)}")
    print("Data transformation completed.")

    return df