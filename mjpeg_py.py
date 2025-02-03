import cv2
import os
import requests
import numpy as np
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from datetime import datetime


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

# Usage with '.env' file
credentials = load_credentials('.env')
username = credentials.get('USERNAME')
password = credentials.get('PASSWORD')
camera_ip = credentials.get('CAMERA_IP')

# Define the output directory where the frames will be saved
output_dir = "output_frames"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create a day folder inside output_dir using current date
current_date = datetime.now().strftime("%Y%m%d")
day_folder = os.path.join(output_dir, current_date)
if not os.path.exists(day_folder):
    os.makedirs(day_folder)

print(f"\n")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"camera_ip: {camera_ip}")

# Replace with your camera's MJPEG URL
mjpeg_url = f"http://{username}:{password}@{camera_ip}/axis-cgi/mjpg/video.cgi"
# Open the MJPEG stream using OpenCV
cap = cv2.VideoCapture(mjpeg_url)

if not cap.isOpened():
    print("Error: Unable to connect to the MJPEG stream.")
else:
    frame_count = 0
    last_date = datetime.now().strftime("%Y%m%d")  # Store the current date initially
    last_minute = datetime.now().strftime("%Y%m%d_%H%M")  # Store the current date and minute

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame. Retrying...")
                continue

            # Get current date and time once for efficiency
            # Get current timestamp once and format it for different uses
            # This is more efficient than calling datetime.now() multiple times
            now = datetime.now()
            current_time = now.strftime("%Y%m%d_%H%M%S")  # Full timestamp for filenames
            current_date = now.strftime("%Y%m%d")  # Date only for daily organization
            current_minute = now.strftime("%Y%m%d_%H%M")

            # Reset frame_count and update tracking variables when we enter a new minute or day
            # This helps organize files by resetting the counter each minute
            if current_date != last_date or current_minute != last_minute:
                frame_count = 0
                last_date = current_date  # Update last_date to the new date
                last_minute = current_minute  # Update last_minute to the new minute

                # Create new day folder if date changes
                day_folder = os.path.join(output_dir, current_date)
                if not os.path.exists(day_folder):
                    os.makedirs(day_folder)

            # Create the filename with date, time, and frame count
            frame_filename = os.path.join(day_folder, f"frame_{current_time}_{frame_count}.jpg")

            # Save the frame as a JPEG file in the output directory
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")

            frame_count += 1

            # Optional: Display the frame
            cv2.imshow("MJPEG Stream", frame)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
    finally:
        cap.release()
    cv2.destroyAllWindows()