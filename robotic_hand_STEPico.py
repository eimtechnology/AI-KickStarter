from machine import Pin
from machine import PWM
from sys import stdin
import math
import uselect 
import time

# this is for servo controlling
servo_thumb = Pin(16)
servo_index = Pin(17)
servo_middle = Pin(18)
servo_ring = Pin(19)
servo_pinky = Pin(20)

servo_pwm1 = PWM(servo_thumb)
servo_pwm2 = PWM(servo_index)
servo_pwm3 = PWM(servo_middle)
servo_pwm4 = PWM(servo_ring)
servo_pwm5 = PWM(servo_pinky)

servo_pwm1.freq(50)
servo_pwm2.freq(50)
servo_pwm3.freq(50)
servo_pwm4.freq(50)
servo_pwm5.freq(50)


thumb_angel = 0
index_angel = 0
middle_angel = 0
ring_angel = 0
pinky_angel = 0


# Minimum Pulse Width (0º) corresponds to 1802
# Maximum Pulse Width (180º) corresponds to 7864

# control servo turn to certain angle
def set_thumb_angle(angle):
    min_duty = 1802 
    max_duty = 7864
    # origin equation
    duty = min_duty + (max_duty - min_duty) * angle // 180
    # optimized equation
    #duty = min_duty + int(math.fabs((max_duty - min_duty) * (math.sin(angle // 180 * math.pi-math.pi/4))))
    '''
    if duty > 7864:
        duty = 7864
    elif duty < 1802:
        duty = 1802
    '''
    servo_pwm1.duty_u16(duty)

def set_index_angle(angle):
    
    min_duty = 1802 
    max_duty = 7864
    duty = min_duty + (max_duty - min_duty) * angle // 180
    servo_pwm2.duty_u16(duty)
    
def set_middle_angle(angle):
    
    min_duty = 1802 
    max_duty = 7864
    duty = min_duty + (max_duty - min_duty) * angle // 180
    servo_pwm3.duty_u16(duty)
    
def set_ring_angle(angle):
    
    min_duty = 1802 
    max_duty = 7864
    duty = min_duty + (max_duty - min_duty) * angle // 180
    servo_pwm4.duty_u16(duty)

def set_pinky_angle(angle):
    
    min_duty = 1802 
    max_duty = 7864
    duty = min_duty + (max_duty - min_duty) * angle // 180
    servo_pwm5.duty_u16(duty)

while True:
    select_result = uselect.select([stdin], [], [], 1)

    while select_result[0]:
        data = stdin.read(15) # Read 15 byte incoming data from USB
        thumb_angel = int(data[0:3])
        index_angel = int(data[3:6])
        middle_angel = int(data[6:9])
        ring_angel = int(data[9:12])
        pinky_angel = int(data[12:15])
        
        set_thumb_angle(thumb_angel)
        set_index_angle(index_angel)
        set_middle_angle(middle_angel)
        set_ring_angle(ring_angel)
        set_pinky_angle(pinky_angel)
        time.sleep_ms(20)
