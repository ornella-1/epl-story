import altair as alt

def chart_season_performance(goal_summary):
    team_dropdown = alt.selection_point(
        fields=["team"],
        bind=alt.binding_select(
            options=sorted(goal_summary["team"].unique()),
            name="Select team: "
        ),
        empty="all"
    )

    chart = (
        alt.Chart(goal_summary)
        .add_params(team_dropdown)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("season:N", title="Season"),
            y=alt.Y("rank:Q", sort="ascending", title="Rank (1 = Best)"),
            color=alt.condition(team_dropdown, "team:N", alt.value("lightgray")),
            opacity=alt.condition(team_dropdown, alt.value(1), alt.value(0.25)),
            detail="team:N",
            tooltip=["team", "season", "goal_difference", "rank"]
        )
        .properties(width=500, height=300)
    )

    return chart


def chart_attacking_consistency(metric_df, team_dropdown):
    metric_param = alt.param(
        value="goals",
        bind=alt.binding_select(
            options=["goals", "shots", "shots_on_target", "corners", "fouls"],
            name="Metric: "
        )
    )

    chart = (
        alt.Chart(metric_df)
        .add_params(metric_param)
        .transform_filter(team_dropdown)  \
        .transform_filter(alt.datum.metric == metric_param)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("matchweek:Q", title="Matchweek"),
            y=alt.Y("value:Q", title="Attacking Performance"),
            color=alt.Color(
                "season:N",
                title="Season",
                legend=alt.Legend(orient="top")
            ),
            tooltip=["team", "season", "matchweek", "value"]
        )
        .properties(width=500, height=300)
        .resolve_scale(color="shared")
    )

    return chart


def chart_home_away(team_summary, team_matches):
    brush = alt.selection_multi(fields=["team"], empty="all")

    scatter = (
        alt.Chart(team_summary)
        .mark_circle(size=120)
        .encode(
            x=alt.X("HomeGoals:Q", title="Total Home Goals"),
            y=alt.Y("AwayGoals:Q", title="Total Away Goals"),
            color=alt.Color("season:N", title="Season"),
            tooltip=["team", "season", "HomeGoals", "AwayGoals"],
            opacity=alt.condition(brush, alt.value(1), alt.value(0.2))
        )
        .add_params(brush)
        .properties(width=400, height=400, title="Home vs Away Goals")
    )

    detail = (
        alt.Chart(team_matches)
        .transform_filter(brush)
        .mark_bar()
        .encode(
            x=alt.X("matchweek:O", title="Matchweek"),
            y=alt.Y("goals:Q", title="Goals Scored"),
            color=alt.Color("venue:N", title="Venue"),
            tooltip=["team", "season", "venue", "matchweek", "goals"]
        )
        .properties(width=400, height=400, title="Match-Level Goals")
    )

    return scatter | detail

