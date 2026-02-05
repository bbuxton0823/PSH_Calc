# PSH Rent Calculator - User Guide for Low-Tech Users

## 🚀 Getting Started (5 Easy Steps)

### Step 1: Install Python (One-Time Setup)
**Windows:**
1. Go to https://python.org/downloads
2. Download Python (any version 3.6 or higher)
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click "Install Now"

**Mac:**
- Python comes installed, or use: `brew install python3`

**Linux:**
- Ubuntu/Debian: `sudo apt install python3 python3-pip`

### Step 2: Download the Calculator
1. Download all files to a folder (like "Desktop/PSH-Calculator")
2. Keep all files in the same folder

### Step 3: Start the Calculator
**Windows:** Double-click `run_calculator.bat`
**Mac/Linux:** Double-click `run_calculator.sh`
**Any System:** Open terminal and type `python run_calculator.py`

### Step 4: First-Time Setup
1. The app will automatically install needed components
2. Go to "Settings" tab to check FMR rates for your area
3. Update rates if needed, click "Save FMR Rates"

### Step 5: Start Calculating!
1. Go to "Calculator" tab
2. Fill in the form
3. Click "Calculate Rent"
4. Click "Export to Excel" to save results

---

## 📋 How to Use Each Tab

### Tab 1: 📊 Calculator (Main Work Area)

#### Household Information Section
- **Head of Household Name:** Type the person's full name
- **Voucher Bedroom Size:** Choose from dropdown (0-5)
- **Bedrooms in Unit:** Choose actual bedrooms in the apartment

*💡 Tip: The app shows which FMR rate will be used (smaller of voucher size or actual bedrooms)*

#### Financial Information Section  
- **Rent to Owner:** Monthly rent amount landlord charges
- **Utility Allowance:** Monthly utility credit from PHA schedule
- **Total Tenant Payment:** Family's share (minimum $50 for PSH)

*💡 Tip: Calculations update automatically as you type*

#### Family Composition Section
- **Eligible Members:** Count of people with qualifying immigration status
- **Ineligible Members:** Count of people without qualifying status

*💡 Tip: If there are ineligible members, you'll see proration warnings*

#### Results Section
Shows your calculated amounts:
- **HAP to Owner:** What housing authority pays landlord
- **Tenant Rent:** What tenant pays landlord directly  
- **Utility Reimbursement:** What tenant gets for utilities

*💡 Tip: Green numbers = good, Red warnings = need supervisor approval*

#### Action Buttons
- **📊 Calculate Rent:** Final calculation with validation
- **📄 Export to Excel:** Create professional report
- **🗑️ Clear Form:** Start over with blank form

### Tab 2: ⚙️ Settings (FMR Management)

#### Fair Market Rent Rates
- Shows current FMR for each bedroom size
- Edit any rate and click "Save FMR Rates"
- Use "Reset to Defaults" if you make mistakes

#### FMR Management Buttons
- **💾 Save FMR Rates:** Keep your changes
- **🔄 Reset to Defaults:** Go back to original rates
- **📁 Load from Excel:** Import rates from spreadsheet

*💡 Tip: FMR rates should match your local HUD-published rates*

#### Data Management
- **📤 Export Settings:** Save your rates to share with others
- **📥 Import Settings:** Load rates from another computer

### Tab 3: ❓ Help (User Guide)

- Complete instructions for every feature
- Explanations of PSH calculation rules
- Tips for low-tech users
- Troubleshooting common problems

---

## ⚠️ Understanding Warnings & Alerts

### 🔴 Red Warnings (Need Attention)
- **"Gross rent exceeds FMR"** → Supervisor approval required
- **"Please enter Head of Household name"** → Required field missing
- **"Rent to Owner must be greater than $0"** → Invalid amount

### 🟡 Yellow Warnings (Information)
- **"MIXED FAMILY: Prorated assistance"** → Some members ineligible
- **"TTP minimum is $50"** → System will use $50 if you enter less

### 🟢 Green Messages (Good News)
- **"All members eligible"** → No proration needed
- **"Calculations updated automatically"** → Everything working
- **"Calculation completed successfully"** → Ready to export

---

