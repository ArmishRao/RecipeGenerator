# from flask import Flask, request, jsonify
# from flask import render_template
# from flask import send_from_directory
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
# import os
# from ultralytics import YOLO
# from transformers import AutoTokenizer, FlaxT5ForConditionalGeneration
# import jax.numpy as jnp
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_LEFT
# from reportlab.lib import colors
# import datetime
# import base64
# from io import BytesIO


# app=Flask(__name__)

# folder_path=os.path.join(os.getcwd(), 'uploads')
# model_image = YOLO("./models/yolov8n")

# print("Check 1: Loaded YOLO model")

# model_recipe = FlaxT5ForConditionalGeneration.from_pretrained("./models/t5-recipe-generation")
# tokenizer = AutoTokenizer.from_pretrained("./models/t5-recipe-generation")

# print("Check 2: Loaded T5 Recipe model")
# @app.route('/')
# def home():
#     return render_template('homepage.html')

# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     if 'image' not in request.files:
#         return jsonify({'error':'No images found in the request.'}), 400
#     file=request.files['image']
#     filename=secure_filename(file.filename)
#     full_path=os.path.join(folder_path, filename)
#     file.save(full_path)
#     return jsonify({"message": "File saved!", "filename": filename})     

# # @app.route('/predict', methods=['POST'])
# # def predict():
# #     filename=request.form.get('text')
# #     if not filename:
# #         return jsonify({'error': 'No file recieved'}), 400
# #     filepath=os.path.join(folder_path, filename)
    
# #     result=model_image(filepath)

# #     result=result[0]#for image 1 incase of multiple images
# #     names=result.names#all possible options
# #     boxes=result.boxes#actual items
# #     cls_ids=boxes.cls.tolist()

# #     detected_items=[names[int(c)] for c in cls_ids]
# #     detected_items=list(set(detected_items))
# #     return jsonify({"items": detected_items})   

# # @app.route("/generaterecipe")
# # def index():
# #     return render_template("index.html")

# # @app.route("/generate", methods=["POST"])
# # def generate_recipe():
# #     ingredients = request.form["ingredients"]

# #     prompt = f"ingredients: {ingredients} recipe:"

# #     inputs = tokenizer(prompt, return_tensors="jax")
# #     output_ids = model_recipe.generate(
# #         input_ids=inputs["input_ids"],
# #         max_length=200
# #     ).sequences

# #     recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)

# #     return jsonify({"recipe": recipe})
# @app.route('/predict', methods=['POST'])
# def predict():
#     filename = request.form.get('text')
#     if not filename:
#         return jsonify({'error': 'No file received'}), 400
    
#     filepath = os.path.join(folder_path, filename)
    
#     # 1. Detect items with YOLOv8
#     result = model_image(filepath)
#     result = result[0]
#     names = result.names
#     boxes = result.boxes
    
#     if boxes is None:
#         return jsonify({"items": [], "recipe": "No ingredients detected."})
    
#     cls_ids = boxes.cls.tolist()
#     detected_items = [names[int(c)] for c in cls_ids]
#     detected_items = list(set(detected_items))
    
#     # 2. Format ingredients for T5 model
#     if detected_items:
#         ingredients_string = ", ".join(detected_items)
        
#         # 3. Generate recipe with T5
#         prompt = f"ingredients: {ingredients_string} recipe:"
        
#         inputs = tokenizer(prompt, return_tensors="jax")
#         output_ids = model_recipe.generate(
#             input_ids=inputs["input_ids"],
#             max_length=300  # Increased for longer recipes
#         ).sequences
        
#         recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
#         return jsonify({
#             "items": detected_items,
#             "recipe": recipe,
#             "ingredients_used": ingredients_string
#         })
#     else:
#         return jsonify({
#             "items": [],
#             "recipe": "No ingredients detected to generate a recipe.",
#             "ingredients_used": ""
#         })
# @app.route("/generaterecipe")
# def index():
#     return render_template("index.html")

# @app.route("/generate", methods=["POST"])
# def generate_recipe():
#     ingredients = request.form.get("ingredients")
    
#     if not ingredients:
#         # Try to get from query parameter if not in form
#         ingredients = request.args.get("ingredients", "")
    
#     prompt = f"ingredients: {ingredients} recipe:"
    
