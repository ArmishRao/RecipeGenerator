from ultralytics import YOLO
from transformers import AutoTokenizer, FlaxT5ForConditionalGeneration

# --- YOLOv8 Model ---
model_image = YOLO('yolov8n.pt') 
model_image.save_pretrained("./models/yolov8n") 

# --- T5 Recipe Model ---
model_name = "flax-community/t5-recipe-generation"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model_recipe = FlaxT5ForConditionalGeneration.from_pretrained(model_name)
model_recipe.save_pretrained("./models/t5-recipe-generation")
tokenizer.save_pretrained("./models/t5-recipe-generation")

print("Models downloaded and saved locally!")
