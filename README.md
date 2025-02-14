# WF Game Tracker

WF Game Tracker is a Python-based graphical application for tracking games in **Warhammer 40000: Warpforge**, built using **Tkinter** for its GUI.

## 🚨 Disclaimer

This project is an **unofficial tool** and is **not affiliated with or endorsed** by the creators or publishers of **Warhammer 40000: Warpforge**.

## 🛠 Prerequisites

- **Python 3.10+** must be installed on your system.
- **Tkinter**:  
  While Tkinter is included with Python on many platforms, some Linux distributions (e.g., Ubuntu/Debian) require it to be installed separately.  
  Install it **outside** your virtual environment:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-tk
  ```

## 🚀 Installation & Running the Application

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/WF_game_tracker.git
cd WF_game_tracker
```

### **2️⃣ Create and Activate a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows (PowerShell)
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Application**
```bash
make run
```

## 🔬 Running Tests

This project includes **unit tests** using `pytest`.  
To run all tests:
```bash
make test
```

To run tests with **code coverage**:
```bash
make coverage
```

> Tests are run **headlessly** using `xvfb-run` to support Tkinter.

## 🧹 Code Formatting & Linting

This project enforces **code quality** using:
- [Black](https://black.readthedocs.io/en/stable/) (auto-formatting)
- [Flake8](https://flake8.pycqa.org/en/latest/) (linting)

### **Run Linting**
```bash
make lint
```

### **Auto-Fix Formatting**
```bash
make format
```

## 🛠 Makefile Commands

Instead of long CLI commands, you can use **Makefile shortcuts**:

| Command        | Description                           |
|---------------|---------------------------------------|
| `make run`     | Start the application (`python run.py`) |
| `make test`    | Run all tests with `pytest`          |
| `make coverage`| Run tests with coverage analysis     |
| `make lint`    | Run code style checks (`flake8`)     |
| `make format`  | Auto-format code with Black          |

To see all available commands:
```bash
make help
```

## 🏗 GitHub Actions (CI/CD)

This repository includes **GitHub Actions** for:
- ✅ **Automated testing**
- ✅ **Code linting**
- ✅ **Coverage reporting**


## 📝 License

This project is licensed under the **MIT License**.
