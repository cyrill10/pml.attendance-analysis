from urllib.request import urlopen
from bs4 import BeautifulSoup

MAIN_PATH = "https://www.weltfussball.com/spielplan/sui-super-league-{}-{}-spieltag/{}/"

latestSeason = 2002
LAST_SEASON = 2010

NUM_MATCHDAYS = 36

file = open("league-table.csv", "a")

while latestSeason < LAST_SEASON:
    latestSeason += 1
    latestMatchday = 0
    while latestMatchday < NUM_MATCHDAYS:
        latestMatchday += 1
        page = urlopen(MAIN_PATH.format(latestSeason, latestSeason+1, latestMatchday))
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        table = soup.findAll("table", {"class": "standard_tabelle"})[1].findAll("tr")
        for i in range(1, 11):
            columns = table[i].findAll("td")
            pos = i
            name = columns[2].a.contents[0]
            win = columns[4].contents[0]
            draw = columns[5].contents[0]
            lose = columns[6].contents[0]
            goalSepIndex = columns[7].contents[0].index(":")
            gf = columns[7].contents[0][:goalSepIndex]
            ga = columns[7].contents[0][goalSepIndex+1:]
            points = columns[9].contents[0]

            file.write(str(latestSeason) + "," + str(latestMatchday) + "," + str(pos) + "," + name + "," + win + "," + draw + "," + lose + "," + gf + "," + ga + "," + points +"\n")
    print("done " + str(latestSeason))