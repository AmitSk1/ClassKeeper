"""
Server for network communication
Amit Skarbin
"""

import socket
import threading
from Protocols.protocol import Protocol


class ServerNetworkModule:
    def __init__(self, host, port, client_handler_callback):
        """
        Initializes the network module with server host and port.

        Args:
            host (str): The IP address or hostname of the server.
            port (int): The port number on which the server listens.
            client_handler_callback (function): A callback function that will
            be called to handle client communication.
        """
        self.host = host
        self.port = port
        self.client_handler_callback = client_handler_callback
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = {}  # Dictionary to store connected clients
        self.running = False

    def notify_clients_test_over(self):
        """
        Notify all connected clients that the test is over.
        """
        for client_address, client_socket in self.clients.items():
            try:
                Protocol.send(client_socket, "TEST_OVER")
            except Exception as e:
                print(f"Error notifying client at {client_address}: {e}")

    def notify_clients_test_file_upload(self):
        """
        Notify all connected clients that the test is over.
        """
        for client_address, client_socket in self.clients.items():
            try:
                Protocol.send(client_socket, "UPLOAD_FILE")
            except Exception as e:
                print(f"Error notifying client at {client_address}: {e}")

    def start_server(self):
        """
        Starts the server to listen for incoming connections and handle them.
        """
        self.server_socket.listen()
        self.running = True
        print(f"Server started on {self.host}:{self.port}")
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.start()

    def accept_connections(self):
        """
        Accepts incoming connections and starts a new thread for each client.
        """
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()

                print(f"Client connected from {client_address}")
                # Add client to the dictionary
                self.clients[client_address] = client_socket
                # Start a new thread to handle communication with this client
                client_thread = threading. \
                    Thread(target=self.
                           client_handler_callback,
                           args=(client_socket, client_address))
                client_thread.start()
            except Exception as e:
                print(f"Error accepting new connection: {e}")
                if not self.running:
                    break  # Exit the loop if the server is stopped

    def stop_server(self):
        """
        Stops the server and closes all resources.
        """
        self.running = False
        self.notify_clients_test_over()
        for client_address, client_socket in self.clients.items():
            client_socket.close()
        self.server_socket.close()
        print("Server stopped")

    def remove_client(self, client_address):
        """
        Removes a client from the connected clients dictionary.

        Args:
            client_address (tuple): The address of the client to remove.
        """
        if client_address in self.clients:
            del self.clients[client_address]
            print(f"Client {client_address} removed")
