import os
import sys
import math
import ast
import time
import random
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont
from lazyacads.scraper import scraper

PATH_ITEMS = Path(os.getcwd(), 'lazyacads', 'scraper', 'items.txt')
PATH_ASSETS = Path(os.getcwd(), 'lazyacads', 'assets')
PATH_FONTS = Path(os.getcwd(), 'lazyacads', 'assets', 'fonts')

DIVISIBLE_ROWS_DESCRIPTION = 20
OFFSET_X_IMAGE = 32
OFFSET_Y_IMAGE = 18

OFFSET_Y_DESCRIPTION = 146

class Renderer:
    def __init__(self, itemsPath: str) -> None:
        # private members
        self.__image = None
        self.__arialFont = None
        self.__draw = None # obtains value inside __newImage()

        self.__rows = 0
        self.__size = []

        self.__images = {}
        self.__items = self.__openItems(itemsPath)
        
        self.__shouldPromptPrice = False

        self.__deletePNGs()
        self.__downloadPNGs()
        self.__openImages()
        self.__calculateRowSize()
        self.__calculateTotalSize()
        
        self.__newImage((self.__size[0], self.__size[1]))
        self.__drawLines()

        self.__render()
        self.__image.show()

    # Private functions
    def __openItems(self, itemsPath: str) -> dict:
        # Verify path opens a legit dictionary
        try:
            with open(itemsPath, 'r') as f:
                tmp = f.read()
            return ast.literal_eval(tmp)
        except OSError:
            print('Items.txt file not found')
            return {}

    def __deletePNGs(self) -> None:
        for file in os.listdir(PATH_ASSETS):
            ext = file.split('.')[-1].lower()
            
            if ext == 'png':
                print(f'deleting {PATH_ASSETS / file}')
                os.remove(os.path.abspath(PATH_ASSETS / file))
        pass

    def __downloadPNGs(self) -> None:
        for fileName in self.__items:
            time.sleep(random.uniform(.4, 1.5))
            print(f'downloading {fileName}')

            with open(PATH_ASSETS / fileName, 'wb') as f:
                image = requests.get(self.__items[fileName][0], stream = True)

                for block in image.iter_content(chunk_size=1024):
                    f.write(block)

    def __openImages(self) -> None:
        for file in os.listdir(PATH_ASSETS):
            if file in self.__items:
                img = Image.open(PATH_ASSETS / file).convert('RGBA').resize((128,128))
                self.__images[file] = img

    def __calculateRowSize(self) -> None:
        '''
        Calculate number of rows based on number of images
        '''
        totalImages = len(self.__images)
        if totalImages <= 4 and totalImages > 0:
            self.__rows =  1
            return

        self.__rows = math.ceil(totalImages / 4)

    def __calculateTotalSize(self) -> None:
        totalImages = len(self.__images)

        x = 768
        y = self.__rows * 192

        if totalImages <= 4 and totalImages > 0:
            x = totalImages * 192
            y = 192
        
        self.__size.append(x) # set width size
        self.__size.append(y) # set height size

    def __newImage(self, xy: tuple) -> None:
        print(f'creating image with these dimensions - width: {xy[0]}, height: {xy[1]}')
        self.__image = Image.new('RGBA', (xy[0], xy[1]))
        self.__draw = ImageDraw.Draw(self.__image)

    def __drawLines(self) -> None:
        fill = 'yellow'
        fill2 = 'red'
        # Draw vertical lines
        self.__draw.line([(192,0), (192, self.__size[1])], fill=fill, width=1)
        self.__draw.line([(384,0), (384, self.__size[1])], fill=fill, width=1)
        self.__draw.line([(576,0), (576, self.__size[1])], fill=fill, width=1)
        # Draw horizontal lines
        self.__draw.line([(0,192), (self.__size[0], 192)], fill=fill2, width=1)
        self.__draw.line([(0,384), (self.__size[0], 384)], fill=fill2, width=1)
        self.__draw.line([(0,576), (self.__size[0], 576)], fill=fill2, width=1)

    def __drawPrice(self, column: int, y: int, amount: int) -> None:
        self.__arialFont = ImageFont.truetype(str(PATH_FONTS / 'arialbd.ttf'), 25)
        if len(amount) > 13:
            raise ValueError('Price cannot exceed 13 characters')
        textSize = self.__draw.textsize(amount, font=self.__arialFont)
        offset = column * 192
        center = (192 - textSize[0]) / 2 + offset
        self.__draw.text((center, y), amount, fill='white', font=self.__arialFont, align='center')

    def __drawImage(self, xy: tuple, image: Image) -> None:
        print(f'drawing: {image}')
        self.__image.paste(image, (xy[0], xy[1]), image)

    def __drawDescription(self, column: int, y: int, description: str) -> None:
        self.__arialFont = ImageFont.truetype(str(PATH_FONTS / 'arialbd.ttf'), 15)
        text = self.__splitText(description)
        textSize = int(self.__draw.textsize(text[0], font=self.__arialFont)[0])

        offset = column * 192
        center = (192 - textSize) / 2 + offset
        
        self.__draw.text((center, y), text[0], fill='white', font=self.__arialFont, align='center', spacing=1)

    def __splitText(self, text: str) -> tuple:
        length = len(text)
        newString = []
        rowCount = 0
        prevIndex = 0
        for char in range(length):
            if rowCount > 3:
                return (''.join(newString), 3)
            if char % DIVISIBLE_ROWS_DESCRIPTION == 0 and char != 0:
                rowCount += 1
                newString.append(text[prevIndex:char] + '\n')
                prevIndex = char

        if prevIndex < length:
            newString.append(text[prevIndex:length])
            rowCount += 1

        return (''.join(newString), rowCount)

    def __render(self) -> None:
        x_image, y_image = 0, 0
        x_price, y_price = 0, 0
        x_desc, y_desc = 0, 0
        col = 0

        for i, values in enumerate(self.__images.items()):
            key = values[0]
            # Need to start drawing in new row
            if i % 4 == 0 and i != 0:
                y_desc += 192
                col = 0
            elif i != 0:
                col += 1
            self.__drawPrice(col, y_desc, '5 NMT')

if __name__ == '__main__':
    test = Renderer(PATH_ITEMS)
