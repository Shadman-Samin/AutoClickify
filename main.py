import sys
import threading
from config import parse_args, ProfileManager
from clicker import AutoClicker
from controller import Controller

def main():
    args, _ = parse_args()
    
    pm = ProfileManager()
    profile_name = args.profile
    profile = pm.get_profile(profile_name)
    
    # Initialize clicker thread
    clicker = AutoClicker(profile)
    clicker.start()
    
    if args.headless:
        print("\n==============================")
        print(" Auto Clicker (Headless Mode) ")
        print("==============================")
        print(f"Profile: {profile_name}")
        print(f"Start/Stop Key: [{profile.get('start_key')}]")
        print(f"Exit Key: [{profile.get('exit_key')}]")
        print(f"Delay: {profile.get('delay')}s")
        print(f"Mode: {profile.get('mode')}")
        print("==============================\n")
        
        controller = Controller(clicker, profile)
        try:
            controller.start()
        except KeyboardInterrupt:
            clicker.exit()
            
        clicker.join()
        print("Auto Clicker closed.")
    else:
        # GUI Mode
        app = None
        def state_callback(is_clicking, exiting=False):
            if app and hasattr(app, 'root'):
                try:
                    app.root.after(0, lambda: app.update_state_label(is_clicking, exiting))
                except Exception:
                    pass
                    
        controller = Controller(clicker, profile, state_callback)
        
        # Pynput listener needs to run in a background thread to allow Tkinter mainloop
        listener_thread = threading.Thread(target=controller.start, daemon=True)
        listener_thread.start()
        
        try:
            from gui import AutoClickerGUI
            app = AutoClickerGUI(clicker, controller, pm, profile_name)
            app.run()
        except ImportError as e:
            print(f"Error loading GUI: {e}")
            print("Please ensure Tkinter is installed, or run with --headless")
            clicker.exit()
            controller.stop()
            
        clicker.join()

if __name__ == "__main__":
    main()
