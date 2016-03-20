# Python script to print the number of race entrants from Ultra Signup events.
# Max Metcalfe - 3/19/2016

from pyvirtualdisplay import Display
from selenium import webdriver
import argparse
import smtplib

parser = argparse.ArgumentParser()

# To Do - make this secure :)
parser.add_argument( "-u", "--user", help="gmail username", required=True )
parser.add_argument( "-p", "--password", help="gmail password", required=True  )
args = parser.parse_args()
username = args.user
password = args.password

# Email settings
fromaddr = args.user
toaddrs  = 'm.maxmetcalfe@gmail.com'
msg = ""
subject = "Ultra Signup Update"

# Race list. Name + event ID
races = [("Quicksilver 100K 2016", 34515),
	("Pine to Palm 2016", 36634),
	("Miwok 100K 2016", 33379),
	("Lake Sonoma 50 Miler 2016", 32787)
]

# Loop through races and gather entrant count
for name, id in races:
	display = Display(visible=0, size=(1024, 768))
	display.start()
	driver = webdriver.Firefox()
	driver.get("https://ultrasignup.com/entrants_event.aspx?did=" + str(id))
	entrant_element = driver.find_element_by_id('ContentPlaceHolder1_lblCount')
	msg = msg + "\n" + name + " " + entrant_element.text
	driver.close()
	display.stop()

# Prepare email
msg = """\
From: %s
To: %s
Subject: %s

%s
""" % (fromaddr, toaddrs, subject, msg)

# Send email
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(args.user,args.password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()