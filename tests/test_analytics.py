import pandas as pd

from src.analytics import (
    calculate_fantasy_points,
    get_player_rankings,
    get_recent_performance
)


def test_fantasy_scoring():
    """Verify that custom fantasy scoring is correct."""

    df = pd.DataFrame({
        "pts": [20],
        "reb": [10],
        "ast": [5]
    })

    weights = {
        "pts": 1,
        "reb": 1,
        "ast": 2
    }

    result = calculate_fantasy_points(df, weights)

    assert result["fantasy_points"].iloc[0] == 40


def test_player_rankings():
    """Verify rankings and minimum-games filtering."""

    df = pd.DataFrame({
        "player_id": [1, 1, 2],
        "player_name": ["Player A", "Player A", "Player B"],
        "game_id": ["001", "002", "001"],
        "fantasy_points": [40, 60, 80],
        "pts": [20, 30, 40],
        "reb": [5, 10, 8],
        "ast": [5, 5, 5]
    })

    result = get_player_rankings(df, min_games=2)

    assert len(result) == 1
    assert result.iloc[0]["player_name"] == "Player A"
    assert result.iloc[0]["fantasy_ppg"] == 50
    assert result.iloc[0]["rank"] == 1


def test_recent_performance():
    """Verify recent-game averages and trends."""

    df = pd.DataFrame({
        "player_id": [1] * 10,
        "player_name": ["Player A"] * 10,
        "game_id": [str(i) for i in range(10)],
        "game_date": pd.date_range("2026-01-01", periods=10),
        "fantasy_points": [20] * 5 + [40] * 5,
        "pts": [10] * 10,
        "reb": [5] * 10,
        "ast": [5] * 10
    })

    result = get_recent_performance(df, min_games=10)

    assert result.iloc[0]["fantasy_ppg"] == 30
    assert result.iloc[0]["last_5_avg"] == 40
    assert result.iloc[0]["last_10_avg"] == 30
    assert result.iloc[0]["trend"] == 10