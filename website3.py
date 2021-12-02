# website for scraping: anibis.ch
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import pandas as pd
import os
import requests
import math
# open the browser
print("Openning browser...\n\n")

# initialize automated browser window, specify the browser we want to use
# store the path of the driver file in the brackets
driver = webdriver.Chrome("C:/Users/potek/Jupyter_projects/chromedriver_win32/chromedriver.exe")
# open the url you would like to request
driver.get("https://www.anibis.ch/fr/c/immobilier-immobilier-locations?sct=GE")#comment
time.sleep(2)
# close cookies tab
driver.find_element_by_class_name("cmp-closebutton_closeButton.cmp-closebutton_hasBorder").click()
