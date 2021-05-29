import requests
from bs4 import BeautifulSoup
import re

url = 'https://books.toscrape.com/'

def get_and_parse_url(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'html.parser')
    return soup


# store all the results into a list
pages_urls = [url]

soup = get_and_parse_url(pages_urls[0])

# while we get two matches, this means that the webpage contains a 'previous' and a 'next' button
# if there is only one button, this means that we are either on the first page or on the last page
# we stop when we get to the last page

while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
    # get the new complete url by adding the fetched URL to the base URL (and removing the .html part of the base URL)
    new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")

    # add the URL to the list
    pages_urls.append(new_url)

    # parse the next page
    soup = get_and_parse_url(new_url)

print(str(len(pages_urls)) + " fetched URLs")
print("Some examples:")
print(pages_urls[:5])

# we could iterate until we get to a page that doesnt exist ie 51 //200 means valid 404 means not existent
new_page = "https://books.toscrape.com/catalogue/page-1.html"
while requests.get(new_page).status_code == 200:
    pages_urls.append(new_page)
    new_page = pages_urls[-1].split("-")[0] + "-" + str(int(pages_urls[-1].split("-")[1].split(".")[0]) + 1) + ".html"

print(str(len(pages_urls)) + " fetched URLs")
print("Some examples:")
print(pages_urls[:5])