#     inputs = tokenizer(prompt, return_tensors="jax")
#     output_ids = model_recipe.generate(
#         input_ids=inputs["input_ids"],
#         max_length=200
#     ).sequences
    
#     recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
#     return jsonify({"recipe": recipe, "ingredients_used": ingredients})

# # Add a new route to go directly from detection to recipe
# @app.route("/detect_and_generate", methods=["POST"])
# def detect_and_generate():
#     filename = request.form.get('text')
#     if not filename:
#         return jsonify({'error': 'No file received'}), 400
#     filepath = os.path.join(folder_path, filename)
    
#     # 1. Detect items with YOLO
#     result = model_image(filepath)
#     result = result[0]
#     names = result.names
#     boxes = result.boxes
#     cls_ids = boxes.cls.tolist()

#     detected_items = [names[int(c)] for c in cls_ids]
#     detected_items = list(set(detected_items))
#     ingredients_string = ", ".join(detected_items)
    
#     # 2. Generate recipe with T5
#     prompt = f"ingredients: {ingredients_string} recipe:"
    
#     inputs = tokenizer(prompt, return_tensors="jax")
#     output_ids = model_recipe.generate(
#         input_ids=inputs["input_ids"],
#         max_length=200
#     ).sequences
    
#     recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
#     return jsonify({
#         "detected_items": detected_items,
#         "recipe": recipe,
#         "ingredients_used": ingredients_string
#     })

# @app.route('/generate_pdf', methods=['POST'])
# def generate_pdf():
#     try:
#         data = request.json
#         recipe_title = data.get('title', 'Generated Recipe')
#         ingredients = data.get('ingredients', [])
#         recipe_text = data.get('recipe', '')
        
#         # Create PDF in memory
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter)
#         story = []
        
#         # Get styles
#         styles = getSampleStyleSheet()
        
#         # Custom styles
#         title_style = ParagraphStyle(
#             'CustomTitle',
#             parent=styles['Heading1'],
#             fontSize=24,
#             textColor=colors.HexColor('#2E8B57'),
#             alignment=TA_CENTER,
#             spaceAfter=30
#         )
        
#         subtitle_style = ParagraphStyle(
#             'CustomSubtitle',
#             parent=styles['Heading2'],
#             fontSize=16,
#             textColor=colors.HexColor('#8FAD88'),
#             spaceAfter=20
#         )
        
#         normal_style = ParagraphStyle(
#             'CustomNormal',
#             parent=styles['Normal'],
#             fontSize=12,
#             leading=14,
#             spaceAfter=10
#         )
        
#         # Add title
#         story.append(Paragraph(recipe_title, title_style))
#         story.append(Spacer(1, 20))
        
#         # Add timestamp
#         timestamp = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
#         story.append(Paragraph(f"Generated on: {timestamp}", styles['Italic']))
#         story.append(Spacer(1, 30))
        
#         # Add ingredients section
#         story.append(Paragraph("Ingredients:", subtitle_style))
        
#         if isinstance(ingredients, list):
#             for ingredient in ingredients:
#                 story.append(Paragraph(f"• {ingredient}", normal_style))
#         else:
#             story.append(Paragraph(ingredients, normal_style))
        
#         story.append(Spacer(1, 30))
        
#         # Add recipe section
#         story.append(Paragraph("Recipe:", subtitle_style))
        
#         # Format recipe text with better spacing
#         recipe_paragraphs = recipe_text.split('\n')
#         for para in recipe_paragraphs:
#             if para.strip():
#                 story.append(Paragraph(para.strip(), normal_style))
#                 story.append(Spacer(1, 8))
        
#         # Build PDF
#         doc.build(story)
        
#         # Get PDF bytes
#         pdf_bytes = buffer.getvalue()
#         buffer.close()
        
#         # Convert to base64 for sending
#         pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
#         return jsonify({
#             'success': True,
#             'pdf_base64': pdf_base64,
#             'filename': f"recipe_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500

# # Simpler PDF generation endpoint (alternative)
# @app.route('/generate_pdf_simple', methods=['POST'])
# def generate_pdf_simple():
#     try:
#         data = request.json
#         ingredients = data.get('ingredients', [])
#         recipe = data.get('recipe', 'No recipe generated.')
        
