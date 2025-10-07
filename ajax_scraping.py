import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.scrapethissite.com/pages/ajax-javascript/'
result = []
year = 2010

while True:
    url = f'{base_url}?ajax=true&year={year}'
    response = requests.get(url)
    print(f'Fetching data from {url}...')
    if response.status_code != 200:
        break
    data = response.json()
    if not data:
        print(f"No more data found for year {year}, ending.")
        break
    result.extend(data)

    year += 1

with open('Film.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'year', 'awards', 'nominations', 'best_picture']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in result:
            writer.writerow(item)

print("Done...")