from selenium import webdriver

# Quicksilver 100K 2016
driver = webdriver.Firefox()
driver.get("https://ultrasignup.com/entrants_event.aspx?did=34516")
entrant_element = driver.find_element_by_id('ContentPlaceHolder1_lblCount')
print "Quicksilver 100K: " + entrant_element.text
driver.close()

# Pine to Palm 2016
driver = webdriver.Firefox()
driver.get("https://ultrasignup.com/entrants_event.aspx?did=36634")
entrant_element = driver.find_element_by_id('ContentPlaceHolder1_lblCount')
print "Pine to Palm 100: " + entrant_element.text
driver.close()