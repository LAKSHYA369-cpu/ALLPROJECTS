from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import mediapipe as mp
import time

class AirGlideMobile(App):
    def build(self):
        self.img = Image()
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.last_tap = 0
        Clock.schedule_interval(self.update, 1.0/30.0)
        return self.img

    def update(self, dt):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = self.hands.process(rgb)
            
            if res.multi_hand_landmarks:
                for hlms in res.multi_hand_landmarks:
                    # Double Tap detection
                    tip = hlms.landmark[8]
                    if tip.y < hlms.landmark[6].y - 0.05:
                        now = time.time()
                        if now - self.last_tap < 0.3:
                            print("DOUBLE TAP DETECTED")
                        self.last_tap = now
            
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

if __name__ == '__main__':
    AirGlideMobile().run()