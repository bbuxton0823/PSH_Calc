@echo off
title PSH Rent Calculator - Web Edition

cls
echo ╔════════════════════════════════════════╗
echo ║       PSH RENT CALCULATOR - 2026      ║
echo ║           Web Edition                  ║
echo ║                                        ║
echo ║    ✨ Beautiful ✨ Simple ✨ Fast     ║
echo ╚════════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    echo.
    echo 📥 Opening Python download page...
    start https://python.org/downloads
    echo.
    echo Please install Python and check "Add Python to PATH"
    echo Then run this file again.
    pause
    exit
)

:: Install dependencies quietly
echo 📦 Checking dependencies...
pip install openpyxl --quiet >nul 2>&1

:: Run the calculator
echo.
echo 🚀 Starting PSH Calculator...
echo 🌐 This will open in your web browser
echo.
python psh_calculator_web.py

pause