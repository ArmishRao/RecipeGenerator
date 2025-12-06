from flask import Flask, request, jsonify
from flask import render_template
from flask import send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
from transformers import AutoTokenizer, FlaxT5ForConditionalGeneration
import jax.numpy as jnp

app=Flask(__name__)

model=YOLO('yolov8n.pt')#download/load a pretrained YOLOv8n model
model.save_pretrained("./models/t5-recipe-generation")
folder_path=os.path.join(os.getcwd(), 'uploads')

# Load model + tokenizer
model_name = "flax-community/t5-recipe-generation"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = FlaxT5ForConditionalGeneration.from_pretrained(model_name)
model.save_pretrained("./models/t5-recipe-generation")

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

# @app.route('/uploads/<filename>')
# def access_file(filename):
#     return send_from_directory("uploads", filename)

@app.route('/predict', methods=['POST'])
def predict():
    filename=request.form.get('text')
    if not filename:
        return jsonify({'error': 'No file recieved'}), 400
    filepath=os.path.join(folder_path, filename)
    
    result=model(filepath)

    result=result[0]#for image 1 incase of multiple images
    names=result.names#all possible options
    boxes=result.boxes#actual items
    cls_ids=boxes.cls.tolist()

    detected_items=[names[int(c)] for c in cls_ids]
    detected_items=list(set(detected_items))
    return jsonify({"items": detected_items})   

@app.route("/generaterecipe")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_recipe():
    ingredients = request.form["ingredients"]

    prompt = f"ingredients: {ingredients} recipe:"

    inputs = tokenizer(prompt, return_tensors="jax")
    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        max_length=200
    ).sequences

    recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return jsonify({"recipe": recipe})

if __name__ == "__main__":
    app.run(debug=True)

