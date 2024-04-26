# from ultralytics import YOLO

# # Load a model
# model = YOLO('yolov8s.pt')  # load an official model
# model = YOLO('C:/Users/villa/OneDrive/Documents/Projects/THESIS/best.pt')  # load a custom trained model

# # Export the model
# model.export(format='onnx')


from ultralytics.utils.checks import parse_requirements

print(parse_requirements(package='ultralytics'))