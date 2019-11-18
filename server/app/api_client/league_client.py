from django.conf import settings
import requests
import json


class LeagueAPIClient():
    """
    API client to contact the League of Legends API.  Full documentation can be found at
        https://developer.riotgames.com/apis

    This Client will only query for information about North American summoners and their
    matches.
    """
    def __init__(self, api_token):
        self.token = api_token

    def _call_endpoint(self, url, params=None):
        response = requests.get(url, params=params)

        if response.status_code == 429:
            raise RateLimitedException("Your API key has hit the rate limit")
        elif response.status_code == 403:
            raise UnauthorizedException("Your API key may have been blacklisted")

        return response.json()

    def get_match_list(self, account_id, begin_index=0, begin_epoch=None):
        """
        Retrieve a list of matches for a given account.
            https://developer.riotgames.com/apis#match-v4/GET_getMatchlist

        account_id: The account to query matches for.
        begin_index: Starting index for matches.  Used for pagination.
        begin_epoch: Earliest desired match date for the query.  Used to limit the scope of a query.
        """
        url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(account_id)
        params = {'api_key': self.token, "beginIndex": begin_index, "beginTime": begin_epoch}
        return self._call_endpoint(url, params)

    def get_match(self, match_id):
        """
        Retrieve detailed information about a single match.  
            https://developer.riotgames.com/apis#match-v4/GET_getMatch

        match_id: Unique match ID to retrieve information about.
        """
        url = "https://na1.api.riotgames.com/lol/match/v4/matches/{}".format(match_id)
        params = {'api_key': self.token}
        return self._call_endpoint(url, params)

    def get_all_champion_data(self):
        """
        Retrieve champion information from the latest version of Data Dragon (ddragon).  ddragon is a separate
        API from the rest of the League of Legends APIs.  
            https://riot-api-libraries.readthedocs.io/en/latest/ddragon.html

        Determines the latest version of ddragon and queries that API for all champion data.
        A full JSON of champion data is the only way to retrieve data from this endpoint.
        """

        version = self._call_endpoint("https://ddragon.leagueoflegends.com/api/versions.json")[0]
        url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
        return self._call_endpoint(url).get("data")

    def get_single_champion_data(self, champ_id):
        """
        Utilize the ddragon endpoint to retrieve information about a specific champion.

        champ_id: Unique champion ID to retrieve information about.
        """
        all_champs = self.get_all_champion_data()
        for champ in all_champs.values():
            if champ.get("key") == str(champ_id):
                return champ

    def get_summoner_info(self, summoner_name):
        """
        Retrieve information about a specific summoner by name.
            https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName

        summoner_name: Unique string summoner name to retrieve information about.
        """
        url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(summoner_name)
        params = {'api_key': self.token}
        return self._call_endpoint(url, params)


api_client = LeagueAPIClient(api_token=settings.LEAGUE_API_KEY)


class RateLimitedException(Exception):
    pass


class UnauthorizedException(Exception):
    pass
