from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime


class Account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    reviews_created = models.IntegerField(default=0)

    class Meta:
        indexes= [
            models.Index(fields=['user']),
        ]
     
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)


class Review(models.Model):

    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='author')
    fans = models.ManyToManyField(User, related_name='fans')
    likes = models.IntegerField(default=0)
    text = models.TextField(max_length=1000)
    title = models.CharField(max_length=25, unique=True)
    create_date = models.DateTimeField(default=datetime.now)    
    slug = models.SlugField(max_length=25, unique=True)

    class Meta:
        ordering = ['-likes']
        indexes= [
            models.Index(fields=['slug']),
            models.Index(fields=['author_id']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title.lower())
        super(Review, self).save(*args, **kwargs)