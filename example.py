import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

# get rid of previous debug clutter
os.system('clear')

images = {}

def openImages():
    # set path to assets folder
    path = os.getcwd() + '/assets'

    # add image objects to dictionary
    for x in os.listdir(path):
        fullPath = os.path.join(path, x)
        # ignore folders
        if os.path.isfile(fullPath):
            tmp = Image.open(fullPath)
            images[fullPath] = tmp

def processText(indexes, text):
    global draw, arialFont

    x, y = None, None
    print(f'{indexes}: {text}')
    
    if indexes[0] == 64:
        x = 0
    elif indexes[0] == 256:
        x = 213
    elif indexes[0] == 448:
        x = 426
    else:
        raise Exception(ArithmeticError('x out of bounds'))

    if indexes[1] == 0:
        y = 120
    elif indexes[1] == 192:
        y = 310
    elif indexes[1] == 384:
        y = 500
    else:
        raise Exception(ArithmeticError('y out of bounds'))
 
    draw.text((x, y), text, fill = 'white', font=arialFont)

    print(f'Alignment: ({x},{y})')

openImages()

root = Image.new('RGBA', (640, 640))
arialFont = ImageFont.truetype("assets/fonts/arialbd.ttf", 15)
draw = ImageDraw.Draw(root)

# drawing algorithm
x = 64
y = 0
for index, key in enumerate(images):
    root.paste(images[key], (x, y))
    processText((x, y), 'WWWWWWWWWWWWWW')
    x += 192

    if x == 640:
        x = 64
        y += 192

root.show()