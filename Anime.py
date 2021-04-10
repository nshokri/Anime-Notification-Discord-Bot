class Anime:

    name = None
    rating = None
    crunchyrollURL = None
    genres = []

    def __init__(self, name, rating, crunchyrollURL, genres):
        self.name = name
        self.rating = rating
        self.crunchyrollURL = crunchyrollURL
        self.genres = genres