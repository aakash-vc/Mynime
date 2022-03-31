import socket
import _thread
import json
import src
from src.user import Signup, User
from src.utils import Utils
from src.content import Content

class TCPServer():
    user = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def shutdown_server(self):
        ''' Shutdown the server '''

        print('Shutting down server...')
        self.sock.close()

    def handleUser(self, client):

        try:
            menu = "User Menu\n1 My Lists\n2 Browse\n3 Edit Profile\n4 Logout\nOption: "

            while True:
                client.send(menu.encode('utf-8'))
                print('Sent User Menu')
                choice = client.recv(1024).decode()

                if choice == '1':
                    pass

                elif choice == '2':
                    Content().browseMenu(client)

                elif choice == '3':
                    pass

                elif choice == '4':
                    break

                else:
                    client.send('Invalid option'.encode('utf-8'))

        except Exception as error:
            print(error)

        

    def handle_client(self, client_sock, client_address):
        """ Handle the accepted client's requests """

        try:
            menu = "Welcome to Mynime\n\n1 Login\n2 Signup\n3 Browse\n('exit' to exit interface)\nOption: "

            while True:
                client_sock.send(menu.encode('utf-8'))
                print('Sent Menu')
                choice = client_sock.recv(1024).decode()

                if choice == 'exit':
                    break

                elif choice == '1':
                    self.user = User().login(client_sock)
                    if self.user:
                        print('User logged in')
                        self.handleUser(client_sock)
                        self.user = None
                        print('User logged out')
                    
                elif choice == '2':
                    status = Signup(client_sock).signup()
                    if status:
                        client_sock.send('Signup Successful'.encode('utf-8'))
                    else:
                        client_sock.send('Signup Failed'.encode('utf-8'))

                elif choice == '3':
                    Content().browseMenu(client_sock)

            print(f'Connection closed by {client_address}')

        except OSError as error:
            print(error)

        finally:
            print(f'Closing client socket for {client_address}...')
            client_sock.close()
            print(f'Client socket closed for {client_address}')

    def configure_server(self):
        ''' Configure the server '''

        # create TCP socket with IPv4 addressing
        print('Creating socket...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        # bind server to the address
        print(f'Binding server to {self.host}:{self.port}...')
        self.sock.bind((self.host, self.port))
        print(f'Server bound to {self.host}:{self.port}')

    def wait_for_client(self):
        try:
            print('Listening for incoming connection')
            self.sock.listen(10)

            client_sock, client_address = self.sock.accept()
            print(f'Accepted connection from {client_address}')
            self.handle_client(client_sock, client_address)
        
            '''
            while True:
                client_sock, client_address = self.sock.accept()
                print(f'Accepted connection from {client_address}')
                _thread.start_new_thread(self.handle_client, (client_sock, client_address,))
            '''

        except KeyboardInterrupt:
            self.shutdown_server()

def main():
    tcp_server_multi_client = TCPServer('127.0.0.1', 4444)
    tcp_server_multi_client.configure_server()
    tcp_server_multi_client.wait_for_client()

if __name__ == '__main__':
    main()