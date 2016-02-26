from rest_framework import viewsets
from match.models import Match
from match.serializers import MatchSerializer

class MatchViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing match objects """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer