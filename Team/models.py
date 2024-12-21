from django.db import models
from League.models import League
# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=255)
    year_of_foundation = models.IntegerField()
    city = models.CharField(max_length=255)
    stadium_name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='images/team_logos/', blank=True, null=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')
    number_of_trophies = models.IntegerField(default=0)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class YoutubeVideo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='youtube_videos')
    title = models.CharField(max_length=255, help_text="Title of the YouTube video")
    url = models.URLField(help_text="YouTube video URL")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the video was added")

    def __str__(self):
        return f"{self.title} - {self.team.name}"