"""Riyadh Urban Intelligence Lab - 2-Day Event Quotation (Misk, 27-28 September 2026).

Base BOQ rates supplied by the client, uplifted by 3% and rounded to whole riyals. Day 2 carries a 50%
reduction on all equipment lines except Photography & Videography. Catering
(lunch + coffee break) is charged per person per day with no Day 2 discount.
"""

from fpdf import FPDF
import csv
import os

PAX_CATERING = 90
CATERING_RATE = 210            # SAR per person per day (client supplied, no uplift)
VAT_RATE = 0.15

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    TEAL = (0, 128, 128)
    ORANGE = (230, 100, 30)
    DARK = (40, 40, 40)
    GRAY = (100, 100, 100)
    LIGHT_BG = (245, 248, 250)
    WHITE = (255, 255, 255)
    SECTION_BG = (230, 243, 243)
    NOTE_BG = (252, 244, 236)

    # column widths (landscape A4, 10mm margins -> 277mm usable)
    W_SN, W_DESC, W_QTY, W_UNIT = 10, 97, 14, 20
    W_D1R, W_D1T, W_D2R, W_D2T, W_TOT = 24, 27, 24, 27, 32

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}  |  Miradore Experiences, Riyadh  |  "
                        f"Riyadh Urban Intelligence Lab  |  Confidential", align="C")

    def add_logo_header(self):
        logo = os.path.join(BASE_DIR, "Miradore Logo Color.png")
        if os.path.exists(logo):
            self.image(logo, x=10, y=10, w=52)
        self.set_xy(180, 11)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.DARK)
        self.cell(107, 5, "MIRADORE EXPERIENCES, RIYADH", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(180, 16)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*self.GRAY)
        self.cell(107, 5, "Event Production  |  Branding  |  Technical Delivery",
                  align="R", new_x="LMARGIN", new_y="NEXT")

    def accent_line(self, gap=2):
        self.set_draw_color(*self.TEAL)
        self.set_line_width(0.8)
        self.line(10, self.get_y() + gap, 287, self.get_y() + gap)
        self.ln(gap + 4)

    def add_title_block(self):
        self.set_y(30)
        self.accent_line()
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*self.TEAL)
        self.cell(0, 9, "DETAILED BOQ  -  QUOTATION", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.ORANGE)
        self.cell(0, 6, "RIYADH URBAN INTELLIGENCE LAB  -  2-DAY EVENT SETUP",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.GRAY)
        self.cell(0, 5, "Misk, Riyadh  |  27 - 28 September 2026  |  Up to 100 Pax  |  Currency: SAR",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.accent_line()

    def add_info_block(self):
        y = self.get_y()
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(140, 5, "EVENT DETAILS:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        for line in [
            "Event: Riyadh Urban Intelligence Lab",
            "Venue: Misk - Riyadh, Kingdom of Saudi Arabia",
            "Dates: 27 - 28 September 2026 (2 Days)",
            "Guest Capacity: Up to 100 Pax  |  Catering for 90 Pax",
        ]:
            self.cell(140, 4.6, line, new_x="LMARGIN", new_y="NEXT")

        self.set_xy(180, y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(107, 5, "FROM:", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(180, y + 5)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(107, 4.6, "Miradore Experiences, Riyadh", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(180, y + 12)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(107, 5, "QUOTATION DATE:", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(180, y + 17)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(107, 4.6, "15 August 2026", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_y(y + 24)

    def table_header(self):
        self.set_fill_color(*self.TEAL)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 6.8)
        y = self.get_y()
        # top band: grouped day headers
        self.cell(self.W_SN + self.W_DESC + self.W_QTY + self.W_UNIT, 5.5, "", fill=True)
        self.cell(self.W_D1R + self.W_D1T, 5.5, "DAY 1  (FULL RATE)", align="C", fill=True)
        self.cell(self.W_D2R + self.W_D2T, 5.5, "DAY 2  (50% DISCOUNT)", align="C", fill=True)
        self.cell(self.W_TOT, 5.5, "", fill=True)
        self.ln()
        self.set_font("Helvetica", "B", 6.8)
        self.cell(self.W_SN, 6, "No.", align="C", fill=True)
        self.cell(self.W_DESC, 6, "  DESCRIPTION", align="L", fill=True)
        self.cell(self.W_QTY, 6, "QTY", align="C", fill=True)
        self.cell(self.W_UNIT, 6, "UNIT", align="C", fill=True)
        self.cell(self.W_D1R, 6, "UNIT RATE", align="R", fill=True)
        self.cell(self.W_D1T, 6, "TOTAL (SAR)", align="R", fill=True)
        self.cell(self.W_D2R, 6, "UNIT RATE", align="R", fill=True)
        self.cell(self.W_D2T, 6, "TOTAL (SAR)", align="R", fill=True)
        self.cell(self.W_TOT, 6, "2-DAY TOTAL", align="R", fill=True)
        self.ln()
        # thin separator between the two header rows and the body
        self.set_draw_color(*self.WHITE)
        self.set_line_width(0.2)
        self.line(10 + self.W_SN + self.W_DESC + self.W_QTY + self.W_UNIT, y + 5.5,
                  10 + self.W_SN + self.W_DESC + self.W_QTY + self.W_UNIT, y + 5.5)

    def section_header(self, title):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(277, 6, f"   {title}", fill=True, new_x="LMARGIN", new_y="NEXT")

    def item_row(self, row, alt=False):
        # wrap long descriptions to a fixed 2-line budget
        self.set_font("Helvetica", "", 6.8)
        lines = self.multi_cell(self.W_DESC - 3, 3.4, row["desc"], dry_run=True,
                                output="LINES", align="L")
        h = max(6.5, 3.4 * len(lines) + 2.2)

        self.set_fill_color(*(self.LIGHT_BG if alt else self.WHITE))
        self.set_text_color(*self.DARK)
        x0, y0 = self.get_x(), self.get_y()

        self.cell(self.W_SN, h, str(row["sn"]), align="C", fill=True)
        # description drawn as a wrapped block inside its own cell box
        xd = self.get_x()
        self.cell(self.W_DESC, h, "", fill=True)
        self.set_xy(xd + 1.5, y0 + (h - 3.4 * len(lines)) / 2)
        self.set_font("Helvetica", "", 6.8)
        for ln in lines:
            self.cell(self.W_DESC - 3, 3.4, ln, align="L", new_x="LEFT", new_y="NEXT")
            self.set_x(xd + 1.5)
        self.set_xy(x0 + self.W_SN + self.W_DESC, y0)

        self.set_font("Helvetica", "", 6.8)
        self.cell(self.W_QTY, h, str(row["qty"]), align="C", fill=True)
        self.cell(self.W_UNIT, h, row["unit"], align="C", fill=True)
        self.cell(self.W_D1R, h, money(row["d1_rate"]), align="R", fill=True)
        self.set_font("Helvetica", "B", 6.8)
        self.cell(self.W_D1T, h, money(row["d1_total"]), align="R", fill=True)

        self.set_font("Helvetica", "", 6.8)
        if row["discounted"]:
            self.cell(self.W_D2R, h, money(row["d2_rate"]), align="R", fill=True)
        else:
            self.set_text_color(*self.ORANGE)
            self.cell(self.W_D2R, h, "no discount", align="R", fill=True)
            self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "B", 6.8)
        self.cell(self.W_D2T, h, money(row["d2_total"]), align="R", fill=True)

        self.set_text_color(*self.TEAL)
        self.cell(self.W_TOT, h, money(row["two_day"]), align="R", fill=True)
        self.set_text_color(*self.DARK)
        self.ln(h)

        self.set_draw_color(225, 232, 235)
        self.set_line_width(0.1)
        self.line(10, self.get_y(), 287, self.get_y())

    def subtotal_row(self, label, d1, d2, two_day):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 7.2)
        self.cell(self.W_SN + self.W_DESC + self.W_QTY + self.W_UNIT, 6.5, f"   {label}", fill=True)
        self.cell(self.W_D1R, 6.5, "", fill=True)
        self.cell(self.W_D1T, 6.5, money(d1), align="R", fill=True)
        self.cell(self.W_D2R, 6.5, "", fill=True)
        self.cell(self.W_D2T, 6.5, money(d2), align="R", fill=True)
        self.cell(self.W_TOT, 6.5, money(two_day), align="R", fill=True)
        self.ln()

    def grand_row(self, label, d1, d2, two_day):
        self.set_fill_color(*self.TEAL)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 8.5)
        self.cell(self.W_SN + self.W_DESC + self.W_QTY + self.W_UNIT, 8, f"   {label}", fill=True)
        self.cell(self.W_D1R, 8, "", fill=True)
        self.cell(self.W_D1T, 8, money(d1), align="R", fill=True)
        self.cell(self.W_D2R, 8, "", fill=True)
        self.cell(self.W_D2T, 8, money(d2), align="R", fill=True)
        self.set_fill_color(*self.ORANGE)
        self.cell(self.W_TOT, 8, money(two_day), align="R", fill=True)
        self.ln()

    def summary_line(self, label, amount, bold=False, highlight=False):
        left = 277 - 72
        if highlight:
            self.set_fill_color(*self.TEAL)
            self.set_text_color(*self.WHITE)
            self.set_font("Helvetica", "B", 10)
            self.cell(left, 9, "", fill=True)
            self.cell(40, 9, label, align="R", fill=True)
            self.cell(32, 9, money(amount), align="R", fill=True)
        else:
            self.set_fill_color(*(self.LIGHT_BG if bold else self.WHITE))
            self.set_text_color(*self.DARK)
            self.set_font("Helvetica", "B" if bold else "", 8)
            self.cell(left, 6.5, "", fill=bold)
            self.cell(40, 6.5, label, align="R", fill=bold)
            self.set_font("Helvetica", "B", 8)
            self.cell(32, 6.5, money(amount), align="R", fill=bold)
        self.ln()


def generate_pdf(rows, totals):
    pdf = QuotationPDF(orientation="L", unit="mm", format="A4")
    pdf.set_margins(10, 10, 10)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    pdf.add_logo_header()
    pdf.add_title_block()
    pdf.add_info_block()
    pdf.table_header()

    pdf.section_header("SECTION A: EVENT INFRASTRUCTURE & TECHNICAL PRODUCTION  "
                       "(OPTION A - NORMAL SOUND SYSTEM)")
    for i, row in enumerate(rows):
        pdf.item_row(row, alt=(i % 2 == 1))
    pdf.subtotal_row("SUBTOTAL - SECTION A (EQUIPMENT & PRODUCTION)",
                     totals["eq_d1"], totals["eq_d2"], totals["eq_2day"])

    # Keep Section B + the grand total together; repeat the column header if it moves
    if pdf.get_y() > 150:
        pdf.add_page()
        pdf.table_header()
    pdf.ln(1.5)
    pdf.section_header("SECTION B: CATERING & HOSPITALITY")
    pdf.item_row(CATERING)
    pdf.subtotal_row("SUBTOTAL - SECTION B (CATERING)",
                     CATERING["d1_total"], CATERING["d2_total"], CATERING["two_day"])

    pdf.ln(1.5)
    pdf.grand_row("TOTAL - SECTIONS A + B (EXCLUSIVE OF VAT)",
                  totals["d1"], totals["d2"], totals["net"])

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 6, "COST SUMMARY", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.summary_line("Section A - Equipment & Production:", totals["eq_2day"])
    pdf.summary_line("Section B - Catering (90 pax x 2 days):", CATERING["two_day"])
    pdf.summary_line("Subtotal before VAT:", totals["net"], bold=True)
    pdf.summary_line("VAT (15%):", totals["vat"])
    pdf.ln(1)
    pdf.summary_line("GRAND TOTAL (INC. VAT):", totals["gross"], highlight=True)

    pdf.ln(6)
    y = pdf.get_y()
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(150, 6, "NOTES & ASSUMPTIONS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    for note in [
        "1.  All prices are in Saudi Riyals (SAR) and are quoted in whole riyals. VAT is 15%.",
        "2.  Day 2 is charged at 50% of Day 1 for all equipment except Photography & Videography.",
        "3.  Catering is charged at 210 SAR per person per day for 90 pax and carries no Day 2",
        "     discount, as it is consumed in full on both days.",
        "4.  Sound is quoted as Option A (Normal Sound System). A line array system can be quoted",
        "     as an alternative on request.",
        "5.  Venue hire, power supply and permits at Misk are assumed to be provided by the client.",
        "6.  Any additional scope beyond this BOQ will be quoted separately.",
        "7.  This quotation is valid for 30 days from the date of issue.",
    ]:
        pdf.cell(150, 4, note, new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(175, y)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(112, 6, "PAYMENT TERMS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(175, y + 6)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(112, 5, "80% Advance Payment  -  20% After the Event", new_x="LMARGIN", new_y="NEXT")

    pdf.set_xy(175, y + 20)
    pdf.set_draw_color(*pdf.TEAL)
    pdf.set_line_width(0.3)
    pdf.line(175, pdf.get_y(), 240, pdf.get_y())
    pdf.set_xy(175, y + 22)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(112, 5, "ADEEL AHMED  -  DIRECTOR", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(175, y + 27)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    pdf.cell(112, 4, "Miradore Experiences, Riyadh", new_x="LMARGIN", new_y="NEXT")

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
    print(f"PDF: {pdf_path}")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
