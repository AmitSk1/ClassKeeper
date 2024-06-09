"""
Server for frame processing
Amit Skarbin
"""

import pickle
import cv2
from Constants.constants import FRAME_DECODE_COLOR_MODE


class ServerFrameProcessingModule:
    def __init__(self, new_frame_callback=None):
        self.new_frame_callback = new_frame_callback

    def handle_incoming_frame(self, data, client_address):
        try:
            frame_data, username = pickle.loads(data)
            frame = cv2.imdecode(frame_data, FRAME_DECODE_COLOR_MODE)
            if frame is not None and self.new_frame_callback is not None:
                self.new_frame_callback(client_address, frame, username)
        except Exception as e:
            print(f"Error decoding frame from client {client_address}: {e}")