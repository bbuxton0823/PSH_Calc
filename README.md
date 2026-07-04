# PSH Rent Calculator

A simple, secure rent calculation tool for **Permanent Supportive Housing (PSH)** programs. Built for Housing Authority staff who need accurate HUD-compliant rent calculations without complex software installs.

---

## ▶️ [Launch Calculator](https://bbuxton0823.github.io/PSH_Calc/)

**Click the link above to open the calculator in your browser — no download or install needed.**

👉 **https://bbuxton0823.github.io/PSH_Calc/**

---

## Want a Local Copy?

1. Click the green **Code** button above → **Download ZIP**
2. Unzip the folder
3. Double-click **`PSH_Rent_Calculator.html`**
4. It opens in your browser.

> **Note:** the page loads the standard React and Babel libraries from a
> public CDN (cdnjs.cloudflare.com), so an internet connection is needed to
> *open* the calculator. Your case data is never sent anywhere — the network
> is only used to download those code libraries.

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

**Your case data never leaves your computer.**

- All calculations run locally in your browser — no servers, no cloud
- No case data is stored, transmitted, or logged anywhere
- No cookies, no tracking, no analytics
- No login required
- When you close the tab, the data is gone

The entire application is a single HTML file you can inspect yourself. The only network requests it makes are to cdnjs.cloudflare.com to load the standard React and Babel code libraries when the page opens — no tenant or calculation data is ever sent. (This also means the page needs an internet connection to load; it is not suitable for fully air-gapped systems as-is.)

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
| `PSH_Rent_Calculator.html` | **The calculator** — a single self-contained web page; this is all you need |
| `index.html` | GitHub Pages entry point — just redirects to `PSH_Rent_Calculator.html` |
| `psh_rent_calculator.jsx` | React component variant of the same calculator, for embedding in a React app |
| `psh_rent_calculator.py` | Desktop (tkinter) variant of the same calculator — run with `python3 psh_rent_calculator.py` |
| `PSH_Rent_Calculation_Reference.xlsx` | Original Excel worksheet the calculation rules come from (**ground truth**) |
| `test_psh_calc.py` | Test suite — run with `python3 test_psh_calc.py` (no display or extra packages needed) |
| `LICENSE` | MIT License |

**For most users, you only need `PSH_Rent_Calculator.html`.** The other files are source code for developers.

> **Developers:** all three implementations (HTML, JSX, Python) contain the same calculation engine and must stay in agreement. If you change the math in one, change it in all three and run `python3 test_psh_calc.py` — the expected values in that file are derived from the Excel reference worksheet.

---

## Compatibility

Works in any modern browser:

- ✅ Chrome, Edge, Firefox, Safari
- ✅ Windows, Mac, Linux, Chromebook
- ✅ Tablets and phones (responsive layout)
- ⚠ Needs an internet connection to load (React/Babel libraries come from a CDN); case data still never leaves the browser
- ✅ No software installation needed
- ✅ No admin/IT permissions required

---

## Calculation Method

All calculations follow HUD PSH rent determination rules:

- **TTP Minimum:** $50 (per HUD guidelines)
- **Gross Rent:** Contract Rent + Utility Allowance
- **HAP:** Gross Rent − TTP, never below $0 (if TTP is at or above Gross Rent, no assistance is paid and the tenant owes the full rent)
- **HAP to Owner:** The lesser of HAP or Contract Rent
- **Utility Reimbursement:** Utility Allowance − TTP, when positive
- **Mixed Family Proration:** HAP × (Eligible Members ÷ Total Members), rounded to the nearest dollar; Mixed Family Rent is Contract Rent minus the exact prorated HAP, rounded **down** (same as the Excel worksheet)
- **FMR Comparison:** Based on the lesser of voucher bedroom size or actual unit bedrooms
- **Supervisor Approval:** Required whenever Gross Rent exceeds the FMR on file (including when no FMR is configured for that bedroom size)

The calculation engine matches the logic in the reference Excel worksheet (`PSH_Rent_Calculation_Reference.xlsx`) and is verified by `test_psh_calc.py`.

---

## Questions or Issues

Contact **Bycha Buxton** — bbuxton0823@github

---

*Built for Housing Authority staff who just need the math to be right.*
