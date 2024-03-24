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
            hand1FingerX, hand1FingerY = lmList1[8][0:2]
            
            # finger plotting
            cv2.line(img, (hand1FingerX-50,hand1FingerY), (hand1FingerX+50,hand1FingerY), (0, 0, 255), 10, 10)
            cv2.line(img, (hand1FingerX,hand1FingerY-50), (hand1FingerX,hand1FingerY+50), (0, 0, 255), 10, 10)

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  
            hand2Number = (detector.fingersUp(hand2)).count(1)
            
            if hand2Number == 1:
                hand2FingerX, hand2FingerY = lmList2[8][0:2]
                
                # finger plotting
                cv2.line(img, (hand2FingerX-50,hand2FingerY), (hand2FingerX+50,hand2FingerY), (0, 0, 255), 10, 10)
                cv2.line(img, (hand2FingerX,hand2FingerY-50), (hand2FingerX,hand2FingerY+50), (0, 0, 255), 10, 10)



    # center box plotting
    cv2.rectangle(img, centerBoxStart, centerBoxEnd, (0, 255, 0), 10, 10)
    # center dot
    cv2.line(img, center, center, (255, 0, 0), 10)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()