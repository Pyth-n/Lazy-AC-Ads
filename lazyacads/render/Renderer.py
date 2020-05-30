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

class Renderer:
    def __init__(self, itemsPath: str) -> None:
        # private members
        self.__image = None
        self.__arialFont = ImageFont.truetype(str(PATH_FONTS / 'arialbd.ttf'), 15)
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
        
if __name__ == '__main__':
    test = Renderer(PATH_ITEMS)
