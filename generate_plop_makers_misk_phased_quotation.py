"""Revised phased quotation for PLOP Makers - MISK immersive screens programme.

Supersedes MRD-QT-2026-0914 (room installation only).

Programme: content development, tunnel build for Misk Art Week 2026,
technical support during the run, dismantle, then re-use of the same
screens to build the immersive room.
"""

from fpdf import FPDF
import os

BASE = os.path.dirname(os.path.abspath(__file__))

CLIENT = "PLOP Makers"
PROJECT = "IMMERSIVE SCREENS PROGRAMME  -  MISK"
QUOTE_NO = "MRD-QT-2026-1006"
SUPERSEDES = "MRD-QT-2026-0914"
QUOTE_DATE = "06 October 2026"

# ---- commercial inputs ----
CONTENT_DEVELOPMENT = 34000
TUNNEL_BUILD = 80000
SUPPORT_DAY_RATE = 7500
ART_WEEK_DAYS = 6                     # Misk Art Week 2026: 5 - 10 December
DISMANTLE_RATE = 0.05                 # 5% of the tunnel build cost
IMMERSIVE_ROOM = 68000                # unchanged from MRD-QT-2026-0914
VAT_RATE = 0.15

SUPPORT_TOTAL = SUPPORT_DAY_RATE * ART_WEEK_DAYS          # 45,000
DISMANTLE_TOTAL = int(TUNNEL_BUILD * DISMANTLE_RATE)      # 4,000

PHASES = [
    (
        "Content development  -  immersive content around MISK City",
        "Creative development and production of the immersive content programme presented around MISK City: "
        "concept and art direction, 3D scene build, motion production, rendering and delivery mastered to the "
        "tunnel canvas. Does not include re-working the content for the immersive room canvas, which is "
        "quoted separately on request.",
        CONTENT_DEVELOPMENT,
    ),
    (
        "Tunnel build  -  Misk Art Week 2026",
        "Setting out, steel erection, screen cabinet installation and alignment to the arch geometry, cable and "
        "power runs behind the surfaces, mapping, colour calibration, commissioning, site supervision and HSE.",
        TUNNEL_BUILD,
    ),
    (
        f"Technical support during Art Week  -  {ART_WEEK_DAYS} days at SAR {SUPPORT_DAY_RATE:,} per day",
        "On-site technical crew for the run of Misk Art Week, 5 - 10 December 2026: daily pre-show checks, show "
        "operation, in-run maintenance and spares handling. Based on a ten hour day; additional hours pro rata.",
        SUPPORT_TOTAL,
    ),
    (
        "Dismantling of the tunnel",
        "Controlled dismantle of the screen cabinets and supporting structure, condition report on each cabinet, "
        "packing and handover for transfer to the immersive room build. Priced at 5% of the tunnel build cost.",
        DISMANTLE_TOTAL,
    ),
    (
        "Immersive room build  -  MISK",
        "Re-installation of the same screens as the five-surface immersive room: setting out, steel erection, "
        "cabinet install and alignment, arc corner forming, floor build, first and second fix, mapping, colour "
        "calibration, commissioning, supervision, HSE and the handover file.",
        IMMERSIVE_ROOM,
    ),
]

PROGRAMME = [
    ("Content lock", "Mid November 2026"),
    ("Tunnel build and commissioning", "01 - 04 December 2026"),
    ("Misk Art Week 2026", "05 - 10 December 2026"),
    ("Dismantle and condition report", "11 - 13 December 2026"),
    ("Immersive room build", "From mid December 2026, handover January 2027"),
]

