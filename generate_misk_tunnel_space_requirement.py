"""Space and services requirement sheet for the Misk Art Week 2026 tunnel.

A one page document PLOP Makers can hand to the venue to reserve floor
space and services. Geometry is derived, not estimated: the tunnel run is
set by the screen inventory released from the immersive room package.
"""

import math
import os
from fpdf import FPDF

BASE = os.path.dirname(os.path.abspath(__file__))

CLIENT = "PLOP Makers"
REF = "MRD-SR-2026-1007"
DOC_DATE = "07 October 2026"
RELATED_QUOTE = "MRD-QT-2026-1006"

# ---- geometry ----------------------------------------------------------
# Arch cross-section: vertical walls to height HW, then a semicircular
# crown of radius W/2. Screen wraps walls and crown; visitors walk on the
# existing floor. No LED floor is the conservative case for reserving
# space: it consumes the least screen per metre, so gives the longest run.
W_INT, HW = 3.0, 1.7                 # internal clear width, wall height
R = W_INT / 2                        # crown radius
H_INT = HW + R                       # internal clear height at centre
SCREEN_PER_M = 2 * HW + math.pi * R  # m2 of screen per linear metre

STRUCT_DEPTH = 0.50                  # frame + cabinet + service void, each side
ACCESS = 1.00                        # working clearance each side
END_CLEAR = 3.00                     # approach / crowd management, each end

W_EXT = W_INT + 2 * STRUCT_DEPTH
W_RESERVE = W_EXT + 2 * ACCESS

# Compact fallback, for a constrained hall
W_INT_C, HW_C = 2.4, 1.6
SCREEN_PER_M_C = 2 * HW_C + math.pi * (W_INT_C / 2)


def sizing(run_m):
    """Screen area needed and footprint to reserve, for a given tunnel run."""
    return run_m * SCREEN_PER_M, W_RESERVE, run_m + 2 * END_CLEAR


CASES = [("Minimum", 12), ("Typical", 22), ("Maximum", 31)]
HEADLINE_RUN = 31

SERVICES = [
    ("Electrical supply",
     "Three phase 125 A at 400 V at the stand. 100 A minimum for the smaller configuration."),
    ("Clear height",
     "4.0 m minimum to the underside of all services, rigging and lighting bars."),
    ("Floor loading",
     "Venue to confirm the rating in kN/m2. Load is concentrated through base plates and ballast."),
    ("Load in",
     "Door and route to accept structural steel and palletised LED cabinets. Vehicle access preferred."),
    ("Emergency egress",
     "Venue to confirm maximum travel distance. A mid point exit may be required on runs over 25 m."),
    ("Build and strike",
     "Access from 01 December for build, and from 11 December for dismantle."),
]

NOTES = [
    "1.  The footprint includes 1.0 m working clearance to each side for build and in-run maintenance, and "
    "3.0 m clear at each end for approach and crowd management.",
    "2.  The tunnel run is set by the screen inventory released from the immersive room package. Final "
    "dimensions are confirmed against the cabinet schedule.",
    "3.  A narrower cross-section consumes screen more slowly and therefore produces a longer run. Where floor "
    "space is constrained, the wider cross-section is preferred.",
    "4.  Where a straight run will not fit the hall, the same tunnel folds into an L or a horseshoe. A 31 m run "
    "folds into approximately 13.0 x 16.5 m for a comparable area.",
    "5.  Reserve the maximum. Space can be released closer to the event; additional space cannot be secured in "
    "build week.",
    "6.  Dimensions assume an indoor location. An outdoor position requires weather protection and a different "
    "structure.",
]


