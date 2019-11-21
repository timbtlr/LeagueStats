from django.db import models
from champion.models import Champion
from summoner.models import Summoner
from match.constants import MATCH_MODE_TYPE, MATCH_QUEUE_TYPE

class MatchPerformance(models.Model):
    """
    Match model.  Contains minimal information about the performance of a specific summoner
    within an individual match of League of Legends.  

    Since this model represents summoner performance in a match and not the totality of the match itself,
    single match IDs are not unique by themselves.  The match_id + foreign key to a summoner object are 
    unique together.
    """
    match_id = models.CharField(max_length=255, default=0)
    summoner = models.ForeignKey(Summoner)
    mode = models.CharField(max_length=100, null=True, blank=True)
    game_type = models.CharField(max_length=255, null=True, blank=True)
    lane = models.CharField(max_length=100, null=True, blank=True)
    champ = models.IntegerField(default=0)
    opposing_champ = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    win = models.BooleanField(default=False)
    level = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    gold_earned = models.IntegerField()
    double_kills = models.IntegerField()
    triple_kills = models.IntegerField()
    quadra_kills = models.IntegerField()
    penta_kills = models.IntegerField()
    damage_dealt = models.IntegerField()

    @property
    def queue_str(self):
        return MATCH_QUEUE_TYPE.get(self.game_type, "Unknown Queue Type")

    @property
    def mode_str(self):
        return MATCH_MODE_TYPE.get(self.mode, "Unknown Mode Type")

    @property
    def champ_name(self):
        champ = Champion.objects.get(pk=self.champ)
        return f"{champ.name}"
    
    def __str__(self):
        return f"{self.summoner.name} ({self.mode} / {self.game_type} / {self.timestamp})"

    class Meta:
        unique_together = ['match_id', 'summoner']