from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time

cap = cv2.VideoCapture(0)

detector = HandDetector(staticMode=False, maxHands=5, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

center = (int(640/2), int(480/2))
centerBoxStart = (center[0]-50, center[1]-50)
centerBoxEnd = (center[0]+50, center[1]+50)

# arduino = serial.Serial(port = 'COM7', timeout=0)

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  
        hand1Number = (detector.fingersUp(hand1)).count(1)
        
        if hand1Number == 1:
            print("Hand1 is showing 1 finger")
            
        if len(hands) == 2:
            hand2 = hands[1]
            hand2Number = (detector.fingersUp(hand2)).count(1)
            
            if hand2Number == 1:
                print("Hand2 is showing 1 finger")
        
        x , y = lmList1[8][0:2]
        finger = lmList1[8][0:2]

                # target locked
        if finger[0] > centerBoxStart[0] and finger[0] < centerBoxEnd[0] and finger[1] > centerBoxStart[1] and finger[1] < centerBoxEnd[1]:
            print("TARGET LOCKED")
        else: 
            # (<, <) - Top Left
            if finger[0] < center[0] and finger[1] < center[1]:
                XdistanceToCenter = center[0] - finger[0]
                YdistanceToCenter = center[1] - finger[1]
                # print(f"TOP LEFT - {XdistanceToCenter}, {YdistanceToCenter}")

            # (>, <) - Top Right
            if finger[0] > center[0] and finger[1] < center[1]:
                XdistanceToCenter = finger[0] - center[0]
                YdistanceToCenter = center[1] - finger[1]
                # print(f"TOP RIGHT - {XdistanceToCenter}, {YdistanceToCenter}")
            
            # (<, >) - Bottom Left
            if finger[0] < center[0] and finger[1] > center[1]:
                XdistanceToCenter = center[0] - finger[0]
                YdistanceToCenter = finger[1] - center[1]
                # print(f"BOTTOM LEFT - {XdistanceToCenter}, {YdistanceToCenter}")

            # (>, >) - Bottom Right
            if finger[0] > center[0] and finger[1] > center[1]:
                XdistanceToCenter = finger[0] - center[0]
                YdistanceToCenter = finger[1] - center[1]
                # print(f"BOTTOM RIGHT - {XdistanceToCenter}, {YdistanceToCenter}")



        # finger plotting
        cv2.line(img, (x-50,y), (x+50,y), (0, 0, 255), 10, 10)
        cv2.line(img, (x,y-50), (x,y+50), (0, 0, 255), 10, 10)

    # center box plotting
    cv2.rectangle(img, centerBoxStart, centerBoxEnd, (0, 255, 0), 10, 10)
    # center dot
    cv2.line(img, center, center, (255, 0, 0), 10)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()