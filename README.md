Pothole detection in images using YOLOV8

The requirements.txt file contains the names of libraries required for training the model, and can be directly imported into python.

The dataset was taken from kaggle, here is the url :: https://www.kaggle.com/datasets/farzadnekouei/pothole-image-segmentation-dataset

evaluate_model_visualize.py.py Evaluates the trained YOLO model on test data and visualizes the detections. Generates annotated images and metrics like precision, recall, and mAP.

inference_single_image.py.py Performs inference on a single image using the trained YOLO model. Displays and saves the output image with detected potholes and confidence scores.

train_model_with_analysis.py.py Trains the YOLO model on the pothole dataset with training and validation monitoring. Also includes analysis such as loss curves and performance summaries after training.