## 📊 Reading Your Excel Report

### Report Sections (Top to Bottom)
1. **Header:** Report title and date
2. **Household Information:** Names, bedroom sizes
3. **Financial Information:** All rent and payment amounts
4. **Family Composition:** Member counts and proration
5. **Calculation Results:** Final amounts (highlighted)

### Color Coding in Excel
- **Green headers:** Main sections
- **Blue headers:** Subsections  
- **Red backgrounds:** Warnings/violations
- **Bold text:** Important results

### What Supervisors Look For
- HAP to Owner amount (in green)
- Any red warnings about FMR violations
- Mixed family proration percentages
- Total tenant payment amounts

---

## 🔧 Troubleshooting Common Problems

### "Module not found" Error
**Problem:** Missing openpyxl package
**Solution:** 
1. Close the app
2. Open terminal/command prompt
3. Type: `pip install openpyxl`
4. Restart the app

### Excel File Won't Open
**Problem:** No spreadsheet program installed
**Solutions:**
- Install Microsoft Excel
- Install LibreOffice (free) from libreoffice.org
- Install Google Sheets and open the file there

### Calculations Look Wrong
**Possible Issues:**
1. Check FMR rates in Settings tab
2. Verify all numbers entered correctly
3. Make sure TTP is at least $50
4. Check if mixed family proration applies

### Can't Save Excel Files
**Problem:** Permission issues
**Solutions:**
- Save to Desktop or Documents folder
- On Windows, run as Administrator
- Check if Excel is already open with the same filename

### App Won't Start
**Problem:** Python not installed or not found
**Solutions:**
- Reinstall Python with "Add to PATH" checked
- Use `python3` instead of `python` on Mac/Linux
- Try running `run_calculator.py` directly

### Settings Won't Save  
**Problem:** File permission issues
**Solutions:**
- Run as administrator on Windows
- Check user folder permissions
- Try exporting/importing settings instead

---

## 💡 Pro Tips for Efficient Use

### Keyboard Shortcuts
- **Tab:** Move to next field
- **Shift+Tab:** Move to previous field  
- **Enter:** Move to next field (in most cases)
- **Ctrl+A:** Select all text in field

### Workflow Tips
1. **Keep FMR rates current** - update monthly when HUD publishes new rates
2. **Use Tab key** - faster than clicking between fields
3. **Save Excel files with good names** - include family name and date
4. **Export settings** - share FMR rates with other staff

### Data Entry Tips
- Enter dollars without commas or $ symbols (app adds formatting)
- Use whole numbers when possible (1500 not 1500.00)
- Required fields show red border when empty
- Hover over fields for helpful hints

### Supervisor Review Process
1. Print or email the Excel report
2. Highlight any red warnings for discussion
3. Have supervisor sign off on over-FMR approvals
4. Keep Excel file for your records

---

## 📞 When to Get Help

### Contact IT Support When:
- App won't install or start
- Python installation problems
- Computer permission issues
- Files won't save to network drives

### Contact Supervisor When:
- Gross rent exceeds FMR
- Unusual mixed family situations  
- TTP calculations seem wrong for specific case
- Policy questions about PSH rules

### Contact Training When:
- Need help with basic PSH calculations
- Questions about HUD rules
- Mixed family policy clarifications
- Voucher sizing questions

---

## ✅ Quality Checklist

### Before Submitting Calculations
- [ ] Head of household name is correct and complete
- [ ] Voucher size matches voucher paperwork
- [ ] Bedroom count matches lease
- [ ] Rent amount matches lease
- [ ] Utility allowance from current PHA schedule
- [ ] TTP calculation verified
- [ ] Mixed family composition is accurate
- [ ] All red warnings addressed
- [ ] Supervisor approval obtained if needed
- [ ] Excel report exported and saved
- [ ] Calculation date is correct

### File Organization Tips
- Create folders by month: "PSH Calculations - January 2024"
- Name files clearly: "Smith_John_PSH_Calc_2024-01-15"
- Keep backup copies of important calculations
- Export settings monthly to backup FMR rates

---

*Remember: This tool makes PSH calculations easier, but you're still the expert! Trust your training and get supervisor help when needed.*