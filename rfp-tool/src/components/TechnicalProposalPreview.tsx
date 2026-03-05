"use client";

import { useRef } from "react";
import { ArrowLeft, Printer } from "lucide-react";
import { TechnicalProposalData } from "@/lib/ai-service";
import { MIRADORE_LOGO_BASE64 } from "@/lib/logo";

interface TechnicalProposalPreviewProps {
  proposal: TechnicalProposalData;
  onClose: () => void;
}

const PRINT_STYLES = `
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Inter', sans-serif; color: #1a1a2e; }

  /* Cover Page */
  .cover-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 0;
    page-break-after: always;
    position: relative;
    overflow: hidden;
  }
  .cover-header {
    background: linear-gradient(135deg, #0d7377, #0a5a5e);
    padding: 40px 50px 30px;
    text-align: center;
    position: relative;
  }
  .cover-header::after {
    content: '';
    display: block;
    height: 4px;
    background: linear-gradient(90deg, #e66420, #f5a623);
    margin-top: 20px;
  }
  .cover-header img { max-width: 180px; height: auto; margin-bottom: 16px; }
  .cover-header .doc-type { font-size: 10px; font-weight: 600; color: rgba(255,255,255,0.7); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 8px; }
  .cover-header .title { font-size: 26px; font-weight: 700; color: #fff; margin-bottom: 6px; line-height: 1.2; }
  .cover-header .subtitle { font-size: 14px; color: rgba(255,220,180,1); font-weight: 600; }

  .cover-details {
    padding: 40px 60px;
    flex: 1;
  }
  .cover-detail-row {
    display: flex;
    padding: 8px 0;
    border-bottom: 1px solid #edf2f7;
  }
  .cover-detail-label {
    width: 160px;
    font-size: 10px;
    font-weight: 700;
    color: #0d7377;
    flex-shrink: 0;
  }
  .cover-detail-value {
    font-size: 10px;
    color: #374151;
    flex: 1;
  }

  .cover-confidential {
    background: #1a2840;
    color: #fff;
    text-align: center;
    padding: 10px;
    font-size: 8px;
    font-weight: 600;
    letter-spacing: 2px;
    margin: 30px 60px;
    border-radius: 4px;
  }

  .cover-footer {
    text-align: center;
    padding: 24px;
  }
  .cover-footer .brand { font-size: 11px; font-weight: 700; color: #0d7377; }
  .cover-footer .info { font-size: 9px; color: #94a3b8; margin-top: 3px; }

  /* Content Pages */
  .content { padding: 30px 50px 40px; }
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    border-bottom: 2px solid #0d7377;
    margin-bottom: 24px;
  }
  .page-header img { max-width: 100px; height: auto; }
  .page-header .ref { font-size: 7px; color: #94a3b8; text-align: right; letter-spacing: 0.5px; }

  /* Table of Contents */
  .toc { margin-bottom: 30px; page-break-after: always; }
  .toc h2 {
    font-size: 16px;
    font-weight: 700;
    color: #0d7377;
    margin-bottom: 16px;
    padding-bottom: 6px;
    border-bottom: 2px solid #e6f5f5;
  }
  .toc-item {
    display: flex;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #f1f5f9;
  }
  .toc-num {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: #0d7377;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    color: #fff;
    margin-right: 14px;
    flex-shrink: 0;
  }
  .toc-title { font-size: 12px; font-weight: 500; color: #1a1a2e; }
  .toc-page { margin-left: auto; font-size: 10px; color: #94a3b8; padding-left: 12px; }

  /* Sections */
  .proposal-section { margin-bottom: 28px; }
  .section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid #e6f5f5;
  }
  .section-num {
    width: 26px;
    height: 26px;
    border-radius: 5px;
    background: #0d7377;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
  }
  .section-title {
    font-size: 14px;
    font-weight: 700;
    color: #0d7377;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .section-content {
    font-size: 11px;
    color: #374151;
    line-height: 1.85;
    white-space: pre-wrap;
  }
  .section-content p { margin-bottom: 6px; }

  /* Footer */
  .page-footer {
    margin-top: 40px;
    padding-top: 12px;
    border-top: 1px solid #e2e8f0;
    text-align: center;
  }
  .page-footer p { font-size: 8px; color: #94a3b8; }
  .page-footer .brand { color: #0d7377; font-weight: 600; }

  @media print {
    body { padding: 0; }
    .cover-page { page-break-after: always; }
    .toc { page-break-after: always; }
    .proposal-section { page-break-inside: avoid; }
  }
`;

