import csv
import wikipedia
import urllib.request
from bs4 import BeautifulSoup as BS
import re

# get a list of programming languages from Wikipedia
pageTitle = "List of programming languages"
nodes = list(wikipedia.page(pageTitle).links)
print(nodes)

# remove unwanted links
removeList = ["List of", "Lists of", "Timeline", "Comparison of", "History of", "Esoteric programming language"]
nodes = [i for i in nodes if not any(r in i for r in removeList)]

# define some functions
base = "https://en.wikipedia.org/wiki/"


# get HTML
def getSoup(n):
    try:
        with urllib.request.urlopen(base + n) as response:
            soup = BS(response.read(), 'html.parser')
        table = soup.find_all("table", class_="infobox vevent")[0]
        return table
    except:
        pass


# get some metadata
def getYear(t):
    try:
        t = t.get_text()
        year = t[t.find("appear"):t.find("appear") + 30]
        year = re.match(r'.*([1-3][0-9]{3})', year).group(1)
        return int(year)
    except:
        return "Could not determine :("


# function to find the links for a given language
def getLinks(t):
    try:
        table_rows = t.find_all("tr")
        for i in range(0, len(table_rows) - 1):
            try:
                if table_rows[i].get_text() == "\nInfluenced\n":
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


# create list objects to store data
edgeList = [["Source,Target"]]
meta = [["Id", "Year"]]

# go through each node, use functions defined earlier to collect data and append to lists
for n in nodes:
    try:
        temp = getSoup(n)
    except:
        continue
    try:
        influenced = getLinks(temp)
        for link in influenced:
            if link in nodes:
                edgeList.append([n + "," + link])
                print([n + "," + link])
    except:
        continue

    year = getYear(temp)
    meta.append([n, year])

# finally - write CSV files to import into Gephi
with open("./data/edge_list.csv", "w") as f:
    wr = csv.writer(f)
    for e in edgeList:
        wr.writerow(e)

with open("./data/metadata.csv", "w") as f2:
    wr = csv.writer(f2)
    for m in meta:
        wr.writerow(m)
