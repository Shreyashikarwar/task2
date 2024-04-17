from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=100) #in mins

class Casting(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100)
    cast_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

class Dialogue(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    character_name = models.CharField(max_length=100)
    dialogue = models.TextField()
