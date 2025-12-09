import yaml
import json
from pathlib import Path
import mlflow
from ultralytics import YOLO 
import os

with open("params.yaml") as f:
    params = yaml.safe_load(f)

name=os.getenv("DAGSHUB_USERNAME")
token = os.getenv("DAGSHUB_TOKEN")

# Dataset paths
train_path = params["dataset"]["train"]
val_path = params["dataset"]["val"]
test_path = params["dataset"]["test"]

# Training params
epochs = params["training"]["epochs"]
batch_size = params["training"]["batch_size"]
img_size = params["training"]["img_size"]
lr = params["training"]["lr"]

# Evaluation metrics
metrics_list = params["evaluation"]["metrics"]

# Output paths
weights_path = Path("models/yolov8n_retrained.pt")

mlflow.set_tracking_uri(f"https://{name}:{token}@dagshub.com/ArmishRao/RecipeGenerator.mlflow")
mlflow.set_experiment("YOLOv8_training")

with mlflow.start_run():

    model = YOLO("yolov8n.pt")  

    # Train the model
    results = model.train(
        data="data.yaml",
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        lr0=lr,
        save=True,
        save_period=0
    )

    model.save(weights_path)

    eval_results = model.val(data="data.yaml")
    metrics = {
    "precision": eval_results.box.precision,
    "recall": eval_results.box.recall,
    "mAP50": eval_results.box.map50,
    "mAP50-95": eval_results.box.map
    }

    #log model and metrics to mlflow
    mlflow.log_artifact(str(weights_path))  
    for key, val in metrics.items():
        if val is not None:
            mlflow.log_metric(key, val)

    print("Training complete. Model and metrics logged successfully.")
