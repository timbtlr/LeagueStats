from rest_framework import serializers
from match.models import MatchPerformance


class MatchSerializer(serializers.ModelSerializer):
    """ 
    Simple serializer for the Match model 
    """
    class Meta:
        model = MatchPerformance
        fields = (
            'id', 'timestamp', 'summoner', 'champ', 'win', 'level',
            'kills', 'deaths', 'assists', 'gold_earned', 'double_kills',
            'triple_kills', 'quadra_kills', 'penta_kills', 'damage_dealt',
            "mode", "lane", "queue_str", "mode_str", "champ_name"
        )
