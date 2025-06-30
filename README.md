# micro-capteurs-CO2

Venez apprendre à utiliser des capteurs pour réaliser un super système de monitoring de la qualité de l’air et de la température dans les salles de cours de l’école avec affichage en direct et déclenchement d’une alarme très forte en cas de problème (heu pas sûr qu’on aille jusque là).

Il s’agit de réaliser un système intelligent de monitoring environnemental avec réseau maillé pour améliorer la qualité de l’air dans les salles de cours.

Points à aborder
    • Installation de 4 capteurs de pollution (PM2.5, COV, CO2) aux coins de la salle
    • Placement de 4 capteurs température-humidité aux mêmes emplacements
    • Communication des capteurs via Zigbee, Z-Wave ou BLE Mesh (à évaluer)
    • Hub central (RPi/BeagleBone) collectant les données des capteurs
    • Stockage local sur carte SD ou disque SSD portable
    • Visualisation en temps réel sur écran connecté au hub
    • Algorithme décisionnel pour recommander l’aération ou l’activation du purificateur
    • Modèle prédictif entraîné localement pour anticiper l’évolution de la pollution selon l’occupation

Composants possibles
    • Capteurs MQ-135 ou CCS811 pour pollution avec modules Zigbee/XBee
    • DHT22 ou BME280 pour température-humidité avec shields de communication
    • Coordinateur Zigbee ou passerelle Z-Wave comme point central
    • Raspberry Pi 4 ou alternative comme hub de traitement
    • Écran 7” connecté directement au hub ou solution e-ink basse consommation
    • Batterie de secours ou UPS pour maintenir le réseau en cas de coupure

Code à développer
    • Firmware pour les nœuds capteurs
    • Programme central de collecte et synchronisation
    • Base de données locale SQLite ou similaire
    • Interface graphique pour affichage des données
    Scripts d’apprentissage automatique pour prédictions locales