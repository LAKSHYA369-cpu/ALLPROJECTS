import socketio
import eventlet
import pyautogui
from flask import Flask

# Speed up PyAutoGUI
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

sio = socketio.Server(cors_allowed_origins='*')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@sio.on('connect')
def connect(sid, environ):
    print(f"Phone Connected: {sid}")

@sio.on('move')
def handle_move(sid, data):
    # Data contains relative movement (dx, dy)
    dx = data.get('dx', 0)
    dy = data.get('dy', 0)
    sensitivity = 1.5 
    pyautogui.moveRel(dx * sensitivity, dy * sensitivity)

@sio.on('click')
def handle_click(sid):
    pyautogui.click()

if __name__ == '__main__':
    print("Server starting... Connect phone to USB Tethering.")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)