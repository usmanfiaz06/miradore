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
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.ORANGE)
        self.cell(0, 7, "PAKISTAN NIGHT  -  LEAP 2026  (VERSION 2)", align="C", new_x="LMARGIN", new_y="NEXT")
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
        self.cell(90, 5, "Client: Pakistan Software Export Board (PSEB)", new_x="LMARGIN", new_y="NEXT")
        self.cell(90, 5, "Ministry of IT & Telecommunication", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "EVENT DETAILS:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        info_items = [
            "Event: Pakistan Night - Welcome Networking Evening",
            "Venue: Crowne Plaza Hotel - Riyadh (Ballroom)",
            "Hospitality: Buffet Dinner + Coffee Break",
            "Date: April 14, 2026 (7:00 PM - 11:00 PM)",
            "Context: LEAP 2026 - Riyadh, Saudi Arabia",
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
        self.cell(75, 5, "09 March 2026", align="R", new_x="LMARGIN", new_y="NEXT")
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
        """Sub-detail row for item breakdowns."""
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
        # thin line
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

    # Section A: Venue & Hospitality
    pdf.section_header("SECTION A: VENUE & HOSPITALITY")
    pdf.item_row(1, "Hotel Crowne Plaza Ballroom (Buffet Dinner + Coffee Break, 400 Guests)", 1, 1, 325000, 325000)
    pdf.item_row(2, "VIP Sofas (50 Pieces @ 350 SAR each)", 50, 1, 350, 17500, alt=True)
    pdf.subtotal_row("Subtotal:", 342500)

    # Section B: Stage & Screens
    pdf.section_header("SECTION B: STAGE & SCREENS")
    pdf.item_row(3, "Stage Screen Setup (Complete Package)", 1, 1, 31300, 31300)
    pdf.detail_row("- Center Screen: 10m x 4m")
    pdf.detail_row("- 2 Side Panel Screens: 2 x (3m x 4m)")
    pdf.detail_row("- Servers")
    pdf.subtotal_row("Subtotal:", 31300)

    # Section C: Venue Branding & Setup
    pdf.section_header("SECTION C: VENUE BRANDING & SETUP")
    pdf.item_row(4, "Reception Counter with Branded Fascia", 1, 1, 13500, 13500)
    pdf.item_row(5, "Media Walls with Front Carpet (4.8m x 2.4m)", 2, 1, 7500, 15000, alt=True)
    pdf.item_row(6, "Cocktail Tables - Coffee Break Area", 10, 1, 200, 2000)
    pdf.item_row(7, "Digital Standees", 6, 1, 1350, 8100, alt=True)
    pdf.item_row(8, "Hall Branding - 4 Side Panels (Flex, 2 each side)", 4, 1, 3750, 15000)
    pdf.subtotal_row("Subtotal:", 53600)

    # Section D: Technical & Audio-Visual
    pdf.section_header("SECTION D: TECHNICAL & AUDIO-VISUAL")
    pdf.item_row(9, "Ambiance Lighting (On-premise)", 1, 1, "On-premise", "On-premise")
    pdf.item_row(10, "Sound System & 2 Wireless Mics (On-premise)", 1, 1, "On-premise", "On-premise", alt=True)
    pdf.item_row(11, "Content Design (Digital, Print & Social)", 1, 1, 12000, 12000)
    pdf.subtotal_row("Subtotal:", 12000)

    # Section E: Event Services & Personnel
    pdf.section_header("SECTION E: EVENT SERVICES & PERSONNEL")
    pdf.item_row(12, "Media Coverage (Photography 6pm-11pm + Videography)", 1, 1, 11500, 11500)
    pdf.item_row(13, "Professional Ushers / Hostesses (Bilingual)", 3, 1, 1500, 4500, alt=True)
    pdf.item_row(14, "Cultural Night Performance (All Provinces incl. AJK & GB)", 1, 1, 45000, 45000)
    pdf.subtotal_row("Subtotal:", 61000)

    # Section F: Miscellaneous
    pdf.section_header("SECTION F: MISCELLANEOUS")
    pdf.item_row(15, "Miscellaneous & Contingency", 1, 1, 5000, 5000)
    pdf.subtotal_row("Subtotal:", 5000)

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
    venue_hospitality = 342500
    production_services = 31300 + 53600 + 12000 + 61000 + 5000  # 162,900
    agency_commission = production_services * 0.15  # 24,435
    subtotal_before_vat = venue_hospitality + production_services + agency_commission  # 529,835
    vat = subtotal_before_vat * 0.15  # 79,475.25
    grand_total = subtotal_before_vat + vat  # 609,310.25

    pdf.summary_row("Venue & Hospitality:", venue_hospitality, bold=True)
    pdf.summary_row("Production Services (B-F):", production_services, bold=True)
    pdf.summary_row("Agency Commission (15%):", agency_commission)
    pdf.ln(1)
    pdf.summary_row("Subtotal before VAT:", subtotal_before_vat, bold=True)
    pdf.summary_row("VAT (15%):", vat)
    pdf.ln(1)
    pdf.summary_row("*  GRAND TOTAL (INC. VAT):", grand_total, highlight=True)

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
        "2.  Venue includes buffet dinner + coffee break for 400 guests at Crowne Plaza Ballroom.",
        "3.  VIP sofas (50 pcs) quoted separately at 350 SAR per piece.",
        "4.  Sound system, wireless mics & ambiance lighting are on-premise at the hotel venue.",
        "5.  Stage screen includes center screen (10m x 4m), 2 side panels (3m x 4m each), and servers.",
        "6.  Seating arrangements as per Embassy/PSEB guidelines.",
        "7.  Any additional requirements beyond this scope will be quoted separately.",
        "8.  This quotation is valid for 30 days from the date of issue.",
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

    out_path = os.path.join(os.path.dirname(__file__), "Riyadh_Digital_City_Event_V2_Quotation.pdf")
    pdf.output(out_path)
    print(f"PDF generated: {out_path}")


if __name__ == "__main__":
    generate()
