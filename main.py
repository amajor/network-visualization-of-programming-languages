import csv
import wikipedia
import urllib.request
from bs4 import BeautifulSoup as BS
import re

# Get a list of programming languages from Wikipedia.
# https://en.wikipedia.org/wiki/List_of_programming_languages
pageTitle = "List of programming languages"
nodes = list(wikipedia.page(pageTitle).links)
print("\nNodes found in the page, '{page}':\n{nodes}".format(page=pageTitle, nodes=nodes))

# Remove items from the list that are not programming languages.
# These are lists, timelines, comparisons, etc.
removeList = ["List of", "Lists of", "Timeline", "Comparison of", "History of", "Esoteric programming language"]
nodes = [i for i in nodes if not any(r in i for r in removeList)]

# Base link to Wikipedia.
base = "https://en.wikipedia.org/wiki/"


# Get HTML from a particular page on Wikipedia.
def get_soup(n):
    try:
        with urllib.request.urlopen(base + n) as response:
            soup = BS(response.read(), 'html.parser')
        table = soup.find_all("table", class_="infobox vevent")[0]
        return table
    except:
        pass


# Find the languages that have been influenced by the parameter.
def get_languages_influenced(language_html_infobox):
    try:
        table_rows = language_html_infobox.find_all("tr")
        for i in range(0, len(table_rows) - 1):
            try:
                if table_rows[i].get_text() == "Influenced":
                    out = []
                    for j in table_rows[i + 1].find_all("a"):
                        try:
                            out.append(j['title'])
                        except:
                            continue
                    return out
            except:
                continue
        return
    except:
        return


# Find the languages that the parameter has been influenced by.
def get_languages_influenced_by(language_html_infobox):
    try:
        table_rows = language_html_infobox.find_all("tr")
        for i in range(0, len(table_rows) - 1):
            try:
                if table_rows[i].get_text() == "Influenced by":
                    out = []
                    for j in table_rows[i + 1].find_all("a"):
                        try:
                            out.append(j['title'])
                        except:
                            continue
                    return out
            except:
                continue
        return
    except:
        return


# Discover the year that the language first appeared.
def get_year_first_appeared(language_html_infobox):
    try:
        all_text = language_html_infobox.get_text()
        year = all_text[all_text.find("appear"):all_text.find("appear") + 30]
        year = re.match(r'.*([1-3][0-9]{3})', year).group(1)
        return int(year)
    except:
        return "Could not determine the year first appeared. :("


# Create list objects to store data for each language
separator = ";"
edgeList = [[f"Source{separator}Target{separator}Label".format(separator=separator)]]
meta = [["Id", "Year"]]

# Loop through each node, collecting data and appending to lists.
print("\n\nFinding edges...\n")
for n in nodes:
    try:
        temp = get_soup(n)
    except:
        continue
    try:
        influenced = get_languages_influenced(temp)
        for link in influenced:
            if link in nodes:
                edgeList.append([n + separator + link + separator + n])
                print([n + separator + link])
    except:
        continue

    year = get_year_first_appeared(temp)
    meta.append([n, year])

# Write CSV file for the Edge List (to be used in Gephi).
file_edge_list = "./data/edge_list.csv"
with open(file_edge_list, "w") as f:
    wr = csv.writer(f)
    for e in edgeList:
        wr.writerow(e)

# Write CSV file for the Meta Data List (to be used in Gephi).
file_meta_data = "./data/metadata.csv"
with open(file_meta_data, "w") as f2:
    wr = csv.writer(f2)
    for m in meta:
        wr.writerow(m)

# Print the number of programming languages found (removing lists, comparisons, timelines, etc).
print("\nWe found {languages} programming languages listed in Wikipedia's list of programming languages."
      .format(languages=len(nodes)))

print("  Edge Cases have been written to the file {}".format(file_edge_list))
print("  Meta Data has been written to the file   {}".format(file_meta_data))
