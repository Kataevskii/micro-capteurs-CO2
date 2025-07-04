import serial
import time

# Ouvre la liaison série sur /dev/serial0 à 9600 bauds
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

# Commande de lecture CO2 (standard MH-Z16)
read_cmd = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])

def read_co2():
    ser.write(read_cmd)
    time.sleep(0.1)
    response = ser.read(9)

    if len(response) != 9:
        print("Réponse incomplète")
        return None

    if response[0] != 0xFF or response[1] != 0x86:
        print("Trame invalide")
        return None

    checksum = (0xFF - (sum(response[1:8]) % 256) + 1) & 0xFF
    if response[8] != checksum:
        print("Checksum incorrect")
        return None

    co2 = response[2] * 256 + response[3]
    temperature = response[4] - 40

    return co2, temperature

# Boucle de lecture continue
while True:
    result = read_co2()
    if result:
        co2, temp = result
        print(f"CO2: {co2} ppm | Température: {temp} °C")
    else:
        print("Lecture échouée")
    time.sleep(2)