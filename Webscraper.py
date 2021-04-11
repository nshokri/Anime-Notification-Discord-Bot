from bs4 import BeautifulSoup
from googlesearch import search
from helper import parse_datetime, get_genre_arr
from datetime import datetime
import requests
import Anime as anime_card
import time

class Webscraper:

    def __init__(self):
        pass

    # Currently params don't do anything
    def get_seasonal_anime(self, season, year):
        #TODO: DEL ME
        start = datetime.now()

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
                s = ' '.join(temp).strip()

                url = anime.find('a', class_ = 'portrait-element block-link titlefix')['href']
                show = anime_card.Anime(s, 'https://www.crunchyroll.com/' + url)
                output.append(show)


                # Get the image for the anime
                images = soup.find_all('img', class_ = 'portrait')
                for image in images:
                    if image['alt'] == s:
                        output[-1].image_url = image['src']
                        break

        #TODO: Might possibly have a query error here
        remove_after = []
        for i in range(len(output)):
            search = self.google_search(output[i].name + ' myanimelist')
            found = False

            for n in search:
                if (n.find('https://myanimelist.net/anime/') != -1):
                    
                    # Get last season
                    output[i].mal_url = self.find_last_season(n[0:n.rindex('/')])

                    # Set up new soup for the new MAL page
                    r = requests.get(output[i].mal_url)
                    soup = BeautifulSoup(r.text, 'lxml')

                    # Remove once out of loop
                    if self.get_property(soup, 'span', 'Type:', 'dark_text', True).find('TV') == -1 or self.get_property(soup, 'div', 'Aired:', 'spaceit', False) == None or self.get_property(soup, 'div', 'Broadcast:', 'spaceit', False) == None:
                        remove_after.append(i)
                        '''
                        print('Removing: ' + str(i))
                        print(self.get_property(soup, 'span', 'Type:', 'dark_text', True).find('TV') == -1)
                        print(self.get_property(soup, 'div', 'Aired:', 'spaceit', False) == None)
                        print(self.get_property(soup, 'div', 'Broadcast:', 'spaceit', False) == None)'''
                        break

                    # Get airing datetime
                    #output[i].datetime_aired = parse_datetime(self.get_air_time(soup), self.get_broadcast_time(soup))
                    
                    output[i].datetime_aired = parse_datetime(self.get_property(soup, 'div', 'Aired:', 'spaceit', False), self.get_property(soup, 'div', 'Broadcast:', 'spaceit', False))
                    
                    # Get rating
                    output[i].rating = self.get_property(soup, 'span', 'Score:', 'dark_text', True).split()[0]

                    # Get genres
                    output[i].genres = get_genre_arr(self.get_property(soup, 'span', 'Genres:', 'dark_text', True))

                    #print(output[i].mal_url)
                    found = True
                    break
            
            if not found:
                remove_after.append(i)
                #print('Remove 2: ' + str(i))

        # Recreate array, ignoring elements that should have been removed
        new_output = []
        for i in range(len(output)):
            if (i not in remove_after):
                new_output.append(output[i])
        output = new_output

        # Scrape MAL for genere, airing time, etc.
        '''
        for i in range(len(output)):
            print('------------------------------------------------------------------')
            print('Name: ' + output[i].name)
            print('Airing Time: ', end = ' ')
            print(output[i].datetime_aired)
            print('Genres:', end =' ')
            print(output[i].genres)
            print('Ratings: ' + output[i].rating)
            print('MAL URL: ' + output[i].mal_url)
            print('Crunchyroll URL: ' + output[i].crunchyroll_url)
            print('Image URL: ' + output[i].image_url)
            print('------------------------------------------------------------------\n\n\n')

        print('Total runtime: ', end = ' ')
        print(datetime.now() - start)
        print('Anime Count: ' + str(len(output)))'''

        '''
        test_anime = Anime('Mashiro no Oto', 'https://myanimelist.net/anime/42590/Mashiro_no_Oto/episode')
        test_anime.mal_url = 'https://myanimelist.net/anime/42590/Mashiro_no_Oto/episode'
        test_anime.crunchyroll_url = 'https://www.crunchyroll.com/those-snow-white-notes'
        test_anime.rating = '5.65'
        test_anime.genre = [Music, Slice of Life, Drama, School, Shounen]
        test_anime.datetime_aired
        output.append()'''

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
            
            if n.text.find('Sequel:') != -1 and self.is_currently_airing(soup) and self.get_property(soup, 'span', 'Type:', 'dark_text', True) == 'TV':
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
    '''
    def get_air_time(self, soup) -> str:
        text = soup.find_all('div', class_ = 'spaceit')

        for n in text:
            if n.text.find('Aired:') != -1:
                aired_date = n.text.split()
                del aired_date[0]

                return ' '.join(aired_date).strip()


    def get_broadcast_time(self, soup) -> str:
        text = soup.find_all('div', class_ = 'spaceit')

        for n in text:
            if n.text.find('Broadcast:') != -1:
                broadcast_time = n.text.split()
                del broadcast_time[0]

                return ' '.join(broadcast_time).strip()
    
    def get_generes(self, soup):
        text = soup.find_all('div', class_ = 'spaceit')

        for n in text:
            if n.text.find('Generes:') != -1:
                generes = n.text.split()
                del broadcast_time[0]

                return ' '.join(broadcast_time).strip()
    '''

    def get_property(self, soup, attribute: str, property: str, style: str, parent: bool):
        text = soup.find_all(attribute, style)
        
        for n in text:
            if n.text.find(property) != -1:
                prop = n.text.split() if not parent else n.parent.text.split()

                #print(n.parent.text)
                del prop[0]

                return ' '.join(prop).strip()

w = Webscraper()
temp = w.get_seasonal_anime(0, 0)
#r = requests.get('https://myanimelist.net/manga/99884/Thunderbolt_Fantasy__Touriken_Yuuki')
#soup = BeautifulSoup(r.text, 'lxml')

#print(w.get_property(soup, 'span', 'Type:', 'dark_text', True))
#print(w.get_property(soup, 'span', 'Type:', 'dark_text', True))
#print("YEEEEEESSSS")

#print(w.get_property(soup, 'div', 'Aired:', 'spaceit', False))
#print(w.get_property(soup, 'div', 'Broadcast:', 'spaceit', False))
#print(parse_datetime(, self.get_property(soup, 'span', 'Broadcast:', 'dark_text', False)))