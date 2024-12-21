import requests


class Team_Helper:
    def __init__(self):
        self.base_url = "https://free-api-live-football-data.p.rapidapi.com/"
        self.headers = {
            "x-rapidapi-key": "845c790af6mshf64b3e0b51ac50ep1b8771jsnc6626df1faa1",
            "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
        }

    def find_team_id(self,team_name):
        url = f"{self.base_url}football-teams-search"
        querystring = {"search": team_name}
        response = requests.get(url, headers=self.headers, params=querystring).json()
        for team_dict in response['response']['suggestions']:
            if team_dict['name'] == team_name:
                return team_dict['id']
        return None

    def get_news_by_team_id(self,team_name):
        team_id = self.find_team_id(team_name)
        url = f"{self.base_url}football-get-team-news"
        querystring = {"teamid": team_id, "page": "1"}
        response = requests.get(url, headers=self.headers, params=querystring).json()
        try:
            data = response['response']['news']
            return data
        except Exception:
            return None

