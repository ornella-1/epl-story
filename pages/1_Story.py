import streamlit as st
import altair as alt

from charts.charts import (
    chart_attacking_consistency_story,
    chart_season_performance,
    chart_attacking_consistency,
    chart_home_away,
    chart_referee
)

from utils.io import (
    load_epl,
    prepare_season_performance,
    prepare_attacking_consistency,
    prepare_home_away,
    prepare_referee_data
)


df = load_epl()

# 1. Season-to-Season Chart

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
st.write("How did teams' goal difference rankings change between seasons?")
st.altair_chart(chart_season_performance(goal_summary), use_container_width=True)
st.caption("The bump chart shows how the relative rankings of teams based on goal difference changed from the 2023-2024 season to the 2024-2025 season in the premier league. Each line represents a team, and the position on the y-axis indicates their rank (1 = best). The interactive dropdown allows you to highlight a specific team across both seasons.")
# 2. Attacking Consistency

metric_df = prepare_attacking_consistency(df)

st.header("Attacking Consistency Across Matchweeks")
st.write("How stable are teams’ attacking metrics across the season?")
st.altair_chart(chart_attacking_consistency_story(metric_df, team_dropdown), use_container_width=True)
st.caption("The line chart shows the attacking performance of teams across matchweeks for two seasons. The X-axis shows the matchweek number, while the Y-axis represents the value of the selected attacking metric(goals, shots, shots on target, corners, or fouls). The interactive dropdown allows the selection of the specific team to highlight its performance trajectory across matchweeks.")


# 3. Home vs Away Influence

team_matches, team_summary = prepare_home_away(df)

st.header("Home vs Away Influence")
st.write("Does being home or away influence the teams performance?")
st.altair_chart(chart_home_away(team_summary, team_matches), use_container_width=True)
st.caption("The left scatter plot compares total goals scored at home vs away for each team across the season. The right bar chart shows match-level goals for selected teams when you click on a point in the scatter plot. This allows you to see if certain teams have stronger home or away performances and how that varies across matches per each season.")
# Referee Influence

df_ref, ref_season = prepare_referee_data(df)

st.header("Referee Influence on Match Discipline")
st.write("How do different referees differ in their disciplinary tendencies and how does this affect performance?")
st.altair_chart(chart_referee(df_ref, ref_season), use_container_width=True)
st.caption("The left horizontal bar chart ranks referees based on the average number of cards they issue per match in a particular season. The right scatter plot shows the relationship between the number of cards given by each referee and the number of fouls committed in the match. The interactive dropdown allows you to select a specific season to see how referee tendencies differ")