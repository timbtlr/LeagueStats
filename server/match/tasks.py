import json
import datetime
from time import sleep
from django.utils import timezone
from summoner.models import Summoner
from match.client import LeagueAPIClient
from match.models import Match

api_client = LeagueAPIClient()

def schedule_pull_matches():
    for summoner in Summoner.objects.all():
        pull_matches(summoner.id)

def pull_matches(summoner_id):
    matches = api_client.get_match_list(summoner_id)

    for match in matches.get("matches"):
        match_id = match.get("matchId")
        match_time = match.get("timestamp")

        try:
            Match.objects.get(id=match_id, summoner__id=summoner_id)
        except Match.DoesNotExist:
            match_data = api_client.get_match(match_id, summoner_id)

            # Get participant ID
            participant_id = None
            for player in match_data.get("participantIdentities"):
                if int(player.get("player").get("summonerId")) == int(summoner_id):
                    participant_id = player.get("participantId")
                    break

            # Find participant in the list, create a match with it
            if participant_id:
                try:
                    print(match_id)
                    for participant in match_data.get("participants"):
                        if participant.get("participantId") == participant_id:
                            create_match(match_id, summoner_id, match_time, participant.get("stats"))
                except:
                    pass

        sleep(5)

def create_match(match_id, summoner_id, match_time, participant_stats):
    match = Match(id=match_id)
    match.timestamp = datetime.datetime.fromtimestamp(int(match_time/1000-18000))
    match.summoner = Summoner.objects.get(id=summoner_id)
    match.win = participant_stats.get("winner")
    match.level = participant_stats.get("champLevel")
    match.kills = participant_stats.get("kills")
    match.deaths = participant_stats.get("deaths")
    match.gold_earned = participant_stats.get("goldEarned")
    match.double_kills = participant_stats.get("doubleKills")
    match.triple_kills = participant_stats.get("tripleKills")
    match.quadra_kills = participant_stats.get("quadraKills")
    match.penta_kills = participant_stats.get("pentaKills")
    match.damage_dealt = participant_stats.get("totalDamageDealtToChampions")
    match.save()

