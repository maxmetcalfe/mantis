# Python script to scrape race results for the Comrades Marathon.
# Max Metcalfe - 6/26/2017

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

# Define the driver / url
url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?results=true&Year={0}&Category=&Club=&StartRecord={1}"
display = Display(visible=0, size=(1024, 768))
display.start()
binary = FirefoxBinary("/usr/bin/firefox")
driver = webdriver.Firefox(firefox_binary=binary)

# Define constants - hardcoded for now.
# To Do: Move these into Jenkins
limit = 300
increment = 100
year = "2017"

# Initialize empty results array
results = []

# Loop through result pages
for i in range(0, limit, increment):
    url = url.format("2017", i)
    print "Gathering data from: " + url
    try:
        driver.get(url)
    except:
        print "Unable to locate page " + url

    if driver:
    	odd = driver.find_elements_by_class_name("rowdd")
    	even = driver.find_elements_by_class_name("roweven")
    	rows = odd + even
        # Loop through rows and cells to gather data
    	for r in rows:
    		result = []
    		cells = r.find_elements_by_class_name("cell")
    		for c in cells:
    			results.append(c.text)

            # Store the result in the results array
	        results.append(result)

    # Wait for a bit to allow the browser to load.
    print "Waiting..."
    time.sleep(2)

# Write results to an ouput CSV file.

print "Writing results to file..."
print str(len(results)) + " results found."
csv_file = open("comrades_" + year + ".csv", "w")

# Write header
csv_file.write("rank, race_no, name, nation, club, time, medal, category\n")

for r in results:
    print r
    csv_file.write(str(r) + "\n")

csv_file.close()

driver.close()
display.stop()