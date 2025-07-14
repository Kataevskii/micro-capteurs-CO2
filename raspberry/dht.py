# Based on Adafruit_CircuitPython_DHT Library Example

import board
import adafruit_dht

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT22(board.D4)

def get_temperature():
    try:
        # Print the values to the serial port
        return sensor.temperature
    except (RuntimeError, Exception) as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error)
        return None

def get_humidity():
    try:
        # Print the values to the serial port
        return sensor.humidity
    except (RuntimeError, Exception) as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error)
        return None