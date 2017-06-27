# Python script to scrape race results for the Comrades Marathon.
# Max Metcalfe - 6/26/2017

from pyvirtualdisplay import Display
from selenium import webdriver
import argparse
import smtplib
import json
import collections
import string
import os

url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?results=true&Year={0}&Category=&Club=&StartRecord={1}"

display = Display(visible=0, size=(1024, 768))
display.start()
driver = webdriver.Firefox()

limit = 40000
increment = 100
year = "2017"

for i in range(0, limit, increment):
    url = url.format("2017", i)
    try:
        driver.get(url)
    except:
        print "Unable to locate page " + url

    print "Waiting..."
    driver.implicitly_wait(3)

driver.close()
display.stop()
