from flask import Flask, render_template, jsonify
# import RPi.GPIO as GPIO
import time
from .transition import transition

currentColor = [0, 0, 0]
FPS = 30
TRANSITION_DURATION = 0.5

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/color/<color>", methods=["POST"])
def set_color(color):
    print(color)
    # transition(currentColor, color, TRANSITION_DURATION, FPS)
    # currentColor = color
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)