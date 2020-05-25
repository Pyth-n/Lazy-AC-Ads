# Lazy Advertisements for Animal Crossing
## About
This is an under-develpoment CLI tool (soon to be GUI) that scrapes [Nookazon Wishslists](https://nookazon.com) and obtains the images and descriptions of individual items. This information is then used to render a PNG image used for bartering with Nook Miles Tickets. The only way to run this currently is to install it as development (see Development Installation) and then running the **main.py** file from the root directory.

This project is fan-made and is in no way affiliated with Nintendo nor Animal Crossing.

## Requirements
* Download [Firefox](https://www.mozilla.org/en-US/exp/firefox/new/)
* Python >= 3.3 < 4
* All other dependencies is handled by **setup.py** (see development installation)

## Development Installation
* `git clone git@github.com:Pyth-n/Lazy-AC-Ads.git` **OR** [Download v1.0.1 Zip](https://github.com/Pyth-n/Lazy-AC-Ads/archive/master.zip)
* Open terminal inside the project root folder:
  * `python3 -m venv env` - Create a virtual environment so that dependencies do not install globally on the system.
  * `source env/bin/activate` - Activate this virtual environment. Shell command prompt should start with *(env)* now.
  * `pip install -e .` - Installs all the dependencies **required** for this project to work.
* `deactivate` - This exits the virtual environment when finished  

* Execute the main file:
  * `python3 main.py` - Run this in the root folder. Make sure the virtual environment is activated (see above).

## TODO
* Major
  * GUI
  * Release .exe (Windows) and .app (MacOS)
  * Support Bells with the amount up to 1,000,000
  * Ability to remove from local items.txt
  * Compare local items.txt and delete items on the website if they were deleted locally
* Minor
  * Add small icons that represent DIYs
  * Handle total size when <= 6 images are used
