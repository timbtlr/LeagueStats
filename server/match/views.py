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
        summoner_name = params.get("summoner")
        summoner = Summoner.objects.get(name=summoner_name)
        matches = Match.objects.filter(summoner=summoner)

        timestamps = []
        kdas = []
        win = []

        for match in matches.iterator():
            timestamps.append(match.timestamp.weekday())
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

    @list_route(methods=['get'], url_path='champion-stats')
    def champion_stats(self, request, pk=None):
        params = request.query_params
        summoner_name = params.get("summoner")

        if not summoner_name:
            return Response(
                data={
                    "status": 400,
                    "detail": "You must provide a summoner name with this query"
                },
                status=400
            )

        summoner = Summoner.objects.get(name=summoner_name)
        matches = Match.objects.filter(summoner=summoner)

        champ = []
        kills = []
        deaths = []
        assists = []
        kdas = []
        gold = []
        damage = []

        for match in matches.iterator():
            champ.append(Champion.objects.get(id=match.champ).name)
            kills.append(match.kills)
            deaths.append(match.deaths)
            assists.append(match.assists)
            if match.deaths > 0:
                kdas.append(float(match.kills + match.assists) / match.deaths)
            else:
                kdas.append(float(match.kills + match.assists))
            gold.append(match.gold_earned)
            damage.append(match.damage_dealt)

        frame = pd.DataFrame({
            "Champion": champ,
            "KDA": kdas,
            "Kills": kills,
            "Deaths": deaths,
            "Assists": assists,
            "Gold": gold,
            "Damage": damage
        })

        kda_groupings = frame.groupby(['Champion']).aggregate(np.mean)
        kda_groupings = kda_groupings.sort_values(by=['KDA'], ascending=[False])
        json_result = kda_groupings.to_json()
        json_result = json.loads(json_result)

        print(kda_groupings)
        print(json_result)

        keys = json_result['Gold'].keys()

        list_result = {}
        for key in keys:
            list_result[key]['Gold'] = json_result['Gold'].get(key)

        print(list_result)

        return Response(
            data=json.loads(list_result),
            status=200
        )