EXCLUSIONS = [
    ("Structural steel", "Sections, plates, fixings and treatment for both structures"),
    ("Cable, wire and containment", "Data and power cable, trays, trunking and connectors"),
    ("Power distribution components", "Distribution boards, breakers and surge protection"),
    ("Floor deck and pedestals", "Load bearing deck, adjustable feet and top layer"),
    ("Access and lifting equipment", "Scaffold, mobile towers, lifting gear and crane time"),
    ("Screens, media and processing", "LED cabinets, processors, servers and spare cabinets"),
    ("Storage and transport", "Storage between the two builds and transfer between sites"),
    ("Permits and approvals", "Event permits, structural certification and public liability cover"),
    ("Content re-master for the room", "Re-scaling and re-stitching tunnel content to the room canvas"),
]


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
            return
        logo_path = os.path.join(BASE, "Miradore Logo Color.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=11, w=38)
        self.set_xy(105, 13)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*self.GRAY)
        self.cell(90, 4.5, f"QUOTATION {QUOTE_NO}  |  {CLIENT}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_xy(105, 17.5)
        self.cell(90, 4.5, "Programme, exclusions, notes and authorisation", align="R", new_x="LMARGIN", new_y="NEXT")
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
        self.set_y(34)
        self.draw_accent_line()
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*self.TEAL)
        self.cell(0, 9, "QUOTATION", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*self.ORANGE)
        self.cell(0, 6, PROJECT, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.GRAY)
        self.cell(0, 5, "MISK ART WEEK 2026 TUNNEL  +  IMMERSIVE ROOM", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.draw_accent_line()

    def add_info_block(self):
        top = self.get_y()

        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "TO:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        self.cell(90, 5, f"Client: {CLIENT}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1.5)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*self.TEAL)
        self.cell(90, 5, "PROJECT DETAILS:", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.DARK)
        for line in [
            "Project: Immersive screens - tunnel and room",
            "Location: MISK, Riyadh",
            "Event: Misk Art Week 2026, 05 - 10 December 2026",
        ]:
            self.cell(90, 5, line, new_x="LMARGIN", new_y="NEXT")

        right = [
            ("FROM:", "Miradore Experiences Company, Riyadh"),
            ("QUOTATION NO:", QUOTE_NO),
            ("QUOTATION DATE:", QUOTE_DATE),
        ]
        y = top
        for label, value in right:
            self.set_xy(105, y)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*self.TEAL)
            self.cell(90, 5, label, align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_xy(105, y + 5)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*self.DARK)
            self.cell(90, 5, value, align="R", new_x="LMARGIN", new_y="NEXT")
            y += 11

        self.set_xy(105, y)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(90, 4.5, f"Supersedes quotation {SUPERSEDES}", align="R", new_x="LMARGIN", new_y="NEXT")

        self.set_y(max(self.get_y(), y + 5))
        self.ln(3)

    # ---------- building blocks ----------

    def section_header(self, title):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(180, 6, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")

    def rule(self, width=0.2):
        self.set_draw_color(*self.TEAL)
        self.set_line_width(width)
        self.line(15, self.get_y(), 195, self.get_y())

    def table_head(self, col2="PHASE / DESCRIPTION", col3="AMOUNT, SAR"):
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*self.TEAL)
        self.cell(10, 6.5, "S#", align="C")
        self.cell(125, 6.5, col2, align="L")
        self.cell(45, 6.5, col3, align="R")
        self.ln()
        self.rule(0.2)
        self.ln(1)

    def phase_row(self, sn, title, detail, amount):
        self.set_text_color(*self.DARK)
        self.set_font("Helvetica", "B", 8)
        self.cell(10, 6, str(sn), align="C")
        self.cell(125, 6, title, align="L")
        self.cell(45, 6, f"{amount:,}", align="R")
        self.ln()
        self.set_x(25)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*self.GRAY)
        self.multi_cell(160, 4.2, detail, align="L", new_x="LMARGIN", new_y="NEXT")
        self.ln(1.5)

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

    def programme_row(self, stage, timing, alt=False):
        self.set_fill_color(*(self.LIGHT_BG if alt else self.WHITE))
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*self.DARK)
        self.cell(90, 6, f"  {stage}", align="L", fill=True)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*self.TEAL)
        self.cell(90, 6, f"{timing}  ", align="R", fill=True)
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
        # The block needs ~32mm; start a fresh page rather than split it.
        if self.get_y() > 243:
            self.add_page()
        y = self.get_y()
        sig = os.path.join(BASE, "adeel_signature-removebg-preview.png")
        if os.path.exists(sig):
            self.image(sig, x=16, y=y, w=42)
        stamp = os.path.join(BASE, "miradore_stamp_teal.png")
        if os.path.exists(stamp):
            self.image(stamp, x=78, y=y - 2, w=48)

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


