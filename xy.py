from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time

arduino = serial.Serial(port = 'COM7', timeout=0)

cap = cv2.VideoCapture(1)

detector = HandDetector(staticMode=False, maxHands=5, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

center = (int(640/2), int(480/2))
centerBoxStart = (center[0]-50, center[1]-50)
centerBoxEnd = (center[0]+50, center[1]+50)

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

        # if x > int(640 / 2):
        #     xCommand = 'r'
        # elif x < int(640 / 2):
        #     xCommand = 'l' 
        # else:
        #     xCommand = 's'

        # if y > int(480 / 2):
        #     yCommand = 'd'
        # elif y < int(480 / 2):
        #     yCommand = 'u' 
        # else:
        #     yCommand = 's'

        # command = xCommand + yCommand

        if finger[0] > centerBoxStart[0] and finger[0] < centerBoxEnd[0] and finger[1] > centerBoxStart[1] and finger[1] < centerBoxEnd[1]:
            command = "S"
            # print("TARGET LOCKED")
        else: 
            # (<, <) - Top Left
            if finger[0] < center[0] and finger[1] < center[1]:
                XdistanceToCenter = center[0] - finger[0]
                YdistanceToCenter = center[1] - finger[1]
                command = "TL"
                print(f"TOP LEFT - {XdistanceToCenter}, {YdistanceToCenter}")

            # (>, <) - Top Right
            elif finger[0] > center[0] and finger[1] < center[1]:
                XdistanceToCenter = finger[0] - center[0]
                YdistanceToCenter = center[1] - finger[1]
                command = "TR"
                print(f"TOP RIGHT - {XdistanceToCenter}, {YdistanceToCenter}")
            
            # (<, >) - Bottom Left
            elif finger[0] < center[0] and finger[1] > center[1]:
                XdistanceToCenter = center[0] - finger[0]
                YdistanceToCenter = finger[1] - center[1]
                command = "BL"
                print(f"BOTTOM LEFT - {XdistanceToCenter}, {YdistanceToCenter}")

            # (>, >) - Bottom Right
            elif finger[0] > center[0] and finger[1] > center[1]:
                XdistanceToCenter = finger[0] - center[0]
                YdistanceToCenter = finger[1] - center[1]
                command = "BR"
                print(f"BOTTOM RIGHT - {XdistanceToCenter}, {YdistanceToCenter}")

        # print(command)
        arduino.write(str.encode(command))
    
    # center box plotting
    cv2.rectangle(img, centerBoxStart, centerBoxEnd, (0, 255, 0), 10, 10)
    # center dot
    cv2.line(img, center, center, (255, 0, 0), 10)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()