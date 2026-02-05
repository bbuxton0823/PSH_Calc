#!/usr/bin/env python3
"""
PSH Rent Calculator - Setup Script
Automatically sets up virtual environment and installs dependencies
"""

import subprocess
import sys
import os
import venv

def create_virtual_environment():
    """Create a virtual environment for the application"""
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    
    if os.path.exists(venv_path):
        print("✓ Virtual environment already exists")
        return venv_path
    
    print("Creating virtual environment...")
    try:
        venv.create(venv_path, with_pip=True)
        print("✓ Virtual environment created successfully")
        return venv_path
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return None

def install_requirements(venv_path):
    """Install required packages in virtual environment"""
    print("Installing required packages...")
    
    # Determine pip executable path
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:  # Unix-like (Mac, Linux)
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        python_path = os.path.join(venv_path, 'bin', 'python')
    
    try:
        # Install openpyxl
        subprocess.check_call([pip_path, 'install', 'openpyxl==3.1.5'])
        print("✓ openpyxl installed successfully")
        
        # Test imports
        subprocess.check_call([python_path, '-c', 'import openpyxl; import tkinter; print("All dependencies working!")'])
        print("✓ All packages verified")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    except FileNotFoundError:
        print("❌ Virtual environment paths not found")
        return False

def create_launcher_scripts(venv_path):
    """Create platform-specific launcher scripts"""
    
    # Python launcher that uses virtual environment
    launcher_content = f'''#!/usr/bin/env python3
"""
PSH Rent Calculator - Virtual Environment Launcher
"""
import os
import sys

# Add virtual environment to path
venv_path = r"{venv_path}"
if os.name == 'nt':
    python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    site_packages = os.path.join(venv_path, 'Lib', 'site-packages')
else:
    python_path = os.path.join(venv_path, 'bin', 'python')
    site_packages = os.path.join(venv_path, 'lib', 'python3.*/site-packages')

# Import and run the calculator
sys.path.insert(0, site_packages)

try:
    from psh_calculator import main
    print("Starting PSH Rent Calculator...")
    main()
except ImportError as e:
    print(f"Error: {{e}}")
    print("Please run setup.py first to install dependencies")
    input("Press Enter to exit...")
except Exception as e:
    print(f"Error starting calculator: {{e}}")
    input("Press Enter to exit...")
'''
    
    # Write launcher script
    with open('start_calculator.py', 'w') as f:
        f.write(launcher_content)
    
    # Create batch file for Windows
    batch_content = f'''@echo off
title PSH Rent Calculator
echo Starting PSH Rent Calculator...
echo.
"{venv_path}\\Scripts\\python.exe" psh_calculator.py
if errorlevel 1 (
    echo.
    echo Error running calculator
    pause
)
'''
    
    with open('start_calculator.bat', 'w') as f:
        f.write(batch_content)
    
    # Create shell script for Mac/Linux  
    shell_content = f'''#!/bin/bash
echo "Starting PSH Rent Calculator..."
echo
"{venv_path}/bin/python" psh_calculator.py
if [ $? -ne 0 ]; then
    echo
    echo "Error running calculator"
    read -p "Press Enter to exit..."
fi
'''
    
    with open('start_calculator.sh', 'w') as f:
        f.write(shell_content)
    
    # Make shell script executable
    try:
        os.chmod('start_calculator.sh', 0o755)
    except:
        pass
    
    print("✓ Launcher scripts created")

def main():
    """Main setup function"""
    print("=" * 60)
    print("PSH RENT CALCULATOR - SETUP")
    print("=" * 60)
    print()
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment
    venv_path = create_virtual_environment()
    if not venv_path:
        print("❌ Setup failed - could not create virtual environment")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements(venv_path):
        print("❌ Setup failed - could not install requirements")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Create launcher scripts
    create_launcher_scripts(venv_path)
    
    print()
    print("=" * 60)
    print("✓ SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("How to start the calculator:")
    print("  Windows: Double-click start_calculator.bat")
    print("  Mac/Linux: Double-click start_calculator.sh")
    print("  Any system: python start_calculator.py")
    print()
    print("Next steps:")
    print("1. Run the calculator")
    print("2. Go to Settings tab to update FMR rates")
    print("3. Start calculating PSH rent assistance!")
    print()
    
    # Ask if user wants to start now
    try:
        response = input("Start the calculator now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("Starting calculator...")
            print()
            
            # Import and run
            if os.name == 'nt':
                python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
            else:
                python_exe = os.path.join(venv_path, 'bin', 'python')
            
            subprocess.call([python_exe, 'psh_calculator.py'])
            
    except KeyboardInterrupt:
        print("\nSetup complete. Exiting...")

if __name__ == "__main__":
    main()