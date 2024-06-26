
"""
Iterate through each object of SeasonTeam
"""


class SeasonTeam:
    def __init__(self, season, name, id, points=0, goals=0):
        self.season = season
        self.name = name
        self.id = id
        self.points = points
        self.goals = goals

    def check_winner(self, data: dict) -> bool:
        print("ID", self.id)

        # print(match)
        print(data["teams"]["home"]["id"])
        if data["teams"]["home"]["id"] == int(self.id):
            print("Home")
            self.goals += data["goals"]["home"]
            return data["teams"]["home"]["winner"]
        else:
            print("Away")
            self.goals += data["goals"]["away"]
            return data["teams"]["away"]["winner"]

    def upgrade_points(self, result):
        if result:
            self.points += 3
        if result is None:
            self.points += 1

    def __lt__(self, other):
        if isinstance(other, SeasonTeam):
            return self.points < other.points
        else:
            raise TypeError

    def __str__(self):
        return self.name
