import requests


class Standings:
    def __init__(self):
        self.api_key = '91b81278ac054507925fad5bf4b604af'
        self.base_url = 'https://api.football-data.org/v4/'
        self.headers = {
            "X-Auth-Token": self.api_key
        }

    def league_mapper(self,country):
        data = {
            'United Kingdom': 'PL',
            'Germany': 'BL1',
            'France': 'FL1',
            'Italy': 'SA',
            'Spain': 'PD',
            'Brazil': 'BSA',
            'Portugal': 'PPL',
            'Netherlands': 'DED'
        }

        if country in data.keys():
            return data[country]
        else:
            return False
    def get_standings(self,country):
        league_id = self.league_mapper(country)
        if not league_id:
            return False
        else:
            url = f"{self.base_url}competitions/{league_id}/standings"
            response = requests.get(url, headers=self.headers)
            standings = []
            if response.status_code == 200:
                data = response.json()
                for group in data.get("standings", []):
                    if group["type"] == "TOTAL":  # Overall standings
                        for team in group["table"]:
                            standings.append({
                                "position": team["position"],
                                "name": team["team"]["name"],
                                "crest": team["team"]["crest"],
                                "points": team["points"],
                                "played": team["playedGames"],
                                "won": team["won"],
                                "draw": team["draw"],
                                "lost": team["lost"],
                                "goal_difference": team["goalDifference"]
                            })
            else:
                standings = {"error": "Failed to fetch league standings"}
            return standings

