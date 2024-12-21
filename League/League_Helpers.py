import requests



class League_Helper:
    def __init__(self):
        self.base_url = "https://free-api-live-football-data.p.rapidapi.com/"
        self.headers = {
            "x-rapidapi-key": "845c790af6mshf64b3e0b51ac50ep1b8771jsnc6626df1faa1",
            "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
        }

    def find_country_code(self,country_name):
        url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-countries"

        headers = {
            "x-rapidapi-key": "845c790af6mshf64b3e0b51ac50ep1b8771jsnc6626df1faa1",
            "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers).json()
        for country_dict in response['response']['countries']:
            if country_name == country_dict['name']:
                return country_dict['ccode']


    def find_league_id(self, country):
        url = f"{self.base_url}football-leagues-search"
        querystring = {"search": country}
        country_code = self.find_country_code(country)
        response = requests.get(url, headers=self.headers, params=querystring).json()
        for league_dict in response['response']['suggestions']:
            if league_dict['ccode'] == country_code:
                return league_dict['id']

    def get_league_news(self, country):
        league_id = str(self.find_league_id(country))
        url = "https://free-api-live-football-data.p.rapidapi.com/football-get-league-news"
        querystring = {"leagueid": league_id, "page": "1"}
        response = requests.get(url, headers=self.headers, params=querystring).json()
        try:
            return response['response']['news']
        except Exception:
            return None


