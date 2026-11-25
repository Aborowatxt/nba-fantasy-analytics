CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_abbreviation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    game_id TEXT PRIMARY KEY,
    game_date TEXT NOT NULL,
    season_year TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS player_game_logs (
    player_id INTEGER NOT NULL,
    game_id TEXT NOT NULL,
    team_id INTEGER NOT NULL,
    matchup TEXT NOT NULL,
    min REAL NOT NULL,
    pts INTEGER NOT NULL,
    reb INTEGER NOT NULL,
    ast INTEGER NOT NULL,
    stl INTEGER NOT NULL,
    blk INTEGER NOT NULL,
    tov INTEGER NOT NULL,
    fgm INTEGER NOT NULL,
    fga INTEGER NOT NULL,
    ftm INTEGER NOT NULL,
    fta INTEGER NOT NULL,
    fg3m INTEGER NOT NULL,

    PRIMARY KEY (player_id, game_id),

    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE INDEX IF NOT EXISTS idx_game_logs_game
ON player_game_logs(game_id);

CREATE INDEX IF NOT EXISTS idx_game_logs_team
ON player_game_logs(team_id);