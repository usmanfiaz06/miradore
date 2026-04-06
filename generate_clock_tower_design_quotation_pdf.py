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
        self.cell(0, 5, "DESIGN & CONTENT SERVICES", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.draw_accent_line()

    def add_info_block(self):
        y = self.get_y()
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
        for item in [
            "Event: Guinness World Record Award Ceremony",
            "Venue: Clock Tower Museum - Makkah",
        ]:
            self.cell(90, 5, item, new_x="LMARGIN", new_y="NEXT")

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

    def section_header(self, title):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(185, 6, f"  {title}", border=0, fill=True, new_x="LMARGIN", new_y="NEXT")

    def package_item(self, sn, desc, alt=False):
        if alt:
            self.set_fill_color(*self.LIGHT_BG)
        else:
            self.set_fill_color(*self.WHITE)
        self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "", 8)
        self.cell(10, 7, str(sn), border=0, align="C", fill=True)
        self.cell(175, 7, desc, border=0, align="L", fill=True)
        self.ln()

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

    pdf.add_logo_header()
    pdf.add_title_block()
    pdf.add_info_block()

    # Package header
    pdf.section_header("DESIGN & CONTENT PACKAGE")
    pdf.ln(2)

    # Package items
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(10, 7, "S#", align="C")
    pdf.cell(175, 7, "DELIVERABLE", align="L")
    pdf.ln()

    pdf.set_draw_color(*pdf.TEAL)
    pdf.set_line_width(0.2)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(1)

    pdf.package_item(1, "Theme Key Visual (KV) Design - Event Identity & Branding")
    pdf.package_item(2, "Social Media Posts & Stories (Event Announcement & Highlights)", alt=True)
    pdf.package_item(3, "Event Introductory Video for Hall Screen")
    pdf.package_item(4, "Backdrop & Lama Stand Artwork (Print-Ready Files)", alt=True)
    pdf.package_item(5, "Digital Invitations & Event Collateral")

    pdf.ln(2)
    pdf.set_draw_color(*pdf.TEAL)
    pdf.set_line_width(0.2)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(120, 7, "", border=0)
    pdf.cell(30, 7, "Package Total:", border=0, align="R")
    pdf.cell(35, 7, "18,000", border=0, align="R")
    pdf.ln()

    pdf.ln(6)

    # Cost Summary
    pdf.set_draw_color(*pdf.TEAL)
    pdf.set_line_width(0.5)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 7, "COST SUMMARY", new_x="LMARGIN", new_y="NEXT")

    design_total = 18000
    vat = design_total * 0.15  # 2,700
    grand_total = design_total + vat  # 20,700

    pdf.summary_row("Design & Content Services:", design_total, bold=True)
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
        "2.  This is a separate quotation for design and content services only.",
        "3.  Theme KV establishes the visual identity for all event materials.",
        "4.  Introductory video designed for hall LED screen playback.",
        "5.  All artwork delivered in print-ready and digital formats.",
        "6.  Any additional design requirements beyond this scope will be quoted separately.",
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

    out_path = os.path.join(os.path.dirname(__file__), "Clock_Tower_Design_Content_Quotation.pdf")
    pdf.output(out_path)
    print(f"PDF generated: {out_path}")


if __name__ == "__main__":
    generate()
