"""Riyadh Urban Intelligence Lab - 2-Day Event Quotation (Misk, 27-28 September 2026).

Base BOQ rates supplied by the client, uplifted by 3% and rounded to whole riyals. Day 2 carries a 50%
reduction on all equipment lines except Photography & Videography. Catering
(lunch + coffee break) is charged per person per day with no Day 2 discount.
"""

from fpdf import FPDF
import csv
import os

CLIENT_CONTACT = "Anarah Dhaka"
CLIENT_ORG = "atomcamp Arabia"

PAX_CATERING = 90
CATERING_RATE = 210            # SAR per person per day (client supplied, no uplift)
VAT_RATE = 0.15

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STAMP_FILE = os.path.join(BASE_DIR, "Miradore_Stamp_Riyadh.png")
SIGNATURE_FILE = os.path.join(BASE_DIR, "Adeel_Ahmed_Signature.png")

# Day-1 unit rates: the supplied base BOQ rate plus ~3%, then settled on a whole
# riyal that also halves to a whole riyal, so every figure in the quotation is a
# round number. Overall this lands at 3.08% over the base BOQ.
# (S#, description, qty, unit, base rate, quoted day-1 rate, day-2 discounted?)
EQUIPMENT = [
    (1, "Round Tables - suitable for group activity setup", 10, "Table", 85, 88, True),
    (2, "Chairs - banquet / event chairs (8 pax per table)", 80, "Chair", 45, 46, True),
    (3, "Professional Normal Sound System - complete package up to 100 pax "
        "(speakers, mixer, microphones, amplifiers, cabling, stands, technician)",
        1, "Lot", 4500, 4650, True),
    (4, "Stage Platform - 6.0m (W) x 3.0m (D) x 0.60m (H), black carpet, "
        "skirting and 2 steps (each side)", 18, "m2 (6x3)", 180, 186, True),
    (5, "SMD LED Screen - 5.0m (W) x 3.0m (H) P2.6 indoor, with supporting "
        "structure, processor and technician", 15, "m2 (5x3)", 300, 310, True),
    (6, "Branded Media Wall - 3.6m x 2.4m, complete with production, "
        "structure and installation", 1, "Lot", 5500, 5670, True),
    (7, "Registration Desk with Branded Back Wall - complete branded "
        "registration setup", 1, "Lot", 7500, 7730, True),
    (8, "Professional Photography & Videography Coverage", 1, "Day", 3500, 3605, False),
]


def build_rows():
    """Return equipment rows with quoted rates and both-day totals."""
    rows = []
    for sn, desc, qty, unit, base_rate, d1_rate, discounted in EQUIPMENT:
        d1_total = d1_rate * qty
        if discounted:
            d2_rate, d2_total = d1_rate // 2, d1_total // 2
            # every quoted rate must halve cleanly, or the printed figures would
            # not add up to the printed totals
            assert d1_rate % 2 == 0 and d1_total % 2 == 0, f"line {sn} does not halve evenly"
        else:
            d2_rate, d2_total = d1_rate, d1_total
        rows.append({
            "sn": sn, "desc": desc, "qty": qty, "unit": unit, "base_rate": base_rate,
            "d1_rate": d1_rate, "d1_total": d1_total,
            "d2_rate": d2_rate, "d2_total": d2_total,
            "two_day": d1_total + d2_total,
            "discounted": discounted,
        })
    return rows


CATERING = {
    "sn": 9,
    "desc": "Lunch & Coffee Break - full-day catering package per delegate",
    "qty": PAX_CATERING, "unit": "Pax",
    "d1_rate": CATERING_RATE, "d1_total": CATERING_RATE * PAX_CATERING,
    "d2_rate": CATERING_RATE, "d2_total": CATERING_RATE * PAX_CATERING,
    "two_day": CATERING_RATE * PAX_CATERING * 2,
    "discounted": False,
}


def money(value):
    return f"{value:,.0f}"


