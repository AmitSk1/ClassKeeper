"""
client for file management
Amit Skarbin
"""

import os
from Protocols.protocol import Protocol
from Protocols.file_protocol import FileProtocol


class ClientFileManagementModule:
    """
    Manages file operations for the streaming client.

    This module handles file-related tasks such as uploading files to the
    server requesting and receiving files from the server.

    Attributes:
        file_socket (socket.socket): Socket used for file-related communication
    """

    def __init__(self, file_socket):
        """
        Initializes the ClientFileManagementModule with a file socket.

        Args:
            file_socket (socket.socket): The socket used for file operations.
        """
        self.file_socket = file_socket

    def request_last_file(self):
        """
        Requests the last uploaded file from the server.
        """
        try:
            Protocol.send(self.file_socket, "REQUEST_LAST_FILE")
        except Exception as e:
            print(f"Error requesting file: {e}")

    def check_if_file_upload(self):
        response = Protocol.recv(self.file_socket)
        if response == "NO_FILE":
            print("no file available for download")
            return False
        else:
            return True

    def receive_file_from_server(self, directory):
        """
        Receives a file from the server and saves it to the specified directory

        Args:
            directory (str): The directory where the file will be saved.
        """
        FileProtocol.recv_file(self.file_socket, directory)
        print(f"File received and saved to {directory}")

    def upload_file(self, file_path, username):
        """
        Uploads a selected file to the server.

        Args:
            file_path (str): The path of the file to upload.
            username (str): The username of the client uploading the file.
        """
        try:
            directory, base_name = os.path.split(file_path)
            new_file_name = os.path.join(directory, username + "_" + base_name)
            os.rename(file_path, new_file_name)
            Protocol.send(self.file_socket, "UPLOAD_FILE")
            FileProtocol.send_file(self.file_socket, new_file_name)
        except Exception as e:
            print(f"Error uploading file: {e}")
