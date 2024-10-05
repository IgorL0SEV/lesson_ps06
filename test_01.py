import requests
from bs4 import BeautifulSoup

url = 'https://'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.fins_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    cleaned_cols = [col.text.strip() for col in cols]

print(data)
