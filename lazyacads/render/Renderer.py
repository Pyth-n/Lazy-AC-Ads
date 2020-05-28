import os
import sys
import math
import ast
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont
from lazyacads.scraper import scraper

class Renderer:
    def __init__(self, itemsPath: str) -> None:
        # private members
        self.__images = {}
        self.__items = self.__openItems(itemsPath)
        self.__itemsLocal = {}
        self.__shouldPromptPrice = False

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

if __name__ == '__main__':
    test = Renderer(Path(os.getcwd(), 'lazyacads', 'scraper', 'items.txt'))
    print(test)