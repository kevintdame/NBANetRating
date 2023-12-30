import requests
import pandas as pd

# URL of the page
url = "https://www.basketball-reference.com/leagues/NBA_2024_per_poss.html"

# Fetch the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML table into a list of pandas DataFrames
    tables = pd.read_html(response.text)

    # Assuming the first table is the one we need
    stats_table = tables[0]

    # Clean up the table if necessary (e.g., handling multi-level columns)

    # Save the table as a CSV file
    stats_table.to_csv('nba_2024_per_poss_stats.csv', index=False)
else:
    print(f"Failed to retrieve web page. Status code: {response.status_code}")
