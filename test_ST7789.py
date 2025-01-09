from machine import Pin, SPI
import framebuf
import st7789
from sys import stdin
import uselect

WIDTH, HEIGHT = 240, 240
'''
BACKLIGHT_PIN = 11 
RES_PIN = 13 
DC_PIN = 7 
CS_PIN = 6 
SCL_PIN = 15 # Clock line， SCK = SCL 
SDA_PIN = 14 # Data line， MOSI = SDA 
SPI_NUM = 0
'''

BACKLIGHT_PIN = 9
SCL_PIN = 6
SDA_PIN = 7
RES_PIN = 13
DC_PIN = 14
CS_PIN = 15
SPI_NUM = 0

# Color Constants
COLOUR_BLACK = st7789.color565(0, 0, 0)
HAND_COLOUR = st7789.color565(0, 0, 63)

# Initialize SPI and TFT Display
spi = SPI(SPI_NUM, baudrate=31250000, sck=Pin(SCL_PIN), mosi=Pin(SDA_PIN))

tft = st7789.ST7789(
    spi, WIDTH, HEIGHT,
    reset=Pin(RES_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT),
    dc=Pin(DC_PIN, Pin.OUT),
    backlight=Pin(BACKLIGHT_PIN, Pin.OUT),
    rotation=0,
)
# tft.init()

# Create framebuffer for hand drawing
hand = framebuf.FrameBuffer(
    bytearray(WIDTH * HEIGHT * 2), WIDTH, HEIGHT, framebuf.RGB565
)

# Initial Screen Fill
tft.fill(COLOUR_BLACK)

#======================================================================
# this part is for testing 
#======================================================================
hand.fill_rect(50, 50, 100, 100, HAND_COLOUR) 

# Display the contents of FrameBuffer to the screen 
tft.blit_buffer(hand, 0, 0, 240, 240)
#======================================================================

