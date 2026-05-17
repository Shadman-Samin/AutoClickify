import json
import os
import argparse

PROFILES_FILE = "profiles.json"
DEFAULT_PROFILE = {
    "delay": 0.01,
    "button": "left",
    "start_key": "a",
    "exit_key": "b",
    "mode": "toggle", # toggle or hold
    "jitter": False,
    "jitter_pct": 0.2
}

class ProfileManager:
    def __init__(self):
        self.profiles = {"Default": DEFAULT_PROFILE.copy()}
        self.load_profiles()

    def load_profiles(self):
        if os.path.exists(PROFILES_FILE):
            try:
                with open(PROFILES_FILE, 'r') as f:
                    data = json.load(f)
                    self.profiles.update(data)
            except Exception as e:
                print(f"Error loading profiles: {e}")

    def save_profiles(self):
        try:
            with open(PROFILES_FILE, 'w') as f:
                json.dump(self.profiles, f, indent=4)
        except Exception as e:
            print(f"Error saving profiles: {e}")

    def get_profile(self, name):
        return self.profiles.get(name, self.profiles["Default"]).copy()

    def save_profile(self, name, profile_data):
        self.profiles[name] = profile_data
        self.save_profiles()
        
    def delete_profile(self, name):
        if name in self.profiles and name != "Default":
            del self.profiles[name]
            self.save_profiles()

def parse_args():
    parser = argparse.ArgumentParser(description="Cross-platform Auto Clicker CLI & GUI")
    parser.add_argument('--headless', action='store_true', help="Run without GUI")
    parser.add_argument('-p', '--profile', type=str, default="Default", help="Profile to load")
    return parser.parse_known_args()
