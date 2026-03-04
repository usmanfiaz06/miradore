"use client";

import { useRef } from "react";
import { ArrowLeft, Printer } from "lucide-react";
import { TechnicalProposalData } from "@/lib/ai-service";
import { MIRADORE_LOGO_BASE64 } from "@/lib/logo";

interface TechnicalProposalPreviewProps {
  proposal: TechnicalProposalData;
  onClose: () => void;
}

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
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body { font-family: 'Inter', sans-serif; color: #1a1a2e; }

          /* Cover Page */
          .cover-page {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 60px 40px;
            background: linear-gradient(135deg, #f0fafa 0%, #fff5f0 100%);
            page-break-after: always;
          }
          .cover-page img { max-width: 220px; height: auto; margin-bottom: 40px; }
          .cover-page .title { font-size: 28px; font-weight: 700; color: #0d7377; margin-bottom: 8px; }
          .cover-page .subtitle { font-size: 16px; color: #64748b; margin-bottom: 40px; }
          .cover-page .event-name { font-size: 22px; font-weight: 600; color: #1a1a2e; margin-bottom: 12px; }
          .cover-page .client-name { font-size: 16px; color: #64748b; }
          .cover-page .date { font-size: 12px; color: #94a3b8; margin-top: 40px; }
          .cover-page .divider { width: 60px; height: 3px; background: #0d7377; margin: 24px auto; border-radius: 2px; }

          /* Content Pages */
          .content { padding: 40px 50px; }
          .page-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 16px; border-bottom: 2px solid #0d7377; margin-bottom: 32px; }
          .page-header img { max-width: 130px; height: auto; }
          .page-header .ref { font-size: 10px; color: #94a3b8; text-align: right; }

          /* Table of Contents */
          .toc { margin-bottom: 40px; page-break-after: always; }
          .toc h2 { font-size: 18px; font-weight: 700; color: #0d7377; margin-bottom: 20px; }
          .toc-item { display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #edf2f7; }
          .toc-num { width: 32px; height: 32px; border-radius: 8px; background: #e6f5f5; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; color: #0d7377; margin-right: 16px; flex-shrink: 0; }
          .toc-title { font-size: 13px; font-weight: 500; color: #1a1a2e; }

          /* Sections */
          .proposal-section { margin-bottom: 36px; }
          .section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #e6f5f5; }
          .section-num { width: 28px; height: 28px; border-radius: 6px; background: #0d7377; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #fff; flex-shrink: 0; }
          .section-title { font-size: 16px; font-weight: 700; color: #0d7377; }
          .section-content { font-size: 12px; color: #374151; line-height: 1.8; white-space: pre-wrap; }
          .section-content p { margin-bottom: 8px; }

          /* Footer */
          .footer { margin-top: 60px; padding-top: 16px; border-top: 1px solid #e2e8f0; text-align: center; }
          .footer p { font-size: 10px; color: #94a3b8; }
          .footer .brand { color: #0d7377; font-weight: 600; }

          @media print {
            body { padding: 0; }
            .cover-page { page-break-after: always; }
            .proposal-section { page-break-inside: avoid; }
          }
        </style>
      </head>
      <body>
        ${content.innerHTML}
      </body>
      </html>
    `);
    printWindow.document.close();
    setTimeout(() => printWindow.print(), 500);
  };

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
          {/* Cover Page */}
          <div className="cover-page min-h-[600px] flex flex-col items-center justify-center text-center p-8 sm:p-16 bg-gradient-to-br from-teal-50 to-orange-50">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={MIRADORE_LOGO_BASE64}
              alt="Miradore"
              style={{ maxWidth: "220px", height: "auto", marginBottom: "32px" }}
            />
            <h1 className="title text-2xl sm:text-3xl font-bold text-teal-600 mb-2">
              TECHNICAL PROPOSAL
            </h1>
            <p className="subtitle text-sm text-text-secondary mb-8">
              Event Management &middot; Production &middot; Creative
            </p>
            <div className="divider w-16 h-[3px] bg-teal-500 mx-auto mb-8 rounded-full" />
            <h2 className="event-name text-xl font-semibold text-text-primary mb-3">
              {proposal.eventName || "Event Management Services"}
            </h2>
            <p className="client-name text-base text-text-secondary">
              Prepared for: {proposal.clientName || "The Client"}
              {proposal.clientCompany && ` — ${proposal.clientCompany}`}
            </p>
            <p className="date text-xs text-text-tertiary mt-8">
              Date: {proposal.createdAt} &middot; Ref: {proposal.id}
            </p>
          </div>

          {/* Content */}
          <div className="content p-6 sm:p-10">
            {/* Page Header */}
            <div className="page-header flex justify-between items-center pb-4 mb-8 border-b-2 border-teal-500">
              <div>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={MIRADORE_LOGO_BASE64}
                  alt="Miradore"
                  style={{ maxWidth: "130px", height: "auto" }}
                />
              </div>
              <div className="ref text-right">
                <p className="text-[10px] text-text-tertiary">Ref: {proposal.id}</p>
                <p className="text-[10px] text-text-tertiary">Date: {proposal.createdAt}</p>
              </div>
            </div>

            {/* Table of Contents */}
            {proposal.sections.length > 0 && (
              <div className="toc mb-10">
                <h2 className="text-lg font-bold text-teal-600 mb-5">Table of Contents</h2>
                {proposal.sections.map((section, i) => (
                  <div key={section.id} className="toc-item flex items-center py-2.5 border-b border-border-subtle">
                    <div className="toc-num w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center mr-4 flex-shrink-0">
                      <span className="text-xs font-bold text-teal-700">{i + 1}</span>
                    </div>
                    <span className="toc-title text-sm font-medium text-text-primary">
                      {section.title}
                    </span>
                  </div>
                ))}
              </div>
            )}

            {/* Sections */}
            {proposal.sections.map((section, i) => (
              <div key={section.id} className="proposal-section mb-10">
                <div className="section-header flex items-center gap-3 mb-4 pb-2 border-b-2 border-teal-50">
                  <div className="section-num w-7 h-7 rounded-md bg-teal-500 flex items-center justify-center flex-shrink-0">
                    <span className="text-[11px] font-bold text-white">{i + 1}</span>
                  </div>
                  <h3 className="section-title text-base font-bold text-teal-600">
                    {section.title}
                  </h3>
                </div>
                <div className="section-content text-xs text-text-secondary leading-relaxed whitespace-pre-wrap">
                  {section.content}
                </div>
              </div>
            ))}

            {/* Footer */}
            <div className="footer mt-16 pt-4 border-t border-border-subtle text-center">
              <p className="text-[10px] text-text-tertiary">
                This proposal is confidential and intended solely for the named recipient.
              </p>
              <p className="text-[10px] text-text-tertiary mt-1">
                <span className="brand text-teal-600 font-semibold">MIRADORE</span>{" "}
                &middot; Event Management &middot; Production &middot; Creative
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
