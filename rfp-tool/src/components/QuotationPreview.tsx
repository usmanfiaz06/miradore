"use client";

import { useRef, useMemo } from "react";
import { ArrowLeft, Printer } from "lucide-react";
import { QuotationData } from "@/types";
import { COUNTRIES } from "@/lib/constants";
import { formatCurrency, getCurrencyConfig } from "@/lib/utils";
import { MIRADORE_LOGO_BASE64 } from "@/lib/logo";

interface QuotationPreviewProps {
  quotation: QuotationData;
  totals: {
    subtotal: number;
    commission: number;
    subtotalWithCommission: number;
    discountAmount: number;
    afterDiscount: number;
    tax: number;
    grandTotal: number;
  };
  onClose: () => void;
}

const PRINT_STYLES = `
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Inter', sans-serif; color: #1a1a2e; padding: 30px 40px; }

  .cover-page { page-break-after: always; padding: 0; }
  .cover-header { background: linear-gradient(135deg, #0d7377, #0a5a5e); padding: 30px 40px 20px; text-align: center; }
  .cover-header::after { content: ''; display: block; height: 3px; background: linear-gradient(90deg, #e66420, #f5a623); margin-top: 16px; }
  .cover-header img { max-width: 160px; height: auto; margin-bottom: 12px; }
  .cover-header .doc-type { font-size: 9px; font-weight: 600; color: rgba(255,255,255,0.7); letter-spacing: 3px; text-transform: uppercase; }
  .cover-header .title { font-size: 22px; font-weight: 700; color: #fff; margin: 6px 0; }
  .cover-header .subtitle { font-size: 13px; color: rgb(255,220,180); font-weight: 600; }

  .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid #0d7377; }
  .logo-area img { max-width: 130px; height: auto; }
  .logo-area p { font-size: 9px; color: #64748b; margin-top: 4px; }
  .quotation-meta { text-align: right; }
  .quotation-meta h2 { font-size: 14px; font-weight: 700; color: #0d7377; letter-spacing: 1px; }
  .quotation-meta p { font-size: 9px; color: #64748b; margin-top: 2px; }

  .section { margin-bottom: 20px; }
  .section-title { font-size: 9px; font-weight: 700; color: #0d7377; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; padding-bottom: 4px; border-bottom: 1px solid #e6f5f5; }
  .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 20px; }
  .detail-item label { font-size: 8px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  .detail-item p { font-size: 10px; color: #1a1a2e; font-weight: 500; margin-top: 1px; }

  /* BOQ Table */
  .category-banner { background: #0d7377; color: #fff; padding: 5px 10px; font-size: 8px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
  table { width: 100%; border-collapse: collapse; }
  thead th { background: #1a2840; padding: 6px 8px; font-size: 7.5px; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: 0.5px; text-align: left; }
  thead th.num-col { text-align: right; }
  tbody td { padding: 6px 8px; font-size: 9px; color: #1a1a2e; border-bottom: 1px solid #edf2f7; }
  tbody td.num-col { text-align: right; font-family: 'Courier New', monospace; }
  tbody tr.alt { background: #f8fafb; }
  tbody tr.subtotal-row td { background: #e6f5f5; font-weight: 700; color: #0d7377; border-bottom: 2px solid #0d7377; }

  /* Totals */
  .totals-section { margin-top: 20px; margin-left: auto; width: 320px; }
  .total-row { display: flex; justify-content: space-between; padding: 4px 0; font-size: 10px; color: #64748b; }
  .total-row .val { font-family: 'Courier New', monospace; color: #1a1a2e; font-weight: 500; }
  .grand-total { background: #0d7377; color: #fff; padding: 10px 12px; display: flex; justify-content: space-between; margin-top: 6px; border-radius: 4px; }
  .grand-total .label { font-size: 11px; font-weight: 700; }
  .grand-total .val { font-size: 13px; font-weight: 700; font-family: 'Courier New', monospace; }

  .notes { margin-top: 20px; padding: 12px; background: #f8f9fa; border-radius: 6px; border-left: 3px solid #0d7377; }
  .notes h3 { font-size: 8px; font-weight: 700; color: #0d7377; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
  .notes p { font-size: 9px; color: #64748b; line-height: 1.5; }

  .tranches { margin-top: 20px; }
  .tranches h3 { font-size: 8px; font-weight: 700; color: #0d7377; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }

  .bank-details { margin-top: 20px; padding: 12px; background: #f0f7f7; border-radius: 6px; border: 1px solid #d1e7e7; }
  .bank-details h3 { font-size: 8px; font-weight: 700; color: #0d7377; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
  .bank-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 20px; }
  .bank-grid label { font-size: 7px; color: #94a3b8; text-transform: uppercase; }
  .bank-grid p { font-size: 9px; color: #1a1a2e; font-weight: 500; margin-top: 1px; }

  .footer { margin-top: 32px; padding-top: 10px; border-top: 1px solid #e2e8f0; text-align: center; }
  .footer p { font-size: 8px; color: #94a3b8; }
  .footer .brand { color: #0d7377; font-weight: 600; }

  .signature { margin-top: 24px; }
  .signature .line { width: 120px; border-top: 1px solid #0d7377; margin-bottom: 4px; }
  .signature .name { font-size: 9px; font-weight: 700; color: #1a1a2e; }
  .signature .role { font-size: 8px; color: #64748b; }

  @media print { body { padding: 15px 20px; } .cover-page { page-break-after: always; } }
`;

