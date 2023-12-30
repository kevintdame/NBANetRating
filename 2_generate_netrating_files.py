import pandas as pd
from scipy.stats import percentileofscore
import os

# Function to calculate standard percentiles and round them
def calculate_percentiles(data_frame, column):
    return data_frame[column].apply(lambda x: round(percentileofscore(data_frame[column], x)))

# Function to calculate inverted percentiles for DRtg
def calculate_inverted_percentiles(data_frame, column):
    return 100 - calculate_percentiles(data_frame, column)

# Function to select players based on the new criteria
def select_players_new_criteria(team_data):
    team_data_copy = team_data.copy()
    
    # Convert 'GS' and 'MP' to float for consistent sorting
    team_data_copy['GS'] = team_data_copy['GS'].astype(float)
    team_data_copy['MP'] = team_data_copy['MP'].astype(float)

    # Select top 4 players that are not Centers
    non_centers = team_data_copy[team_data_copy['Pos'] != 'C'].sort_values(by=['GS', 'MP'], ascending=False).head(4)

    # Select the top Center
    center = team_data_copy[team_data_copy['Pos'] == 'C'].sort_values(by=['GS', 'MP'], ascending=False).head(1)

    # Combine the selected players
    selected_players = pd.concat([non_centers, center])

    # Remove the selected players from the data
    remaining_players = team_data_copy.drop(selected_players.index)

    # Select the next player with the most minutes played
    next_player = remaining_players.sort_values(by='MP', ascending=False).head(1)

    # Combine all selected players
    final_selection = pd.concat([selected_players, next_player])

    return final_selection


# Load the CSV file
file_path = 'nba_2024_per_poss_stats.csv' # Replace with your file path
data = pd.read_csv(file_path)

# Convert 'ORtg' and 'DRtg' to numeric types (float), handling non-numeric values
data['ORtg'] = pd.to_numeric(data['ORtg'], errors='coerce')
data['DRtg'] = pd.to_numeric(data['DRtg'], errors='coerce')

# Remove rows where 'ORtg' or 'DRtg' is NaN
data = data.dropna(subset=['ORtg', 'DRtg'])

# Calculate and round percentiles for ORtg and inverted percentiles for DRtg
data['ORtg_percentile'] = calculate_percentiles(data, 'ORtg')
data['DRtg_percentile'] = calculate_inverted_percentiles(data, 'DRtg')

# Compute Net Rating as ORtg - DRtg
data['Net_Rating'] = data['ORtg'] - data['DRtg']

# Calculate and round percentiles for Net Rating
data['Net_Rating_percentile'] = calculate_percentiles(data, 'Net_Rating')

# Group players by team
grouped_data = data.groupby('Tm')

# Create a folder to save the CSV files
output_folder = 'netratingcsvfiles/' # Replace with your desired output path
os.makedirs(output_folder, exist_ok=True)

# Process each team and save the files using the new selection criteria
for team, players in grouped_data:
    top_players = select_players_new_criteria(players)
    file_name = f"{team}_players.csv"
    file_path = os.path.join(output_folder, file_name)
    top_players.to_csv(file_path, index=False)

# End of script
