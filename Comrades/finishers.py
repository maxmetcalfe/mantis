# Python script to scrape race results for the Comrades Marathon.
# Max Metcalfe - 6/26/2017

import bs4
import requests
import codecs
import argparse
import sys
from fields import *
from termcolor import colored
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--limit", help="The limit for the StartRecord.", type=int)
parser.add_argument("--year", help="The year of the Comrades race.")
parser.add_argument("--increment", help="How many results per page.", type=int, default=100)
parser.add_argument("--startRecord", help="Record number to start from.", type=int, default=0)
parser.add_argument("--row", help="even or odd rows", default="even")
parser.add_argument("--fields", help="comma-separated list of fields, in order", default="place,first,last,time")
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

# If we are running a local server, use url_local
if args.local:
	url = url_local

target_fields = args.fields.split(",")

# Fetch the age for a racer, returned as a string.
def get_age(year, profile_id):
	formatted_url = profile_url.format(profile_id)
	response = requests.get(formatted_url)
	soup = bs4.BeautifulSoup(response.text, "html.parser")
	birth_year = soup.find_all("td", "profiledata")[3].text

	return str(int(year) - int(birth_year))

# Get a result from a result row
def get_result_from_row(row, target_fields):
	cells = row.find_all("td")

	result = {}

	for target_field in target_fields:
		field_config = fields[target_field]
		result[target_field] = field_config["transform"](cells[field_config["cell_index"]], row, args)

	return result

# Write an array of results to an output CSV file.
def write_file(filename, results):
	header = str(target_fields).replace("'", "").replace("[", "").replace("]", "") + "\n"
	csv_file = codecs.open(filename, "w", encoding="utf-8")
	csv_file.write(header)

	for result in results:
		string_result = ""
		for field in target_fields:
			string_result = string_result + result[field] + ","
		csv_file.write(string_result[:-1] + "\n")

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

	if args.startRecord % args.increment > 0:
		print colored("Please provide a valid startRecord.", "red")
		sys.exit(1)

	# Loop through result pages
	for i in range(args.startRecord, args.limit, args.increment):

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
				results.append(get_result_from_row(row, target_fields))
		
		total_results = total_results + len(results)
		filename = args.out + "/" + "comrades_" + args.year + "-" + str(i) + "-" + args.row + ".csv"
		write_file(filename, results)
	
	print colored("- Done.", "green")
	print colored("- Pages loaded: " + str(i + 1) + ".", "green")
	print colored("- Results logged: " + str(total_results) + ".", "green")
	print colored("- Duration: " + str(datetime.now() - startTime) + ".", "green")
	print colored("- Files writeen to " + args.out, "green")

main()
