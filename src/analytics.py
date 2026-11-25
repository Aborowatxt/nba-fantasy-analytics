import sqlite3
import pandas as pd

from src.load import DB_PATH


def get_player_logs():
    """Retrieve player game statistics from the database."""

    query = """
        SELECT
            p.player_name,
            t.team_abbreviation,
            g.game_date,
            g.season_year,
            l.*
        FROM player_game_logs l
        JOIN players p ON l.player_id = p.player_id
        JOIN teams t ON l.team_id = t.team_id
        JOIN games g ON l.game_id = g.game_id
        ORDER BY g.game_date
    """

    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    df["game_date"] = pd.to_datetime(df["game_date"])

    return df


# Default fantasy scoring weights
DEFAULT_WEIGHTS = {
    "pts": 1,
    "reb": 1,
    "ast": 2,
    "stl": 4,
    "blk": 4,
    "tov": -2,
    "fgm": 2,
    "fga": -1,
    "ftm": 1,
    "fta": -1,
    "fg3m": 1
}


def calculate_fantasy_points(df, weights=None):
    """Calculate fantasy points using customizable weights."""

    if weights is None:
        weights = DEFAULT_WEIGHTS

    df = df.copy()

    df["fantasy_points"] = 0.0

    # Multiply each statistic by its scoring weight
    for stat, weight in weights.items():
        df["fantasy_points"] += df[stat] * weight

    return df

def get_player_rankings(df, min_games=10):
    """Rank players by average fantasy points per game."""

    rankings = df.groupby(
        ["player_id", "player_name"]
    ).agg(
        games_played=("game_id", "nunique"),
        total_fantasy_points=("fantasy_points", "sum"),
        fantasy_ppg=("fantasy_points", "mean"),
        points_ppg=("pts", "mean"),
        rebounds_ppg=("reb", "mean"),
        assists_ppg=("ast", "mean")
    ).reset_index()

    # Exclude players with insufficient games
    rankings = rankings[
        rankings["games_played"] >= min_games
    ]

    # Rank players from highest to lowest fantasy average
    rankings = rankings.sort_values(
        "fantasy_ppg", ascending=False
    ).reset_index(drop=True)

    rankings.insert(0, "rank", range(1, len(rankings) + 1))

    return rankings.round(2)


def get_recent_performance(df, min_games=10):
    """Compare recent fantasy performance with season averages."""

    df = df.sort_values(["game_date", "game_id"])

    # Calculate season averages
    season = get_player_rankings(df, min_games)

    # Calculate average fantasy points over the last 5 games
    last_5 = (
        df.groupby("player_id")
        .tail(5)
        .groupby("player_id")["fantasy_points"]
        .mean()
        .rename("last_5_avg")
    )

    # Calculate average fantasy points over the last 10 games
    last_10 = (
        df.groupby("player_id")
        .tail(10)
        .groupby("player_id")["fantasy_points"]
        .mean()
        .rename("last_10_avg")
    )

    # Combine season and recent performance
    performance = season.merge(last_5, on="player_id")
    performance = performance.merge(last_10, on="player_id")

    # Measure recent improvement or decline
    performance["trend"] = (
        performance["last_5_avg"] - performance["fantasy_ppg"]
    )

    return performance.round(2)


def get_breakout_players(df, min_games=15, min_improvement=5):
    """Identify players outperforming their season averages."""

    performance = get_recent_performance(df, min_games)

    # Filter players showing significant improvement
    breakout = performance[
        performance["trend"] >= min_improvement
    ]

    # Rank by recent improvement
    breakout = breakout.sort_values(
        "trend", ascending=False
    )

    return breakout.reset_index(drop=True)