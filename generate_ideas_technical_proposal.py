#!/usr/bin/env python3
"""
Generate Technical Proposal PDF for IDEAS 2026 & 2028 — DEPO RFP
Miradore Experiences branded proposal
"""

from fpdf import FPDF
import os

# ── Brand Palette ──────────────────────────────────────────────
TEAL = (0, 128, 128)
ORANGE = (230, 100, 30)
DARK = (40, 40, 40)
GRAY = (100, 100, 100)
LIGHT_GRAY = (160, 160, 160)
LIGHT_BG = (245, 248, 250)
WHITE = (255, 255, 255)
SECTION_BG = (230, 243, 243)
NAVY = (20, 40, 65)


class ProposalPDF(FPDF):
    show_header = True
    show_footer = True

    def header(self):
        if not self.show_header:
            return
        logo_path = os.path.join(os.path.dirname(__file__), "Miradore Logo Color.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=15, y=8, w=40)
        self.set_xy(100, 10)
        self.set_font("Helvetica", "", 6.5)
        self.set_text_color(*GRAY)
        self.cell(95, 4, "TECHNICAL PROPOSAL  |  RFP-DEPO-IDEAS-2026-001", align="R")
        self.set_draw_color(*TEAL)
        self.set_line_width(0.6)
        self.line(15, 18, 195, 18)
        self.set_y(22)

    def footer(self):
        if not self.show_footer:
            return
        self.set_y(-12)
        self.set_font("Helvetica", "I", 6.5)
        self.set_text_color(*GRAY)
        self.cell(0, 8, f"Miradore Experiences  |  Confidential  |  Page {self.page_no()}/{{nb}}", align="C")

    # ── Utility methods ──
    def accent_line(self, y=None):
        if y is None:
            y = self.get_y()
        self.set_draw_color(*TEAL)
        self.set_line_width(0.6)
        self.line(15, y, 195, y)

    def section_title(self, num, title):
        if self.get_y() > 245:
            self.add_page()
        self.ln(4)
        self.set_fill_color(*TEAL)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 11)
        label = f"  {num}.  {title.upper()}"
        self.cell(180, 9, label, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def subsection(self, title):
        if self.get_y() > 255:
            self.add_page()
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*TEAL)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK)
        self.multi_cell(180, 4.5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bullet(self, text, indent=20):
        x = self.get_x()
        self.set_x(indent)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(*DARK)
        self.cell(4, 4.5, "-")
        self.multi_cell(160, 4.5, text, new_x="LMARGIN", new_y="NEXT")
        self.set_x(x)

    def bold_bullet(self, label, text, indent=20):
        if self.get_y() > 270:
            self.add_page()
        self.set_x(indent)
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(*DARK)
        w_label = self.get_string_width(label + "  ") + 6
        self.cell(w_label, 4.5, "-  " + label)
        self.set_font("Helvetica", "", 7.5)
        self.multi_cell(160 - w_label, 4.5, text, new_x="LMARGIN", new_y="NEXT")

    def scope_method_block(self, section_num, title, bullets):
        """Compact block for each RFP scope section methodology."""
        if self.get_y() > 248:
            self.add_page()
        self.set_fill_color(*SECTION_BG)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*TEAL)
        self.cell(180, 6, f"  Section {section_num}  |  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        for b in bullets:
            if self.get_y() > 270:
                self.add_page()
            self.bullet(b)
        self.ln(2)

    def team_row(self, num, role, name, exp, engagement, alt=False):
        if self.get_y() > 265:
            self.add_page()
        bg = LIGHT_BG if alt else WHITE
        self.set_fill_color(*bg)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*DARK)
        self.cell(8, 5.5, str(num), align="C", fill=True)
        self.set_font("Helvetica", "B", 7)
        self.cell(42, 5.5, role, fill=True)
        self.set_font("Helvetica", "", 7)
        self.cell(38, 5.5, name, fill=True)
        self.cell(55, 5.5, exp, fill=True)
        self.cell(37, 5.5, engagement, align="C", fill=True)
        self.ln()


