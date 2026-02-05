#!/usr/bin/env python3
"""
Create Distribution Package for PSH Rent Calculator
Creates a ZIP file that can be easily shared with co-workers
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_distribution_zip():
    """Create a distribution ZIP file with all necessary components"""
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create distribution folder name with date
    date_str = datetime.now().strftime("%Y%m%d")
    zip_name = f"PSH_Rent_Calculator_{date_str}.zip"
    zip_path = os.path.join(current_dir, zip_name)
    
    # Files to include in distribution
    files_to_include = [
        'psh_calculator.py',
        'setup.py', 
        'requirements.txt',
        'run_calculator.py',
        'run_calculator.bat',
        'run_calculator.sh',
        'README.md',
        'USER_GUIDE.md',
        'INSTALLATION.md',
        'PSH_Calculator_Install.html'
    ]
    
    # Create the ZIP file
    print(f"Creating distribution package: {zip_name}")
    print("=" * 50)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            file_path = os.path.join(current_dir, file)
            if os.path.exists(file_path):
                zipf.write(file_path, file)
                print(f"✓ Added: {file}")
            else:
                print(f"⚠ Missing: {file}")
    
    # Get file size
    file_size = os.path.getsize(zip_path)
    file_size_mb = file_size / (1024 * 1024)
    
    print("=" * 50)
    print(f"✅ Distribution package created successfully!")
    print(f"📁 File: {zip_name}")
    print(f"📊 Size: {file_size_mb:.1f} MB")
    print(f"📍 Location: {zip_path}")
    print()
    print("📋 HOW TO SHARE:")
    print("1. Email the ZIP file to co-workers")
    print("2. Or copy to shared network drive")
    print("3. Recipients extract and run setup.py")
    print("4. Or share PSH_Calculator_Install.html for instructions")
    print()
    print("📧 Email Instructions for Recipients:")
    print("='Attached is the PSH Rent Calculator - extract all files")
    print("  to a folder and double-click setup.py to install'")
    
    return zip_path

def create_simple_installer():
    """Create a simplified installer script for distribution"""
    
    installer_content = '''@echo off
title PSH Rent Calculator - Quick Install

echo =========================================
echo PSH RENT CALCULATOR - QUICK INSTALL
echo =========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo.
    echo Please install Python 3.6+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python found

echo.
echo Installing PSH Rent Calculator...
python setup.py --quick

if errorlevel 0 (
    echo.
    echo ✅ Installation completed!
    echo.
    echo To start the calculator:
    echo   • Double-click start_calculator.bat
    echo   • Or run: python psh_calculator.py
    echo.
    pause
) else (
    echo.
    echo ❌ Installation failed
    echo Please check the error messages above
    echo.
    pause
)
'''
    
    with open('quick_install.bat', 'w') as f:
        f.write(installer_content)
    
    print("✓ Created quick_install.bat for Windows users")

def main():
    """Main function"""
    print("PSH Rent Calculator - Distribution Creator")
    print("=" * 50)
    print()
    
    # Create distribution package
    zip_path = create_distribution_zip()
    
    # Create quick installer
    create_simple_installer()
    
    print()
    print("🎯 DISTRIBUTION READY!")
    print()
    print("Files created for sharing:")
    print(f"  • {os.path.basename(zip_path)} (main package)")
    print("  • PSH_Calculator_Install.html (web instructions)")
    print("  • quick_install.bat (Windows quick installer)")
    print()
    print("Choose sharing method:")
    print("  📧 Email: Send the ZIP file")
    print("  🌐 Web: Share the HTML file") 
    print("  💾 USB: Copy entire folder")
    print("  🖧 Network: Place on shared drive")

if __name__ == "__main__":
    main()