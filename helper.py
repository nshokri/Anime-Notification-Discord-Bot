from time import strptime
from datetime import datetime, date, time
import re


# Given an array of anime objects returns only those with genres in the desired filters
def filter_by_genre(anime_list, filters):
    in_filter = []
    for anime in anime_list:
        for genre in anime.genres:
            if genre in filters:
                in_filter.append(anime)
                break
    return in_filter

# returns datetime converted to PST given the date aired and time broadcasted from MyAnimeList
def parse_datetime(aired, broadcast):
    date_arr = re.sub(" to.*", "", aired.replace(",", "")).split(" ")
    broadcast_arr = re.search("[0-9]{2}:[0-9]{2}", broadcast).span(0)
    broadcast_arr = broadcast[broadcast_arr[0]:broadcast_arr[1]].split(":")

    year = int(date_arr[2])
    month = strptime(date_arr[0], "%b").tm_mon
    day = int(date_arr[1])
    hour = int(broadcast_arr[0])
    minute = int(broadcast_arr[1])

    result_datetime = datetime(year, month, day, hour, minute) - datetime(year, month, day, 14, 30) + datetime(year, month, day)
    return result_datetime