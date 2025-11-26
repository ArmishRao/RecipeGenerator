from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO

app=Flask(__name__)

model=YOLO('yolov8n.pt')#download/load a pretrained YOLOv8n model

folder_path=os.path.join(os.getcwd(), 'uploads')

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error':'No images found in the request.'}), 400
    file=request.files['image']
    filename=secure_filename(file.filename)
    full_path=os.path.join(folder_path, filename)
    file.save(full_path)
    return jsonify({"message": "File saved!", "filename": filename})     

@app.route('/predict', methods=['POST'])
def predict():
    result=model("../uploads/download_2.jpeg")

if __name__ == "__main__":
    app.run(debug=True)