export default function TechnicalProposalPreview({
  proposal,
  onClose,
}: TechnicalProposalPreviewProps) {
  const printRef = useRef<HTMLDivElement>(null);

  const handlePrint = () => {
    const content = printRef.current;
    if (!content) return;

    const printWindow = window.open("", "_blank");
    if (!printWindow) return;

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Technical Proposal - ${proposal.eventName}</title>
        <style>${PRINT_STYLES}</style>
      </head>
      <body>
        ${content.innerHTML}
      </body>
      </html>
    `);
    printWindow.document.close();
    setTimeout(() => printWindow.print(), 500);
  };

  const totalPages = proposal.sections.length + 2; // cover + toc + sections

  return (
    <div className="animate-fade-in">
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-6">
        <div className="flex items-center gap-3">
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-surface-sunken transition-colors"
          >
            <ArrowLeft size={20} className="text-text-secondary" />
          </button>
          <h1 className="text-xl font-bold text-text-primary">
            Technical Proposal Preview
          </h1>
        </div>
        <button
          onClick={handlePrint}
          className="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-border text-sm font-medium text-text-primary hover:bg-surface-sunken transition-colors"
        >
          <Printer size={16} />
          Print / Save PDF
        </button>
      </div>

      {/* Document */}
      <div className="bg-white rounded-2xl border border-border shadow-lg overflow-hidden max-w-4xl mx-auto">
        <div ref={printRef}>
          {/* ═══ COVER PAGE ═══ */}
          <div className="cover-page" style={{ minHeight: "700px" }}>
            {/* Teal Header Band */}
            <div
              className="cover-header text-center relative"
              style={{
                background: "linear-gradient(135deg, #0d7377, #0a5a5e)",
                padding: "40px 50px 30px",
              }}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={MIRADORE_LOGO_BASE64}
                alt="Miradore"
                style={{ maxWidth: "180px", height: "auto", marginBottom: "16px" }}
              />
              <p
                className="doc-type"
                style={{
                  fontSize: "10px",
                  fontWeight: 600,
                  color: "rgba(255,255,255,0.7)",
                  letterSpacing: "3px",
                  textTransform: "uppercase",
                  marginBottom: "8px",
                }}
              >
                TECHNICAL PROPOSAL
              </p>
              <h1
                className="title"
                style={{
                  fontSize: "24px",
                  fontWeight: 700,
                  color: "#fff",
                  marginBottom: "6px",
                  lineHeight: 1.2,
                }}
              >
                {proposal.contractTitle || proposal.eventName || "Event Management Services"}
              </h1>
              <p
                className="subtitle"
                style={{
                  fontSize: "14px",
                  color: "rgb(255,220,180)",
                  fontWeight: 600,
                }}
              >
                {proposal.eventName}
              </p>
              {/* Orange Accent */}
              <div
                style={{
                  height: "4px",
                  background: "linear-gradient(90deg, #e66420, #f5a623)",
                  marginTop: "20px",
                }}
              />
            </div>

            {/* Cover Details */}
            <div className="cover-details" style={{ padding: "36px 60px", flex: 1 }}>
              {[
                ["RFP Reference:", proposal.rfpReference || proposal.id],
                ["Submitted To:", proposal.submittedTo || proposal.clientName],
                [
                  "Submitted By:",
                  "Miradore Experiences\nRiyadh, Kingdom of Saudi Arabia | Karachi, Pakistan",
                ],
                [
                  "Contract Title:",
                  proposal.contractTitle || proposal.eventName || "Event Management Services",
                ],
                ["Contract Period:", proposal.contractPeriod || "As per RFP"],
                ["Proposal Date:", proposal.createdAt ? new Date(proposal.createdAt).toLocaleDateString("en-GB", { month: "long", year: "numeric" }) : "March 2026"],
              ].map(([label, value]) => (
                <div
                  key={label}
                  className="cover-detail-row flex py-2 border-b border-border-subtle"
                >
                  <span
                    className="cover-detail-label"
                    style={{
                      width: "160px",
                      fontSize: "10px",
                      fontWeight: 700,
                      color: "#0d7377",
                      flexShrink: 0,
                    }}
                  >
                    {label}
                  </span>
                  <span
                    className="cover-detail-value"
                    style={{
                      fontSize: "10px",
                      color: "#374151",
                      whiteSpace: "pre-line",
                    }}
                  >
                    {value}
                  </span>
                </div>
              ))}

              {/* Confidential Badge */}
              <div
                className="cover-confidential"
                style={{
                  background: "#1a2840",
                  color: "#fff",
                  textAlign: "center",
                  padding: "10px",
                  fontSize: "8px",
                  fontWeight: 600,
                  letterSpacing: "2px",
                  marginTop: "30px",
                  borderRadius: "4px",
                }}
              >
                CONFIDENTIAL | FOR AUTHORISED RECIPIENTS ONLY
              </div>
            </div>

            {/* Cover Footer */}
            <div className="cover-footer text-center pb-6">
              <p
                className="brand"
                style={{ fontSize: "11px", fontWeight: 700, color: "#0d7377" }}
              >
                MIRADORE EXPERIENCES
              </p>
              <p
                className="info"
                style={{ fontSize: "9px", color: "#94a3b8", marginTop: "3px" }}
              >
                Riyadh, KSA | Karachi, Pakistan | www.miradore.co | hello@miradore.co
              </p>
            </div>
          </div>

          {/* ═══ CONTENT ═══ */}
          <div className="content p-6 sm:p-10">
            {/* Page Header */}
            <div
              className="page-header flex justify-between items-center pb-3 mb-6"
              style={{ borderBottom: "2px solid #0d7377" }}
            >
              <div>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={MIRADORE_LOGO_BASE64}
                  alt="Miradore"
                  style={{ maxWidth: "100px", height: "auto" }}
                />
              </div>
              <div className="ref text-right">
                <p style={{ fontSize: "7px", color: "#94a3b8", letterSpacing: "0.5px" }}>
                  TECHNICAL PROPOSAL | {proposal.rfpReference || proposal.id}
                </p>
              </div>
            </div>

            {/* Table of Contents */}
            {proposal.sections.length > 0 && (
              <div className="toc mb-10">
                <h2
                  style={{
                    fontSize: "16px",
                    fontWeight: 700,
                    color: "#0d7377",
                    marginBottom: "16px",
                    paddingBottom: "6px",
                    borderBottom: "2px solid #e6f5f5",
                  }}
                >
                  TABLE OF CONTENTS
                </h2>
                {proposal.sections.map((section, i) => (
                  <div
                    key={section.id}
                    className="toc-item flex items-center py-2"
                    style={{ borderBottom: "1px solid #f1f5f9" }}
                  >
                    <div
                      className="toc-num w-7 h-7 rounded-md flex items-center justify-center mr-3.5 flex-shrink-0"
                      style={{ background: "#0d7377" }}
                    >
                      <span style={{ fontSize: "11px", fontWeight: 700, color: "#fff" }}>
                        {i + 1}
                      </span>
                    </div>
                    <span style={{ fontSize: "12px", fontWeight: 500, color: "#1a1a2e" }}>
                      {section.title}
                    </span>
                    <span
                      style={{
                        marginLeft: "auto",
                        fontSize: "10px",
                        color: "#94a3b8",
                        paddingLeft: "12px",
                      }}
                    >
                      {i + 3}
                    </span>
                  </div>
                ))}
              </div>
            )}

            {/* Sections */}
            {proposal.sections.map((section, i) => (
              <div key={section.id} className="proposal-section mb-8">
                <div
                  className="section-header flex items-center gap-2.5 mb-3 pb-1.5"
                  style={{ borderBottom: "2px solid #e6f5f5" }}
                >
                  <div
                    className="section-num w-6 h-6 rounded flex items-center justify-center flex-shrink-0"
                    style={{ background: "#0d7377" }}
                  >
                    <span style={{ fontSize: "11px", fontWeight: 700, color: "#fff" }}>
                      {i + 1}
                    </span>
                  </div>
                  <h3
                    className="section-title"
                    style={{
                      fontSize: "13px",
                      fontWeight: 700,
                      color: "#0d7377",
                      textTransform: "uppercase",
                      letterSpacing: "0.5px",
                    }}
                  >
                    {section.title}
                  </h3>
                </div>
                <div
                  className="section-content"
                  style={{
                    fontSize: "11px",
                    color: "#374151",
                    lineHeight: 1.85,
                    whiteSpace: "pre-wrap",
                  }}
                >
                  {section.content}
                </div>
              </div>
            ))}

            {/* Footer */}
            <div
              className="page-footer mt-12 pt-3 text-center"
              style={{ borderTop: "1px solid #e2e8f0" }}
            >
              <p style={{ fontSize: "8px", color: "#94a3b8" }}>
                This proposal is confidential and intended solely for the named recipient.
              </p>
              <p style={{ fontSize: "8px", color: "#94a3b8", marginTop: "3px" }}>
                <span style={{ color: "#0d7377", fontWeight: 600 }}>
                  MIRADORE EXPERIENCES
                </span>{" "}
                | Riyadh, KSA | Karachi, Pakistan | Page {totalPages}/{totalPages}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
