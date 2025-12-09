from ultralytics import YOLO

model = YOLO("../models/yolov8n_retrained.pt")  # or yolov8n.yaml, etc.
metrics = model.val(data="data.yaml")  # or correct relative path

print(f"Precision: {metrics.results_dict['metrics/precision(B)']:.4f}")
print(f"Recall:    {metrics.results_dict['metrics/recall(B)']:.4f}")
print(f"mAP50:     {metrics.results_dict['metrics/mAP50(B)']:.4f}")
print(f"mAP50-95:  {metrics.results_dict['metrics/mAP50-95(B)']:.4f}")