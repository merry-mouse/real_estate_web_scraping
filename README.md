# Real estate web scraping in Python using Selenium webdriver

In this repository I store 3 similar web scrapers, each extracts data and save it in a .csv file.
They also download photos from the website and store each set of photos (for each apartment) in a separate
folder named by a row number of the apartment in a .csv database.
Since there 3 websites, each of them has its own peculiarities and difficulties for scraping.
Website 1 and 2  can identify web scraper as a bot and won't allow it to download photos unless HEADERS
in requests library are used, meanwhile there is not a problem for website 3.

## Legality of web scraping
Web scraping itself is legal unless you use it unethically and try to scrape Nonpublic data.
Web data scraping and crawling aren’t illegal by themselves, but it is important to be ethical while doing it.
Don’t tread onto other people’s sites without being considerate. Respect the rules of their site. 
Consider reading over their Terms of Service, read the robots.txt file. 

## Libraries and modules

Important: for all 3 web scrapers I use Selenium version 3. Not compatible with version 4 (different syntax)

```
# necessary libraries for website1 and 2
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import pandas as pd
import os
import requests
```
Website3 requires additional math module since there isn't total number of pages on the website and 
to scrape all the pages we need to calculate it's total number with ceiling division

```
import math
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries.

```bash
pip install selenium
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

