import os
import sys
import math
import ast
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont
from lazyacads.scraper import scraper

PATH_ITEMS = Path(os.getcwd(), 'lazyacads', 'scraper', 'items.txt')
PATH_ASSETS = Path(os.getcwd(), 'lazyacads', 'assets')

class Renderer:
    def __init__(self, itemsPath: str) -> None:
        # private members
        self.__images = {}
        self.__items = self.__openItems(itemsPath)
        self.__itemsLocal = {}
        self.__shouldPromptPrice = False

        self.__deletePNGs()

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

if __name__ == '__main__':
    test = Renderer(PATH_ITEMS)
