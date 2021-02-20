import numpy as np
import pandas as pd
from datetime import datetime
import locale

team_coordinates_df = pd.read_csv('../data/team_coordinates.csv', index_col=0, header=0)
league_table_df = pd.read_csv('../data/league-table.csv', index_col=0, header=0)


def custom_date_parser(x):
    result = []
    locale.setlocale(locale.LC_ALL, 'de_DE')
    for value in x:
        result.append(datetime.strptime(value, ' %d. %B %Y'))
    return result


def calc_dist(hometeam, awayteam):
    home = team_coordinates_df.loc[hometeam]
    away = team_coordinates_df.loc[awayteam]
    home_array = np.array((home[0], home[1]))
    away_array = np.array((away[0], away[1]))
    return np.linalg.norm(home_array - away_array)


def determine_season(date: datetime):
    year = date.year
    if date.month <= 6:
        year -= 1
    return year


def calc_point_average_before_game(season, matchday, team):
    matchday -= 1
    if matchday == 0:
        return 0
    table = league_table_df.loc[season]
    mask = np.logical_and(table['matchday'] == matchday, table['team'] == team)
    points = table[mask]
    return points['points'][season]/matchday
