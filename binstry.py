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

isXGood = False
isYGood = False

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        for handIndex, hand in enumerate(hands):
            lmList = hand["lmList"]  
            handNumber = (detector.fingersUp(hand)).count(1)
                                                        
            if handIndex == 0: 
                if handNumber >= 1:  
                    
                    cv2.putText(img, f"{handIndex+1}: {handNumber} finger(s)", (lmList[8][0], lmList[8][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                    
                    handFingerX, handFingerY = lmList[8][0:2]
                    
                    # finger plotting
                    cv2.line(img , (handFingerX-50,handFingerY), (handFingerX+50,handFingerY), (0, 0, 255), 3, 3)
                    cv2.line(img, (handFingerX,handFingerY-50), (handFingerX,handFingerY+50), (0, 0, 255), 3, 3)

                   
                    x = handFingerX
                    y = handFingerY

                    if x > centerBoxEnd[0]:
                        xCommand = 'r'
                    elif x < centerBoxStart[0]:
                        xCommand = 'l' 
                    else:
                        xCommand = 's'

                    if isXGood == False:
                        print(f"Hand {handIndex+1}: X-Direction Command: {xCommand}")
                        # arduino.write(str.encode(xCommand))

                    if xCommand == 's':
                        isXGood = True

                        if y > centerBoxEnd[1]:
                            yCommand = 'd'
                        elif y < centerBoxStart[1]:
                            yCommand = 'u' 
                        else:
                            yCommand = 's'

                        if isYGood == False:
                            print(f"Hand {handIndex+1}: Y-Direction Command: {yCommand}")
                            # arduino.write(str.encode(yCommand))

                        if yCommand == 's':
                            isYGood = True
            else:
                # Reset flags for next iteration for other hands
                isXGood = False
                isYGood = False

    # center box plotting
    cv2.rectangle(img, centerBoxStart, centerBoxEnd, (0, 255, 0), 10, 10)
    # center dot
    cv2.line(img, center, center, (255, 0, 0), 10)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
