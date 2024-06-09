# Client
import pickle
import sys
import threading
import cv2
from Client_Modules.client_network_module import ClientNetworkModule
from Client_Modules.client_streaming import ClientStreamingModule
from Client_Modules.client_file_management_module import ClientFileManagementModule
from Constants.constants import JPEG_COMPRESSION_QUALITY, PICKLE_PROTOCOL_VERSION
from Protocols.protocol import Protocol

class Client:
    def __init__(self, host, port):
        self.network_module = ClientNetworkModule(host, port)
        self.streaming_module = ClientStreamingModule()
        self.file_management_module = ClientFileManagementModule(self.network_module.file_socket)
        self.username = None
        self.test_over = False
        self.stream_thread = None
        self.listen_thread = None
        self.running = False

    def begin_video_stream(self, username):
        self.username = username
        self.running = True
        self.network_module.establish_server_connection()
        self.stream_thread = threading.Thread(target=self.transmit_video, daemon=True)
        self.stream_thread.start()
        self.listen_thread = threading.Thread(target=self.await_server_messages)
        self.listen_thread.start()

    def await_server_messages(self):
        try:
            while self.running:
                message = Protocol.receive_data(self.network_module.listen_socket)
                if message == "TEST_OVER":
                    self.test_over = True
                    print("Received TEST_OVER from server, stopping client.")
        except Exception as e:
            print(f"listen to server have an error: {e}")

    def halt_video_stream(self):
        self.streaming_module.camera.release()
        self.network_module.disconnect_all_sockets()
        print("Streaming stopped")

    def transmit_video(self):
        while self.running:
            screen_np = self.streaming_module.grab_screen_frame()
            cam_frame = self.streaming_module.grab_camera_frame()
            if cam_frame is None:
                break
            combined_frame = self.streaming_module.merge_video_frames(screen_np, cam_frame)
            if not self.dispatch_video_frame(combined_frame):
                break
        self.halt_video_stream()

    def dispatch_video_frame(self, frame):
        Protocol.transmit_data(self.network_module.stream_socket, "STREAM")
        result, encoded_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_COMPRESSION_QUALITY])
        if not result:
            return False
        frame_and_username = (encoded_frame, self.username)
        data = pickle.dumps(frame_and_username, protocol=PICKLE_PROTOCOL_VERSION)
        try:
            Protocol.transmit_binary(self.network_module.stream_socket, data)
            return True
        except Exception as e:
            print(f"Connection closed: {e}")
            return False

    def terminate_client(self):
        self.running = False
        Protocol.transmit_data(self.network_module.stream_socket, "STOP")
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join()
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join()
        self.halt_video_stream()
        sys.exit()
        print("Client has been stopped.")