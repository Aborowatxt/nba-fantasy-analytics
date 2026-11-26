# NBA Fantasy Analytics Platform

An end-to-end data engineering and analytics application that helps fantasy basketball managers evaluate player performance and make data-driven roster decisions.

## Features

- NBA player game data extraction through an external API.
- Local data caching, cleaning and validation.
- Relational SQLite database with four interconnected tables.
- Customizable fantasy scoring and player rankings.
- Last-5 and last-10-game performance analysis.
- Interactive player comparison and breakout watchlist.
- CSV exports, pipeline logging and automated testing.

## Tech Stack

Python, Pandas, SQL, SQLite, NBA API, Streamlit, Plotly, Pytest, Git.

## Data Pipeline

NBA API → Raw CSV → Data Transformation → SQLite → Analytics Engine → Streamlit

The pipeline processes 26,651 player game records across 582 players, 30 teams and 1,230 games from the 2025–26 NBA regular season.

## Project Structure

```
nba-fantasy-analytics/
├── data/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── analytics.py
├── sql/
│   └── schema.sql
├── tests/
├── main.py
├── app.py
├── run_analytics.py
├── requirements.txt
└── README.md
```

## Getting Started

Install dependencies:

```
pip install -r requirements.txt
```

Run the ETL pipeline:

```
python main.py
```

Launch the application:

```
streamlit run app.py
```

Run automated tests:

```
python -m pytest tests/ -v
```

## Data Source

NBA statistics retrieved through the unofficial `nba_api` Python library.

## Limitations

The application uses historical regular-season data. Breakout candidates are identified using recent performance trends rather than predictive modelling.