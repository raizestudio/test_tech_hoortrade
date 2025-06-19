from os import wait
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    is_active = models.BooleanField(default=True)
    
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    author = models.ForeignKey("users.Author", on_delete=models.CASCADE, related_name='movies')


    def __str__(self):
        return self.title



