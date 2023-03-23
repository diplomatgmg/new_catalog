import requests
from bs4 import BeautifulSoup as bs


page = requests.get('https://www.ozon.ru/')
soup = bs(page.content, 'html.parser')

print(soup.prettify())