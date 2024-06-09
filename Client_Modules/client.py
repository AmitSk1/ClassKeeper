"""
Client
Amit Skarbin
"""


import pickle
import sys
import threading
import cv2
from Client_Modules.client_network_module import ClientNetworkModule
from Client_Modules.client_streaming import ClientStreamingModule
from Client_Modules.client_file_management_module \
    import ClientFileManagementModule
from Constants.constants import JPEG_COMPRESSION_QUALITY, PICKLE_PROTOCOL_VERSION
from Protocols.protocol import Protocol

class Client:
    """
    A class representing a streaming client that sends video data to a server.

    Attributes:
        network_module (ClientNetworkModule): Manages network communication.
        streaming_module (ClientStreamingModule): Handles video streaming.
        file_management_module (ClientFileManagementModule): Manages file
        operations.

        username (str): The username of the client.
        running (bool): Indicates whether the streaming is active.
    """

    def __init__(self, host, port):
        """
        Initializes the streaming client with the specified server address.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The port number on which the server is listening.
        """
        self.network_module = ClientNetworkModule(host, port)
        self.streaming_module = ClientStreamingModule()
        self.file_management_module = ClientFileManagementModule(
            self.network_module.file_socket)
        self.username = None
        self.test_over = False
        self.upload_file = False
        self.stream_thread = None
        self.listen_thread = None
        self.running = False

    def start_stream(self, username):
        """
        Starts the video streaming process.

        Args:
            username (str): The username to be associated with the streamed
            video.
        """
        self.username = username
        self.running = True
        self.network_module.connect_to_server()
        self.stream_thread = threading.Thread(target=self.stream_video,
                                              daemon=True)
        self.stream_thread.start()
        # Start the listening thread
        self.listen_thread = threading.Thread(target=self.listen_to_server)
        self.listen_thread.start()

    def listen_to_server(self):
        """
        Listens for server messages, specifically for the "TEST_OVER" signal.
        If "TEST_OVER" message is received, it indicates
        the server has ended the test, and sets
        `test_over` flag to True. s
        Raises:
            Exception: Logs any network communication errors encountered.
        """
        try:
            while self.running:
                message = Protocol.recv(self.network_module.listen_socket)
                if message == "TEST_OVER":
                    self.test_over = True
                    print("Received TEST_OVER from server, stopping client.")
                if message == "UPLOAD_FILE":
                    self.upload_file = True
                    print("received upload_file from server")
        except Exception as e:
            print(f"listen to server have an error: {e}")

    def stop_stream(self):
        """
        Stops the video streaming process and releases resources.
        """
        self.streaming_module.camera.release()
        self.network_module.close_sockets()

        print("Streaming stopped")

    def stream_video(self):
        """
        Continuously captures and sends video frames to the server.
        """
        while self.running:
            screen_np = self.streaming_module.capture_screen()
            cam_frame = self.streaming_module.capture_camera_frame()
            if cam_frame is None:
                break

            combined_frame = self.streaming_module.combine_frames(screen_np,
                                                                  cam_frame)
            if not self.send_frame(combined_frame):
                break

        self.stop_stream()

    def send_frame(self, frame):
        """
        Encodes and sends a video frame to the server.

        Args:
            frame (numpy.ndarray): The video frame to send.

        Returns:
            bool: True if the frame was sent successfully, False otherwise.
        """

        Protocol.send(self.network_module.stream_socket, "STREAM")
        result, encoded_frame = cv2. \
            imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY,
                                     JPEG_COMPRESSION_QUALITY])
        if not result:
            return False

        frame_and_username = (encoded_frame, self.username)
        data = pickle.dumps(frame_and_username,
                            protocol=PICKLE_PROTOCOL_VERSION)
        try:
            Protocol.send_bin(self.network_module.stream_socket, data)
            return True
        except Exception as e:
            print(f"Connection closed: {e}")
            return False

    def stop_client(self):
        """
        Signals the client to stop streaming and shuts down the connection.
        """

        # Ensure the running flag is False to stop threads
        self.running = False
        Protocol.send(self.network_module.stream_socket, "STOP")
        # Wait for the streaming and listening threads to finish
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join()
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join()

        self.stop_stream()
        sys.exit()  # Exit the program
        print("Client has been stopped.")
