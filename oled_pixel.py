# Treiber geladen von
# https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py

from machine import Pin, I2C
import ssd1306
import time
import uasyncio as asyncio

# Onboard LED 
led = Pin(35, Pin.OUT)

# Text Für Display
Text1 = "Hello World"
Text2 = "Ich Liebe Dich"

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

# Display leeren
display.fill(0)
display.show()

async def DisplayRefresh():
    while True:
        display.show()
        await asyncio.sleep_ms(100)
    


# fülle von links nach rechts
async def PixelFillLeftRight():
    asyncio.create_task(DisplayRefresh())
    for y in range(64):
        for x in range(128):
            display.pixel(x,y,1)
            await asyncio.sleep_ms(0)

asyncio.run(PixelFillLeftRight())

# fülle von links nach rechts
async def PixelFillTopButton():
    asyncio.create_task(DisplayRefresh())
    for x in range(128):
        for y in range(64):
            display.pixel(x,y,0)
            await asyncio.sleep_ms(0)

asyncio.run(PixelFillTopButton())
    
display.text("Fertig", 0, 0, 1)
display.text("Fertig", 0, 10, 0)
display.show()

# Hilfen 
# Display aktualisieren
# display.show()

# Text anzeigen
# Position in Pixel 
# display.text("Hello World!", 0, 0)

# Linie anzeigen
# von x1,y1 zu x2,y2 in 0 dunkel oder 1 hell
# display.line(1,1,10,10,1)

# Rechteck zeichnen 
#display.rect(x, y, width, height, 1)  # Rechteck zeichnen
#display.fill_rect(x, y, width, height, 1)  # Gefülltes Rechteck zeichnen

# Kreis zeichnen
# x,y ( Position der Kreismitte )
# b,h ( Radius Breite und höhe )
# 1 ( Farbe ) 
# display.ellipse(x,y,b,h,1)

# Pixel
# x = von links nach rechts
# y = oben nach unten 
# display.pixel(x,y,1)

# Bild ( habe ich noch nicht getestet 
# display.blit(bitmap,x,y,key) # Key hat was mit transparentem Hintergrund zu tun



