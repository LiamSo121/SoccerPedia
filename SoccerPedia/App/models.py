from django.db import models

class UploadedImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')  # Uploads to media/images/

    def __str__(self):
        return self.title

