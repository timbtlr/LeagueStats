import datetime
from datetime import timezone
from time import sleep
from summoner.models import Summoner
from api_client.league_client import api_client, RateLimitedException
from match.models import Match
from champion.models import Champion


def populate_champions():
    champs = list(set(list(Match.objects.values_list("champ", flat=True)) + list(Match.objects.values_list("opposing_champ", flat=True))))
    for champ in champs:
        try:
            create_champion(champ)
        except:
            pass


def create_champion(champ_id):
    try:
        return Champion.objects.get(id=champ_id)
    except Champion.DoesNotExist:
        champ_data = api_client.get_single_champion_data(champ_id)
        return Champion.objects.create(
            id=champ_id,
            name=champ_data.get("name"),
            title=champ_data.get("title")
        )


def schedule_pull_matches():
    for summoner in Summoner.objects.all():

        if summoner.match_set.count() == 0:
            pull_matches(summoner.id, begin_index=0)
        else:
            since = int(summoner.match_set.latest("timestamp").timestamp.timestamp()*1000)
            pull_matches(summoner.id, begin_index=0, begin_timestamp=since)


def pull_matches(account_id, begin_index=0, begin_timestamp=None):
    index = begin_index
    matches = api_client.get_match_list(account_id, begin_timestamp=begin_timestamp)

    while matches.get("matches", None):
        try:
            for match in matches.get("matches"):
                match_id = match.get("gameId")
                match_time = match.get("timestamp")
                champ_id = match.get("champion")
                champ = create_champion(champ_id)

                try:
                    Match.objects.get(match_id=match_id, summoner__id=account_id)
                except Match.DoesNotExist:
                    match_data = api_client.get_match(match_id)
                    match = create_match(account_id, match_time, champ_id, match_data)
                    print(match)

            index += len(matches.get("matches"))
            matches = api_client.get_match_list(account_id, begin_index=index, begin_timestamp=begin_timestamp)
        except RateLimitedException:
            print("Rate limited - sleeping 3 minutes")
            sleep(160)

def create_match(account_id, match_time, champ_id, match_data):
    # Get participant ID
    for player in match_data.get("participantIdentities"):
        if player.get("player").get("accountId") == account_id:
            participant_id = player.get("participantId")

            for participant in match_data.get("participants"):
                if participant.get("participantId") == participant_id:
                    participant_stats = participant.get("stats", {})
                    match = Match(match_id=match_data.get("gameId"))
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


