"""
Photoacoustic Trigger for current driver and voltage monitoring display.

Eduardo Santos, David Ariza, Samuel Perez
December 2025
"""

from machine import Pin, PWM, ADC, I2C
import time
import neopixel
import math

# --- 1. Configuración del PWM (Pulsos 5kHz en GP15) ---
pwm_pulse = PWM(Pin(15))
pwm_pulse.freq(5000)
pwm_pulse.duty_u16(32768) 

# --- 2. Configuración del ADC (GP27) ---
adc_pin = ADC(27)
conversion_factor = 3.3 / 65535

# --- 3. Configuración del LED RGB (WS2812 en GP16) ---
# El RP2040-Zero tiene el neopixel en el GP16
NUM_LEDS = 1
np = neopixel.NeoPixel(Pin(16), NUM_LEDS)

# --- 4. Configuración del Display HT16K33 (I2C) ---
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
DISPLAY_ADDR = 0x70
DIGITS = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]

def init_display():
    try:
        i2c.writeto(DISPLAY_ADDR, b'\x21') 
        i2c.writeto(DISPLAY_ADDR, b'\x81') 
        i2c.writeto(DISPLAY_ADDR, b'\xE0') 
    except OSError:
        pass # Ignorar si no está conectado para probar el LED

def show_value(number):
    num = int(min(max(number, 0), 9999))
    str_num = "{:04d}".format(num)
    buffer = bytearray([0x00])
    for char in str_num:
        buffer.append(DIGITS[int(char)])
        buffer.append(0x00)
    try:
        i2c.writeto(DISPLAY_ADDR, buffer)
    except OSError:
        pass

# --- Funciones para Efectos Visuales ---
def update_status_led(voltage_val):
    """
    Cambia el color basado en el voltaje (0.0v a 3.3v).
    Usa una función seno para crear un efecto de 'respiración' en la intensidad.
    """
    # Factor de respiración (breathing effect)
    # Usa el tiempo actual para oscilar la intensidad entre 0.2 y 1.0
    intensity = (math.sin(time.ticks_ms() / 500) + 1) / 2 * 0.8 + 0.2
    
    # Mapeo de color según voltaje
    if voltage_val < 1.0:
        # Zona Seg