"""
client for network
Amit Skarbin
"""

import socket


class ClientNetworkModule:
    """
    Manages network communication for the streaming client.

    This module is responsible for handling socket connections used for
    streaming video data and file operations with the server.

    Attributes:
        host (str): Hostname or IP address of the server.
        port (int): Port number on which the server is listening.
        stream_socket (socket.socket): Socket used for streaming video data.
        file_socket (socket.socket): Socket used for file operations.
    """

    def __init__(self, host, port):
        """
        Initializes the ClientNetworkModule with server host and port.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The port number on which the server is listening.
        """
        self.host = host
        self.port = port
        self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        """
        Establishes the socket connection with the server.
        """
        self.file_socket.connect((self.host, self.port))
        self.stream_socket.connect((self.host, self.port))
        self.listen_socket.connect((self.host, self.port))
        print("Client connection established.")

    def close_sockets(self):
        """
        Closes the streaming and file sockets.
        """
        self.stream_socket.close()
        self.file_socket.close()
        self.listen_socket.close()
        print("closed all sockets .")