#         buffer = BytesIO()
#         c = canvas.Canvas(buffer, pagesize=letter)
        
#         # Set up PDF
#         c.setTitle("Generated Recipe")
#         c.setFont("Helvetica-Bold", 24)
#         c.setFillColorRGB(0.18, 0.55, 0.34)  # #2E8B57
#         c.drawString(50, 750, "Your Recipe")
        
#         # Add timestamp
#         c.setFont("Helvetica", 10)
#         c.setFillColorRGB(0.5, 0.5, 0.5)
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#         c.drawString(50, 730, f"Generated: {timestamp}")
        
#         # Ingredients section
#         c.setFont("Helvetica-Bold", 16)
#         c.setFillColorRGB(0.56, 0.68, 0.53)  # #8FAD88
#         c.drawString(50, 700, "Ingredients:")
        
#         c.setFont("Helvetica", 12)
#         c.setFillColorRGB(0, 0, 0)
        
#         if isinstance(ingredients, list):
#             y_position = 680
#             for item in ingredients:
#                 if y_position < 50:  # New page if needed
#                     c.showPage()
#                     c.setFont("Helvetica", 12)
#                     y_position = 750
#                 c.drawString(70, y_position, f"• {item}")
#                 y_position -= 20
#         else:
#             c.drawString(70, 680, ingredients)
#             y_position = 660
        
#         # Recipe section
#         c.setFont("Helvetica-Bold", 16)
#         c.setFillColorRGB(0.56, 0.68, 0.53)
#         c.drawString(50, y_position - 20, "Recipe:")
        
#         c.setFont("Helvetica", 12)
#         c.setFillColorRGB(0, 0, 0)
        
#         # Split recipe into lines that fit the page
#         words = recipe.split(' ')
#         line = ""
#         y = y_position - 40
        
#         for word in words:
#             test_line = f"{line} {word}".strip()
#             if c.stringWidth(test_line, "Helvetica", 12) < 500:  # Page width minus margins
#                 line = test_line
#             else:
#                 c.drawString(70, y, line)
#                 y -= 20
#                 line = word
#                 if y < 50:  # New page if needed
#                     c.showPage()
#                     c.setFont("Helvetica", 12)
#                     y = 750
        
#         if line:
#             c.drawString(70, y, line)
        
#         c.save()
        
#         pdf_bytes = buffer.getvalue()
#         buffer.close()
#         pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
#         return jsonify({
#             'success': True,
#             'pdf_base64': pdf_base64,
#             'filename': f"recipe_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
#     @app.route('/get_food_image', methods=['POST'])
# @app.route('/get_food_image', methods=['POST'])
# def get_food_image():
#     try:
#         data = request.json
#         ingredients = data.get('ingredients', [])
        
#         # Use TheMealDB API for food images (free, no key needed for basic)
#         if ingredients:
#             # Try to search for a meal with the first ingredient
#             for ingredient in ingredients[:3]:
#                 try:
#                     response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}')
#                     if response.status_code == 200:
#                         meal_data = response.json()
#                         if meal_data['meals']:
#                             # Get random meal from results
#                             import random
#                             meal = random.choice(meal_data['meals'])
#                             return jsonify({
#                                 'success': True, 
#                                 'image_url': meal['strMealThumb'],
#                                 'meal_name': meal['strMeal']
#                             })
#                 except:
#                     continue
        
#         # Fallback 1: Use Foodish API
#         try:
#             response = requests.get('https://foodish-api.com/api/')
#             if response.status_code == 200:
#                 data = response.json()
#                 return jsonify({'success': True, 'image_url': data['image']})
#         except:
#             pass
        
#         # Fallback 2: Use Unsplash source with food query
#         main_ingredient = ingredients[0] if ingredients else "food"
#         placeholder_url = f"https://source.unsplash.com/featured/500x400/?{main_ingredient},dish,meal"
        
#         return jsonify({'success': True, 'image_url': placeholder_url})
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500
# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask import render_template
from flask import send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
from transformers import AutoTokenizer, FlaxT5ForConditionalGeneration
import jax.numpy as jnp
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
import base64
import datetime
import requests
import json
import os

# Ensure uploads directory exists
folder_path = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Created uploads directory at: {folder_path}")
else:
    print(f"Uploads directory exists at: {folder_path}")

