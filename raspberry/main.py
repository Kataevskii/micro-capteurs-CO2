from flask import Flask, jsonify
from temp import *

app = Flask(__name__)

@app.route('/api/temperature', methods=['GET'])
def temperature():
    return jsonify({'temperature': get_temperature()})

@app.route('/api/humidity', methods=['GET'])
def humidity():
    return jsonify({'humidity': get_humidity()})

@app.route('/api/all', methods=['GET'])
def all_data():
    return jsonify({
        'temperature': get_temperature(),
        'humidity': get_humidity()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Accessible from other devices on the network
