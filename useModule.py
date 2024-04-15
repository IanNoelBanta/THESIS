import PersonModule
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

detector = PersonModule.PersonDetector("best.pt")

center = (int(640/2), int(480/2))
centerBoxStart = (center[0]-50, center[1]-50)
centerBoxEnd = (center[0]+50, center[1]+50)

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    list_of_objects, img = detector.detect_objects(img, draw=True, flip_type=True)

    print(len(list_of_objects))

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()