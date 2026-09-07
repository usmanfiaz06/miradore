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
        self.set_y(31)
        self.draw_accent_line()
        self.set_font("Helvetica", "B", 17)
        self.set_text_color(*self.TEAL)
        self.cell(0, 9, "QUOTATION", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.ORANGE)
        self.cell(0, 6, "EVENT SIGNAGE - INSTALLATION SERVICES", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4.5, "DIRECTIONAL & WELCOME SIGNAGE BOARDS  -  INSTALLATION ONLY", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.draw_accent_line()

    def add_info_block(self):
        y = self.get_y()
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "TO:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(90, 5, "Client: [Client Name]", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "SCOPE DETAILS:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        for item in [
            "Scope: Installation of directional & welcome signage",
            "Venue: Event Venue - Riyadh, KSA",
            "Boards: 11 nos.  |  Total Area: 106 sqm",
        ]:
            self.cell(90, 5, item, new_x="LMARGIN", new_y="NEXT")
        left_end = self.get_y()

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
        self.cell(75, 5, "07 September 2026", align="R", new_x="LMARGIN", new_y="NEXT")
        # both columns are drawn independently - continue below the taller one
        self.set_y(max(left_end, self.get_y()))
        self.ln(1)

    def table_header(self):
        self.set_fill_color(*self.HEADER_BG)
        self.set_text_color(*self.WHITE)
        self.set_font("Helvetica", "B", 7)
        self.cell(10, 7, "S#", border=0, align="C", fill=True)
        self.cell(82, 7, "DESCRIPTION", border=0, align="L", fill=True)
        self.cell(14, 7, "QTY", border=0, align="C", fill=True)
        self.cell(14, 7, "SQM", border=0, align="C", fill=True)
        self.cell(30, 7, "RATE (SAR/SQM)", border=0, align="R", fill=True)
        self.cell(35, 7, "AMOUNT (SAR)", border=0, align="R", fill=True)
        self.ln()

    def section_header(self, title):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(185, 6, f"  {title}", border=0, fill=True, new_x="LMARGIN", new_y="NEXT")

    def item_row(self, sn, desc, qty, sqm, rate, amount_sar, alt=False):
        self.set_fill_color(*(self.LIGHT_BG if alt else self.WHITE))
        self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "", 7)
        self.cell(10, 6, str(sn), border=0, align="C", fill=True)
        self.cell(82, 6, desc, border=0, align="L", fill=True)
        self.cell(14, 6, str(qty), border=0, align="C", fill=True)
        self.cell(14, 6, str(sqm), border=0, align="C", fill=True)
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
        self.cell(89, 5, "", border=0, fill=True)
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

    def add_signature_block(self):
        """Signature above the line with the company stamp alongside - same
        layout as the signed Miradore invoices."""
        base_dir = os.path.dirname(__file__)
        sig_path = os.path.join(base_dir, "adeel_signature-removebg-preview.png")
        stamp_path = os.path.join(base_dir, "Miradore_Stamp_Riyadh.png")

        top = self.get_y()
        if os.path.exists(sig_path):
            self.image(sig_path, x=18, y=top, w=38)
        if os.path.exists(stamp_path):
            self.image(stamp_path, x=68, y=top - 2, w=38)

        line_y = top + 15
        self.set_draw_color(*self.TEAL)
        self.set_line_width(0.3)
        self.line(15, line_y, 80, line_y)

        self.set_xy(15, line_y + 1)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.DARK)
        self.cell(0, 5, "ADEEL AHMED - DIRECTOR", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, "Miradore Experiences, Riyadh", new_x="LMARGIN", new_y="NEXT")

    def summary_row(self, label, amount_sar, bold=False, highlight=False):
        if highlight:
            self.set_fill_color(*self.TEAL)
            self.set_text_color(*self.WHITE)
            self.set_font("Helvetica", "B", 8.5)
            self.cell(120, 7.5, "", border=0, fill=True)
            self.cell(30, 7.5, label, border=0, align="R", fill=True)
            self.cell(35, 7.5, f"{amount_sar:,.2f}" if isinstance(amount_sar, float) else f"{amount_sar:,}", border=0, align="R", fill=True)
        else:
            self.set_fill_color(*(self.LIGHT_BG if bold else self.WHITE))
            self.set_text_color(*self.DARK)
            self.set_font("Helvetica", "B" if bold else "", 7.5)
            self.cell(120, 6, "", border=0, fill=bold)
            self.cell(30, 6, label, border=0, align="R", fill=bold)
            self.set_font("Helvetica", "B", 7.5)
            self.cell(35, 6, f"{amount_sar:,.2f}" if isinstance(amount_sar, float) else f"{amount_sar:,}", border=0, align="R", fill=bold)
        self.ln()


