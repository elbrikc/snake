#PLAY SNAKE
from machine import Pin,SPI,PWM
import framebuf
import time
import os
import math
import driver
import random

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


def mp(x,y,colour):
    # Draw mega pixel (10x10), indexed in ascending integer coords
    LCD.fill_rect(x*10,y*10,10,10,colour)


def tgt(snake):
    tgt_x = random.randint(0,23)
    tgt_y = random.randint(0,23)
    
    checked = False
    while not checked:
        checked = True
        for i in snake:
            if i == [tgt_x,tgt_y]:
                tgt_x = random.randint(0,23)
                tgt_y = random.randint(0,23)
                checked = False
    
    return tgt_x,tgt_y


def pause():
    unpause = 0
    while unpause == 0:
        LCD.fill_rect(40,40,160,160,rgb(255,255,255))
        LCD.fill_rect(81,70,26,100,rgb(0,0,0))
        LCD.fill_rect(133,70,26,100,rgb(0,0,0))
        LCD.show()
        time.sleep(1)
        if Y.value() == 0:
            unpause = 1


def check_fail(nose,snake):
    for i in snake[1:]:
        if nose == i:
    #if X.value() == 0:
           while True:
                LCD.fill(0)
                LCD.text('YOU ARE',85,60,rgb(255,255,255))
                LCD.text('ded.',100,80,rgb(255,0,0))
                LCD.text('FUCK YOU',80,100,rgb(255,255,255))
                LCD.text('Cycle power to replay',30,140,rgb(255,255,255))
                LCD.show()


if __name__ == '__main__':

    score = 0
    tstep = 0.3
    
    BL = 13

    pwm = PWM(Pin(BL)) # Screen Brightness
    pwm.freq(1000)
    pwm.duty_u16(32768) # max 65535 - mid value

    LCD = driver.LCD_1inch3()
    
    A = Pin(15,Pin.IN,Pin.PULL_UP) # Normally 1 but 0 if pressed
    B = Pin(17,Pin.IN,Pin.PULL_UP)
    X = Pin(19,Pin.IN,Pin.PULL_UP)
    Y = Pin(21,Pin.IN,Pin.PULL_UP)

    U = Pin(2,Pin.IN,Pin.PULL_UP)
    D = Pin(18,Pin.IN,Pin.PULL_UP)
    L = Pin(16,Pin.IN,Pin.PULL_UP)
    R = Pin(20,Pin.IN,Pin.PULL_UP)
    C = Pin(3,Pin.IN,Pin.PULL_UP)

    LCD.fill(0)
    
    snake = [[12,12],[11,12],[10,12]]
    dx = 1
    dy = 0
    back = ''
    
    tgt_x,tgt_y = tgt(snake)
    
    while True:
        LCD.fill(0)
            
        if U.value() == 0 and back != 'U':
            dx = 0
            dy = -1
            back = 'D'
        if D.value() == 0 and back != 'D':
            dx = 0
            dy = 1
            back = 'U'
        if L.value() == 0 and back != 'L':
            dx = -1
            dy = 0
            back = 'R'
        if R.value() == 0 and back != 'R':
            dx = 1
            dy = 0
            back = 'L'
        #if Y.value() == 0:
            #print(Y.value())
            #pause()
        
        del snake[-1]
        nose = [(snake[0][0]+dx)%24, (snake[0][1]+dy)%24]
        snake.insert(0,nose)
        for i in range(len(snake)):
                mp(snake[i][0],snake[i][1],rgb(0,255,255))

        check_fail(nose,snake)

        LCD.text('SCORE: ',160,10,rgb(255,255,255))
        LCD.text(str(score),210,10,rgb(255,0,255))

        if [tgt_x,tgt_y] == nose:
            score += 1
            if tstep >= 0.05:
                tstep -= 0.01
            print(tstep)
            if (snake[-1][0] - snake[-2][0]) == 0:
                d = snake[-2][1]+snake[-1][1]
                snake.append([snake[-1][0]-d,snake[-1][0]])
            if (snake[-1][1] - snake[-2][1]) == 0:
                d = snake[-2][0]+snake[-1][0]
                snake.append([snake[-1][1]-d,snake[-1][1]])
            
            tgt_x,tgt_y = tgt(snake)

        mp(tgt_x,tgt_y,rgb(255,255,0))

        LCD.show()
        time.sleep(tstep)


