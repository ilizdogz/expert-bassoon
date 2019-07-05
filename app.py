#!/usr/bin/env/python
from flask import Flask, render_template, jsonify, request
# import RPi.GPIO as GPIO
import time
from transition import transition

app = Flask(__name__)

currentColor = [0, 0, 0]
FPS = 30
TRANSITION_DURATION = 0.5

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/color", methods=["GET"])
def set_color():
    print(request)
    # transition(currentColor, color, TRANSITION_DURATION, FPS)
    # currentColor = color
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)