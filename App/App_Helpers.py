import requests
import re
from SoccerPedia.S3 import S3
from django.http import JsonResponse
from League.models import League
from pathlib import Path
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.files.storage import default_storage
from django.conf import settings

s3 = S3()



class App_Helper():
    def __init__(self):
        pass

    def get_league_url_by_country_name(self,country):
        url = f"https://www.thesportsdb.com/api/v1/json/3/search_all_leagues.php?c={country}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            data = dict(data)
            for league in data["countries"]:
                if country.lower() in league["strCountry"].lower():
                    url = league["strBadge"]
                    return url
            return "No logo found"
        else:
            return "Error fetching league logo"

    def download_image(self,image_url, filename):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image downloaded successfully: {filename}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")



    def delete_image(self,filename):
        """Deletes a file using pathlib."""
        file = Path(filename)
        if file.exists():
            file.unlink()
            print(f"Deleted: {filename}")
        else:
            print("File not found!")


    def parse_league_response(self,response_text,url,filename):
        """Extracts league details from structured response text and returns a dictionary."""
        def extract(pattern, text):
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1).strip() if match else None

        league_data = {
            "name": extract(r"\*\*Name\*\*: (.+)", response_text),
            "country": extract(r"\*\*Country\*\*: (.+)", response_text),
            "year_of_foundation": extract(r"\*\*Year of Foundation\*\*: (\d+)", response_text),
            "number_of_teams": extract(r"\*\*Number of Teams\*\*: (\d+)", response_text),
            "description": extract(r"\*\*Brief history\*\*: (.+)", response_text),
            "current_champion": extract(r"\*\*Current Champion\*\*: (.+)", response_text),
            "website": extract(r"\*\*Official Website\*\*: \[.+\]\((.+)\)", response_text),
            "logo": self.download_image(url,filename)
        }

        # Convert numeric fields
        league_data["year_of_foundation"] = int(league_data["year_of_foundation"]) if league_data[
            "year_of_foundation"] else None
        league_data["number_of_teams"] = int(league_data["number_of_teams"]) if league_data["number_of_teams"] else None
        return league_data

    def create_league_from_league_data(self,league_data):
        try:
            league = League.objects.create(
                name=league_data['name'] if league_data['name'] else "Unkown",
                country=league_data['country'] if league_data['country'] else "Unknown",
                year_of_foundation=league_data["year_of_foundation"] if league_data["year_of_foundation"] else None,
                number_of_teams=league_data["number_of_teams"] if league_data["number_of_teams"] else None,
                description=league_data["description"] if league_data["description"] else None,  # Store the full summary as description
                current_champion=league_data["current_champion"] if league_data["current_champion"] else None,
                website=league_data["website"] if league_data["website"] else None,
                logo=league_data["logo"] if league_data["logo"] else None,  # Handle logo separately if needed
            )

            return True
        except Exception as e:
            print(e)
            return False

    def edit_team_text_from_prompt(self,text):
        team_pattern = r"Team: (.*)"
        country_pattern = r"Country: (.*)"
        league_pattern = r"League: (.*)"
        stadium_pattern = r"Stadium: (.*)"
        achievements_pattern = r"Achievements?:(.*?)(?=Fun Fact|$)"
        fun_fact_pattern = r"Fun Fact: (.*)"

        # Use regular expressions to extract the relevant information
        team = re.search(team_pattern, text)
        country = re.search(country_pattern, text)
        league = re.search(league_pattern, text)
        stadium = re.search(stadium_pattern, text)
        achievements = re.search(achievements_pattern, text, re.DOTALL)
        fun_fact = re.search(fun_fact_pattern, text)

        # Build the formatted summary
        summary = ""
        if team:
            summary += f"<b>Team</b>: {team.group(1)}\n"
        if country:
            summary += f"<b>Country</b>: {country.group(1)}\n"
        if league:
            summary += f"<b>League</b>: {league.group(1)}\n"
        if stadium:
            summary += f"<b>Stadium</b>: {stadium.group(1)}\n"

        if achievements:
            summary += f"\n<b>Major Achievements</b>:\n{achievements.group(1).strip()}\n"

        if fun_fact:
            summary += f"\n<b>Fun Fact</b>:\n{fun_fact.group(1).strip()}\n"

        return summary

    def edit_league_summary(self, text):
        # Define patterns for extracting each section from the response
        league_overview_pattern = r"League Overview:(.*?)(?=History & Legacy|$)"
        history_legacy_pattern = r"History & Legacy:(.*?)(?=Major Achievements|$)"
        major_achievements_pattern = r"Major Achievements:(.*?)(?=Notable Players|$)"
        notable_players_pattern = r"Notable Players:(.*?)(?=Unique Features|$)"
        unique_features_pattern = r"Unique Features:(.*)"

        # Use regular expressions to extract the relevant information
        league_overview = re.search(league_overview_pattern, text, re.DOTALL)
        history_legacy = re.search(history_legacy_pattern, text, re.DOTALL)
        major_achievements = re.search(major_achievements_pattern, text, re.DOTALL)
        notable_players = re.search(notable_players_pattern, text, re.DOTALL)
        unique_features = re.search(unique_features_pattern, text, re.DOTALL)

        # Build the formatted summary with bold titles using Markdown
        summary = ""

        if league_overview:
            summary += f"<b>League Overview</b>:{league_overview.group(1).strip()}\n"
        if history_legacy:
            summary += f"<b>History & Legacy</b>:{history_legacy.group(1).strip()}\n"
        if major_achievements:
            summary += f"<b>Major Achievements</b>:{major_achievements.group(1).strip()}\n"
        if notable_players:
            summary += f"<b>Notable Players</b>:{notable_players.group(1).strip()}\n"
        if unique_features:
            summary += f"<b>Unique Features</b>:{unique_features.group(1).strip()}\n"
        print(summary)
        return summary



