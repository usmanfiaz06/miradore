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
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Miradore Marketing Management L.L.C  |  Confidential", align="C")

    def add_logo_header(self):
        logo_path = os.path.join(os.path.dirname(__file__), "Miradore Logo Color.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=12, w=55)
        self.set_xy(120, 12)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.DARK)
        self.cell(75, 5, "MIRADORE MARKETING MANAGEMENT L.L.C", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_x(120)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*self.GRAY)
        self.cell(75, 4, "License No: 1160569", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_x(120)
        self.cell(75, 4, "VAT #: 104140200700003", align="R", new_x="LMARGIN", new_y="NEXT")

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
        self.cell(0, 7, "PAKISTAN NIGHT  -  LEAP 2026", align="C", new_x="LMARGIN", new_y="NEXT")
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
            "Venue: Crowne Plaza Hotel (or similar) - Riyadh",
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
        self.cell(75, 5, "Miradore Marketing Management L.L.C", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(120, right_y + 15)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(75, 5, "QUOTATION DATE:", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(120, right_y + 20)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(75, 5, "03 March 2026", align="R", new_x="LMARGIN", new_y="NEXT")
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
        self.cell(30, 6, f"{rate:,}" if rate else "-", border=0, align="R", fill=True)
        self.set_font("Helvetica", "B", 7)
        self.cell(35, 6, f"{amount_sar:,}" if amount_sar else "-", border=0, align="R", fill=True)
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

    # Section A
    pdf.section_header("SECTION A: VENUE & HOSPITALITY")
    pdf.item_row(1, "Hotel Ballroom (Dinner for 400 Guests, VIP Seating for 50)", 1, 1, 325000, 325000)
    pdf.ln(2)

    # Section B
    pdf.section_header("SECTION B: VENUE BRANDING & SETUP")
    pdf.item_row(2, "Welcome Backdrop (8ft x 8ft, Flex + Frame) with Podium", 1, 1, 16500, 16500)
    pdf.item_row(3, "SMD/LED Screen - Main (10ft x 30ft)", 1, 1, 33000, 33000, alt=True)
    pdf.item_row(4, "02 Media Walls (10ft x 20ft, Flex + Frame)", 2, 1, 5500, 11000)
    pdf.item_row(5, "06 Commercial Branding Panels (10ft x 10ft, Flex + Frame)", 6, 1, 2500, 15000, alt=True)
    pdf.item_row(6, "06 Digital Standees", 6, 1, 1500, 9000)
    pdf.item_row(7, "Reception Counter with Branded Fascia", 1, 1, 11000, 11000, alt=True)
    pdf.item_row(8, "Table Branding, Name Plates & VIP Delegate Collateral", 1, 1, 8000, 8000)
    pdf.subtotal_row("Subtotal:", 103500)

    # Section C
    pdf.section_header("SECTION C: TECHNICAL & AUDIO-VISUAL")
    pdf.item_row(9, "Sound System & 2 Wireless Mics - On-premise (upgrade on-demand)", 1, 1, 0, 0)
    pdf.item_row(10, "Ambiance Lighting Design & Setup", 1, 1, 18500, 18500, alt=True)
    pdf.item_row(11, "Content Design & Development (Digital, Print & Social)", 1, 1, 15000, 15000)
    pdf.subtotal_row("Subtotal:", 33500)

    # Section D
    pdf.section_header("SECTION D: EVENT SERVICES & PERSONNEL")
    pdf.item_row(12, "Cultural Night Performance (All Provinces incl. AJK & GB)", 1, 1, 35000, 35000)
    pdf.item_row(13, "Professional Ushers / Hostesses (Bilingual)", 4, 1, 1750, 7000, alt=True)
    pdf.item_row(14, "Professional MC / Host (Bilingual - English & Arabic)", 1, 1, 12000, 12000)
    pdf.item_row(15, "Event Photography (6pm - 11pm)", 1, 1, 4500, 4500, alt=True)
    pdf.item_row(16, "Event Videography (Highlight Video, Reels & Interviews)", 1, 1, 6000, 6000)
    pdf.subtotal_row("Subtotal:", 64500)

    # Section E
    pdf.section_header("SECTION E: LOGISTICS & COORDINATION")
    pdf.item_row(17, "Logistics, Labor & Transportation", 1, 1, 39000, 39000)
    pdf.item_row(18, "Dedicated Liaison (PSEB & Embassy Coordination)", 1, 1, 8000, 8000, alt=True)
    pdf.item_row(19, "Miscellaneous & Contingency", 1, 1, 5000, 5000)
    pdf.subtotal_row("Subtotal:", 52000)

    pdf.ln(4)

    # Cost Summary
    pdf.set_draw_color(*pdf.TEAL)
    pdf.set_line_width(0.5)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 7, "COST SUMMARY", new_x="LMARGIN", new_y="NEXT")

    pdf.summary_row("Venue & Hospitality:", 325000, bold=True)
    pdf.summary_row("Production Services (B-E):", 253500, bold=True)
    pdf.summary_row("Agency Commission (15%):", 38025)
    pdf.ln(1)
    pdf.summary_row("Subtotal before VAT:", 616525, bold=True)
    pdf.summary_row("VAT (15%):", 92478.75)
    pdf.ln(1)
    pdf.summary_row("*  GRAND TOTAL (INC. VAT):", 709003.75, highlight=True)

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
        "2.  Venue includes dinner for 400 guests with dedicated VIP seating for 50.",
        "3.  Sound system & wireless mics available on-premise at venue; premium upgrade on-demand.",
        "4.  Seating arrangements as per Embassy/PSEB guidelines.",
        "5.  PSEB reserves the right to adjust quantities as per final requirements.",
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
    pdf.cell(0, 4, "Miradore Marketing Management L.L.C", new_x="LMARGIN", new_y="NEXT")

    out_path = os.path.join(os.path.dirname(__file__), "Pakistan_Saudi_Business_Forum_LEAP2026_Quotation.pdf")
    pdf.output(out_path)
    print(f"PDF generated: {out_path}")


if __name__ == "__main__":
    generate()
