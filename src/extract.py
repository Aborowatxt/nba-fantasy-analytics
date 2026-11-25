from pathlib import Path
from nba_api.stats.endpoints import playergamelogs

#Where raw NBA data will be stored
RAW_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def extract_player_logs(season="2025-26"):
    """Extract NBA player game logs and save them locally."""

    print(f"Extracting NBA data for the {season} season...")

    # Request regular season statistics from the NBA API
    response = playergamelogs.PlayerGameLogs(
        season_nullable=season,
        season_type_nullable="Regular Season",
        timeout=60
    )

    # Convert the API response into a DataFrame
    df = response.get_data_frames()[0]

    # Ensure the raw data directory exists
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save the original data as a CSV file
    file_path = RAW_DATA_DIR / f"player_logs_{season}.csv"
    df.to_csv(file_path, index=False)

    print(f"Successfully extracted {len(df):,} records.")
    print(f"Data saved to: {file_path}")

    return df