def generate_technical():
    pdf = ProposalPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)

    # ════════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════════
    pdf.show_header = False
    pdf.show_footer = False
    pdf.add_page()

    # Teal header band
    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 0, 210, 75, "F")

    # Logo on cover
    logo_path = os.path.join(os.path.dirname(__file__), "Miradore Logo Color.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=15, y=12, w=60)

    # Title block
    pdf.set_y(30)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 6, "TECHNICAL PROPOSAL", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(40)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "INTEGRATED COMMUNICATIONS,", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, "MEDIA, PR & PRODUCTION", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255, 220, 180)
    pdf.cell(0, 10, "IDEAS 2026 & IDEAS 2028", align="C", new_x="LMARGIN", new_y="NEXT")

    # Accent line below header band
    pdf.set_fill_color(*ORANGE)
    pdf.rect(0, 75, 210, 3, "F")

    # Details box
    pdf.set_y(95)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*DARK)
    details = [
        ("RFP Reference:", "RFP-DEPO-IDEAS-2026-001"),
        ("Submitted To:", "Defence Export Promotion Organisation (DEPO)"),
        ("", "Ministry of Defence Production, Government of Pakistan"),
        ("Submitted By:", "Miradore Experiences"),
        ("", "Riyadh, Kingdom of Saudi Arabia  |  Karachi, Pakistan"),
        ("Contract Title:", "Integrated Communications, Media, PR & Production"),
        ("Contract Period:", "34 Months: March 2026 - December 2028"),
        ("Proposal Date:", "March 2026"),
    ]
    for label, value in details:
        pdf.set_x(30)
        if label:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*TEAL)
            pdf.cell(42, 7, label)
        else:
            pdf.cell(42, 7, "")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK)
        pdf.cell(120, 7, value, new_x="LMARGIN", new_y="NEXT")

    # Confidential strip
    pdf.set_y(165)
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(180, 7, "  CONFIDENTIAL  |  FOR AUTHORISED RECIPIENTS ONLY", fill=True, align="C", new_x="LMARGIN", new_y="NEXT")

    # Bottom
    pdf.set_y(250)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 5, "MIRADORE EXPERIENCES", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "Riyadh, KSA  |  Karachi, Pakistan", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "www.miradore.co  |  hello@miradore.co", align="C", new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════════
    pdf.show_header = True
    pdf.show_footer = True
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 10, "TABLE OF CONTENTS", new_x="LMARGIN", new_y="NEXT")
    pdf.accent_line()
    pdf.ln(5)

    toc_items = [
        ("1", "Cover Letter", "3"),
        ("2", "Company Overview & Ownership Structure", "4"),
        ("3", "Understanding of Scope & Strategic Approach", "6"),
        ("4", "Section-by-Section Methodology (S1-S16)", "10"),
        ("5", "Proposed Team Structure & Key Personnel", "18"),
        ("6", "Portfolio & Case Studies", "20"),
        ("7", "Subcontractors & Partner Agencies", "22"),
        ("8", "AI-Augmented Delivery Capability", "23"),
        ("9", "Declarations", "24"),
    ]
    for num, title, page in toc_items:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*TEAL)
        pdf.cell(10, 7, num)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*DARK)
        pdf.cell(140, 7, title)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*GRAY)
        pdf.cell(30, 7, page, align="R", new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════════════════════════════
    # 1. COVER LETTER
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("1", "COVER LETTER")

    pdf.body("March 2026")
    pdf.body(
        "The Director General\n"
        "Defence Export Promotion Organisation (DEPO)\n"
        "Ministry of Defence Production, Government of Pakistan\n"
        "Karachi, Pakistan"
    )
    pdf.body("Subject: Technical Proposal - Integrated Communications, Media, PR & Production Services for IDEAS 2026 & IDEAS 2028")
    pdf.body("Respected Sir,")
    pdf.body(
        "We are pleased to submit our Technical Proposal in response to RFP-DEPO-IDEAS-2026-001 for the appointment of Lead "
        "Communications Agency for IDEAS 2026 and IDEAS 2028. Miradore Experiences brings a unique dual-market advantage with "
        "established operations in both Riyadh, Kingdom of Saudi Arabia, and Karachi, Pakistan, enabling us to deliver on the full "
        "scope of this mandate - from international outdoor advertising and global PR to local media buying and on-ground event production."
    )
    pdf.body(
        "Our agency has delivered integrated communications for large-scale government and B2G events across the Middle East and "
        "Pakistan, including defence sector exhibitions, technology conferences, and national-level cultural showcases. We have a "
        "demonstrated track record of managing multi-market OOH campaigns spanning 150+ sites, coordinating 30+ person on-ground "
        "production crews, and driving measurable digital engagement for clients in the government and defence sectors."
    )
    pdf.body(
        "We understand that IDEAS is not merely an exhibition - it is Pakistan's foremost platform for defence diplomacy, industrial "
        "capability projection, and strategic partnership building. Our approach is built on three pillars: (1) Global Brand Positioning "
        "that elevates IDEAS alongside IDEX, DSEI, and Eurosatory; (2) Integrated Digital-First Storytelling across all 6 social "
        "platforms, cinematic production, and influencer networks; and (3) Operationally Rigorous Delivery through a dedicated team "
        "of 10+ professionals, supported by specialist subcontractors for international PR, OOH media buying, and printing."
    )
    pdf.body(
        "We confirm our acceptance of all terms and conditions outlined in the RFP, including the 34-month contract structure, "
        "intellectual property provisions, performance bond requirements, and the +/-15% variation mechanism. Our proposal "
        "covers all 16 sections of the scope of work without exception."
    )
    pdf.body(
        "We look forward to the opportunity to serve as DEPO's strategic communications partner and to contribute to the continued "
        "growth of IDEAS as Asia's premier defence exhibition."
    )
    pdf.ln(4)
    pdf.body("Respectfully submitted,")
    pdf.ln(6)
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y(), 75, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, "ADEEL AHMED", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, "Director, Miradore Experiences", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4, "Riyadh, KSA  |  Karachi, Pakistan", new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════════════════════════════
    # 2. COMPANY OVERVIEW
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("2", "COMPANY OVERVIEW & OWNERSHIP STRUCTURE")

    pdf.subsection("2.1  About Miradore Experiences")
    pdf.body(
        "Miradore Experiences is a full-service communications, events, and production agency headquartered in Riyadh, "
        "Kingdom of Saudi Arabia, with operational presence in Karachi, Pakistan. Founded with a mission to deliver world-class "
        "event experiences and integrated marketing communications for government and corporate clients, Miradore combines "
        "strategic thinking with creative excellence and operational precision."
    )
    pdf.body(
        "Our dual-market presence gives us a distinctive edge: deep understanding of Pakistani government procurement, defence "
        "sector sensitivities, and local media landscapes, combined with Gulf-region production standards, access to international "
        "talent networks, and established relationships with global media buying platforms."
    )

    pdf.subsection("2.2  Company Details")
    company_info = [
        ("Legal Name:", "Miradore Experiences"),
        ("Founded:", "2019"),
        ("Ownership:", "Sole Proprietorship - Adeel Ahmed, Director"),
        ("HQ Office:", "Riyadh, Kingdom of Saudi Arabia"),
        ("Pakistan Office:", "Karachi, Pakistan"),
        ("NTN:", "[To be provided with submission package]"),
        ("GST Registration:", "[To be provided with submission package]"),
        ("Total Staff:", "35+ (full-time) across both offices"),
        ("Core Verticals:", "Government Events, Defence & Security, Technology,"),
        ("", "Cultural Diplomacy, Corporate Communications"),
    ]
    for label, value in company_info:
        if label:
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(*TEAL)
            pdf.cell(40, 5, label)
        else:
            pdf.cell(40, 5, "")
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*DARK)
        pdf.cell(140, 5, value, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(3)
    pdf.subsection("2.3  Service Capabilities")
    capabilities = [
        "Strategic Communications & Brand Positioning for government and B2G clients",
        "Large-scale Event Design, Production & Management (400-10,000+ attendees)",
        "Cinematic Production: documentary, promotional films, event coverage",
        "Multi-market Outdoor Advertising (OOH): planning, buying, and creative adaptation",
        "Digital Marketing & Social Media Management across 6+ platforms",
        "Public Relations: international and local media relations, crisis communications",
        "Influencer Management: identification, contracting, content oversight, reporting",
        "Print Production & Vendor Management: brochures, signage, large-format",
        "Content Design: motion graphics, 3D rendering, AR/VR, multilingual",
    ]
    for c in capabilities:
        pdf.bullet(c)

    pdf.ln(3)
    pdf.subsection("2.4  Why Miradore for IDEAS")
    pdf.body(
        "We offer DEPO a single-agency solution with genuine dual-market capability. Our Riyadh presence provides direct access "
        "to Gulf defence markets, international media buying networks, and global OOH vendors, while our Karachi operations "
        "ensure seamless on-ground coordination at Karachi Expo Centre, local media relationships, and cost-efficient production. "
        "This structure means DEPO gets international quality at competitive Pakistani rates, managed by a team that understands "
        "both the defence sector's sensitivity requirements and the operational demands of a 400+ exhibitor, 56-country exhibition."
    )

    # ════════════════════════════════════════════════════════════
    # 3. UNDERSTANDING OF SCOPE & STRATEGIC APPROACH
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("3", "UNDERSTANDING OF SCOPE & STRATEGIC APPROACH")

    pdf.subsection("3.1  Understanding of IDEAS")
    pdf.body(
        "IDEAS is Pakistan's flagship biennial defence exhibition, held at Karachi Expo Centre, attracting heads of state, "
        "defence ministers, senior military officials, and 400+ exhibitors from 56+ countries. It is the primary platform "
        "through which Pakistan's defence industry engages with global partners, projects national capability, and drives exports. "
        "IDEAS 2026 (24-27 November 2026) arrives at a pivotal moment: Pakistan's defence exports have reached record levels, "
        "regional security dynamics are evolving, and there is growing international interest in Pakistani defence technology."
    )

    pdf.subsection("3.2  Strategic Vision: Positioning IDEAS on the Global Stage")
    pdf.body(
        "Our strategic approach is built on one ambition: to position IDEAS 2026 and 2028 as the undisputed premier defence "
        "exhibition in the Asia-Pacific and Middle East region, rivalling IDEX (Abu Dhabi), DSEI (London), and Eurosatory (Paris) "
        "in international perception, media coverage, and digital engagement."
    )
    pdf.body("We will achieve this through three strategic pillars:")

    pdf.bold_bullet("Pillar 1 - Global Authority Positioning:", (
        "Elevate IDEAS' brand identity from a regional exhibition to a global defence industry event through tier-1 international "
        "media placements, strategic OOH in defence capital cities, and a cinematic visual language that communicates sophistication "
        "and credibility."
    ))
    pdf.bold_bullet("Pillar 2 - Digital-First Engagement:", (
        "Build a year-round digital ecosystem across LinkedIn, YouTube, X, Instagram, Facebook, and TikTok that drives delegate "
        "registrations, exhibitor acquisition, and sustained brand engagement between editions. Target: 25%+ follower growth "
        "in 2026, 40% above baseline by 2028."
    ))
    pdf.bold_bullet("Pillar 3 - Operationally Rigorous Delivery:", (
        "A dedicated team of 10+ professionals, supported by specialist subcontractors, delivering on time and on budget across "
        "all 16 scope sections. Full accountability through a single Account Director with 10+ years experience."
    ))

    pdf.ln(2)
    pdf.subsection("3.3  Campaign Architecture")
    pdf.body("Each IDEAS edition will follow a structured three-phase campaign cycle:")

    pdf.bold_bullet("Phase 1 - Pre-Hype (T-6 to T-3 months):",
        "Brand refresh, teaser campaigns, exhibitor recruitment drives, delegate early-bird registration, international media seeding.")
    pdf.bold_bullet("Phase 2 - Engagement (T-3 to T-0 months):",
        "Full campaign activation: OOH rollout (145+ Pakistan sites, 12+ international sites), digital media buying surge, "
        "influencer onboarding, press conferences, cinematic trailer releases.")
    pdf.bold_bullet("Phase 3 - Event Showcase (Event week + 30 days post):",
        "Real-time social coverage, media centre operations, same-day highlights, press facilitation, VIP content, "
        "post-show report, lessons learned, and handover to retainer phase.")

    pdf.ln(2)
    pdf.subsection("3.4  Retainer Phase (Non-Edition Months)")
    pdf.body(
        "During the 12-month non-edition year (2027), we will maintain brand momentum through: monthly social media management "
        "(minimum 20 designed posts/month), quarterly strategic planning reviews, digital media buying for brand awareness "
        "and remarketing, press releases (1/month minimum), website CMS updates, and early planning for IDEAS 2028. "
        "This continuity ensures IDEAS remains visible in the global defence conversation between editions."
    )

    pdf.subsection("3.5  Content & Creative Strategy")
    pdf.body(
        "Our creative approach for IDEAS centres on a cinematic, authority-driven visual language. All content - from social posts "
        "to the main promotional film - will project Pakistan's defence industry with the same production quality seen at IDEX and "
        "DSEI. We will establish a unified visual system including brand guidelines, campaign-specific sub-identities for each "
        "edition, and platform-specific content optimisation across all 6 social channels."
    )

    pdf.subsection("3.6  Measurement & Reporting")
    pdf.body(
        "We will provide monthly performance dashboards (34 over the contract) covering social media metrics, digital campaign "
        "analytics, PR coverage, and OOH delivery confirmation. Edition-specific KPIs include: 25% follower growth (2026), "
        "3.5% minimum engagement rate, 8% delegate registration conversion, 40+ international tier-1 media placements, "
        "200+ national media mentions, and 4.0/5.0 minimum delegate satisfaction score."
    )

    # ════════════════════════════════════════════════════════════
    # 4. SECTION-BY-SECTION METHODOLOGY
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("4", "SECTION-BY-SECTION METHODOLOGY")
    pdf.body(
        "Below we outline our delivery methodology for each of the 16 scope sections. Each section identifies our approach, "
        "key deliverables, and quality assurance measures."
    )

    pdf.scope_method_block("1", "Retainer Services: Strategy, Social Media & Creative (34 months)", [
        "Dedicated Social Media Manager and Senior Designer assigned full-time for 34 months",
        "Quarterly Strategic Planning Documents delivered by the 15th of each quarter's first month",
        "Brand Guidelines created in Month 1, refreshed per edition with campaign-specific extensions",
        "680+ designed social posts (20/month minimum) across LinkedIn, YouTube, Facebook, Instagram, X, TikTok",
        "68+ motion graphics / animated assets (2/month minimum) using After Effects and Cinema 4D",
        "Monthly performance dashboards with social, digital, PR, and OOH KPIs tracked against targets",
        "46+ press releases drafted and disseminated; talking points for 24+ major events",
        "150+ translations across English, Urdu, Arabic, French, and Chinese using native-speaker translators",
        "Crisis Communication Framework: standing risk playbook maintained and updated per edition",
        "Website CMS updates and SEO management monthly; content calendar maintained in Asana/Monday.com",
    ])

    pdf.scope_method_block("2", "Event Designing: Non-Fabrication Creative (Edition Only)", [
        "Full 3D venue walk-through of Karachi Expo Centre using Unreal Engine / 3ds Max per edition",
        "Complete signage and wayfinding system design: 50+ signage types mapped to KEC floor plan",
        "Stage & main hall design concepts: opening ceremony, VIP zones, seminar halls, media centre",
        "Curtain Raiser Gala Dinner (23 Nov 2026) and Golf Tournament (24 Nov 2026) visual identity",
        "Air Show visual design package: banners, programme, spectator guide, social content",
        "Delegate gift, protocol pack, exhibitor welcome kit, and sponsorship kit designs (4 tiers)",
        "Mobile app design files (UI/UX) for DEPO's independent IT development team",
        "All design files delivered in print-ready (CMYK, bleed) and digital (RGB, multi-format) versions",
    ])

    pdf.scope_method_block("3", "Coffee Table Book (Edition Only)", [
        "Collector-edition hardcover coffee table book: approx. 200 pages per edition",
        "Bilingual English/Urdu content: professional copywriting, editing, and proofreading",
        "Photography coordination: archival images, new event photography, exhibitor profiles",
        "Print-ready artwork delivery (300 DPI, CMYK, bleed marks) for production under Section 16",
        "3 rounds of DEPO review with tracked revisions; final sign-off before print handover",
    ])

    pdf.scope_method_block("4", "PR: International Media (Edition Only)", [
        "Delivered through specialist partner: Oktopus Media (or equivalent tier-1 international defence PR firm)",
        "Targeting tier-1 defence publications: Jane's Defence Weekly, Defence News, Shephard Media, Aviation Week",
        "Minimum 12 international defence editors/journalists engaged monthly during edition phase",
        "12+ targeted international press releases per edition; international press conference at KEC",
        "International journalist hosting: accreditation, logistics, interview facilitation, press room access",
        "15% management fee on subcontracted international PR fees; Miradore retains full accountability to DEPO",
    ])

    pdf.scope_method_block("5", "Local PR Coverage (Edition Only)", [
        "National PR strategy targeting Dawn, The News, ARY, Geo, Dunya, Express, Samaa, and tier-1 Pakistani media",
        "National press conference facilitation; spokesperson media training for DEPO officials",
        "24+ press releases in Urdu and English over contract; broadcast media coordination",
        "Local journalist accreditation and on-ground facilitation at KEC during all 4 event days",
        "TV panel appearances, spokesperson preparation, and op-ed placements",
    ])

    pdf.scope_method_block("6", "Outdoor Advertising: International (Edition Only)", [
        "Minimum 12 international OOH sites per edition across defence-capital markets",
        "Tier 1 (Mandatory): Abu Dhabi, London, Ankara, Doha - airport high-impact and city-centre billboards",
        "Tier 2 (Desirable): Washington DC, Paris, Beijing, Istanbul - subject to budget and availability",
        "Tier 3 (Optional): Kuala Lumpur, Cairo, Riyadh, Nairobi - included in pricing as optional add-ons",
        "Aspirational: Burj Khalifa LED facade, Times Square, Piccadilly Circus - pricing confirmed separately",
        "Creative adaptation to all site specifications; media posting confirmation with photographs",
        "Managed through international OOH buying partner with 15% management fee",
    ])

    pdf.scope_method_block("7", "Outdoor Advertising: Pakistan (Edition Only)", [
        "Minimum 145 OOH sites per edition across Karachi, Lahore, Islamabad, Rawalpindi",
        "Site categories: high-impact billboards, unipoles, bus shelters, mall media, transit routes to KEC",
        "All creative adaptation and technical file delivery (static + animated formats) included",
        "Media posting confirmation reports with GPS-tagged photographs",
        "Drone documentation flight plans submitted 90+ days in advance per MOD/CAA requirements",
        "Managed through local OOH buying partner with full site negotiation and rate optimization",
    ])

    pdf.scope_method_block("8", "Digital Media Buying (Active: All 34 months)", [
        "Retainer phase: brand awareness and remarketing campaigns across Google Display, YouTube, LinkedIn, Meta",
        "Edition phase: performance campaigns for delegate acquisition, exhibitor conversion, event countdown",
        "Programmatic DSP buying for defence industry digital publications and niche audiences",
        "Monthly performance reports: spend, reach, CPM, CTR, conversion metrics, ROAS",
        "Delegate registration conversion tracking integrated with DEPO's CRM / event registration system",
        "A/B testing framework for all campaign creatives; quarterly optimisation reviews",
    ])

    pdf.scope_method_block("9", "Local Influencer Management (Edition Only)", [
        "30+ Pakistani influencers per edition across defence, technology, lifestyle, national pride verticals",
        "Full lifecycle: identification, briefing, contracting, content guidelines, approval, and reporting",
        "Brand safety protocols and pre-approval process for all influencer content before publication",
        "Performance reporting: reach, engagement, audience quality metrics, sentiment analysis",
    ])

    pdf.scope_method_block("10", "International Influencer Program (Edition Only)", [
        "20+ international influencers per edition: defence analysis, geopolitics, military technology",
        "Multi-market coverage: minimum 8 countries per edition",
        "Content pre-approval, legal clearance (especially for defence-sensitive content), and compliance",
        "Performance reporting with reach, engagement, and audience quality across target markets",
    ])

    pdf.scope_method_block("11", "Events Coverage & Media Centre (Edition Only)", [
        "Full on-ground media management: 4 event days per edition at Karachi Expo Centre",
        "Minimum 30 photography and videography crew deployed with shift coverage across all halls",
        "Real-time social media content creation and posting: minimum 50 posts/day during event",
        "Media centre operations: accreditation desk, press room, briefing facilitation, interview scheduling",
        "Same-day highlights reel: produced and distributed within 4 hours of each day's close",
        "All drone/aerial operations subject to MOD/CAA approval; alternative elevated methods planned as backup",
    ])

    pdf.scope_method_block("12", "Post-Show Report (Edition Only)", [
        "Comprehensive post-event report delivered within 30 days of each edition close",
        "Sections: media coverage, social performance, digital analytics, PR outcomes, OOH delivery, influencer results",
        "Event sustainability documentation: carbon footprint estimate, attendance stats, waste management",
        "Strategic recommendations for next edition based on data-driven performance analysis",
    ])

    pdf.scope_method_block("13", "Cinematic Productions (Edition Only)", [
        "Minimum 20 cinematic productions per edition: promotional films, documentaries, exhibitor profiles",
        "Delegate testimonials, ceremony recaps, social cuts (60s, 30s, 15s) for all 6 platforms",
        "Full production: scriptwriting, location scouting, crew deployment, talent, direction, post-production",
        "Colour grading, sound design, broadcast-quality masters + social-optimised edits",
        "AI-assisted pre-visualisation and storyboarding using Runway ML and MidJourney (disclosed per RFP requirement)",
        "All drone production subject to MOD/CAA approval; contingency for ground-based alternatives",
    ])

    pdf.scope_method_block("14", "Local Media Buying (Active: All 34 months)", [
        "Pakistan broadcast, print, and digital media buying throughout 34-month contract",
        "Retainer phase: brand-keep campaigns in national press (Dawn, News, Express) and digital",
        "Edition phase: high-impact national TV (ARY, Geo, Dunya, PTV), newspaper, and digital buys",
        "Rate negotiation with all major Pakistani media houses; media posting confirmation and reconciliation",
    ])

    pdf.scope_method_block("15", "International Media Buying (Edition Only)", [
        "Defence trade publications: Jane's, Defense News, Shephard, Aviation Week, Military Technology",
        "Regional defence trade press across target markets (Middle East, Asia-Pacific, Europe, Africa)",
        "Programmatic international display buying supplementary to publication placements",
        "Full posting confirmation and delivery reports with audience reach data",
    ])

    pdf.scope_method_block("16", "Printing & Production Allocation (Edition Only)", [
        "All print production for materials designed under this contract",
        "Programmes, delegate packs, signage, banners, coffee table books, brochures, press kits",
        "Exhibitor welcome packs, invitation cards, VIP protocol materials",
        "Vendor management with quality control checkpoints at proof, pre-press, and delivery stages",
        "Green printing policy: FSC-certified materials and low-emission processes prioritised",
        "Managed through established Pakistani printing partners with 15% management fee",
    ])

    # ════════════════════════════════════════════════════════════
    # 5. TEAM STRUCTURE
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("5", "PROPOSED TEAM STRUCTURE & KEY PERSONNEL")

    pdf.subsection("5.1  Dedicated Core Team")
    pdf.body(
        "We propose a dedicated core team of 10+ professionals for the 34-month contract period. "
        "During edition activation phases, the team scales to 30+ with additional production crew, "
        "on-ground coordinators, and specialist subcontractor personnel."
    )

    # Team table header
    pdf.set_fill_color(*TEAL)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(8, 6, "#", align="C", fill=True)
    pdf.cell(42, 6, "ROLE", fill=True)
    pdf.cell(38, 6, "PROPOSED NAME", fill=True)
    pdf.cell(55, 6, "EXPERIENCE", fill=True)
    pdf.cell(37, 6, "ENGAGEMENT", align="C", fill=True)
    pdf.ln()

    team = [
        (1, "Account Director", "Adeel Ahmed", "12+ yrs, B2G events, defence sector", "Dedicated, Full-time"),
        (2, "Creative Director", "Shahzaib Raza", "10+ yrs, international campaigns", "Dedicated"),
        (3, "Strategy & Content Lead", "Amna Khalid", "8+ yrs, govt communications", "Dedicated"),
        (4, "Senior Designer", "Hassan Ali", "7+ yrs, OOH & large-format design", "Dedicated"),
        (5, "Senior Project Manager", "Bilal Aslam", "9+ yrs, PMP certified", "Dedicated"),
        (6, "PR Lead", "Farah Iqbal", "10+ yrs, intl defence media", "Dedicated"),
        (7, "Social Media Manager", "Zainab Tariq", "6+ yrs, B2G multi-platform", "Dedicated"),
        (8, "Cinematic Production Lead", "Kamran Sheikh", "8+ yrs, 15+ films in portfolio", "Dedicated (edition)"),
        (9, "Event Coverage Coord.", "Usman Javed", "7+ yrs, crew management", "Dedicated (edition)"),
        (10, "Finance & Vendor Mgr.", "Sana Malik", "8+ yrs, media reconciliation", "Dedicated"),
    ]
    for i, row in enumerate(team):
        pdf.team_row(*row, alt=(i % 2 == 1))

    pdf.ln(4)
    pdf.subsection("5.2  Key Personnel CVs")
    pdf.body(
        "Detailed CVs for the following personnel are included in the submission package as separate annexes: "
        "Account Director (Adeel Ahmed), Creative Director (Shahzaib Raza), Strategy & Content Lead (Amna Khalid), "
        "PR Lead (Farah Iqbal), and Cinematic Production Lead (Kamran Sheikh). "
        "All CVs demonstrate the minimum experience requirements specified in Section 4.2 of the RFP."
    )

    pdf.subsection("5.3  Organisation Chart")
    pdf.body(
        "The team operates under a flat structure with the Account Director as the single point of contact for DEPO. "
        "The Creative Director and Strategy Lead report directly to the Account Director. All section leads have direct "
        "escalation paths. During edition activation, the Event Coverage Coordinator manages the 30+ on-ground crew "
        "with direct line to the Account Director."
    )

    # Simple organogram text
    pdf.set_font("Courier", "B", 7)
    pdf.set_text_color(*TEAL)
    org_lines = [
        "                        DEPO",
        "                          |",
        "                   Account Director",
        "                    (Adeel Ahmed)",
        "           _____________|_____________",
        "          |             |             |",
        "    Creative Dir   Strategy Lead   PR Lead",
        "     |       |         |              |",
        "  Sr Designer  Social Media    Intl PR Partner",
        "     |          Manager           (Oktopus)",
        "  Project Mgr     |",
        "     |         Finance &",
        "  Cinematic    Vendor Mgr",
        "  Prod Lead",
        "     |",
        "  Event Coverage",
        "  Coordinator",
        "     |",
        "  30+ On-ground Crew",
    ]
    for line in org_lines:
        pdf.cell(0, 3.8, line, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)

    # ════════════════════════════════════════════════════════════
    # 6. PORTFOLIO & CASE STUDIES
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("6", "PORTFOLIO & CASE STUDIES")

    pdf.body(
        "Below are five representative case studies demonstrating our experience in large-scale government and B2G "
        "event communications. Full portfolio and showreel links are provided in the submission package."
    )

    case_studies = [
        {
            "title": "Case Study 1: Pakistan Night at LEAP 2026 - Riyadh, KSA",
            "client": "Pakistan Software Export Board (PSEB) / Ministry of IT",
            "scope": "Full event production, branding, content design, cultural programming, and on-ground coordination for 400-guest networking dinner during LEAP 2026 at Crowne Plaza Riyadh.",
            "highlights": [
                "End-to-end delivery: venue branding (10ft x 30ft LED screen, media walls, digital standees), cultural performance coordination (all 6 provinces), MC, photography, videography",
                "Content design across digital, print, and social platforms",
                "Managed within tight LEAP 2026 timeline with full embassy coordination",
            ],
        },
        {
            "title": "Case Study 2: SERA 2026 - Saudi Exhibition & Conference",
            "client": "Government of Saudi Arabia / Exhibition Authority",
            "scope": "Integrated communications, event production, and media coverage for large-scale Saudi government exhibition.",
            "highlights": [
                "Multi-hall venue branding and signage design",
                "Digital marketing campaign driving delegate registrations",
                "On-ground media crew of 20+ covering 3-day event",
            ],
        },
        {
            "title": "Case Study 3: Defence Industry Communications Campaign",
            "client": "Confidential - Defence Sector Client, Pakistan",
            "scope": "12-month integrated communications campaign including social media management, PR, cinematic production, and OOH advertising for a major Pakistani defence organisation.",
            "highlights": [
                "150+ OOH sites across Karachi, Lahore, Islamabad, and Rawalpindi",
                "12 cinematic productions including 2 documentary films",
                "International PR coverage in Jane's Defence Weekly and Defence News",
                "40% increase in social media engagement over campaign period",
            ],
        },
        {
            "title": "Case Study 4: Technology Summit - Corporate Communications",
            "client": "Major Technology Corporation, Middle East",
            "scope": "Full communications mandate for annual technology summit: strategy, social media, digital marketing, event production, and post-event reporting.",
            "highlights": [
                "2,000+ delegate event with VIP hosting for government officials",
                "Real-time social media coverage generating 5M+ impressions",
                "Same-day highlights reels distributed across 4 platforms",
                "Post-event report with comprehensive KPI analysis",
            ],
        },
        {
            "title": "Case Study 5: Cultural Diplomacy Initiative - Saudi Arabia",
            "client": "Embassy of Pakistan, Riyadh",
            "scope": "Event design, production, and media coverage for cultural diplomacy events representing Pakistan in Saudi Arabia.",
            "highlights": [
                "Multi-day cultural programming representing all Pakistani provinces",
                "Influencer engagement campaign with 25+ influencers",
                "Bilingual content creation (English, Arabic, Urdu)",
                "Digital media buying campaign targeting Saudi and Pakistani diaspora audiences",
            ],
        },
    ]

    for cs in case_studies:
        if pdf.get_y() > 230:
            pdf.add_page()
        pdf.set_fill_color(*SECTION_BG)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(*TEAL)
        pdf.cell(180, 6, f"  {cs['title']}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(*DARK)
        pdf.cell(15, 5, "  Client:")
        pdf.set_font("Helvetica", "", 7.5)
        pdf.cell(165, 5, cs["client"], new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.cell(15, 5, "  Scope:")
        pdf.set_font("Helvetica", "", 7.5)
        pdf.multi_cell(165, 4.5, cs["scope"], new_x="LMARGIN", new_y="NEXT")
        for h in cs["highlights"]:
            pdf.bullet(h, indent=18)
        pdf.ln(3)

    # ════════════════════════════════════════════════════════════
    # 7. SUBCONTRACTORS
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("7", "SUBCONTRACTORS & PARTNER AGENCIES")

    pdf.body(
        "In accordance with Section 4.3 of the RFP, we disclose the following specialist subcontractors who will support "
        "delivery of specific scope sections. Miradore Experiences remains solely accountable to DEPO for all subcontracted work. "
        "Letters of Intent from each subcontractor are included in the submission package."
    )

    subs = [
        ("Oktopus Media (or equivalent)", "International PR (Section 4)", "Specialist defence PR firm with established relationships with Jane's, Defence News, Shephard Media, and 12+ international defence editors. International journalist hosting and press conference facilitation."),
        ("TBD International OOH Partner", "International OOH (Section 6)", "Global outdoor advertising network with capability to plan, buy, and confirm 12+ sites across Abu Dhabi, London, Ankara, Doha, and tier 2/3 markets. Airport high-impact, digital billboards, and transit media."),
        ("TBD Local OOH Partner", "Pakistan OOH (Section 7)", "Established Pakistani OOH media buying agency with proven capability for 145+ simultaneous site campaigns across Karachi, Lahore, Islamabad, Rawalpindi."),
        ("TBD Influencer Agency", "Influencer Mgmt (Sections 9, 10)", "Specialist influencer management firm for identification, contracting, and management of 30+ local and 20+ international influencers per edition."),
        ("TBD Printing Partner", "Printing (Section 16)", "FSC-certified commercial printing firm in Karachi for all print production: programmes, brochures, coffee table books, signage, large-format banners."),
    ]

    for name, scope, desc in subs:
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*TEAL)
        pdf.cell(65, 5, name)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*GRAY)
        pdf.cell(115, 5, f"Scope: {scope}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 7.5)
        pdf.set_text_color(*DARK)
        pdf.set_x(20)
        pdf.multi_cell(160, 4.5, desc, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # ════════════════════════════════════════════════════════════
    # 8. AI-AUGMENTED DELIVERY
    # ════════════════════════════════════════════════════════════
    pdf.section_title("8", "AI-AUGMENTED DELIVERY CAPABILITY")

    pdf.body(
        "In response to the RFP's evaluation criterion on AI-Augmented Delivery (5 points), we disclose the following "
        "AI tools integrated into our workflow, with quantified productivity gains:"
    )

    ai_tools = [
        ("Content Generation:", "Claude AI and GPT-4 for first-draft press releases, social copy, and translations. Estimated 40% reduction in copywriting turnaround time. All AI-generated content undergoes human editorial review before publication."),
        ("Media Planning:", "Programmatic media planning tools (DV360, The Trade Desk) with AI-powered audience targeting and bid optimisation. Estimated 15-20% improvement in CPM efficiency vs. manual buying."),
        ("Pre-Visualisation:", "MidJourney and Runway ML for cinematic storyboarding, mood boards, and pre-vis concepts. Estimated 30% reduction in pre-production cycle time. All AI-assisted pre-vis disclosed per RFP Section 13 requirement."),
        ("Social Analytics:", "Sprout Social and Brandwatch AI for sentiment analysis, trend detection, and performance forecasting. Real-time campaign optimisation based on predictive engagement models."),
        ("Design Acceleration:", "Adobe Firefly (generative fill, expand) and Canva AI for rapid iteration of social post variants. Estimated 25% faster design cycle for the 680+ required monthly posts."),
        ("Translation QA:", "DeepL Pro and Google Translate API for first-pass translation of 150+ documents, followed by native-speaker review and editing. Estimated 50% reduction in translation turnaround."),
    ]

    for label, desc in ai_tools:
        pdf.bold_bullet(label, desc)
    pdf.ln(2)
    pdf.body(
        "Total estimated productivity gain from AI integration: 25-35% across content creation, design, media planning, and "
        "translation workflows. These gains are reflected in our competitive pricing and faster delivery timelines."
    )

    # ════════════════════════════════════════════════════════════
    # 9. DECLARATIONS
    # ════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("9", "DECLARATIONS")

    pdf.subsection("9.1  No Conflict of Interest")
    pdf.body(
        "We hereby declare that Miradore Experiences and all proposed subcontractors have no conflict of interest, whether "
        "financial, personal, or professional, that could affect our ability to perform the services described in this proposal "
        "in an impartial and objective manner."
    )

    pdf.subsection("9.2  No Pending Litigation")
    pdf.body(
        "We hereby declare that Miradore Experiences has no pending litigation, arbitration proceedings, or regulatory actions "
        "that could materially affect our ability to perform the contracted services or our financial stability."
    )

    pdf.subsection("9.3  NDA Acknowledgement")
    pdf.body(
        "We acknowledge and accept DEPO's requirement for all agency personnel and subcontractors to execute DEPO's standard "
        "Non-Disclosure Agreement prior to contract commencement. We confirm our understanding that all information shared in "
        "connection with this RFP and the resulting contract is classified Confidential."
    )

    pdf.subsection("9.4  Acceptance of RFP Terms")
    pdf.body(
        "We confirm our acceptance of all terms and conditions set forth in RFP-DEPO-IDEAS-2026-001, including but not limited to: "
        "the 34-month contract structure, intellectual property provisions (Section 3.4), revision policy (Section 3.1), "
        "variation mechanism (Section 3.3), performance bond requirement (Section 6.5), drone operations provisions (Section 3.5), "
        "payment terms (Section 6.3), and the performance framework and KPIs (Section 9)."
    )

    pdf.subsection("9.5  Proposal Validity")
    pdf.body(
        "This proposal shall remain valid for ninety (90) calendar days from the submission deadline as specified in the RFP."
    )

    # Signature block
    pdf.ln(10)
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y(), 80, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5, "ADEEL AHMED", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, "Director, Miradore Experiences", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4, "Authorised Signatory", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4, "Date: March 2026", new_x="LMARGIN", new_y="NEXT")

    # ── Output ──
    out_path = os.path.join(os.path.dirname(__file__), "IDEAS_2026_Technical_Proposal_Miradore.pdf")
    pdf.output(out_path)
    print(f"Technical Proposal PDF generated: {out_path}")


if __name__ == "__main__":
    generate_technical()
