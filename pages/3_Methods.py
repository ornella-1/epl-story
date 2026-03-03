import streamlit as st

st.title("Methods & Limitations")

st.header("Data Sources and Preprocessing")
st.write("""
This project uses two match-level datasets covering the 2023–24 and 2024–25 Premier League seasons. 
After loading the CSV files, dates were parsed using day-first formatting and the two seasons were 
combined into a single dataframe. Additional preprocessing steps included:

- labeling each match with its season
- converting home/away rows into a long format for team-level analysis
- computing goals for and against for each team
- generating matchweek counters within each season
- aggregating goals, shots, shots on target, corners, and fouls
- computing goal difference and ranking teams within each season

These transformations produced clean, team-season and team-match tables used across all charts.
""")

st.header("Visualization Design Choices")
st.write("""
The bump chart was chosen to show how teams' goal-difference rankings changed between seasons. 
It emphasizes relative movement and allows readers to compare trajectories across teams.

The attacking consistency chart uses a line plot with matchweek on the x-axis to highlight temporal 
patterns. A metric selector enables exploration of goals, shots, shots on target, corners, and fouls, 
revealing different dimensions of attacking performance.

The home vs away visualization combines a scatter plot and a match-level bar chart. The scatter plot 
summarizes total home and away goals, while the bar chart reveals match-level patterns when teams are 
selected. This overview + detail structure supports deeper interpretation.
""")

st.header("Interaction Design")
st.write("""
Interactive elements were added to support reader-driven exploration. A team dropdown links multiple 
charts, allowing readers to follow a single team across views. The metric selector enables comparison 
across different attacking indicators. A brush selection in the home/away chart reveals match-level 
details for selected teams. The Explore page consolidates these interactions into a single dashboard 
for open-ended investigation.
""")

st.header("Limitations")
st.write("""
The analysis is based on only two seasons of Premier League data, which limits generalizability. 
Because the data is observational, no causal claims can be made about the relationships between 
performance metrics. Goal difference is a useful but incomplete measure of team quality, and match 
outcomes are influenced by factors not captured in the dataset, such as injuries, tactics, and 
strength of schedule. Home and away effects may also be confounded by opponent difficulty.
""")