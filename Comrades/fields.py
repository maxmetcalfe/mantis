import requests
import bs4

# Define field transforms
def place(cell, row, args):
    return cell.text.split(" ")[0]

def last(cell, row, args):
	name_split = cell.text.split(" ")
	return " ".join(name_split[1:])

def first(cell, row, args):
    name_split = cell.text.split(" ")
    return name_split[0]

def gender(cell, row, args):
    return cell.text.split(" ")[0]    
    
def age(cell, row, args):
    profile_url = "http://results.ultimate.dk/comrades/resultshistory/front/index.php?profile=true&ProfileID={0}"
    profile_id = row.attrs["onclick"].split("=")[-1].replace("'", "")
    formatted_url = profile_url.format(profile_id)
    response = requests.get(formatted_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    birth_year = soup.find_all("td", "profiledata")[3].text

    return str(int(args.year) - int(birth_year))

def default(cell, row, args):
    return cell.text

# This dictionary lists the configuration for each field.
# The key is the name of the field.
# The cell_index is the cell index for where to fetch the data in a row.
# The transform is a function that transforms the data into the final format.
fields = {
    "place": {
        "cell_index": 0,
        "transform": place
    },
    "place_all": {
        "cell_index": 0,
        "transform": default
    },
    "age": {
        "cell_index": 1,
        "transform": age
    },
    "race_no": {
        "cell_index": 1,
        "transform": default
    },
    "first": {
        "cell_index": 2,
        "transform": first
    },
    "last": {
        "cell_index": 2,
        "transform": last
    },
    "nation": {
        "cell_index": 3,
        "transform": default
    },
    "club": {
        "cell_index": 4,
        "transform": default
    },
    "time": {
        "cell_index": 5,
        "transform": default
    },
    "medal": {
        "cell_index": 6,
        "transform": default
    },
    "gender": {
        "cell_index": 7,
        "transform": gender
    },
    "category": {
        "cell_index": 7,
        "transform": default
    }
}
