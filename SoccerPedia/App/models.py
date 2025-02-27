from django.db import models
from django.contrib.auth.models import User

class UploadedImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')  # Uploads to media/images/

    def __str__(self):
        return self.title

# class Profile(models.Model):
#     additional_info = models.TextField(blank=True,null=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)

    #
    # def __str__(self):
    #     return str(self.id)
