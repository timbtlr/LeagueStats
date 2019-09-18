import pandas as pd
import numpy as np
import json
from rest_framework import viewsets
from rest_framework.response import Response
from match.models import Match
from summoner.models import Summoner
from champion.models import Champion
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
        summoner_name = params.get("summoner")
        summoner = Summoner.objects.get(name=summoner_name)
        matches = Match.objects.filter(summoner=summoner)

        timestamps = []
        kdas = []
        wins = []
        kills = []
        assists = []
        deaths = []

        for match in matches.iterator():
            timestamps.append(match.timestamp.hour + 1)
            if match.deaths > 0:
                kdas.append(float(match.kills + match.assists) / match.deaths)
            else:
                kdas.append(float(match.kills + match.assists))
            wins.append(int(match.win))
            kills.append(int(match.kills))
            assists.append(int(match.deaths))
            deaths.append(int(match.assists))

        norm_result = self.normalize_kda_data(
            timestamps, kdas, wins, kills, deaths, assists, range(1, 25)
        )

        return Response(
            data=norm_result,
            status=200
        )

    @list_route(methods=['get'], url_path='daily-kda')
    def daily_kda(self, request, pk=None):
        params = request.query_params
        summoner_name = params.get("summoner")
        summoner = Summoner.objects.get(name=summoner_name)
        matches = Match.objects.filter(summoner=summoner)

        timestamps = []
        kdas = []
        wins = []
        kills = []
        assists = []
        deaths = []

        for match in matches.iterator():
            timestamps.append(match.timestamp.weekday() + 1)
            if match.deaths > 0:
                kdas.append(float(match.kills + match.assists) / match.deaths)
            else:
                kdas.append(float(match.kills + match.assists))
            wins.append(int(match.win))
            kills.append(int(match.kills))
            assists.append(int(match.deaths))
            deaths.append(int(match.assists))

        norm_result = self.normalize_kda_data(
            timestamps, kdas, wins, kills, deaths, assists, range(1, 8)
        )

        return Response(
            data=norm_result,
            status=200
        )

    @list_route(methods=['get'], url_path='monthly-kda')
    def monthly_kda(self, request, pk=None):
        params = request.query_params
        summoner_name = params.get("summoner")
        summoner = Summoner.objects.get(name=summoner_name)
        matches = Match.objects.filter(summoner=summoner)

        timestamps = []
        kdas = []
        wins = []
        kills = []
        assists = []
        deaths = []

        for match in matches.iterator():
            timestamps.append(match.timestamp.month)
            if match.deaths > 0:
                kdas.append(float(match.kills + match.assists) / match.deaths)
            else:
                kdas.append(float(match.kills + match.assists))
            wins.append(int(match.win))
            kills.append(int(match.kills))
            assists.append(int(match.deaths))
            deaths.append(int(match.assists))

        norm_result = self.normalize_kda_data(
            timestamps, kdas, wins, kills, deaths, assists, range(1, 13)
        )

        return Response(
            data=norm_result,
            status=200
        )

    def normalize_kda_data(self, times, kdas, wins, kills, deaths, assists,
                           index_range):
        frame = pd.DataFrame({
            "Month": times,
            "KDA": kdas,
            "Win": wins,
            "Kills": kills,
            "Deaths": deaths,
            "Assists": assists
        })

        kda_groupings = frame.groupby(['Month']).aggregate(np.mean)
        kda_groupings = kda_groupings.reindex(index_range, fill_value=0)
        cols_to_norm = ['KDA', 'Win', 'Kills', 'Deaths', 'Assists']
        kda_groupings[cols_to_norm] = kda_groupings[cols_to_norm].apply(
            lambda x: (x - x.min()) / (x.max() - x.min())
        )
        json_result = kda_groupings.to_json()
        return json.loads(json_result)
