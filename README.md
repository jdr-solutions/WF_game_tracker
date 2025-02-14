# WF_game_tracker

WF_game_tracker is a Python-based graphical application for tracking games in **Warhammer 40000: Warpforge** using Tkinter for its GUI.

## Disclaimer

This project is an unofficial tool and is not affiliated with or endorsed by the creators or publishers of **Warhammer 40000: Warpforge**.

## Prerequisites

- **Python 3.x** must be installed on your system.
- **Tkinter**:  
  While Tkinter is included with Python on many platforms, some Linux distributions (e.g., Ubuntu/Debian) require it to be installed as a separate system package. To install Tkinter, run the following commands **outside** your virtual environment:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-tk
  ```

## Installation & Running the Application

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/WF_game_tracker.git
   cd WF_game_tracker
   ```

2. **(Optional) Create and Activate a Virtual Environment:**
   Although no additional pip packages are required, you can create a virtual environment if desired:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Run the Application:**
   ```bash
   python game_tracker.py
   ```

## Additional Notes

- If you encounter an error like `ModuleNotFoundError: No module named 'tkinter'`, ensure that Tkinter is installed system-wide using the commands listed in the Prerequisites section.
- No external Python libraries are required for this application.

## License

This project is licensed under the MIT License.