def generate():
    subtotal = sum(amount for _, _, amount in PHASES)
    vat = subtotal * VAT_RATE
    grand_total = subtotal + vat
    assert subtotal == 231000, subtotal
    assert grand_total == 265650, grand_total

    pdf = QuotationPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(15, 12, 15)
    pdf.add_page()

    pdf.add_logo_header()
    pdf.add_title_block()
    pdf.add_info_block()

    # ---- phase schedule ----
    pdf.section_header("SCHEDULE OF SERVICES  -  OUR FEE")
    pdf.ln(1.5)
    pdf.table_head()
    for i, (title, detail, amount) in enumerate(PHASES, start=1):
        pdf.phase_row(i, title, detail, amount)

    pdf.rule(0.5)
    pdf.ln(2.5)

    # ---- cost summary ----
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 7, "COST SUMMARY", new_x="LMARGIN", new_y="NEXT")
    pdf.summary_row("Services subtotal:", f"{subtotal:,}", bold=True)
    pdf.summary_row("VAT (15%):", f"{vat:,.2f}")
    pdf.ln(1)
    pdf.summary_row("TOTAL PAYABLE (INC. VAT):", f"{grand_total:,.2f}", highlight=True)
    pdf.ln(1.5)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(*pdf.GRAY)
    pdf.cell(
        180,
        4.5,
        "Amount in words: Two Hundred and Sixty Five Thousand Six Hundred and Fifty Saudi Riyals Only",
        align="R",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.add_page()

    # ---- programme ----
    pdf.section_header("INDICATIVE PROGRAMME")
    pdf.ln(1.5)
    for i, (stage, timing) in enumerate(PROGRAMME):
        pdf.programme_row(stage, timing, alt=(i % 2 == 1))
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    pdf.multi_cell(
        180,
        4.2,
        "The same screens serve both builds, so the immersive room cannot commence until the tunnel is "
        "dismantled and the cabinets are condition checked. Dates are indicative and will be confirmed against "
        "the site survey and the Misk Art Week build access windows.",
        align="L",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)

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
    for i, (item, detail) in enumerate(EXCLUSIONS, start=1):
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
        "All equipment and materials above are to be arranged and supplied by the client, or quoted by Miradore "
        "separately on request. Where Miradore supplies them, they are priced once the survey is signed off and "
        "invoiced at cost.",
        align="L",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(3)

    # ---- payment terms ----
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 6, "PAYMENT TERMS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(0, 5, "80% Advance Payment  -  20% On Completion and Handover of each phase", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # ---- notes ----
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 6, "NOTES", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    notes = [
        "1.  All prices are in Saudi Riyals (SAR).",
        f"2.  This quotation supersedes quotation {SUPERSEDES} in full.",
        "3.  The same screens serve both builds. The room build follows the dismantle and cannot run concurrently.",
        "4.  Tunnel length and geometry are limited by the screen inventory, confirmed at survey.",
        "5.  Pricing assumes the tunnel is sited indoors. Outdoor siting requires weather protection, quoted separately.",
        "6.  Technical support is charged at SAR 7,500 per day for the six days of Art Week, based on a ten hour "
        "day. Additional days are charged at the same daily rate and additional hours pro rata.",
        "7.  Dismantling is priced at 5% of the tunnel build cost and covers a controlled dismantle and condition "
        "report. Cabinets found damaged on condition check are replaced at the client's cost unless caused by "
        "Miradore.",
        "8.  Equipment and materials listed above are not included and will be arranged by the client or quoted "
        "separately at the client's request.",
        "9.  Content produced for the tunnel is mastered to the tunnel canvas only. Re-use on the room canvas "
        "requires re-scaling and re-stitching, which is not included and is quoted separately on request.",
        "10.  The client is to provide safe site access, temporary power, secure storage and a clear work area.",
        "11.  This quotation is valid for 30 days from the date of issue.",
    ]
    for note in notes:
        pdf.multi_cell(180, 3.8, note, align="L", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.add_signature_block()

    out_pdf = os.path.join(BASE, "PLOP_Makers_MISK_Immersive_Screens_Programme_Quotation.pdf")
    pdf.output(out_pdf)
    print(f"PDF generated: {out_pdf}")

    out_csv = os.path.join(BASE, "PLOP_Makers_MISK_Immersive_Screens_Programme_Quotation.csv")
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write("MIRADORE EXPERIENCES COMPANY - QUOTATION\n")
        f.write(f"Quotation No,{QUOTE_NO}\n")
        f.write(f"Supersedes,{SUPERSEDES}\n")
        f.write(f"Date,{QUOTE_DATE}\n")
        f.write(f"Client,{CLIENT}\n")
        f.write("Project,Immersive screens programme - MISK\n")
        f.write("Event,Misk Art Week 2026 (05 - 10 December 2026)\n\n")
        f.write("S#,Phase,Amount SAR\n")
        for i, (title, _, amount) in enumerate(PHASES, start=1):
            f.write(f'{i},"{title}",{amount}\n')
        f.write(f"\nServices subtotal,,{subtotal}\n")
        f.write(f"VAT (15%),,{vat:.2f}\n")
        f.write(f"Total payable (inc. VAT),,{grand_total:.2f}\n\n")
        f.write("Equipment and materials - not included,,\n")
        for i, (item, detail) in enumerate(EXCLUSIONS, start=1):
            f.write(f'{i},"{item} - {detail}",By client / quoted separately\n')
    print(f"CSV generated: {out_csv}")


if __name__ == "__main__":
    generate()
