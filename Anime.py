import re

class Anime:

    name = None
    genres = []
    rating = None

    def __init__(self, name, genres, rating):
        self.name = name
        self.genres = genres
        self.rating = rating

    def getCrunchyrollURL(self):
        baseURL = "https://www.crunchyroll.com/"
        formattedName = re.sub("[-]+", "-", " ".join(re.sub("[^a-zA-Z -]+", "", self.name).split()).replace(" ", "-"))
        crunchyrollURL = baseURL + formattedName
        return crunchyrollURL