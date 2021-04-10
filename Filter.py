
# given an array of anime objects filter for only those with genres in the desired filter
def filterByGenre(animeList, filters):
    inFilter = []
    for anime in animeList:
        for genre in anime.genres:
            if (genre in filters):
                inFilter.append(anime)
                break
    return inFilter