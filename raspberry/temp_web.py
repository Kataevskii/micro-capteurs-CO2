from flask import Flask, jsonify, render_template
import board
import adafruit_dht

app = Flask(__name__)

sensor = adafruit_dht.DHT22(board.D4)

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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    temp, hum = read_sensor()
    return jsonify({'temperature': temp, 'humidity': hum})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)