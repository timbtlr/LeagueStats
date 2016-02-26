from django.db import models
from django.utils import timezone
from summoner.models import Summoner

class Match(models.Model):
    """
    League of Legends Match Model.
    Contains a foreign key to a summoner.
    """
    id = models.CharField(primary_key=True, max_length=255)
    summoner = models.ForeignKey(Summoner)
    timestamp = models.DateTimeField()
    win = models.BooleanField(default=False)
    level = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    gold_earned = models.IntegerField()
    double_kills = models.IntegerField()
    triple_kills = models.IntegerField()
    quadra_kills = models.IntegerField()
    penta_kills = models.IntegerField()
    damage_dealt = models.IntegerField()
