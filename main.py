import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"  

response = requests.get(url)
if response.status_code == 200:
    print(response.text)
    