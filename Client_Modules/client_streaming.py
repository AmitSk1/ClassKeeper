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
    def __init__(self, resolution=(RESOLUTION_VERTICAL, RESOLUTION_HORIZONTAL)):
        self.resolution = resolution
        self.camera = cv2.VideoCapture(CAPTURE_DEVICE_INDEX)

    def grab_screen_frame(self):
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)
        screen_np = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
        return cv2.resize(screen_np, self.resolution)

    def grab_camera_frame(self):
        ret, cam_frame = self.camera.read()
        if not ret:
            print("Failed to grab frame from camera. Exiting...")
            return None
        return cv2.resize(cam_frame, self.resolution)

    def merge_video_frames(self, screen_np, cam_frame):
        return np.hstack((cam_frame, screen_np))