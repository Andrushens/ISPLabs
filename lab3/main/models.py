from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import default, slugify
from datetime import datetime


class Genre(models.Model):
    name = models.CharField(max_length=30, default='none')
    

class Review(models.Model):

    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    fans = models.ManyToManyField(User, related_name='fans')
    text = models.TextField(max_length=1000)
    title = models.CharField(max_length=25)
    create_date = models.DateTimeField(default=datetime.now)    
    slug = models.SlugField(max_length=25, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Review, self).save(*args, **kwargs)