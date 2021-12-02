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
driver.get("https://www.anibis.ch/fr/c/immobilier-immobilier-locations?sct=GE")
# waiting until cookies tab is open
time.sleep(2)
# close cookies tab
driver.find_element_by_class_name("cmp-closebutton_closeButton.cmp-closebutton_hasBorder").click()

# scraping the number of hits and pages found
print("Checking how many apartments there are on the website...\n\n")
num_hits_raw = driver.find_element_by_class_name("sc-1uujbw0-0.sc-1uujbw0-2.hnhhTs.jOORWi").get_attribute("innerText")
num_hits = int((re.search("^(\d)'(\d+)", num_hits_raw).group(0)).replace("'", ""))
# there are 20 apartments per page, using math.ceil to find ceil number after division
num_pages = math.ceil(num_hits / 20)
print("There are {} items on {} pages found.\n\n".format(num_hits, num_pages))

# scraping links (apartments) from each page
links = []
# end of range is EXCLUSIVE
# to scrape ALL PAGES put num_pages+1 in the end of range
for i in range(2, 4):
    # scrapes links
    containers = driver.find_elements_by_class_name("sc-gsTCUz.eJcPpT.sc-1gbeqqm-0.qNwID")
    for apartment in containers:
        link = apartment.get_attribute("href")
        links.append(link)
    print("{} links found.".format(len(links)))
    # clicks to the next page
    driver.find_element_by_xpath("//div[text()='{}']".format(i)).click()
    time.sleep(2)
