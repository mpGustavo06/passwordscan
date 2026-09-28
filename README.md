# passwordscan

A simple command-line tool to check if a password has appeared in a known data breach, using the [Have I Been Pwned](https://haveibeenpwned.com/) k-anonymity API.

It runs 100% locally in your terminal (Windows, Linux, macOS, WSL) and **never sends your password or its full hash** over the network — only the first 5 characters of the SHA-1 hash are transmitted.

## Features

- Check a single password, an interactive hidden prompt, or a whole file (batch mode)
- Zero data exposure: k-anonymity range API (only a 5-character hash prefix leaves your machine)
- Clean English output and meaningful exit codes (`0` = success, `1` = failure)
- Works on Windows, Linux, macOS and WSL
- No API key or account required

## Requirements

- Python 3.10+
- pip (comes with Python)
- Git (optional — you can also download the ZIP)
- Internet access (to reach the HIBP range API)

---

## 1. Install Python (skip if you already have it)

Check first — run this in your terminal:

```bash
python3 --version    # Linux / macOS / WSL
python --version     # Windows (Command Prompt / PowerShell)
```

If you see something like `Python 3.10.x` or newer, you are ready. Otherwise, install it:

### Windows

Option A — winget (built into Windows 10/11):

```powershell
winget install Python.Python.3.12
```

Option B — installer:

1. Download the installer from [python.org/downloads](https://www.python.org/downloads/windows/)
2. Run it and **check "Add python.exe to PATH"** (very important!)
3. Click "Install Now"

Verify in a **new** terminal window:

```powershell
python --version
pip --version
```

### Linux (Debian/Ubuntu/WSL)

```bash
sudo apt update && sudo apt install -y python3 python3-pip
```

### Linux (Fedora)

```bash
sudo dnf install -y python3 python3-pip
```

### Linux (Arch)

```bash
sudo pacman -S python python-pip
```

### macOS

```bash
brew install python3
```

Or download the installer from [python.org](https://www.python.org/downloads/).

> **Note:** On Windows the commands are `python` and `pip`. On Linux/macOS/WSL they are `python3` and `pip3` (or `python -m pip`). The examples below show both.

---

## 2. Get the project

### With Git (all platforms)

```bash
git clone https://github.com/<your-username>/passwordscan.git
cd passwordscan
```

### Without Git (all platforms)

1. Download the ZIP: green **Code** button → **Download ZIP** on the GitHub page
2. Extract it anywhere
3. Open a terminal in the extracted folder

**Windows tip:** in File Explorer, type `cmd` or `powershell` in the folder's address bar to open a terminal there.

---

## 3. Install dependencies

```bash
pip install -r requirements.txt     # Windows
pip3 install -r requirements.txt    # Linux / macOS / WSL
```

If `pip` is not found, use:

```bash
python -m pip install -r requirements.txt     # Windows
python3 -m pip install -r requirements.txt    # Linux / macOS / WSL
```

---

## 4. Usage

```bash
# Check a password passed as an argument
python3 checkpw.py "Tr7#qLp9!vXe2&Wm"     # Linux / macOS / WSL
python  checkpw.py "Tr7#qLp9!vXe2&Wm"     # Windows

# Check a password via a hidden interactive prompt
python3 checkpw.py
python  checkpw.py

# Check many passwords from a file (one per line)
python3 checkpw.py -f passwords.txt

# Show help
python3 checkpw.py --help
```

## Example output

```
Not breached (0 times)
Breached 52372427 times
```

Exit codes: `0` = success, `1` = network/read failure.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `'python' is not recognized` (Windows) | Reinstall Python and check **"Add python.exe to PATH"**, then open a **new** terminal |
| `'python3' is not found` (Linux/macOS) | Install it: `sudo apt install python3` (Debian/Ubuntu) or `brew install python3` (macOS) |
| `ModuleNotFoundError: No module named 'requests'` | Run `pip install -r requirements.txt` (or `python3 -m pip ...`) |
| `pip: command not found` | Use `python3 -m pip install -r requirements.txt` |
| `Permission denied` / `EACCES` on Linux/macOS | Use `python3 -m pip install --user -r requirements.txt` |
| Network error / timeout | Check your internet connection; the tool needs access to `api.pwnedpasswords.com` |

---

## How it works

1. Compute `SHA-1(password)` and convert it to uppercase hex.
2. Send only the **first 5 characters** (the prefix) to `https://api.pwnedpasswords.com/range/{prefix}`.
3. Search the remaining suffix in the response and return the breach count.

The full password and full hash never leave your machine.

## Project layout

```
passwordscan/
├── checkpw.py         # CLI tool
├── requirements.txt   # Dependencies (requests)
├── README.md
└── .gitignore
```

## License

MIT
