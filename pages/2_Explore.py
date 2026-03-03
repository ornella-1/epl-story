import streamlit as st
import altair as alt

from utils.io import (
    load_epl,
    prepare_season_performance,
    prepare_attacking_consistency,
    prepare_home_away
)

from charts.charts import (
    chart_season_performance,
    chart_attacking_consistency,
    chart_home_away
)

st.set_page_config(page_title="Explore", layout="wide")

st.title("Interactive Exploration")
st.write("Use the controls below to explore team performance across seasons.")


df = load_epl()


goal_summary = prepare_season_performance(df)
metric_df = prepare_attacking_consistency(df)
team_matches, team_summary = prepare_home_away(df)

team_dropdown = alt.selection_point(
    fields=["team"],
    bind=alt.binding_select(
        options=sorted(goal_summary["team"].unique()),
        name="Select team: "
    ),
    empty="all"
)


col1, col2 = st.columns(2)

with col1:
    st.subheader("Season-to-Season Ranking")
    st.altair_chart(
        chart_season_performance(goal_summary),
        use_container_width=True
    )

with col2:
    st.subheader("Attacking Consistency")
    st.altair_chart(
        chart_attacking_consistency(metric_df, team_dropdown),
        use_container_width=True
    )

st.subheader("Home vs Away Influence")
st.altair_chart(
    chart_home_away(team_summary, team_matches),
    use_container_width=True
)