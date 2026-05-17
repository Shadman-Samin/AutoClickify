from pynput.keyboard import Listener, KeyCode, Key
import threading

class Controller:
    def __init__(self, clicker, profile, state_callback=None):
        self.clicker = clicker
        self.state_callback = state_callback
        self.listener = None
        self.is_key_held = False
        self.update_settings(profile)
        
    def update_settings(self, profile):
        self.start_key = self._parse_key(profile.get('start_key', 'a'))
        self.exit_key = self._parse_key(profile.get('exit_key', 'b'))
        self.mode = profile.get('mode', 'toggle')
        
    def _parse_key(self, key_str):
        if not key_str:
            return KeyCode.from_char('a')
        key_str = str(key_str).lower()
        if len(key_str) == 1:
            return KeyCode.from_char(key_str)
        try:
            return getattr(Key, key_str)
        except AttributeError:
            return KeyCode.from_char(key_str[0])
            
    def _matches_key(self, key, target_key):
        if hasattr(key, 'char') and hasattr(target_key, 'char'):
            if key.char and target_key.char:
                return key.char.lower() == target_key.char.lower()
        return key == target_key
        
    def on_press(self, key):
        if self._matches_key(key, self.start_key):
            if self.mode == 'toggle':
                # Avoid repeat triggers if held down in toggle mode
                if not self.is_key_held:
                    is_clicking = self.clicker.toggle_clicking()
                    if self.state_callback:
                        self.state_callback(is_clicking)
                        
            elif self.mode == 'hold':
                if not self.is_key_held:
                    self.clicker.start_clicking()
                    if self.state_callback:
                        self.state_callback(True)
            self.is_key_held = True
            
        elif self._matches_key(key, self.exit_key):
            self.clicker.exit()
            if self.state_callback:
                self.state_callback(False, exiting=True)
            return False
            
    def on_release(self, key):
        if self._matches_key(key, self.start_key):
            self.is_key_held = False
            if self.mode == 'hold':
                self.clicker.stop_clicking()
                if self.state_callback:
                    self.state_callback(False)
                    
    def start(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()
            
    def stop(self):
        if self.listener:
            self.listener.stop()
