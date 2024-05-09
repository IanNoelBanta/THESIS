import cv2
from tkinter import *
from PIL import Image, ImageTk
import time
import serial
from ultralytics import YOLO

root = Tk()
root.geometry("1920x1080")
root.title("AMPALAYAAAAAAAAAAAAAAWAAAA")

# global model, cap, CAM_X_CENTER, CAM_Y_CENTER, TOLERANCE, CAM_LEFT_TOLERANCE, CAM_RIGHT_TOLERANCE, CAM_TOP_TOLERANCE, CAM_BOTTOM_TOLERANCE, FONT, FONTSCL, COLOR, THICKNESS, xCommand, yCommand, isXGood, isYGood, reverse, goRightSent, goLeftSent, mask

model = YOLO("v8-500.pt")
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

CAM_X_CENTER = 320
CAM_Y_CENTER = 240
TOLERANCE = 5
CAM_LEFT_TOLERANCE = CAM_X_CENTER - TOLERANCE
CAM_RIGHT_TOLERANCE = CAM_X_CENTER + TOLERANCE
CAM_TOP_TOLERANCE = CAM_Y_CENTER - TOLERANCE
CAM_BOTTOM_TOLERANCE = CAM_Y_CENTER + TOLERANCE

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONTSCL = 1
COLOR = (255, 0, 0) 
THICKNESS = 2

xCommand = ""
yCommand = ""
isXGood = False
isYGood = False
reverse = False
goRightSent = 0
goLeftSent = 0

mask = cv2.imread("mask.png")

cam_on = False


def start(model, cap, CAM_X_CENTER, CAM_Y_CENTER, TOLERANCE, CAM_LEFT_TOLERANCE, CAM_RIGHT_TOLERANCE, CAM_TOP_TOLERANCE, CAM_BOTTOM_TOLERANCE, FONT, FONTSCL, COLOR, THICKNESS, xCommand, yCommand, isXGood, isYGood, reverse, goRightSent, goLeftSent, mask):
    if cam_on:
        success, frame = cap.read()  
        frame = cv2.bitwise_and(frame, mask)

        if success:
            results = model.track(frame, verbose=False, classes=[1], stream_buffer=True, max_det=1, persist=True, tracker="botsort.yaml")

            if results[0]:
                goRightSent = 0
                cv2.putText(frame, f"DETECTED:{len(results[0])}", (0, 50), FONT, FONTSCL, COLOR, THICKNESS, cv2.LINE_AA)
                frame = results[0].plot() # plot lahat ng detections
                targetX1 = int(results[0].boxes.xyxy.cpu().numpy()[0][0])
                targetY1 = int(results[0].boxes.xyxy.cpu().numpy()[0][1])
                targetX2 = int(results[0].boxes.xyxy.cpu().numpy()[0][2])
                targetY2 = int(results[0].boxes.xyxy.cpu().numpy()[0][3])

                targetY1Offset = targetY1 - 0

                targetXCenter, targetYCenter = int((targetX1 + targetX2) / 2), int((targetY1 + targetY2) / 2)

                targetCrosshairVerticalStart, targetCrosshairVerticalEnd = (targetXCenter, targetYCenter - 10), (targetXCenter, targetYCenter + 10) 
                targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd = (targetXCenter - 10, targetYCenter), (targetXCenter + 10, targetYCenter)

                cv2.line(frame, targetCrosshairVerticalStart, targetCrosshairVerticalEnd, (0, 0, 255), 3) # crosshair vertical line
                cv2.line(frame, targetCrosshairHorizontalStart, targetCrosshairHorizontalEnd, (0, 0, 255), 3) # crosshair horizontal line

                if targetXCenter > CAM_RIGHT_TOLERANCE:
                    xCommand = 'l'
                elif targetXCenter < CAM_LEFT_TOLERANCE:
                    xCommand = 'r' 
                else:
                    xCommand = 'x'

                if isXGood == False:
                    print(xCommand)
                    # arduino.write(str.encode(xCommand))

                if xCommand == 'x':
                    isXGood = True

                    if targetYCenter > CAM_BOTTOM_TOLERANCE:
                        yCommand = 'd'
                    elif targetYCenter < CAM_TOP_TOLERANCE:
                        yCommand = 'u'
                    else:
                        yCommand = 'y'

                    if isYGood == False:
                        print(yCommand)
                        # arduino.write(str.encode(yCommand))

                    if yCommand == 'y':
                        isYGood = True
                        print('z')
                        # arduino.write(str.encode('z'))

                        time.sleep(10)
                        # # reset all for next target
                        print("RESET")
                        isXGood = False
                        isYGood = False
            else:
                if isXGood == False and goRightSent == 0:
                    print("NO DETECTION -> GO RIGHT")
                    # arduino.write(str.encode('r'))
                    goRightSent += 1

            cv2.line(frame, (CAM_LEFT_TOLERANCE, 0), (CAM_LEFT_TOLERANCE, 480), (255, 0, 0), 3) # left vertical line
            cv2.line(frame, (CAM_RIGHT_TOLERANCE, 0), (CAM_RIGHT_TOLERANCE, 480), (255, 0, 0), 3) # right vertical line
            cv2.line(frame, (0, CAM_TOP_TOLERANCE), (640, CAM_TOP_TOLERANCE), (0, 0, 255), 3) # top horizontal line
            cv2.line(frame, (0, CAM_BOTTOM_TOLERANCE), (640, CAM_BOTTOM_TOLERANCE), (0, 0, 255), 3) # bottom horizontal line
            # cv2.imshow("Real-time Object Tracking", frame)
            
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)        
            vid_lbl.imgtk = imgtk    
            vid_lbl.configure(image=imgtk)    

            vid_lbl.after(10, start)


def start_tracking():
    global cam_on
    print("Starting tracking")
    cam_on = True
    start(model=model, cap=cap, CAM_X_CENTER=CAM_X_CENTER, CAM_Y_CENTER=CAM_Y_CENTER, TOLERANCE=TOLERANCE, CAM_LEFT_TOLERANCE=CAM_LEFT_TOLERANCE, CAM_RIGHT_TOLERANCE=CAM_RIGHT_TOLERANCE, CAM_TOP_TOLERANCE=CAM_TOP_TOLERANCE, CAM_BOTTOM_TOLERANCE=CAM_BOTTOM_TOLERANCE, FONT=FONT, FONTSCL=FONTSCL, COLOR=COLOR, THICKNESS=THICKNESS, xCommand=xCommand, yCommand=yCommand, isXGood=isXGood, isYGood=isYGood, reverse=reverse, goRightSent=goRightSent, goLeftSent=goLeftSent, mask=mask)

def stop_tracking():
    global cam_on
    print("Stop Tracking")
    cam_on = False

    if cap:
        cap.release()
        # cv2.destroyAllWindows()
        vid_lbl.config(image="") 

start_button = Button(
    root,
    text="START",
    command=start_tracking 
)

stop_button = Button(
    root,
    text="STOP",
    command=stop_tracking 
)

vid_lbl = Label(root)

start_button.pack()
stop_button.pack()
vid_lbl.pack()

if __name__ == "__main__":
    root.mainloop()