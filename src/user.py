from utils import Utils
from database import DB

class User:
    def __init__(self):
        self.__userid = None
        self.__username = None
        self.__gender = None
        self.__dob = None
        self.__country = None
        self.__anime_list = None
        self.__manga_list = None

    def getList(self, client):
        content_options = 'List Type:\n1 Anime List\n2 Manga List\nOption: '
        client.send(content_options.encode('utf-8'))
        print('Sent List Types')
        content = self.client.recv(1024).decode()
        
        if content == '1':
            pass
        elif content == '2':
            pass


    def login(self, client):
        client.send('Username: '.encode('utf-8'))
        username = client.recv(1024).decode()
        client.send('Password: '.encode('utf-8'))
        password = client.recv(1024).decode()

        user = DB().getUser(username, password)
        if not user:
            return
        
        self.__userid = user[0]
        self.__username = user[1]
        self.__gender = user[2]
        self.__dob = user[3]
        self.__country = user[4]
        self.__anime_list = user[5]
        self.__manga_list = user[6]

        return self


class Signup:
    def __init__(self, client):
        self.client = client

    def signup(self):
        self.client.send('Username: '.encode('utf-8'))
        username = self.client.recv(1024).decode()
        self.client.send('Gender: '.encode('utf-8'))
        gender = self.client.recv(1024).decode()
        self.client.send('DOB(YYYY-MM-DD): '.encode('utf-8'))
        dob = self.client.recv(1024).decode()
        self.client.send('Country: '.encode('utf-8'))
        country = self.client.recv(1024).decode()
        
        self.client.send('Password: '.encode('utf-8'))
        password = self.client.recv(1024).decode()

        status = DB().addUser(username, password, gender, dob, country)
        return status

    