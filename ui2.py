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

def reset():
    print("Resetting")
    maskcopy.reset()

def main_loop():
    root = Tk()
    root.geometry("640x480")
    root.title("Control Panel")

    start_button = Button(root, text="START", command=start, font=("Arial", 50))
    stop_button = Button(root, text="STOP", command=stop, font=("Arial", 50))
    reset_button = Button(root, text="RESET", command=reset, font=("Arial", 50))

    start_button.pack(expand=True, pady=10)
    stop_button.pack(expand=True, pady=10)
    reset_button.pack(expand=True, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
