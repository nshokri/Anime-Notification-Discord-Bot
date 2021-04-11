# Anime-Notification-Discord-Bot

<img src="img/capture.PNG">

# Project Goals
Create a live-time notification bot that lets users know when a new episode of their favorite show is available to view.
- Learn how to use web scraping tools in Python
- Learn how to make a Discord bot in Python

# User Experience Example
1) Live demo during presentation
2) You can find all the data we collected from webscraping in the _"Web Scraped Data.txt"_ file in the repo

# Implementation Details

**Language:** Python
## Modules:
- `beautifulsoup4`
- `lxml`
- `google`
- `requests`
- `discord.py`

Used _"requests"_, _"beatifulsoup4"_. and _"lxml"_ for web scraping and parsing html data from Crunchyroll and MyAnimeList. Used _"google"_ for doing google queries.

# Trying it out yourself
Make sure you have Python 3.9 or higher

Type in command line:\
**pip install -r requirements.txt**

_Getting a Discord API key_:
1. Go to Discord developer portal
2. Create new application
3. In app, go to bots tab, create a new bot
4. Click "Copy Token" for the new bot