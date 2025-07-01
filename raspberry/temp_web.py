from flask import Flask, jsonify, render_template
import board
import adafruit_dht
import threading
import time

app = Flask(__name__)
sensor = adafruit_dht.DHT22(board.D4)

# Listes pour stocker les valeurs
temp_values = []
hum_values = []
timestamps = []

def read_sensor():
    try:
        temp_c = sensor.temperature
        hum = sensor.humidity
        return temp_c, hum
    except RuntimeError as error:
        print("RuntimeError:", error.args[0])
        return None, None
    except Exception as error:
        sensor.exit()
        raise error

def sensor_loop():
    while True:
        temp, hum = read_sensor()
        now = time.strftime("%H:%M:%S")
        if temp is not None and hum is not None:
            temp_values.append(temp)
            hum_values.append(hum)
            timestamps.append(now)
            # Garde seulement les 30 dernières valeurs
            if len(temp_values) > 5000:
                temp_values.pop(0)
                hum_values.pop(0)
                timestamps.pop(0)
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify({
        'timestamps': timestamps,
        'temperature': temp_values,
        'humidity': hum_values
    })

if __name__ == '__main__':
    t = threading.Thread(target=sensor_loop, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000)