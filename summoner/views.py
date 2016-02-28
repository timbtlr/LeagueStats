from rest_framework import viewsets
from summoner.models import Summoner
from summoner.serializers import SummonerSerializer
from rest_framework import filters
from api_client.league_client import api_client
from rest_framework.response import Response


class SummonerViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing summoner objects """
    queryset = Summoner.objects.all()
    serializer_class = SummonerSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('name', )

    def create(self, request):
        summoner_name = request.data.get("summoner")
        summoner_data = api_client.get_summoner_info(summoner_name)
        print(summoner_data)

        try:
            summoner = Summoner.objects.get(id=summoner_data.get("id"))
            created = False
        except Summoner.DoesNotExist:
            summoner = Summoner(
                name=summoner_name,
                id=summoner_data.get("id"),
                level=summoner_data.get("summonerLevel")
            )
            created = True

        summoner_serializer = SummonerSerializer(instance=summoner)
        if created:
            status_code = 201
        else:
            status_code = 200

        summoner.save()
        return Response(data=summoner_serializer.data, status=status_code)
