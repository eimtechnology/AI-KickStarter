import time
from neopixel import NeoPixel
from machine import Pin
from sys import stdin

from machine import ADC, Pin

import uselect

red1 = Pin(16 ,Pin.OUT)
orange1 = Pin(17 ,Pin.OUT)
yellow1 = Pin(18 ,Pin.OUT)
green1 = Pin(19 ,Pin.OUT)
blue1 = Pin(20, Pin.OUT)

red2 = Pin(15, Pin.OUT)
orange2 = Pin(14, Pin.OUT)
yellow2 = Pin(13, Pin.OUT)
green2 = Pin(12, Pin.OUT)
blue2 = Pin(9, Pin.OUT)

left_LEDs = [red1, orange1, yellow1, green1, blue1]
right_LEDs = [red2, orange2, yellow2, green2, blue2]

hand = '0'

def turn_on_LEDs (LEDs, num_LEDs):
    num_LEDs = int(num_LEDs)
    if num_LEDs == 0:
        for leds in LEDs:
            leds.value(0)
    else:
        for i in range(num_LEDs):
            LEDs[i].value(1)
        for i in range(num_LEDs, 5, 1):
            LEDs[i].value(0)

while True:
    select_result = uselect.select([stdin], [], [], 0)

    while select_result[0]:

        input_character = stdin.read(1)

        if hand == '1':
            hand = '0'
            turn_on_LEDs(left_LEDs, input_character)
        elif hand == '2':
            hand = '0'
            turn_on_LEDs(right_LEDs, input_character)
        elif input_character == '1' or input_character == '2':
            hand = input_character
        elif input_character == 'L':
            turn_on_LEDs(left_LEDs, 5)
        elif input_character == 'R':
            turn_on_LEDs(right_LEDs, 5)
          
    select_result = uselect.select([stdin], [], [], 0)
