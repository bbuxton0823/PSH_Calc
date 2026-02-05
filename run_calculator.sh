#!/bin/bash

echo "================================================"
echo "PSH RENT CALCULATOR - EXCEL EDITION"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo
        echo "Please install Python 3.6 or higher:"
        echo "  macOS: brew install python3"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
        echo
        read -p "Press Enter to exit..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python is installed. Starting calculator..."
echo

# Make the script executable
chmod +x run_calculator.py

# Run the launcher
$PYTHON_CMD run_calculator.py

if [ $? -ne 0 ]; then
    echo
    echo "Error occurred while running the calculator"
    read -p "Press Enter to exit..."
fi