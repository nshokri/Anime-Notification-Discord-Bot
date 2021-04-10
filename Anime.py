
class Anime:

    name = None
    crunchyroll_url = None
    genres = None
    rating = None
    datetime_aired = None

    # Constructor
    def __init__(self, name, crunchyroll_url):
        self.name = name
        self.crunchyroll_url = crunchyroll_url
    
    # Setters
    def set_genres(self, genres):
        self.genres = genres
    
    def set_rating(self, rating):
        self.rating = rating
    
    def set_datetime_aired(self, datetime_aired):
        self.datetime_aired = datetime_aired