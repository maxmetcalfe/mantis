# Python script to scrape race results for the Comrades Marathon.
# Max Metcalfe - 6/26/2017

import bs4
import requests
import codecs
import argparse
import sys
from termcolor import colored
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--limit", help="The limit for the StartRecord.", type=int)
parser.add_argument("--year", help="The year of the Comrades race.")
parser.add_argument("--increment", help="How many results per page.", type=int, default=100)
parser.add_argument("--row", help="even or odd rows", default="even")
parser.add_argument("--local", help="Do you want to test this on a local server", type=bool, default=False)
parser.add_argument("--out", help="Output file directory", default="./")
args = parser.parse_args()

# Map row types to row class names
row_classes = {
	"odd": "rowodd",
	"even": "roweven"
}

# Define the urls
url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?results=true&Year={0}&Category=&Club=&StartRecord={1}"
url_local = "http://localhost:8080"
profile_url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?profile=true&ProfileID={0}"

# If we are running a local server, use url_local
if args.local:
	url = url_local

# Keep track of which cells contain which data.
field_cell_indices = {
	"place": 0,
	"name": 2,
	"time": 5,
	"gender": 7
}

# Build a template for an output result
result_template = {
	"place": "",
	"time": "",
	"first": "",
	"last": "",
	"age": "",
	"gender": ""
}

# Keep track of the order of the output fields (and the header)
fields_ordered = ["place", "time", "first", "last", "age", "gender"]

# Fetch the age for a racer, returned as a string.
def get_age(year, profile_id):
	formatted_url = profile_url.format(profile_id)
	response = requests.get(formatted_url)
	soup = bs4.BeautifulSoup(response.text, "html.parser")
	birth_year = soup.find_all("td", "profiledata")[3].text

	return str(int(year) - int(birth_year))

# Get a result from a result row
def get_result_from_row(row):
	cells = row.find_all("td")

	result = result_template.copy()

	i = 0
	for cell in cells:

		# Finish place
		if i == field_cell_indices["place"]:
			result["place"] = cell.text.split(" ")[0]

		# Name
		if i == field_cell_indices["name"]:
			name_split = cell.text.split(" ")
			result["first"] = name_split[0]
			result["last"] = " ".join(name_split[1:])

		# Time
		if i == field_cell_indices["time"]:
			result["time"] = cell.text

		# Gender
		if i == field_cell_indices["gender"]:
			result["gender"] = cell.text.split(" ")[0]

		# Increment cell number
		i += 1

	# Age requires an additional request to the profile page
	profile_id = row.attrs["onclick"].split("=")[-1].replace("'", "")
	result["age"] = get_age(args.year, profile_id)

	return result

# Write an array of results to an output CSV file.
def write_file(filename, results):
	header = str(fields_ordered).replace("'", "").replace("[", "").replace("]", "") + "\n"
	csv_file = codecs.open(filename, "w", encoding="utf-8")
	csv_file.write(header)

	for result in results:
		string_result = ""
		for field in fields_ordered:
			string_result = string_result + result[field] + ","
		csv_file.write(string_result + "\n")

	# We are done. Close 'em up.
	csv_file.close()

# The main function
def main():

	startTime = datetime.now()
	total_results = 0

	if args.row not in row_classes.keys():
		print colored("Please provide a valid row type.", "red")
		sys.exit(1)
	else:
		row_class = row_classes[args.row]

	# Loop through result pages
	for i in range(0, args.limit, args.increment):

		# Initialize empty results array
		results = []

		formatted_url = url.format(args.year, str(i))
		print colored("Collecting data from: " + formatted_url, "blue")
		response  = requests.get(formatted_url)

		if response.status_code != 200:
			print colored("Error loading page.", "red")

		if response.status_code == 200:
			soup = bs4.BeautifulSoup(response.text, "html.parser")
			rows = soup.find_all("tr", row_class)

			for row in rows:
				results.append(get_result_from_row(row))
		
		total_results = total_results + len(results)
		filename = args.out + "/" + "comrades_" + args.year + "-" + str(i) + "-" + args.row + ".csv"
		write_file(filename, results)
	
	print colored("- Done.", "green")
	print colored("- Pages loaded: " + str(i + 1) + ".", "green")
	print colored("- Results logged: " + str(total_results) + ".", "green")
	print colored("- Duration: " + str(datetime.now() - startTime) + ".", "green")
	print colored("- Files writeen to " + args.out, "green")

main()
