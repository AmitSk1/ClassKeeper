"""
Server for network communication
Amit Skarbin
"""

import socket
import threading
from Protocols.protocol import Protocol


class ServerNetworkModule:
    def __init__(self, host, port, client_handler_callback):
        self.host = host
        self.port = port
        self.client_handler_callback = client_handler_callback
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = {}
        self.running = False

    def alert_clients_test_ended(self):
        for client_address, client_socket in self.clients.items():
            try:
                Protocol.transmit_data(client_socket, "TEST_OVER")
            except Exception as e:
                print(f"Error notifying client at {client_address}: {e}")

    def launch_server(self):
        self.server_socket.listen()
        self.running = True
        print(f"Server started on {self.host}:{self.port}")
        accept_thread = threading.Thread(target=self.handle_incoming_connections)
        accept_thread.start()

    def handle_incoming_connections(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Client connected from {client_address}")
                self.clients[client_address] = client_socket
                client_thread = threading.Thread(target=self.client_handler_callback, args=(client_socket, client_address))
                client_thread.start()
            except Exception as e:
                print(f"Error accepting new connection: {e}")
                if not self.running:
                    break

    def terminate_server(self):
        self.running = False
        self.alert_clients_test_ended()
        for client_address, client_socket in self.clients.items():
            client_socket.close()
        self.server_socket.close()
        print("Server stopped")

    def expel_client(self, client_address):
        if client_address in self.clients:
            del self.clients[client_address]
            print(f"Client {client_address} removed")