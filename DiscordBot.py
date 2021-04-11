import discord
from discord.ext import commands, tasks
from Webscraper import Webscraper
import time
import helper

REFRESH_RATE = 60
CHANNEL_ID = 830226925669974056
TOKEN = "ODMwMjM0MTA1ODk1MTkwNTU5.YHDtww.FiNA3g2KK3luTIXWz1QmLjgPhvQ"

client = discord.Client()
ws = Webscraper()
anime_list = ws.get_seasonal_anime(0, 0)

@client.event
async def on_ready():
    print("Bot is online")
    check_for_updates.start()

@tasks.loop(seconds = 15)
async def check_for_updates():
     filtered_anime = helper.filter_by_genre(anime_list, helper.get_filters())

     for anime in filtered_anime:
         if helper.just_aired(anime):
            await send_notifications(anime)

def create_embeded_message(name, genres, rating, link, day_aired, time_aired, latest_episode, image):
    embed_var = discord.Embed(title="Episode " + latest_episode + " of " + name + " Just Came Out!", description="Watch here: " + link, color=0xF78C25)
    embed_var.add_field(name="__Day Aired__", value=day_aired, inline=True)
    embed_var.add_field(name="__Time Aired__", value=time_aired, inline=True)
    embed_var.add_field(name="__Rating(9.4)__", value=rating * "⭐", inline=True)
    embed_var.add_field(name="__Genre__", value=genres, inline=True)
    embed_var.set_image(url = image)
    return embed_var

async def send_notifications(anime):

    date = anime.datetime_aired().strftime("%d/%m/%y")
    time = anime.datetime_aired().strftime("%I:%M %p")
    stars = round(int(anime.rating))

    channel = client.get_channel(CHANNEL_ID)
    embed_message = create_embeded_message(anime.name, anime.genres, round(stars / 2), anime.crunchyroll_url, date, time, 3, anime.image_url)
    await channel.send(embed = embed_message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    command = message.content
    if command.startswith("!track"):
        anime_name = command[int(command.index(" ") + 1):]
        if helper.add_tracked(anime_name):
            await message.channel.send("*Now Tracking:* " + "**" + anime_name + "**")
        else:
            await message.channel.send("**" + anime_name + "** *is already being tracked*")
    
    elif command.startswith("!untrack"):
        anime_name = command[int(command.index(" ") + 1):]
        if helper.remove_tracked(anime_name):
            await message.channel.send("*No Longer Tracking:* " + "**" + anime_name + "**")
        else:
            await message.channel.send("**" + anime_name + "** *is not currently being tracked*")

client.run(TOKEN)