"use client";

import { useState, useMemo } from "react";
import {
  Plus,
  Trash2,
  Save,
  Eye,
  Download,
  ArrowLeft,
  GripVertical,
  Percent,
  Receipt,
  Calculator,
  ChevronDown,
  FileText,
  Copy,
} from "lucide-react";
import { QuotationData, LineItem, Country, Currency, RFPEvent } from "@/types";
import { COUNTRIES, CURRENCIES, EVENT_CATEGORIES, TIER_PRICING, DEFAULT_LINE_ITEMS_BY_TIER } from "@/lib/constants";
import {
  generateId,
  formatCurrency,
  formatNumber,
  calculateQuotationTotals,
  generateQuotationNumber,
  getDateString,
  getCurrencyConfig,
} from "@/lib/utils";
import CountryTabs from "./CountryTabs";
import QuotationPreview from "./QuotationPreview";

interface QuotationBuilderProps {
  event: RFPEvent | null;
  onBack: () => void;
  onSave: (quotation: QuotationData) => void;
}

function createLineItem(
  category: string = "",
  description: string = "",
  quantity: number = 1,
  unitPrice: number = 0
): LineItem {
  return {
    id: generateId(),
    category,
    description,
    quantity,
    unitPrice,
    notes: "",
  };
}

function createDefaultQuotation(
  event: RFPEvent | null,
  country: Country
): QuotationData {
  const countryConfig = COUNTRIES.find((c) => c.id === country)!;
  const tier = event?.eventTier || "Medium";
  const basePrice = TIER_PRICING[tier]?.[country] || TIER_PRICING["Medium"][country];
  const templates = DEFAULT_LINE_ITEMS_BY_TIER[tier] || DEFAULT_LINE_ITEMS_BY_TIER["Medium"];

  const lineItems: LineItem[] = templates.map((t) =>
    createLineItem(
      t.category,
      t.description,
      t.quantity,
      Math.round(basePrice * t.priceMultiplier)
    )
  );

  return {
    id: generateQuotationNumber(),
    clientName: "",
    clientCompany: "",
    eventName: event?.eventName || "",
    eventDate: event?.date || "",
    eventVenue: event?.venue || "",
    eventType: event?.category || "",
    estimatedAttendance: event?.estimatedAttendance || 0,
    country,
    currency: countryConfig.defaultCurrency,
    lineItems,
    agencyCommissionRate: 15,
    taxRate: countryConfig.defaultTaxRate,
    discount: 0,
    notes: event?.keyServices || "",
    createdAt: getDateString(),
    validUntil: getDateString(30),
  };
}

