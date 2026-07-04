"""
Tests for the PSH rent calculation engine (psh_rent_calculator.py).

Run with:  python3 test_psh_calc.py

No dependencies beyond the standard library; tkinter is stubbed out so the
tests run headless (e.g. in CI or on servers without a display).

Expected values are derived from the reference worksheet
PSH_Rent_Calculation_Reference.xlsx (sheet "PSH", FMR table in hidden sheet
"VPS") plus HUD rules:

  GROSS RENT            = rent_to_owner + utility_allowance
  FMR                   = FMR table lookup on MIN(voucher_size, br_leased)
  LOWER OF FMR OR GR    = MIN(fmr, gross_rent)
  AMOUNT ABOVE FMR      = MAX(0, gross_rent - fmr)
  TTP                   = MAX(input, 50)                  ($50 PSH minimum)
  TOTAL HAP             = MAX(0, gross_rent - ttp)        (*)
  HAP TO OWNER          = MIN(rent_to_owner, total_hap)
  TENANT RENT           = MAX(0, rent_to_owner - total_hap)
  UTILITY REIMBURSEMENT = MAX(0, utility_allowance - ttp)
  PRORATE %             = num_eligible / total_members
  PRORATED HAP          = prorate_pct * hap_to_owner, ROUND_HALF_UP to $1
                          (the worksheet keeps the exact value and displays
                          it with a whole-dollar cell format)
  MIXED FAMILY RENT     = ROUNDDOWN(rent_to_owner - exact prorated HAP, 0)

(*) Intentional deviation from the raw worksheet formula (C13 = C8 - C12),
which can go negative when TTP exceeds gross rent. Per HUD rules a Housing
Assistance Payment can never be negative: if TTP >= gross rent, no
assistance is paid and the tenant owes the full rent to owner.

The same test cases are mirrored by the JavaScript calculate() functions in
PSH_Rent_Calculator.html and psh_rent_calculator.jsx, which must produce the
same whole-dollar results. If you change the calculation in any one of the
three implementations, change all three and re-run this file.
"""

import sys
import types
import unittest
from decimal import Decimal

# Stub tkinter so importing the app module never needs a display.
for _mod in ("tkinter", "tkinter.messagebox", "tkinter.filedialog"):
    if _mod not in sys.modules:
        sys.modules[_mod] = types.ModuleType(_mod)
sys.modules["tkinter"].messagebox = sys.modules["tkinter.messagebox"]
sys.modules["tkinter"].filedialog = sys.modules["tkinter.filedialog"]

import psh_rent_calculator as psh  # noqa: E402


