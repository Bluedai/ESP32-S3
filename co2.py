# Dieses Skript fragt einen lokalen Grafana Server ab und gibt die letzten 15 Minuten CO2 Werte auf dem Display als Diagramm aus

import wlan
import time
import ntptime
from machine import Pin, I2C
import urequests
import ssd1306
import json

# Display reseten 
reset = Pin(21, Pin.OUT)
reset.off()
time.sleep(0.2) 
reset.on()
time.sleep(0.2)

# Display inizialisieren
i2c = I2C(1, scl=Pin(18), sda=Pin(17), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)

# WLAN Verbinden
display.text("Verbinde WLAN...",0,0,1)
display.show()
wlan.connect_to_wifi()
display.text("{}".format(wlan.station.ifconfig()[0]),0,10,1)
display.show()

# Rufe die aktuelle Zeit ab
ntptime.settime()
current_time = time.localtime()

# Unixtime seit 1970 in Millisekunden ermitteln UTC + 2 Stunden
def unixtime_ermitteln(Minuten):
    # Aktuelle Unixtime
    now = time.time() + 7200
    now = int(now)
    now = (now + 946677638) * 1000  

    # Unixtime vor X Minuten ermitteln 
    before = time.time() - (Minuten * 60) + 7200
    before = int(before)
    before = (before + 946677638) * 1000

    return now,before

# Grafana API abfragen
def grafana_read(before,now):
    url = 'http://192.168.178.32:2090/api/ds/query'
    headers = {}
    data = {
        'queries': [
            {
                'refId': 'A',
                'datasource': {
                    'uid': 'ud0tJxxMk',
                    'type': 'mysql'
                },
                'rawSql': 'SELECT\n  $__timeGroupAlias(Zeit,10s),\n  avg(Wert) AS "Co2"\nFROM Werte\nWHERE\n  $__timeFilter(Zeit) AND\n  SensorID = 39\nGROUP BY 1\nORDER BY $__timeGroup(Zeit,10s)',
                'format': 'time_series',
            }
        ],
        'from': str(before),
        'to': str(now)
    }

    response = urequests.post(url,headers=headers, json=data)
    response.encoding = 'utf-8'
    data = json.loads(response.content)
    data_array = data['results']['A']['frames'][0]['data']['values']
    return data_array

def daten_darstellen(data_array):
    display.fill(0)
    xpos = 10
    ypos = 63
    lastco2 = 0
    # Schleife mit allen Werten
    for time, co2 in zip(data_array[0], data_array[1]):
        lastypos=ypos
        newypos=63-(63/1600*(int(co2)-400))
        ypos=int(round(newypos,0))
        lastxpos=xpos
        xpos=xpos+1
        display.line(lastxpos,lastypos,xpos,ypos,1)
        lastco2=co2

    display.text("Wohnzimmer",30,0,1)
    display.text("co2 = {}".format(lastco2),20,10,1)
    display.show()

while True:
    # Zeiten ermitteln 
    now,before = unixtime_ermitteln(150)

    # API abfragen
    data_array = grafana_read(before,now)

    # Daten darstellen
    daten_darstellen(data_array)
    
    # Warten
    time.sleep(30)

