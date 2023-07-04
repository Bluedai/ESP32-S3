import network
from secrets import WLAN_ssid, WLAN_password

station = ""

def connect_to_wifi():
    global station

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(WLAN_ssid, WLAN_password)

    while not station.isconnected():
        pass

    print("Verbunden mit WLAN")
    print("IP-Adresse:", station.ifconfig()[0])

def disconnect():
    global station
    station.disconnect()


    # Gittest
