import requests
import csv

MAIN_PATH = "https://data.geo.admin.ch/ch.meteoschweiz.klima/nbcn-tageswerte/nbcn-daily_{}_previous.csv"


with open('../data/team_coordinates.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            r = requests.get(MAIN_PATH.format(row[3]), allow_redirects=True)
            file = open("../data/weather/" + row[3] + ".csv", "wb")
            file.write(r.content)
            file.close()
        line_count += 1
