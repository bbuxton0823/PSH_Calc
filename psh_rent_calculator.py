"""
PSH (Permanent Supportive Housing) Rent Calculation Application
A professional desktop application for calculating rent assistance for PSH programs.
Built with Python 3 and tkinter for cross-platform compatibility.

Features:
- Locked wizard with linear flow (cannot skip ahead)
- Progress indicator showing current and completed steps
- Live financial calculations with FMR comparison
- Dashboard-style results display
- Mixed family prorated assistance calculations
- FMR management interface
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
import json
import os


# Color palette
COLOR_PRIMARY_BLUE = "#1a73e8"
COLOR_SUCCESS_GREEN = "#0d7a3f"
COLOR_WARNING_RED = "#d32f2f"
COLOR_WARNING_YELLOW = "#f9a825"
COLOR_LIGHT_GRAY = "#f5f5f5"
COLOR_WHITE = "#ffffff"
COLOR_DARK_TEXT = "#212121"
COLOR_SECONDARY_GRAY = "#757575"


class FMRDatabase:
    """Manages Fair Market Rent (FMR) data and Payment Standards."""

    DEFAULT_FMR = {
        0: {"payment_standard": 2734, "fmr": 2485},
        1: {"payment_standard": 3275, "fmr": 2977},
        2: {"payment_standard": 3964, "fmr": 3604},
        3: {"payment_standard": 5064, "fmr": 4604},
        4: {"payment_standard": 5249, "fmr": 4772},
        5: {"payment_standard": 0, "fmr": 0},
    }

    def __init__(self):
        self.fmr_data = self.DEFAULT_FMR.copy()
        self.effective_date = "2025-01-01"
        self.load_from_file()

    def load_from_file(self):
        """Load FMR data from saved JSON file if it exists."""
        config_file = os.path.expanduser("~/.psh_fmr_data.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    self.fmr_data = {int(k): v for k, v in data.get("fmr_data", {}).items()}
                    self.effective_date = data.get("effective_date", "2025-01-01")
            except Exception as e:
                print(f"Error loading FMR data: {e}")

    def save_to_file(self):
        """Save FMR data to JSON file."""
        config_file = os.path.expanduser("~/.psh_fmr_data.json")
        try:
            with open(config_file, 'w') as f:
                json.dump({
                    "fmr_data": self.fmr_data,
                    "effective_date": self.effective_date
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving FMR data: {e}")

    def get_fmr(self, bedrooms):
        """Get FMR for given bedroom count."""
        if bedrooms in self.fmr_data:
            return self.fmr_data[bedrooms]["fmr"]
        return 0

    def load_from_csv(self, filepath):
        """Load FMR data from CSV file."""
        try:
            fmr_data = {}
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    bedrooms = int(row.get("bedrooms", 0))
                    fmr_data[bedrooms] = {
                        "payment_standard": int(float(row.get("payment_standard", 0))),
                        "fmr": int(float(row.get("fmr", 0)))
                    }
            self.fmr_data = fmr_data
            self.effective_date = datetime.now().strftime("%Y-%m-%d")
            self.save_to_file()
            return True
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {e}")


class RentCalculationEngine:
    """Core calculation engine for PSH rent calculations."""

    MIN_TTP = 50  # Minimum Total Tenant Payment

    def __init__(self, fmr_db):
        self.fmr_db = fmr_db
        self.results = {}

    def calculate(self, inputs):
        """
        Perform all rent calculations based on inputs.
        Returns tuple of (success, result_dict or error_string).
        """
        try:
            # Extract and validate inputs
            rent_to_owner = Decimal(str(inputs.get("rent_to_owner", 0)))
            utility_allowance = Decimal(str(inputs.get("utility_allowance", 0)))
            ttp = Decimal(str(inputs.get("ttp", 0)))
            voucher_size = int(inputs.get("voucher_size", 0))
            br_leased = int(inputs.get("br_leased", 0))
            num_eligible = int(inputs.get("num_eligible", 1))
            num_ineligible = int(inputs.get("num_ineligible", 0))

            # Enforce minimum TTP
            ttp = max(ttp, Decimal(self.MIN_TTP))

            # Validation
            if rent_to_owner < 0:
                raise ValueError("Rent to Owner cannot be negative")
            if utility_allowance < 0:
                raise ValueError("Utility Allowance cannot be negative")
            if num_eligible < 1:
                raise ValueError("Number Eligible must be at least 1")

            # Step 1: GROSS RENT
            gross_rent = rent_to_owner + utility_allowance

            # Step 2: FMR Lookup
            bedroom_for_fmr = min(voucher_size, br_leased)
            fmr = Decimal(str(self.fmr_db.get_fmr(bedroom_for_fmr)))

            # Step 4: AMOUNT ABOVE FMR
            amount_above_fmr = max(Decimal(0), gross_rent - fmr)

            # Step 5-8: Basic HAP calculations
            total_hap = gross_rent - ttp
            total_family_share = ttp
            hap_to_owner = min(rent_to_owner, total_hap)
            tenant_rent = max(Decimal(0), rent_to_owner - total_hap)

            # Step 10: UTILITY REIMBURSEMENT
            utility_reimbursement = max(Decimal(0), utility_allowance - ttp)

            # Prorated assistance for mixed families
            total_family_members = num_eligible + num_ineligible
            is_mixed_family = num_ineligible > 0

            if is_mixed_family:
                prorate_pct = Decimal(num_eligible) / Decimal(total_family_members)
                prorated_hap = (prorate_pct * hap_to_owner).quantize(Decimal('1'), rounding=ROUND_DOWN)
                mixed_family_rent = (rent_to_owner - prorated_hap).quantize(Decimal('1'), rounding=ROUND_DOWN)
            else:
                prorate_pct = Decimal(1)
                prorated_hap = hap_to_owner
                mixed_family_rent = tenant_rent

            # Store results
            self.results = {
                "head_of_household": inputs.get("head_of_household", ""),
                "voucher_size": voucher_size,
                "br_leased": br_leased,
                "rent_to_owner": rent_to_owner,
                "utility_allowance": utility_allowance,
                "ttp": ttp,
                "num_eligible": num_eligible,
                "num_ineligible": num_ineligible,
                "ha_staff": inputs.get("ha_staff", ""),
                "calculation_date": inputs.get("calculation_date", datetime.now().strftime("%m/%d/%Y")),

                # Calculated values
                "gross_rent": gross_rent,
                "fmr": fmr,
                "amount_above_fmr": amount_above_fmr,
                "total_hap": total_hap,
                "total_family_share": total_family_share,
                "hap_to_owner": hap_to_owner,
                "tenant_rent": tenant_rent,
                "utility_reimbursement": utility_reimbursement,

                # Mixed family
                "total_family_members": total_family_members,
                "is_mixed_family": is_mixed_family,
                "prorate_pct": prorate_pct,
                "prorated_hap": prorated_hap,
                "mixed_family_rent": mixed_family_rent,

                "supervisor_name": inputs.get("supervisor_name", ""),
                "supervisor_date": inputs.get("supervisor_date", "")
            }

            return True, self.results

        except Exception as e:
            return False, str(e)

    def get_results(self):
        """Return current calculation results."""
        return self.results


class PSHRentCalculatorApp:
    """Main application class with locked wizard UI and dashboard results."""

    def __init__(self, root):
        self.root = root
        self.root.title("PSH Rent Calculator")
        self.root.geometry("1000x750")
        self.root.configure(bg=COLOR_LIGHT_GRAY)

        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Initialize data
        self.fmr_db = FMRDatabase()
        self.calc_engine = RentCalculationEngine(self.fmr_db)

        # Wizard state
        self.current_step = 0
        self.steps = [
            {"name": "Household", "title": "Household Information"},
            {"name": "Finances", "title": "Financial Information"},
            {"name": "Family", "title": "Family Composition"},
            {"name": "Staff", "title": "Staff & Sign-off"},
            {"name": "Results", "title": "Calculation Results"}
        ]

        # Data storage
        self.current_inputs = {
            "head_of_household": "",
            "voucher_size": 0,
            "br_leased": 0,
            "rent_to_owner": 0,
            "utility_allowance": 0,
            "ttp": 50,
            "num_eligible": 1,
            "num_ineligible": 0,
            "ha_staff": "",
            "calculation_date": datetime.now().strftime("%m/%d/%Y"),
            "supervisor_name": "",
            "supervisor_date": ""
        }
        self.current_results = {}

        # Build UI
        self.build_ui()

        self.root.focus_set()

    def build_ui(self):
        """Build the main UI structure."""
        # Title bar
        title_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        title_frame.pack(fill=tk.X, padx=0, pady=0)

        title_label = tk.Label(title_frame, text="PSH RENT CALCULATOR",
                              font=("TkDefaultFont", 16, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        title_label.pack(anchor=tk.W, padx=20, pady=10)

        # FMR Settings button in top right
        settings_button = tk.Button(title_frame, text="⚙ FMR Settings", command=self.open_fmr_window,
                                   bg=COLOR_PRIMARY_BLUE, fg=COLOR_WHITE, font=("TkDefaultFont", 9),
                                   padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
        settings_button.pack(anchor=tk.NE, padx=20, pady=10)

        # Progress indicator
        self.build_progress_bar()

        # Main content area - will be replaced by steps
        self.content_frame = tk.Frame(self.root, bg=COLOR_LIGHT_GRAY)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Step frames (will be stacked, only one visible)
        self.step_frames = {}
        self.build_step1_frame()
        self.build_step2_frame()
        self.build_step3_frame()
        self.build_step4_frame()
        self.build_step5_frame()

        # Show first step
        self.show_step(0)

    def build_progress_bar(self):
        """Build the progress indicator."""
        progress_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        progress_frame.pack(fill=tk.X, padx=0, pady=0)

        steps_container = tk.Frame(progress_frame, bg=COLOR_WHITE)
        steps_container.pack(fill=tk.X, padx=20, pady=15)

        self.progress_labels = {}
        for i, step in enumerate(self.steps):
            step_frame = tk.Frame(steps_container, bg=COLOR_WHITE)
            step_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

            # Step number circle
            circle_label = tk.Label(step_frame, text=f"①②③④⑤"[i],
                                   font=("TkDefaultFont", 11, "bold"),
                                   bg=COLOR_LIGHT_GRAY, fg=COLOR_SECONDARY_GRAY,
                                   width=3, height=1, relief=tk.FLAT)
            circle_label.pack(side=tk.LEFT, padx=5)

            # Step name
            name_label = tk.Label(step_frame, text=step["name"],
                                 font=("TkDefaultFont", 9),
                                 bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY)
            name_label.pack(side=tk.LEFT, padx=5)

            self.progress_labels[i] = {"circle": circle_label, "name": name_label}

            # Connector line (except after last step)
            if i < len(self.steps) - 1:
                connector = tk.Label(step_frame, text="—", font=("TkDefaultFont", 10),
                                   bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY)
                connector.pack(side=tk.LEFT, padx=0)

        # Separator line
        separator = tk.Frame(progress_frame, height=1, bg="#e0e0e0")
        separator.pack(fill=tk.X, padx=0, pady=0)

    def update_progress(self):
        """Update progress indicator based on current step."""
        for i in range(len(self.steps)):
            if i < self.current_step:
                # Completed step - green checkmark
                self.progress_labels[i]["circle"].config(bg=COLOR_SUCCESS_GREEN, fg=COLOR_WHITE, text="✓")
                self.progress_labels[i]["name"].config(fg=COLOR_SUCCESS_GREEN, font=("TkDefaultFont", 9, "bold"))
            elif i == self.current_step:
                # Current step - blue highlight
                self.progress_labels[i]["circle"].config(bg=COLOR_PRIMARY_BLUE, fg=COLOR_WHITE, text=f"①②③④⑤"[i])
                self.progress_labels[i]["name"].config(fg=COLOR_PRIMARY_BLUE, font=("TkDefaultFont", 9, "bold"))
            else:
                # Future step - gray
                self.progress_labels[i]["circle"].config(bg=COLOR_LIGHT_GRAY, fg=COLOR_SECONDARY_GRAY, text=f"①②③④⑤"[i])
                self.progress_labels[i]["name"].config(fg=COLOR_SECONDARY_GRAY, font=("TkDefaultFont", 9))

    def show_step(self, step_num):
        """Show a specific step and hide others."""
        # Hide all steps
        for frame in self.step_frames.values():
            frame.pack_forget()

        # Show selected step
        self.current_step = step_num
        self.step_frames[step_num].pack(fill=tk.BOTH, expand=True)
        self.update_progress()

    def build_step1_frame(self):
        """Build Step 1: Household Information"""
        frame = tk.Frame(self.content_frame, bg=COLOR_WHITE)
        self.step_frames[0] = frame

        # Title
        title = tk.Label(frame, text="① Household Information",
                        font=("TkDefaultFont", 13, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))

        # Form frame
        form_frame = tk.Frame(frame, bg=COLOR_WHITE)
        form_frame.pack(fill=tk.X, padx=30, pady=10)

        # Head of Household
        tk.Label(form_frame, text="Head of Household Name", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))
        tk.Label(form_frame, text="Required field", font=("TkDefaultFont", 8, "italic"),
                bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W)

        self.hoh_var = tk.StringVar()
        self.hoh_entry = tk.Entry(form_frame, textvariable=self.hoh_var, font=("TkDefaultFont", 10),
                                  width=50)
        self.hoh_entry.pack(anchor=tk.W, pady=(3, 15), ipady=5)
        self.hoh_entry.focus()

        # Voucher Size
        tk.Label(form_frame, text="Voucher Bedroom Size", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))
        tk.Label(form_frame, text="The bedroom size authorized on the housing voucher",
                font=("TkDefaultFont", 8, "italic"),
                bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W)

        self.voucher_var = tk.StringVar(value="0")
        voucher_combo = tk.Spinbox(form_frame, from_=0, to=5, textvariable=self.voucher_var,
                                  font=("TkDefaultFont", 10), width=10,
                                  command=self.update_fmr_display)
        voucher_combo.pack(anchor=tk.W, pady=(3, 15), ipady=5)

        # BR Leased
        tk.Label(form_frame, text="Actual Bedrooms in Unit", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))
        tk.Label(form_frame, text="The actual number of bedrooms in the leased unit",
                font=("TkDefaultFont", 8, "italic"),
                bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W)

        self.br_leased_var = tk.StringVar(value="0")
        br_combo = tk.Spinbox(form_frame, from_=0, to=5, textvariable=self.br_leased_var,
                             font=("TkDefaultFont", 10), width=10,
                             command=self.update_fmr_display)
        br_combo.pack(anchor=tk.W, pady=(3, 15), ipady=5)

        # FMR info display
        self.fmr_info_label = tk.Label(frame, text="", font=("TkDefaultFont", 9),
                                       bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY)
        self.fmr_info_label.pack(anchor=tk.W, padx=30, pady=(5, 15))

        self.update_fmr_display()

        # Navigation buttons
        nav_frame = tk.Frame(frame, bg=COLOR_WHITE)
        nav_frame.pack(fill=tk.X, padx=20, pady=20)

        next_btn = tk.Button(nav_frame, text="Next →", command=self.step1_next,
                            bg=COLOR_PRIMARY_BLUE, fg=COLOR_WHITE, font=("TkDefaultFont", 10, "bold"),
                            padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
        next_btn.pack(side=tk.RIGHT)

    def update_fmr_display(self):
        """Update FMR info display on step 1."""
        try:
            v_size = int(self.voucher_var.get())
            br = int(self.br_leased_var.get())
            fmr_br = min(v_size, br)
            fmr = self.fmr_db.get_fmr(fmr_br)
            if fmr > 0:
                self.fmr_info_label.config(text=f"FMR will be based on {fmr_br}-bedroom rate: ${fmr:,}")
            else:
                self.fmr_info_label.config(text="")
        except:
            pass

    def build_step2_frame(self):
        """Build Step 2: Financial Information"""
        frame = tk.Frame(self.content_frame, bg=COLOR_WHITE)
        self.step_frames[1] = frame

        # Title
        title = tk.Label(frame, text="② Financial Information",
                        font=("TkDefaultFont", 13, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))

        # Form frame
        form_frame = tk.Frame(frame, bg=COLOR_WHITE)
        form_frame.pack(fill=tk.X, padx=30, pady=10)

        # Rent to Owner
        tk.Label(form_frame, text="Rent to Owner ($)", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))
        tk.Label(form_frame, text="Monthly contract rent amount paid to the property owner",
                font=("TkDefaultFont", 8, "italic"),
                bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W)

        self.rent_var = tk.StringVar(value="0")
        rent_entry = tk.Entry(form_frame, textvariable=self.rent_var, font=("TkDefaultFont", 10), width=20)
        rent_entry.pack(anchor=tk.W, pady=(3, 15), ipady=5)
        rent_entry.bind("<KeyRelease>", lambda e: self.update_financial_display())

        # Utility Allowance
        tk.Label(form_frame, text="Utility Allowance ($)", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))
        tk.Label(form_frame, text="Monthly allowance for tenant-paid utilities per PHA schedule",
                font=("TkDefaultFont", 8, "italic"),
                bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W)

        self.ua_var = tk.StringVar(value="0")
        ua_entry = tk.Entry(form_frame, textvariable=self.ua_var, font=("TkDefaultFont", 10), width=20)
        ua_entry.pack(anchor=tk.W, pady=(3, 15), ipady=5)
        ua_entry.bind("<KeyRelease>", lambda e: self.update_financial_display())

        # TTP
        tk.Label(form_frame, text="Total Tenant Payment / TTP ($)", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))
        tk.Label(form_frame, text="The household's share of rent (minimum $50 for PSH)",
                font=("TkDefaultFont", 8, "italic"),
                bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W)

        self.ttp_var = tk.StringVar(value="50")
        ttp_entry = tk.Entry(form_frame, textvariable=self.ttp_var, font=("TkDefaultFont", 10), width=20)
        ttp_entry.pack(anchor=tk.W, pady=(3, 15), ipady=5)
        ttp_entry.bind("<KeyRelease>", lambda e: self.update_financial_display())

        # Gross Rent display
        tk.Label(form_frame, text="Gross Rent (Rent + UA)", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(15, 3))

        self.gross_rent_label = tk.Label(form_frame, text="$0",
                                        font=("TkDefaultFont", 16, "bold"),
                                        bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        self.gross_rent_label.pack(anchor=tk.W, pady=(3, 15))

        # FMR comparison and warnings
        self.fmr_comparison_frame = tk.Frame(frame, bg=COLOR_WHITE)
        self.fmr_comparison_frame.pack(fill=tk.X, padx=30, pady=10)

        # TTP warning
        self.ttp_warning_label = tk.Label(frame, text="", bg=COLOR_WARNING_YELLOW,
                                          fg=COLOR_DARK_TEXT, font=("TkDefaultFont", 9),
                                          wraplength=600, justify=tk.LEFT, padx=10, pady=8)

        self.update_financial_display()

        # Navigation buttons
        nav_frame = tk.Frame(frame, bg=COLOR_WHITE)
        nav_frame.pack(fill=tk.X, padx=20, pady=20)

        back_btn = tk.Button(nav_frame, text="← Back", command=lambda: self.show_step(0),
                            bg=COLOR_SECONDARY_GRAY, fg=COLOR_WHITE, font=("TkDefaultFont", 10),
                            padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        back_btn.pack(side=tk.LEFT)

        next_btn = tk.Button(nav_frame, text="Next →", command=self.step2_next,
                            bg=COLOR_PRIMARY_BLUE, fg=COLOR_WHITE, font=("TkDefaultFont", 10, "bold"),
                            padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
        next_btn.pack(side=tk.RIGHT)

    def update_financial_display(self):
        """Update financial displays in step 2."""
        try:
            rent = float(self.rent_var.get() or 0)
            ua = float(self.ua_var.get() or 0)
            ttp = float(self.ttp_var.get() or 50)

            gross_rent = rent + ua
            self.gross_rent_label.config(text=f"${gross_rent:,}")

            # Get FMR for comparison
            v_size = int(self.voucher_var.get())
            br = int(self.br_leased_var.get())
            fmr_br = min(v_size, br)
            fmr = self.fmr_db.get_fmr(fmr_br)

            # Update FMR comparison
            for widget in self.fmr_comparison_frame.winfo_children():
                widget.destroy()

            if fmr > 0:
                tk.Label(self.fmr_comparison_frame, text=f"FMR for {fmr_br}-BR: ${fmr:,}",
                        font=("TkDefaultFont", 9),
                        bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W, pady=(5, 3))

                if gross_rent > fmr:
                    diff = int(gross_rent - fmr)
                    warning_label = tk.Label(self.fmr_comparison_frame,
                                            text=f"⚠ Gross Rent exceeds FMR by ${diff:,} — Supervisor approval required",
                                            font=("TkDefaultFont", 9), bg=COLOR_WARNING_RED,
                                            fg=COLOR_WHITE, padx=8, pady=6, relief=tk.FLAT)
                    warning_label.pack(anchor=tk.W, pady=(5, 0), fill=tk.X)

            # TTP warning
            self.ttp_warning_label.pack_forget()
            if ttp < 50:
                self.ttp_warning_label.config(text="⚠ TTP minimum is $50.00 per HUD rules. Value will be set to $50 when proceeding.")
                self.ttp_warning_label.pack(fill=tk.X, padx=30, pady=10)

        except ValueError:
            pass

    def build_step3_frame(self):
        """Build Step 3: Family Composition"""
        frame = tk.Frame(self.content_frame, bg=COLOR_WHITE)
        self.step_frames[2] = frame

        # Title
        title = tk.Label(frame, text="③ Family Composition",
                        font=("TkDefaultFont", 13, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))

        # Form frame
        form_frame = tk.Frame(frame, bg=COLOR_WHITE)
        form_frame.pack(fill=tk.X, padx=30, pady=10)

        # Number Eligible
        tk.Label(form_frame, text="Number Eligible", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))
        tk.Label(form_frame, text="Family members with eligible immigration status",
                font=("TkDefaultFont", 8, "italic"),
                bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W)

        self.num_eligible_var = tk.StringVar(value="1")
        eligible_spin = tk.Spinbox(form_frame, from_=1, to=20, textvariable=self.num_eligible_var,
                                  font=("TkDefaultFont", 10), width=10,
                                  command=self.update_family_display)
        eligible_spin.pack(anchor=tk.W, pady=(3, 15), ipady=5)
        eligible_spin.bind("<KeyRelease>", lambda e: self.update_family_display())

        # Number Ineligible
        tk.Label(form_frame, text="Number Ineligible", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))
        tk.Label(form_frame, text="Family members without eligible immigration status",
                font=("TkDefaultFont", 8, "italic"),
                bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY).pack(anchor=tk.W)

        self.num_ineligible_var = tk.StringVar(value="0")
        ineligible_spin = tk.Spinbox(form_frame, from_=0, to=20, textvariable=self.num_ineligible_var,
                                    font=("TkDefaultFont", 10), width=10,
                                    command=self.update_family_display)
        ineligible_spin.pack(anchor=tk.W, pady=(3, 15), ipady=5)
        ineligible_spin.bind("<KeyRelease>", lambda e: self.update_family_display())

        # Total Family Members
        tk.Label(form_frame, text="Total Family Members", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))

        self.total_family_label = tk.Label(form_frame, text="1",
                                          font=("TkDefaultFont", 14, "bold"),
                                          bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        self.total_family_label.pack(anchor=tk.W, pady=(3, 15))

        # Family status messages
        self.family_info_frame = tk.Frame(frame, bg=COLOR_WHITE)
        self.family_info_frame.pack(fill=tk.X, padx=30, pady=10)

        self.update_family_display()

        # Navigation buttons
        nav_frame = tk.Frame(frame, bg=COLOR_WHITE)
        nav_frame.pack(fill=tk.X, padx=20, pady=20)

        back_btn = tk.Button(nav_frame, text="← Back", command=lambda: self.show_step(1),
                            bg=COLOR_SECONDARY_GRAY, fg=COLOR_WHITE, font=("TkDefaultFont", 10),
                            padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        back_btn.pack(side=tk.LEFT)

        next_btn = tk.Button(nav_frame, text="Next →", command=self.step3_next,
                            bg=COLOR_PRIMARY_BLUE, fg=COLOR_WHITE, font=("TkDefaultFont", 10, "bold"),
                            padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
        next_btn.pack(side=tk.RIGHT)

    def update_family_display(self):
        """Update family composition displays in step 3."""
        try:
            eligible = int(self.num_eligible_var.get() or 1)
            ineligible = int(self.num_ineligible_var.get() or 0)
            total = eligible + ineligible

            self.total_family_label.config(text=str(total))

            # Clear previous info
            for widget in self.family_info_frame.winfo_children():
                widget.destroy()

            if ineligible > 0:
                prorate_pct = (eligible / total) * 100
                info_frame = tk.Frame(self.family_info_frame, bg=COLOR_WARNING_YELLOW, relief=tk.FLAT)
                info_frame.pack(fill=tk.X, pady=10, padx=0)

                tk.Label(info_frame, text="⚠ MIXED FAMILY DETECTED",
                        font=("TkDefaultFont", 10, "bold"), bg=COLOR_WARNING_YELLOW,
                        fg=COLOR_DARK_TEXT).pack(anchor=tk.W, padx=10, pady=(8, 3))

                tk.Label(info_frame, text=f"Proration will apply: {eligible}/{total} = {prorate_pct:.1f}% of HAP",
                        font=("TkDefaultFont", 9), bg=COLOR_WARNING_YELLOW,
                        fg=COLOR_DARK_TEXT).pack(anchor=tk.W, padx=10, pady=(0, 3))

                tk.Label(info_frame, text="This means the housing assistance will be reduced proportionally.",
                        font=("TkDefaultFont", 9), bg=COLOR_WARNING_YELLOW,
                        fg=COLOR_DARK_TEXT).pack(anchor=tk.W, padx=10, pady=(0, 8))
            else:
                info_label = tk.Label(self.family_info_frame,
                                     text="✓ All family members are eligible. No proration needed.",
                                     font=("TkDefaultFont", 9), bg=COLOR_SUCCESS_GREEN,
                                     fg=COLOR_WHITE, padx=10, pady=8, relief=tk.FLAT)
                info_label.pack(fill=tk.X, pady=10)

        except ValueError:
            pass

    def build_step4_frame(self):
        """Build Step 4: Staff & Sign-off"""
        frame = tk.Frame(self.content_frame, bg=COLOR_WHITE)
        self.step_frames[3] = frame

        # Title
        title = tk.Label(frame, text="④ Staff & Sign-off",
                        font=("TkDefaultFont", 13, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))

        # Form frame
        form_frame = tk.Frame(frame, bg=COLOR_WHITE)
        form_frame.pack(fill=tk.X, padx=30, pady=10)

        # HA Staff Name
        tk.Label(form_frame, text="HA Staff Name", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))

        self.staff_var = tk.StringVar()
        staff_entry = tk.Entry(form_frame, textvariable=self.staff_var,
                              font=("TkDefaultFont", 10), width=50)
        staff_entry.pack(anchor=tk.W, pady=(3, 15), ipady=5)

        # Calculation Date
        tk.Label(form_frame, text="Calculation Date (MM/DD/YYYY)", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))

        self.date_var = tk.StringVar(value=datetime.now().strftime("%m/%d/%Y"))
        date_entry = tk.Entry(form_frame, textvariable=self.date_var,
                             font=("TkDefaultFont", 10), width=20)
        date_entry.pack(anchor=tk.W, pady=(3, 15), ipady=5)

        # Supervisor info section (conditional)
        self.supervisor_section = tk.Frame(frame, bg=COLOR_WHITE)
        self.supervisor_section.pack(fill=tk.X, padx=30, pady=10)

        # Supervisor Name
        tk.Label(self.supervisor_section, text="Supervisor Name", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))

        self.supervisor_var = tk.StringVar()
        supervisor_entry = tk.Entry(self.supervisor_section, textvariable=self.supervisor_var,
                                   font=("TkDefaultFont", 10), width=50)
        supervisor_entry.pack(anchor=tk.W, pady=(3, 15), ipady=5)

        # Supervisor Date
        tk.Label(self.supervisor_section, text="Supervisor Date (MM/DD/YYYY)",
                font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_WHITE, fg=COLOR_DARK_TEXT).pack(anchor=tk.W, pady=(10, 3))

        self.supervisor_date_var = tk.StringVar()
        supervisor_date_entry = tk.Entry(self.supervisor_section, textvariable=self.supervisor_date_var,
                                        font=("TkDefaultFont", 10), width=20)
        supervisor_date_entry.pack(anchor=tk.W, pady=(3, 15), ipady=5)

        # Approval status (will be updated)
        self.approval_status_frame = tk.Frame(frame, bg=COLOR_WHITE)
        self.approval_status_frame.pack(fill=tk.X, padx=30, pady=10)

        self.update_approval_status()

        # Navigation buttons
        nav_frame = tk.Frame(frame, bg=COLOR_WHITE)
        nav_frame.pack(fill=tk.X, padx=20, pady=20)

        back_btn = tk.Button(nav_frame, text="← Back", command=lambda: self.show_step(2),
                            bg=COLOR_SECONDARY_GRAY, fg=COLOR_WHITE, font=("TkDefaultFont", 10),
                            padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        back_btn.pack(side=tk.LEFT)

        calculate_btn = tk.Button(nav_frame, text="Calculate", command=self.step4_calculate,
                                 bg=COLOR_SUCCESS_GREEN, fg=COLOR_WHITE,
                                 font=("TkDefaultFont", 11, "bold"),
                                 padx=25, pady=10, relief=tk.FLAT, cursor="hand2")
        calculate_btn.pack(side=tk.RIGHT)

    def update_approval_status(self):
        """Update supervisor approval requirement display."""
        for widget in self.approval_status_frame.winfo_children():
            widget.destroy()

        try:
            rent = float(self.rent_var.get() or 0)
            ua = float(self.ua_var.get() or 0)
            gross_rent = rent + ua

            v_size = int(self.voucher_var.get())
            br = int(self.br_leased_var.get())
            fmr_br = min(v_size, br)
            fmr = self.fmr_db.get_fmr(fmr_br)

            if gross_rent > fmr and fmr > 0:
                # Supervisor required
                warning_frame = tk.Frame(self.approval_status_frame, bg=COLOR_WARNING_RED, relief=tk.FLAT)
                warning_frame.pack(fill=tk.X, pady=10)

                tk.Label(warning_frame, text="⚠ SUPERVISOR APPROVAL REQUIRED",
                        font=("TkDefaultFont", 10, "bold"), bg=COLOR_WARNING_RED,
                        fg=COLOR_WHITE).pack(anchor=tk.W, padx=10, pady=(8, 3))

                tk.Label(warning_frame, text="Gross rent exceeds Fair Market Rent",
                        font=("TkDefaultFont", 9), bg=COLOR_WARNING_RED,
                        fg=COLOR_WHITE).pack(anchor=tk.W, padx=10, pady=(0, 8))
            else:
                # No supervisor needed
                info_label = tk.Label(self.approval_status_frame,
                                     text="✓ Rent is within FMR limits. No supervisor approval needed.",
                                     font=("TkDefaultFont", 9), bg=COLOR_SUCCESS_GREEN,
                                     fg=COLOR_WHITE, padx=10, pady=8, relief=tk.FLAT)
                info_label.pack(fill=tk.X, pady=10)
        except ValueError:
            pass

    def build_step5_frame(self):
        """Build Step 5: Results Dashboard"""
        frame = tk.Frame(self.content_frame, bg=COLOR_WHITE)
        self.step_frames[4] = frame

        # Title
        title = tk.Label(frame, text="⑤ Calculation Results",
                        font=("TkDefaultFont", 13, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))

        # Scrollable content area
        canvas = tk.Canvas(frame, bg=COLOR_WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_WHITE)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Dashboard content will be built here
        self.results_container = scrollable_frame

        # Results will be populated on step 5
        self.result_widgets = {}

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons at bottom
        button_frame = tk.Frame(frame, bg=COLOR_WHITE)
        button_frame.pack(fill=tk.X, padx=20, pady=15)

        new_calc_btn = tk.Button(button_frame, text="New Calculation", command=self.new_calculation,
                                bg=COLOR_SECONDARY_GRAY, fg=COLOR_WHITE, font=("TkDefaultFont", 10),
                                padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        new_calc_btn.pack(side=tk.LEFT, padx=5)

        copy_btn = tk.Button(button_frame, text="Copy to Clipboard", command=self.copy_results,
                            bg=COLOR_SECONDARY_GRAY, fg=COLOR_WHITE, font=("TkDefaultFont", 10),
                            padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        copy_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(button_frame, text="Save as Text", command=self.save_results,
                            bg=COLOR_SECONDARY_GRAY, fg=COLOR_WHITE, font=("TkDefaultFont", 10),
                            padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=5)

    def display_results(self):
        """Build and display the results dashboard."""
        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        r = self.current_results

        # Summary cards row
        cards_frame = tk.Frame(self.results_container, bg=COLOR_WHITE)
        cards_frame.pack(fill=tk.X, padx=20, pady=15)

        # HAP to Owner card
        hap_card = self.create_result_card(cards_frame, "HAP TO OWNER",
                                          f"${int(r['hap_to_owner']):,}",
                                          COLOR_SUCCESS_GREEN)
        hap_card.pack(side=tk.LEFT, expand=True, padx=5)

        # Tenant Rent card
        tenant_card = self.create_result_card(cards_frame, "TENANT RENT",
                                             f"${int(r['tenant_rent']):,}",
                                             COLOR_PRIMARY_BLUE)
        tenant_card.pack(side=tk.LEFT, expand=True, padx=5)

        # Utility Reimbursement card
        utility_card = self.create_result_card(cards_frame, "UTILITY REIMB.",
                                              f"${int(r['utility_reimbursement']):,}",
                                              COLOR_PRIMARY_BLUE)
        utility_card.pack(side=tk.LEFT, expand=True, padx=5)

        # Above FMR warning (if applicable)
        if r['amount_above_fmr'] > 0:
            above_fmr_frame = tk.Frame(self.results_container, bg=COLOR_WARNING_RED, relief=tk.FLAT)
            above_fmr_frame.pack(fill=tk.X, padx=20, pady=10)

            tk.Label(above_fmr_frame,
                    text=f"⚠ ABOVE FMR BY ${int(r['amount_above_fmr']):,} — SUPERVISOR APPROVAL REQUIRED",
                    font=("TkDefaultFont", 10, "bold"), bg=COLOR_WARNING_RED,
                    fg=COLOR_WHITE).pack(padx=10, pady=10)

        # Mixed family info (if applicable)
        if r['is_mixed_family']:
            mixed_frame = tk.Frame(self.results_container, bg=COLOR_WARNING_YELLOW, relief=tk.FLAT)
            mixed_frame.pack(fill=tk.X, padx=20, pady=10)

            prorate_pct_display = float(r['prorate_pct']) * 100
            tk.Label(mixed_frame,
                    text=f"MIXED FAMILY: Prorated HAP = ${int(r['prorated_hap']):,} ({prorate_pct_display:.1f}%)",
                    font=("TkDefaultFont", 10, "bold"), bg=COLOR_WARNING_YELLOW,
                    fg=COLOR_DARK_TEXT).pack(anchor=tk.W, padx=10, pady=(8, 3))

            tk.Label(mixed_frame,
                    text=f"Mixed Family Rent = ${int(r['mixed_family_rent']):,}",
                    font=("TkDefaultFont", 10), bg=COLOR_WARNING_YELLOW,
                    fg=COLOR_DARK_TEXT).pack(anchor=tk.W, padx=10, pady=(0, 8))

        # Detailed breakdown table
        breakdown_label = tk.Label(self.results_container, text="Detailed Breakdown",
                                  font=("TkDefaultFont", 11, "bold"), bg=COLOR_WHITE,
                                  fg=COLOR_PRIMARY_BLUE)
        breakdown_label.pack(anchor=tk.W, padx=20, pady=(15, 5))

        table_frame = tk.Frame(self.results_container, bg=COLOR_WHITE)
        table_frame.pack(fill=tk.X, padx=20, pady=5)

        # Build breakdown table
        breakdown_items = [
            ("1", "Rent to Owner", f"${int(r['rent_to_owner']):,}"),
            ("2", "Utility Allowance", f"${int(r['utility_allowance']):,}"),
            ("3", "Gross Rent", f"${int(r['gross_rent']):,}"),
            ("4", "2025 FMR", f"${int(r['fmr']):,}"),
            ("5", "Lower of FMR or GR", f"${int(min(r['gross_rent'], r['fmr'])):,}"),
            ("6", "Amount Above FMR", f"${int(r['amount_above_fmr']):,}", COLOR_WARNING_RED if r['amount_above_fmr'] > 0 else None),
            ("7", "TTP ($50 Minimum)", f"${int(r['ttp']):,}"),
            ("8", "Total HAP", f"${int(r['total_hap']):,}"),
            ("9", "Total Family Share", f"${int(r['total_family_share']):,}"),
            ("10", "HAP to Owner", f"${int(r['hap_to_owner']):,}", COLOR_SUCCESS_GREEN),
            ("11", "Tenant Rent", f"${int(r['tenant_rent']):,}"),
            ("12", "Utility Reimbursement", f"${int(r['utility_reimbursement']):,}"),
        ]

        # Proration section
        if r['is_mixed_family']:
            breakdown_items.append((None, "--- PRORATED ASSISTANCE ---", ""))
            breakdown_items.append(("13", "Normal HAP", f"${int(r['hap_to_owner']):,}"))
            breakdown_items.append(("14", "Number Eligible", str(r['num_eligible'])))
            breakdown_items.append(("15", "Number Ineligible", str(r['num_ineligible'])))
            breakdown_items.append(("16", "Total Family Members", str(r['total_family_members'])))
            prorate_pct_pct = float(r['prorate_pct']) * 100
            breakdown_items.append(("17", "Prorate %", f"{prorate_pct_pct:.2f}%"))
            breakdown_items.append(("18", "Prorated HAP", f"${int(r['prorated_hap']):,}"))
            breakdown_items.append(("19", "Mixed Family Rent", f"${int(r['mixed_family_rent']):,}"))
        else:
            breakdown_items.append(("13", "Number Eligible", str(r['num_eligible'])))
            breakdown_items.append(("14", "Number Ineligible", str(r['num_ineligible'])))
            breakdown_items.append(("15", "Total Family Members", str(r['total_family_members'])))

        # Create table rows
        for idx, item in enumerate(breakdown_items):
            if item[0] is None:
                # Section header
                sep_label = tk.Label(table_frame, text=item[1], font=("TkDefaultFont", 9, "bold"),
                                    bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY)
                sep_label.pack(anchor=tk.W, pady=(10, 3))
            else:
                row_frame = tk.Frame(table_frame,
                                    bg=COLOR_LIGHT_GRAY if idx % 2 == 0 else COLOR_WHITE,
                                    relief=tk.FLAT)
                row_frame.pack(fill=tk.X, pady=1)

                # Determine if this row needs special coloring
                bg_color = COLOR_LIGHT_GRAY if idx % 2 == 0 else COLOR_WHITE
                if len(item) > 3 and item[3]:
                    bg_color = item[3]
                    fg_color = COLOR_WHITE if item[3] == COLOR_WARNING_RED else COLOR_DARK_TEXT
                else:
                    fg_color = COLOR_DARK_TEXT

                row_frame.config(bg=bg_color)

                # Number
                tk.Label(row_frame, text=item[0], font=("TkDefaultFont", 9),
                        bg=bg_color, fg=fg_color, width=3).pack(side=tk.LEFT, padx=8, pady=5)

                # Item name
                tk.Label(row_frame, text=item[1], font=("TkDefaultFont", 9),
                        bg=bg_color, fg=fg_color).pack(side=tk.LEFT, expand=True, anchor=tk.W, padx=5)

                # Amount
                tk.Label(row_frame, text=item[2], font=("TkDefaultFont", 9, "bold"),
                        bg=bg_color, fg=fg_color).pack(side=tk.RIGHT, padx=10, pady=5)

        # Staff info section
        info_frame = tk.Frame(self.results_container, bg=COLOR_LIGHT_GRAY, relief=tk.FLAT)
        info_frame.pack(fill=tk.X, padx=20, pady=20)

        staff_text = f"HA Staff: {r['head_of_household']} ({self.staff_var.get()})  |  Date: {r['calculation_date']}"
        if r['supervisor_name']:
            staff_text += f"  |  Supervisor: {r['supervisor_name']}"

        tk.Label(info_frame, text=staff_text, font=("TkDefaultFont", 9),
                bg=COLOR_LIGHT_GRAY, fg=COLOR_SECONDARY_GRAY, wraplength=600,
                justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=8)

    def create_result_card(self, parent, label, amount, bg_color):
        """Create a summary result card."""
        card = tk.Frame(parent, bg=bg_color, relief=tk.FLAT)

        label_widget = tk.Label(card, text=label, font=("TkDefaultFont", 9),
                               bg=bg_color, fg=COLOR_WHITE)
        label_widget.pack(padx=15, pady=(12, 3))

        amount_widget = tk.Label(card, text=amount, font=("TkDefaultFont", 20, "bold"),
                                bg=bg_color, fg=COLOR_WHITE)
        amount_widget.pack(padx=15, pady=(3, 12))

        return card

    def step1_next(self):
        """Validate step 1 and proceed."""
        if not self.hoh_var.get().strip():
            messagebox.showerror("Validation Error", "Please enter Head of Household name")
            return

        self.current_inputs["head_of_household"] = self.hoh_var.get()
        self.current_inputs["voucher_size"] = int(self.voucher_var.get())
        self.current_inputs["br_leased"] = int(self.br_leased_var.get())

        self.show_step(1)

    def step2_next(self):
        """Validate step 2 and proceed."""
        try:
            rent = float(self.rent_var.get() or 0)
            ua = float(self.ua_var.get() or 0)
            ttp = float(self.ttp_var.get() or 0)

            if rent <= 0:
                messagebox.showerror("Validation Error", "Rent to Owner must be greater than $0")
                return

            if ua < 0:
                messagebox.showerror("Validation Error", "Utility Allowance cannot be negative")
                return

            if ttp < 50:
                ttp = 50

            self.current_inputs["rent_to_owner"] = rent
            self.current_inputs["utility_allowance"] = ua
            self.current_inputs["ttp"] = ttp

            self.show_step(2)
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid numeric values")

    def step3_next(self):
        """Validate step 3 and proceed."""
        try:
            eligible = int(self.num_eligible_var.get() or 1)
            ineligible = int(self.num_ineligible_var.get() or 0)

            if eligible < 1:
                messagebox.showerror("Validation Error", "Number Eligible must be at least 1")
                return

            self.current_inputs["num_eligible"] = eligible
            self.current_inputs["num_ineligible"] = ineligible

            self.show_step(3)
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid integer values")

    def step4_calculate(self):
        """Perform calculation and move to results."""
        if not self.staff_var.get().strip():
            messagebox.showerror("Validation Error", "Please enter HA Staff Name")
            return

        # Check if supervisor approval required
        rent = float(self.rent_var.get() or 0)
        ua = float(self.ua_var.get() or 0)
        gross_rent = rent + ua

        v_size = int(self.voucher_var.get())
        br = int(self.br_leased_var.get())
        fmr_br = min(v_size, br)
        fmr = self.fmr_db.get_fmr(fmr_br)

        if gross_rent > fmr and fmr > 0:
            if not self.supervisor_var.get().strip():
                messagebox.showerror("Validation Error",
                                   "Supervisor Name is required when Gross Rent exceeds FMR")
                return

        # Gather all inputs
        self.current_inputs.update({
            "ha_staff": self.staff_var.get(),
            "calculation_date": self.date_var.get(),
            "supervisor_name": self.supervisor_var.get(),
            "supervisor_date": self.supervisor_date_var.get()
        })

        # Perform calculation
        success, result = self.calc_engine.calculate(self.current_inputs)

        if not success:
            messagebox.showerror("Calculation Error", result)
            return

        self.current_results = result

        # Display results
        self.display_results()
        self.show_step(4)

    def new_calculation(self):
        """Reset all fields and start over."""
        if not messagebox.askyesno("Confirm", "Clear all data and start a new calculation?"):
            return

        self.current_inputs = {
            "head_of_household": "",
            "voucher_size": 0,
            "br_leased": 0,
            "rent_to_owner": 0,
            "utility_allowance": 0,
            "ttp": 50,
            "num_eligible": 1,
            "num_ineligible": 0,
            "ha_staff": "",
            "calculation_date": datetime.now().strftime("%m/%d/%Y"),
            "supervisor_name": "",
            "supervisor_date": ""
        }
        self.current_results = {}

        # Reset all UI fields
        self.hoh_var.set("")
        self.voucher_var.set("0")
        self.br_leased_var.set("0")
        self.rent_var.set("0")
        self.ua_var.set("0")
        self.ttp_var.set("50")
        self.num_eligible_var.set("1")
        self.num_ineligible_var.set("0")
        self.staff_var.set("")
        self.date_var.set(datetime.now().strftime("%m/%d/%Y"))
        self.supervisor_var.set("")
        self.supervisor_date_var.set("")

        self.update_fmr_display()
        self.update_financial_display()
        self.update_family_display()

        self.show_step(0)
        self.hoh_entry.focus()

    def copy_results(self):
        """Copy results to clipboard."""
        text = self.format_results_text()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Success", "Results copied to clipboard")

    def save_results(self):
        """Save results to text file."""
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not filepath:
            return

        try:
            text = self.format_results_text()
            with open(filepath, 'w') as f:
                f.write(text)
            messagebox.showinfo("Success", f"Results saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def format_results_text(self):
        """Format results as text."""
        r = self.current_results
        lines = []

        lines.append("=" * 70)
        lines.append("PSH RENT CALCULATION SUMMARY".center(70))
        lines.append("=" * 70)
        lines.append("")

        lines.append(f"Head of Household: {r['head_of_household']}")
        lines.append(f"Calculation Date: {r['calculation_date']}")
        lines.append(f"HA Staff: {r['ha_staff']}")
        if r['supervisor_name']:
            lines.append(f"Supervisor: {r['supervisor_name']} ({r['supervisor_date']})")
        lines.append("")

        lines.append("-" * 70)
        lines.append("INPUT INFORMATION")
        lines.append("-" * 70)
        lines.append(f"Voucher Size (Bedrooms):        {r['voucher_size']}")
        lines.append(f"# Bedrooms Leased:              {r['br_leased']}")
        lines.append(f"Rent to Owner:                  ${int(r['rent_to_owner']):,}")
        lines.append(f"Utility Allowance:              ${int(r['utility_allowance']):,}")
        lines.append(f"Total Tenant Payment (TTP):     ${int(r['ttp']):,}")
        lines.append("")

        lines.append("-" * 70)
        lines.append("RENT CALCULATION")
        lines.append("-" * 70)
        lines.append(f"Gross Rent (Rent + UA):         ${int(r['gross_rent']):,}")
        lines.append(f"Fair Market Rent (FMR):         ${int(r['fmr']):,}")

        if r['amount_above_fmr'] > 0:
            lines.append(f"Amount Above FMR:               ${int(r['amount_above_fmr']):,} [SUPERVISOR APPROVAL REQUIRED]")
        else:
            lines.append(f"Amount Above FMR:               ${int(r['amount_above_fmr']):,}")

        lines.append("")
        lines.append(f"Total HAP (Gross Rent - TTP):   ${int(r['total_hap']):,}")
        lines.append(f"Total Family Share (TTP):       ${int(r['total_family_share']):,}")
        lines.append(f"HAP to Owner:                   ${int(r['hap_to_owner']):,}")
        lines.append(f"Tenant Rent to Owner:           ${int(r['tenant_rent']):,}")
        lines.append(f"Utility Reimbursement:          ${int(r['utility_reimbursement']):,}")
        lines.append("")

        if r['is_mixed_family']:
            lines.append("-" * 70)
            lines.append("PRORATED ASSISTANCE (MIXED FAMILY)")
            lines.append("-" * 70)
            lines.append(f"Number Eligible:                {r['num_eligible']}")
            lines.append(f"Number Ineligible:              {r['num_ineligible']}")
            lines.append(f"Total Family Members:           {r['total_family_members']}")
            prorate_pct = float(r['prorate_pct']) * 100
            lines.append(f"Prorate Percentage:             {prorate_pct:.2f}%")
            lines.append(f"Prorated HAP:                   ${int(r['prorated_hap']):,}")
            lines.append(f"Mixed Family Rent:              ${int(r['mixed_family_rent']):,}")
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def open_fmr_window(self):
        """Open FMR management window."""
        fmr_window = tk.Toplevel(self.root)
        fmr_window.title("FMR Settings")
        fmr_window.geometry("600x450")
        fmr_window.resizable(False, False)

        # Center on parent
        fmr_window.transient(self.root)
        fmr_window.grab_set()

        # Title
        title = tk.Label(fmr_window, text="Fair Market Rent (FMR) Management",
                        font=("TkDefaultFont", 12, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY_BLUE)
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))

        # Effective date
        date_label = tk.Label(fmr_window, text=f"Effective Date: {self.fmr_db.effective_date}",
                             font=("TkDefaultFont", 9), bg=COLOR_WHITE, fg=COLOR_SECONDARY_GRAY)
        date_label.pack(anchor=tk.W, padx=20, pady=(0, 10))

        # FMR Table
        table_frame = tk.Frame(fmr_window, bg=COLOR_WHITE)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Headers
        header_frame = tk.Frame(table_frame, bg=COLOR_LIGHT_GRAY)
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="Bedrooms", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_LIGHT_GRAY, fg=COLOR_DARK_TEXT, width=12).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Label(header_frame, text="Payment Standard", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_LIGHT_GRAY, fg=COLOR_DARK_TEXT, width=18).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Label(header_frame, text="FMR", font=("TkDefaultFont", 10, "bold"),
                bg=COLOR_LIGHT_GRAY, fg=COLOR_DARK_TEXT, width=18).pack(side=tk.LEFT, padx=5, pady=5)

        # Data rows
        for br in range(6):
            fmr_data = self.fmr_db.fmr_data.get(br, {"payment_standard": 0, "fmr": 0})
            row_frame = tk.Frame(table_frame, bg=COLOR_WHITE if br % 2 == 0 else COLOR_LIGHT_GRAY)
            row_frame.pack(fill=tk.X)

            tk.Label(row_frame, text=str(br), font=("TkDefaultFont", 9),
                    bg=row_frame.cget("bg"), width=12).pack(side=tk.LEFT, padx=5, pady=5)
            tk.Label(row_frame, text=f"${fmr_data['payment_standard']:,}", font=("TkDefaultFont", 9),
                    bg=row_frame.cget("bg"), width=18).pack(side=tk.LEFT, padx=5, pady=5)
            tk.Label(row_frame, text=f"${fmr_data['fmr']:,}", font=("TkDefaultFont", 9),
                    bg=row_frame.cget("bg"), width=18).pack(side=tk.LEFT, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(fmr_window, bg=COLOR_WHITE)
        button_frame.pack(fill=tk.X, padx=20, pady=15)

        upload_btn = tk.Button(button_frame, text="Upload CSV", command=self.upload_fmr_csv,
                              bg=COLOR_PRIMARY_BLUE, fg=COLOR_WHITE, font=("TkDefaultFont", 10),
                              padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        upload_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(button_frame, text="Reset to Default", command=self.reset_fmr,
                             bg=COLOR_WARNING_YELLOW, fg=COLOR_DARK_TEXT, font=("TkDefaultFont", 10),
                             padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        reset_btn.pack(side=tk.LEFT, padx=5)

        close_btn = tk.Button(button_frame, text="Close", command=fmr_window.destroy,
                             bg=COLOR_SECONDARY_GRAY, fg=COLOR_WHITE, font=("TkDefaultFont", 10),
                             padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
        close_btn.pack(side=tk.RIGHT, padx=5)

        # Info text
        info = tk.Label(fmr_window, text="CSV format: bedrooms,payment_standard,fmr",
                       font=("TkDefaultFont", 8, "italic"), bg=COLOR_WHITE,
                       fg=COLOR_SECONDARY_GRAY)
        info.pack(anchor=tk.W, padx=20, pady=(0, 10))

    def upload_fmr_csv(self):
        """Upload FMR data from CSV."""
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filepath:
            return

        try:
            self.fmr_db.load_from_csv(filepath)
            messagebox.showinfo("Success", "FMR data loaded successfully")
            self.update_fmr_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def reset_fmr(self):
        """Reset FMR to default."""
        if messagebox.askyesno("Confirm", "Reset FMR to default 2025 values?"):
            self.fmr_db.fmr_data = self.fmr_db.DEFAULT_FMR.copy()
            self.fmr_db.effective_date = "2025-01-01"
            self.fmr_db.save_to_file()
            messagebox.showinfo("Success", "FMR data reset to default")
            self.update_fmr_display()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = PSHRentCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
