#!/home/vulcan/airflow/airflow_env/bin/python

import requests
from bs4 import BeautifulSoup
import json

def get_category_maps(maps):
    anime_maps = []
    manga_maps = []
    character_maps = []
    staff_maps = []
    article_maps = []

    for map in maps:
        category = map.loc.text.split('/')[-1]
        if 'anime' in category:
            anime_maps.append(map.loc.text)
        elif 'manga' in category:
            manga_maps.append(map.loc.text)
        elif 'character' in category:
            character_maps.append(map.loc.text)
        elif 'staff' in category:
            staff_maps.append(map.loc.text)
        elif 'article' in category:
            article_maps.append(map.loc.text)

    map_data = {'anime': anime_maps,
                'manga': manga_maps,
                'characters': character_maps,
                'staff': staff_maps,
                'articles': article_maps}

    return map_data

def get_map():
    sitemap = 'https://anilist.co/sitemap/index.xml'
    response = requests.get(sitemap, timeout=5)
    print('got response')

    soup = BeautifulSoup(response.text, 'lxml')
    maps = soup.select('sitemap')
    print('got soup')

    map_data = get_category_maps(maps)
    print('got maps')
    
    json_object = json.dumps(map_data, indent=4)
    with open('map_data.json', 'w') as file:
        file.write(json_object)
    print('json created')

if __name__ == '__main__':
    pass