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
    def __init__(self, host, port, new_frame_callback=None):
        self.network_module = ServerNetworkModule(host, port, self.manage_client_connection)
        self.file_management_module = ServerFileManagementModule()
        self.frame_processing_module = ServerFrameProcessingModule(new_frame_callback)

    def initiate_server(self):
        self.network_module.launch_server()

    def shutdown_server(self):
        self.network_module.terminate_server()

    def manage_client_connection(self, client_socket, client_address):
        while self.network_module.running:
            try:
                data = Protocol.receive_data(client_socket)
                if data == "REQUEST_LAST_FILE":
                    self.file_management_module.deliver_archived_file(client_socket)
                elif data == "STREAM":
                    self.process_client_communication(client_socket, client_address)
                elif data == "UPLOAD_FILE":
                    self.file_management_module.archive_client_file(client_socket)
                elif data == "STOP":
                    self.manage_client_disconnection(client_socket, client_address)
            except ConnectionError as e:
                self.manage_client_disconnection(client_socket, client_address, e)
                break
            except Exception as e:
                self.record_error(client_address, e)
                break
        self.cleanup_client_connection(client_socket, client_address)

    def process_client_communication(self, client_socket, client_address):
        data = Protocol.receive_binary(client_socket)
        self.frame_processing_module.handle_incoming_frame(data, client_address)

    def manage_client_disconnection(self, client_socket, client_address, error=None):
        del self.network_module.clients[client_address]
        print(f"Client {client_address} disconnected: {error}")
        self.cleanup_client_connection(client_socket, client_address)

    def record_error(self, client_address, error):
        print(f"Error handling client {client_address}: {error}")
        if self.frame_processing_module.new_frame_callback is not None:
            self.frame_processing_module.new_frame_callback(client_address, None, None)

    def cleanup_client_connection(self, client_socket, client_address):
        client_socket.close()
        if self.frame_processing_module.new_frame_callback is not None:
            self.frame_processing_module.new_frame_callback(client_address, None, None)