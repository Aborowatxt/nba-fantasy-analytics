from src.analytics import (
    get_player_logs,
    calculate_fantasy_points,
    get_player_rankings,
    get_recent_performance,
    get_breakout_players
)


def main():

    # Retrieve data from SQLite
    df = get_player_logs()

    # Calculate fantasy points
    df = calculate_fantasy_points(df)

    print(f"Retrieved {len(df):,} player game records.")

    # Display top 10 fantasy players
    print("\nTOP 10 FANTASY PLAYERS")
    rankings = get_player_rankings(df)
    print(rankings.head(10).to_string(index=False))

    # Display recent performance
    print("\nRECENT PERFORMANCE")
    performance = get_recent_performance(df)
    print(performance.head(10).to_string(index=False))

    # Display breakout candidates
    print("\nBREAKOUT WATCHLIST")
    breakout = get_breakout_players(df)
    print(breakout.head(10).to_string(index=False))


if __name__ == "__main__":
    main()