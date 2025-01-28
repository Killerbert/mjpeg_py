import cv2
import requests
import numpy as np
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv


def load_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as f:
        for line in f:
            # Ignore empty lines or lines that start with a comment
            if not line.strip() or line.startswith("#"):
                continue
            # Split key and value by '=' and strip any surrounding whitespace
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

# Example usage with '.env' file
credentials = load_credentials('.env')
username = credentials.get('USERNAME')
password = credentials.get('PASSWORD')
rtsp_url = credentials.get('rtsp_url')

print(f"Username: {username}")
print(f"Password: {password}")
print(f"rtsp_url: {rtsp_url}")

# Now you can use `username` and `password` securely in your code


# rtsp://jetson:HiJetson@10.20.201.51/axis-media/media.amp

print("Hello, World!")

# RTSP stream URL for AXIS camera (replace <camera_ip> with your camera's IP)
# rtsp://[username]:[password]@[IP_address]:[port]/axis-media/media.amp
# NOTE: RTSP URL (typically H.264):
# TODO: fix this issue
# rtsp_url = REMOVED username password

# Open the RTSP stream using OpenCV
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Unable to connect to the RTSP stream.")
else:
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        # Save the frame as a JPEG file
        frame_filename = f"frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")

        frame_count += 1

        # Optional: Display the frame
        cv2.imshow('RTSP Stream', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()