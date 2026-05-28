import tkinter as tk
from tkinter import ttk, messagebox
import time

class AutoClickerGUI:
    def __init__(self, clicker, controller, profile_manager, current_profile_name):
        self.clicker = clicker
        self.controller = controller
        self.profile_manager = profile_manager
        
        self.root = tk.Tk()
        self.root.title("AutoClickify")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self._setup_ui()
        self.load_profile_to_ui(current_profile_name)
        
        # Start CPS updater loop
        self.update_cps()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def _setup_ui(self):
        # Top Frame - Profiles
        profile_frame = ttk.LabelFrame(self.root, text="Profile Management")
        profile_frame.pack(fill="x", padx=10, pady=5)
        
        self.profile_var = tk.StringVar()
        self.profile_cb = ttk.Combobox(profile_frame, textvariable=self.profile_var, state="readonly")
        self.profile_cb['values'] = list(self.profile_manager.profiles.keys())
        self.profile_cb.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        self.profile_cb.bind('<<ComboboxSelected>>', self.on_profile_select)
        
        ttk.Button(profile_frame, text="Save", command=self.save_profile).pack(side="left", padx=2)
        ttk.Button(profile_frame, text="Delete", command=self.delete_profile).pack(side="left", padx=5)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Configuration")
        settings_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Layout configuring
        settings_frame.columnconfigure(1, weight=1)
        
        # Delay
        ttk.Label(settings_frame, text="Delay (seconds):").grid(row=0, column=0, padx=5, pady=8, sticky="e")
        self.delay_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.delay_var, width=15).grid(row=0, column=1, sticky="w")
        
        # Button
        ttk.Label(settings_frame, text="Mouse Button:").grid(row=1, column=0, padx=5, pady=8, sticky="e")
        self.button_var = tk.StringVar()
        ttk.Combobox(settings_frame, textvariable=self.button_var, values=["left", "right"], state="readonly", width=12).grid(row=1, column=1, sticky="w")
        
        # Mode
        ttk.Label(settings_frame, text="Click Mode:").grid(row=2, column=0, padx=5, pady=8, sticky="e")
        self.mode_var = tk.StringVar()
        ttk.Combobox(settings_frame, textvariable=self.mode_var, values=["toggle", "hold"], state="readonly", width=12).grid(row=2, column=1, sticky="w")
        
        # Hotkeys
        ttk.Label(settings_frame, text="Start/Stop Key:").grid(row=3, column=0, padx=5, pady=8, sticky="e")
        self.start_key_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.start_key_var, width=15).grid(row=3, column=1, sticky="w")
        
        ttk.Label(settings_frame, text="Exit Key:").grid(row=4, column=0, padx=5, pady=8, sticky="e")
        self.exit_key_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.exit_key_var, width=15).grid(row=4, column=1, sticky="w")

        # Jitter
        self.jitter_var = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="Enable Human-like Jitter (Random delay offset)", variable=self.jitter_var).grid(row=5, column=0, columnspan=2, padx=5, pady=8)
        
        ttk.Button(settings_frame, text="Apply Settings", command=self.apply_settings).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Status Frame
        status_frame = ttk.LabelFrame(self.root, text="Live Status")
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="STOPPED", foreground="red", font=("Helvetica", 16, "bold"))
        self.status_label.pack(pady=5)
        
        self.cps_label = ttk.Label(status_frame, text="CPS: 0 | Total Clicks: 0", font=("Helvetica", 11))
        self.cps_label.pack(pady=5)
        
    def load_profile_to_ui(self, name):
        profile = self.profile_manager.get_profile(name)
        self.profile_var.set(name)
        self.delay_var.set(str(profile.get('delay', 0.01)))
        self.button_var.set(profile.get('button', 'left'))
        self.mode_var.set(profile.get('mode', 'toggle'))
        self.jitter_var.set(profile.get('jitter', False))
        self.start_key_var.set(profile.get('start_key', 'a'))
        self.exit_key_var.set(profile.get('exit_key', 'b'))
        
    def on_profile_select(self, event):
        self.load_profile_to_ui(self.profile_var.get())
        self.apply_settings()
        
    def save_profile(self):
        name = self.profile_var.get()
        if name == "Default":
            name = "Custom"
            
        profile = {
            "delay": float(self.delay_var.get()),
            "button": self.button_var.get(),
            "mode": self.mode_var.get(),
            "jitter": self.jitter_var.get(),
            "jitter_pct": 0.2,
            "start_key": self.start_key_var.get(),
            "exit_key": self.exit_key_var.get()
        }
        self.profile_manager.save_profile(name, profile)
        self.profile_cb['values'] = list(self.profile_manager.profiles.keys())
        self.profile_var.set(name)
        messagebox.showinfo("Success", f"Profile '{name}' saved!")
        self.apply_settings()

    def delete_profile(self):
        name = self.profile_var.get()
        if name == "Default":
            messagebox.showwarning("Error", "Cannot delete Default profile.")
            return
        self.profile_manager.delete_profile(name)
        self.profile_cb['values'] = list(self.profile_manager.profiles.keys())
        self.load_profile_to_ui("Default")
        self.apply_settings()
        
    def apply_settings(self):
        try:
            profile = {
                "delay": float(self.delay_var.get()),
                "button": self.button_var.get(),
                "mode": self.mode_var.get(),
                "jitter": self.jitter_var.get(),
                "jitter_pct": 0.2,
                "start_key": self.start_key_var.get(),
                "exit_key": self.exit_key_var.get()
            }
            self.clicker.update_settings(profile)
            self.controller.update_settings(profile)
        except ValueError:
            messagebox.showerror("Error", "Invalid delay value. Please enter a valid number.")

    def update_state_label(self, is_clicking, exiting=False):
        if exiting:
            self.root.quit()
            return
            
        if is_clicking:
            self.status_label.config(text="CLICKING", foreground="green")
        else:
            self.status_label.config(text="STOPPED", foreground="red")
            
    def update_cps(self):
        cps = self.clicker.get_cps()
        total = self.clicker.total_clicks
        self.cps_label.config(text=f"CPS: {cps} | Total Clicks: {total}")
        self.root.after(100, self.update_cps)
        
    def on_close(self):
        self.clicker.exit()
        self.controller.stop()
        self.root.destroy()
        
    def run(self):
        self.root.mainloop()
