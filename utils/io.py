import pandas as pd

def prepare_season_performance(df):
    df_2324 = df[df["season"] == "2023-24"].copy()
    df_2425 = df[df["season"] == "2024-25"].copy()

    df_2324["season"] = "2023-24"
    df_2425["season"] = "2024-25"

    allseasons = pd.concat([df_2324, df_2425], ignore_index=True)

    long = allseasons.melt(
        id_vars=["season", "FTHG", "FTAG"],
        value_vars=["HomeTeam", "AwayTeam"],
        var_name="side",
        value_name="team"
    )

    long["goals_for"] = long.apply(
        lambda r: r["FTHG"] if r["side"] == "HomeTeam" else r["FTAG"],
        axis=1
    )
    long["goals_against"] = long.apply(
        lambda r: r["FTAG"] if r["side"] == "HomeTeam" else r["FTHG"],
        axis=1
    )

    summary = (
        long.groupby(["season", "team"], as_index=False)
            .agg(goals_for=("goals_for", "sum"),
                 goals_against=("goals_against", "sum"))
    )

    summary["goal_difference"] = summary["goals_for"] - summary["goals_against"]

    
    summary["rank"] = (
        summary.groupby("season")["goal_difference"]
        .rank(ascending=False, method="dense")
    )

    return summary

def prepare_attacking_consistency(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values("Date")

    home = df.copy()
    home["team"] = home["HomeTeam"]
    home["goals"] = home["FTHG"]
    home["shots"] = home["HS"]
    home["shots_on_target"] = home["HST"]
    home["corners"] = home["HC"]
    home["fouls"] = home["HF"]

    away = df.copy()
    away["team"] = away["AwayTeam"]
    away["goals"] = away["FTAG"]
    away["shots"] = away["AS"]
    away["shots_on_target"] = away["AST"]
    away["corners"] = away["AC"]
    away["fouls"] = away["AF"]

    team_matches = pd.concat([home, away], ignore_index=True)

    team_matches["matchweek"] = (
        team_matches.sort_values("Date")
        .groupby(["season", "team"])
        .cumcount() + 1
    )

    metric_df = team_matches.melt(
        id_vars=["season", "team", "matchweek"],
        value_vars=["goals", "shots", "shots_on_target", "corners", "fouls"],
        var_name="metric",
        value_name="value"
    )

    return metric_df

def prepare_home_away(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values("Date")

    home = df.copy()
    home["team"] = home["HomeTeam"]
    home["goals"] = home["FTHG"]
    home["venue"] = "Home"

    away = df.copy()
    away["team"] = away["AwayTeam"]
    away["goals"] = away["FTAG"]
    away["venue"] = "Away"

    team_matches = pd.concat([home, away], ignore_index=True)

    team_matches["matchweek"] = (
        team_matches.sort_values("Date")
        .groupby(["season", "team"])
        .cumcount() + 1
    )

    home_summary = (
        home.groupby(["season", "team"], as_index=False)
        .agg(HomeGoals=("goals", "sum"))
    )

    away_summary = (
        away.groupby(["season", "team"], as_index=False)
        .agg(AwayGoals=("goals", "sum"))
    )

    team_summary = pd.merge(home_summary, away_summary, on=["season", "team"])

    return team_matches, team_summary