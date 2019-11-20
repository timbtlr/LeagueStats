import os
import discord
import requests
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD = os.environ.get("DISCORD_GUILD")
STATS_API = os.environ.get("LEAGUE_STATS_API_URL")

bot = commands.Bot(command_prefix='!')

@bot.command(name='stats')
async def summoner_stats(ctx, summoner):
    stats = requests.get(f"{STATS_API}/summoners/{summoner}/stats/").json()
    stats.pop("id")
    embed = discord.Embed(title=f"Statistics for {summoner} for all games on record:", description="", color=0x00ff00)
    for key, value in stats.items():
        embed.add_field(name=key.replace("_", " ").title(), value=value, inline=True)
    await ctx.send("", embed=embed)
    
@bot.command(name='bans')
async def champ_bans(ctx, summoner, champ, role=None):
    stats = requests.post(f"{STATS_API}/summoners/{summoner}/bans/", data={"champ": champ, "role": role}).json()

    embed = discord.Embed(title=f"When playing as {champ}, {summoner} has never won against", description="", color=0xff0000)
    for key, value in stats.get("never").items():
        embed.add_field(name=key, value=f"{value}%", inline=False)
    await ctx.send("", embed=embed)

    embed = discord.Embed(title=f"When playing as {champ}, {summoner} has low win rates against", description="", color=0xffa500)
    for key, value in stats.get("low").items():
        embed.add_field(name=key, value=f"{value}%", inline=False)
    await ctx.send("", embed=embed)

@bot.command(name='recent')
async def summoner_recent(ctx, summoner, count=3):
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
