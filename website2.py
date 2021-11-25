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

# scraping the number of hits and pages found
print("Checking how many apartments there are on a website...\n\n")
num_hits_raw = driver.find_element_by_class_name("items-result-count").get_attribute("innerText") # long comment
num_hits = (re.search("[\s](\d+)", num_hits_raw).group(1))
num_pages_raw = driver.find_element_by_class_name("pagination-counter").get_attribute("innerText")
num_pages = int(re.search("\d+$", num_pages_raw).group(0))

print("There are {} items on {} pages found.\n\n".format(num_hits, num_pages))


# SCRAPING LINKS
links = []
# Scraping only a few first pages
# to scrape all info from the website change second number in range to num_pages
for i in range(2,3):
    try:
        driver.execute_script("window.scrollTo(0, 3500)")
        containers = driver.find_elements_by_class_name("filter-item-container")
        time.sleep(1)
        for container in containers:
            try:
                link = container.find_element_by_css_selector("a").get_attribute("href")
                links.append(link)
            except NoSuchElementException:
                pass
        print("{} links found.".format(len(links)))
        driver.find_element_by_xpath(("//a[text()='{}']").format(i)).click()
        time.sleep(2)
    except NoSuchElementException:
        print("Having problems")


# SCRAPING MAIN INFO FROM EACH LINK
names = []
addresses = []
sqms = []
room_numbs = []
prices = []
descriptions = []
abouts = []
features = []
for num, link in enumerate(links):
    url = link
    driver.get(url)
    # NAME
    try:
        name = driver.find_element_by_css_selector("h1").get_attribute("innerText")
        names.append(name)
    except NoSuchElementException:
        names.append("NO NAME")
    # ADDRESS
    try:
        address = driver.find_element_by_class_name("object-address").get_attribute("innerText")
        addresses.append(address)
    except NoSuchElementException:
        addresses.append("NO ADDRESS INFO")

    # SQM
    try:
        SQM = driver.find_element_by_class_name("title").get_attribute("innerText")
        sqms.append(SQM)
    except NoSuchElementException:
        sqms.append("NO SQM2 INFO")

    # NUMBER OF ROOMS
    try:
        room_numb = driver.find_element_by_xpath(
            "/html/body/div/main/section/div/div/div/section/header/ul/li/following-sibling::li").get_attribute(
            "innerText")
        room_numbs.append(room_numb)
    except NoSuchElementException:
        room_numbs.append("NO ROOM NUMBER INFO")

    # PRICE
    try:
        price = driver.find_element_by_class_name("im__postDetails__price").find_element_by_tag_name(
            "strong").get_attribute("innerText")  # comment
        prices.append(price)

    except NoSuchElementException:
        prices.append("NO PRICE INFO")

    # DESCRIPTION
    try:
        description = driver.find_element_by_class_name("im__postContent__body").find_element_by_tag_name(
            "p").get_attribute("innerText")  # comment
        descriptions.append(description.replace("\n", " "))
    except NoSuchElementException or description == "":
        descriptions.append("NO DESCRIPTION")

    # "ABOUT" TABLE
    try:
        about = driver.find_element_by_class_name("im__table.im__table--responsive.im__row").get_attribute(
            "innerText")  # comment
        abouts.append(about.replace("\n", ","))
    except NoSuchElementException:
        abouts.append("NO TABLE FOUND")

    # FEATURES TABLE
    try:
        feature = driver.find_element_by_xpath("/html/body/div/main/section/div/div[2]/ul").get_attribute("innerText")
        features.append(feature.replace("\n", ",").replace("\n", ", "))
    except NoSuchElementException:
        features.append("NO TABLE FOUND")

    # DOWNLOAD IMAGES
    # finding image containers
    images_urls = []
    # using headers for not being identified as a robot by the website
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"}
    # scrolling down and waiting until all the pictures are rendered
    driver.execute_script("window.scrollTo(0, 3600)")
    time.sleep(1.5)
    try:
        # scraping containers that containers with img tag
        images_container = driver.find_element_by_class_name(
            "im__row.im__row--flex.im__row--flexWrap.im__row--gutter3").find_elements_by_tag_name("img")  # comment
        # informing about the number of pictures found for future debugging
        print(("For apartment number {} there are {} photos found").format(num,len(images_container)))
        for image in images_container:
            # scraping urls from that containers and store it in a list
            images_urls.append(image.get_attribute("src"))
        for i in images_urls:
            # creating new folder in APARTMENTS for storing photos in there
            path = "C:/Users/potek/Jupyter_projects/APARTMENTS/{}".format(num)
            if not os.path.exists(path):
                os.mkdir(path)
            # Download the images using requests library
            with open(os.path.join(path, "Immobilier" + str(time.time()) + ".jpg"), "wb") as f:
                try:
                    f.write(requests.get(i, headers=headers).content)
                except NoSuchElementException:
                    pass
    except NoSuchElementException:
        pass
    time.sleep(0.5)
print("Done with scraping from each link.\n\n")

# checking list lengths to avoid any bugs
if len(names) == len(addresses) == len(sqms) == len(room_numbs) == len(prices) == len(descriptions) == len(abouts) == len(features):
    print(("All lists has the same length ({})").format(len(names)))
    # creating data frame and saving it into a .csv file
    df = pd.DataFrame({"Name": names, "Link": links, "Address": addresses, "SQM": sqms, "Number of rooms": room_numbs,
                       "Price": prices, "Description": descriptions, "About": abouts, "Features": features})
    df.to_csv("Immobilier_scraping_database.csv", index=False)
else:
    print("There is a potential bug, lists have different length!")







