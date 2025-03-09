from django.db import models

class Stadium(models.Model):
    name = models.CharField(max_length=255)
    club = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=255)
    capacity = models.FloatField()



    def __str__(self):
        return self.name