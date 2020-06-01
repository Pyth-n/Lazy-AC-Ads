if __name__ != '__main__':
    print('Can\'t be imported')
    quit()

import sys
import os
import re
from pathlib import Path

from PIL import Image

from lazyacads.scraper import scraper
from lazyacads.render.Renderer import Renderer

PATH_ITEMS = Path(os.getcwd(), 'lazyacads', 'scraper', 'items.txt')

re_url = re.compile(r'^(https://)?(nookazon.com/profile/\d*/wishlist)')

try:
    url = str(input('Enter/paste nookazon link: '))
except ValueError:
    print('input error, run again')
    quit()

try:
    re_url.search(url).group(2)
except AttributeError as err:
    print(err)
    print('That link is not a wishlist!')
    quit()

print('Scraping website, please do NOT touch')
scraper.main(url)

print('Beginning to render file')
_ = Renderer(PATH_ITEMS)