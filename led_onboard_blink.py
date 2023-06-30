import machine
import time

# Heltec Wifi_Kit_32_v3 = 35 
led = machine.Pin(35, machine.Pin.OUT)

while True:
    led.on()
    # led.value(1)
    print("on")
    time.sleep(0.5)
    
    led.off()
    # led.value(0)
    print("off")
    time.sleep(0.5)
