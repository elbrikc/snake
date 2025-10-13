from machine import Pin,SPI,PWM
import framebuf
import time
import os
import math

def rgb(R,G,B):
# Get RED value
    rp = int(R*31/255) # range 0 to 31
    if rp < 0: rp = 0
    r = rp *8
# Get Green value - more complicated!
    gp = int(G*63/255) # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    b = bp *256
    colour = r+g+b
    return colour

# ========= MAIN ===========

pwm = PWM(Pin(BL)) # Screen Brightness
pwm.freq(1000)
pwm.duty_u16(32768) # max 65535 - mid value

LCD = LCD_1inch3()
LCD.fill(0)
LCD.show()

x = y = 120
s = 5 # speed (pix/frame)

keyA = Pin(15,Pin.IN,Pin.PULL_UP) # Normally 1 but 0 if pressed
keyB = Pin(17,Pin.IN,Pin.PULL_UP)
keyX = Pin(19,Pin.IN,Pin.PULL_UP)
keyY= Pin(21,Pin.IN,Pin.PULL_UP)

up = Pin(2,Pin.IN,Pin.PULL_UP)
down = Pin(18,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)
ctrl = Pin(3,Pin.IN,Pin.PULL_UP)

def xhair(x,y,g): 
    """
        I
      h I
        I
        I______________
               w
    """
    w = 3
    h = 16
    
    LCD.fill(0)
    LCD.fill_rect(int(x-(w/2)),y-g-h,w,h,rgb(255,255,255)) # UP
    LCD.fill_rect(int(x-(w/2)),y+g,w,h,rgb(255,255,255)) # DOWN
    LCD.fill_rect(x+g,int(y-(w/2)),h,w,rgb(255,255,255)) # RIGHT
    LCD.fill_rect(x-g-h,int(y-(w/2)),h,w,rgb(255,255,255)) # LEFT


def flash(x,y):
    LCD.fill(rgb(20, 0, 0))
    LCD.fill_rect(x-120,y-120,240,240,rgb(184, 0, 0))
    LCD.fill_rect(x-100,y-100,200,200,rgb(220, 0, 0))
    LCD.fill_rect(x-85,y-85,170,170,rgb(255, 134, 0))
    LCD.fill_rect(x-70,y-70,140,140,rgb(255, 199, 0))
    LCD.fill_rect(x-30,y-30,60,60,rgb(238, 255, 0))
    LCD.fill_rect(x-20,y-20,40,40,rgb(255,255,255))

xhair(x,y,6)

frate = 0.05

while True:
    x = x % 240
    y = y % 240
#=========MOVEMENT=========
    if up.value()==0:
        y -= s
        xhair(x,y,6)
        
    if down.value()==0:
        y += s
        xhair(x,y,6)

    if right.value()==0:
        x += s
        xhair(x,y,6)
        
    if left.value()==0:
        x -= s
        xhair(x,y,6)
        
#==========FLASH===========    
    if keyA.value()==0:
        xhair(x,y,15)
        flash(x,y)
        LCD.show()
        time.sleep(frate)
        LCD.fill(0)
        xhair(x,y,6)
    
#===========QUIT===========
    if keyY.value()==0:
        LCD.fill(0)
        LCD.text('POWER OFF NOW',65,115,LCD.white)
        LCD.show()
        break
    
    time.sleep(frate)
    LCD.show()


