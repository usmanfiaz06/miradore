#!/usr/bin/env python3
"""
Render proposal.html to a print-ready PDF using headless Chromium.

    python3 build.py            # write the PDF
    python3 build.py --preview  # also render page PNGs into preview/

Chromium is pre-installed at /opt/pw-browsers; fonts are inlined as
base64 woff2 in fonts/fonts-inline.css so the PDF is fully self-contained.
"""

import argparse
import asyncio
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "proposal.html")
OUT = os.path.abspath(os.path.join(HERE, "..", "Marsal_Brand_Evolution_Proposal_Miradore.pdf"))
PREVIEW = os.path.join(HERE, "preview")


async def render(preview=False):
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path=chromium_path())
        page = await browser.new_page()
        await page.goto("file://" + SRC, wait_until="networkidle")
        await page.evaluate("document.fonts.ready")

        await page.pdf(
            path=OUT,
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        await browser.close()

    print("PDF:", OUT)

    if preview:
        os.makedirs(PREVIEW, exist_ok=True)
        import pypdfium2 as pdfium

        doc = pdfium.PdfDocument(OUT)
        for i in range(len(doc)):
            doc[i].render(scale=1.35).to_pil().save(
                os.path.join(PREVIEW, f"page-{i + 1:02d}.png")
            )
        print(f"Preview: {len(doc)} pages -> {PREVIEW}")


def chromium_path():
    """Locate the pre-installed Chromium binary, if it is not on the default path."""
    root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    for candidate in (
        os.path.join(root, "chromium", "chrome-linux", "chrome"),
        os.path.join(root, "chromium"),
    ):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    for entry in sorted(os.listdir(root)) if os.path.isdir(root) else []:
        candidate = os.path.join(root, entry, "chrome-linux", "chrome")
        if os.path.isfile(candidate):
            return candidate
    return None  # fall back to Playwright's own resolution


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true", help="also write page PNGs")
    args = ap.parse_args()
    if not os.path.exists(SRC):
        sys.exit("proposal.html not found")
    asyncio.run(render(preview=args.preview))
