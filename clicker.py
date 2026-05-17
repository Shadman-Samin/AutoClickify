import time
import threading
import random
from collections import deque
from pynput.mouse import Controller, Button

class AutoClicker(threading.Thread):
    def __init__(self, profile):
        super().__init__()
        self.mouse = Controller()
        
        # Threading events for safe concurrency
        self.running_event = threading.Event()
        self.clicking_event = threading.Event()
        
        self.running_event.set()
        self.clicking_event.clear()
        
        # Stats
        self.click_times = deque(maxlen=200)
        self.total_clicks = 0
        
        self.update_settings(profile)
        
    def update_settings(self, profile):
        self.delay = float(profile.get('delay', 0.01))
        btn_str = profile.get('button', 'left').lower()
        self.button = Button.left if btn_str == 'left' else Button.right
        self.jitter = profile.get('jitter', False)
        self.jitter_pct = float(profile.get('jitter_pct', 0.2))

    def start_clicking(self):
        self.clicking_event.set()
        
    def stop_clicking(self):
        self.clicking_event.clear()
        
    def exit(self):
        self.stop_clicking()
        self.running_event.clear()
        
    def toggle_clicking(self):
        if self.clicking_event.is_set():
            self.stop_clicking()
            return False
        else:
            self.start_clicking()
            return True
            
    def get_cps(self):
        now = time.time()
        # Remove old clicks older than 1 second
        while self.click_times and self.click_times[0] < now - 1.0:
            self.click_times.popleft()
        return len(self.click_times)
            
    def run(self):
        while self.running_event.is_set():
            if not self.clicking_event.is_set():
                self.clicking_event.wait(timeout=0.1)
                continue
                
            # Perform click
            self.mouse.click(self.button)
            self.total_clicks += 1
            self.click_times.append(time.time())
            
            # Calculate sleep with optional jitter
            sleep_time = self.delay
            if self.jitter:
                offset = sleep_time * self.jitter_pct
                sleep_time = random.uniform(max(0, sleep_time - offset), sleep_time + offset)
                
            time.sleep(sleep_time)
