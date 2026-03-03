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


def chart_attacking_consistency(metric_df, selected_team, selected_metric):

    filtered_df = metric_df[
        (metric_df["team"] == selected_team) &
        (metric_df["metric"] == selected_metric)
    ]

    chart = (
        alt.Chart(filtered_df)
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



def chart_referee(df, ref_season):
    global_brush = alt.selection_interval(name="MatchBrush")

    season_sel = alt.selection_point(
        fields=["season"],
        bind=alt.binding_select(options=sorted(df["season"].unique())),
        name="Season"
    )

    ref_sel = alt.selection_point(
        fields=["Referee"],
        on="click",
        clear="dblclick",
        name="Referee"
    )


    ref_chart = (
        alt.Chart(ref_season)
        .add_params(season_sel, ref_sel)
        .transform_filter(season_sel)
        .mark_bar()
        .encode(
            y=alt.Y("Referee:N", sort="-x", title="Referee"),
            x=alt.X("AvgCards:Q", title="Avg Cards per Match"),
            color=alt.condition(ref_sel, alt.value("#d62728"), alt.value("#1f77b4")),
            opacity=alt.condition(global_brush, alt.value(1), alt.value(0.3)),
            tooltip=[
                "Referee:N",
                alt.Tooltip("AvgCards:Q", format=".2f"),
                alt.Tooltip("AvgFouls:Q", format=".2f"),
                alt.Tooltip("AvgYellows:Q", format=".2f"),
                alt.Tooltip("AvgReds:Q", format=".2f"),
            ],
        )
        .properties(width=350, height=400, title="Referees Ranked by Avg Cards")
    )

    match_chart = (
        alt.Chart(df)
        .transform_filter(season_sel)
        .transform_filter(ref_sel)
        .add_params(global_brush)
        .mark_circle(size=70, opacity=0.7)
        .encode(
            x=alt.X("Fouls:Q", title="Fouls in Match"),
            y=alt.Y("Cards:Q", title="Cards in Match"),
            color=alt.condition(ref_sel, "Referee:N", alt.value("lightgray")),
            tooltip=[
                "Date:T", "HomeTeam", "AwayTeam",
                "Referee", "Fouls", "Yellows", "Reds", "Cards"
            ]
        )
        .properties(width=400, height=400, title="Match-Level Disciplinary Decisions")
    )

    return ref_chart | match_chart