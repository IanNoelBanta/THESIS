from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import pyfirmata
import time

cap = cv2.VideoCapture(0)

# arduino = serial.Serial('COM6', baudrate=9600, timeout=0)
# arduino = pyfirmata.Arduino("COM4")
# servo = arduino.get_pin('d:8:s')

detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, draw=True, flipType=False)

    if hands:
        # arduino.write(b'r')
        hand1 = hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        fingers1 = detector.fingersUp(hand1)
        # print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

        # Calculate distance between specific landmarks on the first hand and draw it on the image
        # length, info, img = detector.findDistance(lmList1[4][0:2], lmList1[20][0:2], img, color=(255, 0, 255),
        #                                           scale=10)

        x , y = lmList1[8][0:2]
        cv2.line(img, (x-100,y), (x+100,y), (255, 0, 0), 50, 50)
        cv2.line(img, (x,y-100), (x,y+100), (255, 0, 0), 50, 50)

        print(f'X = {x}, Y = {y}')

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            fingers2 = detector.fingersUp(hand2)
            # print(f'H2 = {fingers2.count(1)}', end=" ")

            length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
                                                      scale=10)

        print(" ")  # New line for better readability of the printed output
        
    cv2.line(img, (0, 240), (640, 240), (255, 0, 0), 5, 5) # horizontal line
    cv2.line(img, (320, 0), (320, 480), (255, 0, 0), 5, 5) # vertical line

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        # arduino.close()
        break

cap.release()
cv2.destroyAllWindows()