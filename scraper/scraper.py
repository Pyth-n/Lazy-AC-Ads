import os
import ast
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.set_headless()
assert opts.headless

# Item dictionary
items = {}

browser = Firefox(executable_path='scraper/geckodriver')

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

def saveItems():
    global items
    with open('scraper/items.txt', 'w') as f:
        f.write(str(items))
        print('wrote item.txt')

def readItems():
    global items
    tmp = None
    try:
        with open('scraper/items.txt', 'r') as r:
            tmp = r.read()
        items = ast.literal_eval(tmp)
        print('read item.txt')
    except:
        print('error readings items')

readItems()
getDescriptionsAndImages('https://nookazon.com/profile/1921469521/wishlist')
saveItems()

browser.close()