

from machine import Pin, SPI, ADC
# from rotary_irq_rp2 import RotaryIRQ # type: ignore
# https://github.com/MikeTeachman/micropython-rotary
import math, framebuf
import st7789# type: ignore
import vga1_8x8 as font # type: ignore
# from rotary_irq_rp2 import RotaryIRQ # type: ignore
# https://docs.keyestudio.com/projects/KS3024/en/latest/MicroPython/Micropython.html


from sys import stdin
import uselect

# https://www.youtube.com/watch?v=a7MzPA0T_MM



WIDTH, HEIGHT = 240, 240
 # SCK = SCL
 # MOSI = SDA
BACKLIGHT_PIN = 20
RST_PIN = 16
DC_PIN = 21
CS_PIN = 17
SCK_PIN = 18
MOSI_PIN = 19
SPI_NUM = 0

# Voltage Divider
Vin = 3.3
Ro = 10000  # 10k Resistor

# Steinhart Constants
A = 0.001129148
B = 0.000234125
C = 0.0000000876741

T1 = ADC(26)
T2 = ADC(27)

SPDT = Pin(22, Pin.IN)
SW = Pin(0, Pin.IN, Pin.PULL_UP)

spi = SPI(SPI_NUM, baudrate=31250000, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))
tft = st7789.ST7789(
    spi, WIDTH, HEIGHT,
    reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT),
    dc=Pin(DC_PIN, Pin.OUT),
    backlight=Pin(BACKLIGHT_PIN, Pin.OUT),
    rotation=0,
)
print(tft)
tft.init()    

hand = lambda: framebuf.FrameBuffer(
    bytearray(WIDTH*HEIGHT*2), WIDTH, HEIGHT,framebuf.RGB565
)

peach = st7789.color565(241,194,125)
peach2 = 0xf1c27d
# hand.fill_rect(80,140,120,60,peach2)

hands = dict()

# for i in range(2):
#     for j in range(2):
#         for k in range(2):
#             for l in range(2):
#                 for m in range(2):
#                     new_hand  = hand()
#                     new_hand.fill_rect(80,140,120,60,peach2)

#                     new_hand.fill_rect(90,50,20,120-50, peach2) if i == 1 else new_hand.rect(90,50,20,120-50, peach2)
#                     new_hand.fill_rect(120,30,20,120-30, peach2) if j == 1 else new_hand.rect(120,30,20,120-30, peach2)
#                     new_hand.fill_rect(150,50,20,120-50, peach2) if k == 1 else new_hand.rect(150,50,20,120-50, peach2)
#                     new_hand.fill_rect(180,70,20,120-70, peach2) if l == 1 else new_hand.rect(180,70,20,120-70, peach2)
#                     new_hand.fill_rect(40,180,20,20, peach2) if m == 1 else new_hand.rect(40,180,20,20, peach2)
#                     hands[f"{i}{j}{k}{l}{m}"] = hand
#                     "ijklm"



# hand.rect(90,50,20,120-50, peach2)
# hand.rect(120,30,20,120-30, peach2)
# hand.rect(150,50,20,120-50, peach2)
# hand.rect(180,70,20,120-70, peach2)
# hand.rect(40,180,20,20, peach2)


# hand.rect(180,70,20,120-70, peach2)




# hand.line(40,110,70,170,peach2)
# hand.line(30,120,60,180,peach2)
# hand.line(40,110,30,120,peach2)
# hand.line(70,170,60,180,peach2)



# hand.text("Hello", 50, 50, peach2)

tft.fill(st7789.color565(0,0,0))
new_hand  = hand()
s = ""

coords = {
    "thumb": [50,160,20,40],
    "index": [90,60,20,120-50],
    "middle": [120,40,20,120-30],
    "ring": [150,60,20,120-50],
    "pinky": [180,80,20,120-70],
    "palm": [80,140,120,60],
}

while True:


    select_result = uselect.select([stdin], [], [], 0)

    while select_result[0]:
        input_character = stdin.read(1)
        s += str(input_character)
    
        select_result = uselect.select([stdin], [], [], 0)
        
    #tft.text(font,f"InputChar:{repr(s)}",0,0,st7789.color565(0,0,255))
    m,i,j,k,l = 0,0,0,0,0

    if len(s) > 10:
        try:
            
            # tft.fill(st7789.color565(0,0,0))
            
            n = len(s)-1          
            while True:
                if s[n] == "\n":
                    break
                else:
                    n -= 1
            
            # print(tft)
            m = int(s[n-5])
            i = int(s[n-4])
            j = int(s[n-3])
            k = int(s[n-2])
            l = int(s[n-1])
            
            # tft.text(font,str(n),0,180,st7789.color565(255,0,0))

        except Exception as e:
            #tft.fill(st7789.color565(0,0,0))
            #tft.text(font,f"{repr(e)}"[25:],0,180,st7789.color565(0,0,255))
            pass
        
        new_hand.fill(st7789.color565(0,0,0))
        new_hand.fill_rect(*coords["palm"],peach2)

        new_hand.fill_rect(*coords["thumb"], peach2) if m == 1 else new_hand.rect(*coords["thumb"], peach2)
        new_hand.fill_rect(*coords["index"], peach2) if i == 1 else new_hand.rect(*coords["index"], peach2)
        new_hand.fill_rect(*coords["middle"], peach2) if j == 1 else new_hand.rect(*coords["middle"], peach2)
        new_hand.fill_rect(*coords["ring"], peach2) if k == 1 else new_hand.rect(*coords["ring"], peach2)
        new_hand.fill_rect(*coords["pinky"], peach2) if l == 1 else new_hand.rect(*coords["pinky"], peach2)
        
        tft.blit_buffer(new_hand, 0, 0, 240, 240)
    if len(s) > 15:
        s = s[-10:]
        

