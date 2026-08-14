#!/usr/bin/env python3
"""
Marsal - Brand Evolution Proposal
Prepared by Miradore Experiences, Riyadh

Miradore design language: teal primary, orange accent, Helvetica,
hairline rules, generous whitespace.
"""

from fpdf import FPDF
import os
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASE, "Miradore Logo Color.png")


def reversed_logo():
    """Knock the Miradore mark out in white for use on the teal cover band."""
    if not os.path.exists(LOGO):
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    img = Image.open(LOGO).convert("RGBA")
    img.putdata([
        (255, 255, 255, a if a else (0 if (r > 240 and g > 240 and b > 240) else 255))
        for (r, g, b, a) in img.getdata()
    ])
    out = os.path.join(tempfile.gettempdir(), "miradore_logo_reversed.png")
    img.save(out)
    return out

# ── Brand palette (Miradore) ───────────────────────────────────
TEAL = (0, 128, 128)
TEAL_MID = (94, 172, 172)
TEAL_SOFT = (196, 223, 223)
TEAL_TINT = (238, 246, 246)
ORANGE = (230, 100, 30)
ORANGE_SOFT = (250, 226, 212)
DARK = (38, 42, 45)
GRAY = (108, 116, 120)
LIGHT = (168, 176, 180)
HAIRLINE = (222, 228, 230)
PAPER = (248, 250, 251)
WHITE = (255, 255, 255)
NAVY = (20, 40, 65)

# ── Layout grid ────────────────────────────────────────────────
ML = 18          # left margin
MR = 192         # right edge
CW = MR - ML     # content width = 174

# ── Commercials ────────────────────────────────────────────────
FEE = 24000
INCLUDE_VAT = True      # KSA 15% shown as a separate line (house convention)
VAT_RATE = 0.15


