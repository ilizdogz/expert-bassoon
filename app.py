#!/usr/bin/env/python
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
# import RPi.GPIO as GPIO
import time
from transition import transition, checkForButton
import json

app = Flask(__name__)
CORS(app)
checkForButton()

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
    transition(currentColor, color, TRANSITION_DURATION, FPS)
    currentColor = color
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)