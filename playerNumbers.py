import requests
from bs4 import BeautifulSoup
import csv

# The URL of the site to scrape
url = "https://www.espn.com/nba/team/roster/_/name/bos/boston-celtics"

# Make a request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Initialize BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table with player data
    table = soup.find('table', class_='Table')

    # Initialize a list to store player data
    players = []

    # Loop through the table rows and grab data
    for row in table.find_all('tr', class_='Table__TR'):
        cols = row.find_all('td')
        if cols:
            player_name_and_number = cols[1].text.split()  # Name and number are together
            player_name = ' '.join(player_name_and_number[:-1])  # All but the last element
            player_number = player_name_and_number[-1]  # The last element
            players.append({'name': player_name, 'number': player_number})
    
    # Write player data to CSV file
    with open('celtics_players.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'number'])
        writer.writeheader()
        for player in players:
            writer.writerow(player)

    print('Finished writing player data to celtics_players.csv')
else:
    print(f"Failed to retrieve data, status code: {response.status_code}")
