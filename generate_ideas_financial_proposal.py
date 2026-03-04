#!/usr/bin/env python3
"""
Generate Financial / Commercial Proposal (BOQ) PDF for IDEAS 2026 & 2028 - DEPO RFP
Miradore Experiences branded proposal - Pakistani pricing standards (PKR)
"""

from fpdf import FPDF
import os

# ── Brand Palette ──
TEAL = (0, 128, 128)
ORANGE = (230, 100, 30)
DARK = (40, 40, 40)
GRAY = (100, 100, 100)
LIGHT_BG = (245, 248, 250)
WHITE = (255, 255, 255)
SECTION_BG = (230, 243, 243)
NAVY = (20, 40, 65)

# ── Exchange Rates (per RFP Section 6.2) ──
FX_2026 = 279.5
FX_2027 = 290.0
FX_2028 = 300.0


def fmt(n):
    """Format number with commas, no decimals."""
    if n == 0:
        return "-"
    return f"{n:,.0f}"


def fmt_usd(pkr, year=None):
    """Convert PKR to USD at planning rate."""
    if pkr == 0:
        return "-"
    rate = {2026: FX_2026, 2027: FX_2027, 2028: FX_2028}.get(year, FX_2026)
    return f"${pkr / rate:,.0f}"


class FinancialPDF(FPDF):
    show_header = True

    def header(self):
        if not self.show_header:
            return
        logo_path = os.path.join(os.path.dirname(__file__), "Miradore Logo Color.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=8, y=6, w=35)
        self.set_xy(100, 8)
        self.set_font("Helvetica", "", 6)
        self.set_text_color(*GRAY)
        self.cell(98, 4, "COMMERCIAL PROPOSAL  |  RFP-DEPO-IDEAS-2026-001", align="R")
        self.set_draw_color(*TEAL)
        self.set_line_width(0.5)
        self.line(8, 15, 289, 15)
        self.set_y(18)

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 5.5)
        self.set_text_color(*GRAY)
        self.cell(0, 6, f"Miradore Experiences  |  Confidential  |  Page {self.page_no()}/{{nb}}", align="C")

    def accent_line(self, y=None):
        if y is None:
            y = self.get_y()
        self.set_draw_color(*TEAL)
        self.set_line_width(0.5)
        self.line(8, y, 289, y)

    def section_banner(self, title):
        if self.get_y() > 175:
            self.add_page()
        self.set_fill_color(*TEAL)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(281, 6, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")

    def boq_header(self):
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 5.5)
        cols = [
            (8, "#"), (75, "DESCRIPTION"), (12, "QTY"), (16, "UNIT"),
            (28, "UNIT RATE (PKR)"), (32, "2026 (PKR)"), (32, "2027 (PKR)"),
            (32, "2028 (PKR)"), (22, "MGMT FEE"), (28, "TOTAL (PKR)"),
        ]
        for w, label in cols:
            self.cell(w, 6, label, align="C", fill=True)
        self.ln()

    def boq_row(self, num, desc, qty, unit, rate, y2026, y2027, y2028, mgmt_fee, total, alt=False, bold=False):
        if self.get_y() > 190:
            self.add_page()
            self.boq_header()
        bg = LIGHT_BG if alt else WHITE
        self.set_fill_color(*bg)
        self.set_text_color(*DARK)
        style = "B" if bold else ""
        self.set_font("Helvetica", style, 5.5)
        self.cell(8, 5, str(num) if num else "", align="C", fill=True)
        self.set_font("Helvetica", style, 5.5)
        self.cell(75, 5, desc[:62], fill=True)
        self.cell(12, 5, str(qty) if qty else "", align="C", fill=True)
        self.cell(16, 5, unit, align="C", fill=True)
        self.set_font("Helvetica", style, 5.5)
        self.cell(28, 5, fmt(rate) if rate else "", align="R", fill=True)
        self.cell(32, 5, fmt(y2026), align="R", fill=True)
        self.cell(32, 5, fmt(y2027), align="R", fill=True)
        self.cell(32, 5, fmt(y2028), align="R", fill=True)
        self.cell(22, 5, fmt(mgmt_fee), align="R", fill=True)
        self.set_font("Helvetica", "B" if bold else style, 5.5)
        self.cell(28, 5, fmt(total), align="R", fill=True)
        self.ln()

    def subtotal_line(self, label, total, mgmt=0):
        self.set_fill_color(*SECTION_BG)
        self.set_text_color(*TEAL)
        self.set_font("Helvetica", "B", 5.5)
        self.cell(83, 5, "", fill=True)
        self.cell(120, 5, label, align="R", fill=True)
        self.cell(22, 5, fmt(mgmt) if mgmt else "", align="R", fill=True)
        self.cell(28, 5, fmt(total), align="R", fill=True)
        self.ln()

    def summary_line(self, label, amount, highlight=False, bold=True):
        if highlight:
            self.set_fill_color(*TEAL)
            self.set_text_color(*WHITE)
        else:
            self.set_fill_color(*LIGHT_BG if bold else WHITE)
            self.set_text_color(*DARK)
        self.set_font("Helvetica", "B" if bold else "", 7 if highlight else 6.5)
        self.cell(225, 6.5 if highlight else 5.5, label, align="R", fill=True)
        self.set_font("Helvetica", "B", 7 if highlight else 6.5)
        self.cell(28, 6.5 if highlight else 5.5, fmt(amount), align="R", fill=True)
        self.ln()


