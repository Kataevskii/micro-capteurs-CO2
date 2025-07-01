import tkinter as tk
from tkinter import ttk
import time
import board
import adafruit_dht

# Initialiser le capteur DHT22 sur GPIO4
sensor = adafruit_dht.DHT22(board.D4)
# Pour DHT11, décommente la ligne suivante
# sensor = adafruit_dht.DHT11(board.D4)

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

def update_data():
    temp_c, hum = read_sensor()
    if temp_c is not None and hum is not None:
        temp_label.config(text=f"Température : {temp_c:.1f} °C")
        hum_label.config(text=f"Humidité : {hum:.1f} %")
    else:
        temp_label.config(text="Erreur de lecture")
        hum_label.config(text="")

    # Planifier une nouvelle lecture toutes les 2 secondes
    root.after(2000, update_data)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Température & Humidité - DHT22")

# Style (facultatif, pour un rendu plus moderne)
style = ttk.Style()
style.configure("TLabel", font=("Arial", 16))

frame = ttk.Frame(root, padding=20)
frame.pack()

temp_label = ttk.Label(frame, text="Température : -- °C")
temp_label.pack(pady=10)

hum_label = ttk.Label(frame, text="Humidité : -- %")
hum_label.pack(pady=10)

# Lancer la première mise à jour
update_data()

# Boucle principale
root.mainloop()