from urllib.request import urlopen
from bs4 import BeautifulSoup

MAIN_PATH = "https://www.weltfussball.com/spielplan/sui-super-league-{}-{}-spieltag/{}/"

latestSeason = 2002
LAST_SEASON = 2018


file = open("../data/teams_per_season.csv", "a")

while latestSeason < LAST_SEASON:
    latestSeason += 1
    page = urlopen(MAIN_PATH.format(latestSeason, latestSeason+1, 1))
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    table = soup.findAll("table", {"class": "standard_tabelle"})[1].findAll("tr")
    names = [10]
    file.write(str(latestSeason))
    for i in range(1, 11):
        columns = table[i].findAll("td")
        file.write("," + columns[2].a.contents[0])
    file.write("\n")
    print("done " + str(latestSeason))
