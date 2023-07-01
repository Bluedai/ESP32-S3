# Treiber geladen von
# https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py

from machine import Pin, I2C
import ssd1306
import time

# Onboard LED 
led = Pin(35, Pin.OUT)

# Text Für Display
line1 = "Hello"
line2 = "World"

# Je nach Display muss der Resetpin auf 1 oder 0 stehen 
reset = Pin(21, Pin.OUT)
reset.on()

# Onboard LED beim warten leuchten lassen 
led.on()
time.sleep(0.1)
led.off()

# Display inizialisieren 
i2c = I2C(1, scl=Pin(18), sda=Pin(17), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# 2 Zeilen schreiben ( ohne anzuzeigen ) 
display.fill(0)
display.text(line1,0,0)
display.text(line2,0,10)

# Display aktualisieren
display.show()

