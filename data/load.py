import pandas as pd
from util import create_df, load_table, get_json

def load(option):
    map_object = get_json()
    print('Got json object.')
    maps = map_object[option]

    if option == 'anime':
        columns = ['anime_id', 'title', 'url', 'last_modified', 'change_frequency', 'priority']
        table = 'anime_index'

    elif option == 'manga':
        columns=['manga_id', 'title', 'url', 'last_modified', 'change_frequency', 'priority']
        table = 'manga_index'

    elif option == 'characters':
        columns = ['character_id', 'title', 'url', 'last_modified', 'change_frequency', 'priority']
        table = 'character_index'

    elif option == 'staff':
        columns = ['staff_id', 'title', 'url', 'last_modified', 'change_frequency', 'priority']
        table = 'staff_index'

    elif option == 'articles':
        columns = ['title', 'url', 'last_modified', 'change_frequency', 'priority']
        table = 'article_index' 

    df = pd.DataFrame(columns=columns)
    length = len(maps)
    print('Loading maps:')
    for ind, map in enumerate(maps, start=1):
        df = pd.concat([df, create_df(columns, map)], ignore_index=True)
        print(f'{ind}/{length} Done.')
        print(df)
    print('Created dataframe')
    print(df.head())
    print(len(df))

    load_table(df, table)
    print('Table loaded')

if __name__ == '__main__':
    pass