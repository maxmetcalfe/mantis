# Python script to scrape race results for the Comrades Marathon.
# Max Metcalfe - 6/26/2017

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import codecs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--limit', help='The limit for the StartRecord.', type=int)
parser.add_argument('--year', help='The year of the Comrades race.')
parser.add_argument('--increment', help='How many results per page.')
args = parser.parse_args()

# Define the driver / urls
url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?results=true&Year={0}&Category=&Club=&StartRecord={1}"
profile_url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?profile=true&ProfileID={0}"
display = Display(visible=0, size=(200, 200))
display.start()
binary = FirefoxBinary("/usr/bin/firefox")
driver = webdriver.Firefox(firefox_binary=binary)

# Get the racer age from the racer profile.
# This involves another page view.
def get_age(year, race_no):
    print "Sourcing age from profile: " + race_no
    url = profile_url.format(race_no)
    try:
        driver.get(url)
    except:
        print "Unable to locate page " + url

    if driver:
        row = driver.find_elements_by_class_name("rowodd")[0]
        birth_year = r.find_elements_by_class_name("cell")[2]

    return int(year) - int(birth_year)

def encode(text):
    return unicode(c.text).encode("utf-8")

# Initialize empty results array
results = []

# Loop through result pages
for i in range(0, args.limit, args.increment):
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
            for i, c in enumerate(cells):
                if i == 0:
                    place = c.text.split(" ")[0]
                elif i == 1:
                    race_no = c.text
                    age = get_age(args.year, race_no)
                elif i == 2:
                    name_split = c.text.split(" ")
                    first = encode(name_split[0])
                    last = encode(" ".join(name_split[1:]))
                elif i == 5:
                    time = c.text
                elif i == 7:
                    gender = c.text.split(" ")[0]

                # Assemble the data into CSV form.
                result = place + "," + time + "," + first + "," + last + "," + age + "," + gender

            # Store the result in the results array
            results.append(result)

    # Wait for a bit to allow the browser to load.
    print "Waiting..."
    time.sleep(2)

# Write results to an ouput CSV file.

print "Writing results to file..."
print str(len(results)) + " results found."
csv_file = codecs.open("comrades_" + args.year + ".csv", "w", encoding="utf-8")

# Write results to the output file
csv_file.write("place, time, first, last, age, gender\n")
for r in results:
    line = encode(r)
    csv_file.write(line + "\n")

# We are done. Close 'em up.
csv_file.close()
driver.close()
display.stop()