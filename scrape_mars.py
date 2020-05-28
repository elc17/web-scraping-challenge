# Import Dependencies
import os
import requests
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs

# Function for browser initialization
def init_browser():
    # Browser path
    executable_path = {'executable_path': 'chromedriver.exe'}

    # Return browser initialization
    return Browser('chrome', **executable_path, headless=False)

def init_driver():
    # Driver path
    driver_path = 'chromedriver.exe'
    
    # Return the driver initialization
    return webdriver.Chrome(executable_path=driver_path)

def init_soup(url):
    # Create a request to retrieve the page
    response = requests.get(url).text
    
    # Return a BeautifulSoup object
    return bs(response, 'lxml')

def scrape():
    
    # Dictionary to store the Mars data
    mars_data = {}
    
#--------------------------------------- LATEST NEWS -----------------------------------------

    # NASA Mars News Site url
    nasa_mars_url = 'https://mars.nasa.gov/news/'

    # Driver initialization
    driver = init_driver()
    
    # Open the url in the driver
    driver.get(nasa_mars_url)
    
    # Search for the first section called "grid gallery"
    section = driver.find_element_by_class_name('grid_gallery')
    
    # Search for the first element called "slide" which is where the news are
    element = section.find_element_by_class_name('slide')
    
    # Get the title and body text
    news_title = element.find_element_by_class_name('content_title').text
    news_body = element.find_element_by_class_name('article_teaser_body').text
    
    # Add key and value to the mars data dictionary
    mars_data['news_title'] = news_title
    mars_data['news_body'] = news_body

    # Close driver
    driver.quit()
    
#--------------------------------------- FEATURED IMAGE --------------------------------------

    # JPL featured space image url
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Browser initialization
    browser = init_browser()
    
    # Open the url in the browser
    browser.visit(jpl_url)
    
    # Click on the full image button to see it in medium size, use try to not abort in case of error
    try:
        browser.click_link_by_partial_text('FULL IMAGE')
        
    except:
        print('No featured image')

    # Click on the more info button to open the image's page, use try to not abort in case of error
    try:
        browser.click_link_by_partial_text('more info')
        
    except:
        print('The featured image has no extra information')
        
    # Select the current page's html information
    html = browser.html

    # Create a BeautifulSoup object
    jpl_soup = bs(html, 'lxml')

    # Look for the article section to search for the large-size image link
    featured_image = jpl_soup.find('article')

    # Look for the img section to extract the large-size image link (src)
    featured_image_src = featured_image.find('img')['src']

    # Join the JPL NASA link with the image's link to create its full url and store it in a variable
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_src

    # Add key and value to the mars data dictionary
    mars_data['featured_image'] = featured_image_url
    
    # Close browser
    browser.quit()
    
#-------------------------------------- HEMISPHERE IMAGES ------------------------------------
    
    # Mars planet profile
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Browser initialization
    browser = init_browser()
    
    # Open the url in the browser
    browser.visit(hemis_url)

    # Select the main page's html information
    html = browser.html

    # Create a BeautifulSoup object
    main_soup = bs(html, 'lxml')
    
    # Select each image's link
    div = main_soup.find('div', class_ = 'collapsible results')
    
    # Look for all the items in the collapsible results class
    items = div.find_all('div', class_ = 'item')
    
    # Initialize a counter
    count = 0

    # For loop to iterate through each item
    for item in items:
        
        # Add to the counter
        count += 1
        
        # Store the link in a variable for further reference
        href = item.find('a')['href']
        link = 'https://astrogeology.usgs.gov' + href
        
        # Click on the link to open the image's page, use try to not abort in case of error
        try:
            browser.visit(link)

        except:
            print('No')
        
        # Select the current page's html information
        html = browser.html
        
        # Create a beautiful soup object
        hemis_soup = bs(html, 'lxml')
        
        # Search for the firs div element with class content
        pre_title = hemis_soup.find('div', class_ = 'content')
        
        # Search for the first h2 element within the previous result
        title = pre_title.find('h2').text
       
        # Search for the first div element with class wide image wrapper
        pre_src = hemis_soup.find('div', class_ = 'wide-image-wrapper')
        
        # Grab the source link for the element image with class wide image
        src = pre_src.find('img', class_ = 'wide-image')['src']

        # Append the source to the main page
        image_url = 'https://astrogeology.usgs.gov' + src
        
        # Add key and value to the mars data dictionary            
        mars_data[f'title_{count}'] = title
        mars_data[f'image_url_{count}'] = image_url
    
    # Close browser
    browser.quit()
    
#--------------------------------------- TWITTER WEATHER -------------------------------------
    
    # Twitter Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    
    # Call the soup function to create a BeautifulSoup object
    twitter = init_soup(twitter_url)
    
    # Search for the first div (division) tag with class stream
    twitter_results = twitter.find('div', class_ = 'stream')
    # print(twitter_results)

    # Search for the first div tag within the results with class content
    twitter_content = twitter_results.find_all('div', class_ = 'content')

    # Make a for loop to iterate through each tweet 
    for result in twitter_content:

        # Check it's not a retweet (so we make sure the information is the latest weather report)
        name_check = result.find('span', class_ = 'FullNameGroup')
        name = name_check.find('strong', class_ = 'fullname').text


        if (name == 'Mars Weather'):
            # Search for the first p (paragraph) tag within the content
            twitter_paragraph = result.find('p')

            # Loop through the tags in the paragraph for the a tag
            for atag in twitter_paragraph('a'):
                # Delete the items with a tag
                atag.decompose()

            # Store the text version of the paragraph without a tags in a variable
            mars_weather = twitter_paragraph.text
            
            # Add key and value to the mars data dictionary
            mars_data['weather'] = mars_weather
            
            break
        
    # Return the dictionary
    return mars_data

