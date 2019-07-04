import RPi.GPIO as GPIO
import time
import math
import os

# use channel numbers on the Broadcom SOC
GPIO.setmode(GPIO.BCM)

# defining the pins
GPIO_RED = 4
GPIO_GREEN = 18
GPIO_BLUE = 17

def setPwm(color):
    # file = open("/dev/pi-blaster", "w")
    print(hexPercent(color[0]))
    text = "echo '{}={}, {}={}, {}={}' >> /dev/pi-blaster"
    text = text.format(GPIO_RED, hexPercent(color[0]), GPIO_GREEN, hexPercent(color[1]), GPIO_BLUE, hexPercent(color[2]))
    print(text)
    os.system(text)
    # file.write(f"{GPIO_RED}={hexPercent(color[0])}, {GPIO_GREEN}={hexPercent(color[1])}, {GPIO_BLUE}={hexPercent(color[2])}")
    # file.close()

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
    setPwm(currentColor)

def hexPercent(color):
    percent = (color / float(0xFF)) * 100
    return math.floor(percent)

if __name__ == '__main__':
    try:
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