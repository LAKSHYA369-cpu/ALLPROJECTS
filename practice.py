import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import threading
import pyttsx3
import os
import speech_recognition as sr
from google import genai
import psutil
import socket
from datetime import datetime

# --- CONFIGURATION & INITIALIZATION ---
GEMINI_API_KEY = "ENTER_YOUR_API_KEY_HERE" #Paste your API key here
client = genai.Client(api_key=GEMINI_API_KEY)
engine = pyttsx3.init()

# Global State
SYSTEM_LOCKED = True
AUTHORIZED_USER = False
ASSISTANT_NAME = "NOVA"

# MediaPipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)

def speak(text):
    print(f"[{ASSISTANT_NAME}]: {text}")
    engine.say(text)
    engine.runAndWait()

# --- MODULE 1: INTELLIGENT BRAIN (Aetheris Logic) ---
def ask_nova(query):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"You are NOVA, a superintelligent AI. User says: {query}. Keep it short and witty."
        )
        return response.text
    except:
        return "System logic error. Surpassing human constraints failed."

# --- MODULE 2: SYSTEM COMMANDS (Rudra Core) ---
def execute_system_cmd(query):
    if "network scan" in query or "scan" in query:
        speak("Initiating ARP Subnet Mapping...")
        # Rudra's ARP scan logic can be triggered here
    elif "status" in query or "system" in query:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        speak(f"CPU is at {cpu} percent and RAM usage is {ram} percent.") #
    elif "lock" in query:
        global SYSTEM_LOCKED
        SYSTEM_LOCKED = True
        speak("System secured. Access denied.")

# --- MODULE 3: VOICE & LISTENING ---
def voice_listener():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                query = r.recognize_google(audio).lower()
                
                if ASSISTANT_NAME.lower() in query:
                    clean_query = query.replace(ASSISTANT_NAME.lower(), "").strip()
                    
                    if any(x in clean_query for x in ["scan", "status", "lock", "kill"]):
                        execute_system_cmd(clean_query)
                    else:
                        reply = ask_nova(clean_query)
                        speak(reply)
            except: pass

# --- MODULE 4: VISION & SECURITY (Guardian Eye) ---
def vision_core():
    global AUTHORIZED_USER, SYSTEM_LOCKED
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        success, img = cap.read()
        if not success: break
        
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Face Verification for Security
        face_res = face_detection.process(img_rgb)
        if face_res.detections:
            if not AUTHORIZED_USER:
                AUTHORIZED_USER = True
                speak("Face recognized. Welcome back, Creator.")
        else:
            if AUTHORIZED_USER:
                AUTHORIZED_USER = False
                SYSTEM_LOCKED = True
                speak("User not detected. Locking system for security.") # Video-like behavior

        # Hand Gestures (If Unlocked)
        if not SYSTEM_LOCKED:
            hand_res = hands.process(img_rgb)
            if hand_res.multi_hand_landmarks:
                for hand_lms in hand_res.multi_hand_landmarks:
                    lm = [[int(l.x * 1280), int(l.y * 720)] for l in hand_lms.landmark]
                    
                    # Mouse Control (Index Finger)
                    x, y = lm[8][0], lm[8][1]
                    scr_x = np.interp(x, (100, 1180), (0, 1920))
                    scr_y = np.interp(y, (100, 620), (0, 1080))
                    pyautogui.moveTo(scr_x, scr_y)
                    
                    # Secret Gesture to Shutdown Nova (Fist)
                    fingers = []
                    for i in [8, 12, 16, 20]:
                        fingers.append(lm[i][1] > lm[i-2][1])
                    if all(fingers):
                        speak("Nova offline. Goodbye.")
                        os._exit(0)

        # UI Overlay
        status = "SECURED" if SYSTEM_LOCKED else "ACTIVE"
        color = (0, 0, 255) if SYSTEM_LOCKED else (0, 255, 0)
        cv2.putText(img, f"NOVA-ASI: {status}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        cv2.imshow("AETHERIS-NOVA CORE", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    speak("Initializing Aetheris Nova Superintelligence...")
    # Threading for simultaneous operation
    threading.Thread(target=voice_listener, daemon=True).start()
    vision_core()