export default function QuotationBuilder({
  event,
  onBack,
  onSave,
}: QuotationBuilderProps) {
  const [activeCountry, setActiveCountry] = useState<Country>("ksa");
  const [quotation, setQuotation] = useState<QuotationData>(() =>
    createDefaultQuotation(event, "ksa")
  );
  const [showPreview, setShowPreview] = useState(false);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(
    new Set(EVENT_CATEGORIES)
  );

  const totals = useMemo(
    () => calculateQuotationTotals(quotation),
    [quotation]
  );

  const currencyConfig = getCurrencyConfig(quotation.currency);

  const handleCountryChange = (country: Country) => {
    const countryConfig = COUNTRIES.find((c) => c.id === country)!;
    setActiveCountry(country);
    setQuotation((prev) => ({
      ...prev,
      country,
      currency: countryConfig.defaultCurrency,
      taxRate: countryConfig.defaultTaxRate,
    }));
  };

  const handleCurrencyChange = (currency: Currency) => {
    setQuotation((prev) => ({ ...prev, currency }));
  };

  const updateField = (field: keyof QuotationData, value: unknown) => {
    setQuotation((prev) => ({ ...prev, [field]: value }));
  };

  const updateLineItem = (
    id: string,
    field: keyof LineItem,
    value: unknown
  ) => {
    setQuotation((prev) => ({
      ...prev,
      lineItems: prev.lineItems.map((item) =>
        item.id === id ? { ...item, [field]: value } : item
      ),
    }));
  };

  const addLineItem = () => {
    setQuotation((prev) => ({
      ...prev,
      lineItems: [...prev.lineItems, createLineItem()],
    }));
  };

  const removeLineItem = (id: string) => {
    setQuotation((prev) => ({
      ...prev,
      lineItems: prev.lineItems.filter((item) => item.id !== id),
    }));
  };

  const duplicateLineItem = (id: string) => {
    setQuotation((prev) => {
      const itemIndex = prev.lineItems.findIndex((item) => item.id === id);
      if (itemIndex === -1) return prev;
      const original = prev.lineItems[itemIndex];
      const duplicate = { ...original, id: generateId() };
      const newItems = [...prev.lineItems];
      newItems.splice(itemIndex + 1, 0, duplicate);
      return { ...prev, lineItems: newItems };
    });
  };

  const handleSave = () => {
    onSave(quotation);
  };

  if (showPreview) {
    return (
      <QuotationPreview
        quotation={quotation}
        totals={totals}
        onClose={() => setShowPreview(false)}
      />
    );
  }

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={onBack}
            className="p-2 rounded-lg hover:bg-surface-sunken transition-colors"
          >
            <ArrowLeft size={20} className="text-text-secondary" />
          </button>
          <div>
            <h1 className="text-xl font-bold text-text-primary">
              {event ? `Quotation — ${event.eventName}` : "New Quotation"}
            </h1>
            <p className="text-sm text-text-secondary mt-0.5">
              {quotation.id} &middot; Created {quotation.createdAt}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowPreview(true)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-border text-sm font-medium text-text-primary hover:bg-surface-sunken transition-colors"
          >
            <Eye size={16} />
            Preview
          </button>
          <button
            onClick={handleSave}
            className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-teal-500 text-white text-sm font-medium hover:bg-teal-600 transition-colors shadow-sm"
          >
            <Save size={16} />
            Save Quotation
          </button>
        </div>
      </div>

      {/* Country & Currency */}
      <CountryTabs
        activeCountry={activeCountry}
        currency={quotation.currency}
        onCountryChange={handleCountryChange}
        onCurrencyChange={handleCurrencyChange}
      />

      {/* Event Details Card */}
      <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-border-subtle">
          <h2 className="text-base font-semibold text-text-primary flex items-center gap-2">
            <FileText size={18} className="text-teal-500" />
            Event & Client Details
          </h2>
        </div>
        <div className="p-6 grid grid-cols-2 gap-5">
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Client Name
            </label>
            <input
              type="text"
              value={quotation.clientName}
              onChange={(e) => updateField("clientName", e.target.value)}
              placeholder="Enter client name"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Company / Organization
            </label>
            <input
              type="text"
              value={quotation.clientCompany}
              onChange={(e) => updateField("clientCompany", e.target.value)}
              placeholder="Enter company name"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Event Name
            </label>
            <input
              type="text"
              value={quotation.eventName}
              onChange={(e) => updateField("eventName", e.target.value)}
              placeholder="Enter event name"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Event Date
            </label>
            <input
              type="text"
              value={quotation.eventDate}
              onChange={(e) => updateField("eventDate", e.target.value)}
              placeholder="e.g., March 15, 2026"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Venue
            </label>
            <input
              type="text"
              value={quotation.eventVenue}
              onChange={(e) => updateField("eventVenue", e.target.value)}
              placeholder="Enter venue"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Est. Attendance
            </label>
            <input
              type="number"
              value={quotation.estimatedAttendance || ""}
              onChange={(e) =>
                updateField(
                  "estimatedAttendance",
                  parseInt(e.target.value) || 0
                )
              }
              placeholder="0"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
        </div>
      </div>

      {/* Line Items */}
      <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-border-subtle flex items-center justify-between">
          <h2 className="text-base font-semibold text-text-primary flex items-center gap-2">
            <Receipt size={18} className="text-teal-500" />
            Line Items
          </h2>
          <button
            onClick={addLineItem}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-teal-50 text-teal-700 text-xs font-medium hover:bg-teal-100 transition-colors"
          >
            <Plus size={14} />
            Add Item
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-surface-sunken">
                <th className="w-8 px-3 py-3"></th>
                <th className="px-3 py-3 text-left text-xs font-semibold text-text-secondary uppercase tracking-wide">
                  Category
                </th>
                <th className="px-3 py-3 text-left text-xs font-semibold text-text-secondary uppercase tracking-wide min-w-[260px]">
                  Description
                </th>
                <th className="px-3 py-3 text-center text-xs font-semibold text-text-secondary uppercase tracking-wide w-24">
                  Qty
                </th>
                <th className="px-3 py-3 text-right text-xs font-semibold text-text-secondary uppercase tracking-wide w-40">
                  Unit Price ({currencyConfig.code})
                </th>
                <th className="px-3 py-3 text-right text-xs font-semibold text-text-secondary uppercase tracking-wide w-40">
                  Total
                </th>
                <th className="w-20 px-3 py-3"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {quotation.lineItems.map((item, index) => (
                <tr
                  key={item.id}
                  className="table-row-hover group"
                >
                  <td className="px-3 py-3">
                    <GripVertical
                      size={14}
                      className="text-text-tertiary opacity-0 group-hover:opacity-100 transition-opacity cursor-grab"
                    />
                  </td>
                  <td className="px-3 py-3">
                    <div className="relative">
                      <select
                        value={item.category}
                        onChange={(e) =>
                          updateLineItem(item.id, "category", e.target.value)
                        }
                        className="w-full appearance-none px-2.5 py-2 rounded-md border border-transparent hover:border-border focus:border-teal-500 focus:ring-1 focus:ring-teal-500/20 text-xs font-medium text-text-primary bg-transparent cursor-pointer"
                      >
                        <option value="">Select category</option>
                        {EVENT_CATEGORIES.map((cat) => (
                          <option key={cat} value={cat}>
                            {cat}
                          </option>
                        ))}
                      </select>
                      <ChevronDown
                        size={12}
                        className="absolute right-2 top-1/2 -translate-y-1/2 text-text-tertiary pointer-events-none"
                      />
                    </div>
                  </td>
                  <td className="px-3 py-3">
                    <input
                      type="text"
                      value={item.description}
                      onChange={(e) =>
                        updateLineItem(
                          item.id,
                          "description",
                          e.target.value
                        )
                      }
                      placeholder="Item description..."
                      className="w-full px-2.5 py-2 rounded-md border border-transparent hover:border-border focus:border-teal-500 focus:ring-1 focus:ring-teal-500/20 text-sm text-text-primary placeholder-text-tertiary bg-transparent"
                    />
                  </td>
                  <td className="px-3 py-3">
                    <input
                      type="number"
                      value={item.quantity}
                      onChange={(e) =>
                        updateLineItem(
                          item.id,
                          "quantity",
                          parseInt(e.target.value) || 0
                        )
                      }
                      min={0}
                      className="w-full px-2.5 py-2 rounded-md border border-transparent hover:border-border focus:border-teal-500 focus:ring-1 focus:ring-teal-500/20 text-sm text-text-primary text-center bg-transparent"
                    />
                  </td>
                  <td className="px-3 py-3">
                    <input
                      type="number"
                      value={item.unitPrice || ""}
                      onChange={(e) =>
                        updateLineItem(
                          item.id,
                          "unitPrice",
                          parseFloat(e.target.value) || 0
                        )
                      }
                      min={0}
                      step={0.01}
                      placeholder="0.00"
                      className="w-full px-2.5 py-2 rounded-md border border-transparent hover:border-border focus:border-teal-500 focus:ring-1 focus:ring-teal-500/20 text-sm text-text-primary text-right bg-transparent font-mono"
                    />
                  </td>
                  <td className="px-3 py-3 text-right">
                    <span className="text-sm font-semibold text-text-primary font-mono">
                      {formatNumber(item.quantity * item.unitPrice)}
                    </span>
                  </td>
                  <td className="px-3 py-3">
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={() => duplicateLineItem(item.id)}
                        className="p-1.5 rounded-md hover:bg-surface-sunken transition-colors"
                        title="Duplicate"
                      >
                        <Copy size={13} className="text-text-tertiary" />
                      </button>
                      <button
                        onClick={() => removeLineItem(item.id)}
                        className="p-1.5 rounded-md hover:bg-red-50 transition-colors"
                        title="Remove"
                      >
                        <Trash2 size={13} className="text-red-400" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {quotation.lineItems.length === 0 && (
          <div className="px-6 py-12 text-center">
            <Receipt size={32} className="mx-auto text-text-tertiary mb-3" />
            <p className="text-sm text-text-secondary">
              No line items yet. Click &ldquo;Add Item&rdquo; to start building your quotation.
            </p>
          </div>
        )}
      </div>

      {/* Financial Summary */}
      <div className="grid grid-cols-3 gap-6">
        {/* Commission & Tax Controls */}
        <div className="col-span-2 bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-border-subtle">
            <h2 className="text-base font-semibold text-text-primary flex items-center gap-2">
              <Calculator size={18} className="text-teal-500" />
              Adjustments
            </h2>
          </div>
          <div className="p-6 grid grid-cols-3 gap-5">
            {/* Agency Commission */}
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
                Agency Commission
              </label>
              <div className="relative">
                <input
                  type="number"
                  value={quotation.agencyCommissionRate}
                  onChange={(e) =>
                    updateField(
                      "agencyCommissionRate",
                      parseFloat(e.target.value) || 0
                    )
                  }
                  min={0}
                  max={100}
                  step={0.5}
                  className="w-full px-3.5 py-2.5 pr-10 rounded-lg border border-border text-sm text-text-primary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 font-mono"
                />
                <Percent
                  size={14}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-text-tertiary"
                />
              </div>
              <p className="text-xs text-text-tertiary mt-1.5">
                = {formatCurrency(totals.commission, quotation.currency)}
              </p>
            </div>

            {/* Tax Rate */}
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
                {COUNTRIES.find((c) => c.id === activeCountry)?.taxLabel || "Tax"} Rate
              </label>
              <div className="relative">
                <input
                  type="number"
                  value={quotation.taxRate}
                  onChange={(e) =>
                    updateField(
                      "taxRate",
                      parseFloat(e.target.value) || 0
                    )
                  }
                  min={0}
                  max={100}
                  step={0.5}
                  className="w-full px-3.5 py-2.5 pr-10 rounded-lg border border-border text-sm text-text-primary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 font-mono"
                />
                <Percent
                  size={14}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-text-tertiary"
                />
              </div>
              <p className="text-xs text-text-tertiary mt-1.5">
                = {formatCurrency(totals.tax, quotation.currency)}
              </p>
            </div>

            {/* Discount */}
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
                Discount (Fixed Amount)
              </label>
              <div className="relative">
                <input
                  type="number"
                  value={quotation.discount || ""}
                  onChange={(e) =>
                    updateField(
                      "discount",
                      parseFloat(e.target.value) || 0
                    )
                  }
                  min={0}
                  step={100}
                  placeholder="0.00"
                  className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 font-mono"
                />
              </div>
              <p className="text-xs text-text-tertiary mt-1.5">
                Applied before tax
              </p>
            </div>
          </div>

          {/* Notes */}
          <div className="px-6 pb-6">
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Notes / Scope of Work
            </label>
            <textarea
              value={quotation.notes}
              onChange={(e) => updateField("notes", e.target.value)}
              rows={3}
              placeholder="Additional notes, terms, or scope details..."
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 resize-none"
            />
          </div>
        </div>

        {/* Totals Card */}
        <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-border-subtle bg-teal-50/50">
            <h2 className="text-base font-semibold text-teal-800">
              Summary
            </h2>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex justify-between text-sm">
              <span className="text-text-secondary">Subtotal</span>
              <span className="font-mono font-medium text-text-primary">
                {formatCurrency(totals.subtotal, quotation.currency)}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-secondary">
                Commission ({quotation.agencyCommissionRate}%)
              </span>
              <span className="font-mono font-medium text-text-primary">
                {formatCurrency(totals.commission, quotation.currency)}
              </span>
            </div>
            {quotation.discount > 0 && (
              <div className="flex justify-between text-sm">
                <span className="text-text-secondary">Discount</span>
                <span className="font-mono font-medium text-red-500">
                  - {formatCurrency(totals.discountAmount, quotation.currency)}
                </span>
              </div>
            )}
            <div className="border-t border-border-subtle pt-3 flex justify-between text-sm">
              <span className="text-text-secondary">Before Tax</span>
              <span className="font-mono font-medium text-text-primary">
                {formatCurrency(totals.afterDiscount, quotation.currency)}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-secondary">
                {COUNTRIES.find((c) => c.id === activeCountry)?.taxLabel} ({quotation.taxRate}%)
              </span>
              <span className="font-mono font-medium text-text-primary">
                {formatCurrency(totals.tax, quotation.currency)}
              </span>
            </div>

            <div className="border-t-2 border-teal-500 pt-4 flex justify-between">
              <span className="text-base font-bold text-text-primary">
                Grand Total
              </span>
              <span className="text-lg font-bold text-teal-700 font-mono">
                {formatCurrency(totals.grandTotal, quotation.currency)}
              </span>
            </div>

            <p className="text-xs text-text-tertiary pt-2">
              Valid until: {quotation.validUntil}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
