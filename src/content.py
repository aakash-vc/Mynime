from utils import Utils
import requests
from bs4 import BeautifulSoup

class Content:
    def __init__(self):
        self.client = None

    def getPageData(self, url):
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        tit = soup.select('div.media-card a.title')
        links = [str(x).split(' ')[3].split('=')[1].split('/')[2:4] for x in tit]

        message = ''
        for link in links:
            message += '{0:<8}'.format(link[0]) + f'{link[1]}\n'
        
        prompt = 'Press Enter to continue..\n'
        message += prompt
        self.client.send(f'\n{message}'.encode('utf-8'))
        print('Sent page data')

    def browseMenu(self, client):
        self.client = client

        options = 'Content Type\n1 Anime\n2 Manga\nOption: '
        self.client.send(options.encode('utf-8'))
        print('Sent Content Type Options')
        type = self.client.recv(1024).decode()

        try:
            menu = "Browse Options\n1 Trending\n2 All Time Popular\n3 Search\n4 Go Back\nOption: "

            while True:
                self.client.send(menu.encode('utf-8'))
                print('Sent Browse Menu')
                choice = self.client.recv(1024).decode()

                if choice == '1':
                    if type == '1':
                        url = 'https://anilist.co/search/anime/trending'
                    elif type == '2':
                        url = 'https://anilist.co/search/manga/trending'

                    self.getPageData(url)
                    
                elif choice == '2':
                    if type == '1':
                        url = 'https://anilist.co/search/anime/popular'
                    elif type == '2':
                        url = 'https://anilist.co/search/manga/popular'

                    self.getPageData(url)
                    
                elif choice == '3':
                    pass

                elif choice == '4':
                    break

                else:
                    self.client.send('Invalid option'.encode('utf-8'))

        except Exception as error:
            print(error)