
class Anime:

    name = None
    crunchyroll_url = None
    mal_url = None
    genres = None
    rating = None
    datetime_aired = None

    def __init__(self, name, crunchyroll_url):
        self.name = name
        self.crunchyroll_url = crunchyroll_url