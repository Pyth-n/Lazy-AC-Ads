import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.set_headless()
assert opts.headless

def getDescriptionsAndImages(link):
    global browser
    # opens the link. waits every DOM query
    browser.get(link)
    browser.implicitly_wait(100)
    results = browser.find_elements_by_class_name('row')
    browser.implicitly_wait(100)
    children = results[0].find_elements_by_class_name('listing-row')
    browser.implicitly_wait(100)

    # stores description and image links in dictionary
    for text in children:
        browser.implicitly_wait(100)
        description = text.find_element_by_xpath('.//div[@class="listing-name"]').text
        imgSrc = text.find_element_by_xpath('.//img[@class="listing-item-img"]').get_attribute('src')
        items[imgSrc] = description

# Item dictionary
items = {}

browser = Firefox(executable_path='scraper/geckodriver')

getDescriptionsAndImages('https://nookazon.com/profile/1921469521/wishlist')

browser.close()