# (name, inputs{rent, ua, ttp, voucher, leased, elig, inelig}, expected)
# Expected values are whole dollars as shown on the calculation sheet.
CASES = [
    # The worked example saved in PSH_Rent_Calculation_Reference.xlsx
    ("xlsx_sample", dict(rent=4700, ua=469, ttp=50, voucher=3, leased=4, elig=4, inelig=0),
     dict(gross_rent=5169, fmr=4604, lower_fmr_or_gr=4604, amount_above_fmr=565,
          ttp=50, total_hap=5119, hap_to_owner=4700, tenant_rent=0,
          utility_reimbursement=419, prorated_hap=4700, mixed_family_rent=0)),

    ("typical_within_fmr", dict(rent=2000, ua=100, ttp=400, voucher=1, leased=1, elig=1, inelig=0),
     dict(gross_rent=2100, fmr=2977, lower_fmr_or_gr=2100, amount_above_fmr=0,
          ttp=400, total_hap=1700, hap_to_owner=1700, tenant_rent=300,
          utility_reimbursement=0, prorated_hap=1700, mixed_family_rent=300)),

    # Zero income: TTP raised to the $50 PSH minimum
    ("zero_income_min_ttp", dict(rent=1500, ua=0, ttp=0, voucher=0, leased=0, elig=1, inelig=0),
     dict(gross_rent=1500, fmr=2485, lower_fmr_or_gr=1500, amount_above_fmr=0,
          ttp=50, total_hap=1450, hap_to_owner=1450, tenant_rent=50,
          utility_reimbursement=0, prorated_hap=1450, mixed_family_rent=50)),

    # TTP entered below the minimum is raised to $50
    ("ttp_below_min_raised", dict(rent=1200, ua=50, ttp=30, voucher=0, leased=1, elig=2, inelig=0),
     dict(gross_rent=1250, fmr=2485, lower_fmr_or_gr=1250, amount_above_fmr=0,
          ttp=50, total_hap=1200, hap_to_owner=1200, tenant_rent=0,
          utility_reimbursement=0, prorated_hap=1200, mixed_family_rent=0)),

    # Utility allowance exceeds TTP -> utility reimbursement to the tenant
    ("utility_reimbursement", dict(rent=800, ua=300, ttp=50, voucher=1, leased=1, elig=1, inelig=0),
     dict(gross_rent=1100, fmr=2977, lower_fmr_or_gr=1100, amount_above_fmr=0,
          ttp=50, total_hap=1050, hap_to_owner=800, tenant_rent=0,
          utility_reimbursement=250, prorated_hap=800, mixed_family_rent=0)),

    # Mixed family, 2/3 proration: exact prorated HAP = 1266.66...
    # Sheet shows 1267 (rounded) and mixed rent ROUNDDOWN(2000 - 1266.67) = 733
    ("mixed_two_thirds", dict(rent=2000, ua=200, ttp=300, voucher=2, leased=2, elig=2, inelig=1),
     dict(gross_rent=2200, fmr=3604, lower_fmr_or_gr=2200, amount_above_fmr=0,
          ttp=300, total_hap=1900, hap_to_owner=1900, tenant_rent=100,
          utility_reimbursement=0, prorated_hap=1267, mixed_family_rent=733)),

    ("mixed_half", dict(rent=1000, ua=0, ttp=200, voucher=1, leased=1, elig=1, inelig=1),
     dict(gross_rent=1000, fmr=2977, lower_fmr_or_gr=1000, amount_above_fmr=0,
          ttp=200, total_hap=800, hap_to_owner=800, tenant_rent=200,
          utility_reimbursement=0, prorated_hap=400, mixed_family_rent=600)),

    # Mixed family, 5/6 proration: exact prorated HAP = 833.33...
    # Sheet shows 833 and mixed rent ROUNDDOWN(1200 - 833.33) = 366
    ("mixed_five_sixths", dict(rent=1200, ua=0, ttp=200, voucher=2, leased=2, elig=5, inelig=1),
     dict(gross_rent=1200, fmr=3604, lower_fmr_or_gr=1200, amount_above_fmr=0,
          ttp=200, total_hap=1000, hap_to_owner=1000, tenant_rent=200,
          utility_reimbursement=0, prorated_hap=833, mixed_family_rent=366)),

    # TTP exceeds gross rent: HAP floors at $0, tenant owes the full rent.
    # (See note (*) at the top of this file.)
    ("ttp_exceeds_gross_rent", dict(rent=500, ua=100, ttp=800, voucher=1, leased=1, elig=1, inelig=0),
     dict(gross_rent=600, fmr=2977, lower_fmr_or_gr=600, amount_above_fmr=0,
          ttp=800, total_hap=0, hap_to_owner=0, tenant_rent=500,
          utility_reimbursement=0, prorated_hap=0, mixed_family_rent=500)),

    # FMR uses the SMALLER of voucher size and bedrooms leased
    ("voucher_caps_fmr", dict(rent=3000, ua=77, ttp=500, voucher=1, leased=3, elig=2, inelig=0),
     dict(gross_rent=3077, fmr=2977, lower_fmr_or_gr=2977, amount_above_fmr=100,
          ttp=500, total_hap=2577, hap_to_owner=2577, tenant_rent=423,
          utility_reimbursement=0, prorated_hap=2577, mixed_family_rent=423)),

    # 5-BR has no FMR on file (0): whole gross rent is "above FMR",
    # matching the worksheet, so supervisor review is flagged.
    ("no_fmr_on_file_5br", dict(rent=4000, ua=0, ttp=600, voucher=5, leased=5, elig=1, inelig=0),
     dict(gross_rent=4000, fmr=0, lower_fmr_or_gr=0, amount_above_fmr=4000,
          ttp=600, total_hap=3400, hap_to_owner=3400, tenant_rent=600,
          utility_reimbursement=0, prorated_hap=3400, mixed_family_rent=600)),

    # TTP high but still below gross rent; UA smaller than TTP -> no reimbursement
    ("high_ttp_below_gross", dict(rent=1000, ua=500, ttp=1200, voucher=2, leased=2, elig=1, inelig=0),
     dict(gross_rent=1500, fmr=3604, lower_fmr_or_gr=1500, amount_above_fmr=0,
          ttp=1200, total_hap=300, hap_to_owner=300, tenant_rent=700,
          utility_reimbursement=0, prorated_hap=300, mixed_family_rent=700)),
]


def make_engine():
    db = psh.FMRDatabase()
    # Force built-in 2025 defaults so a user's ~/.psh_fmr_data.json
    # cannot change test results.
    db.fmr_data = psh.FMRDatabase.DEFAULT_FMR.copy()
    return psh.RentCalculationEngine(db)


class TestRentCalculationEngine(unittest.TestCase):
    def test_cases(self):
        engine = make_engine()
        for name, inp, expected in CASES:
            with self.subTest(case=name):
                ok, result = engine.calculate({
                    "rent_to_owner": inp["rent"],
                    "utility_allowance": inp["ua"],
                    "ttp": inp["ttp"],
                    "voucher_size": inp["voucher"],
                    "br_leased": inp["leased"],
                    "num_eligible": inp["elig"],
                    "num_ineligible": inp["inelig"],
                })
                self.assertTrue(ok, f"{name}: engine error: {result}")
                for key, want in expected.items():
                    got = result[key]
                    # Compare as whole dollars (what the sheet displays)
                    got_int = int(Decimal(str(got)).quantize(Decimal("1")))
                    self.assertEqual(
                        got_int, want,
                        f"{name}: {key} = {got_int}, expected {want}",
                    )

    def test_validation_errors(self):
        engine = make_engine()
        ok, msg = engine.calculate({"rent_to_owner": -1, "num_eligible": 1})
        self.assertFalse(ok)
        ok, msg = engine.calculate({"rent_to_owner": 100, "utility_allowance": -5, "num_eligible": 1})
        self.assertFalse(ok)
        ok, msg = engine.calculate({"rent_to_owner": 100, "num_eligible": 0})
        self.assertFalse(ok)

    def test_hap_never_negative(self):
        engine = make_engine()
        ok, r = engine.calculate({
            "rent_to_owner": 300, "utility_allowance": 0, "ttp": 5000,
            "voucher_size": 1, "br_leased": 1,
            "num_eligible": 1, "num_ineligible": 1,
        })
        self.assertTrue(ok)
        self.assertGreaterEqual(r["total_hap"], 0)
        self.assertGreaterEqual(r["hap_to_owner"], 0)
        self.assertGreaterEqual(r["prorated_hap"], 0)
        self.assertLessEqual(r["tenant_rent"], r["rent_to_owner"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
