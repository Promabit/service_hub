import serial
import time
from serial.serialutil import SerialException

# CAS PR-II device info
device_info = {
    "name": "CAS PR-II",
    "baudRate": 9600,
    "dataBits": 8,
    "stopBits": 1,
    "parity": serial.PARITY_NONE,
}

BYTE_INIT_READ = b"\x05"
BYTE_DEVICE_CONTROL = b"\x11"
BYTE_ACKNOWLEDGE = b"\x06"
BYTE_END_OF_TRANSMISSION = b"\x04"
BYTE_START_OF_MESSAGE = b"\x02"
BYTE_END_OF_MESSAGE = b"\x03"



def read_scale_data(port_name):
    try:
        # Set up the serial connection
        with serial.Serial(port_name, baudrate=device_info['baudRate'], bytesize=device_info['dataBits'],
                           stopbits=device_info['stopBits'], parity=device_info['parity'], timeout=2) as port:
            
            if port.writable():
                # Send the initial command to the scale
                port.write(BYTE_INIT_READ)
                return_data = b""

                while True:
                    try:
                        data = port.read()
                        if BYTE_ACKNOWLEDGE in data:
                            port.write(BYTE_DEVICE_CONTROL)
                        else:
                            return_data += data

                        # Check for end of message
                        if BYTE_END_OF_MESSAGE in return_data or return_data[-1:] == BYTE_END_OF_MESSAGE:
                            break
                    except SerialException as e:
                        print("Error reading from port:", e)
                        break

                # Process the returned data
                if return_data:
                    data_string = return_data.decode('ascii')

                    start_index = return_data.index(BYTE_START_OF_MESSAGE)
                    end_index = return_data.index(BYTE_END_OF_MESSAGE)

                    if start_index != -1 and end_index != -1:
                        stable = data_string[start_index + 1] == "S"  # S for stable, U for unstable
                        weight_data = data_string[start_index + 3:end_index - 3]
                        weight_number = float(weight_data.strip())
                        return weight_number, stable
                return None, None

            else:
                raise SerialException("Port is not writable. Cannot request digital scale data.")
    except SerialException as e:
        print("Serial port error:", e)

# Example usage
port_name = '/dev/ttyUSB0'  # Replace with your actual serial port
weight, is_stable = read_scale_data(port_name)
print("Result:", weight, is_stable)
