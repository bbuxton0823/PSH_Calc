@echo off
title PSH Rent Calculator - PDF Edition

cls
echo ╔════════════════════════════════════════╗
echo ║       PSH RENT CALCULATOR - 2026      ║
echo ║         PDF Edition - COMPLETE         ║
echo ║                                        ║
echo ║  📄 Professional PDF Reports           ║
echo ║  📊 Excel Export                       ║
echo ║  🖨️  Print Ready Forms                 ║
echo ║  ⚙️  Admin FMR Controls                ║
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

:: Install dependencies
echo 📦 Installing PDF generation libraries...
pip install reportlab openpyxl --quiet
if errorlevel 1 (
    echo ⚠️  Some dependencies may not have installed properly
    echo The calculator should still work for basic functions
)

:: Run the PDF-enabled calculator
echo.
echo 🚀 Starting PSH Calculator with PDF support...
echo 🌐 This will open in your web browser
echo 📄 Click "Print/Save PDF" to generate professional reports
echo.
python psh_calculator_web_pdf.py

pause