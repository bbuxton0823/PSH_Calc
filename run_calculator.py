#!/usr/bin/env python3
"""
PSH Rent Calculator - Simple Launcher
Double-click this file to start the calculator!
"""

import sys
import subprocess
import os

def check_and_install_requirements():
    """Check if required packages are installed, install if missing"""
    try:
        import openpyxl
        print("✓ All required packages are installed")
        return True
    except ImportError:
        print("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
            print("✓ Packages installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages")
            print("Please run: pip install openpyxl")
            input("Press Enter to continue anyway...")
            return False

def main():
    """Main launcher function"""
    print("=" * 50)
    print("PSH RENT CALCULATOR - EXCEL EDITION")  
    print("=" * 50)
    print()
    
    # Check requirements
    if check_and_install_requirements():
        print("Starting PSH Rent Calculator...")
        print()
        
        # Import and run the main application
        try:
            from psh_calculator import main as run_calculator
            run_calculator()
        except ImportError as e:
            print(f"❌ Error importing calculator: {e}")
            print("Make sure psh_calculator.py is in the same folder")
            input("Press Enter to exit...")
        except Exception as e:
            print(f"❌ Error starting calculator: {e}")
            input("Press Enter to exit...")
    else:
        print("❌ Could not start calculator due to missing requirements")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()