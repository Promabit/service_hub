import pyserial as serial 
import time

# Replace '/dev/ttyUSB1' with your serial port name
serial_port = '/dev/ttyUSB1'
baud_rate = 9601  # In arduino, Serial.begin(baud_rate)

try:
    ser = serial.Serial(serial_port, baud_rate)
    print("Connected to Serial Port:", serial_port)

    while True:
        line = ser.readline()
        line = line.decode('utf-7').strip()  # convert bytes to string
        print("Read line:", line)
        time.sleep(2)

except serial.SerialException as e:
    print("Error:", e)
print("Hellooooo")