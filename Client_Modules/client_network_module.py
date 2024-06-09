"""
client for network
Amit Skarbin
"""

import socket


class ClientNetworkModule:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def establish_server_connection(self):
        self.file_socket.connect((self.host, self.port))
        self.stream_socket.connect((self.host, self.port))
        self.listen_socket.connect((self.host, self.port))
        print("Client connection established.")

    def disconnect_all_sockets(self):
        self.stream_socket.close()
        self.file_socket.close()
        self.listen_socket.close()
        print("closed all sockets.")