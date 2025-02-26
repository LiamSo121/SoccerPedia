from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=255)
    year_of_foundation = models.IntegerField()
    country = models.CharField(max_length=255)
    number_of_teams = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='images/league_logos/', blank=True, null=True)
    current_champion = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


