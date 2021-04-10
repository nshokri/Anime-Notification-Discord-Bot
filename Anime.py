class Anime:

    name = None
    crunchyrollURL = None
    genres = None
    rating = None
    datetimeAired = None

    def __init__(self, name, crunchyrollURL):
        self.name = name
        self.crunchyrollURL = crunchyrollURL
    
    def setGenres(self, genres):
        self.genres = genres
    
    def setRating(self, rating):
        self.rating = rating
    
    def setDateTimeAired(self, datetimeAired):
        self.datetimeAired = datetimeAiredAired