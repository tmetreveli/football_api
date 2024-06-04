"""
Get all the team ids from Premier league
iterate over all the games of the team in that season to find
the best goalscorer, avg. goals per match for each team
and which team has scored the most goals
league id of premier league = 39
"""
import json
# from models import conn, c
from databse_setup import conn, c
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
"""
Iterate through each object of SeasonTeam object(each team in the particular season)
get the results, including points and goals scored
"""
for team in teams:


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

"""
Compare team results, find out tbe team with the most points and
most goals scored
"""
team_with_most_points = max(teams)
team_with_most_goals = max(teams, key=lambda x: x.goals)
print(f"Team with most points {team_with_most_points} : {team_with_most_points.points}, team with most goals {team_with_most_goals}:{team_with_most_goals.goals}")

"""
Load into database
"""
if __name__ == "__main__":

    # Create the season table if it doesn't exist
    c.execute("""CREATE TABLE IF NOT EXISTS season (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        year INTEGER NOT NULL)""")

    # Create the team table if it doesn't exist
    c.execute("""CREATE TABLE IF NOT EXISTS team (
                     id SERIAL PRIMARY KEY,
                     name TEXT NOT NULL,
                     season_id INTEGER,
                     FOREIGN KEY(season_id) REFERENCES season(id))""")

    # Create the team_statistics table if it doesn't exist
    c.execute("""CREATE TABLE IF NOT EXISTS team_statistics (
                     id SERIAL PRIMARY KEY,
                     points INTEGER NOT NULL,
                     goals INTEGER NOT NULL,
                     team_id INTEGER,
                     FOREIGN KEY(team_id) REFERENCES team(id))""")

    # Insert a season record
    c.execute("""INSERT INTO season (name, year) VALUES (%s, %s) RETURNING id""", ("Premier league", season))
    season_id = c.fetchone()[0]

    # Insert team records
    for team in teams:
        c.execute("""INSERT INTO team (name, season_id) VALUES (%s, %s) RETURNING id""", (team.name, season_id))
        team_id = c.fetchone()[0]
        c.execute("""INSERT INTO team_statistics (points, goals, team_id) VALUES (%s, %s, %s)""",
                  (team.points, team.goals, team_id))

    # Commit changes and close the connection
    conn.commit()
    conn.close()