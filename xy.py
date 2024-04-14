from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time

arduino = serial.Serial(port = 'COM5', baudrate=9600, timeout=0)

cap = cv2.VideoCapture(1)

detector = HandDetector(staticMode=False, maxHands=5, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

center = (int(640/2), int(480/2))
centerBoxStart = (center[0]-50, center[1]-50)
centerBoxEnd = (center[0]+50, center[1]+50)

isXGood = False
isYGood = False

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  
        finger = lmList1[8][0:2]

        x , y = lmList1[8][0:2]
        cv2.line(img, (x-20,y), (x+20,y), (255, 0, 0), 3, 3)
        cv2.line(img, (x,y-20), (x,y+20), (255, 0, 0), 3, 3)

        if x > 340:
            xCommand = 'r'
        elif x < 280:
            xCommand = 'l' 
        else:
            xCommand = 's'

        if isXGood == False:
            print(xCommand)
            arduino.write(str.encode(xCommand))

        if xCommand == 's':
            isXGood = True

            if y > 260:
                yCommand = 'd'
            elif y < 220:
                yCommand = 'u' 
            else:
                yCommand = 's'

            if isYGood == False:
                print(yCommand)
                arduino.write(str.encode(yCommand))

            if yCommand == 's':
                isYGood = True

    # center box plotting
    cv2.rectangle(img, centerBoxStart, centerBoxEnd, (0, 255, 0), 10, 10)
    # center dot
    cv2.line(img, center, center, (255, 0, 0), 10)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()