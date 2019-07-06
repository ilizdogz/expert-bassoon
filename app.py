#!/usr/bin/env/python
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
# import RPi.GPIO as GPIO
import time
from transition import transition
import json
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

app = Flask(__name__)
CORS(app)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
# checkForButton()
isOn = False
lastChange = datetime.now()

def checkForButton():
    global lastChange
    global isOn
    while True:
        if (GPIO.input(27)):
            lastChange = datetime.now()
        else:
            if (datetime.now() - lastChange).seconds < 1:
                isOn = True
            else:
                isOn = False
        time.sleep(0.05)

currentColor = [0, 0, 0]
FPS = 30
TRANSITION_DURATION = 0.5

@app.route("/")
def main():
    return render_template("index.html", color=currentColor)

@app.route("/color", methods=["POST"])
def set_color():
    global currentColor
    data = request.get_json()
    print(data["color"])
    color = data["color"].lstrip("#")
    color =  list(int(color[i:i+2], 16) for i in (0, 2, 4))
    if isOn:
        color =  list(int(color[i:i+2], 16) for i in (0, 2, 4))
    else:
        color = [0, 0, 0]
    transition(currentColor, color, TRANSITION_DURATION, FPS)
    currentColor = color
    return jsonify({"success": True})

if __name__ == "__main__":
    checkForButton()
    app.run(host='0.0.0.0',debug=True)