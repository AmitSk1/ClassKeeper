"""
client for file management
Amit Skarbin
"""
import os
from Protocols.protocol import Protocol
from Protocols.file_protocol import FileProtocol

class ClientFileManagementModule:
    def __init__(self, file_socket):
        self.file_socket = file_socket

    def fetch_latest_file(self):
        try:
            Protocol.transmit_data(self.file_socket, "REQUEST_LAST_FILE")
        except Exception as e:
            print(f"Error requesting file: {e}")

    def verify_file_upload(self):
        response = Protocol.receive_data(self.file_socket)
        if response == "NO_FILE":
            print("no file available for download")
            return False
        else:
            return True

    def download_file_from_server(self, directory):
        FileProtocol.download_file(self.file_socket, directory)
        print(f"File received and saved to {directory}")

    def transmit_file_to_server(self, file_path, username):
        try:
            directory, base_name = os.path.split(file_path)
            new_file_name = os.path.join(directory, username + "_" + base_name)
            os.rename(file_path, new_file_name)
            Protocol.transmit_data(self.file_socket, "UPLOAD_FILE")
            FileProtocol.dispatch_file(self.file_socket, new_file_name)
        except Exception as e:
            print(f"Error uploading file: {e}")