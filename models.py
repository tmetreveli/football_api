import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


if __name__ == "__main__":
    c.execute("""SELECT team.name, team_statistics.points, team_statistics.goals 
                 FROM team_statistics 
                 INNER JOIN team ON team_statistics.team_id = team.id 
                 ORDER BY team_statistics.points DESC""")
    rows = c.fetchall()

    for row in rows:
        print(row)
