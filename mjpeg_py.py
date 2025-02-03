import cv2
import os
import requests
import numpy as np
from requests.auth import HTTPBasicAuth
#from dotenv import load_dotenv
from datetime import datetime

def create_folder_if_not_exists(folder_path):
    """Create folder if it doesn't exist"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_current_timestamps():
    """Get all current timestamp formats"""
    # Get current date and time once for efficiency
    now = datetime.now()
    return {
        'time': now.strftime("%Y%m%d_%H%M%S"),
        'date': now.strftime("%Y%m%d"),
        'minute': now.strftime("%Y%m%d_%H%M")
    }

def check_new_period(current_date, current_minute, last_date, last_minute):
    """Check if we've entered a new time period"""
    # TODO: determine if this function is needed.
    return current_date != last_date or current_minute != last_minute

def update_datetime_info(output_dir, last_date, last_minute, frame_count):
    """Manage all datetime related operations"""
    # Get current timestamps
    timestamps = get_current_timestamps()

    # Create day folder path
    day_folder = os.path.join(output_dir, timestamps['date'])

    # Check if we're in a new period
    #if check_new_period(timestamps['date'], timestamps['minute'], last_date, last_minute):
    if timestamps['date'] != last_date or timestamps['minute'] != last_minute:
        frame_count = 0
        create_folder_if_not_exists(day_folder)
        last_date = timestamps['date']
        last_minute = timestamps['minute']

    return {
        'current_time': timestamps['time'],
        'current_date': timestamps['date'],
        'current_minute': timestamps['minute'],
        'day_folder': day_folder,
        'frame_count': frame_count,
        'last_date': last_date,
        'last_minute': last_minute
    }

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

            datetime_info = update_datetime_info(output_dir, last_date, last_minute, frame_count)
            current_time = datetime_info['current_time']
            current_date = datetime_info['current_date']
            current_minute = datetime_info['current_minute']
            day_folder = datetime_info['day_folder']
            frame_count = datetime_info['frame_count']
            last_date = datetime_info['last_date']
            last_minute = datetime_info['last_minute']

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