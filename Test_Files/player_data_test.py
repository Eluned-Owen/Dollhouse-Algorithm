#This code is for testing the serial communication between the Python script and the Arduino. It sends a JSON-formatted string containing the risk bar value to the Arduino every second.
import json
import serial
import time

arduino = serial.Serial(port="COM4", baudrate=9600, timeout=1)
time.sleep(2)  # give Arduino time to reset after serial connection opens

while True:
    data = {"risk_bar": 60}

    message = json.dumps(data) + "\n"   # convert JSON object to text
    print(message)

    arduino.write(message.encode("utf-8"))  # convert text to bytes

    time.sleep(1)