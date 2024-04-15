import serial
import keyboard

# Replace 'COM3' with the appropriate serial port
arduino = serial.Serial('COM3', 9600, timeout=1)

while True:
    if keyboard.is_pressed('left'):
        arduino.write(b'l')  # Send 'l' for left
        print("Left")
    elif keyboard.is_pressed('right'):
        arduino.write(b'r')  # Send 'r' for right
        print("Right")
    else:
        arduino.write(b's')
        print("no key pressed")
