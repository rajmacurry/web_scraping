import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'

def get_and_parse_url(url):
    result=requests.get(url)
    soup=BeautifulSoup(result.text,'html.parser')
    return soup

soup = get_and_parse_url(url)
#print(soup.find("article",class_ = "product_pod").div.a.get('href'))   #for thr first link using find()
#this also works
#all_links = []
#for link in soup.findAll('article', class_= "product_pod"):
#    all_links.append(link.div.a.get('href'))
#print(all_links)

main_page_product_urls = [x.div.a.get('href') for x in soup.findAll('article',class_= "product_pod")]
print(main_page_product_urls)

#all these links are relative paths from the index page. So we need to remove index.html from  http://books.toscrape.com/index.html and add the respective links
def getBooksURLs(url):
    soup = get_and_parse_url(url)
    # remove the index.html part of the base url before returning the results
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])

print(getBooksURLs(url))