class Proposal(FPDF):
    show_chrome = True

    # ── Page furniture ──
    def header(self):
        if not self.show_chrome:
            return
        if os.path.exists(LOGO):
            self.image(LOGO, x=ML, y=10, w=26)
        self.set_xy(100, 12)
        self.set_font("Helvetica", "", 6.5)
        self.set_text_color(*LIGHT)
        self.cell(MR - 100, 4, "BRAND EVOLUTION  /  MARSAL", align="R")
        self.set_draw_color(*HAIRLINE)
        self.set_line_width(0.2)
        self.line(ML, 21, MR, 21)
        self.set_y(32)

    def footer(self):
        if not self.show_chrome or self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_draw_color(*HAIRLINE)
        self.set_line_width(0.2)
        self.line(ML, self.get_y(), MR, self.get_y())
        self.ln(1.5)
        self.set_font("Helvetica", "", 6.5)
        self.set_text_color(*LIGHT)
        self.set_x(ML)
        self.cell(CW / 2, 4, "Miradore Experiences  /  Riyadh")
        self.cell(CW / 2, 4, f"{self.page_no():02d}", align="R")

    # ── Space management ──
    def need(self, h):
        if self.get_y() + h > 268:
            self.add_page()

    # ── Typographic components ──
    def section(self, num, title, kicker=None):
        """Oversized ghost numeral + title + hairline. Airy, not boxed."""
        self.need(34)
        y = self.get_y()
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(*TEAL_SOFT)
        self.set_xy(ML, y - 2)
        self.cell(18, 12, num)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*DARK)
        self.set_xy(ML + 18, y)
        self.cell(CW - 18, 8, title, new_x="LMARGIN", new_y="NEXT")
        if kicker:
            self.set_xy(ML + 18, self.get_y())
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*GRAY)
            self.cell(CW - 18, 5, kicker, new_x="LMARGIN", new_y="NEXT")
        self.ln(2.5)
        self.set_draw_color(*TEAL)
        self.set_line_width(0.5)
        self.line(ML, self.get_y(), ML + 22, self.get_y())
        self.set_draw_color(*HAIRLINE)
        self.set_line_width(0.2)
        self.line(ML + 22, self.get_y(), MR, self.get_y())
        self.ln(6)

    def lead(self, text):
        self.need(16)
        self.set_x(ML)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(CW, 5.6, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def body(self, text, w=None, size=8.6, color=None, lh=4.9):
        self.need(10)
        self.set_x(ML)
        self.set_font("Helvetica", "", size)
        self.set_text_color(*(color or GRAY))
        self.multi_cell(w or CW, lh, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2.5)

    def note_line(self, label, text):
        self.need(9)
        self.set_x(ML)
        self.set_font("Helvetica", "B", 8.2)
        self.set_text_color(*TEAL)
        w = self.get_string_width(label) + 2
        self.cell(w, 4.8, label)
        self.set_font("Helvetica", "", 8.2)
        self.set_text_color(*GRAY)
        self.multi_cell(CW - w, 4.8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1.5)

    def bullet(self, text, indent=0, size=8.2, lh=4.6):
        self.need(8)
        x = ML + 4 + indent
        self.set_draw_color(*TEAL_MID)
        self.set_fill_color(*TEAL_MID)
        self.rect(x, self.get_y() + 1.7, 1.3, 1.3, "F")
        self.set_xy(x + 4, self.get_y())
        self.set_font("Helvetica", "", size)
        self.set_text_color(*GRAY)
        self.multi_cell(CW - 8 - indent, lh, text, new_x="LMARGIN", new_y="NEXT")

    def phase_head(self, tag, title, meta=None):
        self.need(14)
        y = self.get_y()
        self.set_fill_color(*TEAL_TINT)
        self.rect(ML, y, CW, 7.4, "F", round_corners=True, corner_radius=1.2)
        self.set_xy(ML + 3, y + 0.4)
        self.set_font("Helvetica", "B", 7.2)
        self.set_text_color(*ORANGE)
        self.cell(16, 6.6, tag)
        self.set_font("Helvetica", "B", 8.6)
        self.set_text_color(*TEAL)
        self.cell(CW - 60, 6.6, title)
        if meta:
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*TEAL_MID)
            self.cell(38, 6.6, meta, align="R")
        self.set_xy(ML, y + 7.4)
        self.ln(2.5)

    def numbered_point(self, num, head, text):
        self.need(22)
        y = self.get_y()
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*ORANGE)
        self.set_xy(ML, y)
        self.cell(10, 5, num)
        self.set_font("Helvetica", "B", 9.4)
        self.set_text_color(*DARK)
        self.set_xy(ML + 10, y)
        self.cell(CW - 10, 5, head, new_x="LMARGIN", new_y="NEXT")
        self.set_xy(ML + 10, self.get_y() + 1)
        self.set_font("Helvetica", "", 8.4)
        self.set_text_color(*GRAY)
        self.multi_cell(CW - 10, 4.8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def rule(self, soft=True, gap=4):
        self.ln(gap)
        self.set_draw_color(*(HAIRLINE if soft else TEAL))
        self.set_line_width(0.2 if soft else 0.4)
        self.line(ML, self.get_y(), MR, self.get_y())
        self.ln(gap)


# ═══════════════════════════════════════════════════════════════
def build():
    p = Proposal(orientation="P", unit="mm", format="A4")
    p.set_auto_page_break(auto=True, margin=20)
    p.set_title("Marsal - Brand Evolution Proposal")
    p.set_author("Miradore Experiences")

    # ───────────────────────────────────────────── COVER
    p.show_chrome = False
    p.add_page()

    p.set_fill_color(*TEAL)
    p.rect(0, 0, 210, 108, "F")
    p.set_fill_color(*ORANGE)
    p.rect(0, 108, 210, 2.4, "F")

    rev = reversed_logo()
    if rev:
        p.image(rev, x=ML, y=18, w=42)
    elif os.path.exists(LOGO):
        p.image(LOGO, x=ML, y=18, w=42)

    p.set_xy(ML, 52)
    p.set_font("Helvetica", "", 8)
    p.set_text_color(*ORANGE_SOFT)
    p.cell(CW, 5, "A PROPOSAL FOR", new_x="LMARGIN", new_y="NEXT")
    p.set_x(ML)
    p.set_font("Helvetica", "B", 34)
    p.set_text_color(*WHITE)
    p.cell(CW, 16, "MARSAL", new_x="LMARGIN", new_y="NEXT")
    p.set_x(ML)
    p.set_font("Helvetica", "", 14)
    p.set_text_color(255, 232, 214)
    p.cell(CW, 9, "Brand Evolution, Bilingual Identity System", new_x="LMARGIN", new_y="NEXT")
    p.set_x(ML)
    p.cell(CW, 9, "and Extended Collateral", new_x="LMARGIN", new_y="NEXT")

    # Details, set low and quiet
    p.set_y(132)
    rows = [
        ("Prepared for", "Marsal  /  Logistics & Transport"),
        ("Prepared by", "Miradore Experiences, Riyadh"),
        ("Date", "14 August 2026"),
        ("Delivery", "Monday, 24 August 2026"),
        ("Investment", f"SAR {FEE:,}"),
        ("Validity", "30 days from date of issue"),
    ]
    for label, value in rows:
        p.set_x(ML)
        p.set_font("Helvetica", "", 7.4)
        p.set_text_color(*LIGHT)
        p.cell(34, 7, label.upper())
        p.set_font("Helvetica", "B", 9)
        p.set_text_color(*DARK)
        p.cell(CW - 34, 7, value, new_x="LMARGIN", new_y="NEXT")

    p.set_y(192)
    p.set_draw_color(*HAIRLINE)
    p.set_line_width(0.2)
    p.line(ML, p.get_y(), MR, p.get_y())

    p.set_y(204)
    p.set_x(ML)
    p.set_font("Helvetica", "", 10)
    p.set_text_color(*GRAY)
    p.multi_cell(
        CW - 30, 5.6,
        "Marsal does not need a new logo. It needs the one it already owns to work "
        "at 32 pixels, in one colour, in two languages, and in the hands of people "
        "who are not designers. That is the whole brief.",
        new_x="LMARGIN", new_y="NEXT",
    )

    p.set_y(262)
    p.set_x(ML)
    p.set_font("Helvetica", "B", 7.4)
    p.set_text_color(*TEAL)
    p.cell(CW / 2, 4, "MIRADORE EXPERIENCES")
    p.set_font("Helvetica", "", 7.4)
    p.set_text_color(*LIGHT)
    p.cell(CW / 2, 4, "www.miradore.co  /  hello@miradore.co", align="R")
    p.set_x(ML)
    p.ln(4)
    p.set_font("Helvetica", "", 7.4)
    p.set_text_color(*LIGHT)
    p.cell(CW, 4, "Riyadh, Kingdom of Saudi Arabia  /  Confidential")

    # ───────────────────────────────────────────── LETTER
    p.show_chrome = True
    p.add_page()

    p.set_x(ML)
    p.set_font("Helvetica", "", 7.6)
    p.set_text_color(*LIGHT)
    p.cell(CW, 5, "RIYADH  /  14 AUGUST 2026", new_x="LMARGIN", new_y="NEXT")
    p.ln(6)
    p.set_x(ML)
    p.set_font("Helvetica", "B", 15)
    p.set_text_color(*DARK)
    p.cell(CW, 9, "To the team at Marsal,", new_x="LMARGIN", new_y="NEXT")
    p.ln(4)

    for para in [
        "Thank you for the call last week, and for sending across the logo files. We have spent "
        "a few days with them, put them through the places they actually have to live, and this "
        "proposal is what came out of that.",

        "The short version: you do not need a new logo. The one you have is doing its job, and "
        "there is real equity in it already sitting on your paperwork, your vehicles and your "
        "invoices. Redrawing it would be an expensive way to solve a problem you do not have.",

        "What you do need is for that logo to work harder in the places it currently struggles. "
        "It has no short form, so there is nothing clean to put in a profile picture or an app "
        "icon. And when the Arabic and the English sit together, the signature runs wide and low "
        "- which is why it keeps getting shrunk into illegibility on cards, on nav bars, and on "
        "the side of a truck.",

        "So the work here is evolution, not replacement. We pull a proper logomark out of the "
        "identity you already own. We consolidate the bilingual signature so Arabic and Latin "
        "hold equal weight in a footprint that fits. Then we build out the everyday pieces - "
        "cards, letterhead, profile pictures, social templates, the website - so the next hundred "
        "things Marsal produces look like they came from the same company, without anyone having "
        "to ask us first.",

        "We have scoped this to nine working days. Everything lands with you on Monday 24 August, "
        "with two review points along the way so there are no surprises at the end.",

        "If any part of this reads as more, or less, than what you had in mind, tell us and we "
        "will reshape it. We would much rather adjust the scope now than hand you something you "
        "have to explain internally.",
    ]:
        p.set_x(ML)
        p.set_font("Helvetica", "", 9.2)
        p.set_text_color(*GRAY)
        p.multi_cell(CW - 12, 5.4, para, new_x="LMARGIN", new_y="NEXT")
        p.ln(3.2)

    p.ln(6)
    p.set_x(ML)
    p.set_font("Helvetica", "", 9.2)
    p.set_text_color(*GRAY)
    p.cell(CW, 5, "Warm regards,", new_x="LMARGIN", new_y="NEXT")
    p.ln(8)
    p.set_draw_color(*TEAL)
    p.set_line_width(0.4)
    p.line(ML, p.get_y(), ML + 46, p.get_y())
    p.ln(2)
    p.set_x(ML)
    p.set_font("Helvetica", "B", 9)
    p.set_text_color(*DARK)
    p.cell(CW, 5, "Adeel Ahmed", new_x="LMARGIN", new_y="NEXT")
    p.set_x(ML)
    p.set_font("Helvetica", "", 7.8)
    p.set_text_color(*LIGHT)
    p.cell(CW, 4, "Director  /  Miradore Experiences", new_x="LMARGIN", new_y="NEXT")

    # ───────────────────────────────────────────── CONTENTS + THE READ
    p.add_page()

    p.set_x(ML)
    p.set_font("Helvetica", "B", 8)
    p.set_text_color(*TEAL)
    p.cell(CW, 5, "CONTENTS", new_x="LMARGIN", new_y="NEXT")
    p.ln(2)

    toc = [
        ("01", "Where the identity stands today", "03"),
        ("02", "What we are proposing", "04"),
        ("03", "Scope of work, phase by phase", "05"),
        ("04", "Delivery schedule", "07"),
        ("05", "Investment and terms", "08"),
        ("06", "What we need from Marsal", "09"),
    ]
    for num, title, pg in toc:
        p.set_x(ML)
        p.set_font("Helvetica", "B", 8)
        p.set_text_color(*TEAL_SOFT)
        p.cell(10, 6.2, num)
        p.set_font("Helvetica", "", 8.6)
        p.set_text_color(*DARK)
        p.cell(CW - 22, 6.2, title)
        p.set_font("Helvetica", "", 7.6)
        p.set_text_color(*LIGHT)
        p.cell(12, 6.2, pg, align="R", new_x="LMARGIN", new_y="NEXT")

    p.ln(8)
    p.section("01", "Where the identity stands today",
              "An honest read of the current logo, and the three things holding it back")

    p.body(
        "This is not a criticism of the mark. It is a list of the jobs it is being asked to do "
        "that it was never drawn to do. All three are fixable without losing anything you have "
        "already built."
    )
    p.ln(1)

    p.numbered_point(
        "01", "There is no short form",
        "Every strong logistics brand has two assets: a full signature for documents and "
        "letterhead, and a compact mark for everything else. Marsal currently has only the first. "
        "That means a profile picture becomes a squeezed wordmark, an app icon is not possible, "
        "and there is nothing to stitch onto a uniform, cut into vinyl for a vehicle door, or "
        "stamp onto a seal. Anything below about 25 mm wide simply stops reading."
    )
    p.numbered_point(
        "02", "The bilingual lockup runs too wide",
        "Placed side by side, the Arabic and English signature becomes long and shallow. In a "
        "business card corner, a website navigation bar or a truck panel, the only way to fit it "
        "is to scale it down until neither language is legible. The two scripts also carry "
        "different optical weights, so one visually dominates the other depending on the size."
    )
    p.numbered_point(
        "03", "Collateral is being made one piece at a time",
        "Without an agreed system for colour, type and spacing, every new card, post or document "
        "is a fresh set of decisions. It is slower, it costs more over a year, and the drift shows "
        "- especially to the enterprise clients and government tenders where consistency is read "
        "as operational discipline."
    )

    # ───────────────────────────────────────────── THE PROPOSAL
    p.add_page()
    p.section("02", "What we are proposing",
              "Three moves. Everything else in this document follows from them.")

    # ── A. The logomark
    p.phase_head("A", "A logomark drawn out of the logo you already own")
    p.body(
        "We do not start with a blank page. We take the existing Marsal logo apart, find the one "
        "element carrying the most recognition, and develop it into a mark that stands alone. It "
        "must survive four tests before we present it: legible at 16 pixels, readable in a single "
        "colour, cuttable in vinyl without detail loss, and distinct from the other logistics "
        "marks operating in the Kingdom. You will see three routes; we develop the one you choose."
    )

    # Scale demo strip - shows the mark working down in size
    y = p.get_y() + 1
    p.set_font("Helvetica", "", 6.6)
    sizes = [(20, "512 px"), (13, "128 px"), (8.5, "64 px"), (5.5, "32 px"), (3.6, "16 px")]
    x = ML + 2
    for s, label in sizes:
        p.set_draw_color(*TEAL_SOFT)
        p.set_line_width(0.25)
        p.set_fill_color(*TEAL_TINT)
        p.rect(x, y + (20 - s), s, s, "DF", round_corners=True, corner_radius=0.8)
        p.set_text_color(*LIGHT)
        p.set_xy(x - 2, y + 22)
        p.cell(s + 4, 4, label, align="C")
        x += s + 9
    p.set_xy(ML + 118, y + 3)
    p.set_font("Helvetica", "", 7.6)
    p.set_text_color(*GRAY)
    p.multi_cell(CW - 118, 4.4,
                 "The mark is tested at every size it will actually be used at, not just the size "
                 "it is designed at.", new_x="LMARGIN", new_y="NEXT")
    p.set_y(y + 30)

    # ── B. The bilingual signature
    p.phase_head("B", "One consolidated bilingual signature, in three footprints")
    p.body(
        "Arabic and Latin are matched on a shared baseline, with optical weights and heights "
        "tuned so neither script overpowers the other. The result is one signature that holds "
        "together at any size, delivered in three configurations with a defined minimum size and "
        "clear-space rule for each - so nobody has to guess which version to use."
    )

    y = p.get_y() + 1
    boxes = [
        ("Horizontal", "Primary. Letterhead, website\nheader, vehicle panels.", "min. 30 mm"),
        ("Stacked", "Secondary. Cards, signage,\nsquare formats, uniforms.", "min. 18 mm"),
        ("Mark only", "Tertiary. Profile pictures,\nfavicon, app icon, stamps.", "min. 8 mm"),
    ]
    bw = (CW - 12) / 3
    x = ML
    for title, desc, minsize in boxes:
        p.set_draw_color(*HAIRLINE)
        p.set_line_width(0.25)
        p.rect(x, y, bw, 30, "D", round_corners=True, corner_radius=1.5)
        p.set_fill_color(*ORANGE)
        p.rect(x + 6, y + 6, 12, 1.6, "F")
        p.set_fill_color(*TEAL_SOFT)
        p.rect(x + 6, y + 10, 20, 1.6, "F")
        p.set_xy(x + 6, y + 15)
        p.set_font("Helvetica", "B", 8)
        p.set_text_color(*DARK)
        p.cell(bw - 12, 4.5, title, new_x="LMARGIN", new_y="NEXT")
        p.set_xy(x + 6, y + 19.5)
        p.set_font("Helvetica", "", 6.8)
        p.set_text_color(*GRAY)
        p.multi_cell(bw - 10, 3.4, desc, new_x="LMARGIN", new_y="NEXT")
        p.set_xy(x + 6, y + 25.6)
        p.set_font("Helvetica", "B", 6.4)
        p.set_text_color(*ORANGE)
        p.cell(bw - 12, 3.4, minsize.upper())
        x += bw + 6
    p.set_y(y + 36)

    p.set_x(ML)
    p.set_font("Helvetica", "", 7.4)
    p.set_text_color(*LIGHT)
    p.multi_cell(CW, 4, "Indicative layout of the lockup system. Actual construction is developed "
                        "in Phase 02 once a logomark route is selected.",
                 new_x="LMARGIN", new_y="NEXT")
    p.ln(4)

    # ── C. The system
    p.phase_head("C", "A system light enough that your team will actually use it")
    p.body(
        "Colour, typography, a supporting graphic device and clear placement rules - documented "
        "in a guidelines file people can read in fifteen minutes, not a 120-page manual that gets "
        "opened once. Everything ships with editable working files, so your team can produce "
        "day-to-day material without coming back to us for every post."
    )

    # ── What the three moves change, in plain terms
    p.ln(6)
    p.set_draw_color(*HAIRLINE)
    p.set_line_width(0.2)
    p.line(ML, p.get_y(), MR, p.get_y())
    p.ln(4)
    p.set_x(ML)
    p.set_font("Helvetica", "B", 8.6)
    p.set_text_color(*DARK)
    p.cell(CW, 5, "What that changes, in practice", new_x="LMARGIN", new_y="NEXT")
    p.ln(2)

    y = p.get_y()
    cases = [
        ("On a truck door",
         "One mark, cut in vinyl, still readable from the other side of a yard."),
        ("On a profile picture",
         "A square mark that fills the frame, instead of a wordmark squeezed into a circle."),
        ("On a tender document",
         "The full bilingual signature, correct in both scripts, at a size that fits the page."),
    ]
    cw3 = (CW - 12) / 3
    x = ML
    for title, text in cases:
        p.set_draw_color(*ORANGE)
        p.set_line_width(0.6)
        p.line(x, y, x + 10, y)
        p.set_xy(x, y + 2.5)
        p.set_font("Helvetica", "B", 7.8)
        p.set_text_color(*TEAL)
        p.cell(cw3, 4.6, title, new_x="LMARGIN", new_y="NEXT")
        p.set_xy(x, y + 8)
        p.set_font("Helvetica", "", 7.6)
        p.set_text_color(*GRAY)
        p.multi_cell(cw3 - 4, 4.2, text, new_x="LMARGIN", new_y="NEXT")
        x += cw3 + 6
    p.set_y(y + 24)

    # ───────────────────────────────────────────── SCOPE
    p.add_page()
    p.section("03", "Scope of work, phase by phase",
              "Seven phases, all delivered inside the same nine-day window")

    phases = [
        ("01", "Read and audit", "Day 1 - 2", [
            "Review of existing logo files, current collateral and how the mark is being applied today",
            "Benchmark of eight to ten logistics identities operating in KSA and the wider Gulf",
            "A 60 to 90 minute working session with your team - what the brand needs to carry, and where it keeps failing",
            "A one-page direction note, agreed before any design begins",
        ]),
        ("02", "Logomark and bilingual signature", "Day 2 - 5", [
            "Three logomark routes, each derived from the existing Marsal logo",
            "One selected route developed in full: construction grid, proportions, clear space, minimum sizes",
            "Consolidated bilingual lockups - horizontal, stacked and mark-only",
            "One-colour, reversed, mono and vinyl-cut versions for production",
            "Icon renderings at 16, 32, 64, 128 and 512 px, plus favicon and app-icon files",
            "Master artwork delivered as AI, EPS, SVG, PDF and PNG",
        ]),
        ("03", "Core brand system", "Day 5 - 6", [
            "Colour palette with print (CMYK, Pantone), screen (RGB, HEX) and fleet references (vinyl and paint codes)",
            "Typography: a matched Arabic and Latin pairing with weights, hierarchy and usage rules",
            "One supporting graphic device drawn from the mark, for backgrounds, edges and pattern",
            "Iconography direction and photography art direction for fleet, facility and team imagery",
        ]),
        ("04", "Print and corporate collateral", "Day 5 - 8", [
            "Business card, bilingual, both faces, print-ready with bleed and crop marks",
            "Letterhead and continuation sheet - print version plus an editable Word template for daily use",
            "Envelopes, DL and A4, and a document folder",
            "HTML email signature, bilingual, tested in Outlook and Gmail",
            "Operational document set: quotation, invoice, delivery note and waybill layouts",
            "Staff ID card, lanyard and uniform placement guide",
            "Fleet identity art direction - truck panel, van and container door placement",
        ]),
        ("05", "Digital and social", "Day 6 - 8", [
            "Profile picture set, correctly cropped and sized for LinkedIn, Instagram, X, WhatsApp Business and Google Business",
            "Cover and banner artwork for each platform",
            "Nine social post masters - announcement, service, milestone, hiring, client quote, route and network, seasonal greeting, event and a general-purpose layout",
            "Each master supplied in feed and story format, bilingual, as editable files",
            "16:9 presentation template, twelve master slides, for tenders and client meetings",
        ]),
        ("06", "Website design", "Day 6 - 8", [
            "Sitemap and wireframes for five key pages: Home, Services, Fleet and Network, About, Contact and Quote Request",
            "Full visual design of the Home page and one inner page, desktop and mobile",
            "A UI component kit - buttons, cards, forms, navigation, footer - so the remaining pages can be built consistently",
            "Bilingual layout logic, including right-to-left behaviour for the Arabic version",
            "Developer-ready handoff in Figma with specs and exported assets",
        ]),
        ("07", "Guidelines and handover", "Day 8 - 9", [
            "Brand guidelines document covering the mark, lockups, colour, type, collateral and digital application",
            "Organised master file library, named and structured so files can be found without us",
            "A 30-minute handover walkthrough with your team",
            "14 days of post-handover support for file and format questions",
        ]),
    ]

    for tag, title, days, items in phases:
        p.need(30)
        p.phase_head("PHASE " + tag, title, days)
        for it in items:
            p.bullet(it)
        p.ln(4)

    p.rule()
    p.note_line("Revisions  ",
                "Two rounds of consolidated feedback are included at each review point. "
                "Further rounds, or a change of direction after a route has been signed off, "
                "are quoted separately before any work begins.")

    # ── Tangible summary of the handover
    p.ln(6)
    p.set_x(ML)
    p.set_font("Helvetica", "B", 10)
    p.set_text_color(*DARK)
    p.cell(CW, 6, "What lands in your hands on 24 August", new_x="LMARGIN", new_y="NEXT")
    p.set_x(ML)
    p.set_font("Helvetica", "", 8.2)
    p.set_text_color(*GRAY)
    p.multi_cell(CW - 20, 4.8,
                 "Counted out, so the scope above is easy to check against what actually arrives.",
                 new_x="LMARGIN", new_y="NEXT")
    p.ln(4)

    tiles = [
        ("01", "logomark, developed\nand production ready"),
        ("03", "lockups, plus reversed\nand one-colour variants"),
        ("07", "print and corporate\ncollateral items"),
        ("05", "profile picture sets,\nsized per platform"),
        ("09", "social post masters,\nin feed and story"),
        ("12", "presentation master\nslides, 16:9"),
        ("05", "website pages designed\nor specified, with UI kit"),
        ("01", "guidelines document\nand master file library"),
    ]
    tw = (CW - 9) / 4
    y0 = p.get_y()
    for i, (num, label) in enumerate(tiles):
        col = i % 4
        row = i // 4
        x = ML + col * (tw + 3)
        ty = y0 + row * 26
        p.set_draw_color(*TEAL_SOFT)
        p.set_line_width(0.5)
        p.line(x, ty, x + 12, ty)
        p.set_xy(x, ty + 2)
        p.set_font("Helvetica", "B", 17)
        p.set_text_color(*TEAL)
        p.cell(tw, 9, num, new_x="LMARGIN", new_y="NEXT")
        p.set_xy(x, ty + 12)
        p.set_font("Helvetica", "", 7.2)
        p.set_text_color(*GRAY)
        p.multi_cell(tw - 4, 3.8, label, new_x="LMARGIN", new_y="NEXT")
    p.set_y(y0 + 54)

    p.set_x(ML)
    p.set_font("Helvetica", "", 7.4)
    p.set_text_color(*LIGHT)
    p.multi_cell(CW, 4,
                 "Every item is supplied in both an open, editable working file and a "
                 "ready-to-use export, in the formats your printers and developers will ask for.",
                 new_x="LMARGIN", new_y="NEXT")

    # ───────────────────────────────────────────── TIMELINE
    p.add_page()
    p.section("04", "Delivery schedule",
              "Kick-off Sunday 16 August, final handover Monday 24 August 2026")

    p.body(
        "The plan below runs nine consecutive days. Phases overlap deliberately - collateral, "
        "social and website design all begin from the same approved signature, so they progress "
        "in parallel rather than in a queue. Your input is only needed at the two review points "
        "marked in orange."
    )

    draw_gantt(p)

    # ── The three dates that matter
    p.ln(5)
    p.set_draw_color(*HAIRLINE)
    p.set_line_width(0.2)
    p.line(ML, p.get_y(), MR, p.get_y())
    p.ln(4)

    y = p.get_y()
    dates = [
        ("WED 19 AUG", "Review 01", "Three logomark routes presented. You select one direction.", ORANGE),
        ("SUN 23 AUG", "Review 02", "The full system applied - card, letterhead, social, website - reviewed together.", ORANGE),
        ("MON 24 AUG", "Handover", "Every file delivered, organised, with a 30-minute walkthrough.", TEAL),
    ]
    cw3 = (CW - 12) / 3
    x = ML
    for date, title, text, color in dates:
        p.set_fill_color(*color)
        p.rect(x, y, 10, 1.6, "F")
        p.set_xy(x, y + 3.5)
        p.set_font("Helvetica", "B", 7)
        p.set_text_color(*color)
        p.cell(cw3, 4.2, date, new_x="LMARGIN", new_y="NEXT")
        p.set_xy(x, y + 8)
        p.set_font("Helvetica", "B", 9)
        p.set_text_color(*DARK)
        p.cell(cw3, 5, title, new_x="LMARGIN", new_y="NEXT")
        p.set_xy(x, y + 13.5)
        p.set_font("Helvetica", "", 7.4)
        p.set_text_color(*GRAY)
        p.multi_cell(cw3 - 5, 4.1, text, new_x="LMARGIN", new_y="NEXT")
        x += cw3 + 6
    p.set_y(y + 30)

    p.set_draw_color(*HAIRLINE)
    p.set_line_width(0.2)
    p.line(ML, p.get_y(), MR, p.get_y())
    p.ln(5)

    p.note_line("On the weekend  ",
                "Friday 21 and Saturday 22 August fall inside the window. Our studio keeps a "
                "reduced working pass across both days so the schedule holds - no input is "
                "needed from your side on those dates.")
    p.note_line("The one dependency  ",
                "Phase 02 cannot start until the existing logo is supplied in vector format and "
                "a single approver is named. Everything downstream moves with that date.")

    # ───────────────────────────────────────────── INVESTMENT
    p.add_page()
    p.section("05", "Investment and terms",
              "One fee, broken down so you can see where the effort sits")

    lines = [
        ("01", "Read and audit", 1500),
        ("02", "Logomark and bilingual signature", 7000),
        ("03", "Core brand system", 3000),
        ("04", "Print and corporate collateral", 4000),
        ("05", "Digital and social", 3500),
        ("06", "Website design", 3500),
        ("07", "Guidelines and handover", 1500),
    ]

    # table head
    p.set_x(ML)
    p.set_font("Helvetica", "B", 7)
    p.set_text_color(*TEAL)
    p.cell(12, 6, "")
    p.cell(CW - 52, 6, "PHASE")
    p.cell(40, 6, "SAR", align="R", new_x="LMARGIN", new_y="NEXT")
    p.set_draw_color(*TEAL)
    p.set_line_width(0.4)
    p.line(ML, p.get_y(), MR, p.get_y())
    p.ln(1.5)

    for i, (num, title, amt) in enumerate(lines):
        p.set_x(ML)
        if i % 2 == 0:
            p.set_fill_color(*PAPER)
            p.rect(ML, p.get_y(), CW, 7.6, "F")
        p.set_font("Helvetica", "B", 7.6)
        p.set_text_color(*TEAL_SOFT)
        p.cell(12, 7.6, num)
        p.set_font("Helvetica", "", 8.6)
        p.set_text_color(*DARK)
        p.cell(CW - 52, 7.6, title)
        p.set_font("Helvetica", "", 8.6)
        p.set_text_color(*DARK)
        p.cell(40, 7.6, f"{amt:,}", align="R", new_x="LMARGIN", new_y="NEXT")

    p.ln(1)
    p.set_draw_color(*HAIRLINE)
    p.set_line_width(0.2)
    p.line(ML, p.get_y(), MR, p.get_y())
    p.ln(2)

    # Fee headline
    p.set_x(ML)
    p.set_font("Helvetica", "B", 8.6)
    p.set_text_color(*DARK)
    p.cell(CW - 40, 7, "Total professional fee")
    p.cell(40, 7, f"{FEE:,}", align="R", new_x="LMARGIN", new_y="NEXT")

    if INCLUDE_VAT:
        vat = FEE * VAT_RATE
        p.set_x(ML)
        p.set_font("Helvetica", "", 8)
        p.set_text_color(*GRAY)
        p.cell(CW - 40, 6.5, "VAT at 15%, as required in the Kingdom")
        p.cell(40, 6.5, f"{vat:,.0f}", align="R", new_x="LMARGIN", new_y="NEXT")
        p.ln(2)
        y = p.get_y()
        p.set_fill_color(*TEAL)
        p.rect(ML, y, CW, 11, "F", round_corners=True, corner_radius=1.2)
        p.set_xy(ML + 4, y)
        p.set_font("Helvetica", "B", 9)
        p.set_text_color(*WHITE)
        p.cell(CW - 48, 11, "TOTAL PAYABLE, INCLUSIVE OF VAT")
        p.set_font("Helvetica", "B", 11)
        p.cell(40, 11, f"SAR {FEE + vat:,.0f}", align="R", new_x="LMARGIN", new_y="NEXT")
        p.set_y(y + 11)
    else:
        p.ln(2)
        y = p.get_y()
        p.set_fill_color(*TEAL)
        p.rect(ML, y, CW, 11, "F", round_corners=True, corner_radius=1.2)
        p.set_xy(ML + 4, y)
        p.set_font("Helvetica", "B", 9)
        p.set_text_color(*WHITE)
        p.cell(CW - 48, 11, "TOTAL PROFESSIONAL FEE")
        p.set_font("Helvetica", "B", 11)
        p.cell(40, 11, f"SAR {FEE:,}", align="R", new_x="LMARGIN", new_y="NEXT")
        p.set_y(y + 11)

    p.ln(8)

    # Two-column: included / not included
    y = p.get_y()
    colw = (CW - 10) / 2

    p.set_xy(ML, y)
    p.set_font("Helvetica", "B", 7.4)
    p.set_text_color(*TEAL)
    p.cell(colw, 5, "INCLUDED IN THE FEE", new_x="LMARGIN", new_y="NEXT")
    p.ln(1)
    for t in [
        "All design, artwork and file preparation across the seven phases",
        "Two rounds of consolidated revisions at each review point",
        "Full ownership of the final approved artwork, transferred to Marsal on settlement",
        "Editable working files and organised master library",
        "14 days of support after handover",
    ]:
        p.set_x(ML)
        p.set_draw_color(*TEAL_MID)
        p.set_fill_color(*TEAL_MID)
        p.rect(ML, p.get_y() + 1.6, 1.2, 1.2, "F")
        p.set_xy(ML + 3.5, p.get_y())
        p.set_font("Helvetica", "", 7.6)
        p.set_text_color(*GRAY)
        p.multi_cell(colw - 5, 4.3, t, new_x="LMARGIN", new_y="NEXT")
        p.ln(0.8)
    left_end = p.get_y()

    p.set_xy(ML + colw + 10, y)
    p.set_font("Helvetica", "B", 7.4)
    p.set_text_color(*ORANGE)
    p.cell(colw, 5, "NOT INCLUDED", new_x="LMARGIN", new_y="NEXT")
    p.ln(1)
    for t in [
        "Printing and physical production of any item",
        "Website development and hosting - design only at this stage",
        "Photography and video production, should new imagery be required",
        "Third-party font licences, if a commercial typeface is selected",
        "Vehicle wrap production and fitting",
        "Trademark filing and registration",
    ]:
        p.set_xy(ML + colw + 10, p.get_y())
        p.set_fill_color(*ORANGE_SOFT)
        p.rect(ML + colw + 10, p.get_y() + 1.6, 1.2, 1.2, "F")
        p.set_xy(ML + colw + 13.5, p.get_y())
        p.set_font("Helvetica", "", 7.6)
        p.set_text_color(*GRAY)
        p.multi_cell(colw - 5, 4.3, t, new_x="LMARGIN", new_y="NEXT")
        p.ln(0.8)

    p.set_y(max(left_end, p.get_y()))
    p.rule()

    p.note_line("Payment  ",
                "50% on written confirmation to proceed, 50% on final handover. "
                "Bank transfer to Miradore Experiences, Riyadh. A tax invoice is issued against each stage.")
    p.note_line("Validity  ",
                "This proposal holds for 30 days from 14 August 2026. The 24 August delivery date "
                "assumes confirmation by Saturday 15 August.")
    p.note_line("If it needs to flex  ",
                "Website design is the one block that can be deferred without weakening anything "
                "else - the mark, the bilingual signature and the collateral all stand on their "
                "own, and the fee reduces by SAR 3,500 if you would rather take it up later. "
                "Equally, if you want fleet livery production artwork or a full tender document "
                "set added, say so and we will price it against the same schedule.")

    # ───────────────────────────────────────────── WHAT WE NEED
    p.add_page()
    p.section("06", "What we need from Marsal",
              "Five things. Nothing that should take more than an hour to gather.")

    for t in [
        "The existing logo in vector format - AI, EPS or SVG. A PNG or JPG will not carry us through print or vehicle production.",
        "One named approver. Nine days does not survive design by committee, and this is the single biggest risk to the date.",
        "Your Arabic legal name exactly as registered, plus CR number, VAT number and the address block for stationery.",
        "Contact details for cards and email signatures - names, titles in both languages, numbers.",
        "Two or three photographs of the current fleet and facility, so the art direction is built on what Marsal actually looks like.",
    ]:
        p.bullet(t, size=8.6, lh=4.9)
        p.ln(2.5)

    p.rule(gap=6)

    p.set_x(ML)
    p.set_font("Helvetica", "B", 10)
    p.set_text_color(*DARK)
    p.cell(CW, 7, "How we work through it", new_x="LMARGIN", new_y="NEXT")
    p.ln(1)
    p.body(
        "You will hear from us at two points, not ten. The first is the logomark route "
        "presentation, where you pick a direction. The second is the full system review, where "
        "you see everything applied together - card, letterhead, social, website - before we "
        "finalise. Between those points we work, and we do not send fragments for reaction. "
        "It keeps the decisions clean and it keeps the date."
    )

    p.ln(6)

    # Acceptance block
    y = p.get_y()
    p.set_draw_color(*TEAL_SOFT)
    p.set_line_width(0.3)
    p.rect(ML, y, CW, 52, "D", round_corners=True, corner_radius=2)
    p.set_xy(ML + 6, y + 6)
    p.set_font("Helvetica", "B", 8)
    p.set_text_color(*TEAL)
    p.cell(CW - 12, 5, "CONFIRMATION TO PROCEED", new_x="LMARGIN", new_y="NEXT")
    p.set_xy(ML + 6, y + 12)
    p.set_font("Helvetica", "", 7.8)
    p.set_text_color(*GRAY)
    p.multi_cell(CW - 12, 4.4,
                 "Signing below confirms the scope, fee and schedule set out in this document, "
                 "and authorises Miradore Experiences to begin work.",
                 new_x="LMARGIN", new_y="NEXT")

    sy = y + 34
    p.set_draw_color(*LIGHT)
    p.set_line_width(0.25)
    p.line(ML + 6, sy, ML + 6 + 52, sy)
    p.line(ML + 70, sy, ML + 70 + 42, sy)
    p.line(ML + 122, sy, ML + 122 + 40, sy)
    p.set_font("Helvetica", "", 6.6)
    p.set_text_color(*LIGHT)
    p.set_xy(ML + 6, sy + 1.5)
    p.cell(52, 4, "NAME AND SIGNATURE, FOR MARSAL")
    p.set_xy(ML + 70, sy + 1.5)
    p.cell(42, 4, "TITLE")
    p.set_xy(ML + 122, sy + 1.5)
    p.cell(40, 4, "DATE")

    p.set_y(y + 60)
    p.set_x(ML)
    p.set_font("Helvetica", "", 8.6)
    p.set_text_color(*GRAY)
    p.multi_cell(CW, 5,
                 "Any questions before you sign, call us. We would rather talk it through than "
                 "have you agree to something on paper that does not match what you pictured.",
                 new_x="LMARGIN", new_y="NEXT")

    p.ln(8)
    p.set_x(ML)
    p.set_font("Helvetica", "B", 8)
    p.set_text_color(*TEAL)
    p.cell(CW, 5, "MIRADORE EXPERIENCES", new_x="LMARGIN", new_y="NEXT")
    p.set_x(ML)
    p.set_font("Helvetica", "", 7.6)
    p.set_text_color(*LIGHT)
    p.cell(CW, 4.4, "Riyadh, Kingdom of Saudi Arabia", new_x="LMARGIN", new_y="NEXT")
    p.set_x(ML)
    p.cell(CW, 4.4, "hello@miradore.co  /  www.miradore.co", new_x="LMARGIN", new_y="NEXT")

    out = os.path.join(BASE, "Marsal_Brand_Evolution_Proposal_Miradore.pdf")
    p.output(out)
    write_cost_csv(lines)
    return out


def write_cost_csv(lines):
    """Companion cost breakdown, matching the convention of the other quotations."""
    import csv
    path = os.path.join(BASE, "Marsal_Brand_Evolution_Cost_Breakdown.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Marsal - Brand Evolution Proposal"])
        w.writerow(["Prepared by", "Miradore Experiences, Riyadh"])
        w.writerow(["Date", "14 August 2026"])
        w.writerow(["Delivery", "24 August 2026"])
        w.writerow([])
        w.writerow(["Phase", "Description", "Amount (SAR)"])
        for num, title, amt in lines:
            w.writerow([num, title, amt])
        w.writerow([])
        w.writerow(["", "Total professional fee", FEE])
        if INCLUDE_VAT:
            w.writerow(["", "VAT (15%)", round(FEE * VAT_RATE)])
            w.writerow(["", "Total payable incl. VAT", round(FEE * (1 + VAT_RATE))])
    return path