class QuotationPDF(FPDF):
    """Single-page portrait A4 quotation.

    Widths total the 190mm of usable page, and the vertical metrics are sized
    so the whole document lands on one page; PAGE_LIMIT is asserted after
    rendering so a future edit that overflows fails loudly instead of silently
    spilling onto a second page.
    """

    TEAL = (0, 128, 128)
    ORANGE = (230, 100, 30)
    DARK = (40, 40, 40)
    GRAY = (100, 100, 100)
    LIGHT_BG = (245, 248, 250)
    WHITE = (255, 255, 255)
    SECTION_BG = (230, 243, 243)
    RULE = (225, 232, 235)

    L, R = 10.0, 200.0          # left / right page edges
    W = R - L                   # 190mm of usable width
    PAGE_LIMIT = 283.0          # last usable y before the footer band

    W_SN, W_DESC, W_QTY, W_UNIT = 8, 68, 10, 14
    W_D1R, W_D1T, W_D2R, W_D2T, W_TOT = 17, 19, 17, 19, 18
    W_LEAD = W_SN + W_DESC + W_QTY + W_UNIT

    FS_ROW = 6.5
    ROW_MIN_H = 6.4
    LINE_H = 3.3

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 6.5)
        self.set_text_color(*self.GRAY)
        self.cell(0, 6, "Miradore Experiences, Riyadh  |  Riyadh Urban Intelligence Lab  |  "
                        "atomcamp Arabia  |  Confidential", align="C")

    def add_logo_header(self):
        logo = os.path.join(BASE_DIR, "Miradore Logo Color.png")
        if os.path.exists(logo):
            self.image(logo, x=self.L, y=8, w=44)
        self.set_xy(110, 9)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.DARK)
        self.cell(90, 4.5, "MIRADORE EXPERIENCES, RIYADH", align="R")
        self.set_xy(110, 13.5)
        self.set_font("Helvetica", "", 6.6)
        self.set_text_color(*self.GRAY)
        self.cell(90, 4.5, "Event Production  |  Branding  |  Technical Delivery", align="R")

    def rule(self, y, weight=0.7, color=None):
        self.set_draw_color(*(color or self.TEAL))
        self.set_line_width(weight)
        self.line(self.L, y, self.R, y)

    def add_title_block(self):
        self.rule(21)
        self.set_xy(self.L, 23)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*self.TEAL)
        self.cell(self.W, 7, "DETAILED BOQ  -  QUOTATION", align="C")
        self.set_xy(self.L, 30)
        self.set_font("Helvetica", "B", 8.8)
        self.set_text_color(*self.ORANGE)
        self.cell(self.W, 5, "RIYADH URBAN INTELLIGENCE LAB  -  2-DAY EVENT SETUP", align="C")
        self.set_xy(self.L, 35)
        self.set_font("Helvetica", "", 6.8)
        self.set_text_color(*self.GRAY)
        self.cell(self.W, 4.5, "Misk, Riyadh  |  27 - 28 September 2026  |  Up to 100 Pax  |  "
                               "Currency: SAR", align="C")
        self.rule(41)
        self.set_y(43.5)

    def _info_column(self, x, y, width, label, lines, align="L"):
        self.set_xy(x, y)
        self.set_font("Helvetica", "B", 7.4)
        self.set_text_color(*self.TEAL)
        self.cell(width, 4.4, label, align=align)
        for i, line in enumerate(lines):
            self.set_xy(x, y + 4.4 + i * 4.0)
            self.set_font("Helvetica", "", 7.4)
            self.set_text_color(*self.DARK)
            self.cell(width, 4.0, line, align=align)

    def add_info_block(self):
        """Two columns: recipient over event details on the left, us on the right."""
        y = self.get_y()
        self._info_column(self.L, y, 92, "TO:", [CLIENT_CONTACT, CLIENT_ORG])
        self._info_column(108, y, 92, "FROM:", ["Miradore Experiences, Riyadh"], align="R")
        self._info_column(108, y + 10, 92, "QUOTATION DATE:", ["15 August 2026"], align="R")
        self._info_column(self.L, y + 15, 130, "EVENT DETAILS:", [
            "Event: Riyadh Urban Intelligence Lab",
            "Venue: Misk - Riyadh, Kingdom of Saudi Arabia",
            "Dates: 27 - 28 September 2026 (2 Days)",
            "Guest Capacity: Up to 100 Pax  |  Catering for 90 Pax",
        ])
        self.set_y(y + 36)

    def table_header(self):
        self.set_fill_color(*self.TEAL)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 6.0)
        self.cell(self.W_LEAD, 5, "", fill=True)
        self.cell(self.W_D1R + self.W_D1T, 5, "DAY 1  (FULL RATE)", align="C", fill=True)
        self.cell(self.W_D2R + self.W_D2T, 5, "DAY 2  (50% DISCOUNT)", align="C", fill=True)
        self.cell(self.W_TOT, 5, "", fill=True)
        self.ln()
        self.cell(self.W_SN, 5.5, "No.", align="C", fill=True)
        self.cell(self.W_DESC, 5.5, "  DESCRIPTION", align="L", fill=True)
        self.cell(self.W_QTY, 5.5, "QTY", align="C", fill=True)
        self.cell(self.W_UNIT, 5.5, "UNIT", align="C", fill=True)
        self.cell(self.W_D1R, 5.5, "UNIT RATE", align="R", fill=True)
        self.cell(self.W_D1T, 5.5, "TOTAL (SAR)", align="R", fill=True)
        self.cell(self.W_D2R, 5.5, "UNIT RATE", align="R", fill=True)
        self.cell(self.W_D2T, 5.5, "TOTAL (SAR)", align="R", fill=True)
        self.cell(self.W_TOT, 5.5, "2-DAY TOTAL", align="R", fill=True)
        self.ln()

    def section_header(self, title):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 6.6)
        self.cell(self.W, 5.6, f"   {title}", fill=True, new_x="LMARGIN", new_y="NEXT")

    def item_row(self, row, alt=False):
        self.set_font("Helvetica", "", self.FS_ROW)
        lines = self.multi_cell(self.W_DESC - 3, self.LINE_H, row["desc"], dry_run=True,
                                output="LINES", align="L")
        h = max(self.ROW_MIN_H, self.LINE_H * len(lines) + 2.0)

        self.set_fill_color(*(self.LIGHT_BG if alt else self.WHITE))
        self.set_text_color(*self.DARK)
        x0, y0 = self.get_x(), self.get_y()

        self.cell(self.W_SN, h, str(row["sn"]), align="C", fill=True)
        xd = self.get_x()
        self.cell(self.W_DESC, h, "", fill=True)
        self.set_xy(xd + 1.5, y0 + (h - self.LINE_H * len(lines)) / 2)
        for ln in lines:
            self.cell(self.W_DESC - 3, self.LINE_H, ln, align="L", new_x="LEFT", new_y="NEXT")
            self.set_x(xd + 1.5)
        self.set_xy(x0 + self.W_SN + self.W_DESC, y0)

        self.cell(self.W_QTY, h, str(row["qty"]), align="C", fill=True)
        self.cell(self.W_UNIT, h, row["unit"], align="C", fill=True)
        self.cell(self.W_D1R, h, money(row["d1_rate"]), align="R", fill=True)
        self.set_font("Helvetica", "B", self.FS_ROW)
        self.cell(self.W_D1T, h, money(row["d1_total"]), align="R", fill=True)

        self.set_font("Helvetica", "", self.FS_ROW)
        if row["discounted"]:
            self.cell(self.W_D2R, h, money(row["d2_rate"]), align="R", fill=True)
        else:
            self.set_text_color(*self.ORANGE)
            self.set_font("Helvetica", "", 5.6)
            self.cell(self.W_D2R, h, "no discount", align="R", fill=True)
            self.set_font("Helvetica", "", self.FS_ROW)
            self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "B", self.FS_ROW)
        self.cell(self.W_D2T, h, money(row["d2_total"]), align="R", fill=True)

        self.set_text_color(*self.TEAL)
        self.cell(self.W_TOT, h, money(row["two_day"]), align="R", fill=True)
        self.set_text_color(*self.DARK)
        self.ln(h)
        self.rule(self.get_y(), 0.1, self.RULE)

    def subtotal_row(self, label, d1, d2, two_day):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 6.6)
        self.cell(self.W_LEAD, 6.2, f"   {label}", fill=True)
        self.cell(self.W_D1R, 6.2, "", fill=True)
        self.cell(self.W_D1T, 6.2, money(d1), align="R", fill=True)
        self.cell(self.W_D2R, 6.2, "", fill=True)
        self.cell(self.W_D2T, 6.2, money(d2), align="R", fill=True)
        self.cell(self.W_TOT, 6.2, money(two_day), align="R", fill=True)
        self.ln()

    def grand_row(self, label, d1, d2, two_day):
        self.set_fill_color(*self.TEAL)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 7.0)
        self.cell(self.W_LEAD, 7.2, f"   {label}", fill=True)
        self.cell(self.W_D1R, 7.2, "", fill=True)
        self.cell(self.W_D1T, 7.2, money(d1), align="R", fill=True)
        self.cell(self.W_D2R, 7.2, "", fill=True)
        self.cell(self.W_D2T, 7.2, money(d2), align="R", fill=True)
        self.set_fill_color(*self.ORANGE)
        self.cell(self.W_TOT, 7.2, money(two_day), align="R", fill=True)
        self.ln()

    def summary_block(self, totals):
        """Full-width right-aligned cost summary."""
        w_amt, w_lbl = 30.0, 50.0
        pad = self.W - w_amt - w_lbl
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(self.W, 5.5, "COST SUMMARY", new_x="LMARGIN", new_y="NEXT")

        for i, (label, amount) in enumerate([("Subtotal before VAT:", totals["net"]),
                                             ("VAT (15%):", totals["vat"])]):
            self.set_fill_color(*self.LIGHT_BG)
            self.set_text_color(*self.DARK)
            self.set_font("Helvetica", "", 7.5)
            self.cell(pad, 5.8, "", fill=(i == 0))
            self.cell(w_lbl, 5.8, label, align="R", fill=(i == 0))
            self.set_font("Helvetica", "B", 7.5)
            self.cell(w_amt, 5.8, money(amount), align="R", fill=(i == 0))
            self.ln()

        self.ln(1.2)
        self.set_fill_color(*self.TEAL)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 9)
        self.cell(pad, 8.5, "", fill=True)
        self.cell(w_lbl, 8.5, "GRAND TOTAL (INC. VAT):", align="R", fill=True)
        self.set_fill_color(*self.ORANGE)
        self.cell(w_amt, 8.5, money(totals["gross"]), align="R", fill=True)
        self.ln()

    def notes_column(self, x, y, width, notes):
        self.set_xy(x, y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(width, 5, "NOTES & ASSUMPTIONS")
        self.set_font("Helvetica", "", 6.0)
        self.set_text_color(*self.GRAY)
        for i, note in enumerate(notes):
            self.set_xy(x, y + 5.5 + i * 3.9)
            self.cell(width, 3.9, f"{i + 1}.  {note}")

    def terms_column(self, x, y, width):
        """Payment terms above the signed-and-stamped execution block."""
        self.set_xy(x, y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(width, 5, "PAYMENT TERMS")
        self.set_xy(x, y + 5.5)
        self.set_font("Helvetica", "", 6.8)
        self.set_text_color(*self.DARK)
        self.cell(width, 4, "80% Advance Payment  -  20% After the Event")

        # wet signature, sitting on the rule
        if os.path.exists(SIGNATURE_FILE):
            self.image(SIGNATURE_FILE, x=x, y=y + 13.5, w=38)

        self.set_draw_color(*self.TEAL)
        self.set_line_width(0.3)
        self.line(x, y + 30, x + 48, y + 30)
        self.set_xy(x, y + 31)
        self.set_font("Helvetica", "B", 7.4)
        self.set_text_color(*self.DARK)
        self.cell(width, 4.2, "ADEEL AHMED  -  DIRECTOR")
        self.set_xy(x, y + 35.2)
        self.set_font("Helvetica", "", 6.4)
        self.set_text_color(*self.GRAY)
        self.cell(width, 3.6, "Miradore Experiences, Riyadh")

        # company stamp, alongside the signature
        if os.path.exists(STAMP_FILE):
            self.image(STAMP_FILE, x=x + 42, y=y + 11, w=37)


NOTES = [
    "All prices are in Saudi Riyals (SAR), quoted in whole riyals. VAT is charged at 15%.",
    "Day 2 is charged at 50% of Day 1 for all equipment except Photography & Videography.",
    "Catering is charged at 210 SAR per person per day for 90 pax, with no Day 2 discount.",
    "Sound is quoted as Option A (Normal Sound System); line array available on request.",
    "Venue hire, power supply and permits at Misk are assumed to be provided by the client.",
    "Any additional scope beyond this BOQ will be quoted separately.",
    "This quotation is valid for 30 days from the date of issue.",
]


def generate_pdf(rows, totals):
    pdf = QuotationPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(QuotationPDF.L, 10, QuotationPDF.L)
    pdf.set_auto_page_break(auto=False)     # the layout is sized to one page
    pdf.add_page()

    pdf.add_logo_header()
    pdf.add_title_block()
    pdf.add_info_block()
    pdf.table_header()

    pdf.section_header("SECTION A: EVENT INFRASTRUCTURE & TECHNICAL PRODUCTION "
                       "(OPTION A - NORMAL SOUND SYSTEM)")
    for i, row in enumerate(rows):
        pdf.item_row(row, alt=(i % 2 == 1))
    pdf.subtotal_row("SUBTOTAL - SECTION A (EQUIPMENT & PRODUCTION)",
                     totals["eq_d1"], totals["eq_d2"], totals["eq_2day"])

    pdf.ln(1.2)
    pdf.section_header("SECTION B: CATERING & HOSPITALITY")
    pdf.item_row(CATERING)
    pdf.subtotal_row("SUBTOTAL - SECTION B (CATERING)",
                     CATERING["d1_total"], CATERING["d2_total"], CATERING["two_day"])

    pdf.ln(1.2)
    pdf.grand_row("TOTAL - SECTIONS A + B (EXCLUSIVE OF VAT)",
                  totals["d1"], totals["d2"], totals["net"])

    pdf.ln(4)
    pdf.summary_block(totals)

    # bottom band: notes alongside payment terms and signature
    y = pdf.get_y() + 5
    pdf.notes_column(pdf.L, y, 105, NOTES)
    pdf.terms_column(120, y, 80)

    bottom = max(y + 5.5 + len(NOTES) * 3.9, y + 39.0)
    assert bottom <= pdf.PAGE_LIMIT, f"layout overflows the page: {bottom:.1f}mm"
    assert pdf.page_no() == 1, f"quotation spilled onto {pdf.page_no()} pages"

    out = os.path.join(BASE_DIR, "Riyadh_Urban_Intelligence_Lab_Quotation.pdf")
    pdf.output(out)
    return out


def generate_csv(rows, totals):
    out = os.path.join(BASE_DIR, "Riyadh_Urban_Intelligence_Lab_Quotation.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        blank = [""] * 9
        w.writerow(blank)
        w.writerow(["", "MIRADORE EXPERIENCES - RIYADH"])
        w.writerow(blank)
        w.writerow(["", "DETAILED BOQ - QUOTATION"])
        w.writerow(["", "RIYADH URBAN INTELLIGENCE LAB - 2-DAY EVENT SETUP"])
        w.writerow(blank)
        w.writerow(["", f"TO: {CLIENT_CONTACT}"])
        w.writerow(["", f"CLIENT: {CLIENT_ORG}"])
        w.writerow(blank)
        w.writerow(["", "EVENT: Riyadh Urban Intelligence Lab"])
        w.writerow(["", "VENUE: Misk - Riyadh, Kingdom of Saudi Arabia"])
        w.writerow(["", "DATES: 27 - 28 September 2026 (2 Days)"])
        w.writerow(["", "CAPACITY: Up to 100 Pax  |  Catering for 90 Pax"])
        w.writerow(["", "QUOTATION DATE: 15 August 2026"])
        w.writerow(["", "FROM: Miradore Experiences - Riyadh"])
        w.writerow(blank)
        w.writerow(["", "", "", "", "DAY 1 (FULL RATE)", "", "DAY 2 (50% DISCOUNT)", "", ""])
        w.writerow(["No.", "DESCRIPTION", "QTY", "UNIT", "UNIT RATE (SAR)", "TOTAL (SAR)",
                    "UNIT RATE (SAR)", "TOTAL (SAR)", "2-DAY TOTAL (SAR)"])
        w.writerow(blank)
        w.writerow(["", "SECTION A: EVENT INFRASTRUCTURE & TECHNICAL PRODUCTION "
                        "(OPTION A - NORMAL SOUND SYSTEM)"])
        for row in rows:
            w.writerow([row["sn"], row["desc"], row["qty"], row["unit"],
                        money(row["d1_rate"]), money(row["d1_total"]),
                        money(row["d2_rate"]) if row["discounted"] else "NO DISCOUNT",
                        money(row["d2_total"]), money(row["two_day"])])
        w.writerow(["", "SUBTOTAL - SECTION A", "", "", "", money(totals["eq_d1"]),
                    "", money(totals["eq_d2"]), money(totals["eq_2day"])])
        w.writerow(blank)
        w.writerow(["", "SECTION B: CATERING & HOSPITALITY"])
        w.writerow([CATERING["sn"], CATERING["desc"], CATERING["qty"], CATERING["unit"],
                    money(CATERING["d1_rate"]), money(CATERING["d1_total"]),
                    "NO DISCOUNT", money(CATERING["d2_total"]), money(CATERING["two_day"])])
        w.writerow(["", "SUBTOTAL - SECTION B", "", "", "", money(CATERING["d1_total"]),
                    "", money(CATERING["d2_total"]), money(CATERING["two_day"])])
        w.writerow(blank)
        w.writerow(["", "TOTAL - SECTIONS A + B (EXCL. VAT)", "", "", "", money(totals["d1"]),
                    "", money(totals["d2"]), money(totals["net"])])
        w.writerow(blank)
        w.writerow(["", "COST SUMMARY"])
        w.writerow(["", "Section A - Equipment & Production", "", "", "", "", "", "",
                    money(totals["eq_2day"])])
        w.writerow(["", "Section B - Catering (90 pax x 2 days)", "", "", "", "", "", "",
                    money(CATERING["two_day"])])
        w.writerow(["", "SUBTOTAL BEFORE VAT", "", "", "", "", "", "", money(totals["net"])])
        w.writerow(["", "VAT (15%)", "", "", "", "", "", "", money(totals["vat"])])
        w.writerow(["", "GRAND TOTAL (INCLUSIVE OF VAT)", "", "", "", "", "", "",
                    money(totals["gross"])])
        w.writerow(blank)
        w.writerow(["", "PAYMENT TERMS"])
        w.writerow(["", "80% Advance Payment - 20% After the Event"])
        w.writerow(blank)
        w.writerow(["", "NOTES"])
        for note in [
            "1. All prices are in Saudi Riyals (SAR), quoted in whole riyals. VAT is 15%.",
            "2. Day 2 is charged at 50% of Day 1 for all equipment except Photography & Videography.",
            "3. Catering is 210 SAR per person per day for 90 pax, with no Day 2 discount.",
            "4. Sound is quoted as Option A (Normal Sound System); line array available on request.",
            "5. Venue hire, power supply and permits at Misk assumed provided by the client.",
            "6. Any additional scope beyond this BOQ will be quoted separately.",
            "7. This quotation is valid for 30 days from the date of issue.",
        ]:
            w.writerow(["", note])
        w.writerow(blank)
        w.writerow(["", "ADEEL AHMED - DIRECTOR"])
        w.writerow(["", "Miradore Experiences, Riyadh"])
    return out


def main():
    rows = build_rows()
    eq_d1 = sum(r["d1_total"] for r in rows)
    eq_d2 = sum(r["d2_total"] for r in rows)
    totals = {
        "eq_d1": eq_d1,
        "eq_d2": eq_d2,
        "eq_2day": eq_d1 + eq_d2,
        "d1": eq_d1 + CATERING["d1_total"],
        "d2": eq_d2 + CATERING["d2_total"],
    }
    totals["net"] = totals["d1"] + totals["d2"]
    totals["vat"] = round(totals["net"] * VAT_RATE)   # to the nearest riyal
    totals["gross"] = totals["net"] + totals["vat"]

    pdf_path = generate_pdf(rows, totals)
    csv_path = generate_csv(rows, totals)

    print(f"Equipment  Day 1: {money(totals['eq_d1'])}   Day 2: {money(totals['eq_d2'])}"
          f"   2-Day: {money(totals['eq_2day'])}")
    print(f"Catering   2-Day: {money(CATERING['two_day'])}")
    print(f"Net (excl VAT):   {money(totals['net'])}")
    print(f"VAT (15%):        {money(totals['vat'])}")
    print(f"GRAND TOTAL:      {money(totals['gross'])}")
    if not os.path.exists(SIGNATURE_FILE):
        print(f"WARNING: no signature at {SIGNATURE_FILE} - document rendered unsigned")
    print(f"PDF: {pdf_path}")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
