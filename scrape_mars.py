from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    listings["news_t"] = soup.find('div', class_='content_title').get_text()
    listings["news_p"] = soup.find('div', class_='article_teaser_body').get_text()
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = soup.find('a', class_='button fancybox')['data-fancybox-href']
    listings["image_url"] = 'https://www.jpl.nasa.gov' + featured_image_url

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet = soup.find_all('div', class_='js-tweet-text-container')
    for result in tweet:
        x = result.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        x = x.split(' ')
        if x[0] == 'Sol':
            listings["weather"] = result.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
            break


    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['', 'value']
    df.set_index('', inplace=True)

    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    listings["table"] =  html_table

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    lst = []

    results = soup.find_all('div', class_='item')
    for result in results:
        link_text = result.find('h3').text
    #     print(link_text)
    #     browser.click_link_by_partial_text(link_text)
    #     img_url = soup.find('img', class_='wide-large')['src']
        lst.append({'title':link_text})
    #     browser.back()

    listings["hemisphere"] = lst

    return listings
