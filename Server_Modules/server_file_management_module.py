"""
Server for file management
Amit Skarbin
"""

import os

from Protocols.file_protocol import FileProtocol
from Protocols.protocol import Protocol



class ServerFileManagementModule:
    """
    Manages file operations for the server.

    This module handles tasks related to file storage and retrieval, including
    storing files received from clients and sending files to clients.

    Attributes:
        last_uploaded_file (str): The path of the last file uploaded
        by a client.
    """

    def __init__(self):
        """
        Initializes the ServerFileManagementModule.
        """
        self.last_uploaded_file = None

    def store_client_file(self, client_socket):
        """
        Stores a file received from a client.

        Args:
            client_socket (socket.socket): The client socket from which to
            receive the file.
        """
        directory = "C:/client_files"
        if not os.path.exists(directory):
            os.makedirs(directory)
        FileProtocol.recv_file(client_socket, directory)
        print("File stored successfully in " + directory)

    def send_stored_file(self, client_socket):
        """
        Sends the last uploaded file to a client.

        Args:
            client_socket (socket.socket): The client socket to which to send
            the file.
        """
        if self.last_uploaded_file:
            Protocol.send(client_socket, "FILE")
            FileProtocol.send_file(client_socket, self.last_uploaded_file)
        else:
            Protocol.send(client_socket, "NO_FILE")
            print("No file has been uploaded yet.")

    def upload_file(self, file_path):
        """
        Updates the path of the last uploaded file.

        Args:
            file_path (str): The path of the file to be considered as the last
            uploaded.
        """

        self.last_uploaded_file = file_path
        print("Uploading file " + file_path)
