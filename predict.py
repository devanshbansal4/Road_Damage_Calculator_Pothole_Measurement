from ultralytics import YOLO
import cv2, os, numpy as np
from collections import deque
import time
import ffmpeg

model = YOLO(r'D:\projects\road_damage_assessment_system\best.pt')
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
text_position = (40, 80)
font_color = (255, 255, 255)    # White color for text
background_color = (0, 0, 255)  # Red background for text



def predict_image(image_path):

    try:
        results = model.predict(image_path)
        processed = results[0].plot(boxes=False)
        percentage_damage = 0

        if results[0].masks is not None:
            total_area = 0
            masks = results[0].masks.data.cpu().numpy()
            image_area = processed.shape[0] * processed.shape[1]
            for mask in masks:
                binary_mask = (mask > 0.5).astype(np.uint8) * 255
                contours, _ = cv2.findContours(binary_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    total_area += cv2.contourArea(cnt)
            percentage_damage = (total_area / image_area) * 100
 
        cv2.line(processed, (text_position[0], text_position[1] - 10), (text_position[0] + 350, text_position[1] - 10), background_color, 40)
        
        cv2.putText(processed, f'Road Damage: {percentage_damage:.2f}%', text_position, font, font_scale, font_color, 2, cv2.LINE_AA)


        filename = os.path.basename(image_path)
        output_path = os.path.join("static/predictions", filename)
        # cv2.imshow("Output Image", processed)
        # cv2.waitKey(0)

        cv2.imwrite(output_path, processed)
        return f"predictions/{filename}"

    
    except Exception as e:
        print(f"Error in image prediction: {e}")
        return None, None

def convert(input_path):
    os.makedirs("static/predictions", exist_ok=True)
    base_name, _ = os.path.splitext(os.path.basename(input_path))
    converted_name = base_name + '_c_.mp4'
    output_path = os.path.join("static/predictions", converted_name)
    
    ffmpeg.input(input_path).output(output_path, vcodec='libx264', acodec='aac').run(overwrite_output=True)
    print(f"Video successfully converted to {output_path}")
    
    return output_path  # Return the final converted video path


def predict_video(video_path):
    damage_deque = deque(maxlen=10)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    os.makedirs("static/predictions", exist_ok=True)
    original_filename = os.path.basename(video_path)
    temp_output_path = os.path.join("static/predictions", original_filename)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform inference (assuming model is defined globally)
        results = model.predict(source=frame, imgsz=640, conf=0.25)
        processed_frame = results[0].plot(boxes=False)

        percentage_damage = 0
        if results[0].masks is not None:
            total_area = 0
            masks = results[0].masks.data.cpu().numpy()
            image_area = frame.shape[0] * frame.shape[1]

            for mask in masks:
                binary_mask = (mask > 0).astype(np.uint8) * 255
                contours, _ = cv2.findContours(binary_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    total_area += cv2.contourArea(cnt)

            percentage_damage = (total_area / image_area) * 100

        damage_deque.append(percentage_damage)
        smoothed_percentage_damage = sum(damage_deque) / len(damage_deque)

        # Annotate frame
        cv2.line(processed_frame, (text_position[0], text_position[1] - 10),
                 (text_position[0] + 350, text_position[1] - 10), background_color, 40)
        cv2.putText(processed_frame, f'Road Damage: {smoothed_percentage_damage:.2f}%',
                    text_position, font, font_scale, font_color, 2, cv2.LINE_AA)

        out.write(processed_frame)

    cap.release()
    out.release()

    time.sleep(1)

    final_path = convert(temp_output_path)  # Convert and return final file path
    filename = os.path.basename(final_path)
    return f"predictions/{filename}"
