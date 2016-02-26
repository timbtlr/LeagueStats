from django.conf import settings
import requests
import json


class LeagueAPIClient():
    def __init__(self):
        self.LEAGUE_API_URL = "https://na.api.pvp.net/api/lol/na/v2.2/"

    def get_match_list(self, summoner_id):
        url = self.LEAGUE_API_URL + "matchlist/by-summoner/{}".format(summoner_id)
        params = {'api_key': settings.LEAGUE_API_KEY}

        response = requests.get(
            url,
            params=params
        )

        return json.loads(response.content)

    def get_match(self, match_id, summoner_id):
        url = self.LEAGUE_API_URL + "match/{}".format(match_id)
        params = {'api_key': settings.LEAGUE_API_KEY}

        response = requests.get(
            url,
            params=params
        )

        return json.loads(response.content)