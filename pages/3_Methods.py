import streamlit as st

st.title("Methods & Limitations")

st.header("Data Sources and Preprocessing")
st.write("""
This project uses two match-level datasets covering the 2023–24 and 2024–25 Premier League seasons. 
After loading the CSV files, dates were parsed using day-first formatting and the two seasons were 
combined into a single dataframe. Additional preprocessing steps included:

- labeling each match with its season
- converted home/away rows into a long format for team-level analysis
- computing goals for and against for each team
- generating matchweek counters within each season
- aggregating goals, shots, shots on target, corners, and fouls
- computing goal difference and ranking teams within each season for and against each team

""")

st.header("Visualization Design Choices")
st.write("""
The bump chart was chosen to show how teams' goal-difference rankings changed between seasons. 
It gives the general picture of how the teams performed and how that changed across seasons.

The attacking consistency chart uses a line plot with matchweek on the x-axis to highlight changes over time. A metric selector enables exploration of goals, shots, shots on target, corners, and fouls, 
revealing different dimensions of attacking performance.

The home vs away visualization combines a scatter plot and a match-level bar chart. The scatter plot 
summarizes total home and away goals, while the bar chart reveals match-level patterns when teams are 
selected. This overview + detail structure supports deeper interpretation.
        
The referee influence chart uses a bar chart to rank referees by their average disciplinary decisions per match. A season selector allows readers to focus on specific seasons, while a referee selector enables exploration of individual referees' performance.
""")

st.header("Interaction Design")
st.write("""
Interactive elements were added to allow for exploration and condensation of data. A team dropdown links multiple 
charts, allowing readers to follow a single team across views. The metric selector enables comparison 
across different attacking indicators. And the brush selection in the home/away chart reveals match-level 
details for selected teams. The Explore page consolidates these interactions into a single dashboard 
for more side by side comparison.
""")

st.header("Limitations")
st.write("""
The analysis is based on only two seasons of Premier League data, which limits generalizability. 
We used goal difference to measure performance and though it is a useful tool, it's also an incomplete measure of team quality, and match 
outcomes as matches are influenced by factors not captured in the dataset strategies and 
strength of team members. The relationship between home and away effects is also not well shown as it can be confounded by opponent difficulty.
""")