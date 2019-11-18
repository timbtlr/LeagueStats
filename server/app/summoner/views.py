from collections import Counter 

from rest_framework import viewsets
from summoner.helpers import fill_data_frame, normalize_kda_data
from summoner.models import Summoner
from summoner.serializers import SummonerSerializer
from rest_framework import filters
from api_client.league_client import api_client
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from match.models import MatchPerformance
from match.serializers import MatchSerializer
from champion.models import Champion


class SummonerViewSet(viewsets.ModelViewSet):
    """ 
    ViewSet for viewing and editing summoner objects 
    """
    queryset = Summoner.objects.all()
    serializer_class = SummonerSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('name', )

    def create_by_name(self, summoner_name):
        summoner_data = api_client.get_summoner_info(summoner_name)

        try:
            summoner = Summoner.objects.get(id=summoner_data.get("id"))
            return summoner, False
        except Summoner.DoesNotExist:
            summoner = Summoner(
                name=summoner_name,
                id=summoner_data.get("accountId"),
                account_id=summoner_data.get("accountId"),
                puuid=summoner_data.get("puuid"),
                level=summoner_data.get("summonerLevel")
            )
            return summoner, True

    def create(self, request):
        summoner_name = request.data.get("summoner")
        summoner, created = self.create_by_name(summoner_name)

        summoner_serializer = SummonerSerializer(instance=summoner)
        if created:
            status_code = 201
        else:
            status_code = 200

        summoner.save()
        return Response(data=summoner_serializer.data, status=status_code)

    @detail_route(methods=['get'])
    def stats(self, request, pk=None):
        summoner = Summoner.objects.get(name__iexact=pk)
        matches = MatchPerformance.objects.filter(summoner=summoner)

        wins = 0
        kills = 0
        assists = 0
        deaths = 0
        total_gold = 0
        doubles = 0
        triples = 0
        quads = 0
        pentas = 0
        total_dmg = 0

        for match in matches.iterator():
            if match.win:
                wins += 1
            kills += match.kills
            deaths += match.deaths
            assists += match.assists
            total_gold += match.gold_earned
            doubles += match.double_kills
            triples += match.triple_kills
            quads += match.quadra_kills
            pentas += match.penta_kills
            total_dmg += match.damage_dealt

        losses = len(matches) - wins
        avg_gold = float(total_gold / len(matches))
        avg_dmg = float(total_dmg / len(matches))

        return Response(
            data={
                "id": summoner.id,
                "kills": kills,
                "deaths": deaths,
                "assists": assists,
                "total_gold": total_gold,
                "doubles": doubles,
                "triples": triples,
                "quads": quads,
                "pentas": pentas,
                "total_dmg": total_dmg,
                "wins": wins,
                "losses": losses,
                "avg_gold": avg_gold,
                "avg_dmg": avg_dmg
            },
            status=200
        )

    @detail_route(methods=['post'])
    def bans(self, request, pk=None):
        try:
            summoner = Summoner.objects.get(name__iexact=pk)
        except Summoner.DoesNotExist:
            summoner, created = self.create_by_name(summoner_name)
            return Response("No games on record for this summoner.  Check back in 30 minutes after games populate.", status=404)

        try:
            champ = Champion.objects.get(name__iexact=request.data.get("champ"))
        except Champion.DoesNotExist:
            return Response("No games played as this champion", status=404)

        matches = MatchPerformance.objects.filter(summoner__pk=summoner.pk, champ=champ.pk, mode="CLASSIC")
        role = request.data.get("role")
        if role:
            matches = matches.filter(lane__icontains=f"{role.upper()}")

        if not matches:
            return Response("No games played as this champion", status=404)

        opposing_champs = matches.values_list("opposing_champ", flat=True)

        bans = {}
        nevers = {}
        for opponent in opposing_champs:
            try:
                pct = float(matches.filter(win=True, opposing_champ=opponent).count()) / float(matches.filter(opposing_champ=opponent).count()) * 100.0
                if pct == 0:
                    nevers[opponent] = pct
                elif pct == 100:
                    continue
                else:
                    bans[opponent] = pct
            except:
                pass # Perfect win record against this champ.  Don't ban.

        result = {"never": {}, "low": {}}

        max = 5
        index = 0
        for key, value in nevers.items():
            index += 1
            try:
                champ = Champion.objects.get(pk=key)
                result["never"][f"{champ.name}, {champ.title}"] = f"{value}"
            except Champion.DoesNotExist:
                pass
            if index >= max:
                break

        c = Counter(bans) 
        bad_champs = c.most_common()[:-6-1:-1]
        for bad in bad_champs:
            try:
                champ = Champion.objects.get(pk=bad[0])
                result["low"][f"{champ.name}, {champ.title}"] = f"{bad[1]}"
            except Champion.DoesNotExist:
                pass

        return Response(
            data=result,
            status=200
        )

    @detail_route(methods=['post'])
    def recent(self, request, pk=None):
        try:
            summoner = Summoner.objects.get(name__iexact=pk)
        except Summoner.DoesNotExist:
            summoner, created = self.create_by_name(summoner_name)
            return Response("No games on record for this summoner.  Check back in 30 minutes after games populate.", status=404)

        count = int(request.data.get("count") or 3)
        matches = MatchPerformance.objects.filter(summoner__pk=summoner.pk).order_by("-timestamp")

        response = [MatchSerializer(m).data for m in matches[:count]]
        return Response(
            data=response,
            status=200
        )

    


    @detail_route(methods=['get'], url_path='hourly-kda')
    def hourly_kda(self, request, pk):
        """
        Return average KDA for a summoner broken down hourly.  Results
        are mormalized between 0 and 1.
        """
        summoner = Summoner.objects.get(name__iexact=pk)
        matches = MatchPerformance.objects.filter(summoner=summoner)

        data_frame = fill_data_frame(matches, "%H")
        norm_result = normalize_kda_data(data_frame, range(1, 25))

        return Response(
            data=norm_result,
            status=200
        )

    @detail_route(methods=['get'], url_path='daily-kda')
    def daily_kda(self, request, pk):
        """
        Return average KDA for a summoner broken down by day of the week.  Results
        are mormalized between 0 and 1.
        """
        summoner = Summoner.objects.get(name__iexact=pk)
        matches = MatchPerformance.objects.filter(summoner=summoner)

        data_frame = fill_data_frame(matches, "%w")
        norm_result = normalize_kda_data(data_frame, range(1, 8))

        return Response(
            data=norm_result,
            status=200
        )

    @detail_route(methods=['get'], url_path='monthly-kda')
    def monthly_kda(self, request, pk):
        """
        Return average KDA for a summoner broken down by month of the year.  Results
        are mormalized between 0 and 1.

        value
        """
        summoner = Summoner.objects.get(name__iexact=pk)
        matches = MatchPerformance.objects.filter(summoner=summoner)

        data_frame = fill_data_frame(matches, "%-m")
        norm_result = normalize_kda_data(data_frame, range(1, 13))

        return Response(
            data=norm_result,
            status=200
        )
