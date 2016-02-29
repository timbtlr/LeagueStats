import pandas as pd
import numpy as np
import json
from rest_framework import viewsets
from rest_framework.response import Response
from match.models import Match
from summoner.models import Summoner
from match.serializers import MatchSerializer
from rest_framework.decorators import list_route
from rest_framework import filters


class MatchViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing match objects """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('summoner', )

    @list_route(methods=['get'], url_path='hourly-kda')
    def hourly_kda(self, request, pk=None):
        params = request.query_params
        summoner_name = params.get("summoner", True)
        summoner = Summoner.objects.get(name=summoner_name)
        matches = Match.objects.filter(summoner=summoner)

        timestamps = []
        kdas = []
        win = []

        for match in matches.iterator():
            timestamps.append(match.timestamp.hour)
            if match.deaths > 0:
                kdas.append(float(match.kills + match.assists) / match.deaths)
            else:
                kdas.append(float(match.kills + match.assists))
            win.append(int(match.win))


        frame = pd.DataFrame({
            "Hour": timestamps,
            "KDA": kdas,
            "Win": win
        })

        kda_groupings = frame.groupby(['Hour']).aggregate(np.mean)
        json_result = kda_groupings.to_json()

        return Response(
            data=json.loads(json_result),
            status=200
        )

    @list_route(methods=['get'], url_path='daily-kda')
    def daily_kda(self, request, pk=None):
        params = request.query_params
        summoner_name = params.get("summoner", True)
        summoner = Summoner.objects.get(name=summoner_name)
        matches = Match.objects.filter(summoner=summoner)

        timestamps = []
        kdas = []

        for match in matches.iterator():
            timestamps.append(match.timestamp.weekday())
            if match.deaths > 0:
                kdas.append(float(match.kills + match.assists) / match.deaths)
            else:
                kdas.append(float(match.kills + match.assists))

        frame = pd.DataFrame({
            "Hour": timestamps,
            "KDA": kdas
        })

        kda_groupings = frame.groupby(['Hour']).aggregate(np.mean)
        json_result = kda_groupings.to_json()

        return Response(
            data=json.loads(json_result),
            status=200
        )
