import discord
import Webscraper as web
import time

refreshRate = 1
channelID = 830226925669974056

client = discord.Client()
newAnimes = []

@client.event
async def on_ready():
    while True:
        if checkForUpdates():
            await sendNotifications()
        time.sleep(refreshRate * 60)

def checkForUpdates():
    animes = [1,2] #web.getSeasonalAnime()
    return len(animes) > 0

def createEmbededMessage(name, genres, rating, link, dayAired, timeAired, latestEpisode, image):


    embedVar = discord.Embed(title="Episode " + latestEpisode + " of " + name + " Just Came Out!", description="Watch here: " + link, color=0xF78C25)
    embedVar.add_field(name="__Day Aired__", value=dayAired, inline=True)
    embedVar.add_field(name="__Time Aired__", value=timeAired, inline=True)
    embedVar.add_field(name="__Rating__", value=rating * "⭐", inline=True)
    embedVar.add_field(name="__Genre__", value=genres, inline=True)
    embedVar.set_image(url = image)
    return embedVar

async def sendNotifications():
    """
    for anime in animes:
        animeLink = anime.getCrunchyrollURL()
        currentEpisodeNum = web.getLastEpisode(animeLink)
        animeImage = web.getImageURL(animeLink)
    """

    channel = client.get_channel(channelID)
    embedMessage = createEmbededMessage("My Hero Academia", "Action, Fantasy, Shonen", 4, "https://www.crunchyroll.com/my-hero-academia/videos", "3/2/20", "7:50 PM", "3", "https://img1.ak.crunchyroll.com/i/spire3/137c90ecc4fae013811fab5275b307791617056778_full.jpg")
    await channel.send(embed = embedMessage)

client.run("ODMwMjM0MTA1ODk1MTkwNTU5.YHDtww.FiNA3g2KK3luTIXWz1QmLjgPhvQ")