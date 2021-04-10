from bs4 import BeautifulSoup
from googlesearch import search
import Anime as anime_card

class Webscraper:

    def __init__(self):
        pass

    # Currently params don't do anything
    def get_seasonal_anime(self, season, year):
        
        output = [] 
        with open('Crunchyroll.html', 'rb') as html_file:

            content = html_file.read()

            soup = BeautifulSoup(content, 'lxml')
            all_anime_cards = soup.find_all('div', class_ = 'wrapper hover-toggle-queue container-shadow hover-classes')

            for anime in all_anime_cards:
                # Remove episode count
                temp = anime.text.split()
                temp.pop()
                temp.pop()
                
                # Reconstruct title
                s = ''
                for n in temp:
                    s += n + ' '
                s = s.strip()

                url = anime.find('a', class_ = 'portrait-element block-link titlefix')['href']
                show = anime_card.Anime(s, 'https://www.crunchyroll.com/' + url)
                output.append(show)

        return output
        
    def google_search(self, query):
        results = []
        for j in search(query, tld="com", num=3, stop=3, pause=2):
            results.append(j)
        
        return results


w = Webscraper()
temp = w.get_seasonal_anime(0, 0)

for s in temp:
    
    for n in w.google_search(s.name + ' myanimelist'):
        if (n.find('https://myanimelist.net/anime/') != -1):
            print(n)
            break