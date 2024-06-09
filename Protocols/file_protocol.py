"""
Amit skarbin
"""

import os
from Constants.constants import CHUNK_SIZE
from Protocols.protocol import Protocol


class FileProtocol:
    @staticmethod
    def dispatch_file(sock, file_path):
        file_name = os.path.basename(file_path)
        file_name_encoded = file_name.encode()
        Protocol.transmit_binary(sock, file_name_encoded)
        with open(file_path, 'rb') as file:
            while True:
                file_data = file.read(CHUNK_SIZE)
                if not file_data:
                    break
                Protocol.transmit_binary(sock, file_data)
        Protocol.transmit_binary(sock, b'')

    @staticmethod
    def download_file(sock, directory):
        file_name_encoded = Protocol.receive_binary(sock)
        file_name = file_name_encoded.decode()
        os.makedirs(directory, exist_ok=True)
        save_path = os.path.join(directory, file_name)
        with open(save_path, 'wb') as file:
            while True:
                file_data = Protocol.receive_binary(sock)
                if not file_data:
                    break
                file.write(file_data)
