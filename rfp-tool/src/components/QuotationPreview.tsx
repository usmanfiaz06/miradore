"use client";

import { useRef } from "react";
import {
  ArrowLeft,
  Printer,
} from "lucide-react";
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

export default function QuotationPreview({
  quotation,
  totals,
  onClose,
}: QuotationPreviewProps) {
  const printRef = useRef<HTMLDivElement>(null);
  const countryConfig = COUNTRIES.find((c) => c.id === quotation.country);
  const currConfig = getCurrencyConfig(quotation.currency);

  const handlePrint = () => {
    const content = printRef.current;
    if (!content) return;

    const printWindow = window.open("", "_blank");
    if (!printWindow) return;

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Quotation ${quotation.id}</title>
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body { font-family: 'Inter', sans-serif; color: #1a1a2e; padding: 40px; }
          .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; padding-bottom: 24px; border-bottom: 3px solid #0d7377; }
          .logo-area img { max-width: 180px; height: auto; }
          .logo-area p { font-size: 11px; color: #64748b; margin-top: 6px; }
          .quotation-meta { text-align: right; }
          .quotation-meta h2 { font-size: 18px; font-weight: 600; color: #0d7377; }
          .quotation-meta p { font-size: 11px; color: #64748b; margin-top: 2px; }
          .section { margin-bottom: 24px; }
          .section-title { font-size: 11px; font-weight: 600; color: #0d7377; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px; }
          .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 24px; }
          .detail-item label { font-size: 10px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }
          .detail-item p { font-size: 12px; color: #1a1a2e; font-weight: 500; margin-top: 2px; }
          table { width: 100%; border-collapse: collapse; margin-top: 8px; }
          thead th { background: #f0f7f7; padding: 8px 12px; font-size: 10px; font-weight: 600; color: #0d7377; text-transform: uppercase; letter-spacing: 0.05em; text-align: left; border-bottom: 2px solid #0d7377; }
          thead th:nth-child(4), thead th:nth-child(5) { text-align: right; }
          tbody td { padding: 10px 12px; font-size: 11px; color: #1a1a2e; border-bottom: 1px solid #e2e8f0; }
          tbody td:nth-child(3) { text-align: center; }
          tbody td:nth-child(4), tbody td:nth-child(5) { text-align: right; font-family: 'Courier New', monospace; }
          .totals { margin-top: 24px; margin-left: auto; width: 300px; }
          .total-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 12px; color: #64748b; }
          .total-row span:last-child { font-family: 'Courier New', monospace; color: #1a1a2e; font-weight: 500; }
          .grand-total { border-top: 3px solid #0d7377; margin-top: 8px; padding-top: 12px; display: flex; justify-content: space-between; }
          .grand-total span:first-child { font-size: 14px; font-weight: 700; color: #1a1a2e; }
          .grand-total span:last-child { font-size: 16px; font-weight: 700; color: #0d7377; font-family: 'Courier New', monospace; }
          .notes { margin-top: 32px; padding: 16px; background: #f8f9fa; border-radius: 8px; border-left: 3px solid #0d7377; }
          .notes h3 { font-size: 11px; font-weight: 600; color: #0d7377; text-transform: uppercase; margin-bottom: 6px; }
          .notes p { font-size: 11px; color: #64748b; line-height: 1.5; }
          .footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #e2e8f0; text-align: center; }
          .footer p { font-size: 10px; color: #94a3b8; }
          .footer .brand { color: #0d7377; font-weight: 600; }
          @media print { body { padding: 20px; } }
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
      {/* Preview Toolbar */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-surface-sunken transition-colors"
          >
            <ArrowLeft size={20} className="text-text-secondary" />
          </button>
          <h1 className="text-xl font-bold text-text-primary">
            Quotation Preview
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handlePrint}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-border text-sm font-medium text-text-primary hover:bg-surface-sunken transition-colors"
          >
            <Printer size={16} />
            Print / Save PDF
          </button>
        </div>
      </div>

      {/* Preview Document */}
      <div className="bg-white rounded-2xl border border-border shadow-lg overflow-hidden max-w-4xl mx-auto">
        <div ref={printRef} className="p-10">
          {/* Header */}
          <div className="header flex justify-between items-start mb-10 pb-6 border-b-[3px] border-teal-500">
            <div className="logo-area">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={MIRADORE_LOGO_BASE64}
                alt="Miradore"
                width={180}
                height={50}
                style={{ height: "auto", maxWidth: "180px" }}
              />
              <p className="text-xs text-text-secondary mt-2">
                Event Management &middot; Production &middot; Creative
              </p>
              <p className="text-xs text-text-tertiary mt-0.5">
                {countryConfig?.name}
              </p>
            </div>
            <div className="quotation-meta text-right">
              <h2 className="text-lg font-semibold text-teal-600">
                QUOTATION
              </h2>
              <p className="text-xs text-text-secondary mt-1">
                Ref: {quotation.id}
              </p>
              <p className="text-xs text-text-secondary">
                Date: {quotation.createdAt}
              </p>
              <p className="text-xs text-text-secondary">
                Valid Until: {quotation.validUntil}
              </p>
            </div>
          </div>

          {/* Client & Event Details */}
          <div className="section mb-8">
            <div className="section-title text-xs font-semibold text-teal-600 uppercase tracking-wider mb-3">
              Client & Event Details
            </div>
            <div className="detail-grid grid grid-cols-2 gap-x-8 gap-y-3">
              <div className="detail-item">
                <label className="text-[10px] text-text-tertiary uppercase tracking-wide">
                  Client
                </label>
                <p className="text-sm text-text-primary font-medium mt-0.5">
                  {quotation.clientName || "—"}
                </p>
              </div>
              <div className="detail-item">
                <label className="text-[10px] text-text-tertiary uppercase tracking-wide">
                  Company
                </label>
                <p className="text-sm text-text-primary font-medium mt-0.5">
                  {quotation.clientCompany || "—"}
                </p>
              </div>
              <div className="detail-item">
                <label className="text-[10px] text-text-tertiary uppercase tracking-wide">
                  Event
                </label>
                <p className="text-sm text-text-primary font-medium mt-0.5">
                  {quotation.eventName || "—"}
                </p>
              </div>
              <div className="detail-item">
                <label className="text-[10px] text-text-tertiary uppercase tracking-wide">
                  Date & Venue
                </label>
                <p className="text-sm text-text-primary font-medium mt-0.5">
                  {quotation.eventDate || "TBD"}
                  {quotation.eventVenue && ` — ${quotation.eventVenue}`}
                </p>
              </div>
              <div className="detail-item">
                <label className="text-[10px] text-text-tertiary uppercase tracking-wide">
                  Attendance
                </label>
                <p className="text-sm text-text-primary font-medium mt-0.5">
                  {quotation.estimatedAttendance || "—"} persons
                </p>
              </div>
              <div className="detail-item">
                <label className="text-[10px] text-text-tertiary uppercase tracking-wide">
                  Currency
                </label>
                <p className="text-sm text-text-primary font-medium mt-0.5">
                  {currConfig.code} ({currConfig.name})
                </p>
              </div>
            </div>
          </div>

          {/* Line Items Table */}
          <div className="section mb-8">
            <div className="section-title text-xs font-semibold text-teal-600 uppercase tracking-wider mb-3">
              Cost Breakdown
            </div>
            <table className="w-full border-collapse">
              <thead>
                <tr>
                  <th className="bg-teal-50 px-3 py-2.5 text-left text-[10px] font-semibold text-teal-700 uppercase tracking-wide border-b-2 border-teal-500">
                    #
                  </th>
                  <th className="bg-teal-50 px-3 py-2.5 text-left text-[10px] font-semibold text-teal-700 uppercase tracking-wide border-b-2 border-teal-500">
                    Description
                  </th>
                  <th className="bg-teal-50 px-3 py-2.5 text-center text-[10px] font-semibold text-teal-700 uppercase tracking-wide border-b-2 border-teal-500">
                    Qty
                  </th>
                  <th className="bg-teal-50 px-3 py-2.5 text-right text-[10px] font-semibold text-teal-700 uppercase tracking-wide border-b-2 border-teal-500">
                    Unit Price
                  </th>
                  <th className="bg-teal-50 px-3 py-2.5 text-right text-[10px] font-semibold text-teal-700 uppercase tracking-wide border-b-2 border-teal-500">
                    Amount
                  </th>
                </tr>
              </thead>
              <tbody>
                {quotation.lineItems.map((item, index) => (
                  <tr key={item.id} className="border-b border-border-subtle">
                    <td className="px-3 py-2.5 text-xs text-text-tertiary">
                      {index + 1}
                    </td>
                    <td className="px-3 py-2.5">
                      <p className="text-xs font-medium text-text-primary">
                        {item.description || "—"}
                      </p>
                      {item.category && (
                        <p className="text-[10px] text-text-tertiary mt-0.5">
                          {item.category}
                        </p>
                      )}
                    </td>
                    <td className="px-3 py-2.5 text-xs text-text-primary text-center">
                      {item.quantity}
                    </td>
                    <td className="px-3 py-2.5 text-xs text-text-primary text-right font-mono">
                      {formatCurrency(item.unitPrice, quotation.currency)}
                    </td>
                    <td className="px-3 py-2.5 text-xs font-semibold text-text-primary text-right font-mono">
                      {formatCurrency(
                        item.quantity * item.unitPrice,
                        quotation.currency
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Totals */}
          <div className="totals ml-auto w-80">
            <div className="total-row flex justify-between py-1.5 text-xs">
              <span className="text-text-secondary">Subtotal</span>
              <span className="font-mono font-medium text-text-primary">
                {formatCurrency(totals.subtotal, quotation.currency)}
              </span>
            </div>
            <div className="total-row flex justify-between py-1.5 text-xs">
              <span className="text-text-secondary">
                Agency Commission ({quotation.agencyCommissionRate}%)
              </span>
              <span className="font-mono font-medium text-text-primary">
                {formatCurrency(totals.commission, quotation.currency)}
              </span>
            </div>
            {quotation.discount > 0 && (
              <div className="total-row flex justify-between py-1.5 text-xs">
                <span className="text-text-secondary">Discount</span>
                <span className="font-mono font-medium text-red-500">
                  - {formatCurrency(totals.discountAmount, quotation.currency)}
                </span>
              </div>
            )}
            <div className="total-row flex justify-between py-1.5 text-xs border-t border-border-subtle mt-2 pt-2">
              <span className="text-text-secondary">Before Tax</span>
              <span className="font-mono font-medium text-text-primary">
                {formatCurrency(totals.afterDiscount, quotation.currency)}
              </span>
            </div>
            <div className="total-row flex justify-between py-1.5 text-xs">
              <span className="text-text-secondary">
                {COUNTRIES.find((c) => c.id === quotation.country)?.taxLabel} (
                {quotation.taxRate}%)
              </span>
              <span className="font-mono font-medium text-text-primary">
                {formatCurrency(totals.tax, quotation.currency)}
              </span>
            </div>
            <div className="grand-total flex justify-between border-t-[3px] border-teal-500 mt-3 pt-4">
              <span className="text-sm font-bold text-text-primary">
                Grand Total
              </span>
              <span className="text-base font-bold text-teal-700 font-mono">
                {formatCurrency(totals.grandTotal, quotation.currency)}
              </span>
            </div>
          </div>

          {/* Notes */}
          {quotation.notes && (
            <div className="notes mt-8 p-4 bg-surface-sunken rounded-lg border-l-[3px] border-teal-500">
              <h3 className="text-[10px] font-semibold text-teal-600 uppercase tracking-wide mb-2">
                Notes & Scope
              </h3>
              <p className="text-xs text-text-secondary leading-relaxed whitespace-pre-wrap">
                {quotation.notes}
              </p>
            </div>
          )}

          {/* Footer */}
          <div className="footer mt-12 pt-4 border-t border-border-subtle text-center">
            <p className="text-[10px] text-text-tertiary">
              This quotation is valid for 30 days from the date of issue.
            </p>
            <p className="text-[10px] text-text-tertiary mt-1">
              <span className="brand text-teal-600 font-semibold">
                MIRADORE
              </span>{" "}
              &middot; Event Management &middot; Production &middot; Creative
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
