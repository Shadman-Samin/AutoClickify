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

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shadman-Samin/AutoClickify.git
   cd AutoClickify
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   Make sure to install the required libraries. If a `requirements.txt` is present, run:
   ```bash
   pip install -r requirements.txt
   ```
   Otherwise, install `pynput` and GUI requirements manually:
   ```bash
   pip install pynput
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Use the GUI to configure your desired click interval, mouse button (left/right/middle), and hotkeys.
3. Start the clicker using the configured hotkey or the start button in the UI.
4. Stop the clicker using the hotkey or the stop button.

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
