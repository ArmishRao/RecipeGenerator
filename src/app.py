from flask import Flask, request, jsonify
from flask import render_template
from flask import send_from_directory
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

@app.route('/uploads/<filename>')
def access_file(filename):
    return send_from_directory("uploads", filename)

@app.route('/predict', methods=['POST'])
def predict():
    filename=request.form.get('text')
    if not filename:
        return jsonify({'error': 'No file recieved'}), 400
    filepath=os.path.join(folder_path, filename)
    
    result=model(filepath)

if __name__ == "__main__":
    app.run(debug=True)