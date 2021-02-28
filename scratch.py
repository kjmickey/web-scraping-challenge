#dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager



# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



# Part 4 
# Scrape the 4 hi-rez Mars Hemispheres images from 
# https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

marsHemisphereURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

def getMarsHemiURLs(url):
    browser.visit(url)

    marsHemisphereHtml = browser.html
    marsHemisphereSoup = bs(marsHemisphereHtml, 'html.parser')

    hemisphereImageURLs = []
    foundLinks = browser.find_by_css('a.product-item h3')
    for item in range(len(foundLinks)):
        hemisphere = {}
    
        # Find Element
        browser.find_by_css("a.product-item h3")[item].click()
    
        # Find Sample Image Anchor Tag & Extract <href>
        sampleTag = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sampleTag["href"]
    
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        # Append Hemisphere Object to List
        hemisphereImageURLs.append(hemisphere)

        browser.back()
    return(hemisphereImageURLs)



def scrape():
    bigDict = []
    hemiURLs = getMarsHemiURLs(marsHemisphereURL)        
    # print(hemiURLs)
    return(hemiURLs)

bigDict = scrape()
print(f'\ntada! {bigDict}\n')