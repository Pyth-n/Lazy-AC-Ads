import os
import sys
import math
import ast
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from lazyacads.scraper import scraper

# get rid of previous debug clutter
os.system('clear')

# Holds dictionary of Image instances
images = {}

# Holds local scraper/items.txt
# Keys: full link to PNG files. Values: Description of item
items = {}
itemsLocal = {}
shouldPromptNMTs = False

# global variables
root = Image.new('RGBA', (580, 580))
arialFont = ImageFont.truetype("lazyacads/assets/fonts/arialbd.ttf", 15)
arialFontBig = ImageFont.truetype('lazyacads/assets/fonts/arialbd.ttf', 26)
draw = ImageDraw.Draw(root)

def openItems():
    global items

    try:
        with open('lazyacads/scraper/items.txt', 'r') as r:
            tmp = r.read()
        items = ast.literal_eval(tmp)
    except FileNotFoundError as fnf:
        print(fnf)
        quit()

    # store items locally
    for x in items:
        tmpUrl = x.split('/')[-1]
        itemsLocal[tmpUrl] = items[x]

def downloadImages():
    global items

    for i, key in enumerate(items):
        # save only 9 items
        if i > 8:
            break

        filename = key.split('/')[-1]
        savePath = os.path.join('lazyacads/assets', filename)

        with open(savePath, 'wb') as f:
            time.sleep(1)
            print(f'Download image: {filename}')
            res = requests.get(key, stream = True)

            for block in res.iter_content(1024):
                if not block:
                    break
                f.write(block)

def openImages():
    # set path to assets folder
    path = os.getcwd() + '/lazyacads/assets'

    # add image objects to dictionary
    for x in os.listdir(path):
        if len(images) > 8:
            break # don't add more than 9 files
        fullPath = os.path.join(path, x)
        filePath, ext = os.path.splitext(fullPath)

        # ignore folders
        if os.path.isfile(fullPath) and ext == '.png':
            tmp = Image.open(fullPath)
            tmp2 = tmp.resize((128, 128))
            images[fullPath] = tmp2
            tmp.close()

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
 
    __splitText((x, y), text)
    
def drawNMTs(coords, amount):
    '''
    Draws the price
    '''
    global draw, arialFontBig
    x = coords[0] - 64
    y = coords[1] + 20

    amount = str(amount)

    y2 = y + 25
    draw.text((x, y), amount, font=arialFontBig)
    draw.text((x, y2), 'NMTs', font=arialFontBig)

def renderAll():
    global images, root, shouldPromptNMTs
    # drawing algorithm
    x = 64
    y = 0
    for key in images:
        amount = 5
        if shouldPromptNMTs:
            while True:
                try:
                    amount = int(input(f'Enter NMT price for {__getValue(key)}: '))
                    break
                except ValueError:
                    print('Not a valid number, try again!')
        drawNMTs((x,y), amount)
        root.paste(images[key], (x, y), images[key])
        processText((x, y), __getValue(key))
        x += 192

        if x == 640:
            x = 64
            y += 192

def drawLines():
    global draw
    # draw vertical lines
    draw.line([(192, 0), 192,640], fill='white', width=1)
    draw.line([(384,0), (384,640)], fill='white', width=1)

    # draw horizontal lines
    draw.line([(0, 384), 640,384], fill='white', width=1)
    draw.line([(0, 192), 640,192], fill='white', width=1)

def deletePNGs():
    '''
    Deletes ALL .png files inside the assets directory
    '''
    cwd = os.getcwd() + '/lazyacads/assets'
    
    for file in os.listdir(cwd):
        fullPath = os.path.join(cwd, file)

        filePath, ext = os.path.splitext(fullPath)
        
        if ext.lower() == '.png':
            os.remove(fullPath)

def __getValue(key):
    key = key.split('/')[-1]
    if key in itemsLocal:
        return itemsLocal[key]
    return 'error getting name'

def __splitText(indexes, text):
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

    __drawText(indexes, textAppend)

def __drawText(indexes, text):
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

def main():
    global root
    openItems()
    deletePNGs()
    downloadImages()
    openImages()
    drawLines()
    renderAll()
    root.show()
    root.save('rendered.png')

if __name__ == '__main__':
    main()