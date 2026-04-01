from fpdf import FPDF
import os


class QuotationPDF(FPDF):
    TEAL = (0, 128, 128)
    ORANGE = (230, 100, 30)
    DARK = (40, 40, 40)
    GRAY = (100, 100, 100)
    LIGHT_BG = (245, 248, 250)
    WHITE = (255, 255, 255)
    HEADER_BG = (0, 128, 128)
    SECTION_BG = (230, 243, 243)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Miradore Experiences, Riyadh  |  Confidential", align="C")

    def add_logo_header(self):
        logo_path = os.path.join(os.path.dirname(__file__), "Miradore Logo Color.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=12, w=55)
        self.set_xy(120, 12)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.DARK)
        self.cell(75, 5, "MIRADORE EXPERIENCES, RIYADH", align="R", new_x="LMARGIN", new_y="NEXT")

    def draw_accent_line(self):
        self.set_draw_color(*self.TEAL)
        self.set_line_width(0.8)
        self.line(15, self.get_y() + 2, 195, self.get_y() + 2)
        self.ln(6)

    def add_title_block(self):
        self.set_y(35)
        self.draw_accent_line()
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*self.TEAL)
        self.cell(0, 10, "QUOTATION", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.ORANGE)
        self.cell(0, 7, "GUINNESS WORLD RECORD CEREMONY  -  CLOCK TOWER MUSEUM", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.GRAY)
        self.cell(0, 5, "REVISED SCOPE", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.draw_accent_line()

    def add_info_block(self):
        y = self.get_y()
        # Left - TO
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "TO:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(90, 5, "Client: Clock Tower Museum", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "EVENT DETAILS:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        info_items = [
            "Event: Guinness World Record Award Ceremony",
            "Venue: Clock Tower Museum - Makkah",
            "Zones: Crystal Hall & Balcony",
        ]
        for item in info_items:
            self.cell(90, 5, item, new_x="LMARGIN", new_y="NEXT")

        # Right - FROM
        right_y = y
        self.set_xy(120, right_y)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(75, 5, "FROM:", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(120, right_y + 5)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(75, 5, "Miradore Experiences, Riyadh", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(120, right_y + 15)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(75, 5, "QUOTATION DATE:", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(120, right_y + 20)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(75, 5, "01 April 2026", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)

    def table_header(self):
        self.set_fill_color(*self.HEADER_BG)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 7)
        self.cell(10, 7, "S#", border=0, align="C", fill=True)
        self.cell(82, 7, "DESCRIPTION", border=0, align="L", fill=True)
        self.cell(14, 7, "QTY", border=0, align="C", fill=True)
        self.cell(14, 7, "DAYS", border=0, align="C", fill=True)
        self.cell(30, 7, "RATE (SAR)", border=0, align="R", fill=True)
        self.cell(35, 7, "AMOUNT (SAR)", border=0, align="R", fill=True)
        self.ln()

    def section_header(self, title):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(185, 6, f"  {title}", border=0, fill=True, new_x="LMARGIN", new_y="NEXT")

    def item_row(self, sn, desc, qty, days, rate, amount_sar, alt=False):
        if alt:
            self.set_fill_color(*self.LIGHT_BG)
        else:
            self.set_fill_color(*self.WHITE)
        self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "", 7)
        self.cell(10, 6, str(sn), border=0, align="C", fill=True)
        self.cell(82, 6, desc, border=0, align="L", fill=True)
        self.cell(14, 6, str(qty), border=0, align="C", fill=True)
        self.cell(14, 6, str(days), border=0, align="C", fill=True)
        self.set_font("Helvetica", "", 7)
        rate_text = rate if isinstance(rate, str) else (f"{rate:,}" if rate else "-")
        self.cell(30, 6, rate_text, border=0, align="R", fill=True)
        self.set_font("Helvetica", "B", 7)
        amt_text = amount_sar if isinstance(amount_sar, str) else (f"{amount_sar:,}" if amount_sar else "-")
        self.cell(35, 6, amt_text, border=0, align="R", fill=True)
        self.ln()

    def detail_row(self, text):
        self.set_fill_color(*self.WHITE)
        self.set_text_color(*self.GRAY)
        self.set_font("Helvetica", "I", 6.5)
        self.cell(10, 5, "", border=0, fill=True)
        self.cell(82, 5, f"   {text}", border=0, align="L", fill=True)
        self.cell(14, 5, "", border=0, fill=True)
        self.cell(14, 5, "", border=0, fill=True)
        self.cell(30, 5, "", border=0, fill=True)
        self.cell(35, 5, "", border=0, fill=True)
        self.ln()

    def subtotal_row(self, label, amount_sar):
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*self.TEAL)
        self.cell(120, 6, "", border=0)
        self.cell(30, 6, label, border=0, align="R")
        self.cell(35, 6, f"{amount_sar:,}", border=0, align="R")
        self.ln()
        self.set_draw_color(*self.TEAL)
        self.set_line_width(0.2)
        self.line(150, self.get_y(), 195, self.get_y())
        self.ln(1)

    def summary_row(self, label, amount_sar, bold=False, highlight=False):
        if highlight:
            self.set_fill_color(*self.TEAL)
            self.set_text_color(*self.WHITE)
            self.set_font("Helvetica", "B", 8.5)
            self.cell(120, 8, "", border=0, fill=True)
            self.cell(30, 8, label, border=0, align="R", fill=True)
            self.cell(35, 8, f"{amount_sar:,.2f}" if isinstance(amount_sar, float) else f"{amount_sar:,}", border=0, align="R", fill=True)
        else:
            self.set_fill_color(*self.LIGHT_BG if bold else self.WHITE)
            self.set_text_color(*self.DARK)
            self.set_font("Helvetica", "B" if bold else "", 7.5)
            self.cell(120, 7, "", border=0, fill=bold)
            self.cell(30, 7, label, border=0, align="R", fill=bold)
            self.set_font("Helvetica", "B", 7.5)
            self.cell(35, 7, f"{amount_sar:,.2f}" if isinstance(amount_sar, float) else f"{amount_sar:,}", border=0, align="R", fill=bold)
        self.ln()


def generate():
    pdf = QuotationPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Header
    pdf.add_logo_header()
    pdf.add_title_block()
    pdf.add_info_block()

    # Table
    pdf.table_header()

    # Section A: Branding & Display
    pdf.section_header("SECTION A: BRANDING & DISPLAY")
    pdf.item_row(1, "Lama Stands - Printed Display Stands (Hall & Balcony)", 5, 1, 550, 2750)
    pdf.detail_row("- For reception & introduction areas")
    pdf.subtotal_row("Subtotal:", 2750)

    # Section B: Stage & Screens
    pdf.section_header("SECTION B: STAGE & SCREENS")
    pdf.item_row(2, "LED Screen - Hall Center (10m x 4m = 40 sqm)", 40, 1, 420, 16800)
    pdf.detail_row("- Rate per square meter: 420 SAR")
    pdf.subtotal_row("Subtotal:", 16800)

    # Section C: Hospitality
    pdf.section_header("SECTION C: HOSPITALITY")
    pdf.item_row(3, "Saudi Hospitality - Inside the Hall", 1, 1, 9000, 9000)
    pdf.item_row(4, "Saudi Hospitality - Balcony", 1, 1, 9000, 9000, alt=True)
    pdf.subtotal_row("Subtotal:", 18000)

    # Section D: Event Services & Personnel
    pdf.section_header("SECTION D: EVENT SERVICES & PERSONNEL")
    pdf.item_row(5, "Event MC / Host", 1, 1, 10000, 10000)
    pdf.item_row(6, "Media Coverage - Photography & Videography", 1, 1, 6500, 6500, alt=True)
    pdf.item_row(7, "Event Organizers / Coordinators", 3, 1, 1200, 3600)
    pdf.subtotal_row("Subtotal:", 20100)

    pdf.ln(4)

    # Cost Summary
    pdf.set_draw_color(*pdf.TEAL)
    pdf.set_line_width(0.5)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 7, "COST SUMMARY", new_x="LMARGIN", new_y="NEXT")

    # Calculations
    services_total = 2750 + 16800 + 18000 + 20100  # 57,650
    agency_commission = services_total * 0.07  # 4,035.50
    subtotal_before_vat = services_total + agency_commission  # 65,607.50
    vat = subtotal_before_vat * 0.15  # 9,841.125
    grand_total = subtotal_before_vat + vat  # 75,448.625

    pdf.summary_row("Services Total (A-D):", services_total, bold=True)
    pdf.summary_row("Agency Commission (7%):", agency_commission)
    pdf.ln(1)
    pdf.summary_row("Subtotal before VAT:", subtotal_before_vat, bold=True)
    pdf.summary_row("VAT (15%):", round(vat, 2))
    pdf.ln(1)
    pdf.summary_row("*  GRAND TOTAL (INC. VAT):", round(grand_total, 2), highlight=True)

    pdf.ln(6)

    # Payment Terms
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 6, "PAYMENT TERMS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(0, 5, "80% Advance Payment  -  20% After the Event", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)

    # Notes
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 6, "NOTES", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    notes = [
        "1.  All prices are in Saudi Riyals (SAR).",
        "2.  Lama stands are printed physical display stands for reception and introduction areas.",
        "3.  LED screen priced at 420 SAR per sqm (10m x 4m = 40 sqm center screen).",
        "4.  Saudi hospitality quoted separately for the hall and balcony areas.",
        "5.  Media coverage includes both photography and videography.",
        "6.  Any additional requirements beyond this scope will be quoted separately.",
        "7.  This quotation is valid for 30 days from the date of issue.",
    ]
    for note in notes:
        pdf.cell(0, 4.5, note, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)

    # Signature
    pdf.set_draw_color(*pdf.TEAL)
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y(), 80, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(0, 5, "ADEEL AHMED - DIRECTOR", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    pdf.cell(0, 4, "Miradore Experiences, Riyadh", new_x="LMARGIN", new_y="NEXT")

    out_path = os.path.join(os.path.dirname(__file__), "Clock_Tower_Guinness_Ceremony_Quotation.pdf")
    pdf.output(out_path)
    print(f"PDF generated: {out_path}")


if __name__ == "__main__":
    generate()