# ═══════════════════════════════════════════════════════════════
def draw_gantt(p):
    """Nine-day schedule, Sun 16 Aug - Mon 24 Aug 2026."""
    days = [
        ("SUN", "16"), ("MON", "17"), ("TUE", "18"), ("WED", "19"), ("THU", "20"),
        ("FRI", "21"), ("SAT", "22"), ("SUN", "23"), ("MON", "24"),
    ]
    weekend = {5, 6}

    label_w = 62
    gx = ML + label_w
    gw = MR - gx
    col = gw / len(days)
    top = p.get_y() + 4
    row_h = 7.0

    # ── Day header
    p.set_font("Helvetica", "B", 6.2)
    for i, (dow, num) in enumerate(days):
        x = gx + i * col
        if i in weekend:
            p.set_fill_color(*PAPER)
            p.rect(x, top - 1, col, 4 + row_h * 11 + 3, "F")
        p.set_text_color(*(LIGHT if i in weekend else TEAL_MID))
        p.set_xy(x, top - 0.5)
        p.cell(col, 3.4, dow, align="C", new_x="LEFT", new_y="NEXT")
        p.set_font("Helvetica", "B", 7.6)
        p.set_text_color(*(LIGHT if i in weekend else DARK))
        p.set_xy(x, top + 2.6)
        p.cell(col, 4, num, align="C")
        p.set_font("Helvetica", "B", 6.2)

    p.set_xy(ML, top + 0.5)
    p.set_font("Helvetica", "B", 6.2)
    p.set_text_color(*LIGHT)
    p.cell(label_w, 4, "AUGUST 2026")

    grid_top = top + 8
    p.set_draw_color(*TEAL)
    p.set_line_width(0.4)
    p.line(ML, grid_top, MR, grid_top)

    # ── Rows: (label, start_idx, end_idx, kind)
    #    kind: "work" | "gate" | "final"
    rows = [
        ("Kick-off, audit and direction", 0, 1, "work"),
        ("Logomark routes  x3", 1, 2, "work"),
        ("Review 01  /  route selection", 3, 3, "gate"),
        ("Refinement and bilingual signature", 3, 4, "work"),
        ("Colour, typography, core system", 4, 5, "work"),
        ("Print and corporate collateral", 4, 6, "work"),
        ("Digital, social and profile kit", 5, 7, "work"),
        ("Website design and UI kit", 5, 7, "work"),
        ("Review 02  /  full system", 7, 7, "gate"),
        ("Guidelines, packaging and QA", 7, 8, "work"),
        ("Final handover", 8, 8, "final"),
    ]

    y = grid_top + 2
    for label, s, e, kind in rows:
        # row label
        p.set_xy(ML, y)
        p.set_font("Helvetica", "B" if kind != "work" else "", 7.2)
        p.set_text_color(*(ORANGE if kind == "gate" else (TEAL if kind == "final" else DARK)))
        p.cell(label_w - 4, row_h - 1.4, label)

        # bar
        bx = gx + s * col + 1.2
        bw = (e - s + 1) * col - 2.4
        by = y + 1.4
        bh = row_h - 4.2

        if kind == "gate":
            # diamond marker + light chip
            p.set_fill_color(*ORANGE_SOFT)
            p.rect(bx, by, bw, bh, "F", round_corners=True, corner_radius=bh / 2)
            cx = bx + bw / 2
            cy = by + bh / 2
            r = 1.9
            p.set_fill_color(*ORANGE)
            p.set_draw_color(*ORANGE)
            p.polygon(
                [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
                style="F",
            )
        elif kind == "final":
            p.set_fill_color(*TEAL)
            p.rect(bx, by, bw, bh, "F", round_corners=True, corner_radius=bh / 2)
        else:
            p.set_fill_color(*TEAL_SOFT)
            p.rect(bx, by, bw, bh, "F", round_corners=True, corner_radius=bh / 2)
            p.set_fill_color(*TEAL)
            p.rect(bx, by, min(2.2, bw), bh, "F", round_corners=True, corner_radius=bh / 2)

        # row hairline
        p.set_draw_color(*HAIRLINE)
        p.set_line_width(0.15)
        p.line(ML, y + row_h - 0.6, MR, y + row_h - 0.6)
        y += row_h

    # column ticks
    p.set_draw_color(*HAIRLINE)
    p.set_line_width(0.15)
    for i in range(1, len(days)):
        x = gx + i * col
        p.line(x, grid_top, x, y - 0.6)

    # ── Legend
    ly = y + 4
    p.set_xy(ML, ly)
    items = [
        (TEAL_SOFT, "Studio work"),
        (ORANGE, "Marsal input required"),
        (TEAL, "Handover"),
        (PAPER, "Kingdom weekend"),
    ]
    x = ML
    for color, label in items:
        p.set_fill_color(*color)
        p.set_draw_color(*HAIRLINE)
        p.set_line_width(0.15)
        p.rect(x, ly + 1, 6, 2.6, "DF", round_corners=True, corner_radius=1.3)
        p.set_xy(x + 8, ly)
        p.set_font("Helvetica", "", 6.8)
        p.set_text_color(*GRAY)
        w = p.get_string_width(label) + 2
        p.cell(w, 4.6, label)
        x += 8 + w + 7

    p.set_y(ly + 8)


if __name__ == "__main__":
    path = build()
    print("Written:", path)
