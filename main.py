if __name__ != '__main__':
    print('Can\'t be imported')
    quit()

import sys
import os
import re

from PIL import Image

from lazyacads.scraper import scraper
from lazyacads.render import render

re_url = re.compile(r'^(https://)?(nookazon.com/profile/\d*/wishlist)')

url = 'https://nookazon.com/profile/1921469521/wishlist' #input('Enter/paste nookazon link: ')

try:
    re_url.search(url).group(2)
except AttributeError as ae:
    print(ae)
    print('That link is not a wishlist!')
    quit()

print('Scraping website, please do NOT touch')
scraper.main(url)

print('Beginning to render file')
render.main()