import requests
from bs4 import BeautifulSoup
import re

url='https://books.toscrape.com/'

def get_and_parse_url(url):
    result=requests.get(url)
    soup = BeautifulSoup(result.text,'html.parser')
    return soup

soup = get_and_parse_url(url)
main_url = url
categories_url = [main_url + x.get('href') for x in soup.find_all('a', href = re.compile('catalogue/category/books'))]
categories_url = categories_url[1:]

print(categories_url)
