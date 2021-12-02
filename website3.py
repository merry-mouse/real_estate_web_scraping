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

# SCRAPING MAIN INFO FROM EACH LINK
headers = []
details = []
descriptions = []
addresses = []
announcers = []
announces = []
tels = []
for num, link in enumerate(links):
    driver.get(link)
    # HEADERS
    try:
        header = driver.find_element_by_class_name("cahxkj-0.sc-1645p4v-0.brwHqV.edLfCV").get_attribute("innerText")
        headers.append(header.replace("\n", ", "))
    except NoSuchElementException:
        headers.append("No header found")
    # DETAILS (list of dicts)
    try:
        detail = (driver.find_element_by_class_name("sc-79mv0k-0.cthnIw").get_attribute("innerText")).split(
            "\n")  # comme
        details.append(dict(zip(detail[::2], detail[1::2])))
    except NoSuchElementException:
        details.append("No details found")

    # DESCRIPTIONS
    try:
        description = driver.find_element_by_class_name("urtii3-0.xVgjA").get_attribute("innerText").replace("\n", ", ")
        descriptions.append(description)
    except NoSuchElementException:
        descriptions.append("No description found")
    # ADDRESSES
    try:
        address = driver.find_element_by_class_name("sc-1oudagz-0.sc-1f77bma-0.covveV.bylUyk").get_attribute(
            "innerText").replace("\n", ", ")  # comment
        addresses.append(address)
    except NoSuchElementException:
        addresses.append("No address found")
    # ANNOUNCER
    try:
        announcer = driver.find_element_by_class_name("sc-gsTCUz.iqdsSd").get_attribute("innerText")
        announcers.append(announcer)
    except NoSuchElementException:
        announcers.append("No announcer info")
    # PHONE NUMBER
    try:
        tel = driver.find_element_by_class_name("sc-1nm2xjp-0.jJCcfn").find_element_by_tag_name("a").get_attribute(
            "innerText")  # comment
        tels.append(tel)
    except NoSuchElementException:
        tels.append("No contact number found")
    # ANNOUNCE
    try:
        announce = driver.find_element_by_class_name("sc-1daxexx-0.fPZErg").get_attribute("innerText").split("\n")
        a = dict(zip(announce[::2], announce[1::2]))
        b = a.pop("Signaler une annonce suspecte")
        announces.append(a)
    except NoSuchElementException:
        announces.append("No announce found")
    # DOWNLOAD PICTURES
    try:
        # find number of circles(photos) at the page
        circles = driver.find_elements_by_class_name("v6h5f1-0.jvMQcP")
        # find swiping button
        button = driver.find_element_by_class_name("cahxkj-0.nw116f-0.kyWlQc.jOqXyv.swiper-button-prev")
        # we can oly scrape 5 urls, for more urls we have to scroll ptotos to the right|left
        number_of_clicks = (len(circles) + 1 - 5)
        if number_of_clicks > 0:
            for i in range(number_of_clicks):
                button.click()
                time.sleep(0.3)
    # sometimes there is just 1 photo and thus, 0 circles
    except NoSuchElementException:
        pass
    # creating a set where we store urls for pics if there are pics
    try:
        images_urls = set()
        img_containers = driver.find_element_by_class_name(
            "vs5092-0.bJHlto.swiper-container.swiper-uid-catalog-gallery").find_elements_by_tag_name("img")
        for img in img_containers:
            try:
                images_urls.update([img.get_attribute("src")])
            except NoSuchElementException:
                pass
        print("For apartment {}, {} photos found at the website.".format(num, len(images_urls)))
        # download photos in the same folder
        for i in images_urls:
            path = "C:/Users/potek/Jupyter_projects/APARTMENTS/{}".format(num)
            if not os.path.exists(path):
                os.mkdir(path)
            # Download the images using requests library
            with open(os.path.join(path, "Anibis" + str(time.time()) + ".jpg"), "wb") as f:  # comment
                f.write(requests.get(i).content)
    except NoSuchElementException:
        print("For apartment {}, 0 photos found at the website.".format(num))

    time.sleep(0.5)
print("Done with scraping from each link.\n\n")

# saving into dataframe to take a look in jupyter notebook
df = pd.DataFrame({"Link" : links, "Header": headers, "Details": details, "Description" : descriptions, "Address" : addresses, "Announcer" : announcers, "Announce" : announces})
# removing all the brackets from the dataframe
for col in df:
    df[col] =df[col].astype(str).str.replace("[","").str.replace("]","")
    df[col] =df[col].astype(str).str.replace("{","").str.replace("}","")
# saving the dataframe to a csv file
df.to_csv("Anibis_web_scraping.csv", index=False)