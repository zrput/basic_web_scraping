import requests
from bs4 import BeautifulSoup
import csv

# get the HTML content of the page
response = requests.get('https://www.scrapethissite.com/pages/simple/')
# print(response.status_code)
# print(response.text)

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
countries = soup.find_all('div', class_='col-md-4 country')
#print(f'There are {len(countries)} countries on the page.')

# extract the required data
result = []
for block in countries:
    country_name = block.find('h3', class_='country-name').text.strip()
    capital = block.find('span', class_='country-capital').text.strip()
    population = block.find('span', class_='country-population').text.strip()
    area = block.find('span', class_='country-area').text.strip()
    result.append({
        'country': country_name,
        'capital': capital,
        'population': population,
        'area': area
    })

# for item in result:
#     print(f"country: {item['country']}, capital: {item['capital']}, population: {item['population']}, area: {item['area']}")


# write the data to a CSV file
with open('countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['country', 'capital', 'population', 'area']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in result:
        writer.writerow(item)