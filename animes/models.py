from django.db import models
from django.conf import settings

# Create your models here.
class Anime(models.Model):
    name = models.CharField(max_length=255)
    episode_count = models.IntegerField()
    season_count = models.IntegerField()
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    studio = models.CharField(max_length=255)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    character = models.ForeignKey('animes.Anime', related_name='votes', on_delete=models.CASCADE)