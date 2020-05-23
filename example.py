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
    '''
    Determines the coordinates where the text will be placed
    '''
    x, y = None, None

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
 
    _splitText((x, y), text)
    
def drawNMTs(coords):
    '''
    Draws the price
    '''
    global draw, arialFontBig
    x = coords[0] - 64
    y = coords[1] + 20

    y2 = y + 25
    draw.text((x, y), '5', font=arialFontBig)
    draw.text((x, y2), 'NMTs', font=arialFontBig)

# TODO: make this function splits large text. Maximum of 42 characters
def _splitText(indexes, text):
    '''
    Splits the text after 13 characters and stores them into an array
    Supports up to 4 lines, so a total of 14 * 3 characters
    '''
    textAppend = []
    secondLine = ''
    thirdLine = ''
    fourthLine = ''
    
    # split the first line
    if len(text) > 13:
        secondLine = text[13:]
        if not text[13].isspace():
            text = text[:13] + '-'
        else:
            text = text[:13]
        secondLine = secondLine.lstrip() if secondLine else None

    # Split the second line
    if len(secondLine) > 13:
        thirdLine = secondLine[13:]

        if not secondLine[13].isspace():
            secondLine = secondLine[:13] + '-'
        else:
            secondLine = secondLine[:13]
        thirdLine = thirdLine.lstrip() if thirdLine else None

    # Split the third line
    if len(thirdLine) > 13:
        fourthLine = thirdLine[13:]

        if not thirdLine[13].isspace():
            thirdLine = thirdLine[:13] + '-'
        else:
            thirdLine = thirdLine[:13]
        fourthLine = fourthLine.lstrip() if thirdLine else None

    if len(fourthLine) > 13:
        fourthLine = fourthLine[:13] + '.'

    # append to array and send to next function
    textAppend.append(text)
    textAppend.append(secondLine)
    textAppend.append(thirdLine)
    textAppend.append(fourthLine)

    _drawText(indexes, textAppend)

def _drawText(indexes, text):
    global draw, arialFont

    # calculate the y position of where the text should be placed
    for i, x in enumerate(text):
        yPos = indexes[1]

        if x:
            if i == 1:
                yPos = indexes[1] + 18
            if i == 2:
                yPos = indexes[1] + 36
            if i == 3:
                yPos = indexes[1] + 54
            draw.text((indexes[0], yPos), text[i], fill = 'white', font=arialFont)

openImages()

root = Image.new('RGBA', (580, 580))
arialFont = ImageFont.truetype("assets/fonts/arialbd.ttf", 15)
arialFontBig = ImageFont.truetype('assets/fonts/arialbd.ttf', 26)
draw = ImageDraw.Draw(root)

# draw vertical lines
draw.line([(192, 0), 192,640], fill='white', width=1)
draw.line([(384,0), (384,640)], fill='white', width=1)

# draw horizontal lines
draw.line([(0, 384), 640,384], fill='white', width=1)
draw.line([(0, 192), 640,192], fill='white', width=1)


x = 64
y = 0
for index, key in enumerate(images):
    drawNMTs((x,y))
    root.paste(images[key], (x, y), images[key])
    processText((x, y), '01234567890123abcdefghijklmnopqrstubwxyzXX01234567890123abcdefghijklmnopqrstubwxyzXX')
    x += 192

    if x == 640:
        x = 64
        y += 192

root.show()
