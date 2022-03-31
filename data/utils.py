import json
import requests
import psycopg2
import psycopg2.extras as extras
from bs4 import BeautifulSoup
import pandas as pd

def get_json():
    with open('map_data.json', 'r') as json_file:
        return json.load(json_file)

def get_connection():
    dbname = 'mynime'
    user = 'student' #input('User: ')
    password = 'qnpiEW9s5G'  #input('Password: ')

    try:
        conn = psycopg2.connect('dbname={} user={} password={}'.format(dbname, user, password))
        conn.set_session(autocommit=True)
        print('Connected to database')
    except psycopg2.Error as e:
        print('Error: Could not connect to the database')
        print(e)
    
    return conn

def insert_table(table, cols, conn, tuples, primary):
    query = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT (%s) DO UPDATE SET last_modified = EXCLUDED.last_modified" % (table, cols, primary)
    print(query)
    cur = conn.cursor()

    try:
        extras.execute_values(cur, query, tuples)
        print('Table Updated')
    except psycopg2.Error as e:
        print('Error: insertion')
        conn.rollback()
        print(e)
    
    cur.close()

def load_table(df, table):
    columns = list(df.columns)
    primary = columns[0]
    columns_string = ','.join(columns)
    tuples = [tuple(x) for x in df.to_numpy()]
    conn = get_connection()

    insert_table(table, columns_string, conn, tuples, primary)
    conn.close()

def getTitle(id):
    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title {
                english
            }
        }
    }
    '''
    variables = {
        'id': 20
    }

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    return json.loads(response.text)['data']['Media']['title']['english']

def create_df(columns, map):
    print(columns)
    response = requests.get(map)
    soup = BeautifulSoup(response.text, 'lxml')

    url = [x.text for x in soup.select('loc')]
    title = [x.split('/')[-1] for x in url]
    lastmod = [x.text for x in soup.select('lastmod')]
    changefreq = [x.text for x in soup.select('changefreq')]
    priority = [x.text for x in soup.select('priority')]

    if map.split('/')[-1].startswith('article'):
        df = pd.DataFrame(list(zip(title, url, lastmod, changefreq, priority)), columns=columns)
    else:
        ids = [x.split('/')[4] for x in url]
        df = pd.DataFrame(list(zip(ids, title, url, lastmod, changefreq, priority)), columns=columns)
    
    return df

if __name__ == '__main__':
    pass