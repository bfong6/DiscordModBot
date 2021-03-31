import RPi.GPIO as GPIO
import lcddriver
#import time
lcd = lcddriver.lcd()
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        pass_state = GPIO.input(17)
        warn_state = GPIO.input(18)
        ban_state = GPIO.input(27)
        if pass_state == False:
            lcd.lcd_display_string("pass", 1)
        if warn_state == False:
            lcd.lcd_display_string("warn", 1)
        if ban_state == False:
            lcd.lcd_display_string("ban", 1)
finally:
    gpio.cleanup()
