from machine import Pin, SPI, ADC
import math, framebuf
import st7789
from sys import stdin
import uselect

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

spi = SPI(SPI_NUM, baudrate=31250000, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))
tft = st7789.ST7789(
    spi, WIDTH, HEIGHT,
    reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT),
    dc=Pin(DC_PIN, Pin.OUT),
    backlight=Pin(BACKLIGHT_PIN, Pin.OUT),
    rotation=0,
)   

hand = lambda: framebuf.FrameBuffer(
    bytearray(WIDTH*HEIGHT*2), WIDTH, HEIGHT,framebuf.RGB565
)

tft.fill(st7789.BLACK)

'''
# this part is for testing

buffer= fb.fill_rect(50, 50, 100, 100, HAND_COLOUR)

# Display the contents of FrameBuffer to the screen
tft.blit_buffer(buffer, 0, 0, width, height)
'''

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
        new_hand.fill_rect(*coords["palm"],st7789.RED)

        new_hand.fill_rect(*coords["thumb"], st7789.RED) if m == 1 else new_hand.rect(*coords["thumb"], st7789.RED)
        new_hand.fill_rect(*coords["index"], st7789.RED) if i == 1 else new_hand.rect(*coords["index"], st7789.RED)
        new_hand.fill_rect(*coords["middle"], st7789.RED) if j == 1 else new_hand.rect(*coords["middle"], st7789.RED)
        new_hand.fill_rect(*coords["ring"], st7789.RED) if k == 1 else new_hand.rect(*coords["ring"], st7789.RED)
        new_hand.fill_rect(*coords["pinky"], st7789.RED) if l == 1 else new_hand.rect(*coords["pinky"], st7789.RED)
        
        tft.blit_buffer(new_hand, 0, 0, 240, 240)
    if len(s) > 15:
        s = s[-10:]

