#!/usr/bin/env/python
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
# import RPi.GPIO as GPIO
import time
from transition import transition
import json
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import threading

app = Flask(__name__)
CORS(app)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)
# checkForButton()
isOn = False
currentColor = "#000000"
savedColor = "#000000"
FPS = 30
TRANSITION_DURATION = 0.5

def checkForButton():
    global isOn
    global currentColor
    global savedColor
    lastChange = datetime.now()
    while True:
        if (GPIO.input(27)):
            if savedColor != currentColor:
                transition(currentColor, savedColor, TRANSITION_DURATION, FPS)
                currentColor = savedColor
                print("On! Saved: {} Current: {}".format(savedColor, currentColor))
            lastChange = datetime.now()
        else:
            if (datetime.now() - lastChange).seconds < 1:
                isOn = True
            else:
                isOn = False
                if not currentColor == "#000000":
                    savedColor = currentColor
                    currentColor = "#000000"
                    print("Off! Saved: {} Current: {}".format(savedColor, currentColor))
                    transition(currentColor, currentColor, TRANSITION_DURATION, FPS)
        time.sleep(0.05)

@app.route("/")
def main():
    return render_template("index.html", color=currentColor)

@app.route("/color", methods=["POST"])
def set_color():
    global currentColor
    data = request.get_json()
    print(data["color"])
    color = data["color"] #if isOn else "#000000"
    # print("Color: {} isOn: {}".format(color, isOn))
    transition(currentColor, color, TRANSITION_DURATION, FPS)
    currentColor = color
    return jsonify({"success": True})

if __name__ == "__main__":
    # thread = threading.Thread(target=checkForButton, daemon=True)
    # thread.start()
    app.run(host='0.0.0.0',debug=True)
