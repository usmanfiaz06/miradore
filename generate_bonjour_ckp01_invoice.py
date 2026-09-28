"""Tax invoice for Bonjour Arabia - CKP-01 Cultural Knowledge Platform.

Amounts follow quotation BA-CKP-01 (28 Sep 2026): 180 invoiced days at
SAR 1,375 = SAR 247,500 + 15% VAT = SAR 284,625.
Output: Bonjour_Arabia_CKP01_Invoice.pdf (Miradore letterhead, stamp, signature).
"""
import os

import fitz  # pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "Miradore Logo Color.png")
SIGNATURE = os.path.join(HERE, "adeel_signature-removebg-preview.png")
STAMP = os.path.join(HERE, "Miradore_Stamp_Rectangular_Riyadh_v2.1.pdf")
OUT = os.path.join(HERE, "Bonjour_Arabia_CKP01_Invoice.pdf")
TMP = OUT + ".tmp"

TEAL = colors.HexColor("#0E7C7B")
ORANGE = colors.HexColor("#E0662A")
DARK = colors.HexColor("#222222")
GRAY = colors.HexColor("#666666")
LIGHT = colors.HexColor("#EEF6F6")
LINE = colors.HexColor("#C9D6D6")

INVOICE_NO = "MX-INV-2026-BA-001"
INVOICE_DATE = "28 September 2026"
QUOTE_REF = "BA-CKP-01 (28 September 2026)"
DAY_RATE = 1375
VAT_RATE = 0.15

ITEMS = [
    ("WS1", "Acquisition", "Source register, connectors, crawler, partner intake", "Lead AI Engineer", 25, "G1"),
    ("WS2", "Graph and validation", "Entity model, resolution, reviewer workflow", "Lead AI Engineer", 35, "G2"),
    ("WS3", "Field data and dialect", "Upload, transcription, correction interface, WER", "Lead AI Engineer", 30, "G2"),
    ("WS4", "Grounded narration", "Retrieval, generation, verifier, abstention tests", "Full-stack AI Engineer", 30, "G2"),
    ("WS5", "Itineraries", "Constraint solver, feasibility check, regeneration", "Full-stack AI Engineer", 20, "G3"),
    ("WS6", "Surfaces and delivery", "API, web app, partner console, dashboard, cloud, handover", "Full-stack AI Engineer", 40, "G3"),
]

SCHEDULE = [
    ("Advance on signing", "On signing", 0.30),
    ("Gate G1 acceptance", "Month 2", 0.15),
    ("Gate G2 acceptance", "Month 4", 0.30),
    ("Gate G3 acceptance", "Month 6", 0.25),
]

W, H = A4
L, R = 18 * mm, W - 18 * mm


def money(v):
    return f"{v:,.2f}" if v % 1 else f"{v:,.0f}"


