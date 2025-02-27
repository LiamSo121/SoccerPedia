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
    title = models.CharField(max_length=255)
    url = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the video was added")

    def __str__(self):
        return f"{self.title} - {self.team.name}"


class Review(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='team_reviews')
    stars = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],  # Limit to 1-5 stars
        default=5,  # Default rating
    )
    content = models.TextField()
    image = models.ImageField(upload_to='review_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.created_at)
