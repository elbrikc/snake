import driver
from machine import Pin,PWM
import utime
import math

def colour(R,G,B):
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
    
def ring(cx,cy,r,cc):   # Draws a circle - with centre (x,y), radius, colour 
    for angle in range(91):  # 0 to 90 degrees in 2s
        y3=int(r*math.sin(math.radians(angle)))
        x3=int(r*math.cos(math.radians(angle)))
        LCD.pixel(cx-x3,cy+y3,cc)  # 4 quadrants
        LCD.pixel(cx-x3,cy-y3,cc)
        LCD.pixel(cx+x3,cy+y3,cc)
        LCD.pixel(cx+x3,cy-y3,cc)
  
# =========== Main ============
BL = 13  # Pins used for display screen

pwm = PWM(Pin(BL)) # Screen Brightness
pwm.freq(1000)
pwm.duty_u16(32768) # max 65535 - mid value

LCD = driver.LCD_1inch3()
# Background colour - dark grey
LCD.fill(colour(40,40,40))
LCD.show()

# Define pins for buttons and Joystick
keyA = Pin(15,Pin.IN,Pin.PULL_UP) # Normally 1 but 0 if pressed
keyB = Pin(17,Pin.IN,Pin.PULL_UP)
keyX = Pin(19,Pin.IN,Pin.PULL_UP)
keyY= Pin(21,Pin.IN,Pin.PULL_UP)

up = Pin(2,Pin.IN,Pin.PULL_UP)
down = Pin(18,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)
ctrl = Pin(3,Pin.IN,Pin.PULL_UP)

# Draw background, frame, title and instructions
LCD.rect(0,0,240,240,LCD.red) # Red edge
# White Corners
LCD.pixel(1,1,LCD.white)     # LT
LCD.pixel(0,239,LCD.white)   # LB
LCD.pixel(239,0,LCD.white)   # RT
LCD.pixel(239,239,LCD.white) # RB
LCD.text('WS 1.3" IPS Display', 20, 10, colour(0,0,255))
LCD.text('  240x240 pixels', 20, 20, colour(0,0,255))
LCD.text('Use your joystick', 25, 33, colour(255,255,0))
LCD.text('   and buttons', 25, 43, colour(255,255,0))
LCD.text("Press A & Y to", 30, 200, colour(255,0,0))
LCD.text(" Halt program", 30, 220, colour(255,0,0))
LCD.show()

running = True # Loop control
# =========== Main loop ===============
while(running):
    if keyA.value() == 0:
        LCD.fill_rect(200,15,30,30,colour(255,255,0)) # Yellow
        print("A")
    else :
        LCD.fill_rect(200,15,30,30,LCD.white)
        LCD.rect(200,15,30,30,LCD.red)            
        
    if(keyB.value() == 0):
        LCD.fill_rect(200,75,30,30,colour(255,0,255)) # Magenta
        print("B")
    else :
        LCD.fill_rect(200,75,30,30,LCD.white)
        LCD.rect(200,75,30,30,LCD.red)
                   
    if(keyX.value() == 0):
        LCD.fill_rect(200,135,30,30,colour(0,255,255)) # Cyan
        print("X")
    else :
        LCD.fill_rect(200,135,30,30,LCD.white)
        LCD.rect(200,135,30,30,LCD.red)
        
    if(keyY.value() == 0):
        LCD.fill_rect(200,195,30,30,colour(255,180,50)) # Orange
        print("Y")
    else :
        LCD.fill_rect(200,195,30,30,LCD.white)
        LCD.rect(200,195,30,30,LCD.red)
        
    if(up.value() == 0):
        LCD.fill_rect(60,60,30,30,LCD.red)
        print("UP")
    else :
        LCD.fill_rect(60,60,30,30,LCD.white)
        LCD.rect(60,60,30,30,LCD.red)
        
    if(down.value() == 0):
        LCD.fill_rect(60,150,30,30,LCD.red)
        print("DOWN")
    else :
        LCD.fill_rect(60,150,30,30,LCD.white)
        LCD.rect(60,150,30,30,LCD.red)
        
    if(left.value() == 0):
        LCD.fill_rect(15,105,30,30,LCD.red)
        print("LEFT")
    else :
        LCD.fill_rect(15,105,30,30,LCD.white)
        LCD.rect(15,105,30,30,LCD.red)
    
    if(right.value() == 0):
        LCD.fill_rect(105,105,30,30,LCD.red)
        print("RIGHT")
    else :
        LCD.fill_rect(105,105,30,30,LCD.white)
        LCD.rect(105,105,30,30,LCD.red)
    
    if(ctrl.value() == 0):
        LCD.fill_rect(60,105,30,30,LCD.red)
        print("CTRL")
    else :
        LCD.fill_rect(60,105,30,30,LCD.white)
        LCD.rect(60,105,30,30,LCD.red)
                   
    LCD.show()
    if (keyA.value() == 0) and (keyY.value() == 0): # Halt looping?
        running = False
        
    utime.sleep(.15) # Debounce delay - reduce multiple button reads
    
# Finish
LCD.fill(0)
for r in range(10):
    ring(120,120,60+r,colour(255,255,0))
LCD.text("Halted", 95, 115, colour(255,0,0))
LCD.show()
# Tidy up
utime.sleep(3)
LCD.fill(0)
LCD.show()