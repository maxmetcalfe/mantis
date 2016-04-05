# Python script to print the number of race entrants from Ultra Signup events.
# Max Metcalfe - 3/19/2016

from pyvirtualdisplay import Display
from selenium import webdriver
import argparse
import smtplib
import json
import collections
import string
import os

parser = argparse.ArgumentParser()
parser.add_argument( "-u", "--user", help="gmail username", required=True )
parser.add_argument( "-p", "--password", help="gmail password", required=True  )
parser.add_argument( "-r", "--recipients", help="recipients", required=True  )
args = parser.parse_args()

# Load race JSON from file
with open('races.json') as race_file:
    race_json = json.load(race_file)

# Email settings
fromaddr = args.user
msg = ""
subject = "Ultra Signup Digest"

# Sort JSON alphabetically by name
race_json_sorted = collections.OrderedDict(sorted(race_json.items()))

display = Display(visible=0, size=(1024, 768))
display.start()
driver = webdriver.Firefox()

first = True
# Loop through races and gather entrant count
for name,id in race_json_sorted.iteritems():
    print name,id
    try:
        driver.get("https://ultrasignup.com/entrants_event.aspx?did=" + str(id))
        entrant_element = driver.find_element_by_id('ContentPlaceHolder1_lblCount')
    	msg = msg + name + ": " + entrant_element.text + "\n" + "https://ultrasignup.com/entrants_event.aspx?did=" + str(id) + "\n\n"
    except:
        print "Unable to locate element: " + name + "," + str(id)

driver.close()
display.stop()

# Make list out of args.recipients string
recipients = string.split(args.recipients, ",")

# Prepare email
msg = """\
From: %s
To: %s
Subject: %s

%s
""" % (fromaddr, ", ".join(recipients), subject, msg)

# Send email
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(args.user,args.password)
server.sendmail(fromaddr, recipients, msg)
server.quit()