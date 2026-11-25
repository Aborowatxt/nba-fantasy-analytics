import streamlit as st
import plotly.express as px

from src.analytics import (
    DEFAULT_WEIGHTS,
    get_player_logs,
    calculate_fantasy_points,
    get_player_rankings,
    get_recent_performance,
    get_breakout_players
)

# Configure the application
st.set_page_config(
    page_title="NBA Fantasy Analytics",
    page_icon="🏀",
    layout="wide"
)

st.title("🏀 NBA Fantasy Analytics")
st.caption("2025–26 NBA Regular Season")

# Cache database queries to improve performance
@st.cache_data
def load_data():
    return get_player_logs()


# Retrieve data from SQLite
raw_df = load_data()

# Sidebar configuration
st.sidebar.header("Fantasy Settings")

min_games = st.sidebar.slider(
    "Minimum games played",
    min_value=10,
    max_value=82,
    value=15
)

st.sidebar.subheader("Scoring Weights")

# Allow users to customize their league scoring
weights = {}

for stat, default_weight in DEFAULT_WEIGHTS.items():

    weights[stat] = st.sidebar.number_input(
        label=stat.upper(),
        value=float(default_weight),
        step=0.5
    )

# Calculate fantasy points using selected weights
df = calculate_fantasy_points(raw_df, weights)

# Generate player rankings
rankings = get_player_rankings(df, min_games)

# Display dataset metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Players",
    df["player_id"].nunique()
)

col2.metric(
    "Teams",
    df["team_id"].nunique()
)

col3.metric(
    "Games",
    f"{df['game_id'].nunique():,}"
)

col4.metric(
    "Game Records",
    f"{len(df):,}"
)

st.divider()

# Create application tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Player Rankings",
    "Recent Performance",
    "Player Comparison",
    "Breakout Watchlist"
])

with tab1:

    st.header("Fantasy Player Rankings")

    # Allow users to search for players
    search = st.text_input(
        "Search for a player",
        placeholder="Enter player name..."
    )

    filtered_rankings = rankings[
        rankings["player_name"].str.contains(
            search,
            case=False,
            regex=False
        )
    ]

    # Visualize the top 10 matching players
    fig = px.bar(
        filtered_rankings.head(10),
        x="fantasy_ppg",
        y="player_name",
        orientation="h",
        title="Top Fantasy Players",
        labels={
            "fantasy_ppg": "Fantasy Points Per Game",
            "player_name": "Player"
        }
    )

    fig.update_layout(
        yaxis={"autorange": "reversed"}
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display the complete rankings table
    st.dataframe(
        filtered_rankings.drop(columns=["player_id"]),
        use_container_width=True,
        hide_index=True
    )

    # Export rankings
    st.download_button(
        label="Download Rankings CSV",
        data=filtered_rankings.to_csv(index=False),
        file_name="fantasy_rankings.csv",
        mime="text/csv"
    )

with tab2:

    st.header("Recent Player Performance")

    st.caption(
        "Compare season averages with the final 5 and 10 games."
    )

    performance = get_recent_performance(df, min_games)

    # Select a performance metric
    metric = st.selectbox(
        "Rank players by",
        options=["fantasy_ppg", "last_5_avg", "last_10_avg", "trend"],
        format_func=lambda x: {
            "fantasy_ppg": "Season Average",
            "last_5_avg": "Last 5 Games",
            "last_10_avg": "Last 10 Games",
            "trend": "Performance Improvement"
        }[x]
    )

    # Sort players by selected metric
    performance = performance.sort_values(
        metric, ascending=False
    )

    # Compare season and recent averages
    fig = px.bar(
        performance.head(10),
        x="player_name",
        y=["fantasy_ppg", "last_5_avg", "last_10_avg"],
        barmode="group",
        title="Season vs Recent Performance",
        labels={
            "player_name": "Player",
            "value": "Fantasy Points",
            "variable": "Period"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        performance.drop(columns=["player_id"]),
        use_container_width=True,
        hide_index=True
    )

    with tab3:

        st.header("Compare Players")

        # Create unique player selection options
        players = (
            df[["player_id", "player_name"]]
            .drop_duplicates(subset=["player_id"])
            .sort_values("player_name")
        )

        player_names = dict(
            zip(players["player_id"], players["player_name"])
        )

        player_ids = players["player_id"].tolist()

        col1, col2 = st.columns(2)

        player_1 = col1.selectbox(
            "Select first player",
            player_ids,
            format_func=lambda x: player_names[x]
        )

        player_2 = col2.selectbox(
            "Select second player",
            player_ids,
            index=1,
            format_func=lambda x: player_names[x]
        )

        if player_1 == player_2:

            st.warning("Please select two different players.")

        else:

            # Retrieve selected player records
            comparison = df[
                df["player_id"].isin([player_1, player_2])
            ].copy()

            # Calculate summary statistics
            summary = get_recent_performance(
                comparison, min_games=1
            )

            st.subheader("Performance Summary")

            st.dataframe(
                summary.drop(columns=["player_id", "rank"]),
                use_container_width=True,
                hide_index=True
            )

            # Visualize individual game performance
            comparison = comparison.sort_values("game_date")

            fig = px.line(
                comparison,
                x="game_date",
                y="fantasy_points",
                color="player_name",
                markers=True,
                title="Fantasy Points Throughout the Season",
                labels={
                    "game_date": "Game Date",
                    "fantasy_points": "Fantasy Points",
                    "player_name": "Player"
                }
            )

            st.plotly_chart(fig, use_container_width=True)

            # Compare average basketball statistics
            fig2 = px.bar(
                summary,
                x="player_name",
                y=["points_ppg", "rebounds_ppg", "assists_ppg"],
                barmode="group",
                title="Average Player Statistics"
            )

            st.plotly_chart(fig2, use_container_width=True)

            with tab4:

                st.header("Breakout Watchlist")

                st.caption(
                    "Identify players outperforming their season averages."
                )

                col1, col2 = st.columns(2)

                breakout_min_games = col1.slider(
                    "Minimum games for breakout candidates",
                    min_value=10,
                    max_value=82,
                    value=15
                )

                min_improvement = col2.slider(
                    "Minimum fantasy point improvement",
                    min_value=0,
                    max_value=30,
                    value=5
                )

                # Identify improving players
                breakout = get_breakout_players(
                    df,
                    min_games=breakout_min_games,
                    min_improvement=min_improvement
                )

                st.metric(
                    "Breakout Candidates",
                    len(breakout)
                )

                # Visualize the biggest improvements
                fig = px.bar(
                    breakout.head(15),
                    x="trend",
                    y="player_name",
                    orientation="h",
                    color="trend",
                    color_continuous_scale="Greens",
                    title="Biggest Recent Performance Improvements",
                    labels={
                        "trend": "Fantasy Point Improvement",
                        "player_name": "Player"
                    }
                )

                fig.update_layout(
                    yaxis={"autorange": "reversed"}
                )

                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(
                    breakout.drop(columns=["player_id"]),
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    label="Download Breakout Watchlist",
                    data=breakout.to_csv(index=False),
                    file_name="breakout_watchlist.csv",
                    mime="text/csv"
                )

                st.info(
                    "Breakout candidates are based on historical performance "
                    "trends, not predictions of future performance."
                )