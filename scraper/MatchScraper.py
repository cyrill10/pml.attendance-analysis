import time
import requests
from bs4 import BeautifulSoup


def extract_game_data(game_url, match_file):
    page = requests.get(game_url, allow_redirects=False)
    if page.status_code == 200:
        home_team = ""
        away_team = ""
        result = ""
        date = ""
        match_time = ""
        stadium = ""
        attendance = ""
        match_day = ""
        html = page.content.decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        page_tables = soup.findAll("table", {"class": "standard_tabelle"})

        try:
            teams_table = page_tables[0].findAll("tr")[0].findAll("th")

            home_team = teams_table[0].a.contents[0]
            away_team = teams_table[2].a.contents[0]
            result = page_tables[0].find("div",  {"class": "resultat"}).contents[0].strip()
            date = teams_table[1].contents[0].strip()
            match_time = teams_table[1].contents[2].strip().split(" ")[0]

            meta_table = page_tables[len(page_tables)-1].findAll("td")

            stadium = meta_table[2].a.contents[0]
            attendance = meta_table[5].contents[0].strip().replace(".", "")

            match_day = soup.findAll("select", {"name": "phase2"})[0].find("option", {
                "selected": "selected"})['value'].split("/")[-2]
        except IndexError:
            print("Index Error: " + " " + game_url)
        except TypeError:
            print("Type Error: " + " " + game_url)

        match_file.write(date + "," + match_time + "," + stadium + "," + attendance + "," + home_team +
                         "," + away_team + "," + match_day + "," + result + "\n")
        return 0
    else:
        return -1


def easy_fix_url(url, match_file):
    success_new = -1
    if "Grasshoppers" in url:
        success_new = extract_game_data(url.replace("Grasshoppers", "Grasshopper-Club"), match_file)
        if success_new == -1:
            if "_2" in url:
                success_new = extract_game_data(url.replace("Grasshoppers", "Grasshopper-Club").replace("_2", ""),
                                                match_file)
                if success_new == -1:
                    print("could not easyFix GCZ1")
                else:
                    print("easyFix GCZ1 worked")
            else:
                print("could not easyFix GCZ1")
        else:
            print("easyFix GCZ1 worked")
    if "Grasshopper-Club" in url:
        success_new = extract_game_data(url.replace("Grasshopper-Club", "Grasshoppers"), match_file)
        if success_new == -1:
            if "_2" in url:
                success_new = extract_game_data(url.replace("Grasshopper-Club", "Grasshoppers").replace("_2", ""), match_file)
                if success_new == -1:
                    print("could not easyFix GCZ2")
                else:
                    print("easyFix GCZ2 worked")
            else:
                print("could not easyFix GCZ2")
        else:
            print("easyFix GCZ2 worked")

    if "Neuchatel-Xamax-FC" in url:
        success_new = extract_game_data(url.replace("Neuchatel-Xamax-FC", "Neuchatel-Xamax").replace("_2", ""),
                                        match_file)
        if success_new == -1:
            print("could not easyFix Xamax")
        else:
            print("easyFix Xamax worked")
    if "FC-Thun" in url:
        success_new = extract_game_data(url.replace("_2", "-1898"),
                                            match_file)
        if success_new == -1:
            print("could not easyFix Thun")
        else:
            print("easyFix Thun worked")
    return success_new


teamData = open("../data/teams_per_season.csv", "r")

matchFile = open("../data/matches.csv", "a")

matchURL = "https://www.weltfussball.com/spielbericht/super-league-{year1}-{year2}-{homeTeam}-{awayTeam}{index}/"

for line in teamData:
    if not line.startswith("2017") and not line.startswith("2018"):
        line = line.replace("Grasshopper Club", "Grasshoppers")
    if line.startswith("2003"):
        line = line.replace("Xamax FC", "Xamax FCS")
    if line.startswith("2004") or line.startswith("2005"):
        line = line.replace("Xamax FC", "Xamax")
    if line.startswith("2004"):
        line = line.replace("Genève", "Genf")
    if line.startswith("2005"):
        line = line.replace("Yverdon-Sport FC", "Yverdon-Sport")
    values = line.replace(" ", "-").replace("â", "a").replace("è", "e").replace("ü", "ue").replace(".", "") \
        .replace("\n", "").split(",")
    year = values[0]
    teams = values[1:]
    for i, team in enumerate(teams):
        for ii in range(0, 10):
            if i != ii:
                urlFirstGame = matchURL.format(year1=year, year2=str(int(year) + 1), homeTeam=team, awayTeam=teams[ii],
                                               index="")
                urlSecondGame = matchURL.format(year1=year, year2=str(int(year) + 1), homeTeam=team, awayTeam=teams[ii],
                                                index="_2")

                # Wait for 1 seconds to not trigger any call limits
                time.sleep(1)

                success1 = extract_game_data(urlFirstGame, matchFile)
                if success1 == -1:
                    successEasyFix1 = easy_fix_url(urlFirstGame, matchFile)
                    if successEasyFix1 == -1:
                        print("Bad URL: " + " " + urlFirstGame)
                # # Wait for 1 seconds to not trigger any call limits
                time.sleep(1)

                success2 = extract_game_data(urlSecondGame, matchFile)
                if success2 == -1:
                    successEasyFix2 = easy_fix_url(urlSecondGame, matchFile)
                    if successEasyFix2 == -1:
                        print("Bad URL: " + " " + urlSecondGame)

        print("done " + year + " " + team)

teamData.close()
matchFile.close()
