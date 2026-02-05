# 📊 PSH Rent Calculator - Complete Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)](https://github.com/bbuxton0823/PSH_Calc)

Professional tools for calculating PSH (Permanent Supportive Housing) rent assistance - now with **two complete applications** to meet different workflow needs!

**🌐 [One-Click Install Page](https://bbuxton0823.github.io/PSH_Calc/)**

---

## 🎯 Choose Your Version

### 📱 **Web Calculator** (NEW!) - Modern & Mobile-Friendly
Perfect for **quick calculations** and **professional PDF reports**

**✨ Key Features:**
- **Beautiful web interface** - Works on desktop, tablet, and mobile
- **Professional PDF reports** - Generate official-looking documents
- **Admin panel** - Update FMR rates annually with built-in controls  
- **Real-time updates** - FMR amounts update instantly as you select bedroom count
- **No installation** - Just double-click and run in your browser

**🚀 Quick Start:** 
1. Download `PSH_Calculator_COMPLETE.zip`
2. Extract and double-click `START_CALCULATOR.bat`
3. Calculator opens in your browser - start calculating!

### 🖥️ **Desktop Calculator** - Traditional & Excel-Focused  
Perfect for **detailed workflows** and **Excel integration**

**✨ Key Features:**
- **Desktop interface** - Familiar Windows-style forms
- **Excel integration** - Generates professional Excel reports
- **Works offline** - No internet connection required
- **Mixed family support** - Handles prorated assistance calculations
- **Smart validation** - Prevents calculation errors with warnings

**🚀 Quick Start:**
```bash
pip install -r requirements.txt
python psh_calculator.py
```

---

## 📱 Web Calculator Features

### 🎨 **Modern Interface**
- Responsive gradient design that works on any device
- Clear FMR year display (currently 2026)
- Real-time FMR updates as you select bedroom count
- Professional results formatting

### 📄 **Professional Reports** 
- **PDF Reports** - Official-looking documents for filing
- **Excel Export** - Formatted spreadsheets
- **Quick Print** - Direct browser printing

### ⚙️ **Admin Controls**
Click the **⚙️ Admin** button to:
- Update FMR rates for all bedroom counts (Studio through 4+)
- Change the FMR year
- Save changes instantly - no file editing required

### 🚀 **Web Calculator Quick Start**

1. **Enter Property Details:**
   - Property address
   - Number of bedrooms (Studio to 4+)
   - Tenant rent payment

2. **Calculate PSH:**
   - Click "Calculate Project-Based Subsidy"  
   - See instant results with breakdown

3. **Generate Reports:**
   - **PDF Report** (recommended) - Professional documents
   - **Excel Export** - Formatted spreadsheets
   - **Quick Print** - Browser printing

### 🔧 **Web Files Structure**
```
Web Calculator/
├── START_CALCULATOR.bat          # Smart launcher (tries PDF first)
├── psh_calculator_web_pdf.py     # Full version with PDF support
├── psh_calculator_web.py         # Web-only backup version
├── PSH_Calculator_COMPLETE.zip   # Ready-to-distribute package
└── README.txt                    # User instructions
```

---

## 🖥️ Desktop Calculator Features  

### 🎯 **Perfect for Detailed Workflows**
- **Household Tab** - Complete household information entry
- **Financial Tab** - Detailed rent and utility calculations  
- **Family Tab** - Mixed family composition handling
- **Settings Tab** - Customizable FMR rates for your area

### 📊 **Excel Integration**
- Professional Excel reports with formatting
- Print-ready output for official documentation
- Automatic calculation validation
- Smart warnings for FMR violations

### 💰 **Advanced Calculations**
- **HAP to Owner** calculations
- **Mixed family** prorated assistance  
- **Utility allowance** integration
- **Total Tenant Payment (TTP)** handling

### 🚀 **Desktop Calculator Usage**

1. **Installation:**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Run application
   python psh_calculator.py
   ```

2. **First Time Setup:**
   - Open Settings tab to review FMR rates
   - Update FMR rates for your local area
   - Save settings for future use

3. **Basic Workflow:**
   - **Household Tab** - Enter household info
   - **Financial Tab** - Enter rent/utility details
   - **Family Tab** - Enter family composition
   - **Calculate** - Generate results
   - **Export** - Save Excel report

### 🔧 **Desktop Files Structure**
```
Desktop Calculator/
├── psh_calculator.py             # Main desktop application
├── requirements.txt              # Python dependencies  
├── setup.py                      # Installation helper
├── run_calculator.py/.bat/.sh    # Platform launchers
├── USER_GUIDE.md                 # Detailed user manual
└── index.html                    # Web installer page
```

---

## 📋 System Requirements

### Web Calculator
- **Python 3.6+** (auto-prompted if missing)
- **Web Browser** (any modern browser)
- **Optional**: `reportlab`, `openpyxl` (auto-installed)

### Desktop Calculator  
- **Python 3.6+**
- **tkinter** (usually included with Python)
- **openpyxl** (for Excel export)

---

## 🎯 Which Version Should I Use?

### Choose **Web Calculator** if you want:
✅ **Quick calculations** with beautiful interface  
✅ **Professional PDF reports** for filing  
✅ **Mobile/tablet compatibility**  
✅ **No installation hassles** - just download and run  
✅ **Modern, responsive design**

### Choose **Desktop Calculator** if you want:
✅ **Detailed workflow management**  
✅ **Excel-native reports** and integration  
✅ **Mixed family** prorated calculations  
✅ **Traditional desktop interface**  
✅ **Offline operation** (no internet required)

### Or Use Both!
Many organizations find value in both:
- **Web version** for quick calculations and client meetings
- **Desktop version** for detailed case management and record-keeping

---

## 📞 Support

For questions, issues, or customizations:
- **Email**: monday@aimagery.com
- **Issues**: [GitHub Issues](https://github.com/bbuxton0823/PSH_Calc/issues)

---

## 📝 License

Created for housing assistance professionals. Free to use and modify.

## 🚀 Contributing

Pull requests welcome! These tools are designed to help housing assistance programs streamline their PSH calculations.

---

**Made with ❤️ for housing assistance professionals**

*Supporting both quick calculations and detailed case management workflows*