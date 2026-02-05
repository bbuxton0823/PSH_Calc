@echo off
title PSH Rent Calculator - Excel Edition

echo ================================================
echo PSH RENT CALCULATOR - EXCEL EDITION
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.6 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python is installed. Starting calculator...
echo.

REM Run the launcher
python run_calculator.py

if errorlevel 1 (
    echo.
    echo Error occurred while running the calculator
    pause
)