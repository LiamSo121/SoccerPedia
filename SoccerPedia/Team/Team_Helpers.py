import requests
import boto3
from urllib.parse import unquote
import asyncio
import aiohttp


class Team_Helper():
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

    async def find_team_id(self,team_name):
        url = f"{self.base_url}football-teams-search"
        querystring = {"search": team_name}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url,headers=self.headers,params=querystring) as response:
                response.raise_for_status()
                data = await response.json()
        for team_dict in data['response']['suggestions']:
            if team_dict['name'] == team_name:
                return team_dict['id']
        return None

    async def get_news_by_team_id(self, team_name):
        team_id = await self.find_team_id(team_name)
        url = f"{self.base_url}football-get-team-news"
        querystring = {"teamid": team_id, "page": "1"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=querystring) as response:
                try:
                    response.raise_for_status()
                    data = await response.json()
                    return data['response'].get('news', None)
                except Exception as e:
                    print(f"Error fetching team news: {e}")
                    return None

