import os
import ast
import re
import time
import random
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.set_headless()
assert opts.headless

# Item dictionary
items = {}

browser = None

def scrape(link):
    '''
    Gets only up to 9 total items from a Nookazon wishlist
    '''
    global browser
    browser = Firefox(executable_path='lazyacads/scraper/geckodriver')
    browser.implicitly_wait(12)

    try:
        __scrapeLinksAndDescriptions(browser, link)
    except:
        print('There was connection issue (high traffic possibly). Please try again.')
        close()
        quit()

def __scrapeLinksAndDescriptions(browser, link):
    '''
    getDescriptionsAndImages worker
    '''
    # opens the link. waits every DOM query
    browser.get(link)
    
    try:
        results = browser.find_elements_by_class_name('row')
        children = results[0].find_elements_by_class_name('listing-row')
    except exceptions.StaleElementReferenceException as e:
        print(f'{e}')
        raise

    # stores description and image links in dictionary
    for i, text in enumerate(children):
        if i > 8:
            break
        try:
            description = text.find_element_by_xpath('.//div[@class="listing-name"]').text
            imgSrc = text.find_element_by_xpath('.//img[@class="listing-item-img"]').get_attribute('src')
            items[imgSrc] = __stripAmount(description)
        except exceptions.StaleElementReferenceException as e:
            print(f'{e}')
            raise

def __stripAmount(item):
    '''
    input: "2 X Name of item"
    output: "Name of item"
    '''
    newString = re.sub(r'^(\d*\sX\s)?', '', item)
    return newString

def __loadAllItems():
    '''
    Looks for 'Load More' button no the Nookazon website and clicks it all the way to the bottom
    '''
    global browser
    while True:
        try:
            print('Looking for \'Load More\' button to click...')
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, './/div[@class="see-all-btn-bar"]/button'))).click()
            time.sleep(random.randint(2, 4)) # don't want the api to throttle connection
        except:
            print('Bottom page reached')
            break
    return

def saveItems():
    '''
    Saves dictionary string of picture links and its description
    '''
    global items
    try:
        with open('lazyacads/scraper/items.txt', 'w') as f:
            f.write(str(items))
            print('wrote items.txt')
    except OSError as e:
        print(f'{e}: Could not save items.txt')
        close()
        quit()
        raise

def readItems():
    global items
    tmp = None
    try:
        with open('lazyacads/scraper/items.txt', 'r') as r:
            tmp = r.read()
        items = ast.literal_eval(tmp)
        print('Read items.txt successfully')
    except FileNotFoundError as e:
        print(f'{e}: items.txt not found')
        raise

def close():
    global browser
    '''
    Closes FireFox browser
    '''
    browser.close()

def main(link):
    '''
    Output: items.txt
    '''
    scrape(link)
    saveItems()
    close()

if __name__ == '__main__':
    main('https://nookazon.com/profile/1921469521/wishlist')