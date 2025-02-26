from django.db import models
from users.models import CustomUser


class Message(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}..."