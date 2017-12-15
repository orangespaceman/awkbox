import os
import random
import time
import RPi.GPIO as GPIO
import speakerphat
import pygame

# tilt
tiltswitchPin = 23
tiltState = 1          # 0 or 1, depending on whether the tilt switch is active
lastTiltState = 1

# play
is_playing = False
pygame.init()
pygame.mixer.init()
sfx_path = "/home/pi/awkbox/sfx"

# lights
active_led = 0
led_direction = -1
led_count = 9
led_brightness = 255

# GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(tiltswitchPin, GPIO.IN)

while True:
    # get state
    is_playing = pygame.mixer.music.get_busy()
    tiltState = GPIO.input(tiltswitchPin)

    # play
    if tiltState is not 1 and lastTiltState is 1 and is_playing is not True:
        sfx = random.choice(os.listdir(sfx_path))
        pygame.mixer.music.load("%s/%s" % (sfx_path, sfx))
        pygame.mixer.music.play()
        print sfx

    # lights
    if is_playing:
        if active_led == led_count or active_led == 0:
            led_direction = -led_direction
        active_led += led_direction
        led_brightness = 255
    else:
        active_led = 0
        led_direction = -1
        led_brightness = 0 if led_brightness == 255 else 255

    speakerphat.clear()
    speakerphat.set_led(active_led, led_brightness)
    speakerphat.show()

    lastTiltState = tiltState
    time.sleep(0.5)
