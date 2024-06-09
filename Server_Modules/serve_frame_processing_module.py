"""
Server for frame processing
Amit Skarbin
"""

import pickle
import cv2
from Constants.constants import FRAME_DECODE_COLOR_MODE


class ServerFrameProcessingModule:
    """
    Manages the processing of video frames received from clients.

    This module is responsible for decoding video frames sent by clients and
    invoking a callback function for further processing.

    Attributes:
        new_frame_callback (function): A callback function that is called when
        a new frame is received.
    """

    def __init__(self, new_frame_callback=None):
        """
        Initializes the ServerFrameProcessingModule with an optional callback
        function.

        Args:
            new_frame_callback (function): Optional. A function to be called
            when a new frame is received.
        """
        self.new_frame_callback = new_frame_callback

    def process_received_frame(self, data, client_address):
        """
        Processes a received video frame.

        Args:
            data (bytes): The data containing the encoded video frame.
            client_address (tuple): The address of the client that
             sent the frame.
        """
        try:
            frame_data, username = pickle.loads(data)
            frame = cv2.imdecode(frame_data, FRAME_DECODE_COLOR_MODE)
            if frame is not None and self.new_frame_callback is not None:
                self.new_frame_callback(client_address, frame, username)
        except Exception as e:
            print(f"Error decoding frame from client {client_address}: {e}")
