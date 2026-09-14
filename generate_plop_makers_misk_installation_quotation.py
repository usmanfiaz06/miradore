"""Generate the Miradore quotation for the MISK immersive room screens installation.

Client: PLOP Makers
Scope:  Installation services only (installation, steel work, electrical work)
Value:  SAR 68,000 + 15% VAT
"""

from fpdf import FPDF
import os

BASE = os.path.dirname(os.path.abspath(__file__))

CLIENT = "PLOP Makers"
PROJECT = "IMMERSIVE ROOM SCREENS  -  MISK"
QUOTE_NO = "MRD-QT-2026-0914"
QUOTE_DATE = "14 September 2026"

INSTALLATION_COST = 68000
VAT_RATE = 0.15


class QuotationPDF(FPDF):
    TEAL = (0, 128, 128)
    ORANGE = (230, 100, 30)
    DARK = (40, 40, 40)
    GRAY = (100, 100, 100)
    LIGHT_BG = (245, 248, 250)
    WHITE = (255, 255, 255)
    SECTION_BG = (230, 243, 243)

    def header(self):
        if self.page_no() == 1:
            # Page 1 draws its own full letterhead via add_logo_header().
            return
        logo_path = os.path.join(BASE, "Miradore Logo Color.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=11, w=38)
        self.set_xy(110, 13)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*self.GRAY)
        self.cell(85, 4.5, f"QUOTATION {QUOTE_NO}  |  {CLIENT}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(110, 17.5)
        self.cell(85, 4.5, "Terms, notes and authorisation", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_y(26)
        self.draw_accent_line(0.5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(
            0,
            10,
            f"Page {self.page_no()}/{{nb}}  |  Miradore Experiences Company, Riyadh, KSA  |  Confidential",
            align="C",
        )

    # ---------- letterhead ----------

    def add_logo_header(self):
        logo_path = os.path.join(BASE, "Miradore Logo Color.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=12, w=55)
        self.set_xy(110, 12)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.DARK)
        self.cell(85, 5, "MIRADORE EXPERIENCES COMPANY", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(110, 17)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*self.GRAY)
        self.cell(85, 4.5, "C.R. No. 7054053371", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(110, 21.5)
        self.cell(85, 4.5, "Riyadh, Kingdom of Saudi Arabia", align="R", new_x="LMARGIN", new_y="NEXT")

    def draw_accent_line(self, width=0.8):
        self.set_draw_color(*self.TEAL)
        self.set_line_width(width)
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
        self.cell(0, 7, PROJECT, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.GRAY)
        self.cell(0, 5, "INSTALLATION SERVICES", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.draw_accent_line()

    def add_info_block(self):
        top = self.get_y()

        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "TO:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(90, 5, f"Client: {CLIENT}", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "PROJECT DETAILS:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        for line in [
            "Project: Immersive Room - Screen Installation",
            "Location: MISK",
            "Scope: Installation, steel work and electrical work",
        ]:
            self.cell(90, 5, line, new_x="LMARGIN", new_y="NEXT")

        right_labels = [
            ("FROM:", "Miradore Experiences Company, Riyadh"),
            ("QUOTATION NO:", QUOTE_NO),
            ("QUOTATION DATE:", QUOTE_DATE),
        ]
        y = top
        for label, value in right_labels:
            self.set_xy(110, y)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*self.TEAL)
            self.cell(85, 5, label, align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_xy(110, y + 5)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*self.DARK)
            self.cell(85, 5, value, align="R", new_x="LMARGIN", new_y="NEXT")
            y += 12

        self.set_y(max(self.get_y(), y))
        self.ln(4)

    # ---------- building blocks ----------

    def section_header(self, title):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(180, 6, f"  {title}", border=0, fill=True, new_x="LMARGIN", new_y="NEXT")

    def table_head(self, third_col="AMOUNT, SAR"):
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*self.TEAL)
        self.cell(10, 7, "S#", align="C")
        self.cell(125, 7, "DESCRIPTION", align="L")
        self.cell(45, 7, third_col, align="R")
        self.ln()
        self.rule(0.2)
        self.ln(1)

    def rule(self, width=0.2):
        self.set_draw_color(*self.TEAL)
        self.set_line_width(width)
        self.line(15, self.get_y(), 195, self.get_y())

    def line_item(self, sn, desc, amount, bold=True):
        self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "B" if bold else "", 8)
        self.cell(10, 7, str(sn), align="C")
        self.cell(125, 7, desc, align="L")
        self.set_font("Helvetica", "B" if bold else "", 8)
        self.cell(45, 7, amount, align="R")
        self.ln()

    def sub_item(self, label, text):
        self.set_x(25)
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*self.TEAL)
        self.cell(24, 4.5, f"{label}", align="L")
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*self.GRAY)
        self.multi_cell(146, 4.5, text, align="L", new_x="LMARGIN", new_y="NEXT")

    def exclusion_row(self, sn, item, detail, alt=False):
        self.set_fill_color(*(self.LIGHT_BG if alt else self.WHITE))
        self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "", 7.5)
        self.cell(10, 6, str(sn), align="C", fill=True)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(52, 6, item, align="L", fill=True)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*self.GRAY)
        self.cell(73, 6, detail, align="L", fill=True)
        self.set_font("Helvetica", "B", 7)
        self.set_text_color(*self.TEAL)
        self.cell(45, 6, "By client / quoted separately", align="R", fill=True)
        self.ln()

    def summary_row(self, label, amount, bold=False, highlight=False):
        if highlight:
            self.set_fill_color(*self.TEAL)
            self.set_text_color(*self.WHITE)
            self.set_font("Helvetica", "B", 8.5)
            self.cell(100, 8, "", fill=True)
            self.cell(45, 8, label, align="R", fill=True)
            self.cell(35, 8, amount, align="R", fill=True)
        else:
            self.set_fill_color(*self.LIGHT_BG)
            self.set_text_color(*self.DARK)
            self.set_font("Helvetica", "B" if bold else "", 7.5)
            self.cell(100, 7, "", fill=bold)
            self.cell(45, 7, label, align="R", fill=bold)
            self.set_font("Helvetica", "B", 7.5)
            self.cell(35, 7, amount, align="R", fill=bold)
        self.ln()

    def add_signature_block(self):
        y = self.get_y()

        sig_path = os.path.join(BASE, "adeel_signature-removebg-preview.png")
        if os.path.exists(sig_path):
            self.image(sig_path, x=16, y=y, w=42)

        stamp_path = os.path.join(BASE, "miradore_stamp_teal.png")
        if os.path.exists(stamp_path):
            self.image(stamp_path, x=78, y=y - 2, w=48)

        self.set_y(y + 18)
        self.set_draw_color(*self.TEAL)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 80, self.get_y())
        self.ln(2)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.DARK)
        self.cell(0, 5, "ADEEL AHMED  -  DIRECTOR", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, "Miradore Experiences Company, Riyadh, KSA", new_x="LMARGIN", new_y="NEXT")


