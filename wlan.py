import network

def connect_to_wifi():
    ssid = "<ssid>"  # SSID deines WLAN-Netzwerks
    password = "<password>"  # WLAN-Passwort

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        pass

    print("Verbunden mit WLAN")
    print("IP-Adresse:", station.ifconfig()[0])

# WLAN-Verbindung herstellen
connect_to_wifi()
