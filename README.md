# mjpeg_py Camera Frame Capture

This Python script captures frames from an MJPEG stream from an IP camera and saves them as JPEG images. The frames are organized in folders by date and named with timestamps.

## Features

- Captures frames from MJPEG stream
- Organizes saved frames by date in separate folders
- Names files with timestamps and frame count
- Handles authentication for camera access
- Creates new folders automatically for different dates
- Live preview of captured frames

## Requirements

- Python 3.x
- OpenCV
- Requests
- NumPy

## Installation

1. Clone this repository:
2. Install required packages:
bash pip install -r requirements.txt

## Usage

1. Run the script:
bash python mjpeg_py.py

## Troubleshooting

- If the script can't connect to the camera, verify your credentials in the `.env` file
- Check if the camera IP and port are correct
- Ensure your camera supports MJPEG streaming
- Verify network connectivity to the camera

## Notes

- Frames are saved every second
- Each minute gets a new frame count starting from 0
- The script creates new directories automatically

2. The script will:
   - Create an 'output_frames' directory
   - Create subdirectories for each date (YYYYMMDD)
   - Save frames as JPG files with timestamp names
   - Show live preview window
   - Press 'q' to quit

## Output Structure

output_frames/ ├── 20231101/ │
├── frame_20231101_143022_0.jpg │
├── frame_20231101_143022_1.jpg │ └── ... └──
20231102/ ├── frame_20231102_143022_0.jpg
└── ...