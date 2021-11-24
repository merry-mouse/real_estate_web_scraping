# NOT FINISHED
# website for scraping: immobilier.ch

# importing necessary libraries and modules
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import pandas as pd
import os
import requests

# open the browser
print("Openning browser...\n\n")

# initialize automated browser window, specify the browser you want to use
# store the path of the driver file in the brackets (using Firefox here)
driver = webdriver.Firefox(executable_path="C:\\Users\\potek\\Jupyter_projects\\geckodriver\\geckodriver.exe")
# open the url you would like to request
driver.get("https://www.immobilier.ch/en/rent/apartment-house/vaud/lausanne")#comment
time.sleep(2)


