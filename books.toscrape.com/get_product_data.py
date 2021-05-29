import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://books.toscrape.com/"

def get_and_parse_url(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'html.parser')
    return soup


pages_urls = [url]

soup = get_and_parse_url(pages_urls[0])

while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
    # get the new complete url by adding the fetched URL to the base URL (and removing the .html part of the base URL)
    new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")

    # add the URL to the list
    pages_urls.append(new_url)

    # parse the next page
    soup = get_and_parse_url(new_url)


def getBooksURLs(url):
    soup = get_and_parse_url(url)
    # remove the index.html part of the base url before returning the results
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])


booksURLs = []
for page in pages_urls:
    booksURLs.extend(getBooksURLs(page))

names = []
prices = []
nb_in_stock = []
img_urls = []
categories = []
ratings = []

# scrape data for every book URL: this may take some time
for url in booksURLs:
    soup = get_and_parse_url(url)
    # product name
    names.append(soup.find("div", class_=re.compile("product_main")).h1.text)
    # product price
    prices.append(soup.find("p", class_="price_color").text[2:])  # get rid of the pound sign
    # number of available products
    nb_in_stock.append(
        re.sub("[^0-9]", "", soup.find("p", class_="instock availability").text))  # get rid of non numerical characters
    # image url
    img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))
    # product category
    categories.append(soup.find("a", href=re.compile("../category/books/")).get("href").split("/")[3])
    # ratings
    ratings.append(soup.find("p", class_=re.compile("star-rating")).get("class")[1])



scraped_data = pd.DataFrame(
    {'name': names, 'price': prices, 'nb_in_stock': nb_in_stock, "url_img": img_urls, "product_category": categories,
     "rating": ratings})
print(scraped_data.head())

