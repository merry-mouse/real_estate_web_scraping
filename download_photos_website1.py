# Only work with Selenium earlier versions (before 4.0)
# necessary libraries and modules

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import requests
import os

# open the browser
print("Openning browser...\n\n")

# initialize automated browser window, specify the browser we want to use
# store the path of the driver file in the brackets
driver = webdriver.Chrome("C:/Users/potek/Jupyter_projects/chromedriver_win32/chromedriver.exe")
# open the url you would like to request
driver.get("https://en.comparis.ch/immobilien/result/list?requestobject=%7B%22DealType%22%3A%2210%22%2C%22LocationSearchString%22%3A%22Bern%22%2C%22RootPropertyTypes%22%3A%5B%220%22%5D%2C%22PriceTo%22%3A%22-10%22%2C%22RoomsFrom%22%3A%22-10%22%2C%22Sort%22%3A%2211%22%2C%22AdAgeMax%22%3A-1%2C%22ComparisPointsMin%22%3A-1%2C%22SiteId%22%3A-1%7D&sort=11")
time.sleep(2)


# USE THIS BLOCK ONLY IF WANTS TO SCRAPE ALL LINKS FROM ALL PAGES
# scraping the number of hits found
# print("Checking how many apartments there are on a website...\n\n")
# num_hits_raw = driver.find_element_by_xpath('//html/body/div/div/div/div/div/div/div/div/div/div/p/strong').get_attribute("innerText") # long comment
# num_hits = int(re.match("(^\d*(?:\,)\d*)", num_hits_raw).group(0).replace(",", ""))
# print("There are {} items found at the website.\n\n".format(num_hits))
# last_page = int(num_hits/10+2)


links = []
# SCRAPING ONLY ONE PAGE
# to scrape all info from the website change second number in range to last_page
for i in range(2,3):
    try:
        driver.execute_script("window.scrollTo(0, 1900);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, window.scrollY + 1100)")
        time.sleep(1)
        containers =  driver.find_elements_by_class_name("css-ctytwt.excbu0j5")
        for container in containers:
            link = container.find_element_by_css_selector("a").get_attribute("href")
            links.append(link)
        print("{} links found.".format(len(links)))
        driver.find_element_by_xpath(("//a[text()='{}']").format(i)).click()
        time.sleep(2)
    except NoSuchElementException:
        print("Having problems")


# CREATE A LOOP, OPEN EACH LINK
for num, link in enumerate(links):
    url = link
    driver.get(url)
    # COUNT NUMBER OF SMALL CIRCLES, ADD 1
    circles = len(driver.find_elements_by_class_name("svg-inline--fa.fa-circle.fa-w-16.css-1xkwzfp"))
    print("for apartment {}, {} photos found at the website.".format(num, circles+1))
    # CREATE A SET TO GET RID OF DUPLICATES
    images_urls = set()
    for n in range(circles):
        # FIND IMAGE CONTAINERS
        images_containers = driver.find_element_by_class_name("css-ze3zoq").find_elements_by_tag_name("img")
        for image in images_containers:
            # FIND IMAGES' URLS, STORE THEM IN A SET
            images_urls.update([image.get_attribute("src")])
        # FIND BUTTON THAT SCROLL TO THE RIGHT AND CLICK IT
        driver.find_element_by_class_name("css-11m3oda.excbu0j2").click()
        time.sleep(0.1)

    # DOWNLOAD PHOTOS IN "APARTMENTS" AND CREATE NEW FOLDER FOR EACH APARTMENT
    for i in images_urls:
        path = "C:/Users/potek/Jupyter_projects/APARTMENTS/{}".format(num)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(os.path.join(path, "Comparis"+str(time.time())+".jpg"), "wb") as f:
            try:
                # DOWNLOAD CONTENT OF THE URL
                f.write(requests.get(i).content)
            except:
                pass
    time.sleep(0.2)
print("\nDONE!")


