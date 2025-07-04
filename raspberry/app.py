from flask import Flask, jsonify, render_template, send_file
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'sensors.db'


def get_temp():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value, timestamp FROM temperature ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    temperatures = [row[0] for row in rows]
    time = [row[1] for row in rows]
    return temperatures,time

def get_hum():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value, timestamp FROM humidity ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    humidities = [row[0] for row in rows]
    time = [row[1] for row in rows]
    return humidities, time

def get_pres():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value, timestamp FROM pressure ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    pressures = [row[0] for row in rows]
    time = [row[1] for row in rows]
    return pressures, time


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    temp_values, temp_times = get_temp()
    hum_values, hum_times = get_hum()
    pres_values, pres_times = get_pres()
    return jsonify({
        "temperature": {
            "values": temp_values,
            "timestamps": temp_times
        },
        "humidity": {
            "values": hum_values,
            "timestamps": hum_times
        },
        "pressure": {
            "values": pres_values,
            "timestamps": pres_times
        }
    })


@app.route('/images')
def images():
    image_folder = 'static/images'
    files = sorted(os.listdir(image_folder))
    jpg_files = [f for f in files if f.endswith('.jpg')]
    return jsonify(jpg_files)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')