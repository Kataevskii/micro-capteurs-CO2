import sqlite3
import threading
import time
from datetime import datetime
from dht import get_humidity, get_temperature
from bme import get_pressure
from camera import save_image

sensors = {
        'temperature': get_temperature,
        'humidity': get_humidity,
        'pressure': get_pressure
}

DB_PATH = 'sensors.db'
INTERVAL_SECONDS = 300 # 5 minutes

def data_collector():
    while True:
        timestamp = datetime.now()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for sensor_name, sensor_func in sensors.items():
                value = sensor_func()
                cursor.execute(f'''
                    INSERT INTO {sensor_name} (timestamp, value)
                    VALUES (?, ?)
                ''', (timestamp, value))
            conn.commit()
        time.sleep(INTERVAL_SECONDS)

        save_image(url="http://10.42.0.85/photo", filename=f"static/images/{timestamp}.jpg")

def init():
    thread = threading.Thread(target=data_collector)
    thread.start()