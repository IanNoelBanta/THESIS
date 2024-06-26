import time
import cv2
# import numpy as np
import serial
from ultralytics import YOLO

# from ultralytics.utils.checks import check_imshow
from ultralytics.utils.plotting import Annotator, colors

from collections import defaultdict

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

arduino = serial.Serial(port = 'COM5', baudrate=9600, timeout=0)

# track_history = defaultdict(lambda: [])
model = YOLO("best500n.pt")
names = model.model.names

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

CAM_X_CENTER = 320
CAM_Y_CENTER = 240
TOLERANCE = 5
CAM_LEFT_TOLERANCE = CAM_X_CENTER - TOLERANCE
CAM_RIGHT_TOLERANCE = CAM_X_CENTER + TOLERANCE
CAM_TOP_TOLERANCE = CAM_Y_CENTER - TOLERANCE
CAM_BOTTOM_TOLERANCE = CAM_Y_CENTER + TOLERANCE

xCommand = ""
yCommand = ""
isXGood = False
isYGood = False


while True:
    success, frame = cap.read()
    
    if not success:
        print("Error reading frame")
        break

    results = model.track(frame, verbose=False, classes=[1], max_det=1, stream_buffer=True, conf=0.8)
    boxes = results[0].boxes.xyxy.cpu()

    cv2.line(frame, (CAM_LEFT_TOLERANCE, 0), (CAM_LEFT_TOLERANCE, 480), (255, 0, 0), 3) # left vertical line
    cv2.line(frame, (CAM_RIGHT_TOLERANCE, 0), (CAM_RIGHT_TOLERANCE, 480), (255, 0, 0), 3) # right vertical line
    cv2.line(frame, (0, CAM_TOP_TOLERANCE), (640, CAM_TOP_TOLERANCE), (0, 0, 255), 3) # top horizontal line
    cv2.line(frame, (0, CAM_BOTTOM_TOLERANCE), (640, CAM_BOTTOM_TOLERANCE), (0, 0, 255), 3) # bottom horizontal line


    if results[0].boxes.id is not None:

        # Extract prediction results
        clss = results[0].boxes.cls.cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        confs = results[0].boxes.conf.float().cpu().tolist()

        annotator = Annotator(frame, line_width=2)

        annotator.box_label(boxes[0], color=colors(int(clss[0]), True), label=f"{names[int(clss[0])]} - Track ID: {track_ids[0]} - Confidence: {confs[0]:.2f}")

        targetX1, targetY1, targetX2, targetY2 = int(boxes[0][0]), int(boxes[0][1]), int(boxes[0][2]), int(boxes[0][3])
        
        targetY1Offset = targetY1 - 0 #75
        
        targetXCenter, targetYCenter = int((targetX1 + targetX2) / 2), int((targetY1 + targetY2) / 2)

        # targetCrosshairVerticalStart, targetCrosshairVerticalEnd = (targetXCenter, targetY1Offset - 10), (qtargetXCenter, targetY1Offset + 10) 
        # targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd = (targetXCenter - 10, targetY1Offset), (targetXCenter + 10, targetY1Offset)

        # cv2.line(frame, targetCrosshairVerticalStart, targetCrosshairVerticalEnd, (0, 0, 255), 3) # crosshair vertical line
        # cv2.line(frame, targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd, (0, 0, 255), 3) # crosshair horizontal line
        
        targetCrosshairVerticalStart, targetCrosshairVerticalEnd = (targetXCenter, targetYCenter - 10), (targetXCenter, targetYCenter + 10) 
        targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd = (targetXCenter - 10, targetYCenter), (targetXCenter + 10, targetYCenter)

        cv2.line(frame, targetCrosshairVerticalStart, targetCrosshairVerticalEnd, (0, 0, 255), 3) # crosshair vertical line
        cv2.line(frame, targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd, (0, 0, 255), 3) # crosshair horizontal line

        if targetXCenter > CAM_RIGHT_TOLERANCE:
            xCommand = 'l'
        elif targetXCenter < CAM_LEFT_TOLERANCE:
            xCommand = 'r' 
        else:
            xCommand = 'x'

        if isXGood == False:
            print(xCommand)
            arduino.write(str.encode(xCommand))

        if xCommand == 'x':
            isXGood = True

            if targetYCenter > CAM_BOTTOM_TOLERANCE:
                yCommand = 'd'
            elif targetYCenter < CAM_TOP_TOLERANCE:
                yCommand = 'u'
            else:
                yCommand = 'y'

            if isYGood == False:
                print(yCommand)
                arduino.write(str.encode(yCommand))

            if yCommand == 'y':
                isYGood = True
                print('z')
                arduino.write(str.encode('z'))
                
                time.sleep(20) #10 orig
                # reset all for next target
                print("RESET")
                isXGood = False
                isYGood = False
        
    cv2.imshow("Real-time Object Tracking", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
