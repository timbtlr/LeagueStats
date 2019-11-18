import datetime
from datetime import timezone
from time import sleep

from api_client.league_client import api_client, RateLimitedException
from champion.models import Champion
from match.models import MatchPerformance
from summoner.models import Summoner


def get_or_create_champion(champ_id):
    """
    Collect information about and save a champion into the system if the champion does
    not already exist.  If the champion exists, return it without contacting the API.
    """
    try:
        return Champion.objects.get(id=champ_id)
    except Champion.DoesNotExist:
        champ_data = api_client.get_single_champion_data(champ_id)
        return Champion.objects.create(
            id=champ_id,
            name=champ_data.get("name"),
            title=champ_data.get("title")
        )


def collect_all_new_matches():
    """
    Collect the most recent set of matches for each summoner on record.  
    If a summoner has matches on record then only ask the API for matches since their
    most recent match.  Otherwise ask for all matches for the summoner.
    """
    for summoner in Summoner.objects.all():
        latest_matches = summoner.matchperformance_set.all()
        if latest_matches.exists():
            match_epoch = int(latest_matches.latest("timestamp").timestamp.timestamp()*1000)
            collect_new_matches(summoner.id, begin_epoch=match_epoch)
        else:
            collect_new_matches(summoner.id)


def get_or_create_match_performance(account_id, match_id, match_time, champ_id):
    """
    Retrieves an existing MatchPerformance model by (match_id, account_id) or creates one from match details.
    Query the API to get detailed match information before filling in the new MatchPerformance object.
    """
    try:
        return MatchPerformance.objects.get(match_id=match_id, summoner__id=account_id)
    except MatchPerformance.DoesNotExist:
        try:
            match_data = api_client.get_match(match_id)
            for player in match_data.get("participantIdentities", []):
                if player.get("player").get("accountId") == account_id:
                    participant_id = player.get("participantId")
                    for participant in match_data.get("participants"):
                        if participant.get("participantId") == participant_id:
                            participant_stats = participant.get("stats", {})
                            match = MatchPerformance(match_id=match_data.get("gameId"))
                            match.timestamp = datetime.datetime.fromtimestamp(int(match_time / 1000 - 18000)).replace(tzinfo=timezone.utc)
                            match.summoner = Summoner.objects.get(id=account_id)
                            match.mode = match_data["gameMode"]
                            match.lane = participant.get("timeline", {}).get("lane") + "/" + participant.get("timeline", {}).get("role")
                            match.champ = champ_id
                            match.game_type = match_data["queueId"]
                            if match.mode != "ARAM":
                                for opponent in match_data.get("participants"):
                                    lane = opponent.get("timeline", {}).get("lane") + "/" + opponent.get("timeline", {}).get("role")
                                    if lane == match.lane and opponent.get("participantId") != participant_id:
                                        match.opposing_champ = opponent["championId"]
                            match.win = participant_stats.get("win")
                            match.level = participant_stats.get("champLevel")
                            match.kills = participant_stats.get("kills")
                            match.deaths = participant_stats.get("deaths")
                            match.assists = participant_stats.get("assists")
                            match.gold_earned = participant_stats.get("goldEarned")
                            match.double_kills = participant_stats.get("doubleKills")
                            match.triple_kills = participant_stats.get("tripleKills")
                            match.quadra_kills = participant_stats.get("quadraKills")
                            match.penta_kills = participant_stats.get("pentaKills")
                            match.damage_dealt = participant_stats.get("totalDamageDealtToChampions")
                            match.save()
                            return match
        except RateLimitedException:
            print("Rate limited - sleeping 3 minutes")
            sleep(160)
            get_or_create_match_performance(account_id, match_id, match_time, champ_id)



def get_matches(account_id, begin_epoch=None, begin_index=0):
    """
    Paginate through all matches for the provided summoner account yielding each match as it is collected.

    There is currently a bug in the League API where the totalGames field is sometimes incorrect.  Because of that, 
    we paginate through the API until the results are an empty list.
    """
    more_to_query = True
    while more_to_query:
        try:
            matches = api_client.get_match_list(account_id, begin_index=begin_index, begin_epoch=begin_epoch).get("matches", [])
            yield from matches
            begin_index += len(matches)
            more_to_query = len(matches) > 0
        except RateLimitedException:
            print("Rate limited - sleeping 3 minutes")
            sleep(160)


def collect_new_matches(account_id, begin_epoch=None):
    """
    Collect and save MatchPerformance objects for the given account ID for matches occurring after the
    provided epoch.
    """
    for match in get_matches(account_id, begin_epoch):
        match_id = match.get("gameId")
        match_time = match.get("timestamp")
        champ_id = match.get("champion")
        champ = get_or_create_champion(champ_id)
        match_performance = get_or_create_match_performance(account_id, match_id, match_time, champ_id)
        print(match_performance)
