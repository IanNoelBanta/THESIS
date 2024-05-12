# main.py
from tkinter import *
from PIL import Image, ImageTk
import maskcopy
import threading
import cv2
import customtkinter

def start():
    maskcopy.main()

def stop():
    print("Stopping") 
    maskcopy.stop_opencv()

def reset():
    print("Resetting")
    maskcopy.reset()

def main_loop():
    
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
        
    root = customtkinter.CTk()
    root.geometry("640x480")
    root.iconbitmap('images/ampalaya.ico')
    root.title("Control Panel")

    start_button = customtkinter.CTkButton(root, text="START", command=start, font=("Arial", 50))
    stop_button = customtkinter.CTkButton(root, text="STOP", command=stop, font=("Arial", 50))
    reset_button = customtkinter.CTkButton(root, text="RESET", command=reset, font=("Arial", 50))

    start_button.pack(expand=True, pady=10)
    stop_button.pack(expand=True, pady=10)
    reset_button.pack(expand=True, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
