from src.extract import extract_player_logs
from src.transform import transform_player_logs
from src.load import load_player_logs


def main():
    print("Starting NBA Fantasy Analytics Pipeline...")

    # Extract
    raw_df = extract_player_logs()

    # Transform
    cleaned_df = transform_player_logs(raw_df)

    # Load
    load_player_logs(cleaned_df)

    print("\nETL pipeline completed successfully!")


if __name__ == "__main__":
    main()