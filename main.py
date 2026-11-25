from src.extract import extract_player_logs


def main():
    print("Starting NBA Fantasy Analytics Pipeline...")

    # Extract NBA player game logs
    df = extract_player_logs()

    # Inspect the extracted data
    print("\nData preview:")
    print(df.head())

    print("\nDataset dimensions:")
    print(df.shape)

    print("\nAvailable columns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()