from bs4 import BeautifulSoup

with open('Crunchyroll.html', 'rb') as html_file:

    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')
    all_anime_cards = soup.find_all('div', class_ = 'wrapper hover-toggle-queue container-shadow hover-classes')

    for anime in all_anime_cards:

        text = anime.text
        index = 0
        for i in range(8):
            index = text.find(' ', index + 1)

        print(text[0:index])