#include <WiFiS3.h>

const char* ssid = "Raspberry-Wifi";
const char* password = "raspberry";

const int pin = A0;         // entrée analogique pour mesurer la tension
const float Rpales = 0.085; // rayon en mètres
const int seuil = 800;      // seuil de détection

int status = 0;
unsigned long t_debut;
unsigned long t_fin;
bool detectionPrecedente = false;
float lastSpeed = 0.0;

WiFiServer server(80);

void setup() {
  Serial.begin(9600);
  //Serial.println("Serial communication OK");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    //Serial.print("test");
    delay(500);
  }
  server.begin();
}

// on a deux fentes, on calcule la vitesse sur 1 tour
void loop() {
  // Serial.println("test");
  int valeur = analogRead(pin);
  bool detectionActuelle = (valeur > seuil);

  if (detectionActuelle && !detectionPrecedente) {     // passage de pas détecté à détecté

    if (status == 0) {
      t_debut = millis();
      status = 1;  // on attend la prochaine détection
    } 
    
    else {
      t_fin = millis();
      float deltaT = (t_fin - t_debut)/1000.0; // en secondes
      float vitesse = (2 * 3.1416 * Rpales) / deltaT; // m/s
      Serial.print("Vitesse : ");
      Serial.print(3.6 * vitesse, 2);
      Serial.println(" km/h");
      status = 0; // on rénitialise pour un prochain passage
    }
  }
  detectionPrecedente = detectionActuelle;

  // envoi des mesures de vent au raspberry quand il le demande
  WiFiClient client = server.available();
  if (client) {
    String req = client.readStringUntil('\r');

    if (req.indexOf("GET /wind") >= 0) {
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: text/plain");
      client.println("Connection: close");
      client.println();
      client.print(lastSpeed, 2);
    }

    delay(1);
    client.stop();
  }
}
