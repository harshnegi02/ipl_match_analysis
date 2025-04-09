import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title="IPL Match Analysis", layout="centered")

# Title
st.title("🏏 IPL Match Analysis Dashboard")

# Load datasets
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# Prepare match descriptions
matches['match_desc'] = matches['team1'] + " vs " + matches['team2'] + " (Match ID: " + matches['id'].astype(str) + ")"
match_desc = st.selectbox("Select a Match", matches['match_desc'].unique())

# Extract selected match ID
match_id = int(match_desc.split("Match ID: ")[-1].replace(")", ""))

# Filter match data
match_data = deliveries[deliveries['match_id'] == match_id]

# Split into innings
first_innings = match_data[match_data['inning'] == 1].copy()
second_innings = match_data[match_data['inning'] == 2].copy()

# Ball number and cumulative runs
first_innings['ball_no'] = range(1, len(first_innings) + 1)
first_innings['cum_runs'] = first_innings['total_runs'].cumsum()

second_innings['ball_no'] = range(1, len(second_innings) + 1)
second_innings['cum_runs'] = second_innings['total_runs'].cumsum()

# Plotting runs
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(first_innings['ball_no'], first_innings['cum_runs'], label="1st Innings", color='blue')
ax.plot(second_innings['ball_no'], second_innings['cum_runs'], label="2nd Innings", color='orange')
ax.set_xlabel("Ball Number")
ax.set_ylabel("Cumulative Runs")
ax.set_title("Run Progression per Innings")
ax.legend()
st.pyplot(fig)

# Calculate win prediction
target = first_innings['cum_runs'].iloc[-1]
current_score = second_innings['cum_runs'].iloc[-1]
balls_played = len(second_innings)

if current_score >= target:
    win_percent = 100
else:
    max_balls = 120
    run_rate_needed = (target - current_score) / (max_balls - balls_played + 1)
    current_rr = current_score / balls_played
    win_percent = min(100, max(0, (current_rr / run_rate_needed) * 100))

# Show prediction
st.markdown(f"### 📊 Win Prediction: `{round(win_percent, 2)}%` chance for the chasing team")

# Show winner
winner = matches[matches['id'] == match_id]['winner'].values[0]
st.success(f"🏆 Match Winner: **{winner}**")

