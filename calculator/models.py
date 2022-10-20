from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username

class Score(models.Model):
    golfer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_by')
    course = models.CharField(max_length=64)
    date = models.DateField()
    score = models.IntegerField()
    rating = models.FloatField()
    slope = models.IntegerField()
    differential = models.FloatField()
