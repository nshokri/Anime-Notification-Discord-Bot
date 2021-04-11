import discord
from discord.ext import commands, tasks
from Webscraper import Webscraper
import time
import helper

REFRESH_RATE = 60
CHANNEL_ID = 830690599447035914
TOKEN = "ODMwMjM0MTA1ODk1MTkwNTU5.YHDtww.FiNA3g2KK3luTIXWz1QmLjgPhvQ"

client = discord.Client()
ws = Webscraper()
anime_list = ws.get_seasonal_anime(0, 0)

@client.event
async def on_ready():
    print("Bot is online")
    check_for_updates.start()

@tasks.loop(seconds = REFRESH_RATE)
async def check_for_updates():
    filtered_anime = helper.filter_by_genre(anime_list, helper.get_filters())
    print("filtered: ", end=" ")
    print(filtered_anime)
    for anime in filtered_anime:
        if helper.just_aired(anime):
            print(anime.datetime_aired)
            await send_notifications(anime)

def create_embeded_message(name, genres, rating, link, day_aired, time_aired, latest_episode, image):
    embed_var = discord.Embed(title="Episode " + latest_episode + " of \"" + name + "\" Just Came Out!", description="Watch here: " + link, color=0xF78C25)
    embed_var.add_field(name="__Day Aired__", value=day_aired, inline=True)
    embed_var.add_field(name="__Time Aired__", value=time_aired, inline=True)
    embed_var.add_field(name="__Rating (" + str(round(float(rating) / 2, 2)) + "/5)__", value=round(float(rating) / 2) * "⭐", inline=True)
    embed_var.add_field(name="__Genre__", value=genres, inline=True)
    embed_var.set_image(url = image)
    return embed_var

async def send_notifications(anime):

    date = anime.datetime_aired.strftime("%d/%m/%y")
    time = anime.datetime_aired.strftime("%I:%M %p")
    genres = ""
    if anime.genres != None:
        for i in range(0, len(anime.genres)):
            genres += anime.genres[i]
            if i != len(anime.genres) - 1:
                genres += ", "
    else:
        genres = "N/A"

    channel = client.get_channel(CHANNEL_ID)
    embed_message = create_embeded_message(anime.name, genres, anime.rating, anime.crunchyroll_url, date, time, str(helper.get_last_episode(anime)), anime.image_url)
    await channel.send(embed = embed_message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    command = message.content
    if command.startswith("!track"):
        anime_name = command[int(command.index(" ") + 1):]
        if helper.add_tracked(anime_name):
            await message.channel.send("*Now Tracking* " + "**" + anime_name + "**")
        else:
            await message.channel.send("**" + anime_name + "** *is already being tracked*")
    
    elif command.startswith("!untrack"):
        anime_name = command[int(command.index(" ") + 1):]
        if helper.remove_tracked(anime_name):
            await message.channel.send("*No Longer Tracking* " + "**" + anime_name + "**")
        else:
            await message.channel.send("**" + anime_name + "** *is not currently being tracked*")

    elif command.startswith("!addg"):
        genre = command[int(command.index(" ") + 1):]
        if helper.add_filter(genre):
            await message.channel.send("*Now including* **" + genre + "** *in filter*")
        else:
            await message.channel.send("**" + genre + "** *is already included in filter*")
    
    elif command.startswith("!removeg"):
        genre = command[int(command.index(" ") + 1):]
        if helper.remove_filter(genre):
            await message.channel.send("*No longer including* **" + genre + "** *in filter*")
        else:
            await message.channel.send("**" + genre + "** *is not currently included in filter*")

    elif command.startswith("!help"):
        embed_var = discord.Embed(title="Current Command List", description="", color=0xF78C25)
        embed_var.add_field(name="```!track [Anime Name]```", value="Tracks an anime and notifies the server when a new episode comes out", inline=False)
        embed_var.add_field(name="```!untrack [Anime Name]```", value="Removes an anime from tracking list", inline=False)
        embed_var.add_field(name="```!addg [Genre]```", value="Adds a genre to the filter", inline=False)
        embed_var.add_field(name="```!removeg [Genre]```", value="Removes a genre to the filter", inline=False)
        await message.channel.send(embed = embed_var)

client.run(TOKEN)