export default function QuotationPreview({
  quotation,
  totals,
  onClose,
}: QuotationPreviewProps) {
  const printRef = useRef<HTMLDivElement>(null);
  const countryConfig = COUNTRIES.find((c) => c.id === quotation.country);
  const currConfig = getCurrencyConfig(quotation.currency);

  // Group line items by category for BOQ-style layout
  const categoryGroups = useMemo(() => {
    const groups: { category: string; items: typeof quotation.lineItems; subtotal: number }[] = [];
    const catMap = new Map<string, typeof quotation.lineItems>();

    for (const item of quotation.lineItems) {
      const cat = item.category || "General";
      if (!catMap.has(cat)) catMap.set(cat, []);
      catMap.get(cat)!.push(item);
    }

    for (const [category, items] of catMap) {
      const subtotal = items.reduce((s, i) => s + i.quantity * i.unitPrice, 0);
      groups.push({ category, items, subtotal });
    }

    return groups;
  }, [quotation.lineItems]);

  const handlePrint = () => {
    const content = printRef.current;
    if (!content) return;
    const printWindow = window.open("", "_blank");
    if (!printWindow) return;
    printWindow.document.write(`<!DOCTYPE html><html><head><title>Quotation ${quotation.id}</title><style>${PRINT_STYLES}</style></head><body>${content.innerHTML}</body></html>`);
    printWindow.document.close();
    setTimeout(() => printWindow.print(), 500);
  };

  let globalIndex = 0;

  return (
    <div className="animate-fade-in">
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-6">
        <div className="flex items-center gap-3">
          <button onClick={onClose} className="p-2 rounded-lg hover:bg-surface-sunken transition-colors">
            <ArrowLeft size={20} className="text-text-secondary" />
          </button>
          <h1 className="text-xl font-bold text-text-primary">Commercial Proposal Preview</h1>
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
      <div className="bg-white rounded-2xl border border-border shadow-lg overflow-hidden max-w-4xl mx-auto overflow-x-auto">
        <div ref={printRef} className="p-4 sm:p-6 md:p-10">

          {/* ═══ COVER PAGE ═══ */}
          <div className="cover-page mb-10" style={{ pageBreakAfter: "always" }}>
            {/* Teal Header */}
            <div style={{ background: "linear-gradient(135deg, #0d7377, #0a5a5e)", padding: "30px 40px 20px", textAlign: "center", borderRadius: "12px 12px 0 0" }}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={MIRADORE_LOGO_BASE64} alt="Miradore" style={{ maxWidth: "160px", height: "auto", marginBottom: "12px" }} />
              <p style={{ fontSize: "9px", fontWeight: 600, color: "rgba(255,255,255,0.7)", letterSpacing: "3px", textTransform: "uppercase" }}>
                COMMERCIAL / FINANCIAL PROPOSAL
              </p>
              <h1 style={{ fontSize: "22px", fontWeight: 700, color: "#fff", margin: "6px 0" }}>
                QUOTATION
              </h1>
              <p style={{ fontSize: "13px", color: "rgb(255,220,180)", fontWeight: 600 }}>
                {quotation.eventName || "Event Management Services"}
              </p>
              <div style={{ height: "3px", background: "linear-gradient(90deg, #e66420, #f5a623)", marginTop: "16px" }} />
            </div>

            {/* Cover Details */}
            <div style={{ padding: "28px 40px", background: "#fafbfc", borderRadius: "0 0 12px 12px", border: "1px solid #edf2f7", borderTop: "none" }}>
              {[
                ["Ref:", quotation.id],
                ["Submitted To:", `${quotation.clientName || "—"}${quotation.clientCompany ? `, ${quotation.clientCompany}` : ""}`],
                ["Submitted By:", "Miradore Experiences — Riyadh, KSA | Karachi, Pakistan"],
                ["Currency:", `${currConfig.code} (${currConfig.name}) | All prices exclusive of sales tax`],
                ["Proposal Date:", quotation.createdAt],
                ["Validity:", `Valid until ${quotation.validUntil}`],
              ].map(([label, value]) => (
                <div key={label} style={{ display: "flex", padding: "6px 0", borderBottom: "1px solid #edf2f7" }}>
                  <span style={{ width: "140px", fontSize: "9px", fontWeight: 700, color: "#0d7377", flexShrink: 0 }}>{label}</span>
                  <span style={{ fontSize: "9px", color: "#374151" }}>{value}</span>
                </div>
              ))}

              <div style={{ background: "#1a2840", color: "#fff", textAlign: "center", padding: "8px", fontSize: "7px", fontWeight: 600, letterSpacing: "2px", marginTop: "24px", borderRadius: "4px" }}>
                CONFIDENTIAL | FOR AUTHORISED RECIPIENTS ONLY
              </div>
            </div>
          </div>

          {/* ═══ HEADER ═══ */}
          <div className="header flex flex-col sm:flex-row justify-between items-start mb-8 pb-4 gap-4" style={{ borderBottom: "2px solid #0d7377" }}>
            <div className="logo-area">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={MIRADORE_LOGO_BASE64} alt="Miradore" style={{ maxWidth: "130px", height: "auto" }} />
              <p style={{ fontSize: "9px", color: "#64748b", marginTop: "4px" }}>
                Event Management &middot; Production &middot; Creative
              </p>
              <p style={{ fontSize: "8px", color: "#94a3b8" }}>{countryConfig?.name}</p>
            </div>
            <div className="quotation-meta text-right">
              <h2 style={{ fontSize: "14px", fontWeight: 700, color: "#0d7377", letterSpacing: "1px" }}>COMMERCIAL PROPOSAL</h2>
              <p style={{ fontSize: "9px", color: "#64748b", marginTop: "2px" }}>Ref: {quotation.id}</p>
              <p style={{ fontSize: "9px", color: "#64748b" }}>Date: {quotation.createdAt}</p>
              <p style={{ fontSize: "9px", color: "#64748b" }}>Valid Until: {quotation.validUntil}</p>
            </div>
          </div>

          {/* ═══ CLIENT & EVENT DETAILS ═══ */}
          <div className="section mb-6">
            <div style={{ fontSize: "9px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "8px", paddingBottom: "4px", borderBottom: "1px solid #e6f5f5" }}>
              Client & Event Details
            </div>
            <div className="detail-grid grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2">
              {[
                ["Client", quotation.clientName || "—"],
                ["Company", quotation.clientCompany || "—"],
                ["Event", quotation.eventName || "—"],
                ["Date & Venue", `${quotation.eventDate || "TBD"}${quotation.eventVenue ? ` — ${quotation.eventVenue}` : ""}`],
                ["Attendance", `${quotation.estimatedAttendance || "—"} persons`],
                ["Currency", `${currConfig.code} (${currConfig.name})`],
              ].map(([label, value]) => (
                <div key={label} className="detail-item">
                  <label style={{ fontSize: "8px", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.5px" }}>{label}</label>
                  <p style={{ fontSize: "10px", color: "#1a1a2e", fontWeight: 500, marginTop: "1px" }}>{value}</p>
                </div>
              ))}
            </div>
          </div>

          {/* ═══ BOQ TABLE ═══ */}
          <div className="section mb-6">
            <div style={{ fontSize: "9px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "8px", paddingBottom: "4px", borderBottom: "1px solid #e6f5f5" }}>
              Bill of Quantities
            </div>

            <table className="w-full" style={{ borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={{ background: "#1a2840", padding: "6px 8px", fontSize: "7.5px", fontWeight: 700, color: "#fff", textTransform: "uppercase", letterSpacing: "0.5px", textAlign: "left", width: "30px" }}>#</th>
                  <th style={{ background: "#1a2840", padding: "6px 8px", fontSize: "7.5px", fontWeight: 700, color: "#fff", textTransform: "uppercase", letterSpacing: "0.5px", textAlign: "left" }}>Description</th>
                  <th style={{ background: "#1a2840", padding: "6px 8px", fontSize: "7.5px", fontWeight: 700, color: "#fff", textTransform: "uppercase", letterSpacing: "0.5px", textAlign: "center", width: "50px" }}>Qty</th>
                  <th style={{ background: "#1a2840", padding: "6px 8px", fontSize: "7.5px", fontWeight: 700, color: "#fff", textTransform: "uppercase", letterSpacing: "0.5px", textAlign: "right", width: "100px" }}>Unit Rate ({currConfig.code})</th>
                  <th style={{ background: "#1a2840", padding: "6px 8px", fontSize: "7.5px", fontWeight: 700, color: "#fff", textTransform: "uppercase", letterSpacing: "0.5px", textAlign: "right", width: "110px" }}>Amount ({currConfig.code})</th>
                </tr>
              </thead>
              <tbody>
                {categoryGroups.map((group) => (
                  <>
                    {/* Category Banner */}
                    <tr key={`cat-${group.category}`}>
                      <td colSpan={5} style={{ background: "#0d7377", color: "#fff", padding: "5px 8px", fontSize: "8px", fontWeight: 700, letterSpacing: "0.5px", textTransform: "uppercase" }}>
                        {group.category}
                      </td>
                    </tr>
                    {/* Items */}
                    {group.items.map((item, idx) => {
                      globalIndex++;
                      const isAlt = idx % 2 === 1;
                      return (
                        <tr key={item.id} style={{ background: isAlt ? "#f8fafb" : "#fff" }}>
                          <td style={{ padding: "6px 8px", fontSize: "9px", color: "#64748b", borderBottom: "1px solid #edf2f7", textAlign: "center" }}>{globalIndex}</td>
                          <td style={{ padding: "6px 8px", fontSize: "9px", color: "#1a1a2e", borderBottom: "1px solid #edf2f7", fontWeight: 500 }}>{item.description || "—"}</td>
                          <td style={{ padding: "6px 8px", fontSize: "9px", color: "#1a1a2e", borderBottom: "1px solid #edf2f7", textAlign: "center" }}>{item.quantity}</td>
                          <td style={{ padding: "6px 8px", fontSize: "9px", color: "#1a1a2e", borderBottom: "1px solid #edf2f7", textAlign: "right", fontFamily: "'Courier New', monospace" }}>{formatCurrency(item.unitPrice, quotation.currency)}</td>
                          <td style={{ padding: "6px 8px", fontSize: "9px", color: "#1a1a2e", borderBottom: "1px solid #edf2f7", textAlign: "right", fontFamily: "'Courier New', monospace", fontWeight: 600 }}>{formatCurrency(item.quantity * item.unitPrice, quotation.currency)}</td>
                        </tr>
                      );
                    })}
                    {/* Category Subtotal */}
                    <tr key={`sub-${group.category}`}>
                      <td colSpan={4} style={{ background: "#e6f5f5", padding: "5px 8px", fontSize: "8px", fontWeight: 700, color: "#0d7377", textAlign: "right", borderBottom: "2px solid #0d7377" }}>
                        {group.category} Subtotal:
                      </td>
                      <td style={{ background: "#e6f5f5", padding: "5px 8px", fontSize: "9px", fontWeight: 700, color: "#0d7377", textAlign: "right", fontFamily: "'Courier New', monospace", borderBottom: "2px solid #0d7377" }}>
                        {formatCurrency(group.subtotal, quotation.currency)}
                      </td>
                    </tr>
                  </>
                ))}
              </tbody>
            </table>
          </div>

          {/* ═══ COST SUMMARY ═══ */}
          <div className="totals-section ml-auto" style={{ width: "320px", marginTop: "16px" }}>
            <div style={{ fontSize: "9px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "8px", paddingBottom: "4px", borderBottom: "1px solid #e6f5f5" }}>
              Cost Summary
            </div>
            {[
              ["Subtotal", formatCurrency(totals.subtotal, quotation.currency)],
              [`Agency Commission (${quotation.agencyCommissionRate}%)`, formatCurrency(totals.commission, quotation.currency)],
              ...(quotation.discount > 0 ? [["Discount", `- ${formatCurrency(totals.discountAmount, quotation.currency)}`]] : []),
              ["Before Tax", formatCurrency(totals.afterDiscount, quotation.currency)],
              [`${COUNTRIES.find((c) => c.id === quotation.country)?.taxLabel} (${quotation.taxRate}%)`, formatCurrency(totals.tax, quotation.currency)],
            ].map(([label, val], i) => (
              <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "3px 0", fontSize: "10px", color: "#64748b" }}>
                <span>{label}</span>
                <span style={{ fontFamily: "'Courier New', monospace", color: label === "Discount" ? "#ef4444" : "#1a1a2e", fontWeight: 500 }}>{val}</span>
              </div>
            ))}
            {/* Grand Total */}
            <div style={{ background: "#0d7377", color: "#fff", padding: "10px 12px", display: "flex", justifyContent: "space-between", marginTop: "6px", borderRadius: "4px" }}>
              <span style={{ fontSize: "11px", fontWeight: 700 }}>GRAND TOTAL</span>
              <span style={{ fontSize: "13px", fontWeight: 700, fontFamily: "'Courier New', monospace" }}>{formatCurrency(totals.grandTotal, quotation.currency)}</span>
            </div>
          </div>

          {/* ═══ NOTES ═══ */}
          {quotation.notes && (
            <div style={{ marginTop: "20px", padding: "12px", background: "#f8f9fa", borderRadius: "6px", borderLeft: "3px solid #0d7377" }}>
              <h3 style={{ fontSize: "8px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "4px" }}>Notes & Scope</h3>
              <p style={{ fontSize: "9px", color: "#64748b", lineHeight: 1.5, whiteSpace: "pre-wrap" }}>{quotation.notes}</p>
            </div>
          )}

          {/* ═══ PAYMENT SCHEDULE ═══ */}
          {quotation.tranches && quotation.tranches.length > 0 && (
            <div style={{ marginTop: "20px" }}>
              <h3 style={{ fontSize: "8px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "6px" }}>Payment Schedule</h3>
              <table className="w-full" style={{ borderCollapse: "collapse" }}>
                <thead>
                  <tr>
                    <th style={{ background: "#e6f5f5", padding: "5px 8px", fontSize: "7.5px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", textAlign: "left", borderBottom: "2px solid #0d7377" }}>Tranche</th>
                    <th style={{ background: "#e6f5f5", padding: "5px 8px", fontSize: "7.5px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", textAlign: "left", borderBottom: "2px solid #0d7377" }}>Description</th>
                    <th style={{ background: "#e6f5f5", padding: "5px 8px", fontSize: "7.5px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", textAlign: "right", borderBottom: "2px solid #0d7377" }}>%</th>
                    <th style={{ background: "#e6f5f5", padding: "5px 8px", fontSize: "7.5px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", textAlign: "right", borderBottom: "2px solid #0d7377" }}>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {quotation.tranches.map((tranche) => (
                    <tr key={tranche.id} style={{ borderBottom: "1px solid #edf2f7" }}>
                      <td style={{ padding: "6px 8px", fontSize: "9px", fontWeight: 500, color: "#1a1a2e" }}>
                        {tranche.label}
                        {tranche.dueDate && <span style={{ display: "block", fontSize: "8px", color: "#94a3b8", marginTop: "2px" }}>Due: {tranche.dueDate}</span>}
                      </td>
                      <td style={{ padding: "6px 8px", fontSize: "9px", color: "#64748b" }}>{tranche.description}</td>
                      <td style={{ padding: "6px 8px", fontSize: "9px", color: "#1a1a2e", textAlign: "right", fontFamily: "'Courier New', monospace" }}>{tranche.percentage}%</td>
                      <td style={{ padding: "6px 8px", fontSize: "9px", fontWeight: 600, color: "#1a1a2e", textAlign: "right", fontFamily: "'Courier New', monospace" }}>
                        {formatCurrency(totals.grandTotal * (tranche.percentage / 100), quotation.currency)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {quotation.paymentTerms && (
                <p style={{ fontSize: "8px", color: "#64748b", marginTop: "6px", lineHeight: 1.5 }}>{quotation.paymentTerms}</p>
              )}
            </div>
          )}

          {/* ═══ BANK DETAILS ═══ */}
          {quotation.bankDetails && quotation.bankDetails.bankName && (
            <div style={{ marginTop: "20px", padding: "12px", background: "#f0f7f7", borderRadius: "6px", border: "1px solid #d1e7e7" }}>
              <h3 style={{ fontSize: "8px", fontWeight: 700, color: "#0d7377", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "8px" }}>Bank Account Details</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5">
                {[
                  ["Bank Name", quotation.bankDetails.bankName],
                  ["Account Title", quotation.bankDetails.accountTitle],
                  ["Account Number", quotation.bankDetails.accountNumber],
                  ["IBAN", quotation.bankDetails.iban],
                  ["SWIFT Code", quotation.bankDetails.swiftCode],
                  ["Branch", quotation.bankDetails.branchName],
                ].filter(([, v]) => v).map(([label, value]) => (
                  <div key={label}>
                    <label style={{ fontSize: "7px", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.5px" }}>{label}</label>
                    <p style={{ fontSize: "9px", color: "#1a1a2e", fontWeight: 500, marginTop: "1px", fontFamily: label === "IBAN" || label === "SWIFT Code" || label === "Account Number" ? "'Courier New', monospace" : "inherit" }}>{value}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ═══ SIGNATURE ═══ */}
          <div style={{ marginTop: "28px" }}>
            <div style={{ width: "120px", borderTop: "1px solid #0d7377", marginBottom: "4px" }} />
            <p style={{ fontSize: "9px", fontWeight: 700, color: "#1a1a2e" }}>ADEEL AHMED — DIRECTOR</p>
            <p style={{ fontSize: "8px", color: "#64748b" }}>Miradore Experiences</p>
            <p style={{ fontSize: "8px", color: "#64748b" }}>Authorised Signatory | {quotation.createdAt}</p>
          </div>

          {/* ═══ FOOTER ═══ */}
          <div style={{ marginTop: "24px", paddingTop: "10px", borderTop: "1px solid #e2e8f0", textAlign: "center" }}>
            <p style={{ fontSize: "8px", color: "#94a3b8" }}>
              This quotation is valid for 30 days from the date of issue.
            </p>
            <p style={{ fontSize: "8px", color: "#94a3b8", marginTop: "2px" }}>
              <span style={{ color: "#0d7377", fontWeight: 600 }}>MIRADORE EXPERIENCES</span> | Event Management &middot; Production &middot; Creative
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
