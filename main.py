import csv
import wikipedia
import urllib.request
from bs4 import BeautifulSoup as BS
import re

# Get a list of programming languages from Wikipedia.
# https://en.wikipedia.org/wiki/List_of_programming_languages
pageTitle = "List of programming languages"
nodes = list(wikipedia.page(pageTitle).links)
print(nodes)
print("\nWe found {items} items listed in Wikipedia's list of programming languages.".format(items=len(nodes)))

# Remove items from the list that are not programming languages.
# These are lists, timelines, comparisons, etc.
removeList = ["List of", "Lists of", "Timeline", "Comparison of", "History of", "Esoteric programming language"]
nodes = [i for i in nodes if not any(r in i for r in removeList)]
print("We found {languages} programming languages listed in Wikipedia's list of programming languages."
      .format(languages=len(nodes)))

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


temp_html_infobox = get_soup('JavaScript')
print("\nJavaScript HTML:\n {soup}".format(soup=temp_html_infobox))


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


temp_languages_influenced = get_languages_influenced(temp_html_infobox)
print("\nJavaScript influenced:\n {influenced}".format(influenced=temp_languages_influenced))

temp_languages_influenced_by = get_languages_influenced_by(temp_html_infobox)
print("\nJavaScript was influenced by:\n {influenced_by}".format(influenced_by=temp_languages_influenced_by))

# # get some metadata
# def getYear(t):
#     try:
#         t = t.get_text()
#         year = t[t.find("appear"):t.find("appear") + 30]
#         year = re.match(r'.*([1-3][0-9]{3})', year).group(1)
#         return int(year)
#     except:
#         return "Could not determine :("
#
# # create list objects to store data
# edgeList = [["Source,Target"]]
# meta = [["Id", "Year"]]
#
# # go through each node, use functions defined earlier to collect data and append to lists
# for n in nodes:
#     try:
#         temp = getSoup(n)
#     except:
#         continue
#     try:
#         influenced = getLinks(temp)
#         for link in influenced:
#             if link in nodes:
#                 edgeList.append([n + "," + link])
#                 print([n + "," + link])
#     except:
#         continue
#
#     year = getYear(temp)
#     meta.append([n, year])
#
# # finally - write CSV files to import into Gephi
# with open("./data/edge_list.csv", "w") as f:
#     wr = csv.writer(f)
#     for e in edgeList:
#         wr.writerow(e)
#
# with open("./data/metadata.csv", "w") as f2:
#     wr = csv.writer(f2)
#     for m in meta:
#         wr.writerow(m)
