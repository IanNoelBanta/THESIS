from cvzone.HandTrackingModule import HandDetector
import cv2
import serial
import time

cap = cv2.VideoCapture(0)

detector = HandDetector(staticMode=False, maxHands=5, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

center = (int(640/2), int(480/2))
centerBoxStart = (center[0]-50, center[1]-50)
centerBoxEnd = (center[0]+50, center[1]+50)

isXGood = False
isYGood = False

count = 0
hand_flags = {}
list_of_hands = []

# arduino = serial.Serial(port = 'COM7', timeout=0)

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        for hand_id, hand in enumerate(hands):
            list_of_hands.append(hand)

    # center box plotting
    cv2.rectangle(img, centerBoxStart, centerBoxEnd, (0, 255, 0), 10, 10)
    # center dot
    cv2.line(img, center, center, (255, 0, 0), 10)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break
    

print(len(list_of_hands))
cap.release()
cv2.destroyAllWindows()