RATE = 80  # SAR per sqm - installation


def generate():
    pdf = QuotationPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_logo_header()
    pdf.add_title_block()
    pdf.add_info_block()

    pdf.table_header()

    pdf.section_header("SECTION A: SIGNAGE INSTALLATION (INSTALLATION ONLY - BANNERS & FRAMES SUPPLIED BY CLIENT)")

    a1 = 3 * 10 * RATE   # 2,400
    a2 = 7 * 8 * RATE    # 4,480
    a3 = 1 * 20 * RATE   # 1,600

    pdf.item_row(1, "Directional & Welcome Board - 2m x 5m (10 sqm ea., base 50 cm)", 3, 30, RATE, a1)
    pdf.item_row(2, "Directional & Welcome Board - 2m x 4m (8 sqm ea., base 50 cm)", 7, 56, RATE, a2, alt=True)
    pdf.item_row(3, "Directional & Welcome Board - 2m x 10m (20 sqm, base 50 cm)", 1, 20, RATE, a3)

    installation_total = a1 + a2 + a3  # 8,480
    pdf.subtotal_row("Subtotal:", installation_total)

    pdf.ln(2)

    pdf.set_draw_color(*pdf.TEAL)
    pdf.set_line_width(0.5)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 6, "COST SUMMARY", new_x="LMARGIN", new_y="NEXT")

    # All figures rounded to the nearest Saudi Riyal
    agency_commission = round(installation_total * 0.12)          # 1,018
    subtotal_before_vat = installation_total + agency_commission  # 9,498
    vat = round(subtotal_before_vat * 0.15)                       # 1,425
    grand_total = subtotal_before_vat + vat                       # 10,923

    pdf.summary_row("Installation Total (106 sqm @ 80 SAR):", installation_total, bold=True)
    pdf.summary_row("Agency Commission (12%):", agency_commission)
    pdf.ln(1)
    pdf.summary_row("Subtotal before VAT:", subtotal_before_vat, bold=True)
    pdf.summary_row("VAT (15%):", vat)
    pdf.ln(1)
    pdf.summary_row("*  GRAND TOTAL (INC. VAT):", grand_total, highlight=True)

    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 5, "PAYMENT TERMS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(0, 5, "80% Advance Payment  -  20% After the Event", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 5, "SCOPE OF WORK", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    for line in [
        "-  Receiving and handling of client-supplied banners and frames, and assembly and erection of the",
        "    11 signage boards on 50 cm bases at the designated venue locations.",
        "-  Levelling, alignment, fixing and anchoring of all structures, plus on-site banner re-tensioning.",
        "-  Installation labour, tools, access equipment, on-site supervision, post-event dismantling,",
        "    removal of structures and site clearance.",
    ]:
        pdf.cell(0, 4, line, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 5, "NOTES", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    notes = [
        "1.  All prices are in Saudi Riyals (SAR) and rounded to the nearest Riyal.",
        "2.  Installation charged at 80 SAR per sqm of signage face area - total billable area 106 sqm",
        "     (3 x 10 sqm + 7 x 8 sqm + 1 x 20 sqm). The 50 cm base is included, not charged as extra area.",
        "3.  Banners and frames are client-supplied and available at the venue. Printing, fabrication and",
        "     supply of materials are NOT included. Client to provide site access, storage and power at no cost.",
        "4.  Rate assumes ground-level installation in a single mobilisation. Additional mobilisations, night",
        "     shifts, elevated fixing or any other requirement will be quoted separately. Validity: 30 days.",
    ]
    for note in notes:
        pdf.cell(0, 4, note, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)
    pdf.add_signature_block()

    out_path = os.path.join(os.path.dirname(__file__), "Event_Signage_Installation_Quotation.pdf")
    pdf.output(out_path)
    print(f"PDF generated: {out_path}")


if __name__ == "__main__":
    generate()
