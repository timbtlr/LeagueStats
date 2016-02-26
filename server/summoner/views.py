from rest_framework import viewsets
from summoner.models import Summoner
from summoner.serializers import SummonerSerializer

class SummonerViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing summoner objects """
    queryset = Summoner.objects.all()
    serializer_class = SummonerSerializer