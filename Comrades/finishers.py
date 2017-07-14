# Python script to scrape race results for the Comrades Marathon.
# Max Metcalfe - 6/26/2017

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import codecs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--limit', help='The limit for the StartRecord.', type=int)
parser.add_argument('--year', help='The year of the Comrades race.')
parser.add_argument('--increment', help='How many results per page.', type=int)
parser.add_argument('--row', help='Which row type odd/even.')
args = parser.parse_args()

# Define the driver / urls
url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?results=true&Year={0}&Category=&Club=&StartRecord={1}"
profile_url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?profile=true&ProfileID={0}"
display = Display(visible=0, size=(200, 200))
display.start()
binary = FirefoxBinary("/usr/bin/firefox")
driver = webdriver.Firefox(firefox_binary=binary)

def get_element(parent_element, class_name, attempts):
	for i in range(attempts):
		try:
			element = parent_element.find_elements_by_class_name(class_name)
			if element:
				return element
		except:
			print "Can't get element. Trying again..."

# Get the racer age from the racer profile.
# This involves another page view.
def get_age(year, profile_id):
    formatted_url = profile_url.format(profile_id)
    age_driver = webdriver.Firefox(firefox_binary=binary)
    try:
        age_driver.get(formatted_url)
    except:
        print "Unable to locate page " + formatted_url

    if driver:
		birth_year = get_element(age_driver, "profiledata", 3)[3].text
		age_driver.close()
		return int(year) - int(birth_year)
    else:
		print "Invalid row."

def encode_text(text):
    return unicode(text).encode("utf-8")

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
		odd = get_element(driver, "rowodd", 3)
		even = get_element(driver, "roweven", 3)
		if args.row == "even":
			rows = even
		elif args.row == "odd":
			rows = odd
		else:
			rows = odd + even
        # Loop through rows and cells to gather data
		for r in rows:
			result = ""
			cells = get_element(r, "cell", 3)
			i = 0
			for cell in cells:
				text = cell.text

				if i == 0:
					place = text.split(" ")[0]
				elif i == 1:
					race_no = text
					profile_id = r.get_attribute('onclick').split("=")[-1].replace("'", "")
					age = encode_text(get_age(args.year, profile_id))
				elif i == 2:
					name_split = text.split(" ")
					first = encode_text(name_split[0])
					last = encode_text(" ".join(name_split[1:]))
				elif i == 5:
					time = text
				elif i == 7:
					gender = text.split(" ")[0]

				# Increment the counter
				i += 1

			# Assemble the data into CSV form.
			print place, time, first, last, age, gender
			result = place + "," + time + "," + first + "," + last + "," + age + "," + gender
			# Store the result in the results array
			results.append(result)

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
