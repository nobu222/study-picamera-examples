from flask import Flask, render_template, Response

from pyzbar import pyzbar
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import numpy as np
import cv2
import time

from processor.simple_streamer import SimpleStreamer as VideoCamera
# from processor.pedestrian_detector import PedestrianDetector as VideoCamera
# from processor.motion_detector import MotionDetector as VideoCamera
import time
import threading

video_camera = VideoCamera(flip=False)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.5)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)

@app.route('/stream')
def stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def get_frame():
    camera.capture(rawCapture, format="bgr", use_video_port=True)
    frame = rawCapture.array
    decoded_objs = decode(frame)
    frame = display(frame, decoded_objs)
    ret, jpeg = cv2.imencode('.jpg', frame)
    rawCapture.truncate(0)
    return jpeg.tobytes()
    