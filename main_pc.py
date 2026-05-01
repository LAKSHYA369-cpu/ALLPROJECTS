import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import threading
import pyttsx3
import os
import webbrowser
import speech_recognition as sr

# Settings
pyautogui.PAUSE = 0
CAM_W, CAM_H = 1280, 720
SYSTEM_LOCKED = True
FACE_VERIFIED = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def voice_thread():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                audio = r.listen(source)
                query = r.recognize_google(audio).lower()
                if "airglide" in query and "open chrome" in query:
                    webbrowser.open("https://google.com")
                    speak("Opening Chrome")
            except: pass

threading.Thread(target=voice_thread, daemon=True).start()

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Face Security
    if not FACE_VERIFIED:
        results = face_detection.process(img_rgb)
        if results.detections:
            FACE_VERIFIED = True
            speak("Welcome back. AirGlide is active.")

    # Hand Tracking
    if FACE_VERIFIED:
        hand_res = hands.process(img_rgb)
        if hand_res.multi_hand_landmarks:
            for hand_lms in hand_res.multi_hand_landmarks:
                lm = [[int(l.x * CAM_W), int(l.y * CAM_H)] for l in hand_lms.landmark]
                
                # Mouse Movement (Index Finger)
                x, y = lm[8][0], lm[8][1]
                scr_x = np.interp(x, (100, CAM_W-100), (0, 1920))
                scr_y = np.interp(y, (100, CAM_H-100), (0, 1080))
                pyautogui.moveTo(scr_x, scr_y)

                # Unlock Gesture (L-Shape: Thumb & Index)
                if lm[4][1] < lm[3][1] and lm[8][1] < lm[6][1] and SYSTEM_LOCKED:
                    SYSTEM_LOCKED = False
                    speak("System Unlocked.")

    cv2.imshow("AirGlide PC", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break
cap.release()
cv2.destroyAllWindows()