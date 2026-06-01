# AutoClickify

AutoClickify is a production-quality, cross-platform Auto Clicker application built in Python. It offers a robust and modular architecture to automate repetitive clicking tasks efficiently, ensuring system stability through thread-safe operations.

## Features

- **Automated Clicking**: Simulates rapid mouse clicks to save time and effort.
- **Graphical User Interface (GUI)**: Easy-to-use interface for configuring click settings and managing profiles.
- **Configurable Intervals**: Set custom delays between clicks to suit different scenarios.
- **Hotkey Toggling**: Start and stop the auto-clicker instantly using dedicated hotkeys.
- **Thread-Safe Operations**: Clean threading and shutdown procedures for smooth performance without freezing your system.
- **Cross-Platform Compatibility**: Works seamlessly across multiple operating systems.
- **Profile Management**: Save and load different clicking configurations for various tasks.

## Requirements

- Python 3.x
- `pynput` (for mouse and keyboard control)
- Other dependencies as required by the GUI framework (e.g., `customtkinter`, `tkinter`)

## Installation & Usage

### Running from Source
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shadman-Samin/AutoClickify.git
   cd AutoClickify
   ```

2. **Install dependencies:**
   ```bash
   pip install pynput
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Running Standalone (Windows)
If you have built the executable, you can run `AutoClickify.exe` directly from the root directory. No command prompt will open, only the GUI.

**Download the latest release:**
<a href="https://mega.nz/file/1l8k2B7Y#7cHzzfbavP9psWBsG2vynP4sex7Wk4CDk9UAYetMVsA" target="_blank">Download AutoClickify.exe from MEGA</a>

## Building the Executable
To rebuild the standalone executable without a console window:
```bash
pyinstaller --onefile --noconsole --distpath . --name AutoClickify --clean main.py
```

## Architecture

- **`main.py`**: The entry point of the application.
- **`gui.py`**: Manages the graphical user interface.
- **`clicker.py`**: Handles the core clicking logic using `pynput`.
- **`controller.py`**: Acts as a bridge between the GUI and the underlying clicker mechanism, managing threads and hotkeys.
- **`config.py`**: Handles application configuration and settings.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## License

This project is licensed under the MIT License.
