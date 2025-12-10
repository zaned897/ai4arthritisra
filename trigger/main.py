"""
Photoacoustic Trigger for current driver and voltage monitoring display.

Eduardo Santos, David Ariza, Samuel Perez
December 2025
"""

from machine import Pin, PWM, ADC, I2C
import time

pwm_pulse = PWM(Pin(15))
pwm_pulse.freq(5000)
pwm_pulse.duty_u16(32768) 

adc_pin = ADC(27)
conversion_factor = 3.3 / 65535

# TODO: Look for an already built library for HT16K33 7-segment display
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
DISPLAY_ADDR = 0x70

def init_display():
    try:
        i2c.writeto(DISPLAY_ADDR, b'\x21')
        i2c.writeto(DISPLAY_ADDR, b'\x81')
        i2c.writeto(DISPLAY_ADDR, b'\xE0')
    except OSError:
        print("Error: Display no detectado en 0x70")

DIGITS = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]

def show_value(number):
    num = int(min(max(number, 0), 9999))
    str_num = "{:04d}".format(num)
    
    buffer = bytearray([0x00])
    
    for char in str_num:
        digit_bits = DIGITS[int(char)]
        buffer.append(digit_bits)
        buffer.append(0x00) 
        
    try:
        i2c.writeto(DISPLAY_ADDR, buffer)
    except OSError:
        pass

init_display()

while True:
    raw_value = adc_pin.read_u16()
    voltage = raw_value * conversion_factor
    display_val = int(voltage * 100) 
    show_value(display_val)
    time.sleep(0.1)
