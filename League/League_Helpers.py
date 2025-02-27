import asyncio

import requests
import pycountry


class League_Helper:
    def __init__(self):
        self.base_url = "https://free-api-live-football-data.p.rapidapi.com/"
        self.headers = {
            "x-rapidapi-key": "845c790af6mshf64b3e0b51ac50ep1b8771jsnc6626df1faa1",
            "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
        }
    def fix_url(self,object_key):
        object_key = unquote(object_key)
        base_s3_url = "https://soccerpedia.s3.amazonaws.com/media/"
        fixed_url = object_key.replace(base_s3_url, "", 1)
        fixed_url = unquote(fixed_url)
        return fixed_url

    def _get_country_flag_url_sync(self,country_name):
        """ Synchronous function to retrieve country flag URL """
        country = pycountry.countries.get(name=country_name)
        if country:
            return f"https://flagcdn.com/w320/{country.alpha_2.lower()}.png"
        return "Country not found"

    def get_country_flag_url(self,country_name):
        country = pycountry.countries.get(name=country_name)
        if country:
            return f"https://flagcdn.com/w320/{country.alpha_2.lower()}.png"
        return "Country not found"
        # return await asyncio.to_thread(self._get_country_flag_url_sync,country_name)


    async def get_flags(self,countries):
        # countries_dict = {}
        # for country in countries:
        #     countries_dict[country] = await League_Helper.get_country_flag_url(League_Helper,country)
        # return countries_dict
        tasks = {country: self.get_country_flag_url(country) for country in countries}
        results = await asyncio.gather(*tasks.values())
        return dict(zip(tasks.keys(), results))

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



