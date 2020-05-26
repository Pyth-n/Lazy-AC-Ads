import os
import sys
import math
import ast
import time

import requests
from PIL import Image, ImageDraw, ImageFont
from lazyacads.scraper import scraper

__defaultItemsPath = os.getcwd()

class Renderer:
    def __init__(self, itemsPath: str) -> None:
        self.__images = {}
        self.__items = {}
        self.__itemsLocal = {}
        self.__shouldPromptPrice = False
        print(self)

if __name__ == '__main__':
    Renderer('lol')