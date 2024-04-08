from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time

# arduino = serial.Serial(port = 'COM7', timeout=0)

cap = cv2.VideoCapture(0)

detector = HandDetector(staticMode=False, maxHands=5, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

center = (int(640/2), int(480/2))
centerBoxStart = (center[0]-20, center[1]-20)
centerBoxEnd = (center[0]+20, center[1]+20)

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  
        finger = lmList1[8][0:2]


        x , y = lmList1[8][0:2]
        cv2.line(img, (x-50,y), (x+50,y), (255, 0, 0), 10, 10)
        cv2.line(img, (x,y-50), (x,y+50), (255, 0, 0), 10, 10)

        if y > 260:
            yCommand = 'd'
        elif y < 220:
            yCommand = 'u' 
        else:
            yCommand = 's'

        print(yCommand)
        # arduino.write(str.encode(yCommand))
    
    # center box plotting
    cv2.rectangle(img, centerBoxStart, centerBoxEnd, (0, 255, 0), 2, 2)
    # center dot
    cv2.line(img, center, center, (255, 0, 0), 10)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()