def amount_in_words(value):
    return "Seventy Eight Thousand Two Hundred Saudi Riyals Only"


def generate():
    pdf = QuotationPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(15, 12, 15)
    pdf.add_page()

    pdf.add_logo_header()
    pdf.add_title_block()
    pdf.add_info_block()

    # ---- scope of work / price ----
    pdf.section_header("SCOPE OF WORK  -  OUR FEE")
    pdf.ln(1.5)
    pdf.table_head()

    pdf.line_item(1, "Installation of the immersive room screens  -  MISK", "68,000")
    pdf.ln(0.5)
    pdf.sub_item(
        "Installation:",
        "Full crew for the duration of the works: setting out the room, screen cabinet installation "
        "and alignment, corner forming, floor build, mapping and alignment support, commissioning, "
        "site supervision, HSE and the handover file.",
    )
    pdf.sub_item(
        "Steel work:",
        "Fabrication, treatment and erection of the structural steel substructure and supporting "
        "framework carrying the screen surfaces.",
    )
    pdf.sub_item(
        "Electrical work:",
        "Power distribution and data / power cable runs behind the surfaces, containment, first and "
        "second fix, terminations, testing and commissioning.",
    )

    pdf.ln(1)
    pdf.rule(0.2)
    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(100, 7, "")
    pdf.cell(45, 7, "Installation (lump sum):", align="R")
    pdf.cell(35, 7, "68,000", align="R")
    pdf.ln(6)

    # ---- exclusions ----
    pdf.section_header("EQUIPMENT AND MATERIALS  -  NOT INCLUDED IN THIS QUOTATION")
    pdf.ln(1.5)

    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(10, 6, "S#", align="C")
    pdf.cell(52, 6, "ITEM", align="L")
    pdf.cell(73, 6, "DETAIL", align="L")
    pdf.cell(45, 6, "SUPPLY", align="R")
    pdf.ln()
    pdf.rule(0.2)
    pdf.ln(1)

    exclusions = [
        ("Structural steel", "Sections, plates, fixings and treatment for the substructure"),
        ("Cable, wire and containment", "Data and power cable, trays, trunking and connectors"),
        ("Power distribution components", "Distribution boards, breakers and surge protection"),
        ("Floor deck and pedestals", "Load bearing deck, adjustable feet and top layer"),
        ("Access and lifting equipment", "Scaffold, mobile towers, lifting gear and crane time"),
        ("Screens, media and processing", "LED cabinets, processors, servers and content"),
    ]
    for i, (item, detail) in enumerate(exclusions, start=1):
        pdf.exclusion_row(i, item, detail, alt=(i % 2 == 0))

    pdf.ln(1)
    pdf.rule(0.2)
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(38, 4.5, "How materials are handled.")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    pdf.multi_cell(
        142,
        4.5,
        "All equipment and materials above are to be arranged and supplied by the client, or quoted "
        "by Miradore separately on request. Where Miradore is asked to supply them, they are priced "
        "once the site survey is signed off and the schedule is approved, and invoiced at cost "
        "against that approved schedule.",
        align="L",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(2)

    # ---- cost summary ----
    pdf.rule(0.5)
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 7, "COST SUMMARY", new_x="LMARGIN", new_y="NEXT")

    vat = INSTALLATION_COST * VAT_RATE
    grand_total = INSTALLATION_COST + vat

    pdf.summary_row("Installation services:", f"{INSTALLATION_COST:,}", bold=True)
    pdf.summary_row("VAT (15%):", f"{vat:,.2f}")
    pdf.ln(1)
    pdf.summary_row("TOTAL PAYABLE (INC. VAT):", f"{grand_total:,.2f}", highlight=True)
    pdf.ln(1.5)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(*pdf.GRAY)
    pdf.cell(180, 4.5, f"Amount in words: {amount_in_words(grand_total)}", align="R", new_x="LMARGIN", new_y="NEXT")

    # Terms, notes and the sign-off sit together on their own page.
    pdf.add_page()

    # ---- payment terms ----
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 6, "PAYMENT TERMS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(0, 5, "80% Advance Payment  -  20% On Completion and Handover", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(3)

    # ---- notes ----
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 6, "NOTES", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    notes = [
        "1.  All prices are in Saudi Riyals (SAR).",
        "2.  This quotation covers the installation of the immersive room screens at MISK only, "
        "inclusive of installation, steel work and electrical work as described above.",
        "3.  Equipment and materials (steel, cable and wire, containment, distribution components, "
        "floor deck, access and lifting gear) are not included. They will be arranged by the client, "
        "or quoted by Miradore separately at the client's request.",
        "4.  Screens, processing, media servers and content are supplied by the client.",
        "5.  The client is to provide safe site access, a temporary power supply, secure storage and "
        "a clear work area for the duration of the installation.",
        "6.  Pricing is based on a single continuous mobilisation. Any variation to the scope, or work "
        "outside the agreed programme, will be quoted separately.",
        "7.  This quotation is valid for 30 days from the date of issue.",
    ]
    for note in notes:
        pdf.multi_cell(180, 4.2, note, align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    pdf.add_signature_block()

    out_path = os.path.join(BASE, "PLOP_Makers_MISK_Immersive_Room_Installation_Quotation.pdf")
    pdf.output(out_path)
    print(f"PDF generated: {out_path}")

    # ---- companion CSV ----
    csv_path = os.path.join(BASE, "PLOP_Makers_MISK_Immersive_Room_Installation_Quotation.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("MIRADORE EXPERIENCES COMPANY - QUOTATION\n")
        f.write(f"Quotation No,{QUOTE_NO}\n")
        f.write(f"Date,{QUOTE_DATE}\n")
        f.write(f"Client,{CLIENT}\n")
        f.write("Project,Immersive Room Screens - MISK\n")
        f.write("Scope,Installation / Steel work / Electrical work\n\n")
        f.write("S#,Description,Amount SAR\n")
        f.write("1,Installation of the immersive room screens - MISK (lump sum),68000\n")
        f.write(",  Installation: crew, setting out, cabinet install and alignment, commissioning, supervision, HSE, handover,Included\n")
        f.write(",  Steel work: fabrication, treatment and erection of structural substructure,Included\n")
        f.write(",  Electrical work: power distribution, cable and containment, terminations, testing,Included\n\n")
        f.write("Equipment and materials - not included,,\n")
        for i, (item, detail) in enumerate(exclusions, start=1):
            f.write(f"{i},{item} - {detail},By client / quoted separately\n")
        f.write("\nCost Summary,,\n")
        f.write(f"Installation services,,{INSTALLATION_COST}\n")
        f.write(f"VAT (15%),,{vat:.2f}\n")
        f.write(f"Total payable (inc. VAT),,{grand_total:.2f}\n")
    print(f"CSV generated: {csv_path}")


if __name__ == "__main__":
    generate()
