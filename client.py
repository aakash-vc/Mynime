import socket

class TCPClient:
    ''' A simple TCP Client that uses IPv4 '''

    def __init__(self, host, port):
        self.host = host        # host address
        self.port = port        # host port
        self.conn_sock = None   # connection socket

    def create_socket(self):
        ''' Create a socket that uses IPv4 and TCP '''        
        self.conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def interact_with_server(self):
        ''' Connect and interact with a TCP Server. '''

        try:
            print('Connecting to mynime ...')
            self.conn_sock.connect((self.host, self.port))
            
            print('Connected\n\n')

            while True:
                resp = self.conn_sock.recv(1024).decode() #
                print(f'\n {resp}', end = '')
                command = input()
                if command == 'exit':
                    break
                self.conn_sock.send(command.encode('utf-8'))

        except OSError as err:
            print('Cannot connect to server')
            print(err)

        finally:
            # close socket
            print('Closing connection socket...')
            self.conn_sock.sendall('exit'.encode('utf-8'))
            self.conn_sock.close()
            print('Socket closed')

def main():
    ''' Create a TCP Client and interact with the server at 127.0.0.1:4444'''

    tcp_client = TCPClient('127.0.0.1', 4444)
    tcp_client.create_socket()
    tcp_client.interact_with_server()

if __name__ == '__main__':
    main()