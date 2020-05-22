import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.set_headless()
assert opts.headless

itemNames = []

browser = Firefox(executable_path='scraper/geckodriver')
browser.get('https://nookazon.com/profile/1921469521/wishlist')
browser.implicitly_wait(100)

results = browser.find_elements_by_class_name('row')

# text
for text in results[0].find_elements_by_class_name('listing-row'):
    lol = text.find_element_by_xpath('.//div[@class="listing-name"]').text
    itemNames.append(lol)

print(itemNames)
browser.close()