# PSH Rent Calculator - Installation Guide

## 🚀 Quick Installation (Recommended)

### Step 1: Download Files
Download all files to a folder on your computer (e.g., Desktop/PSH-Calculator)

### Step 2: Run Setup
**Windows:**
1. Double-click `setup.py` 
2. If that doesn't work, open Command Prompt and type: `python setup.py`

**Mac/Linux:**
1. Open Terminal
2. Navigate to the folder: `cd /path/to/PSH-Calculator`
3. Run: `python3 setup.py`

### Step 3: Start Using
After setup completes:
- **Windows:** Double-click `start_calculator.bat`
- **Mac/Linux:** Double-click `start_calculator.sh`
- **Any System:** `python start_calculator.py`

---

## 🔧 Manual Installation

If automatic setup doesn't work, follow these manual steps:

### 1. Check Python Installation
```bash
# Check if Python is installed
python --version
# or try
python3 --version

# Should show Python 3.6 or higher
```

### 2. Create Virtual Environment
```bash
# Create isolated environment for the app
python3 -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install required packages
pip install openpyxl

# Verify installation
python -c "import openpyxl; print('Success!')"
```

### 4. Run the Calculator
```bash
# With virtual environment activated
python psh_calculator.py
```

---

## 🐛 Troubleshooting

### "Python is not recognized"
**Windows:**
1. Download Python from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart Command Prompt

**Mac:**
- Install with Homebrew: `brew install python3`
- Or download from https://python.org

### "tkinter not found"
**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Other Linux:**
```bash
# CentOS/RHEL
sudo yum install tkinter
# or
sudo dnf install python3-tkinter
```

### "Permission denied"
**Mac/Linux:**
```bash
chmod +x setup.py
chmod +x start_calculator.sh
```

**Windows:**
- Right-click → "Run as Administrator"

### "Virtual environment failed"
Try installing virtualenv manually:
```bash
pip install virtualenv
virtualenv venv
```

### Excel Files Won't Open
Install a spreadsheet program:
- **Microsoft Excel** (paid)
- **LibreOffice Calc** (free) - https://libreoffice.org
- **Google Sheets** (web-based, free)

---

## 📁 File Structure

After installation, you should have:

```
PSH-Calculator/
├── psh_calculator.py      # Main application
├── setup.py               # Automatic setup script
├── requirements.txt       # Python dependencies
├── README.md              # Technical documentation
├── USER_GUIDE.md          # User instructions
├── INSTALLATION.md        # This file
├── run_calculator.py      # Simple launcher
├── run_calculator.bat     # Windows launcher
├── run_calculator.sh      # Mac/Linux launcher
├── start_calculator.py    # Venv launcher (created by setup)
├── start_calculator.bat   # Windows venv launcher (created by setup)
├── start_calculator.sh    # Mac/Linux venv launcher (created by setup)
└── venv/                  # Virtual environment (created by setup)
    ├── bin/               # Executables (Mac/Linux)
    ├── Scripts/           # Executables (Windows)
    └── lib/               # Python packages
```

---

## 🔄 Updates and Maintenance

### Updating FMR Rates
1. Start the calculator
2. Go to "Settings" tab
3. Update the rates
4. Click "Save FMR Rates"

### Backing Up Settings
1. Go to "Settings" tab
2. Click "Export Settings"
3. Save the JSON file somewhere safe

### Installing on Multiple Computers
1. Copy the entire folder to the new computer
2. Run `setup.py` on each computer
3. Import settings from your backup JSON file

---

## 💡 Tips for IT Administrators

### Network Deployment
- Copy the folder to a shared network location
- Have users run `setup.py` from their local machines
- Share FMR settings files via "Export/Import Settings"

### Security Considerations  
- Application works entirely offline
- No network connections made
- All data stored locally
- Excel files saved to user-specified locations

### System Requirements
- **OS:** Windows 7+, macOS 10.10+, Linux (any modern distribution)
- **Python:** 3.6 or higher
- **Memory:** 50MB RAM for the application
- **Disk:** 10MB for program files, plus space for Excel outputs
- **Spreadsheet Program:** Excel, LibreOffice, or similar for viewing reports

### Corporate Installation
```bash
# Silent installation script for corporate environments
python3 setup.py --silent --no-start
# Then deploy start_calculator.bat to desktops
```

---

## 📞 Support

### Self-Help
1. Check this installation guide
2. Read the USER_GUIDE.md
3. Try the built-in help tab

### Common Solutions
- **Won't start:** Reinstall Python with PATH option
- **Missing openpyxl:** Run `pip install openpyxl` 
- **Excel issues:** Install LibreOffice as free alternative
- **Permission errors:** Run as administrator

### When to Contact IT
- Python installation fails repeatedly
- Virtual environment creation fails
- Network/permission issues
- Need help with corporate deployment

---

*Installation should take 2-3 minutes on most systems*