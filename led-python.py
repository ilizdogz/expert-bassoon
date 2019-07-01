from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO
import time

# use channel numbers on the Broadcom SOC
GPIO.setmode(GPIO.BCM)

# defining the pins
GPIO_RED = 4
GPIO_GREEN = 18
GPIO_BLUE = 17

# defining the pins as output
GPIO.setup(GPIO_RED, GPIO.OUT)
GPIO.setup(GPIO_GREEN, GPIO.OUT)
GPIO.setup(GPIO_BLUE, GPIO.OUT)

# choosing a frequency for pwm
PWM_FREQUENCY = 50

# configure to use PWM
COLOR_PWM = [ 
    GPIO.PWM(GPIO_RED, PWM_FREQUENCY),
    GPIO.PWM(GPIO_GREEN, PWM_FREQUENCY),
    GPIO.PWM(GPIO_BLUE, PWM_FREQUENCY)
]

# For CATHODE this must be 0
# For ANODE this must be 1
COMMON_NODE = 1

def transition(currentColor, targetColor, duration, fps):
    distance = colorDistance(currentColor, targetColor)
    increment = calculateIncrement(distance, fps, duration)

    for i in range(0, int(fps)):
        transitionStep(currentColor, targetColor, increment)
        time.sleep(duration/fps)

def colorDistance(currentColor, targetColor):
    distance = [0, 0, 0]

    for i in range(len(currentColor)):
        distance[i] = abs(currentColor[i] - targetColor[i])

    return distance

def calculateIncrement(distance, fps, duration):
    increment = [0, 0, 0]

    for i in range(len(distance)):
        inc = abs(distance[i] / fps)
        increment[i] = inc
    return increment

def transitionStep(currentColor, targetColor, increment):
    for i in range(len(currentColor)):
        if currentColor[i] > targetColor[i]:
            currentColor[i] -= increment[i]
            if currentColor[i] <= targetColor[i]:
                increment[i] = 0
        else:
            currentColor[i] += increment[i]
            if currentColor[i] >= targetColor[i]:
                increment[i] = 0
    setColor(currentColor)

def setColor(color):
    for i in range(len(COLOR_PWM)):
        percent = hexPercent(color[i])
        if COMMON_NODE:
            percent = 100 - percent
        COLOR_PWM[i].ChangeDutyCycle(percent)

def hexPercent(color):
    percent = (color / float(0xFF)) * 100
    return percent

if __name__ == '__main__':
    try:
        for i in range(len(COLOR_PWM)):
            COLOR_PWM[i].start(1)

        duration = 2.0
        fps = 90.0

        i = 0
        while 1:
            colors = [
                [0xE8, 0x0B, 0x0B], # red
                [0x0b, 0x12, 0xe8], # blue
                [0xe8, 0xd5, 0x0b], # yellow
                [0xdd, 0x0b, 0xe8], # purple
                [0x1A, 0xe8, 0x0B], # green
                [0x0b, 0xd5, 0xe8]  # teal
            ]

            currentColor = colors[i % len(colors)]

            i = (i + 1) % len(colors)
            nextColor = colors[i]

            transition(currentColor, nextColor, duration, fps)

        # close execution by pressing CTRL + C
    except KeyboardInterrupt:
        print("Intrerrupted by user")
        pass
    finally:
        print("Program stopped")
        for colorPwm in COLOR_PWM:
            colorPwm.stop()
        GPIO.cleanup()