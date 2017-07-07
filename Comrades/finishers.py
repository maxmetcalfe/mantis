# Python script to scrape race results for the Comrades Marathon.
# Max Metcalfe - 6/26/2017

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import codecs

parser = argparse.ArgumentParser()
parser.add_argument('--limit', help='The limit for the StartRecord.')
parser.add_argument('--year', help='The year of the Comrades race.')
args = parser.parse_args()

# Define the driver / url
url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?results=true&Year={0}&Category=&Club=&StartRecord={1}"
display = Display(visible=0, size=(200, 200))
display.start()
binary = FirefoxBinary("/usr/bin/firefox")
driver = webdriver.Firefox(firefox_binary=binary)

# Define increment for result page.
# How many results on each page.
increment = 100

# Initialize empty results array
results = []

# Loop through result pages
for i in range(0, args.limit, increment):
    formatted_url = url.format(args.year, str(i))
    print "Gathering data from: " + formatted_url
    try:
        driver.get(formatted_url)
    except:
        print "Unable to locate page " + formatted_url

    if driver:
        odd = driver.find_elements_by_class_name("rowodd")
        even = driver.find_elements_by_class_name("roweven")
        rows = odd + even
        # Loop through rows and cells to gather data
        for r in rows:
            result = ""
            cells = r.find_elements_by_class_name("cell")
            for c in cells:
                t=unicode(c.text)
                t.encode("utf-8")
                result += t + ","

            # Store the result in the results array
            results.append(result[:-1])

    # Wait for a bit to allow the browser to load.
    print "Waiting..."
    time.sleep(2)

# Write results to an ouput CSV file.

print "Writing results to file..."
print str(len(results)) + " results found."
csv_file = codecs.open("comrades_" + year + ".csv", "w", encoding="utf-8")

# Write header
csv_file.write("rank, race_no, name, nation, club, time, medal, category\n")

for r in results:
    line = unicode(r)
    line.encode("utf-8")
    csv_file.write(line + "\n")

csv_file.close()

driver.close()
display.stop()