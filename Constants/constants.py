"""
Constants
Amit Skarbin
"""
import cv2
CHUNK_SIZE = 4096  # bytes

# Constants for the client
FPS = 10
RESOLUTION_VERTICAL = 320
RESOLUTION_HORIZONTAL = 240
CAPTURE_DEVICE_INDEX = 0  # Index of the camera capture device
JPEG_COMPRESSION_QUALITY = 50  # Compression quality for JPEG images
PICKLE_PROTOCOL_VERSION = 4  # Protocol version for pickle
# Time to wait between frames, calculated from FPS
WAIT_TIME_PER_FRAME = int(1000 / FPS)

# Constants for the server
FRAME_DECODE_COLOR_MODE = cv2.IMREAD_COLOR  # Color mode for frame decoding
