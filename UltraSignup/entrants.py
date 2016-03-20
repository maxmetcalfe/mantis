# Python script to print the number of race entrants from Ultra Signup events.
# Max Metcalfe - 3/19/2016

from pyvirtualdisplay import Display
from selenium import webdriver

# Create virtual display
display = Display(visible=0, size=(1024, 768))
display.start()

# # Quicksilver 100K 2016
# driver = webdriver.Firefox()
# driver.get("https://ultrasignup.com/entrants_event.aspx?did=34516")
# entrant_element = driver.find_element_by_id('ContentPlaceHolder1_lblCount')
# print "Quicksilver 100K: " + entrant_element.text
# driver.close()

# Pine to Palm 2016
driver = webdriver.Firefox()
driver.get("https://ultrasignup.com/entrants_event.aspx?did=36634")
entrant_element = driver.find_element_by_id('ContentPlaceHolder1_lblCount')
print "Pine to Palm 100: " + entrant_element.text
driver.close()
display.stop()