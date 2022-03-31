import psycopg2
import bcrypt

class DB:
    def __init__(self):
        pass

    def hashPassword(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(10))

    def checkPassword(self, password, password_hash):
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    def getConnection(self):
        dbname = 'mynime'
        user = 'student'
        password = ''
        try:
            conn = psycopg2.connect('dbname={} user={} password={}'.format(dbname, user, password))
            conn.set_session(autocommit=True)
        except psycopg2.Error as e:
            print('Error: Could not connect to the database')
            print(e)
    
        return conn

    def getCursor(self, conn):
        try:
            cur = conn.cursor()
        except psycopg2.Error as e:
            print('Error: Could not get cursor to the database')
            print(e)
    
        return cur

    def getAnimeList(self, user_id):
        query = "select list, array_agg(anime_id) from anime_list where user_id = %s GROUP BY list;"
        conn = self.getConnection()
        cur = self.getCursor(conn)

        try:
            cur.execute(query,(user_id,))
        except psycopg2.Error as e:
            print('Error: Error retrieving user data')
            print(e)
            return

        anime_list = {}
        data = cur.fetchall()
        for row in data:
            anime_list[row[0]] = row[1]

        cur.close()
        conn.close()

        return anime_list

    def getMangaList(self, user_id):
        query = "select list, array_agg(manga_id) from manga_list where user_id = %s GROUP BY list;"
        conn = self.getConnection()
        cur = self.getCursor(conn)

        try:
            cur.execute(query,(user_id,))
        except psycopg2.Error as e:
            print('Error: Error retrieving user data')
            print(e)
            return

        manga_list = {}
        data = cur.fetchall()
        for row in data:
            manga_list[row[0]] = row[1]

        cur.close()
        conn.close()

        return manga_list        


    def getUser(self, username, password):
        query = "SELECT user_id, username, gender, dob, country, password from users WHERE username = %s;"
        
        conn = self.getConnection()
        cur = self.getCursor(conn)
        
        try:
            cur.execute(query,(username,))
        except psycopg2.Error as e:
            print('Error: Error retrieving user data')
            print(e)
            return

        data = cur.fetchone()
        if data == None:
            return

        if self.checkPassword(password, data[-1]):
            print('Login success')
            data = data[:-1]
            data.append(self.getAnimeList(data[0]))
            data.append(self.getMangaList(data[0]))
            return data[:len(data)-1]

        print('Login Failed')

        cur.close()
        conn.close()
        return        

    def addUser(self, username, password, gender, dob, country):
        hash_pwd = self.hashPassword(password)
        password = str(hash_pwd.decode())
        query = "INSERT INTO users(username, gender, dob, country, password) VALUES(%s, %s, %s, %s, %s);"

        conn = self.getConnection()
        cur = self.getCursor(conn)

        try:
            cur.execute(query,(username, gender, dob, country, password,))
            return True
        except psycopg2.Error as e:
            print('Error: Issue adding user')
            print(e)

        cur.close()
        conn.close()

        return

