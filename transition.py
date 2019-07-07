# import RPi.GPIO as GPIO
import pigpio
import time
import math
# import os
# from datetime import datetime, timedelta

pi = pigpio.pi()
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(27, GPIO.IN)

# isOn = False
# lastChange = datetime.now()

# defining the pins
GPIO_RED = 4
GPIO_GREEN = 18
GPIO_BLUE = 17

def setPwm(color):
    # if (isOn):
    pi.set_PWM_dutycycle(GPIO_RED, color[0])
    pi.set_PWM_dutycycle(GPIO_GREEN, color[1])
    pi.set_PWM_dutycycle(GPIO_BLUE, color[2])
    # else:
    #     pi.set_PWM_dutycycle(GPIO_RED, 0)
    #     pi.set_PWM_dutycycle(GPIO_GREEN, 0)
    #     pi.set_PWM_dutycycle(GPIO_BLUE, 0)

def transition(currentColor, targetColor, duration, fps):
    currentColor = hexToRgb(currentColor)
    targetColor = hexToRgb(targetColor)
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
    setPwm(currentColor)

def hexToRgb(color):
    color = color.lstrip("#")
    return list(int(color[i:i+2], 16) for i in (0, 2, 4))

# def checkForButton():
#     global lastChange
#     global isOn
#     while True:
#         if (GPIO.input(27)):
#             lastChange = datetime.now()
#         else:
#             if (datetime.now() - lastChange).seconds < 1:
#                 isOn = True
#             else:
#                 isOn = False
#         time.sleep(0.05)
    
# if __name__ == '__main__':
#     try:
#         duration = 2.0
#         fps = 90.0

#         i = 0
#         while 1:
#             colors = [
#                 [255, 0, 0], # red
#                 [0, 0, 255], # blue
#                 [255, 255, 0], # yellow
#                 [255, 0, 232], # purple
#                 [0, 255, 0], # green
#                 [0, 255, 255]  # teal
#             ]

#             currentColor = colors[i % len(colors)]

#             i = (i + 1) % len(colors)
#             nextColor = colors[i]

#             transition(currentColor, nextColor, duration, fps)

#         # close execution by pressing CTRL + C
#     except KeyboardInterrupt:
#         print("Intrerrupted by user")
#         pass
#     finally:
#         setPwm([0, 0, 0])
#         pi.stop()
#         print("Program stopped")
