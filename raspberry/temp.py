# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-dht11-dht22-python/
# Based on Adafruit_CircuitPython_DHT Library Example

import time
import board
import adafruit_dht

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT22(board.D4)
# Uncomment for DHT11
#sensor = adafruit_dht.DHT11(board.D4)

def get_temperature():
    try:
        # Print the values to the serial port
        temperature = sensor.temperature
        humidity = sensor.humidity
        return temperature
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    except Exception as error:
        sensor.exit()
        raise error

def get_humidity():
    try:
        # Print the values to the serial port
        humidity = sensor.humidity
        return humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    except Exception as error:
        sensor.exit()
        raise error