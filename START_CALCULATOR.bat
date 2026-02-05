@echo off
title PSH Rent Calculator - Smart Launcher

cls
echo ╔════════════════════════════════════════╗
echo ║       PSH RENT CALCULATOR - 2026      ║
echo ║           Smart Launcher               ║
echo ╚════════════════════════════════════════╝
echo.

:: Check Python installation
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

echo ✅ Python found
echo.

:: Try to install PDF dependencies
echo 📄 Attempting to install PDF support...
pip install reportlab openpyxl --quiet >nul 2>&1

:: Test if PDF version works
echo 🧪 Testing PDF support...
python -c "from reportlab.lib import colors; print('PDF support available')" >nul 2>&1
if errorlevel 0 (
    echo ✅ PDF support confirmed - starting full version
    echo.
    echo Features available:
    echo   📄 Professional PDF reports
    echo   📊 Excel export
    echo   🖨️  Print functionality
    echo   ⚙️  Admin controls
    echo.
    python psh_calculator_web_pdf.py
) else (
    echo ⚠️  PDF libraries not available - using web version
    echo.
    echo Features available:
    echo   📊 Excel export
    echo   🖨️  Print functionality
    echo   ⚙️  Admin controls
    echo.
    echo Note: You can manually install PDF support later with:
    echo   pip install reportlab
    echo.
    python psh_calculator_web.py
)

if errorlevel 1 (
    echo.
    echo ❌ Calculator failed to start
    echo Please check error messages above
    echo.
    pause
)