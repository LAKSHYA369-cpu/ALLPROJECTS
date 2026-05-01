import ctypes
import win32gui
import win32con
import time
import threading
import tkinter as tk
import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# --- UNDOCUMENTED WINDOWS ACCENT API ---
class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_int),
        ("AccentFlags", ctypes.c_int),
        ("GradientColor", ctypes.c_int),
        ("AnimationId", ctypes.c_int),
    ]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.POINTER(ACCENT_POLICY)),
        ("SizeOfData", ctypes.c_size_t),
    ]

def apply_crystal_transparency():
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    if not hwnd: return

    accent = ACCENT_POLICY()
    # State 3 + Gradient 0 = 100% Clear Transparent (No Blur, No Grey)
    accent.AccentState = 3 
    accent.GradientColor = 0x00000000 
    
    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19  # WCA_ACCENT_POLICY
    data.SizeOfData = ctypes.sizeof(accent)
    data.Data = ctypes.pointer(accent)
    
    ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

# --- VOLUME API ---
def get_vol_api():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    except: return None

vol_api = get_vol_api()

# --- REAL ONE UI 6.1 UI ---
class OneUIVolume:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        # One UI 6.1 uses a very subtle dark blur-like bg
        self.root.configure(bg='#1a1a1a')
        self.root.attributes("-alpha", 0.98)

        # Container for the Rounded Pill (One UI Style)
        # Width increased for a more 'Phone' look
        self.canvas = tk.Canvas(self.root, width=50, height=260, bg='#1a1a1a', highlightthickness=0)
        self.canvas.pack(pady=10)

        # Track (The empty part of the slider)
        # Using rounded shape logic via CreateRoundRect (simplified here with Canvas)
        self.canvas.create_rectangle(15, 20, 35, 220, fill="#333333", outline="", tags="track")
        # Fill (The Blue Volume part)
        self.fill = self.canvas.create_rectangle(15, 220, 35, 220, fill="#3e8ede", outline="", tags="fill")
        
        self.label = tk.Label(self.root, text="0", fg="white", bg='#1a1a1a', font=("Segoe UI Variable", 11, "bold"))
        self.label.pack()

        # Binding Mouse for Dragging
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-1>", self.on_drag)
        
        self.is_visible = False

    def on_drag(self, event):
        if not vol_api: return
        y = event.y - 20
        # Normalizing 0 to 200px
        val = 1 - (y / 200)
        val = max(0, min(1, val))
        vol_api.SetMasterVolumeLevelScalar(val, None)
        self.update_view()

    def update_view(self):
        if not vol_api: return
        v = vol_api.GetMasterVolumeLevelScalar()
        y_fill = 220 - (v * 200)
        self.canvas.coords(self.fill, 15, y_fill, 35, 220)
        self.label.config(text=str(int(v * 100)))

    def toggle(self):
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
        else:
            self.update_view()
            sw, sh = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
            # Center-Right position
            self.root.geometry(f"70x310+{sw-90}+{sh//2-155}")
            self.root.deiconify()
            self.is_visible = True
            # Auto-hide
            threading.Timer(2.5, self.root.withdraw).start()

def taskbar_loop():
    while not stop_event.is_set():
        apply_crystal_transparency()
        time.sleep(1)

def restore():
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    if hwnd:
        accent = ACCENT_POLICY()
        accent.AccentState = 0
        data = WINDOWCOMPOSITIONATTRIBDATA(19, ctypes.pointer(accent), ctypes.sizeof(accent))
        ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

if __name__ == "__main__":
    app = OneUIVolume()
    stop_event = threading.Event()

    # Hotkey registration
    keyboard.add_hotkey('ctrl+shift+space+enter', app.toggle)
    
    # Transparency Thread
    threading.Thread(target=taskbar_loop, daemon=True).start()

    print("Nexus X Active: Crystal Taskbar + One UI Volume")
    
    try:
        app.root.mainloop()
    except:
        pass
    finally:
        stop_event.set()
        restore()