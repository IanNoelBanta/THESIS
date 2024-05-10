from ultralytics import YOLO

# # Load a model
# model = YOLO('yolov8s.pt')  # load an official model
# model = YOLO('C:/Users/villa/OneDrive/Documents/Projects/THESIS/best.pt')  # load a custom trained model

# # Export the model
# model.export(format='onnx')


from ultralytics.utils.checks import parse_requirements

# Load the YOLOv8 model
model = YOLO('best500n.pt')

# Export the model to TFLite format
model.export(format='tflite') # creates 'yolov8n_float32.tflite'
