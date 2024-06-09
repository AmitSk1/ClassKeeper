"""
Server for file management
Amit Skarbin
"""

import os

from Protocols.file_protocol import FileProtocol
from Protocols.protocol import Protocol



class ServerFileManagementModule:
    def __init__(self):
        self.last_uploaded_file = None

    def archive_client_file(self, client_socket):
        directory = "C:/client_files"
        if not os.path.exists(directory):
            os.makedirs(directory)
        FileProtocol.download_file(client_socket, directory)
        print("File stored successfully in " + directory)

    def deliver_archived_file(self, client_socket):
        if self.last_uploaded_file:
            Protocol.transmit_data(client_socket, "FILE")
            FileProtocol.dispatch_file(client_socket, self.last_uploaded_file)
        else:
            Protocol.transmit_data(client_socket, "NO_FILE")
            print("No file has been uploaded yet.")

    def register_uploaded_file(self, file_path):
        self.last_uploaded_file = file_path
        print("Uploading file " + file_path)