def generate_financial():
    pdf = FinancialPDF(orientation="L", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)

    # ════════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════════
    pdf.show_header = False
    pdf.add_page()

    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 0, 297, 60, "F")

    logo_path = os.path.join(os.path.dirname(__file__), "Miradore Logo Color.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=15, y=10, w=55)

    pdf.set_y(25)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 5, "COMMERCIAL / FINANCIAL PROPOSAL", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "BILL OF QUANTITIES (BOQ)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(255, 220, 180)
    pdf.cell(0, 8, "IDEAS 2026 & IDEAS 2028", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_fill_color(*ORANGE)
    pdf.rect(0, 60, 297, 2.5, "F")

    pdf.set_y(75)
    details = [
        ("RFP Reference:", "RFP-DEPO-IDEAS-2026-001"),
        ("Submitted To:", "Defence Export Promotion Organisation (DEPO), Ministry of Defence Production"),
        ("Submitted By:", "Miradore Experiences - Riyadh, KSA | Karachi, Pakistan"),
        ("Currency:", "Pakistani Rupee (PKR)  |  All prices exclusive of sales tax"),
        ("Exchange Rates:", f"2026: USD 1 = PKR {FX_2026}  |  2027: USD 1 = PKR {FX_2027}  |  2028: USD 1 = PKR {FX_2028}"),
        ("Proposal Date:", "March 2026"),
        ("Validity:", "90 days from submission deadline"),
    ]
    for label, value in details:
        pdf.set_x(40)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(*TEAL)
        pdf.cell(45, 6.5, label)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*DARK)
        pdf.cell(200, 6.5, value, new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(130)
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_x(40)
    pdf.cell(220, 6, "  CONFIDENTIAL  |  ENVELOPE 2: COMMERCIAL / FINANCIAL PROPOSAL  |  FOR AUTHORISED RECIPIENTS ONLY", fill=True, align="C")

    # Bottom
    pdf.set_y(170)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 5, "MIRADORE EXPERIENCES", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, "Riyadh, KSA  |  Karachi, Pakistan  |  hello@miradore.co", align="C")

    # ════════════════════════════════════════════════════════════
    # BOQ - MAIN TABLE
    # ════════════════════════════════════════════════════════════
    pdf.show_header = True
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 7, "SECTION-BY-SECTION BILL OF QUANTITIES", new_x="LMARGIN", new_y="NEXT")
    pdf.accent_line()
    pdf.ln(3)

    pdf.boq_header()

    # ────────────────────────────────────────────────────────────
    # SECTION 1: RETAINER (34 months)
    # Monthly retainer: PKR 3,200,000
    # ────────────────────────────────────────────────────────────
    monthly_retainer = 3_200_000
    s1_2026 = monthly_retainer * 10  # Mar-Dec
    s1_2027 = monthly_retainer * 12
    s1_2028 = monthly_retainer * 12
    s1_total = s1_2026 + s1_2027 + s1_2028

    pdf.section_banner("SECTION 1  |  Retainer Services: Strategy, Social Media & Creative (34 months)")
    pdf.boq_row("1.1", "Monthly Retainer Fee (Strategy, Planning, Brand Mgmt)", 34, "Month", monthly_retainer, s1_2026, s1_2027, s1_2028, 0, s1_total)
    pdf.boq_row("1.2", "Social Media Management (6 platforms, daily)", 34, "Month", 0, 0, 0, 0, 0, 0, alt=True)
    pdf.boq_row("", "  (Included in monthly retainer)", "", "", 0, 0, 0, 0, 0, 0)
    pdf.boq_row("1.3", "Visual Design - 20 posts/month (680 total)", 680, "Post", 0, 0, 0, 0, 0, 0, alt=True)
    pdf.boq_row("", "  (Included in monthly retainer)", "", "", 0, 0, 0, 0, 0, 0)
    pdf.boq_row("1.4", "Motion Graphics & Animated Assets (68 total)", 68, "Asset", 0, 0, 0, 0, 0, 0, alt=True)
    pdf.boq_row("", "  (Included in monthly retainer)", "", "", 0, 0, 0, 0, 0, 0)
    pdf.boq_row("1.5", "Press Release Drafting (46+ over contract)", 46, "Release", 0, 0, 0, 0, 0, 0, alt=True)
    pdf.boq_row("", "  (Included in monthly retainer)", "", "", 0, 0, 0, 0, 0, 0)
    pdf.boq_row("1.6", "Translation Services (150+ documents)", 150, "Doc", 0, 0, 0, 0, 0, 0, alt=True)
    pdf.boq_row("", "  (Included in monthly retainer)", "", "", 0, 0, 0, 0, 0, 0)
    pdf.boq_row("1.7", "Monthly Performance Dashboards", 34, "Report", 0, 0, 0, 0, 0, 0, alt=True)
    pdf.boq_row("", "  (Included in monthly retainer)", "", "", 0, 0, 0, 0, 0, 0)
    pdf.boq_row("1.8", "Website Content & SEO (monthly CMS updates)", 34, "Month", 0, 0, 0, 0, 0, 0, alt=True)
    pdf.boq_row("", "  (Included in monthly retainer)", "", "", 0, 0, 0, 0, 0, 0)
    pdf.subtotal_line("Section 1 Subtotal:", s1_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 2: Event Designing (edition only)
    # ────────────────────────────────────────────────────────────
    s2_per_edition = 9_500_000
    s2_2026 = s2_per_edition
    s2_2028 = s2_per_edition
    s2_total = s2_2026 + s2_2028

    pdf.section_banner("SECTION 2  |  Event Designing: Non-Fabrication Creative (Edition Only)")
    pdf.boq_row("2.1", "3D Venue Walk-through Rendering (full KEC layout)", 2, "Edition", 1_800_000, 1_800_000, 0, 1_800_000, 0, 3_600_000)
    pdf.boq_row("2.2", "Signage & Wayfinding System Design (complete set)", 2, "Edition", 1_200_000, 1_200_000, 0, 1_200_000, 0, 2_400_000, alt=True)
    pdf.boq_row("2.3", "Stage & Main Hall Design Concepts", 2, "Edition", 1_500_000, 1_500_000, 0, 1_500_000, 0, 3_000_000)
    pdf.boq_row("2.4", "Opening Ceremony Design", 2, "Edition", 1_000_000, 1_000_000, 0, 1_000_000, 0, 2_000_000, alt=True)
    pdf.boq_row("2.5", "Gala Dinner, Golf Tournament, Air Show Designs", 2, "Edition", 1_200_000, 1_200_000, 0, 1_200_000, 0, 2_400_000)
    pdf.boq_row("2.6", "Conference Branding, Gift/Protocol Pack, Exhibitor Kit", 2, "Edition", 1_000_000, 1_000_000, 0, 1_000_000, 0, 2_000_000, alt=True)
    pdf.boq_row("2.7", "Print Collateral Design & Sponsorship Kit (4 tiers)", 2, "Edition", 900_000, 900_000, 0, 900_000, 0, 1_800_000)
    pdf.boq_row("2.8", "Event Mobile App Design Files (UI/UX)", 2, "Edition", 900_000, 900_000, 0, 900_000, 0, 1_800_000, alt=True)
    pdf.subtotal_line("Section 2 Subtotal:", s2_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 3: Coffee Table Book (edition only, subcontracted printing)
    # ────────────────────────────────────────────────────────────
    s3_agency = 2_800_000  # design, copy, editing per edition
    s3_mgmt = int(s3_agency * 0.15)
    s3_total_per = s3_agency + s3_mgmt
    s3_total = s3_total_per * 2

    pdf.section_banner("SECTION 3  |  Coffee Table Book (Edition Only)")
    pdf.boq_row("3.1", "Content: Copywriting, Editing, Bilingual (EN/UR)", 2, "Edition", 1_200_000, 1_200_000, 0, 1_200_000, 0, 2_400_000)
    pdf.boq_row("3.2", "Design & Layout (~200 pages, print-ready artwork)", 2, "Edition", 1_600_000, 1_600_000, 0, 1_600_000, 0, 3_200_000, alt=True)
    s3_mgmt_total = int(2_800_000 * 0.15) * 2
    pdf.boq_row("3.3", "Management Fee (15% on production coordination)", 2, "Edition", int(2_800_000 * 0.15), s3_mgmt, 0, s3_mgmt, 0, s3_mgmt_total)
    pdf.subtotal_line("Section 3 Subtotal:", s3_total, s3_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 4: International PR (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s4_sub = 14_500_000  # subcontractor cost per edition
    s4_mgmt_per = int(s4_sub * 0.15)
    s4_total = (s4_sub + s4_mgmt_per) * 2

    pdf.section_banner("SECTION 4  |  PR: International Media (Edition Only) - Subcontracted")
    pdf.boq_row("4.1", "International PR Strategy & Execution", 2, "Edition", 6_000_000, 6_000_000, 0, 6_000_000, 0, 12_000_000)
    pdf.boq_row("4.2", "International Journalist Hosting & Accreditation", 2, "Edition", 4_500_000, 4_500_000, 0, 4_500_000, 0, 9_000_000, alt=True)
    pdf.boq_row("4.3", "Press Releases (12/edition) & Press Conference", 2, "Edition", 2_000_000, 2_000_000, 0, 2_000_000, 0, 4_000_000)
    pdf.boq_row("4.4", "Relationship Mgmt (12+ intl defence editors)", 2, "Edition", 2_000_000, 2_000_000, 0, 2_000_000, 0, 4_000_000, alt=True)
    s4_mgmt_total = s4_mgmt_per * 2
    pdf.boq_row("4.5", "Management Fee (15%)", 2, "Edition", s4_mgmt_per, s4_mgmt_per, 0, s4_mgmt_per, 0, s4_mgmt_total)
    pdf.subtotal_line("Section 4 Subtotal:", s4_total, s4_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 5: Local PR (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s5_sub = 7_500_000
    s5_mgmt_per = int(s5_sub * 0.15)
    s5_total = (s5_sub + s5_mgmt_per) * 2

    pdf.section_banner("SECTION 5  |  Local PR Coverage (Edition Only) - Subcontracted")
    pdf.boq_row("5.1", "Local PR Strategy & National Media Relations", 2, "Edition", 3_000_000, 3_000_000, 0, 3_000_000, 0, 6_000_000)
    pdf.boq_row("5.2", "Press Conferences & Spokesperson Preparation", 2, "Edition", 2_000_000, 2_000_000, 0, 2_000_000, 0, 4_000_000, alt=True)
    pdf.boq_row("5.3", "Press Releases (24 total EN/UR) & Broadcast Coord.", 2, "Edition", 1_500_000, 1_500_000, 0, 1_500_000, 0, 3_000_000)
    pdf.boq_row("5.4", "Journalist Accreditation & On-ground Facilitation", 2, "Edition", 1_000_000, 1_000_000, 0, 1_000_000, 0, 2_000_000, alt=True)
    s5_mgmt_total = s5_mgmt_per * 2
    pdf.boq_row("5.5", "Management Fee (15%)", 2, "Edition", s5_mgmt_per, s5_mgmt_per, 0, s5_mgmt_per, 0, s5_mgmt_total)
    pdf.subtotal_line("Section 5 Subtotal:", s5_total, s5_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 6: International OOH (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s6_media = 82_000_000  # media spend per edition
    s6_agency = 8_000_000  # creative adaptation, planning per edition
    s6_sub_total = s6_media + s6_agency
    s6_mgmt_per = int(s6_sub_total * 0.15)
    s6_total = (s6_sub_total + s6_mgmt_per) * 2

    pdf.section_banner("SECTION 6  |  Outdoor Advertising: International (Edition Only) - Subcontracted")
    pdf.boq_row("6.1", "Tier 1 OOH: Abu Dhabi, London, Ankara, Doha (4 cities)", 2, "Edition", 42_000_000, 42_000_000, 0, 42_000_000, 0, 84_000_000)
    pdf.boq_row("6.2", "Tier 2 OOH: Washington DC, Paris, Beijing, Istanbul", 2, "Edition", 28_000_000, 28_000_000, 0, 28_000_000, 0, 56_000_000, alt=True)
    pdf.boq_row("6.3", "Tier 3 OOH: KL, Cairo, Riyadh, Nairobi (optional)", 2, "Edition", 12_000_000, 12_000_000, 0, 12_000_000, 0, 24_000_000)
    pdf.boq_row("6.4", "Creative Adaptation & Technical File Delivery", 2, "Edition", 4_000_000, 4_000_000, 0, 4_000_000, 0, 8_000_000, alt=True)
    pdf.boq_row("6.5", "Media Planning, Buying & Confirmation Reports", 2, "Edition", 4_000_000, 4_000_000, 0, 4_000_000, 0, 8_000_000)
    s6_mgmt_total = s6_mgmt_per * 2
    pdf.boq_row("6.6", "Management Fee (15%)", 2, "Edition", s6_mgmt_per, s6_mgmt_per, 0, s6_mgmt_per, 0, s6_mgmt_total)
    pdf.subtotal_line("Section 6 Subtotal:", s6_total, s6_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 7: Pakistan OOH (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s7_media = 42_000_000  # 145+ sites
    s7_agency = 5_500_000
    s7_sub_total = s7_media + s7_agency
    s7_mgmt_per = int(s7_sub_total * 0.15)
    s7_total = (s7_sub_total + s7_mgmt_per) * 2

    pdf.section_banner("SECTION 7  |  Outdoor Advertising: Pakistan (Edition Only) - Subcontracted")
    pdf.boq_row("7.1", "Karachi OOH (60+ sites: billboards, unipoles, transit)", 2, "Edition", 18_000_000, 18_000_000, 0, 18_000_000, 0, 36_000_000)
    pdf.boq_row("7.2", "Lahore OOH (35+ sites)", 2, "Edition", 10_000_000, 10_000_000, 0, 10_000_000, 0, 20_000_000, alt=True)
    pdf.boq_row("7.3", "Islamabad/Rawalpindi OOH (35+ sites)", 2, "Edition", 9_000_000, 9_000_000, 0, 9_000_000, 0, 18_000_000)
    pdf.boq_row("7.4", "Additional Cities / Mall Media / Bus Shelters", 2, "Edition", 5_000_000, 5_000_000, 0, 5_000_000, 0, 10_000_000, alt=True)
    pdf.boq_row("7.5", "Creative Adaptation & GPS-tagged Confirmation", 2, "Edition", 3_000_000, 3_000_000, 0, 3_000_000, 0, 6_000_000)
    pdf.boq_row("7.6", "Drone Documentation (subject to MOD/CAA approval)", 2, "Edition", 2_500_000, 2_500_000, 0, 2_500_000, 0, 5_000_000, alt=True)
    s7_mgmt_total = s7_mgmt_per * 2
    pdf.boq_row("7.7", "Management Fee (15%)", 2, "Edition", s7_mgmt_per, s7_mgmt_per, 0, s7_mgmt_per, 0, s7_mgmt_total)
    pdf.subtotal_line("Section 7 Subtotal:", s7_total, s7_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 8: Digital Media Buying (all 34 months)
    # ────────────────────────────────────────────────────────────
    s8_retainer_monthly = 1_800_000
    s8_edition_activation = 18_000_000  # per edition surge
    s8_2026 = s8_retainer_monthly * 10 + s8_edition_activation
    s8_2027 = s8_retainer_monthly * 12
    s8_2028 = s8_retainer_monthly * 12 + s8_edition_activation
    s8_sub = s8_2026 + s8_2027 + s8_2028
    s8_mgmt = int(s8_sub * 0.15)
    s8_total = s8_sub + s8_mgmt

    pdf.section_banner("SECTION 8  |  Digital Media Buying (Active: All 34 months) - Subcontracted")
    pdf.boq_row("8.1", "Retainer Phase: Brand Awareness & Remarketing", 34, "Month", s8_retainer_monthly, s8_retainer_monthly * 10, s8_retainer_monthly * 12, s8_retainer_monthly * 12, 0, s8_retainer_monthly * 34)
    pdf.boq_row("8.2", "Edition Activation: Performance Campaigns", 2, "Edition", s8_edition_activation, s8_edition_activation, 0, s8_edition_activation, 0, s8_edition_activation * 2, alt=True)
    pdf.boq_row("8.3", "Management Fee (15%)", 1, "Lump", s8_mgmt, 0, 0, 0, s8_mgmt, s8_mgmt)
    pdf.subtotal_line("Section 8 Subtotal:", s8_total, s8_mgmt)

    # ────────────────────────────────────────────────────────────
    # SECTION 9: Local Influencers (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s9_sub = 10_000_000
    s9_mgmt_per = int(s9_sub * 0.15)
    s9_total = (s9_sub + s9_mgmt_per) * 2

    pdf.section_banner("SECTION 9  |  Local Influencer Management (Edition Only) - Subcontracted")
    pdf.boq_row("9.1", "Influencer Identification, Briefing & Contracting (30+)", 2, "Edition", 2_500_000, 2_500_000, 0, 2_500_000, 0, 5_000_000)
    pdf.boq_row("9.2", "Influencer Fees & Content Production", 2, "Edition", 6_000_000, 6_000_000, 0, 6_000_000, 0, 12_000_000, alt=True)
    pdf.boq_row("9.3", "Campaign Management & Performance Reporting", 2, "Edition", 1_500_000, 1_500_000, 0, 1_500_000, 0, 3_000_000)
    s9_mgmt_total = s9_mgmt_per * 2
    pdf.boq_row("9.4", "Management Fee (15%)", 2, "Edition", s9_mgmt_per, s9_mgmt_per, 0, s9_mgmt_per, 0, s9_mgmt_total)
    pdf.subtotal_line("Section 9 Subtotal:", s9_total, s9_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 10: International Influencers (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s10_sub = 16_000_000
    s10_mgmt_per = int(s10_sub * 0.15)
    s10_total = (s10_sub + s10_mgmt_per) * 2

    pdf.section_banner("SECTION 10  |  International Influencer Program (Edition Only) - Subcontracted")
    pdf.boq_row("10.1", "Influencer Identification & Multi-market Sourcing (20+, 8 countries)", 2, "Edition", 3_500_000, 3_500_000, 0, 3_500_000, 0, 7_000_000)
    pdf.boq_row("10.2", "Influencer Fees & Content Production (Intl rates)", 2, "Edition", 10_000_000, 10_000_000, 0, 10_000_000, 0, 20_000_000, alt=True)
    pdf.boq_row("10.3", "Legal Clearance, Compliance & Performance Reporting", 2, "Edition", 2_500_000, 2_500_000, 0, 2_500_000, 0, 5_000_000)
    s10_mgmt_total = s10_mgmt_per * 2
    pdf.boq_row("10.4", "Management Fee (15%)", 2, "Edition", s10_mgmt_per, s10_mgmt_per, 0, s10_mgmt_per, 0, s10_mgmt_total)
    pdf.subtotal_line("Section 10 Subtotal:", s10_total, s10_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 11: Events Coverage & Media Centre (edition only)
    # ────────────────────────────────────────────────────────────
    s11_per = 9_000_000
    s11_total = s11_per * 2

    pdf.section_banner("SECTION 11  |  Events Coverage & Media Centre (Edition Only)")
    pdf.boq_row("11.1", "Photography Crew (15+ photographers, 4 days)", 2, "Edition", 2_500_000, 2_500_000, 0, 2_500_000, 0, 5_000_000)
    pdf.boq_row("11.2", "Videography Crew (15+ videographers, 4 days)", 2, "Edition", 3_000_000, 3_000_000, 0, 3_000_000, 0, 6_000_000, alt=True)
    pdf.boq_row("11.3", "Real-time Social Media Content Team", 2, "Edition", 1_200_000, 1_200_000, 0, 1_200_000, 0, 2_400_000)
    pdf.boq_row("11.4", "Media Centre Operations & Accreditation", 2, "Edition", 1_300_000, 1_300_000, 0, 1_300_000, 0, 2_600_000, alt=True)
    pdf.boq_row("11.5", "Same-day Highlights Reel Production", 2, "Edition", 1_000_000, 1_000_000, 0, 1_000_000, 0, 2_000_000)
    pdf.subtotal_line("Section 11 Subtotal:", s11_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 12: Post-Show Report (edition only)
    # ────────────────────────────────────────────────────────────
    s12_per = 2_200_000
    s12_total = s12_per * 2

    pdf.section_banner("SECTION 12  |  Post-Show Report (Edition Only)")
    pdf.boq_row("12.1", "Comprehensive Post-Event Report (all sections)", 2, "Edition", 1_500_000, 1_500_000, 0, 1_500_000, 0, 3_000_000)
    pdf.boq_row("12.2", "Sustainability Documentation & Recommendations", 2, "Edition", 700_000, 700_000, 0, 700_000, 0, 1_400_000, alt=True)
    pdf.subtotal_line("Section 12 Subtotal:", s12_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 13: Cinematic Productions (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s13_sub = 28_000_000
    s13_mgmt_per = int(s13_sub * 0.15)
    s13_total = (s13_sub + s13_mgmt_per) * 2

    pdf.section_banner("SECTION 13  |  Cinematic Productions (Edition Only) - Subcontracted")
    pdf.boq_row("13.1", "Main Promotional Film (concept to delivery)", 2, "Edition", 5_000_000, 5_000_000, 0, 5_000_000, 0, 10_000_000)
    pdf.boq_row("13.2", "Documentary Segments (3 per edition)", 6, "Film", 2_500_000, 7_500_000, 0, 7_500_000, 0, 15_000_000, alt=True)
    pdf.boq_row("13.3", "Exhibitor Profiles & Delegate Testimonials (10/ed)", 20, "Film", 800_000, 8_000_000, 0, 8_000_000, 0, 16_000_000)
    pdf.boq_row("13.4", "Ceremony Recap Films & Social Cuts", 2, "Edition", 3_500_000, 3_500_000, 0, 3_500_000, 0, 7_000_000, alt=True)
    pdf.boq_row("13.5", "Post-production: Colour Grading, Sound Design", 2, "Edition", 4_000_000, 4_000_000, 0, 4_000_000, 0, 8_000_000)
    s13_mgmt_total = s13_mgmt_per * 2
    pdf.boq_row("13.6", "Management Fee (15%)", 2, "Edition", s13_mgmt_per, s13_mgmt_per, 0, s13_mgmt_per, 0, s13_mgmt_total)
    pdf.subtotal_line("Section 13 Subtotal:", s13_total, s13_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 14: Local Media Buying (all 34 months, subcontracted)
    # ────────────────────────────────────────────────────────────
    s14_retainer_monthly = 2_200_000
    s14_edition_surge = 22_000_000
    s14_2026 = s14_retainer_monthly * 10 + s14_edition_surge
    s14_2027 = s14_retainer_monthly * 12
    s14_2028 = s14_retainer_monthly * 12 + s14_edition_surge
    s14_sub = s14_2026 + s14_2027 + s14_2028
    s14_mgmt = int(s14_sub * 0.15)
    s14_total = s14_sub + s14_mgmt

    pdf.section_banner("SECTION 14  |  Local Media Buying (Active: All 34 months) - Subcontracted")
    pdf.boq_row("14.1", "Retainer Phase: National Press & Digital Brand-keep", 34, "Month", s14_retainer_monthly, s14_retainer_monthly * 10, s14_retainer_monthly * 12, s14_retainer_monthly * 12, 0, s14_retainer_monthly * 34)
    pdf.boq_row("14.2", "Edition Phase: National TV, Newspaper, Digital Buys", 2, "Edition", s14_edition_surge, s14_edition_surge, 0, s14_edition_surge, 0, s14_edition_surge * 2, alt=True)
    pdf.boq_row("14.3", "Management Fee (15%)", 1, "Lump", s14_mgmt, 0, 0, 0, s14_mgmt, s14_mgmt)
    pdf.subtotal_line("Section 14 Subtotal:", s14_total, s14_mgmt)

    # ────────────────────────────────────────────────────────────
    # SECTION 15: International Media Buying (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s15_sub = 48_000_000
    s15_mgmt_per = int(s15_sub * 0.15)
    s15_total = (s15_sub + s15_mgmt_per) * 2

    pdf.section_banner("SECTION 15  |  International Media Buying (Edition Only) - Subcontracted")
    pdf.boq_row("15.1", "Defence Trade Publications (Jane's, Defense News, etc.)", 2, "Edition", 28_000_000, 28_000_000, 0, 28_000_000, 0, 56_000_000)
    pdf.boq_row("15.2", "Regional Defence Trade Press (ME, APAC, Europe, Africa)", 2, "Edition", 12_000_000, 12_000_000, 0, 12_000_000, 0, 24_000_000, alt=True)
    pdf.boq_row("15.3", "Programmatic International Display Buying", 2, "Edition", 8_000_000, 8_000_000, 0, 8_000_000, 0, 16_000_000)
    s15_mgmt_total = s15_mgmt_per * 2
    pdf.boq_row("15.4", "Management Fee (15%)", 2, "Edition", s15_mgmt_per, s15_mgmt_per, 0, s15_mgmt_per, 0, s15_mgmt_total)
    pdf.subtotal_line("Section 15 Subtotal:", s15_total, s15_mgmt_total)

    # ────────────────────────────────────────────────────────────
    # SECTION 16: Printing & Production (edition only, subcontracted)
    # ────────────────────────────────────────────────────────────
    s16_sub = 14_000_000
    s16_mgmt_per = int(s16_sub * 0.15)
    s16_total = (s16_sub + s16_mgmt_per) * 2

    pdf.section_banner("SECTION 16  |  Printing & Production Allocation (Edition Only) - Subcontracted")
    pdf.boq_row("16.1", "Programmes, Delegate Packs, Press Kits", 2, "Edition", 3_500_000, 3_500_000, 0, 3_500_000, 0, 7_000_000)
    pdf.boq_row("16.2", "Coffee Table Book Printing (from S3 artwork)", 2, "Edition", 3_000_000, 3_000_000, 0, 3_000_000, 0, 6_000_000, alt=True)
    pdf.boq_row("16.3", "Signage, Banners & Large-format Production", 2, "Edition", 4_000_000, 4_000_000, 0, 4_000_000, 0, 8_000_000)
    pdf.boq_row("16.4", "Invitation Cards, VIP Protocol, Exhibitor Welcome Packs", 2, "Edition", 3_500_000, 3_500_000, 0, 3_500_000, 0, 7_000_000, alt=True)
    s16_mgmt_total = s16_mgmt_per * 2
    pdf.boq_row("16.5", "Management Fee (15%)", 2, "Edition", s16_mgmt_per, s16_mgmt_per, 0, s16_mgmt_per, 0, s16_mgmt_total)
    pdf.subtotal_line("Section 16 Subtotal:", s16_total, s16_mgmt_total)

    # ════════════════════════════════════════════════════════════
    # GRAND SUMMARY
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 8, "COST SUMMARY - ALL SECTIONS", new_x="LMARGIN", new_y="NEXT")
    pdf.accent_line()
    pdf.ln(3)

    # Calculate all totals
    section_totals = [
        ("Section 1: Retainer Services (34 months)", s1_total),
        ("Section 2: Event Designing (2 editions)", s2_total),
        ("Section 3: Coffee Table Book (2 editions)", s3_total),
        ("Section 4: International PR (2 editions)", s4_total),
        ("Section 5: Local PR (2 editions)", s5_total),
        ("Section 6: International OOH (2 editions)", s6_total),
        ("Section 7: Pakistan OOH (2 editions)", s7_total),
        ("Section 8: Digital Media Buying (34 months)", s8_total),
        ("Section 9: Local Influencers (2 editions)", s9_total),
        ("Section 10: International Influencers (2 editions)", s10_total),
        ("Section 11: Events Coverage (2 editions)", s11_total),
        ("Section 12: Post-Show Report (2 editions)", s12_total),
        ("Section 13: Cinematic Productions (2 editions)", s13_total),
        ("Section 14: Local Media Buying (34 months)", s14_total),
        ("Section 15: International Media Buying (2 editions)", s15_total),
        ("Section 16: Printing & Production (2 editions)", s16_total),
    ]

    grand_total = sum(t for _, t in section_totals)

    # Summary table
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 6.5)
    pdf.cell(8, 6, "S#", align="C", fill=True)
    pdf.cell(145, 6, "SECTION", fill=True)
    pdf.cell(40, 6, "TOTAL (PKR)", align="R", fill=True)
    pdf.cell(35, 6, "USD EQUIVALENT", align="R", fill=True)
    pdf.cell(30, 6, "% OF TOTAL", align="R", fill=True)
    pdf.ln()

    for i, (label, total) in enumerate(section_totals):
        bg = LIGHT_BG if i % 2 == 0 else WHITE
        pdf.set_fill_color(*bg)
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 6.5)
        pdf.cell(8, 5.5, f"S{i + 1}", align="C", fill=True)
        pdf.cell(145, 5.5, label, fill=True)
        pdf.set_font("Helvetica", "B", 6.5)
        pdf.cell(40, 5.5, fmt(total), align="R", fill=True)
        pdf.set_font("Helvetica", "", 6.5)
        usd_val = total / FX_2026
        pdf.cell(35, 5.5, f"${usd_val:,.0f}", align="R", fill=True)
        pct = (total / grand_total) * 100
        pdf.cell(30, 5.5, f"{pct:.1f}%", align="R", fill=True)
        pdf.ln()

    pdf.ln(2)
    pdf.summary_line("GRAND TOTAL (ALL 16 SECTIONS - EXCLUSIVE OF SALES TAX):", grand_total, highlight=True)
    pdf.ln(1)
    pdf.summary_line(f"USD EQUIVALENT (at PKR {FX_2026}):", 0)
    # Override the last cell
    pdf.set_y(pdf.get_y() - 5.5)
    pdf.set_font("Helvetica", "B", 6.5)
    pdf.set_text_color(*TEAL)
    pdf.cell(225, 5.5, "", align="R")
    usd_grand = grand_total / FX_2026
    pdf.cell(28, 5.5, f"${usd_grand:,.0f}", align="R")
    pdf.ln()

    # ════════════════════════════════════════════════════════════
    # YEAR-WISE BREAKDOWN
    # ════════════════════════════════════════════════════════════
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 7, "YEAR-WISE COST BREAKDOWN", new_x="LMARGIN", new_y="NEXT")
    pdf.accent_line()
    pdf.ln(3)

    # Calculate year-wise totals
    y2026_total = (
        s1_2026 + s2_2026 + s3_agency + s3_mgmt +
        (s4_sub + s4_mgmt_per) + (s5_sub + s5_mgmt_per) +
        (s6_sub_total + s6_mgmt_per) + (s7_sub_total + s7_mgmt_per) +
        s8_2026 + (s9_sub + s9_mgmt_per) + (s10_sub + s10_mgmt_per) +
        s11_per + s12_per + (s13_sub + s13_mgmt_per) +
        s14_2026 + (s15_sub + s15_mgmt_per) + (s16_sub + s16_mgmt_per)
    )
    y2027_total = s1_2027 + s8_2027 + s14_2027
    y2028_total = (
        s1_2028 + s2_2028 + s3_agency + s3_mgmt +
        (s4_sub + s4_mgmt_per) + (s5_sub + s5_mgmt_per) +
        (s6_sub_total + s6_mgmt_per) + (s7_sub_total + s7_mgmt_per) +
        s8_2028 + (s9_sub + s9_mgmt_per) + (s10_sub + s10_mgmt_per) +
        s11_per + s12_per + (s13_sub + s13_mgmt_per) +
        s14_2028 + (s15_sub + s15_mgmt_per) + (s16_sub + s16_mgmt_per)
    )

    year_data = [
        ("2026 (Mar-Dec)", "10 months - Retainer + IDEAS 2026 Edition", y2026_total, FX_2026),
        ("2027 (Jan-Dec)", "12 months - Retainer Only (no edition)", y2027_total, FX_2027),
        ("2028 (Jan-Dec)", "12 months - Retainer + IDEAS 2028 Edition", y2028_total, FX_2028),
    ]

    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(40, 6, "YEAR", fill=True, align="C")
    pdf.cell(100, 6, "DESCRIPTION", fill=True)
    pdf.cell(45, 6, "AMOUNT (PKR)", fill=True, align="R")
    pdf.cell(35, 6, "USD EQUIVALENT", fill=True, align="R")
    pdf.ln()

    for i, (year, desc, amount, fx) in enumerate(year_data):
        bg = LIGHT_BG if i % 2 == 0 else WHITE
        pdf.set_fill_color(*bg)
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "B", 7)
        pdf.cell(40, 6, year, fill=True, align="C")
        pdf.set_font("Helvetica", "", 7)
        pdf.cell(100, 6, desc, fill=True)
        pdf.set_font("Helvetica", "B", 7)
        pdf.cell(45, 6, fmt(amount), fill=True, align="R")
        pdf.set_font("Helvetica", "", 7)
        pdf.cell(35, 6, f"${amount / fx:,.0f}", fill=True, align="R")
        pdf.ln()

    pdf.set_fill_color(*TEAL)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(40, 6, "TOTAL", fill=True, align="C")
    pdf.cell(100, 6, "34-Month Contract", fill=True)
    pdf.cell(45, 6, fmt(y2026_total + y2027_total + y2028_total), fill=True, align="R")
    pdf.cell(35, 6, f"${(y2026_total + y2027_total + y2028_total) / FX_2026:,.0f}", fill=True, align="R")
    pdf.ln()

    # ════════════════════════════════════════════════════════════
    # RATE CARD (ANNEX B)
    # ════════════════════════════════════════════════════════════
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 7, "ANNEX B: RATE CARD - OUT-OF-SCOPE VARIATIONS", new_x="LMARGIN", new_y="NEXT")
    pdf.accent_line()
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*DARK)
    pdf.multi_cell(250, 4, "The following rates apply to out-of-scope work requested by DEPO under the +/-15% variation mechanism or formal contract amendments. All rates are in PKR, exclusive of applicable sales tax.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Rate card table
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 6.5)
    pdf.cell(8, 6, "#", fill=True, align="C")
    pdf.cell(70, 6, "ROLE / DELIVERABLE", fill=True)
    pdf.cell(35, 6, "HOURLY RATE (PKR)", fill=True, align="R")
    pdf.cell(35, 6, "DAY RATE (PKR)", fill=True, align="R")
    pdf.cell(40, 6, "PER-UNIT RATE (PKR)", fill=True, align="R")
    pdf.cell(55, 6, "NOTES", fill=True)
    pdf.ln()

    rates = [
        ("1", "Account Director", "15,000", "100,000", "-", "Senior strategic oversight"),
        ("2", "Creative Director", "12,000", "85,000", "-", "Campaign-level creative"),
        ("3", "Strategy & Content Lead", "10,000", "70,000", "-", "Planning & content"),
        ("4", "Senior Designer", "7,000", "50,000", "-", "OOH, print, digital"),
        ("5", "Social Media Manager", "6,000", "42,000", "-", "Platform management"),
        ("6", "Junior Designer / Copywriter", "4,000", "28,000", "-", "Support roles"),
        ("7", "Additional Press Release", "-", "-", "120,000", "Per release, EN or UR"),
        ("8", "Additional Social Post (designed)", "-", "-", "25,000", "Per post, single platform"),
        ("9", "Additional Motion Graphic", "-", "-", "180,000", "Up to 30 seconds"),
        ("10", "Additional OOH Site (Pakistan)", "-", "-", "350,000", "Per site, per month"),
        ("11", "Additional OOH Site (International)", "-", "-", "2,500,000", "Per site, per month (avg)"),
        ("12", "Additional Translation Document", "-", "-", "45,000", "Per document, any language"),
        ("13", "Video Production (crew + equipment)", "-", "450,000", "-", "Full crew, per shoot day"),
        ("14", "Post-production (editing, grading)", "-", "120,000", "-", "Per day, per editor"),
        ("15", "Third-party Vendor Markup", "-", "-", "15%", "On all out-of-scope vendors"),
    ]

    for i, (num, desc, hourly, daily, unit, notes) in enumerate(rates):
        bg = LIGHT_BG if i % 2 == 0 else WHITE
        pdf.set_fill_color(*bg)
        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 6)
        pdf.cell(8, 5, num, fill=True, align="C")
        pdf.set_font("Helvetica", "B" if i < 6 else "", 6)
        pdf.cell(70, 5, desc, fill=True)
        pdf.set_font("Helvetica", "", 6)
        pdf.cell(35, 5, hourly, fill=True, align="R")
        pdf.cell(35, 5, daily, fill=True, align="R")
        pdf.cell(40, 5, unit, fill=True, align="R")
        pdf.set_font("Helvetica", "", 5.5)
        pdf.cell(55, 5, notes, fill=True)
        pdf.ln()

    # ════════════════════════════════════════════════════════════
    # PAYMENT TERMS & NOTES
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 7, "PAYMENT TERMS", new_x="LMARGIN", new_y="NEXT")
    pdf.accent_line()
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, "Monthly Retainer (Section 1):", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4.5, "Monthly invoicing; payment within 30 days of invoice receipt.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, "Edition Activation (Sections 2-7, 9-13, 15-16):", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4.5, "30% advance upon signing of edition work order", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4.5, "40% at mid-point (T-2 months before edition)", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4.5, "30% within 30 days of edition close and post-show report acceptance", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, "Media Buying (Sections 8, 14):", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4.5, "Pass-through costs supported by third-party invoices; payment upon receipt of vendor invoices.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, "Performance Bond:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4.5, "5% of annual contract value as bank guarantee from a scheduled Pakistani bank.", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 7, "NOTES & ASSUMPTIONS", new_x="LMARGIN", new_y="NEXT")
    pdf.accent_line()
    pdf.ln(3)

    notes = [
        "1.  All prices are in Pakistani Rupees (PKR), exclusive of applicable sales tax.",
        "2.  USD equivalents are provided for reference only using planning rates: 2026 = PKR 279.5, 2027 = PKR 290, 2028 = PKR 300.",
        "3.  Exchange rate risk on international spend (Sections 6, 10, 15) is borne by the agency as per RFP Section 6.2.",
        "4.  15% management fee is applied to all subcontracted sections as specified in the RFP (Sections 3-10, 13-16).",
        "5.  Media buying costs (Sections 6, 7, 8, 14, 15) include both media spend and agency planning/buying fees.",
        "6.  Tier 3 international OOH sites (Section 6.3) are included as optional; DEPO may activate or exclude per edition.",
        "7.  Aspirational OOH sites (Burj Khalifa, Times Square, Piccadilly Circus) are NOT included; pricing available on request.",
        "8.  Drone operations costs assume approval is granted; alternative elevated methods at same cost if denied.",
        "9.  IDEAS 2028 pricing assumes equivalent scope to 2026; actual costs may vary with confirmed dates and scope.",
        "10. This quotation is valid for 90 days from the submission deadline.",
        "11. Withholding tax deductions will be applied per Pakistani tax law.",
        "12. Quantities may vary +/-15% per the RFP variation mechanism (Section 3.3) at disclosed rate card rates.",
    ]

    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*GRAY)
    for note in notes:
        pdf.multi_cell(250, 4.5, note, new_x="LMARGIN", new_y="NEXT")

    # Signature
    pdf.ln(8)
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.3)
    pdf.line(8, pdf.get_y(), 70, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, "ADEEL AHMED - DIRECTOR", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, "Miradore Experiences", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4, "Authorised Signatory  |  March 2026", new_x="LMARGIN", new_y="NEXT")

    # ── Output ──
    out_path = os.path.join(os.path.dirname(__file__), "IDEAS_2026_Financial_Proposal_BOQ_Miradore.pdf")
    pdf.output(out_path)
    print(f"Financial Proposal PDF generated: {out_path}")
    print(f"\nGrand Total: PKR {grand_total:,.0f}")
    print(f"USD Equivalent: ${grand_total / FX_2026:,.0f}")


if __name__ == "__main__":
    generate_financial()