app = Flask(__name__)

folder_path = os.path.join(os.getcwd(), 'uploads')
model_image = YOLO("./models/yolov8n")

print("Check 1: Loaded YOLO model")

model_recipe = FlaxT5ForConditionalGeneration.from_pretrained("./models/t5-recipe-generation")
tokenizer = AutoTokenizer.from_pretrained("./models/t5-recipe-generation")

print("Check 2: Loaded T5 Recipe model")

@app.route('/')
def home():
    return render_template('homepage.html')

# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     if 'image' not in request.files:
#         return jsonify({'error':'No images found in the request.'}), 400
#     file = request.files['image']
#     filename = secure_filename(file.filename)
#     full_path = os.path.join(folder_path, filename)
#     file.save(full_path)
#     return jsonify({"message": "File saved!", "filename": filename}
@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error':'No images found in the request.'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        full_path = os.path.join(folder_path, filename)
        
        print(f"DEBUG: Saving file to: {full_path}")
        print(f"DEBUG: File size: {file.content_length} bytes")
        
        # Save the file
        file.save(full_path)
        
        # Verify the file was saved
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            print(f"DEBUG: File saved successfully! Size: {file_size} bytes")
            return jsonify({
                "message": "File saved successfully!", 
                "filename": filename,
                "filepath": full_path
            })
        else:
            print(f"ERROR: File not saved at {full_path}")
            return jsonify({"error": "File failed to save"}), 500
                
    except Exception as e:
        print(f"ERROR in upload_image: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500
# @app.route('/predict', methods=['POST'])
# def predict():
#     filename = request.form.get('text')
#     if not filename:
#         return jsonify({'error': 'No file received'}), 400
    
#     filepath = os.path.join(folder_path, filename)
    
#     # 1. Detect items with YOLOv8
#     result = model_image(filepath)
#     result = result[0]
#     names = result.names
#     boxes = result.boxes
    
#     if boxes is None:
#         return jsonify({"items": [], "recipe": "No ingredients detected."})
    
#     cls_ids = boxes.cls.tolist()
#     detected_items = [names[int(c)] for c in cls_ids]
#     detected_items = list(set(detected_items))
    
#     # 2. Format ingredients for T5 model
#     if detected_items:
#         ingredients_string = ", ".join(detected_items)
        
#         # 3. Generate recipe with T5
#         prompt = f"ingredients: {ingredients_string} recipe:"
        
#         inputs = tokenizer(prompt, return_tensors="jax")
#         output_ids = model_recipe.generate(
#             input_ids=inputs["input_ids"],
#             max_length=300
#         ).sequences
        
#         recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
#         return jsonify({
#             "items": detected_items,
#             "recipe": recipe,
#             "ingredients_used": ingredients_string
#         })
#     else:
#         return jsonify({
#             "items": [],
#             "recipe": "No ingredients detected to generate a recipe.",
#             "ingredients_used": ""
#         })
@app.route('/predict', methods=['POST'])
def predict():
    try:
        filename = request.form.get('text')
        if not filename:
            return jsonify({'error': 'No file received'}), 400
        
        filepath = os.path.join(folder_path, filename)
        
        print(f"DEBUG: Looking for file at: {filepath}")
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"ERROR: File does not exist at {filepath}")
            
            # List files in uploads directory to debug
            if os.path.exists(folder_path):
                files_in_folder = os.listdir(folder_path)
                print(f"DEBUG: Files in uploads folder: {files_in_folder}")
            
            return jsonify({
                "error": f"File not found: {filename}",
                "suggestion": "Try uploading the image again"
            }), 404
        
        print(f"DEBUG: File found! Size: {os.path.getsize(filepath)} bytes")
        
        # Rest of your detection code...
        
    except Exception as e:
        print(f"ERROR in predict: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
           

@app.route("/generaterecipe")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_recipe():
    ingredients = request.form.get("ingredients")
    
    if not ingredients:
        # Try to get from query parameter if not in form
        ingredients = request.args.get("ingredients", "")
    
    prompt = f"ingredients: {ingredients} recipe:"
    
    inputs = tokenizer(prompt, return_tensors="jax")
    output_ids = model_recipe.generate(
        input_ids=inputs["input_ids"],
        max_length=200
    ).sequences
    
    recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return jsonify({"recipe": recipe, "ingredients_used": ingredients})

@app.route("/detect_and_generate", methods=["POST"])
def detect_and_generate():
    filename = request.form.get('text')
    if not filename:
        return jsonify({'error': 'No file received'}), 400
    filepath = os.path.join(folder_path, filename)
    
    # 1. Detect items with YOLO
    result = model_image(filepath)
    result = result[0]
    names = result.names
    boxes = result.boxes
    cls_ids = boxes.cls.tolist()

    detected_items = [names[int(c)] for c in cls_ids]
    detected_items = list(set(detected_items))
    ingredients_string = ", ".join(detected_items)
    
    # 2. Generate recipe with T5
    prompt = f"ingredients: {ingredients_string} recipe:"
    
    inputs = tokenizer(prompt, return_tensors="jax")
    output_ids = model_recipe.generate(
        input_ids=inputs["input_ids"],
        max_length=200
    ).sequences
    
    recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return jsonify({
        "detected_items": detected_items,
        "recipe": recipe,
        "ingredients_used": ingredients_string
    })

# PDF Generation Routes
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        recipe_title = data.get('title', 'Generated Recipe')
        ingredients = data.get('ingredients', [])
        recipe_text = data.get('recipe', '')
        
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E8B57'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#8FAD88'),
            spaceAfter=20
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            leading=14,
            spaceAfter=10
        )
        
        # Add title
        story.append(Paragraph(recipe_title, title_style))
        story.append(Spacer(1, 20))
        
        # Add timestamp
        timestamp = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"Generated on: {timestamp}", styles['Italic']))
        story.append(Spacer(1, 30))
        
        # Add ingredients section
        story.append(Paragraph("Ingredients:", subtitle_style))
        
        if isinstance(ingredients, list):
            for ingredient in ingredients:
                story.append(Paragraph(f"• {ingredient}", normal_style))
        else:
            story.append(Paragraph(ingredients, normal_style))
        
        story.append(Spacer(1, 30))
        
        # Add recipe section
        story.append(Paragraph("Recipe:", subtitle_style))
        
        # Format recipe text with better spacing
        recipe_paragraphs = recipe_text.split('\n')
        for para in recipe_paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), normal_style))
                story.append(Spacer(1, 8))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        # Convert to base64 for sending
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return jsonify({
            'success': True,
            'pdf_base64': pdf_base64,
            'filename': f"recipe_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/generate_pdf_simple', methods=['POST'])
def generate_pdf_simple():
    try:
        data = request.json
        ingredients = data.get('ingredients', [])
        recipe = data.get('recipe', 'No recipe generated.')
        
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Set up PDF
        c.setTitle("Generated Recipe")
        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(0.18, 0.55, 0.34)  # #2E8B57
        c.drawString(50, 750, "Your Recipe")
        
        # Add timestamp
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        c.drawString(50, 730, f"Generated: {timestamp}")
        
        # Ingredients section
        c.setFont("Helvetica-Bold", 16)
        c.setFillColorRGB(0.56, 0.68, 0.53)  # #8FAD88
        c.drawString(50, 700, "Ingredients:")
        
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0, 0, 0)
        
        if isinstance(ingredients, list):
            y_position = 680
            for item in ingredients:
                if y_position < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = 750
                c.drawString(70, y_position, f"• {item}")
                y_position -= 20
        else:
            c.drawString(70, 680, ingredients)
            y_position = 660
        
        # Recipe section
        c.setFont("Helvetica-Bold", 16)
        c.setFillColorRGB(0.56, 0.68, 0.53)
        c.drawString(50, y_position - 20, "Recipe:")
        
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0, 0, 0)
        
        # Split recipe into lines that fit the page
        words = recipe.split(' ')
        line = ""
        y = y_position - 40
        
        for word in words:
            test_line = f"{line} {word}".strip()
            if c.stringWidth(test_line, "Helvetica", 12) < 500:
                line = test_line
            else:
                c.drawString(70, y, line)
                y -= 20
                line = word
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
        
        if line:
            c.drawString(70, y, line)
        
        c.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return jsonify({
            'success': True,
            'pdf_base64': pdf_base64,
            'filename': f"recipe_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_food_image', methods=['POST'])
def get_food_image():
    try:
        data = request.json
        ingredients = data.get('ingredients', [])
        
        # Use TheMealDB API for food images
        if ingredients:
            # Try to search for a meal with the first ingredient
            for ingredient in ingredients[:3]:
                try:
                    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}')
                    if response.status_code == 200:
                        meal_data = response.json()
                        if meal_data['meals']:
                            # Get random meal from results
                            import random
                            meal = random.choice(meal_data['meals'])
                            return jsonify({
                                'success': True, 
                                'image_url': meal['strMealThumb'],
                                'meal_name': meal['strMeal']
                            })
                except:
                    continue
        
        # Fallback to Foodish API
        try:
            response = requests.get('https://foodish-api.com/api/')
            if response.status_code == 200:
                data = response.json()
                return jsonify({'success': True, 'image_url': data['image']})
        except:
            pass
        
        # Final fallback
        main_ingredient = ingredients[0] if ingredients else "food"
        placeholder_url = f"https://source.unsplash.com/featured/500x400/?{main_ingredient},dish,meal"
        
        return jsonify({'success': True, 'image_url': placeholder_url})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
        
@app.route('/get_recipe_image', methods=['POST'])
def get_recipe_image():
    try:
        data = request.json
        recipe_title = data.get('title', '')
        ingredients = data.get('ingredients', [])
        
        print(f"DEBUG: Received request for recipe image")
        print(f"DEBUG - Title: {recipe_title}")
        print(f"DEBUG - Ingredients: {ingredients}")
        
        # Ensure ingredients is a list
        if not isinstance(ingredients, list):
            ingredients = [str(ingredients)] if ingredients else []
        
        # Clean ingredients list
        ingredients = [ing.strip().lower() for ing in ingredients if ing and str(ing).strip()]
        print(f"DEBUG - Cleaned ingredients: {ingredients}")
        
        image_url = None
        source_used = "default"
        
        # STRATEGY 1: Try direct Unsplash with specific food terms
        if ingredients:
            # Create a search query from ingredients
            search_terms = []
            for ingredient in ingredients:
                # Add the ingredient itself
                search_terms.append(ingredient)
                # Add common recipe types for that ingredient
                if ingredient in ['chicken', 'beef', 'pork', 'fish']:
                    search_terms.append(f"{ingredient} recipe")
                    search_terms.append(f"{ingredient} dish")
                elif ingredient in ['apple', 'banana', 'orange', 'fruit']:
                    search_terms.append("fruit smoothie")
                    search_terms.append("fruit salad")
                elif ingredient in ['rice', 'pasta', 'noodles']:
                    search_terms.append(f"{ingredient} dish")
            
            # Add general food terms
            search_terms.extend(['food', 'cooking', 'delicious', 'meal'])
            
            # Use the most specific terms first
            query = ','.join(search_terms[:3])
            image_url = f"https://source.unsplash.com/featured/600x400/?{query}"
            source_used = "Unsplash"
            print(f"DEBUG - Unsplash query: {query}")
            print(f"DEBUG - Unsplash URL: {image_url}")
        
        # STRATEGY 2: Try Spoonacular API (free, food-focused)
        if not image_url and ingredients:
            try:
                # Spoonacular food images API
                api_key = "YOUR_API_KEY_HERE"  # Get free key from spoonacular.com
                if api_key != "YOUR_API_KEY_HERE":
                    ingredient_query = '+'.join(ingredients[:2])
                    spoonacular_url = f"https://api.spoonacular.com/recipes/complexSearch?query={ingredient_query}&number=1&apiKey={api_key}"
                    response = requests.get(spoonacular_url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('results') and len(data['results']) > 0:
                            image_url = data['results'][0]['image']
                            source_used = "Spoonacular"
                            print(f"DEBUG - Spoonacular result: {image_url}")
            except Exception as e:
                print(f"DEBUG - Spoonacular error: {e}")
        
        # STRATEGY 3: Try TheMealDB with the first ingredient
        if not image_url and ingredients:
            try:
                first_ingredient = ingredients[0]
                # Clean ingredient name for API
                clean_ingredient = first_ingredient.replace(' ', '_')
                themaldb_url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={clean_ingredient}"
                response = requests.get(themaldb_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('meals'):
                        import random
                        meal = random.choice(data['meals'])
                        image_url = meal['strMealThumb']
                        source_used = "TheMealDB"
                        print(f"DEBUG - TheMealDB result: {image_url}")
            except Exception as e:
                print(f"DEBUG - TheMealDB error: {e}")
        
        # STRATEGY 4: Try Foodish API as backup
        if not image_url:
            try:
                response = requests.get('https://foodish-api.com/api/', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    image_url = data['image']
                    source_used = "Foodish"
                    print(f"DEBUG - Foodish result: {image_url}")
            except Exception as e:
                print(f"DEBUG - Foodish error: {e}")
        
        # STRATEGY 5: Final fallback - Use recipe-specific placeholder
        if not image_url:
            # Create a more specific fallback based on ingredients
            if 'smoothie' in recipe_title.lower() or any(x in ['apple', 'banana', 'orange', 'fruit'] for x in ingredients):
                image_url = "https://images.unsplash.com/photo-1502741224143-90386d7f8c82?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80"
            elif any(x in ['chicken', 'beef', 'meat'] for x in ingredients):
                image_url = "https://images.unsplash.com/photo-1600891964092-4316c288032e?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80"
            elif any(x in ['pasta', 'noodles', 'spaghetti'] for x in ingredients):
                image_url = "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80"
            else:
                image_url = "https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80"
            source_used = "Unsplash Fallback"
            print(f"DEBUG - Using fallback: {image_url}")
        
        # Add cache-busting timestamp
        import time
        timestamp = int(time.time())
        if '?' in image_url:
            image_url += f"&t={timestamp}"
        else:
            image_url += f"?t={timestamp}"
        
        print(f"DEBUG - Final image URL: {image_url}")
        print(f"DEBUG - Source: {source_used}")
        
        return jsonify({
            'success': True, 
            'image_url': image_url,
            'source': source_used
        })
        
    except Exception as e:
        print(f"ERROR in get_recipe_image: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'error': str(e),
            'image_url': "https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80"
        })
def get_foodish_image():
    """Get image from Foodish API"""
    response = requests.get('https://foodish-api.com/api/', timeout=3)
    if response.status_code == 200:
        data = response.json()
        return data['image']
    raise Exception("Foodish API failed")

# Add this route after your other routes
@app.route('/direct_predict', methods=['POST'])
def direct_predict():
    """Handle prediction directly from uploaded file without saving first"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file received'}), 400
        
        file = request.files['image']
        
        # Create a temporary file path
        import tempfile
        import uuid
        
        # Create a unique filename
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        
        # Save the file temporarily
        file.save(temp_path)
        
        print(f"DEBUG: Processing file directly: {filename}")
        print(f"DEBUG: Temporary path: {temp_path}")
        print(f"DEBUG: File size: {os.path.getsize(temp_path)} bytes")
        
        # 1. Detect items with YOLOv8
        result = model_image(temp_path)
        result = result[0]
        names = result.names
        boxes = result.boxes
        
        if boxes is None:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({"items": [], "recipe": "No ingredients detected."})
        
        cls_ids = boxes.cls.tolist()
        detected_items = [names[int(c)] for c in cls_ids]
        detected_items = list(set(detected_items))
        
        print(f"DEBUG: Direct prediction - Detected items: {detected_items}")
        
        # 2. Format ingredients for T5 model
        if detected_items:
            ingredients_string = ", ".join(detected_items)
            
            # 3. Generate recipe with T5
            prompt = f"ingredients: {ingredients_string} recipe:"
            
            inputs = tokenizer(prompt, return_tensors="jax")
            output_ids = model_recipe.generate(
                input_ids=inputs["input_ids"],
                max_length=300
            ).sequences
            
            recipe = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return jsonify({
                "items": detected_items,
                "recipe": recipe,
                "ingredients_used": ingredients_string
            })
        else:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return jsonify({
                "items": [],
                "recipe": "No ingredients detected to generate a recipe.",
                "ingredients_used": ""
            })
            
    except Exception as e:
        print(f"ERROR in direct_predict: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Clean up temp file if it exists
        try:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass
        
        return jsonify({'error': f'Direct prediction failed: {str(e)}'}), 500
if __name__ == "__main__":
    app.run(debug=True)
