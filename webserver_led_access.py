import wlan # WLAN Verbindung aus wlan.py nutzen
import machine
import socket

# Webserver erstellen
port = "80"
webserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
webserver.bind(('', port))
webserver.listen(5) # Zahl ist die größe der Queue 
print("Webserver gestartet. Horche auf Port ",port,"...")

# LED initialisieren
led = machine.Pin(35, machine.Pin.OUT)
led_state = 0  # Aktueller Zustand der LED (0 = aus, 1 = an)

# HTML-Vorlage für die Webseite
html = """
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
<title>LED Steuerung</title>
<script>
    function getLEDStatus() {{
        fetch('/status')
            .then(response => response.text())
            .then(status => {{ document.getElementById('status').innerText = status; }})
            .catch(error => {{ document.getElementById('status').innerText = 'unbekannt'; }});
    }}
    
    function toggleLED() {{
        fetch('/toggle');
        setTimeout(getLEDStatus, 100); // LED-Status nach dem Umschalten aktualisieren
    }}
    
    function loopLEDStatus() {{
        getLEDStatus();
        setTimeout(loopLEDStatus, 2000); // LED-Status alle 2 Sekunden aktualisieren
    }}
    
    window.onload = function() {{
        loopLEDStatus(); // Beim Laden der Seite den LED-Status abrufen und aktualisieren
    }};
</script>
</head>
<body>
<h1>LED Steuerung</h1>
<p>LED: <span id="status">{status}</span></p>
<button onclick="toggleLED()">LED umschalten</button>
</body>
</html>
"""

# Funktion zum Verarbeiten von Anfragen
def handle_request(client_socket):
    request = client_socket.recv(1024) # Zahl ist die maximale größe der Anfrage ca 350 Byte braucht bereits der Header
    request = request.decode('utf-8')
    
    if "/toggle" in request:
        global led_state
        led_state = not led_state  # Sollstatus der LED umschalten
        print("	LED auf",led_state,"schalten")
        led.value(led_state)  # LED entsprechend setzen
    
    if "/status" in request:
        response = "An" if led_state else "Aus"
        print("	Status wird abgefragt LED ist",response )
        client_socket.send(response.encode('utf-8'))
        client_socket.close()
        return
    
    response = html.format(status="An" if led_state else "Aus")
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

# Webserver-Schleife
while True:
    client, addr = webserver.accept()
    print("Neue Anfrage von:", addr)
    handle_request(client)

