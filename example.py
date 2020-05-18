import os
import sys
import math
from PIL import Image, ImageFilter

# get rid of previous debug clutter
os.system('clear')

images = {}

def openImages():
    # set path to assets folder
    path = os.getcwd() + '/assets'

    # add image objects to dictionary
    for x in os.listdir(path):
        fullPath = os.path.join(path, x)
        tmp = Image.open(fullPath)
        images[fullPath] = tmp

openImages()

root = Image.new('RGBA', (640, 640))

x = 64
y = 0
for key in images:
    root.paste(images[key], (x, y))
    x += 192

    if x == 640:
        x = 64
        y += 192

root.show()