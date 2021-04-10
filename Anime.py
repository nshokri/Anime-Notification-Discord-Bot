
class Anime:

    name = None
    crunchyrollURL = None
    genres = None
    rating = None
    datetimeAired = None

    # Constructor
    def __init__(self, name, crunchyrollURL):
        self.name = name
        self.crunchyrollURL = crunchyrollURL
    
    # Setters
    def setGenres(self, genres):
        self.genres = genres
    
    def setRating(self, rating):
        self.rating = rating
    
    def setDateTimeAired(self, datetimeAired):
        self.datetimeAired = datetimeAired