Pothole detection in images using YOLOV8
The dataset was taken from kaggle, here is the url :: https://www.kaggle.com/datasets/farzadnekouei/pothole-image-segmentation-dataset


## Features
Image upload with segmentation-based road damage detection.
Video upload with frame-by-frame inference and smoothed damage percentage.
Outputs are saved automatically to the static/predictions directory.
Processed videos are converted to MP4 using FFmpeg for reliable playback.
Simple HTML/CSS/JavaScript frontend and Flask backend.


## Tech Stack
YOLOv8 (Ultralytics)
Flask
OpenCV
FFmpeg
HTML, CSS, JavaScript


## Project Structure
static/
    uploads/        # user-uploaded files
    predictions/    # generated result images and videos
templates/
    index.html
app.py
predict.py
requirements.txt
best.pt


## Running the Application ##

## Install dependencies:
pip install -r requirements.txt
Start the server:
python app.py
Open the application in a browser:
http://127.0.0.1:5000

## Model
Place your YOLOv8 model file (best.pt) in the project directory.
If the model path differs, update it in predict.py.

## Output
Image input: returns the original image alongside the predicted segmentation image.
Video input: returns an MP4 video containing processed frames with the road damage percentage overlaid.

Image input: returns the original image alongside the predicted segmentation image.

Video input: returns an MP4 video containing processed frames with the road damage percentage overlaid.
