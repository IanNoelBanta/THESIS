from ultralytics import YOLO 
import cv2 as cv

model = YOLO('yolov8n.pt')

camera = cv.VideoCapture(0)

while True:
    ret, frame = camera.read()

    results = model(frame, stream=True)

    for r in results:
        print(r.boxes.xywhn, )

    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv.destroyAllWindows()