# main.py
from tkinter import *
from PIL import Image, ImageTk
import maskcopy
import threading
import cv2

def start():
    maskcopy.main()

def stop():
    print("Stopping") 
    maskcopy.stop_opencv()
    
def main_loop():
    root = Tk()
    root.geometry("720x640")
    root.title("AMPALAYAAAAAAAAAAAAAAWAAAA")

    start_button = Button(
        root,
        text="START",
        command=start 
    )
    stop_button = Button(
        root,
        text="STOP",
        command=stop 
    )

    start_button.pack()
    stop_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
