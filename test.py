from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time

# arduino = serial.Serial(port = 'COM11', timeout=0)
# time.sleep(2)

cap = cv2.VideoCapture(0)

detector = HandDetector(staticMode=False, maxHands=5, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

# last_command = 's'

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, draw=True, flipType=False)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  

        x , y = lmList1[8][0:2]
        cv2.line(img, (x-50,y), (x+50,y), (255, 0, 0), 10, 10)
        cv2.line(img, (x,y-50), (x,y+50), (255, 0, 0), 10, 10)

    #     if x > int(640 / 2):
    #         new_command = 'r'
    #     elif x < int(640 / 2):
    #         new_command = 'l'
    # else:
    #     new_command = 's'

    # print(new_command)
    # arduino.write(str.encode(new_command))


    
    cv2.line(img, (int(640/2), int(480/2) - 50), (int(640/2), int(480/2) + 50), (255, 0, 0), 10)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()