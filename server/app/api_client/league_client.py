from django.conf import settings
import requests
import json


class LeagueAPIClient():
    def __init__(self):
        self.league_api_url = "https://na.api.pvp.net/api/lol/na/v2.2/"
        self.static_champ_url = "https://global.api.pvp.net/api/lol/static-data/v3"
        self.summoner_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}"

    def _call_endpoint(self, url, params=None):
        response = requests.get(url, params=params)

        if response.status_code == 429:
            raise RateLimitedException("Your API key has hit the rate limit")
        elif response.status_code == 403:
            raise UnauthorizedException("Your API key may have been blacklisted")

        return response.json()

    def get_match_list(self, account_id, begin_index=0, begin_timestamp=None):
        url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(account_id)
        params = {'api_key': settings.LEAGUE_API_KEY, "beginIndex": begin_index, "beginTime": begin_timestamp}
        return self._call_endpoint(url, params)

    def get_match(self, match_id):
        url = "https://na1.api.riotgames.com/lol/match/v4/matches/{}".format(match_id)
        params = {'api_key': settings.LEAGUE_API_KEY}
        return self._call_endpoint(url, params)

    def get_all_champion_data(self):
        version = self._call_endpoint("https://ddragon.leagueoflegends.com/api/versions.json")[0]
        url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
        return self._call_endpoint(url).get("data")

    def get_single_champion_data(self, champ_id):
        all_champs = self.get_all_champion_data()
        for champ in all_champs.values():
            if champ.get("key") == str(champ_id):
                return champ

    def get_summoner_info(self, summoner_name):
        url = self.summoner_url.format(summoner_name)
        params = {'api_key': settings.LEAGUE_API_KEY}
        return self._call_endpoint(url, params)


api_client = LeagueAPIClient()


class RateLimitedException(Exception):
    pass


class UnauthorizedException(Exception):
    pass
