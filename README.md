# PSH Rent Calculator

A professional web-based calculator for Project-Based Housing Subsidy (PSH) calculations with beautiful interface and PDF report generation.

![PSH Calculator](https://img.shields.io/badge/Version-2026-blue)
![Python](https://img.shields.io/badge/Python-3.6+-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)

## ✨ Features

- **Beautiful Web Interface** - Responsive design that works on desktop, tablet, and mobile
- **Professional PDF Reports** - Generate official-looking documents for filing and documentation
- **Excel Export** - Formatted spreadsheet output with calculations
- **Admin Panel** - Update Fair Market Rent (FMR) rates annually with built-in controls
- **Print Ready** - Multiple printing options for different needs
- **Current Year Display** - Prominently shows FMR year (currently 2026)
- **Real-time Updates** - FMR amounts update instantly as you select bedroom count

## 🚀 Quick Start

### Option 1: Download Ready-to-Use Package
1. Download `PSH_Calculator_COMPLETE.zip`
2. Extract anywhere on your computer
3. Double-click `START_CALCULATOR.bat`
4. Calculator opens in your web browser
5. Start calculating!

### Option 2: Run from Source
```bash
git clone https://github.com/bbuxton0823/psh-calculator.git
cd psh-calculator
python psh_calculator_web.py
```

## 📋 Requirements

- **Python 3.6+** (automatically prompted for installation if missing)
- **Web Browser** (Chrome, Firefox, Safari, Edge - any modern browser)
- **Optional**: `reportlab` and `openpyxl` for PDF/Excel features (auto-installed)

## 🎯 How to Use

1. **Enter Property Address** - Full address of the property
2. **Select Bedrooms** - Choose from Studio (0) to 4+ bedrooms
3. **Enter Tenant Rent** - Monthly rent payment from tenant
4. **Click Calculate** - Instantly see PSH calculation results
5. **Generate Reports** - Choose PDF, Excel, or print options

## 📄 Report Options

- **📄 Print/Save PDF** - Professional formatted reports (RECOMMENDED)
- **📊 Export Excel** - Formatted spreadsheet with calculations  
- **🖨️ Quick Print** - Direct browser printing

## ⚙️ Admin Features

Click the **⚙️ Admin** button to:
- Update FMR rates for all bedroom counts (Studio through 4+)
- Change the FMR year 
- Save changes instantly - no file editing required
- All changes take effect immediately

## 📁 File Structure

```
psh-calculator/
├── START_CALCULATOR.bat          # Main launcher (tries PDF first)
├── psh_calculator_web_pdf.py     # Full version with PDF support
├── psh_calculator_web.py         # Backup web-only version
├── start_pdf.bat                 # PDF version launcher
├── start_web.bat                 # Web-only launcher
├── README.txt                    # User instructions
└── PSH_Calculator_COMPLETE.zip   # Ready-to-distribute package
```

## 💡 Smart Launcher System

The `START_CALCULATOR.bat` file automatically:
1. **Checks for Python** - Opens download page if needed
2. **Attempts PDF support** - Installs required libraries
3. **Falls back gracefully** - Uses web version if PDF libraries fail
4. **Always works** - No installation failures

## 🎨 Interface Preview

- **Modern gradient design** with professional styling
- **Clear FMR year badge** prominently displayed
- **Real-time FMR display** updates as you select options
- **Professional results formatting** with clean typography
- **Mobile responsive** - works great on phones and tablets

## 🔧 Customization

All FMR rates and settings can be updated through the web interface:
- No code editing required
- Changes save automatically to `fmr_config.json`
- Interface updates immediately

## 📞 Support

For questions, issues, or customizations:
- **Email**: monday@aimagery.com
- **Issues**: [GitHub Issues](https://github.com/bbuxton0823/psh-calculator/issues)

## 📝 License

Created for housing assistance professionals. Free to use and modify.

## 🚀 Contributing

Pull requests welcome! This tool is designed to help housing assistance programs streamline their PSH calculations.

---

**Made with ❤️ for housing assistance professionals**