from django.db import models
from django.utils import timezone

class Summoner(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    rank = models.CharField(max_length=20, blank=True, null=True)