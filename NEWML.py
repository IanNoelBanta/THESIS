import time
import cv2
import serial
from ultralytics import YOLO

arduino = serial.Serial(port = 'COM5', baudrate=9600, timeout=0)

model = YOLO("best500n.pt")

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

mask = cv2.imread("mask.png")

while True:
    success, frame = cap.read()
    frame = cv2.bitwise_and(frame, mask)

    if not success:
        print("Error reading frame")
        break

    results = model.track(frame, verbose=False, classes=[1], max_det=1, stream_buffer=True, conf=0.8)
    # results = model.track(frame, classes=[1], max_det=1, stream_buffer=True, conf=0.5, verbose=False) # detect
    # results = model.predict(frame, classes=[1], max_det=1, stream_buffer=True, conf=0.75, verbose=False) # detect


    if results[0]:
        frame = results[0].plot() # plot lahat ng detections
        targetX1 = int(results[0].boxes.xyxy.cpu().numpy()[0][0])
        targetY1 = int(results[0].boxes.xyxy.cpu().numpy()[0][1])
        targetX2 = int(results[0].boxes.xyxy.cpu().numpy()[0][2])
        targetY2 = int(results[0].boxes.xyxy.cpu().numpy()[0][3])

        targetY1Offset = targetY1 - 0

        targetXCenter, targetYCenter = int((targetX1 + targetX2) / 2), int((targetY1 + targetY2) / 2)

        # targetCrosshairVerticalStart, targetCrosshairVerticalEnd = (targetXCenter, targetY1Offset - 10), (qtargetXCenter, targetY1Offset + 10) 
        # targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd = (targetXCenter - 10, targetY1Offset), (targetXCenter + 10, targetY1Offset)

        # cv2.line(frame, targetCrosshairVerticalStart, targetCrosshairVerticalEnd, (0, 0, 255), 3) # crosshair vertical line
        # cv2.line(frame, targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd, (0, 0, 255), 3) # crosshair horizontal line
        
        targetCrosshairVerticalStart, targetCrosshairVerticalEnd = (targetXCenter, targetYCenter - 10), (targetXCenter, targetYCenter + 10) 
        targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd = (targetXCenter - 10, targetYCenter), (targetXCenter + 10, targetYCenter)

        cv2.line(frame, targetCrosshairVerticalStart, targetCrosshairVerticalEnd, (0, 0, 255), 3) # crosshair vertical line
        cv2.line(frame, targetCrosshairVerticalStart, targetCrosshairVerticalEnd, (0, 0, 255), 3) # crosshair vertical line

        cv2.line(frame, (CAM_X_CENTER - 50, CAM_Y_CENTER - 50), (CAM_X_CENTER + 50, CAM_Y_CENTER - 50), (0, 255, 0), 3) # crosshair horizontal line
        cv2.line(frame, (CAM_X_CENTER - 50, CAM_Y_CENTER + 50), (CAM_X_CENTER + 50, CAM_Y_CENTER + 50), (0, 255, 0), 3) # crosshair vertical line


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
                
                time.sleep(10)
                # reset all for next target
                print("RESET")
                isXGood = False
                isYGood = False
    else:
        if isXGood:
            pass
            # if isYGood:
            #     pass
            # else:
            #     if yCommand == 'u':
            #         print("LAST MOVE: U -> GO DOWN")
            #         arduino.write(str.encode('d'))
            #     else:
            #         print("LAST MOVE: D -> GO UP")
            #         arduino.write(str.encode('u'))
        elif isXGood == False:
            print("NO DETECTION -> GO RIGHT")
            arduino.write(str.encode('r'))
        


    cv2.line(frame, (CAM_LEFT_TOLERANCE, 0), (CAM_LEFT_TOLERANCE, 480), (255, 0, 0), 3) # left vertical line
    cv2.line(frame, (CAM_RIGHT_TOLERANCE, 0), (CAM_RIGHT_TOLERANCE, 480), (255, 0, 0), 3) # right vertical line
    cv2.line(frame, (0, CAM_TOP_TOLERANCE), (640, CAM_TOP_TOLERANCE), (0, 0, 255), 3) # top horizontal line
    cv2.line(frame, (0, CAM_BOTTOM_TOLERANCE), (640, CAM_BOTTOM_TOLERANCE), (0, 0, 255), 3) # bottom horizontal line
    cv2.imshow("Real-time Object Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
