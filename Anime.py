class Anime:

    name = None
    genres = []
    rating = None
    crunchyrollURL = None
    timeAired = []
    dayAired = None

    def __init__(self, name, rating, crunchyrollURL, genres, timeAired, dayAired):
        self.name = name
        self.rating = rating
        self.crunchyrollURL = crunchyrollURL
        self.genres = genres
        self.timeAired = timeAired
        self.dayAired = dayAired