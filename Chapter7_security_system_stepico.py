from machine import Pin, SPI, ADC, PWM
from sys import stdin
from fonts import vga1_16x32 as font1
from fonts import vga2_8x8 as font2
import st7789py as st7789
import uselect
import math 
import time

# this part is for servo controlling
gate_servo = Pin(18)
gate_pwm = PWM(gate_servo)
gate_pwm.freq(50)

# false for closed, true for opened
gate_condition = False

# false for stopped, true for working
buzzer_condition = False

# empty place holder
names = ["","",""]

#led wiring 
green_led = Pin(17, Pin.OUT)
red_led = Pin(27, Pin.OUT)

#buzzer wiring 
buzzer = Pin(19)
buzzer_pwm = PWM(buzzer)
buzzer_pwm.freq(400)

#[0] for recognized, [1] for unrecognized
condition = [0,0]

# Set up st7789 display Pins 
WIDTH, HEIGHT = 240, 240

BACKLIGHT_PIN = 9
# SCK = SCL
# MOSI = SDA
# RET = RES
SCK_PIN = 6
MOSI_PIN = 7
RST_PIN = 13
DC_PIN = 14
CS_PIN = 15
SPI_NUM = 0

# initialize spi communication
spi = SPI(SPI_NUM, baudrate=31250000, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))
tft = st7789.ST7789(
    spi, WIDTH, HEIGHT,
    reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT),
    dc=Pin(DC_PIN, Pin.OUT),
    backlight=Pin(BACKLIGHT_PIN, Pin.OUT),
    rotation=0,
)

# testing text display on the st7789
#t = "Hello World"
#tft.text(font,str(t),35,108,st7789.color565(255,0,0))

tft.text(font2,str("Recognized Personnel: "),8,8,st7789.color565(0,255,255))

# Minimum Pulse Width (0º) corresponds to 1802
# Maximum Pulse Width (180º) corresponds to 7864

def unrecognized_warn_on():
    tft.text(font1,str("Unrecognized Personnel"),8,120,st7789.color565(255,0,0))
    tft.text(font1,str("Present"),8,160,st7789.color565(255,0,0))

def unrecognized_warn_off():
    tft.text(font1,str("                      "),8,120,st7789.color565(255,0,0))
    tft.text(font1,str("       "),8,160,st7789.color565(255,0,0))

def show_names(name_list):
    for i in range(len(name_list)):
        string = str(name_list[i])
        tft.text(font2,str(string),8,18+10*i,st7789.color565(255,0,0))
        
def clear_names(name_list):
    for i in range(len(name_list)):
        tft.text(font2,str("                "),8,18+10*i,st7789.color565(255,0,0))

def set_gate_angle(angel):    
    min_duty = 1802 
    max_duty = 7864
    duty = min_duty + (max_duty - min_duty) * angel // 180
    gate_pwm.duty_u16(duty)

while True:
    select_result = uselect.select([stdin], [], [], 1)

    while select_result[0]:
        # Original
        #data = stdin.read(2)
        data = stdin.read(38)
        
        condition = [int(data[0]),int(data[1])]
        names = [str(data[2:14]),str(data[14:26]),str(data[26:38])] 
        
        if condition[0] == 1:
            green_led.value(1)
            show_names(names)
            # deciding gate condition
            if condition[1] == 0:
                gate_condition = True
                set_gate_angle(90)
            else:
                pass
            print("Trun on green LED, Gate:", gate_condition, ", Buzzer:", buzzer_condition)
        else:
            green_led.value(0)
            clear_names(names)
            gate_condition = False
            set_gate_angle(0)
            print("Trun off green LED, Gate:", gate_condition, ", Buzzer:", buzzer_condition)
        
        if condition[1] == 1:
            if buzzer_condition is True:
                pass
            else:
                buzzer_condition = True
                buzzer_pwm.duty_u16(1000)
            gate_condition = False
            set_gate_angle(0)
            red_led.value(1)
            unrecognized_warn_on()
            print("Trun on red LED, Gate:", gate_condition, ", Buzzer:", buzzer_condition)
        else:
            red_led.value(0)
            buzzer_condition = False
            buzzer_pwm.duty_u16(0)
            unrecognized_warn_off()
            print("Trun off red LED, Gate:", gate_condition, ", Buzzer:", buzzer_condition)
            
        #flush_cache()
        
