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

try:
    url = str(input('Enter/paste nookazon link: '))
except ValueError:
    print('input error, run again')
    quit()

try:
    re_url.search(url).group(2)
except AttributeError as ae:
    print(ae)
    print('That link is not a wishlist!')
    quit()

try:
    shouldPrompt = str(input('Would you like to price the items (5 default)? (y/n): ').lower().lstrip())
except ValueError:
    print('invalid input, no nmt prompts')
    shouldPrompt = 'n'

print('Scraping website, please do NOT touch')
scraper.main(url)

try:
    if shouldPrompt[0] == 'y':
        render.shouldPromptNMTs = True
except IndexError as e:
    print(e)

print('Beginning to render file')
render.main()