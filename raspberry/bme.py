import time
import smbus2
import bme280

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

def get_pressure():
    try:
        # Read sensor data
        data = bme280.sample(bus, address, calibration_params)

        # Extract pressure
        pressure = data.pressure
        return pressure

    except Exception as e:
        print(e)
        return None