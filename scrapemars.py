# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager



# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# URLs of pages to be scraped
# Mars News URL
marsNewsURL = 'https://mars.nasa.gov/news/'
# Mars Facts URL
marsProfileURL = 'https://space-facts.com/mars/'
# Mars Hemisphere URL
marsHemisphereURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# Part 1
# Scrape the first news story (title and teaser) from https://mars.nasa.gov/news/
def getMarsNews(url):

    newsDict = {}
    browser.visit(url)
    newsHTML = browser.html
    soup = bs(newsHTML, 'html.parser')
    soupDiv = soup.find(class_="slide")
    soupNews = soupDiv.find_all('a')
    newsTitle = soupNews[1].get_text().strip()


    soupTeaser = soup.find(class_="article_teaser_body")
    newsPara = soupTeaser.get_text().strip()

    # These are used in mongo part
    # print("\n")
    # print(newsTitle)
    # print(newsPara)
    newsDict = {'title': newsTitle, 'teaser' : newsPara}
    return newsDict


# Part 2  
# Get the image of the day from https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html

def getMarsImageOTD():
    
    # URL of page to be scraped
    imageURL = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    imageBaseURL = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    browser.visit(imageURL)
    
    # Setup the browser
    featuredImageHTML = browser.html
    featuredImagesSoup = bs(featuredImageHTML, 'html.parser')
    
    # Find the partial image link
    soupDiv = featuredImagesSoup.find(class_="showimg fancybox-thumbs")
    partialImageURL = soupDiv['href']
    
    # Create the entire link
    featuredImageURL = imageBaseURL + partialImageURL
    browser.visit(featuredImageURL)
    # print("\n")
    # print(partialImageURL)
    # print(featuredImageURL)
    featuredImageURLDict = {'url': featuredImageURL}
    return(featuredImageURLDict)


# Part 3 
# Scrape Mars facts page https://space-facts.com/mars/ and scrape the Mars Planet Profile Table 

def marsFacts(url):
    browser.visit(url)

    marsProfileTables = pd.read_html(marsProfileURL)
    # marsProfileTables
    # 3 tables, but table 1 and 3 are identical

    df0 = marsProfileTables[0]
    df0.columns  =["Mars Facts",""]  # gets rid of 0 and 1 in header

    df1 = marsProfileTables[1]
    return df0, df1


# Part 4 
# Scrape the 4 hi-rez Mars Hemispheres images from 
# https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
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

# marsNews is the result for step 1
marsNews = getMarsNews(marsNewsURL)
print(f'NewsDict = {marsNews}')
print(marsNews.values())

# ------
# # imageOTDDict is the Dictionary result of step 2
# This is where the function gets called
imageOTDDict = getMarsImageOTD()
print(f'Image of the Day Dict = {imageOTDDict}')
# ------


# table1 and table2 are the dataframes from step 3

table1, table2 = marsFacts(marsProfileURL)
print(table1)
print('\n')
print(table2)
htmlTable1 = table1.to_html(index=False)
htmlTable2 = table2.to_html(index=False)



# hemiURLs are the dictionary items for the hi rez photos of mars
hemiURLs = getMarsHemiURLs(marsHemisphereURL)        
print(hemiURLs)