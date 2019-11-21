import os
import discord
import requests
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD = os.environ.get("DISCORD_GUILD")
STATS_API = os.environ.get("LEAGUE_STATS_API_URL")

bot = commands.Bot(command_prefix='!')

@bot.command(name='stats')
async def summoner_stats(ctx, summoner, count=None):
    """
    Retrieve a set of statistics for a summoner from all games currently on record for that summoner in the LeagueStats app.

    The LeagueStats API will only return statistics from classic game modes (ranked and unranked).

    Example:
        !stats ketsun
    """
    stats = requests.get(f"{STATS_API}/summoners/{summoner}/stats/", params={"count": count}).json()
    stats.pop("id")

    embed = discord.Embed(title=f"Statistics for {summoner} for {'all games on record' if not count else 'past ' + count + ' game(s)'}:", description="", color=0x00ff00)
    for key, value in stats.items():
        embed.add_field(name=key.replace("_", " ").title(), value=value, inline=True)
    await ctx.send("", embed=embed)
    
@bot.command(name='bans')
async def champ_bans(ctx, summoner, champ, role=None):
    """
    Displays in Discord a list of champions a summoner should ban while planning to play a specific champion.  Also displays a list of 
    champions the summoner plays well against.

    Contacts the LeagueStats API for the set of high percentage and low percentage win rates for a given summoner/champion combination.
    Optionally, role may be provided to only retrieve matches played as a specific role.

    The results are formatted into two embed objects for Discord - one with a green border for high percentage win rates and one with
    a red border for low percentage win rates.

    Example:
        !bans ketsun ekko
        !bans ketsun orianna mid
    """
    stats = requests.post(f"{STATS_API}/summoners/{summoner}/bans/", data={"champ": champ, "role": role}).json()

    embed = discord.Embed(title=f"When playing as {champ}, {summoner} performs well against", description="", color=0x00ff00)
    for key, value in stats.get("high").items():
        embed.add_field(name=key, value=f"{value}% win rate", inline=False)
    await ctx.send("", embed=embed)

    embed = discord.Embed(title=f"When playing as {champ}, {summoner} performs poorly against", description="", color=0xff0000)
    for key, value in stats.get("low").items():
        embed.add_field(name=key, value=f"{value}% win rate", inline=False)
    await ctx.send("", embed=embed)

@bot.command(name='recent')
async def summoner_recent(ctx, summoner, count=3):
    """
    Retrieve <count> recent games from the LeagueStats API for the summoner name provided.  Formats the match list into readable
    text and colors wins as green and losses as red.

    A subset of match metrics (KDA, game mode, etc.) are provided alongside each match in the list.

    Example:
        !recent ketsun 15
    """
    matches = requests.get(f"{STATS_API}/summoners/{summoner}/recent/?count={count}").json()

    message = f"Top {count} most recent games for {summoner}:\n```diff\n"

    for match_data in matches:
        win = "Win" if match_data["win"] else "Loss"
        prefix = "+"if match_data["win"] else "-"
        timestamp = match_data['timestamp'].replace("T", " ").replace("Z", " ")
        match_stats = f"{match_data['kills']}/{match_data['deaths']}/{match_data['assists']}"
        try:
            kda = float(match_data['kills'] + match_data['assists']) / float(match_data['deaths'])
        except:
            kda = float(match_data['kills'] + match_data['assists'])

        message += f"{prefix} {timestamp}: {win} as {match_data['champ_name']} playing {match_data['queue_str']} ({match_stats})\n"

    message += "```"
    await ctx.send(message)

bot.run(TOKEN)
