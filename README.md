# PSH Rent Calculator

A simple, secure rent calculation tool for **Permanent Supportive Housing (PSH)** programs. Built for Housing Authority staff who need accurate HUD-compliant rent calculations without complex software installs.

---

## ▶️ [Launch Calculator](https://bbuxton0823.github.io/PSH_Calc/)

**Click the link above to open the calculator in your browser — no download or install needed.**

👉 **https://bbuxton0823.github.io/PSH_Calc/**

---

## Want an Offline Copy?

1. Click the green **Code** button above → **Download ZIP**
2. Unzip the folder
3. Double-click **`PSH_Rent_Calculator.html`**
4. It opens in your browser. Works without internet.

> **Already downloaded?** Just double-click the `.html` file anytime. It works offline.

---

## What It Does

Calculates PSH rent assistance following HUD guidelines:

- **Gross Rent** (contract rent + utility allowance)
- **HAP to Owner** (Housing Assistance Payment)
- **Tenant Rent** (what the household pays)
- **Utility Reimbursement** (when UA exceeds TTP)
- **Mixed Family Proration** (automatic for households with ineligible members)
- **FMR Compliance Check** (flags when gross rent exceeds Fair Market Rent)

The calculator walks you through 4 simple steps:

| Step | What You Enter |
|------|---------------|
| 1. Household | Head of household name, voucher size, unit bedrooms |
| 2. Finances | Rent to owner, utility allowance, TTP |
| 3. Family | Eligible and ineligible member counts |
| 4. Staff | Your name, date, supervisor (if needed) |

Results display instantly with a printable summary.

---

## Security & Privacy

**Your data never leaves your computer.**

- Runs 100% locally in your browser — no servers, no cloud, no internet connection needed
- No data is stored, transmitted, or logged anywhere
- No cookies, no tracking, no analytics
- No login required
- When you close the tab, the data is gone
- Safe to use on government networks and air-gapped systems

The entire application is a single HTML file you can inspect yourself. There is no hidden code, no external data calls, and no background processes.

---

## Printing & Filing

Click **Print** on the results page to generate a clean, printable calculation sheet.

- Headers, navigation, and buttons are automatically hidden in print
- Formatted for standard 8.5" x 11" paper
- Suitable for filing in tenant records
- **Copy to Clipboard** button also available for pasting into emails or case notes

---

## Admin: Updating FMR Rates

When HUD publishes new Fair Market Rent rates each year:

1. Click **FMR Settings** (top-right corner of the calculator)
2. Click **Edit** on any bedroom row
3. Update the **Payment Standard** and **FMR** values
4. Click **Save**
5. Changes take effect immediately for all calculations

To reset to the built-in 2025 defaults, click **Reset to 2025 Defaults**.

> **Note:** FMR changes are session-only. To make permanent updates, edit the `DEFAULT_FMR` array at the top of the HTML file (any text editor works — the values are clearly labeled).

---

## Files in This Repo

| File | Purpose |
|------|---------|
| `PSH_Rent_Calculator.html` | **The calculator** — this is all you need |
| `psh_rent_calculator.py` | Python source (reference implementation) |
| `psh_rent_calculator.jsx` | React component source code |
| `PSH_Rent_Calculation_Reference.xlsx` | Original Excel calculation worksheet |
| `LICENSE` | MIT License |

**For most users, you only need `PSH_Rent_Calculator.html`.** The other files are source code for developers.

---

## Compatibility

Works in any modern browser:

- ✅ Chrome, Edge, Firefox, Safari
- ✅ Windows, Mac, Linux, Chromebook
- ✅ Tablets and phones (responsive layout)
- ✅ Works offline — no internet required
- ✅ No software installation needed
- ✅ No admin/IT permissions required

---

## Calculation Method

All calculations follow HUD PSH rent determination rules:

- **TTP Minimum:** $50 (per HUD guidelines)
- **Gross Rent:** Contract Rent + Utility Allowance
- **HAP:** Gross Rent − TTP
- **Mixed Family Proration:** HAP × (Eligible Members ÷ Total Members)
- **FMR Comparison:** Based on the lesser of voucher bedroom size or actual unit bedrooms
- **Supervisor Approval:** Required when Gross Rent exceeds FMR

The calculation engine matches the logic in the reference Excel worksheet (`PSH_Rent_Calculation_Reference.xlsx`).

---

## Questions or Issues

Contact **Bycha Buxton** — bbuxton0823@github

---

*Built for Housing Authority staff who just need the math to be right.*
