from time import strptime
import datetime
import re
import json

# Given an array of anime objects returns only those with genres in the desired filters
def filter_by_genre(anime_list, filters):
    in_filter = []
    if len(filters) != 0:
        for anime in anime_list:
            for genre in anime.genres:
                if genre in filters:
                    in_filter.append(anime)
                    break
        return in_filter
    else:
        return anime_list

# returns datetime converted to PST given the date aired and time broadcasted from MyAnimeList
def parse_datetime(aired, broadcast):

    # convert airing date and broadcast times to arrays
    date_arr = re.sub(" to.*", "", aired.replace(",", "")).split(" ")
    broadcast_arr = re.search("[0-9]{2}:[0-9]{2}", broadcast).span(0)
    broadcast_arr = broadcast[broadcast_arr[0]:broadcast_arr[1]].split(":")

    # parse arrays
    year = int(date_arr[2])
    month = strptime(date_arr[0], "%b").tm_mon
    day = int(date_arr[1])
    hour = int(broadcast_arr[0])
    minute = int(broadcast_arr[1])

    # format/return datetime (JST -> PST)
    result_datetime = datetime.datetime(year, month, day, hour, minute) - datetime.datetime(year, month, day, 14, 30) + datetime.datetime(year, month, day)
    return result_datetime

# given string of genres return as array
def get_genre_arr(genres):
    genre_arr = genres.split(", ")
    for i in range(0, len(genre_arr)):
        genre = genre_arr[i]
        genre_arr[i] = genre[0:int(len(genre) / 2)]  
    return genre_arr

# returns array of anime names being tracking
def get_tracked():
    f = open('config.json', 'r')
    data = json.load(f)
    return data["tracking"]

# returns array of genre filters being used
def get_filters():
    f = open('config.json', 'r') 
    data = json.load(f)
    return data["filters"]

# adds given filter to the filters array in json file
# iff the given filter is not already present
def add_filter(filter):
    f = open('config.json', 'r')
    data = json.load(f)

    if filter not in data["filters"]:
        data["filters"].append(filter)
    else:
        return False

    f = open('config.json', 'w')
    json.dump(data, f)
    return True

# adds given anime to the tracked array in json file
# iff the given anime is not already present
def add_tracked(anime_name):
    f = open('config.json', 'r')
    data = json.load(f)

    if anime_name not in data["tracking"]:
        data["tracking"].append(anime_name)
    else:
        return False

    f = open('config.json', 'w')
    json.dump(data, f)
    return True

# remove given filter from the array in json file
# iff it exists
def remove_filter(filter):
    f = open('config.json', 'r')
    data = json.load(f)

    if (filter in data["filters"]):
        data["filters"].remove(filter)
    else:
        return False

    f = open('config.json', 'w')
    json.dump(data, f)
    return True

# remove given filter from the array in json file
# iff it exists
def remove_tracked(anime_name):
    f = open('config.json', 'r')
    data = json.load(f)

    if (anime_name in data["tracking"]):
        data["tracking"].remove(anime_name)
    else:
        return False

    f = open('config.json', 'w')
    json.dump(data, f)
    return True

# returns true if anime was just released, false otherwise
def just_aired(anime):
    curr_day = datetime.datetime.today().strftime("%A")
    curr_time = datetime.datetime.now().time().replace(second=0, microsecond=0)

    anime_air_day = anime.datetime_aired.strftime("%A")
    anime_air_time = anime.datetime_aired.time()

    return curr_day == anime_air_day and curr_time == anime_air_time

def get_last_episode(anime):
    episodes = 0
    curr_datetime = anime.datetime_aired

    while curr_datetime.date() < datetime.datetime.now().date():
        episodes += 1
        curr_datetime += datetime.timedelta(days=7)

    return str(episodes)
