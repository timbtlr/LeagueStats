from rest_framework import serializers
from match.models import Match

class MatchSerializer(serializers.ModelSerializer):
    """ Simple serializer for the Match resource """
    class Meta:
        model = Match
        fields = ('id', 'timestamp', 'summoner', 'win', 'level', 'kills', 'deaths', 'gold_earned', 'double_kills', 'triple_kills', 'quadra_kills', 'penta_kills', 'damage_dealt', )
