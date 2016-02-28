from django.conf import settings
import requests
import json


class LeagueAPIClient():
    def __init__(self):
        self.league_api_url = "https://na.api.pvp.net/api/lol/na/v2.2/"
        self.static_champ_url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/"

    def _call_endpoint(self, url, params=None):
        response = requests.get(
            url,
            params=params
        )

        if response.status_code == 429:
            raise RateLimitedException("Your API key has hit the rate limit")
        elif response.status_code == 403:
            raise UnauthorizedException("Your API key may have been blacklisted")

        return json.loads(response.content)

    def get_match_list(self, summoner_id):
        url = self.league_api_url + "matchlist/by-summoner/{}".format(summoner_id)
        params = {'api_key': settings.LEAGUE_API_KEY}
        return self._call_endpoint(url, params)

    def get_match(self, match_id, summoner_id):
        url = self.league_api_url + "match/{}".format(match_id)
        params = {'api_key': settings.LEAGUE_API_KEY}
        return self._call_endpoint(url, params)

    def get_champion(self, champ_id):
        url = self.static_champ_url + "champion/{}".format(champ_id)
        params = {'api_key': settings.LEAGUE_API_KEY}
        return self._call_endpoint(url, params)


class RateLimitedException(Exception):
    pass


class UnauthorizedException(Exception):
    pass
