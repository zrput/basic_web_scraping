import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.scrapethissite.com/pages/forms/'
page_number = 1
result = []

while True:
    url = f'{base_url}?page_num={page_number}&per_page=100'
    print(f'Fetching page {url}...')
    # get the HTML content of the page
    response = requests.get(url)
    # check if the request was successful
    if response.status_code != 200:
        break
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # find the table containing the data
    table = soup.find('table', class_='table')
    # find all rows in the table
    rows = table.find_all('tr', class_='team')

    # if no rows are found, we have reached the end of the pagination
    if not rows:
        print(f"No more data found {page_number}, ending pagination.")
        break

    # extract the required data from each row
    for row in rows:
        team_name = row.find('td', class_='name').get_text(strip=True)
        year = row.find('td', class_='year').get_text(strip=True)
        wins = row.find('td', class_='wins').get_text(strip=True)
        losses = row.find('td', class_='losses').get_text(strip=True)
        ot_losses = row.find('td', class_='ot-losses').get_text(strip=True)
        win_pct = row.find('td', class_='pct').get_text(strip=True)
        goals_for = row.find('td', class_='gf').get_text(strip=True)
        goals_against = row.find('td', class_='ga').get_text(strip=True)
        diff = row.find('td', class_='diff').get_text(strip=True)
        result.append({
            'team_name': team_name,
            'year': year,
            'wins': wins,
            'losses': losses,
            'ot_losses': ot_losses,
            'win_pct': win_pct,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'diff': diff
        })
    
    page_number += 1

# write the data to a CSV file
with open('teams.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['team_name', 'year', 'wins', 'losses', 'ot_losses', 'win_pct', 'goals_for', 'goals_against', 'diff']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in result:
        writer.writerow(item)

print(f'Total records fetched: {len(result)}')