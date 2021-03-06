"""
Use Selenium version 3 for this code, version 4 has different syntax
"""
# necessary libraries and modules
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import pandas as pd
import requests
import os

# open the browser
print("Openning browser...\n\n")

# initialize automated browser window, specify the browser we want to use
# store the path of the driver file in the brackets
driver = webdriver.Chrome("C:/zadachki/Different_Upwork_Projects/chromedriver_win32/chromedriver.exe")
# open the url you would like to request
driver.get("https://en.comparis.ch/immobilien/result/list?requestobject=%7B%22DealType%22%3A10%2C%22SiteId%22%3A-1%2C%22RootPropertyTypes%22%3A%5B%5D%2C%22PropertyTypes%22%3Anull%2C%22RoomsFrom%22%3A%22-10%22%2C%22RoomsTo%22%3Anull%2C%22FloorSearchType%22%3A0%2C%22LivingSpaceFrom%22%3Anull%2C%22LivingSpaceTo%22%3Anull%2C%22PriceFrom%22%3Anull%2C%22PriceTo%22%3A%22-10%22%2C%22ComparisPointsMin%22%3A-1%2C%22AdAgeMax%22%3A-1%2C%22AdAgeInHoursMax%22%3Anull%2C%22Keyword%22%3Anull%2C%22WithImagesOnly%22%3Anull%2C%22WithPointsOnly%22%3Anull%2C%22Radius%22%3Anull%2C%22MinAvailableDate%22%3Anull%2C%22MinChangeDate%22%3Anull%2C%22LocationSearchString%22%3A%22Geneve%22%2C%22Sort%22%3A11%2C%22HasBalcony%22%3Afalse%2C%22HasTerrace%22%3Afalse%2C%22HasFireplace%22%3Afalse%2C%22HasDishwasher%22%3Afalse%2C%22HasWashingMachine%22%3Afalse%2C%22HasLift%22%3Afalse%2C%22HasParking%22%3Afalse%2C%22PetsAllowed%22%3Afalse%2C%22MinergieCertified%22%3Afalse%2C%22WheelchairAccessible%22%3Afalse%2C%22LowerLeftLatitude%22%3Anull%2C%22LowerLeftLongitude%22%3Anull%2C%22UpperRightLatitude%22%3Anull%2C%22UpperRightLongitude%22%3Anull%7D&page=0")
time.sleep(2)


# scraping the number of hits found
# we need this number if want to scrape links from all pages, specify it in range() in the next block
print("Checking how many apartments there are on a website...\n\n")
num_hits_raw = driver.find_element_by_xpath('//html/body/div/div/div/div/div/div/div/div/div/div/p/strong').get_attribute("innerText") # long comment
num_hits = int(re.match("(^\d*(?:\,)\d*)", num_hits_raw).group(0).replace(",", ""))
print("There are {} items found at the website.\n\n".format(num_hits))


# scraping all the links and saving them into "links" list
last_page = int(num_hits/10+2)
links = []
# here I am scraping only from 5 pages (number of pages needed +2)
# to scrape all, change the second number in range() to last_page
for i in range(2, 7):
    try:
        driver.execute_script("window.scrollTo(0, 1900);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, window.scrollY + 1100)")
        time.sleep(1)
        containers = driver.find_elements_by_class_name("css-ctytwt.excbu0j5")
        for container in containers:
            link = container.find_element_by_css_selector("a").get_attribute("href")
            links.append(link)
        driver.find_element_by_xpath(("//a[text()='{}']").format(i)).click()
        time.sleep(2)
    except NoSuchElementException:
        print("Having problems")
print("There are {} links found.\n\n".format(len(links)))


# scraping info from each link into lists
address = []
agent = []
found_on = []
key_data = []
descriptions = []
print("Scraping key info from each link...\n\n")
for link in links:
    url = link
    driver.get(url)
    # Scraping ADDRESS (map)
    try:
        address1 = driver.find_element_by_css_selector("h5").get_attribute("innerText")
        address.append(address1)
    except NoSuchElementException:
        address.append("NO ADDRESS INFO")

    # Scraping AGENT INFO
    try:
        agent1 = driver.find_element_by_class_name("css-1xc2u8a.excbu0j2").get_attribute("innerText")
        agent.append([agent1.replace("\n\n", "; ").replace("\nShow", "")])
    except NoSuchElementException:
        agent.append("NO AGENT INFO")

    # Scraping FOUND ON
    # step 1
    try:
        found1 = [
            driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div/a").get_attribute(
                "innerText")]
    except NoSuchElementException:
        found1 = ["NO 'Found on' INFO"]
        # step 2
    try:
        found2 = driver.find_elements_by_css_selector("p.css-8jx3va.excbu0j2")
        for a in found2:
            found1.append(a.get_attribute("innerText"))
    except NoSuchElementException:
        pass
    found_on.append(found1)

    # Scraping  KEY DATA
    hdrs = driver.find_elements_by_class_name("css-cyiock.excbu0j2")
    undrhdrs = driver.find_elements_by_class_name("css-1ush3w6.excbu0j2")
    keyd_dict = {k.get_attribute("innerText"): v.get_attribute("innerText") for k, v in zip(hdrs, undrhdrs)}
    # changing empty values to "Available"
    empty = ""
    # initializing replace value
    repl_val = "Available"
    # iterating dictionary
    for key, val in keyd_dict.items():
        # checking for required value
        if val == empty:
            keyd_dict[key] = repl_val
    key_data.append(keyd_dict)

    # Scraping DESCRIPTION
    try:
        description = [driver.find_element_by_class_name("css-bxr8ec.excbu0j5").get_attribute("innerText").replace("\n\n", "; ").replace("\n", " ")]
        descriptions.append(description)
    except NoSuchElementException:
        descriptions.append(["No description found."])
    time.sleep(2)

# saving scraped info into a single dataframe
print("Saving scraped info into a dataframe and .csv\n\n")
df = pd.DataFrame({"Link" : links, "Address": address, "Agent": agent, "Found on" : found_on, "Key data" : key_data, "Description" : descriptions})

# removing all the brackets from the final dataframe
for col in df:
    df[col] = df[col].astype(str).str.replace("[", "").str.replace("]", "")
    df[col] = df[col].astype(str).str.replace("{", "").str.replace("}", "")

# saving the dataframe to a csv file
# change the name if needed
df.to_csv("Comparis_web_scraping.csv", index=False)
print("Done with all the tasks!\n\n")

