import discord
from discord.ext import commands, tasks
#import Webscraper as web
import time
import helper

REFRESH_RATE = 60
CHANNEL_ID = 830226925669974056
TOKEN = "ODMwMjM0MTA1ODk1MTkwNTU5.YHDtww.FiNA3g2KK3luTIXWz1QmLjgPhvQ"

client = discord.Client()
anime_list = [1,2]    #web.getSeasonalAnime()


@client.event
async def on_ready():
    print("Bot is online")
    check_for_updates.start()


@tasks.loop(seconds = 10)
async def check_for_updates():
    if len(anime_list) > 0:
        await send_notifications()

def create_embeded_message(name, genres, rating, link, day_aired, time_aired, latest_episode, image):
    embed_var = discord.Embed(title="Episode " + latest_episode + " of " + name + " Just Came Out!", description="Watch here: " + link, color=0xF78C25)
    embed_var.add_field(name="__Day Aired__", value=day_aired, inline=True)
    embed_var.add_field(name="__Time Aired__", value=time_aired, inline=True)
    embed_var.add_field(name="__Rating__", value=rating * "⭐", inline=True)
    embed_var.add_field(name="__Genre__", value=genres, inline=True)
    embed_var.set_image(url = image)
    return embed_var

async def send_notifications():
    """
    for anime in animes:
        animeLink = anime.getCrunchyrollURL()
        currentEpisodeNum = web.getLastEpisode(animeLink)
        animeImage = web.getImageURL(animeLink)
    """

    channel = client.get_channel(CHANNEL_ID)
    embed_message = create_embeded_message("My Hero Academia", "Action, Fantasy, Shonen", 4, "https://www.crunchyroll.com/my-hero-academia/videos", "3/2/20", "7:50 PM", "3", "https://img1.ak.crunchyroll.com/i/spire3/137c90ecc4fae013811fab5275b307791617056778_full.jpg")
    await channel.send(embed = embed_message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    command = message.content
    if command.startswith("!track"):
        animeName = command[command.index(" "):]
        await message.channel.send("**Now Tracking: **" + animeName)

client.run(TOKEN)