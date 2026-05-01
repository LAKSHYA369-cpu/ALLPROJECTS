import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import keyboard  # Install using: pip install keyboard

# Performance Optimization
pyautogui.PAUSE = 0

class TechGestureKeyboard:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
        self.mp_draw = mp.solutions.drawing_utils
        
        self.show_keyboard = False
        self.keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                     ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
                     ["Z", "X", "C", "V", "B", "N", "M"]]
        
        # Button settings
        self.btn_w, self.btn_h = 60, 60
        self.start_x, self.start_y = 50, 150

    def draw_keyboard(self, img):
        # Create a tech-style transparent overlay
        overlay = img.copy()
        for i, row in enumerate(self.keys):
            for j, key in enumerate(row):
                x = self.start_x + j * (self.btn_w + 10) + (i * 20)
                y = self.start_y + i * (self.btn_h + 10)
                # Neon Blue Rectangles
                cv2.rectangle(overlay, (x, y), (x + self.btn_w, y + self.btn_h), (255, 255, 0), -1)
                cv2.putText(overlay, key, (x + 15, y + 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        # Merge with transparency
        return cv2.addWeighted(overlay, 0.4, img, 0.6, 0)

    def check_trigger(self):
        # Detect physical keys K + E + Y
        if keyboard.is_pressed('k') and keyboard.is_pressed('e') and keyboard.is_pressed('y'):
            self.show_keyboard = not self.show_keyboard
            print(f"Keyboard Visibility: {self.show_keyboard}")
            time.sleep(0.3) # Debounce

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        while cap.isOpened():
            success, img = cap.read()
            if not success: break
            img = cv2.flip(img, 1)
            
            self.check_trigger()

            if self.show_keyboard:
                img = self.draw_keyboard(img)
                results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                
                if results.multi_hand_landmarks:
                    lm = results.multi_hand_landmarks[0].landmark
                    # Index (8) and Thumb (4) tips
                    h, w, _ = img.shape
                    thumb = (int(lm[4].x * w), int(lm[4].y * h))
                    index = (int(lm[8].x * w), int(lm[8].y * h))

                    # Draw a tech-line between Index and Thumb
                    cv2.line(img, thumb, index, (0, 255, 255), 2)
                    
                    # Pinch detection (Distance between thumb and index)
                    dist = np.hypot(thumb[0] - index[0], thumb[1] - index[1])
                    
                    if dist < 30: # Pinch Triggered
                        cv2.circle(img, index, 10, (0, 0, 255), -1)
                        # Check which key is pressed
                        for i, row in enumerate(self.keys):
                            for j, key in enumerate(row):
                                kx = self.start_x + j * (self.btn_w + 10) + (i * 20)
                                ky = self.start_y + i * (self.btn_h + 10)
                                if kx < index[0] < kx + self.btn_w and ky < index[1] < ky + self.btn_h:
                                    pyautogui.press(key.lower())
                                    cv2.rectangle(img, (kx, ky), (kx+self.btn_w, ky+self.btn_h), (0, 255, 0), -1)
                                    cv2.waitKey(200) # Typing delay

            cv2.imshow("Tech Lightning Keyboard", img)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import time
    TechGestureKeyboard().run()