def num_words(n):
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
            "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
            "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def below_1000(x):
        parts = []
        if x >= 100:
            parts.append(ones[x // 100] + " Hundred")
            x %= 100
        if x >= 20:
            parts.append(tens[x // 10] + ("-" + ones[x % 10] if x % 10 else ""))
        elif x:
            parts.append(ones[x])
        return " ".join(parts)

    out = []
    if n >= 1_000_000:
        out.append(below_1000(n // 1_000_000) + " Million")
        n %= 1_000_000
    if n >= 1000:
        out.append(below_1000(n // 1000) + " Thousand")
        n %= 1000
    if n:
        out.append(below_1000(n))
    return " ".join(out)


def letterhead(c):
    c.drawImage(LOGO, L, H - 31 * mm, width=52 * mm, height=18 * mm,
                preserveAspectRatio=True, anchor="w", mask="auto")
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(R, H - 17 * mm, "MIRADORE EXPERIENCES COMPANY")
    c.setFont("Helvetica", 8)
    c.setFillColor(GRAY)
    c.drawRightString(R, H - 21.5 * mm, "Riyadh, Kingdom of Saudi Arabia")
    c.drawRightString(R, H - 25.5 * mm, "C.R. No. 7054053371")
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.6)
    c.line(L, H - 34 * mm, R, H - 34 * mm)
    c.setStrokeColor(ORANGE)
    c.setLineWidth(0.6)
    c.line(L, H - 35.2 * mm, R, H - 35.2 * mm)

    # footer
    c.setStrokeColor(ORANGE)
    c.setLineWidth(0.8)
    c.line(L, 16 * mm, R, 16 * mm)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(GRAY)
    c.drawString(L, 11 * mm, "Miradore Experiences Company  |  Riyadh, KSA  |  C.R. 7054053371")
    c.drawRightString(R, 11 * mm, "info@miradoreproductions.com.pk")


def main():
    c = canvas.Canvas(TMP, pagesize=A4)
    c.setTitle(f"Tax Invoice {INVOICE_NO} - Bonjour Arabia CKP-01")
    c.setAuthor("Miradore Experiences Company")
    letterhead(c)

    # Title
    y = H - 45 * mm
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(L, y, "TAX INVOICE")
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(DARK)
    meta = [("Invoice No.", INVOICE_NO), ("Invoice Date", INVOICE_DATE),
            ("Quotation Ref.", QUOTE_REF), ("Currency", "Saudi Riyal (SAR)")]
    my = y + 3 * mm
    for k, v in meta:
        c.setFont("Helvetica", 8)
        c.setFillColor(GRAY)
        c.drawRightString(R - 48 * mm, my, k)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(DARK)
        c.drawRightString(R, my, v)
        my -= 4.3 * mm

    # Bill to / From
    y = H - 64 * mm
    box_h = 22 * mm
    half = (R - L - 6 * mm) / 2
    for i, (title, lines) in enumerate([
        ("BILL TO", ["Bonjour Arabia",
                     "Travel and Experiences Design House",
                     "Riyadh, Kingdom of Saudi Arabia"]),
        ("FROM", ["Miradore Experiences Company",
                  "Riyadh, Kingdom of Saudi Arabia",
                  "C.R. No. 7054053371"]),
    ]):
        x = L + i * (half + 6 * mm)
        c.setFillColor(LIGHT)
        c.setStrokeColor(LINE)
        c.rect(x, y - box_h, half, box_h, fill=1, stroke=1)
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x + 4 * mm, y - 5.5 * mm, title)
        c.setFillColor(DARK)
        ly = y - 10 * mm
        for j, line in enumerate(lines):
            c.setFont("Helvetica-Bold" if j == 0 else "Helvetica", 9 if j == 0 else 8.5)
            c.drawString(x + 4 * mm, ly, line)
            ly -= 4.3 * mm

    # Project line
    y -= box_h + 6 * mm
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(L, y, "Project: CKP-01 Cultural Knowledge Platform - engineering delivery, WS1 to WS6")
    c.setFont("Helvetica", 8)
    c.setFillColor(GRAY)
    c.drawString(L, y - 4.3 * mm, "Six-month programme  |  Two Saudi engineers, part time, remote  |  180 invoiced days")

    # Items table
    y -= 8 * mm
    cols = [("#", 8), ("Ref", 12), ("Workstream and deliverable", 72), ("Resource", 32),
            ("Days", 10), ("Rate", 16), ("Amount (SAR)", 24)]
    total_w = sum(w for _, w in cols)
    scale = (R - L) / (total_w * mm)
    xs = [L]
    for _, w in cols:
        xs.append(xs[-1] + w * mm * scale)

    hdr_h = 7 * mm
    c.setFillColor(TEAL)
    c.rect(L, y - hdr_h, R - L, hdr_h, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    for i, (name, _) in enumerate(cols):
        if i >= 4:
            c.drawRightString(xs[i + 1] - 2 * mm, y - 4.7 * mm, name)
        else:
            c.drawString(xs[i] + 2 * mm, y - 4.7 * mm, name)
    y -= hdr_h

    row_h = 9.2 * mm
    subtotal = 0
    for n, (ref, name, desc, res, days, gate) in enumerate(ITEMS, 1):
        amt = days * DAY_RATE
        subtotal += amt
        if n % 2 == 0:
            c.setFillColor(LIGHT)
            c.rect(L, y - row_h, R - L, row_h, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.setFont("Helvetica", 8.5)
        c.drawString(xs[0] + 2 * mm, y - 4.6 * mm, str(n))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(xs[1] + 2 * mm, y - 4.6 * mm, ref)
        c.drawString(xs[2] + 2 * mm, y - 4.6 * mm, f"{name}  ({gate})")
        c.setFont("Helvetica", 7.2)
        c.setFillColor(GRAY)
        c.drawString(xs[2] + 2 * mm, y - 7.9 * mm, desc)
        c.setFillColor(DARK)
        c.setFont("Helvetica", 8)
        c.drawString(xs[3] + 2 * mm, y - 4.6 * mm, res)
        c.drawRightString(xs[5] - 2 * mm, y - 4.6 * mm, str(days))
        c.drawRightString(xs[6] - 2 * mm, y - 4.6 * mm, money(DAY_RATE))
        c.setFont("Helvetica-Bold", 8.5)
        c.drawRightString(xs[7] - 2 * mm, y - 4.6 * mm, money(amt))
        c.setStrokeColor(LINE)
        c.setLineWidth(0.4)
        c.line(L, y - row_h, R, y - row_h)
        y -= row_h

    assert subtotal == 247_500
    vat = subtotal * VAT_RATE
    total = subtotal + vat

    # Totals
    y -= 3 * mm
    tx = xs[3]
    for label, val, strong in [("Subtotal (180 invoiced days)", subtotal, False),
                               ("VAT 15%", vat, False),
                               ("TOTAL AMOUNT DUE (SAR)", total, True)]:
        h = 7.5 * mm if strong else 5.6 * mm
        if strong:
            c.setFillColor(TEAL)
            c.rect(tx, y - h, R - tx, h, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 10)
        else:
            c.setFillColor(DARK)
            c.setFont("Helvetica", 9)
        c.drawString(tx + 3 * mm, y - h + 2.4 * mm, label)
        c.drawRightString(R - 2 * mm, y - h + 2.4 * mm, money(val))
        y -= h + 0.8 * mm

    c.setFillColor(DARK)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(L, y - 3 * mm, f"Amount in words: {num_words(int(total))} Saudi Riyals Only.")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(GRAY)
    c.drawString(L, y - 7.3 * mm, "In addition, 20 in-kind engineering days (SAR 27,500) are delivered and not invoiced.")

    # Payment schedule
    y -= 13 * mm
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(L, y, "PAYMENT SCHEDULE  -  30% ADVANCE ON SIGNING, BALANCE ON ACCEPTANCE AT EACH GATE")
    y -= 3 * mm
    scols = [("Milestone", 58), ("Timing", 28), ("Share", 18), ("Net (SAR)", 26), ("VAT 15%", 26), ("Payable (SAR)", 30)]
    sw = sum(w for _, w in scols)
    sxs = [L]
    for _, w in scols:
        sxs.append(sxs[-1] + w * (R - L) / sw)
    c.setFillColor(ORANGE)
    c.rect(L, y - 6.5 * mm, R - L, 6.5 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    for i, (name, _) in enumerate(scols):
        if i >= 2:
            c.drawRightString(sxs[i + 1] - 2 * mm, y - 4.5 * mm, name)
        else:
            c.drawString(sxs[i] + 2 * mm, y - 4.5 * mm, name)
    y -= 6.5 * mm
    sums = [0, 0, 0]
    for milestone, timing, pct in SCHEDULE:
        net = subtotal * pct
        v = net * VAT_RATE
        vals = [net, v, net + v]
        sums = [a + b for a, b in zip(sums, vals)]
        c.setFillColor(DARK)
        c.setFont("Helvetica", 8)
        c.drawString(sxs[0] + 2 * mm, y - 4.1 * mm, milestone)
        c.drawString(sxs[1] + 2 * mm, y - 4.1 * mm, timing)
        c.drawRightString(sxs[3] - 2 * mm, y - 4.1 * mm, f"{int(pct * 100)}%")
        for k, val in enumerate(vals):
            c.drawRightString(sxs[4 + k] - 2 * mm, y - 4.1 * mm, money(val))
        c.setStrokeColor(LINE)
        c.line(L, y - 5.8 * mm, R, y - 5.8 * mm)
        y -= 5.8 * mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(sxs[0] + 2 * mm, y - 4.1 * mm, "Total")
    c.drawRightString(sxs[3] - 2 * mm, y - 4.1 * mm, "100%")
    for k, val in enumerate(sums):
        c.drawRightString(sxs[4 + k] - 2 * mm, y - 4.1 * mm, money(val))
    assert round(sums[2], 2) == 284_625

    # Terms (left) and signature + stamp (right)
    y -= 11 * mm
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(L, y, "TERMS")
    c.setFillColor(DARK)
    c.setFont("Helvetica", 7.3)
    for line in [
        "1. Amounts as per quotation BA-CKP-01.",
        "2. Gate payments are due on acceptance against",
        "    each gate's written criteria.",
        "3. Recurring cloud, GPU, inference and third-party",
        "    services are billed separately, monthly at",
        "    documented cost, no markup.",
        "4. Please quote the invoice number on all payments.",
    ]:
        y -= 3.8 * mm
        c.drawString(L, y, line)

    sig_x = 118 * mm
    sig_y = 24 * mm
    c.drawImage(SIGNATURE, sig_x, sig_y + 7 * mm, width=45 * mm, height=16 * mm,
                preserveAspectRatio=True, mask="auto")
    c.setStrokeColor(DARK)
    c.setLineWidth(0.5)
    c.line(sig_x, sig_y + 6 * mm, R, sig_y + 6 * mm)
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(sig_x, sig_y + 2 * mm, "ADEEL AHMED - DIRECTOR")
    c.setFont("Helvetica", 7.3)
    c.drawString(sig_x, sig_y - 1.8 * mm, "Authorised Signatory, Miradore Experiences Company")

    c.showPage()
    c.save()

    # Overlay the vector company stamp (teal version, page 0)
    doc = fitz.open(TMP)
    stamp = fitz.open(STAMP)
    page = doc[0]
    sw_pt, sh_pt = 48 * mm, 36 * mm
    x0 = sig_x + 24 * mm
    y0 = H - (sig_y + 33 * mm)  # PDF->fitz coords (top-left origin)
    page.show_pdf_page(fitz.Rect(x0, y0, x0 + sw_pt, y0 + sh_pt), stamp, 0, rotate=-4)
    doc.save(OUT, garbage=3, deflate=True)
    os.remove(TMP)
    print("Wrote", OUT, "| subtotal", subtotal, "| VAT", vat, "| total", total)


if __name__ == "__main__":
    main()
