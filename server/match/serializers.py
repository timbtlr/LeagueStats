from rest_framework import serializers
from match.models import Match


class MatchSerializer(serializers.ModelSerializer):
    """ Simple serializer for the Match resource """
    class Meta:
        model = Match
        fields = (
            'id', 'timestamp', 'summoner', 'champ', 'win', 'level',
            'kills', 'deaths', 'assists', 'gold_earned', 'double_kills',
            'triple_kills', 'quadra_kills', 'penta_kills', 'damage_dealt',
        )
