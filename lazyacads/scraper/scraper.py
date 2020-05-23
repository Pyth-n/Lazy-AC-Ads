import os
import ast
import re
import time
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.set_headless()
assert opts.headless

# Item dictionary
items = {}

browser = None

def getDescriptionsAndImages(link):
    global browser
    browser = Firefox(executable_path='lazyacads/scraper/geckodriver')
    browser.implicitly_wait(12)

    # opens the link. waits every DOM query
    browser.get(link)
    __loadAllItems()
    results = browser.find_elements_by_class_name('row')

    children = results[0].find_elements_by_class_name('listing-row')

    # stores description and image links in dictionary
    for text in children:
        description = text.find_element_by_xpath('.//div[@class="listing-name"]').text
        imgSrc = text.find_element_by_xpath('.//img[@class="listing-item-img"]').get_attribute('src')
        items[imgSrc] = __stripAmount(description)

def __stripAmount(item):
    newString = re.sub(r'^(\d*\sX\s)?', '', item)
    return newString

def __loadAllItems():
    global browser
    while True:
        try:
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, './/div[@class="see-all-btn-bar"]/button'))).click()
            time.sleep(2) # don't want the api to throttle connection
        except:
            break
    return

def saveItems():
    global items
    with open('lazyacads/scraper/items.txt', 'w') as f:
        f.write(str(items))
        print('wrote item.txt')

def readItems():
    global items
    tmp = None
    try:
        with open('lazyacads/scraper/items.txt', 'r') as r:
            tmp = r.read()
        items = ast.literal_eval(tmp)
        print('read item.txt')
    except:
        print('error readings items')

def close():
    global browser
    '''
    Closes FireFox browser
    '''
    browser.close()

if __name__ == '__main__':
    readItems()
    getDescriptionsAndImages('https://nookazon.com/profile/1921469521/wishlist')
    saveItems()
    close()