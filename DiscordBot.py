import discord

refreshRate = 1

client = discord.Client()


@client.event
async def on_ready():
    print("Online")


def checkForUpdates():
    print("asdasd")

def sendNotifications():
    print("ADSF")