# 📊 PSH Rent Calculator - Excel Edition

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)](https://github.com/bbuxton0823/psh-rent-calculator-excel)

A professional desktop application for calculating PSH (Permanent Supportive Housing) rent assistance that works entirely with Excel spreadsheets - no internet required!

**🌐 [One-Click Install Page](https://bbuxton0823.github.io/psh-rent-calculator-excel/)**

## 🎯 Perfect for Low-Tech Users

This application is specifically designed for housing authority staff who need a simple, reliable tool for PSH rent calculations without dealing with complex software or internet requirements.

## ✨ Key Features

- **🖥️ Simple Desktop Interface** - Easy-to-use forms with clear labels
- **📊 Excel Integration** - Generates professional Excel reports
- **🔒 Works Offline** - No internet connection required
- **✅ Automatic Validation** - Prevents calculation errors
- **⚠️ Smart Warnings** - Alerts for FMR violations and supervisor approval
- **👥 Mixed Family Support** - Handles prorated assistance calculations
- **💾 Settings Management** - Customizable FMR rates for your area
- **📄 Professional Reports** - Print-ready Excel output

## 🚀 Quick Start

### 1. Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the application
python psh_calculator.py
```

### 2. First Time Setup

1. **Open the Settings tab** to review FMR (Fair Market Rent) rates
2. **Update FMR rates** for your local area if needed
3. **Save the settings** - they'll be remembered for future use

### 3. Basic Usage

1. **📋 Household Tab** - Enter household information
   - Head of Household name
   - Voucher bedroom size
   - Actual bedrooms in unit

2. **💰 Financial Tab** - Enter financial details  
   - Rent to owner
   - Utility allowance
   - Total tenant payment (TTP)

3. **👥 Family Tab** - Enter family composition
   - Number of eligible members
   - Number of ineligible members

4. **Calculate** - Click "Calculate Rent" to see results

5. **Export** - Click "Export to Excel" to save professional report

## 📊 Understanding the Results

### Key Outputs
- **HAP to Owner** - Amount housing authority pays to landlord
- **Tenant Rent** - Amount tenant pays directly to landlord  
- **Utility Reimbursement** - Amount tenant receives for utilities
- **Gross Rent** - Total rent (rent to owner + utility allowance)

### Warnings & Alerts
- **🔴 FMR Violation** - When gross rent exceeds Fair Market Rent
- **🟡 Mixed Family** - When proration applies due to ineligible members
- **🔴 Validation Errors** - Missing or invalid input data

## 👥 Mixed Family Calculations

When some family members don't have eligible immigration status, the application automatically:
- Calculates proration percentage (eligible ÷ total members)
- Reduces HAP proportionally
- Shows both regular and prorated amounts
- Clearly identifies mixed family status

## 🏠 FMR (Fair Market Rent) Management

### Built-in FMR Rates
The application includes default FMR rates that can be customized:
- Studio (0-BR): $2,485
- 1-Bedroom: $2,977
- 2-Bedroom: $3,604
- 3-Bedroom: $4,604
- 4-Bedroom: $4,772
- 5-Bedroom: $5,000

### Updating FMR Rates
1. Go to **Settings tab**
2. Enter new rates in the FMR section
3. Click **Save FMR Rates**
4. Or **Load from Excel** if you have rates in a spreadsheet

## 📄 Excel Reports

### What's Included
- Complete household information
- All financial calculations step-by-step
- Family composition details
- Clear warnings for violations
- Professional formatting for printing
- Date and staff information

### Report Sections
1. **Household Information** - Names, bedroom sizes, dates
2. **Financial Information** - All rent and payment details  
3. **Family Composition** - Member counts and proration
4. **Calculation Results** - Final amounts in bold/color
5. **Warnings** - FMR violations and approval requirements

## 🔧 Settings & Data Management

### Export/Import Settings
- **Export Settings** - Save your FMR rates and preferences
- **Import Settings** - Load rates from another computer
- **Load FMR from Excel** - Import rates from spreadsheet

### File Storage
- Settings automatically saved to user profile
- No data sent to internet or cloud services
- All calculations and data stay on your computer

## 💡 Tips for Low-Tech Users

### Getting Started
- **Use Tab key** to move between fields quickly
- **All fields show hints** when you hover over them
- **Red text means** something needs attention
- **Green text means** calculations are good

### Common Workflows
1. **Standard Family** - Just fill in the basic info and calculate
2. **Mixed Family** - Enter ineligible members, watch for proration warnings
3. **Over FMR** - Look for supervisor approval warnings in red

### Troubleshooting
- **Can't type in field** - Make sure it's not a dropdown (use arrow keys)
- **Wrong calculations** - Check all numbers are entered correctly
- **Excel won't open** - Make sure you have Excel or LibreOffice installed
- **Settings won't save** - Run as administrator on Windows

## ⚠️ Important Notes

### HUD Compliance
- Follows standard PSH calculation guidelines
- $50 minimum TTP automatically enforced  
- FMR comparison with supervisor approval warnings
- Mixed family proration per HUD requirements

### System Requirements
- Python 3.6 or higher
- Excel, LibreOffice, or compatible spreadsheet program
- Windows, Mac, or Linux operating system
- No internet connection required

### Data Privacy
- All data stays on your local computer
- No cloud storage or internet transmission
- Excel files saved to locations you choose
- Settings stored in user profile only

## 📞 Support

### Common Issues
1. **"Module not found" error** - Run `pip install openpyxl`
2. **Excel file won't open** - Make sure Excel/LibreOffice is installed
3. **Calculations seem wrong** - Verify FMR rates in Settings tab
4. **Can't save files** - Check folder permissions

### Getting Help
- All calculations follow HUD guidelines
- Results match standard PSH worksheets
- Professional Excel output for supervisor review
- Built-in help tab with detailed explanations

---

## 🏗️ For Developers

### Architecture
- **Frontend**: tkinter (comes with Python)
- **Excel**: openpyxl library
- **Storage**: JSON files in user profile
- **Design**: Low-tech friendly with clear visual hierarchy

### Customization
- FMR rates easily configurable
- Color scheme defined in `colors` dictionary
- Calculation logic in separate methods
- Export formatting in `export_to_excel()` method

### Testing
```bash
# Run the application in test mode
python psh_calculator.py

# Test different scenarios:
# 1. Standard family (eligible only)
# 2. Mixed family (eligible + ineligible) 
# 3. Over FMR (gross rent > fair market rent)
# 4. Edge cases (zero values, maximum values)
```

---

*Built with ❤️ for Housing Authority staff who make a difference every day*