"""
Server
Amit Skarbin
"""

import socket
from Protocols.protocol import Protocol
from Server_Modules.server_network_module import ServerNetworkModule
from Server_Modules.server_file_management_module \
    import ServerFileManagementModule
from Server_Modules.serve_frame_processing_module \
    import ServerFrameProcessingModule


class Server:
    """
    A server class for handling video streaming from multiple clients.

    This class manages the server operations including network communication,
    file management, and frame processing.

    Attributes:
        network_module (ServerNetworkModule): Manages network communication.
        file_management_module (ServerFileManagementModule):
        Handles file operations.
        frame_processing_module (ServerFrameProcessingModule):
        Manages frame processing.
    """

    def __init__(self, host, port, new_frame_callback=None):
        """
        Initializes the Server with host, port, and frame callback.

        Args:
            host (str): Host address of the server.
            port (int): Port number the server listens on.
            new_frame_callback (function): Callback function for new frames.
        """
        self.network_module = ServerNetworkModule(host,
                                                  port, self.client_handler)
        self.file_management_module = ServerFileManagementModule()
        self.frame_processing_module = ServerFrameProcessingModule(
            new_frame_callback)

    def start_server(self):
        """
        Starts the server to listen for incoming connections.
        """
        self.network_module.start_server()

    def stop_server(self):
        """
        Stops the server and closes all resources.
        """
        self.network_module.stop_server()

    def client_handler(self, client_socket, client_address):
        """
        Handles communication with a connected client.

        Args:
            client_socket (socket.socket): Socket for the client connection.
            client_address (tuple): Address of the client.
        """
        while self.network_module.running:
            try:
                data = Protocol.recv(client_socket)
                if data == "REQUEST_LAST_FILE":  # if client request file
                    self.file_management_module.send_stored_file(client_socket)
                elif data == "STREAM":  # client start stream
                    self.handle_client_communication(client_socket,
                                                     client_address)
                elif data == "UPLOAD_FILE":  # server upload file
                    self.file_management_module. \
                        store_client_file(client_socket)
                elif data == "STOP":  # client finish test or teacher stop test
                    self.handle_disconnection(client_socket, client_address)
            except ConnectionError as e:
                self.handle_disconnection(client_socket, client_address, e)
                break
            except Exception as e:
                self.log_error(client_address, e)
                break
        self.cleanup_connection(client_socket, client_address)

    def handle_client_communication(self, client_socket, client_address):
        """
            Processes data received from a client.
            Args:
                client_socket (socket.socket): The client's socket.
                client_address (tuple): The client's address.
            """
        data = Protocol.recv_bin(client_socket)
        self.frame_processing_module. \
            process_received_frame(data, client_address)

    def diconnection(self, client_socket, client_address):
        """
            Handles the immediate disconnection logic for a client.
            Removes the client from the active clients' dictionary,
            Args:
                client_socket (socket.socket): The client's socket.
                client_address (tuple): The client's address.
        """
        # Remove client from the dictionary when disconnected
        del self.network_module.clients[client_address]
        print(f"Client {client_address} disconnecte")
        if self.frame_processing_module.new_frame_callback is not None:
            self.frame_processing_module \
                .new_frame_callback(client_address, None, None)
        client_socket.close()

    def handle_disconnection(self, client_socket, client_address, error=None):
        """
        Cleans up after a client disconnect.
        Removes the client from the server's active client dictionary,
        and performs cleanup.

        Args:
            client_socket (socket.socket): The client's socket.
            client_address (tuple): The client's address.
            error (str, optional): Description of the error leading to
            disconnection, if any.
        """
        # Remove client from the dictionary when disconnected
        del self.network_module.clients[client_address]
        print(f"Client {client_address} disconnected: {error}")
        self.cleanup_connection(client_socket, client_address)

    def log_error(self, client_address, error):
        """
           Logs an error related to a client.
           Args:
               client_address (tuple): The address of the client
               that encountered an error.
               error (str): The error message.
        """
        print(f"Error handling client {client_address}: {error}")
        if self.frame_processing_module.new_frame_callback is not None:
            self.frame_processing_module \
                .new_frame_callback(client_address, None, None)

    def cleanup_connection(self, client_socket, client_address):
        """
        Performs cleanup tasks for a disconnected client's socket.

        Closes the client's socket and, if a new frame callback is set,
        notifies the frame
        processing module about the disconnection.

        Args:
            client_socket (socket.socket): The client's socket.
            client_address (tuple): The client's address.
        """
        client_socket.close()
        if self.frame_processing_module.new_frame_callback is not None:
            self.frame_processing_module \
                .new_frame_callback(client_address, None, None)
