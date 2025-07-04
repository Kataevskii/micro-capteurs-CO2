import sqlite3
import threading
import time
from datetime import datetime
from dht import get_humidity, get_temperature
from bme import get_pressure
from wind import get_wind
from camera import save_image

sensors = {
        'temperature': get_temperature,
        'humidity': get_humidity,
        'pressure': get_pressure,
        'wind': get_wind
}

DB_PATH = 'sensors.db'
INTERVAL_SECONDS = 300 # 5 minutes

def data_collector():
    while True:
        timestamp = datetime.now()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for sensor_name, sensor_func in sensors.items():
                try:
                    value = sensor_func()
                    if value is not None:
                        cursor.execute(f'''
                            INSERT INTO {sensor_name} (timestamp, value)
                            VALUES (?, ?)
                        ''', (timestamp, value))
                except Exception as e:
                    print(f"Error reading {sensor_name}: {e}")
            conn.commit()

        save_image(url="http://10.42.0.85/photo", filename=f"static/images/{timestamp}.jpg")
        time.sleep(INTERVAL_SECONDS)


def init():
    thread = threading.Thread(target=data_collector)
    thread.start()