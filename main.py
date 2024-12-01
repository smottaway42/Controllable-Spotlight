"""
Sean Ottaway - Assembly, Parts, Software
Yun Kim - Assembly, Software
Controllable Spotlight

Push switch up to pitch up, down to pitch down, must manually move switch to middle position
Top light turns light on, bottom turns off

*Sources*
[*] Motor Control - Nerd Cave - Accessed 11/15/2024 - Link: https://www.youtube.com/watch?v=H1Fzil_VUq4
[*] External Buttons - Nerd Cave - Accessed 11/27/2024 - Link: https://www.youtube.com/watch?v=q_sXuOMiWjY
"""
from PicoBreadboard import BUTTON
from machine import Pin, PWM
import time
from time import sleep

#Controller pins
button1 = Pin("GP0", Pin.IN, Pin.PULL_UP) #White Wire Up
button2 = Pin("GP1", Pin.IN, Pin.PULL_UP) #Red Wire Down
button3 = Pin("GP2", Pin.IN, Pin.PULL_UP) #Green Wire On
button4 = Pin("GP4", Pin.IN, Pin.PULL_UP) #Yellow Wire Off

# Relay pins
relay = Pin(16, Pin.OUT) #GP16

# Motor pins
in3 = Pin(14, Pin.OUT)  # IN3 connected to GPIO 14 (left pin) Orange
in4 = Pin(15, Pin.OUT)  # IN4 connected to GPIO 15 (middle pin) Yellow
enb = PWM(Pin(13))      # ENB connected to GPIO 13 for PWM control (right pin) Brown
enb.freq(1000)          # Set PWM frequency to 1 kHz

def motor_forward(speed):
    in3.high()          # Set IN3 high
    in4.low()           # Set IN4 low
    enb.duty_u16(speed) # Set motor speed (0-65535 for duty cycle)

def motor_backward(speed):
    in3.low()           # Set IN3 low
    in4.high()          # Set IN4 high
    enb.duty_u16(speed) # Set motor speed (0-65535 for duty cycle)

def motor_stop():
    in3.low()           # Stop motor
    in4.low()           # Stop motor
    enb.duty_u16(0)     # Disable motor (set PWM duty cycle to 0)
            
relay.value(0) #reset light    

try:
    while True:
        
        if button1.value() == 0:
            print("Moving forward")
            motor_forward(65535)  # Set speed to 50% (PWM value)
        
        elif button2.value() == 0:
            print("Moving backward")
            motor_backward(65535)
            
        elif button3.value() == 0:
            relay.value(1)
            print("ON")
        
        elif button4.value() == 0:
            relay.value(0)
            print("OFF")
        
        else:
            print(".")
            motor_stop()
            
    
        time.sleep(0.1)
        
except KeyboardInterrupt:
    motor_stop()
    relay.value(0)
    print("Program stopped")