class SheetPDF(FPDF):
    TEAL = (0, 128, 128)
    ORANGE = (230, 100, 30)
    DARK = (40, 40, 40)
    GRAY = (100, 100, 100)
    LIGHT_BG = (245, 248, 250)
    WHITE = (255, 255, 255)
    SECTION_BG = (230, 243, 243)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(
            0, 10,
            f"Page {self.page_no()}/{{nb}}  |  Miradore Experiences Company, Riyadh, KSA  |  Confidential",
            align="C",
        )

    def add_logo_header(self):
        logo = os.path.join(BASE, "Miradore Logo Color.png")
        if os.path.exists(logo):
            self.image(logo, x=15, y=12, w=55)
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

    def accent(self, width=0.8):
        self.set_draw_color(*self.TEAL)
        self.set_line_width(width)
        self.line(15, self.get_y() + 2, 195, self.get_y() + 2)
        self.ln(6)

    def rule(self, width=0.2):
        self.set_draw_color(*self.TEAL)
        self.set_line_width(width)
        self.line(15, self.get_y(), 195, self.get_y())

    def section(self, title):
        self.set_fill_color(*self.SECTION_BG)
        self.set_text_color(*self.TEAL)
        self.set_font("Helvetica", "B", 7.5)
        self.cell(180, 5.5, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")

    def signature(self):
        if self.get_y() > 248:
            self.add_page()
        y = self.get_y()
        sig = os.path.join(BASE, "adeel_signature-removebg-preview.png")
        if os.path.exists(sig):
            self.image(sig, x=16, y=y, w=42)
        stamp = os.path.join(BASE, "miradore_stamp_teal.png")
        if os.path.exists(stamp):
            self.image(stamp, x=78, y=y - 2, w=46)
        self.set_y(y + 17)
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
    pdf = SheetPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(15, 12, 15)
    pdf.add_page()

    pdf.add_logo_header()

    # ---- title ----
    pdf.set_y(33)
    pdf.accent()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 8, "SPACE AND SERVICES REQUIREMENT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*pdf.ORANGE)
    pdf.cell(0, 6, "IMMERSIVE TUNNEL  -  MISK ART WEEK 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*pdf.GRAY)
    pdf.cell(0, 5, "05 - 10 DECEMBER 2026, RIYADH", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(0.5)
    pdf.accent()

    # ---- info ----
    top = pdf.get_y()
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(90, 5, "PREPARED FOR:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(90, 5, f"{CLIENT}  -  for venue reservation", new_x="LMARGIN", new_y="NEXT")
    for label, value in (("REFERENCE:", REF), ("DATE:", DOC_DATE)):
        pdf.set_xy(110, top)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*pdf.TEAL)
        pdf.cell(85, 5, label, align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(110, top + 5)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*pdf.DARK)
        pdf.cell(85, 5, value, align="R", new_x="LMARGIN", new_y="NEXT")
        top += 10
    pdf.set_y(max(pdf.get_y(), top))
    pdf.ln(3)

    # ---- headline ----
    _, w_res, len_res = sizing(HEADLINE_RUN)
    pdf.set_fill_color(*pdf.TEAL)
    pdf.set_text_color(*pdf.WHITE)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(80, 9, "   SPACE TO RESERVE", fill=True)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(100, 9, f"{w_res:.1f} m  x  {len_res:.0f} m     =     {w_res * len_res:.0f} m2   ",
             align="R", fill=True)
    pdf.ln(11)

    # ---- sizing options ----
    pdf.section("TUNNEL SIZE OPTIONS")
    pdf.ln(1.5)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*pdf.TEAL)
    for w, t, a in ((38, "CONFIGURATION", "L"), (28, "TUNNEL RUN", "R"),
                    (36, "SCREEN REQUIRED", "R"), (46, "FOOTPRINT TO RESERVE", "R"),
                    (32, "AREA", "R")):
        pdf.cell(w, 6, t, align=a)
    pdf.ln()
    pdf.rule(0.2)
    pdf.ln(1)

    for i, (name, run) in enumerate(CASES):
        screen, w_res, l_res = sizing(run)
        highlight = name == "Maximum"
        pdf.set_fill_color(*(pdf.SECTION_BG if highlight else (pdf.LIGHT_BG if i % 2 else pdf.WHITE)))
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*(pdf.TEAL if highlight else pdf.DARK))
        pdf.cell(38, 6.5, f"  {name}", align="L", fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*pdf.DARK)
        pdf.cell(28, 6.5, f"{run} m", align="R", fill=True)
        pdf.cell(36, 6.5, f"{screen:.0f} m2", align="R", fill=True)
        pdf.cell(46, 6.5, f"{w_res:.1f} x {l_res:.0f} m", align="R", fill=True)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*(pdf.TEAL if highlight else pdf.DARK))
        pdf.cell(32, 6.5, f"{w_res * l_res:.0f} m2  ", align="R", fill=True)
        pdf.ln()

    pdf.ln(1)
    pdf.rule(0.2)
    pdf.ln(2)

    # ---- cross section ----
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(32, 4.5, "Cross-section.")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    pdf.multi_cell(
        148, 4.5,
        f"Arched walk-through, {W_INT:.1f} m internal clear width by {H_INT:.1f} m internal clear height "
        f"(vertical walls to {HW:.1f} m, then a semicircular crown of {R:.2f} m radius). Screen wraps the walls "
        f"and crown at {SCREEN_PER_M:.1f} m2 per linear metre. Clear width stays above 2.8 m at head height. "
        f"External structure width {W_EXT:.1f} m. A {W_INT_C:.1f} x {HW_C + W_INT_C / 2:.1f} m section is "
        f"available where the hall is tight, but consumes only {SCREEN_PER_M_C:.1f} m2 per metre and so runs "
        f"about 16% longer for the same screens.",
        align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ---- services ----
    pdf.section("SERVICES TO RESERVE")
    pdf.ln(1.5)
    for i, (item, spec) in enumerate(SERVICES):
        pdf.set_fill_color(*(pdf.LIGHT_BG if i % 2 else pdf.WHITE))
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(*pdf.DARK)
        pdf.cell(44, 6, f"  {item}", align="L", fill=True)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(*pdf.GRAY)
        pdf.cell(136, 6, spec, align="L", fill=True)
        pdf.ln()
    pdf.ln(3)

    # ---- notes ----
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(*pdf.TEAL)
    pdf.cell(0, 5.5, "NOTES", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*pdf.GRAY)
    for note in NOTES:
        pdf.multi_cell(180, 4.0, note, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.signature()

    out = os.path.join(BASE, "MISK_Art_Week_2026_Tunnel_Space_Requirement.pdf")
    pdf.output(out)
    print(f"PDF generated: {out}")

    # ---- reference table for internal use ----
    csv = os.path.join(BASE, "MISK_Art_Week_2026_Tunnel_Space_Requirement.csv")
    with open(csv, "w", encoding="utf-8") as f:
        f.write("MIRADORE EXPERIENCES COMPANY - SPACE AND SERVICES REQUIREMENT\n")
        f.write(f"Reference,{REF}\nDate,{DOC_DATE}\nPrepared for,{CLIENT}\n")
        f.write("Event,Misk Art Week 2026 (05 - 10 December 2026)\n")
        f.write(f"Related quotation,{RELATED_QUOTE}\n\n")
        f.write(f"Cross-section,{W_INT} m wide x {H_INT} m high,"
                f"{SCREEN_PER_M:.2f} m2 screen per linear metre\n\n")
        f.write("Configuration,Tunnel run m,Screen required m2,Reserve width m,Reserve length m,Reserve area m2\n")
        for name, run in CASES:
            screen, w_res, l_res = sizing(run)
            f.write(f"{name},{run},{screen:.0f},{w_res:.1f},{l_res:.0f},{w_res * l_res:.0f}\n")
        f.write("\nServices to reserve,\n")
        for item, spec in SERVICES:
            f.write(f'"{item}","{spec}"\n')
    print(f"CSV generated: {csv}")


if __name__ == "__main__":
    generate()
