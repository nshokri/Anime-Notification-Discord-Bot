from bs4 import BeautifulSoup
from googlesearch import search
import requests
import Anime as anime_card
import time

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


        #TODO: Might possibly have a query error here
        for i in range(len(output)):
            for n in self.google_search(output[i].name + ' myanimelist'):
                if (n.find('https://myanimelist.net/anime/') != -1):
                    
                    output[i].mal_url = n[0:n.rindex('/')]
                    output[i].mal_url = self.find_last_season(output[i].mal_url)

                    print(output[i].mal_url)
                    break

        # Scrape MAL for genere, airing time, etc.

        return output
        
    def google_search(self, query: str):
        results = []
        for j in search(query, tld = "com", num = 3, stop = 3, pause = 2):
            results.append(j)
        
        return results
    
    def find_last_season(self, mal_url: str) -> str:

        prev_url = mal_url

        try:
            while (len(self.find_next_season(mal_url)) != 0):
                mal_url = self.find_next_season(mal_url)

                time.sleep(2)
        except:
            pass
        
        return mal_url

    def find_next_season(self, mal_url: str) -> str:
        
        r = requests.get(mal_url)
        soup = BeautifulSoup(r.text, 'lxml')
        all_links = soup.find('table', class_ = 'anime_detail_related_anime').find_all('tr')
        
        for n in all_links:

            if n.text.find('Sequel:') != -1 and self.is_currently_airing(soup):
                for x in n.find_all('a'):
                    link = x['href']
                    
                    if link.find('/anime/') != -1:
                        return 'https://myanimelist.net' + link
        
        return ''

    def is_currently_airing(self, soup) -> bool:
        text = soup.find_all('div')

        for n in text:
            if n.text.find('Currently Airing') != -1:
                return True
        
        return False

    def get_air_time(self, soup) -> str:
        text = soup.find_all('div', class_ = 'spaceit')

        for n in text:
            if n.find('Aired:') != -1:
                print(n.text)



w = Webscraper()
#temp = w.get_seasonal_anime(0, 0)
r = requests.get('https://myanimelist.net/anime/42590')
soup = BeautifulSoup(r.text, 'lxml')
w.get_air_time(soup)