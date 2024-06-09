"""
Amit skarbin
"""

import os
import struct
from Constants.constants import CHUNK_SIZE
from Protocols.protocol import Protocol


class FileProtocol:

    @staticmethod
    def send_file(sock, file_path):
        """
        Sends a file over a socket using only methods from the Protocol class.

        Args:
            sock (socket.socket): The socket over which to send the file.
            file_path (str): The path of the file to send.
        """
        file_name = os.path.basename(file_path)
        file_name_encoded = file_name.encode()

        # Send the file name using Protocol.send_bin
        Protocol.send_bin(sock, file_name_encoded)

        # Send the file content
        with open(file_path, 'rb') as file:
            file_data = file.read()
            Protocol.send_bin(sock, file_data)

    @staticmethod
    def recv_file(sock, directory):
        """
        Receives a file over a socket and saves it to the specified directory
        using only methods from the Protocol class.

        Args:
            sock (socket.socket): The socket from which to receive the file.
            directory (str): The directory where the file will be saved.
        """
        # Receive the file name using Protocol.recv_bin
        file_name_encoded = Protocol.recv_bin(sock)
        file_name = file_name_encoded.decode()

        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        save_path = os.path.join(directory, file_name)

        # Receive the file data using Protocol.recv_bin
        file_data = Protocol.recv_bin(sock)

        with open(save_path, 'wb') as file:
            file.write(file_data)