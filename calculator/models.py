from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    handicap = models.FloatField(blank=True, null=True)
    following = models.ManyToManyField('self', blank=True, related_name="followers", symmetrical=False)
    def __str__(self):
        return self.username
        
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "handicap": self.handicap
        }

class Score(models.Model):
    golfer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_by')
    holes = models.IntegerField(choices = [(9,9),(18,18)])
    course = models.CharField(max_length=64)
    date = models.DateField()
    score = models.IntegerField()
    rating = models.FloatField()
    slope = models.IntegerField()
    differential = models.FloatField()
   