import asyncio
import openai
from django.http import HttpResponse
from django.views import View
import requests
from .App_Helpers import App_Helper
from urllib.parse import urlparse
import os
from django.shortcuts import render, redirect
import requests
import io
import json
from PIL import Image
from SoccerPedia.S3 import S3
from django.conf import settings

app_helper = App_Helper()
s3 = S3()

class AI(View):
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.AI_API_KEY)
        self.current_team_summary = None
        self.current_league_summary = None
        self.image_base_url = "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image"
        self.image_headers = {"Authorization": "Bearer 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"}

    def generate_image(self,prompt):
        prompt += "the image is about sport, and needs to be sport related,the image should be clear, stylish and very nice to see, the colors has to be sharp"
        payload = {"inputs": prompt}
        response = requests.post(self.image_base_url, headers=self.image_headers, json=payload)
        # Check response status
        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return None
        url = self.save_image(response.content)
        return url

    def save_image(self,content):
        if content:
            filename = "ai_generation.png"
            try:
                # Open the image
                image = Image.open(io.BytesIO(content))
                # Save the image locally
                image.save(filename)
                url = s3.upload_photo(filename,"ai")
                os.remove(filename)
                return url
            except Exception as e:
                print("Error opening image:", e)



    def _generate_summary(self,prompt,flag):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a football expert. you know all the football leagues statistics globally"},
                      {"role": "user", "content": prompt}],
            max_tokens=500
        )
        print(response.choices[0].message.content)
        if flag == 'team':
            response = app_helper.edit_team_text_from_prompt(response.choices[0].message.content)
        elif flag == 'league':
            response = app_helper.edit_league_summary(response.choices[0].message.content)
        return response



    def _generate_summary_with_context(self,question,context):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a football expert. you know all the football leagues statistics globally"},
                {"role": "user", "content": context},
                {"role": "user", "content": question}
            ],
            max_tokens=500
        )
        return response

    async def generate_random_team_summary(self):
        prompt = (
            "Pick a random football team from any league in the world and provide an interesting summary. "
            "Include the country, league, stadium, major achievements, and a fun fact."
        )
        self.current_team_summary = await asyncio.to_thread(self._generate_summary,prompt,'team')
        return  self.current_team_summary

    async def ask_team_follow_up_question(self,question):
        if not self.current_team_summary:
            return "Please ask me to choose a football team first."
        # Add context about the current team to the conversation
        context = f"The current team is: {self.current_team_summary}"
        response = await asyncio.to_thread(self._generate_summary_with_context,question,context)
        return response.choices[0].message.content


    async def generate_random_league_summary(self):
        prompt = (
            "Generate a detailed summary of a randomly chosen football league which is not from england or spain or germany, i prefer a small country."
            "The response should be structured with clear headings and formatting. Include the following sections:\n\n"
            "League Overview- Name, country, and number of teams.\n"
            "History & Legacy - Brief history and key milestones.\n"
            "Major Achievements - Titles, international success, and notable contributions.\n"
            "Notable Players - Famous players who have played in this league.\n"
            "Unique Features - Special rules, promotion/relegation system, or anything distinctive.\n"
        )
        response = await asyncio.to_thread(self._generate_summary,prompt,'league')
        # self.current_league_summary = response.choices[0].message.content
        print(response)
        self.current_league_summary = response
        return  self.current_league_summary

    async def ask_league_follow_up_question(self,question):
        if not self.current_league_summary:
            return "Please ask me to choose a football league first."

        context = f"The current league is: {self.current_league_summary}"
        response = await asyncio.to_thread(self._generate_summary_with_context,question,context)
        return response.choices[0].message.content

    def create_league_by_prompt(self):
        if not self.current_league_summary:
            return HttpResponse("Please ask me to choose a football league first.")
        question = "give me only the country of the current league, i need only the name of the country, nothing else"
        # Add context about the current team to the conversation
        context = f"The current league is: {self.current_league_summary}"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a football expert. You are a football expert. you know all the football leagues statistics globally"},
                {"role": "user", "content": context},
                {"role": "user", "content": question}
            ],
            max_tokens=300
        )
        answer = response.choices[0].message.content
        url = app_helper.get_league_url_by_country_name(answer)
        filename = f"{answer}.png"
        app_helper.download_image(url,filename)
        answer = self.gather_information_for_league_creation()
        league_details = app_helper.parse_league_response(answer,url,filename)
        app_helper.delete_image(filename)
        flag = app_helper.create_league_from_league_data(league_details)
        if flag:
            return redirect('present_leagues')
        else:
            return HttpResponse("Failed to create League From AI")

    def gather_information_for_league_creation(self):
        prompt = ("Generate a detailed summary of the already chosen football league."
                    "The response must be **structured** with clear headings and formatted as follows:\n\n"
                    "### League Overview:\n"
                    "- **Name**: (Full official name of the league)\n"
                    "- **Country**: (Which country the league belongs to)\n"
                    "- **Year of Foundation**: (When the league was established)\n"
                    "- **Number of Teams**: (How many teams participate)\n\n"
                    "### History & Legacy:\n"
                    "- **Brief history**: (Key milestones, origin story, and significant moments)\n\n"
                    "### Additional Information:\n"
                    "- **Current Champion**: (The team that won the most recent league title or the last champion you know, give me the name of the team)\n"
                    "- **Official Website**: (URL of the official league website or any website related, just give me a URL to fill in)\n"
                    "The response **must be structured with proper headings** so that each piece of information is easy to extract.")        # Add context about the current team to the conversation
        context = f"The current league is: {self.current_league_summary}"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a football expert. You are a football expert. you know all the football leagues statistics globally"},
                {"role": "user", "content": context},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        answer = response.choices[0].message.content
        return answer
