import streamlit as st
from utils.io import load_epl, prepare_season_performance, prepare_attacking_consistency, prepare_home_away, prepare_referee_data
from charts.charts import chart_season_performance, chart_attacking_consistency, chart_home_away, chart_referee

df = load_epl()
goal_summary = prepare_season_performance(df)

st.header("Season-to-Season Performance")
st.write("How did teams' goal difference rankings change between seasons?")

st.altair_chart(chart_season_performance(goal_summary), use_container_width=True)


goal_summary = prepare_season_performance(df)

team_dropdown = alt.selection_point(
    fields=["team"],
    bind=alt.binding_select(
        options=sorted(goal_summary["team"].unique()),
        name="Select team: "
    ),
    empty="all"
)

st.header("Season-to-Season Performance")
st.altair_chart(chart_season_performance(goal_summary), use_container_width=True)

metric_df = prepare_attacking_consistency(df)

st.header("Attacking Consistency Across Matchweeks")
st.write("How stable are teams’ attacking metrics across the season?")

st.altair_chart(
    chart_attacking_consistency(metric_df, team_dropdown),
    use_container_width=True
)


team_matches, team_summary = prepare_home_away(df)

st.header("Home vs Away Influence")
st.write("Do teams perform differently at home compared to away?")

st.altair_chart(
    chart_home_away(team_summary, team_matches),
    use_container_width=True
)


df_ref, ref_season = prepare_referee_data(df)

st.header("Referee Influence on Match Discipline")
st.write("How do referees differ in their disciplinary tendencies across seasons?")

st.altair_chart(
    chart_referee(df_ref, ref_season),
    use_container_width=True
)