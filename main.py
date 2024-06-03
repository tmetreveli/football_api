"""
Get all the team ids from Premier league
iterate over all the games of the team in that season to find
the best goalscorer, avg. goals per match for each team
and which team has scored the most goals
league id of premier league = 39
"""
import json

from football_api.utils import url_for_team_fixtures, headers_for_team_fixtures, league_id, season, url_for_team_ids, \
    headers_for_team_ids, querystring_for_team_ids
import requests
from football_api.seasonTeam import SeasonTeam

"""
Getting all the team ids from Premier league
"""

response = requests.get(url_for_team_ids, headers=headers_for_team_ids, params=querystring_for_team_ids)

entries = response.json()["response"]
teams = [] # Initialize empty list for teams in the league for the particular season
for team in entries:
    teams.append(SeasonTeam(season=season, name=team["team"]["name"], id=team["team"]["id"]))

"""
Iterate through all the games of each team in that season
"""
count = 0
for team in teams:

    if count > 0:
        break
    querystring_for_team_fixtures = {"league": league_id, "season": season, "team": team.id}

    response = requests.get(url_for_team_fixtures, headers=headers_for_team_fixtures,
                            params=querystring_for_team_fixtures)
    response_json = response.json()
    # print(json.dumps(response_json, indent=4))
    games = 0
    for game in response_json["response"]:
        print(json.dumps(game, indent=4))
        print("Result", game["teams"]["home"]["winner"])
        result = team.check_winner(game)
        team.upgrade_points(result)

    print(team.name, team.id, team.points, team.goals)
    count += 1

"""
Iterate through each object of SeasonTeam object(each team in the particular season)
get the results, including poits and goals scored
"""
