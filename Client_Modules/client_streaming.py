"""
client for streaming
Amit Skarbin
"""

import cv2
import numpy as np
import pyautogui
from Constants.constants import RESOLUTION_VERTICAL, RESOLUTION_HORIZONTAL, \
    CAPTURE_DEVICE_INDEX


class ClientStreamingModule:
    """
    Manages the streaming of video data for the client.
    This module handles the capture of screen and camera frames and combines
    them for streaming.

    Attributes:
        resolution (tuple): The resolution for capturing video frames.
        camera (cv2.VideoCapture): The camera device for capturing video frames
    """

    def __init__(self,
                 resolution=(RESOLUTION_VERTICAL, RESOLUTION_HORIZONTAL)):
        """
        Initializes the ClientStreamingModule with a specified resolution.

        Args:
            resolution (tuple): The resolution to be used for video capture.
        """
        self.resolution = resolution
        self.camera = cv2.VideoCapture(CAPTURE_DEVICE_INDEX)

    def capture_screen(self):
        """
        Captures the current screen.

        Returns:
            numpy.ndarray: An array representing the captured screen frame.
        """
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)
        screen_np = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
        return cv2.resize(screen_np, self.resolution)

    def capture_camera_frame(self):
        """
        Captures a frame from the camera.

        Returns:
            numpy.ndarray: An array representing the captured camera frame.
            None if the frame capture fails.
        """
        ret, cam_frame = self.camera.read()
        if not ret:
            print("Failed to grab frame from camera. Exiting...")
            return None
        return cv2.resize(cam_frame, self.resolution)

    def combine_frames(self, screen_np, cam_frame):
        """
        Combines the screen and camera frames horizontally.

        Args:
            screen_np (numpy.ndarray): The captured screen frame.
            cam_frame (numpy.ndarray): The captured camera frame.

        Returns:
            numpy.ndarray: An array representing the combined frame.
        """
        return np.hstack((cam_frame, screen_np))
