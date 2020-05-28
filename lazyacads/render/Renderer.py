import os
import sys
import math
import ast
import time

import requests
from PIL import Image, ImageDraw, ImageFont
from lazyacads.scraper import scraper

class Renderer:
    def __init__(self, itemsPath: str) -> None:
        self.__images = {}
        self.__items = self.__openItems(itemsPath)
        self.__itemsLocal = {}
        self.__shouldPromptPrice = False
        print(self)

    # Private functions
    def __openItems(self, itemsPath: str) -> dict:
        # Verify path exists
        try:
            with open(itemsPath, 'rb') as f:
                tmp = f.read()
            return ast.literal_eval(tmp)
        except OSError:
            return {}

if __name__ == '__main__':
    Renderer('lol')