from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
#=========================================================================================
# NASA Mars News
# def init browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # Mac Users : 
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    # Windowss Users :
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():

#   Create Dictionary
    mars_data ={}
#   <<scrap news>>
    browser = init_browser()

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

#   scrap news title
    news_titles=soup.find('div', class_='content_title')
    news_title=news_titles.text.strip()

#   scrap news body
    news_ps = soup.find('div', class_='article_teaser_body')
    news_p=news_ps.text.strip()

#   Store data in a dictionary
    
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

#   Quite the browser after scraping
    browser.quit()

#   <<Scrape Featured Image>>
    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

#   scrape feathure image link
    f_image_url=soup.find('article' , class_='carousel_item')['style']
    query_url=f_image_url.split("('")[1].split("')")[0]
    base_url='https://www.jpl.nasa.gov'
    featured_image_url=base_url + query_url

#   Store data in a dictionary
    mars_data["featured_image_url"] = featured_image_url

#   Quite the browser after scraping
    browser.quit()

#   <<Scrape Mars Weather>>
    browser = init_browser()

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

#   Scrape Mars Weather
    mars_w=soup.find('div', class_='js-tweet-text-container').find('p').text
    mars_weather=mars_w.split("Papic")[0]
    mars_data["mars_weather"] = mars_weather

#   Quite the browser after scraping
    browser.quit()

#   <<Scrape Mars Facts>>
    url= 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts=tables[0].rename(columns={0: 'Description', 1: 'Value'}).set_index('Description')
    mars_facts_html = mars_facts.to_html(index = True, header =True).replace('\n','').replace('right','left')
    mars_data["mars_facts_html"]=mars_facts_html


 #   <<Scrape Mars Hemisphere>>
    browser = init_browser()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

#   <<scrap Mars Hemisphere url>>
    mars_hemispheres = soup.find_all('div', class_ = 'item')
    base_url='https://astrogeology.usgs.gov'
    hemisphere_image_urls=[]

    for mars_hemisphere in mars_hemispheres:
        link = mars_hemisphere.find('a')
        href = link['href']
        browser.visit(base_url+href)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2',class_='title').text.split('Enhanced')[0]
        img_url = soup.find_all('li')[0].a['href']
        hemisphere_image_urls.append({'title':title,'img_url':img_url})
        browser.back()
    mars_data["hemisphere_image_urls"]=hemisphere_image_urls
#   Quite the browser after scraping
    browser.quit()   
    return mars_data
