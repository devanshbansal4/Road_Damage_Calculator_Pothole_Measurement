import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, url_for
from datetime import datetime
from predict import predict_image, predict_video

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        _, ext = os.path.splitext(secure_filename(file.filename))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{timestamp}{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(save_path)

        # Setup the app to predict the stuff
        predicted_image_path = predict_image(save_path)

        if predicted_image_path:
            original_url=url_for('static', filename=f'uploads/{new_filename}')
            predicted_url = url_for('static', filename=f'predictions/{new_filename}')
            return render_template("index.html", original_image_url=original_url, predicted_image_url=predicted_url, input_type="image")
            # return render_template('index.html', original_image_url=original_url, predicted_image_url=predicted_url)

        else:
            return "Prediction failed", 400
        
    return "No file uploaded", 400

@app.route('/upload_video', methods=['POST'])
def upload_video():
    file = request.files['video']
    if file:
        _, ext = os.path.splitext(secure_filename(file.filename))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{timestamp}{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(save_path)
        predict_video_path = predict_video(save_path)
        final_filename = os.path.basename(predict_video_path)
        if predict_video_path:
            predicted_video_url = url_for('static', filename=f'predictions/{final_filename}')
            print(url_for('static', filename=f'predictions/{final_filename}'))
            return render_template("index.html", predicted_video_url=predicted_video_url, input_type="video")
            # return render_template('index.html', predicted_video_url=predicted_video_url)

        else:
            return "Prediction failed", 400
    return "No file uploaded", 400



if __name__ == '__main__':
    app.run(debug=True)