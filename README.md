# Hand RGB Controller

**Version:** 1.0.0  
**Last Updated:** April 22, 2025

Control an RGB LED using hand gestures detected by your webcam. 
This project uses **MediaPipe** for hand tracking, **OpenCV** for visual interaction, and an **Arduino** to light up RGB LEDs based on finger positioning over color zones on the screen.
## Acknowledgements

- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide) by Google - for powerful hand tracking.
- [OpenCV](https://opencv.org/about/) - for video capture and real-time drawing.
- [Arduino](https://docs.arduino.cc/learn/starting-guide/whats-arduino/) - for microcontroller support and controlling RGB LEDs.

## Demo

![Demo of Hand RGB Controller](demo.gif)

> Hover your finger over the colored zones (red, green, or blue) on your screen.

> Your Arduino will light up the RGB LED to match the zone color.
## Documentation

This project consists of two main components:

### 1. `hand_rgb_controller.py` (Python script)

- Uses MediaPipe and OpenCV to detect your index fingertip position.
- Draws 3 interactive zones (Red, Green, Blue) on the screen.
- Sends RGB values via Serial to an Arduino when the fingertip is detected in a zone.

### 2. `arduino_rgb_receiver.ino` (Arduino sketch)

- Listens for RGB values sent from the Python script via Serial.
- Adjusts the brightness of the RGB LED based on received values using PWM.
## Installation

### Python Environment

Install the required Python packages:

```bash
pip install opencv-python mediapipe pyserial
```

### Arduino

1. Open arduino_rgb_receiver.ino in the Arduino IDE.

2. Upload it to your Arduino board (e.g., UNO)

3. Connect your RGB LED to the correct PWM pins:

4. Red → Pin 9

5. Green → Pin 10

6. Blue → Pin 11

Make sure you're using common cathode RGB LEDs, or adjust your wiring/code ***accordingly***.
## Usage/Examples

### Step 1: Start the Arduino
- Upload and run the Arduino sketch.
- Make sure it's connected to the correct `COM` port (e.g., `COM5` on Windows).

### Step 2: Run the Python script
```bash
python hand_rgb_controller.py
```
- A webcam window will appear with red, green, and blue zones at the top.
- Move your index fingertip (landmark 8) over any zone to activate that color.

> Press Q to quit.
## Feedback

Have an idea to improve this project?
Found a bug or want to add a new feature?
Feel free to open an issue or submit a pull request.

