#!/usr/bin/env/python
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
# import RPi.GPIO as GPIO
import time
from transition import transition
import json

app = Flask(__name__)
CORS(app)

currentColor = [0, 0, 0]
FPS = 30
TRANSITION_DURATION = 0.5

@app.route("/")
def main():
    return render_template("index.html", color=currentColor)

@app.route("/color", methods=["POST"])
def set_color():
    data = json.loads(request.get_json())
    print(data)
    # print(request.get_json())
    # transition(currentColor, color, TRANSITION_DURATION, FPS)
    # currentColor = color
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)