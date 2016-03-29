from rest_framework import serializers
from summoner.models import Summoner

class SummonerSerializer(serializers.ModelSerializer):
    """ Simple serializer for the Summoner resource """
    class Meta:
        model = Summoner
        fields = ('id', 'name', 'level', 'rank')