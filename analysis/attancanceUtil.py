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


def time_categorizer(x):
    result = []
    locale.setlocale(locale.LC_ALL, 'de_DE')
    for value in x:
        time = datetime.strptime(value, '%H:%M')
        afternoonSplit = datetime.strptime('15:00', '%H:%M')
        eveningSplit = datetime.strptime('18:30', '%H:%M')
        if time < afternoonSplit:
            result.append("noon")
        elif time < eveningSplit:
            result.append("afternoon")
        else:
            result.append("evening")
    return result


def matchday_categorizer(x):
    result = []
    for value in x:
        if value < 36/4:
            result.append("first_quarter")
        elif value < 36/2:
            result.append("second_quarter")
        elif value < 3*36/4:
            result.append("third_quarter")
        else:
            result.append("fourth_quarter")
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
    point_df = table[mask]
    points = point_df['points'][season]
    if season == 2004 and team == 'Servette Genève':
        points += 3
    if season == 2011 and team == 'FC Sion':
        points += 36
    return points/matchday


def calc_postion_before_game(season, matchday, team):
    matchday -= 1
    if matchday == 0:
        matchday = 1
    table = league_table_df.loc[season]
    mask = np.logical_and(table['matchday'] == matchday, table['team'] == team)
    table_df = table[mask]
    position = table_df['place'][season]
    return position


def calc_last_seasons_position(season, team):
    season -= 1
    table = league_table_df.loc[season]
    mask = np.logical_and(table['matchday'] == 36, table['team'] == team)
    table_df = table[mask]
    if table_df.empty:
        position = 10
    else:
        position = table_df['place'][season]
    return position


def calc_point_average_from_last_five_games(season, matchday, team, attendance_df):
    if matchday == 1:
        return 0
    matchdays = np.arange(matchday-min(5, matchday-1), matchday)
    home_mask = np.logical_and(attendance_df['hometeam'] == team, attendance_df['season'] == season)
    away_mask = np.logical_and(attendance_df['awayteam'] == team, attendance_df['season'] == season)
    home_df = attendance_df[home_mask].copy()
    away_df = attendance_df[away_mask].copy()
    home_df[['for', 'against']] = home_df['result'].str.split(":", expand=True)
    away_df[['against', 'for']] = away_df['result'].str.split(":", expand=True)
    home_results = home_df[home_df['matchday'].isin(matchdays)]
    away_results = away_df[away_df['matchday'].isin(matchdays)]
    results = pd.concat([home_results, away_results], ignore_index=True)
    results['points'] = np.where(results['for'] > results['against'], 3,
                                 np.where(results['for'] == results['against'], 1, 0))
    return sum(results.loc[:, 'points']) / len(results)


def calc_weather_data(date, hometeam):
    weather_station = team_coordinates_df.loc[hometeam][2]
    weather_df = pd.read_csv('../data/weather/' + weather_station + '.csv',
                             sep=';', index_col=1, header=0)
    date = int(date.strftime("%Y%m%d"))
    rain = weather_df.loc[date]['rre150d0']
    sun = weather_df.loc[date]['sre000d0']
    avg_temp = weather_df.loc[date]['tre200d0']
    return rain, sun, avg_temp


def calc_weather_data2(date, hometeam):
    rain = 1
    sun = 5
    avg_temp = 8
    return rain, sun, avg_temp
