import pandas as pd

from src.transform import transform_player_logs


def test_data_validation(tmp_path, monkeypatch):
    """Verify duplicate and invalid record removal."""

    # Use temporary storage instead of real processed data
    monkeypatch.setattr(
        "src.transform.PROCESSED_DATA_DIR",
        tmp_path
    )

    valid_record = {
        "SEASON_YEAR": "2025-26",
        "PLAYER_ID": 1,
        "PLAYER_NAME": "Test Player",
        "TEAM_ID": 10,
        "TEAM_ABBREVIATION": "LAL",
        "GAME_ID": "001",
        "GAME_DATE": "2026-01-01",
        "MATCHUP": "LAL vs. BOS",
        "MIN": 30,
        "PTS": 25,
        "REB": 8,
        "AST": 5,
        "STL": 2,
        "BLK": 1,
        "TOV": 3,
        "FGM": 10,
        "FGA": 18,
        "FTM": 3,
        "FTA": 4,
        "FG3M": 2
    }

    duplicate = valid_record.copy()

    invalid = valid_record.copy()
    invalid["GAME_ID"] = "002"
    invalid["PTS"] = -10

    df = pd.DataFrame([
        valid_record,
        duplicate,
        invalid
    ])

    result = transform_player_logs(df)

    assert len(result) == 1
    assert result.iloc[0]["pts"] == 25
    assert result.iloc[0]["game_id"] == "001"
    assert len(result.columns) == 20