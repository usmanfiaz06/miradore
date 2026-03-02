"use client";

import {
  FileText,
  Search,
  Trash2,
  Eye,
  Copy,
  MoreVertical,
  Filter,
  SortAsc,
} from "lucide-react";
import { useState } from "react";
import { QuotationData, Country } from "@/types";
import { COUNTRIES } from "@/lib/constants";
import { formatCurrency, calculateQuotationTotals } from "@/lib/utils";

interface QuotationsListProps {
  quotations: QuotationData[];
  onView: (quotation: QuotationData) => void;
  onDelete: (id: string) => void;
  onDuplicate: (quotation: QuotationData) => void;
}

export default function QuotationsList({
  quotations,
  onView,
  onDelete,
  onDuplicate,
}: QuotationsListProps) {
  const [search, setSearch] = useState("");
  const [filterCountry, setFilterCountry] = useState<Country | "all">("all");

  const filtered = quotations.filter((q) => {
    const matchesSearch =
      !search ||
      q.eventName.toLowerCase().includes(search.toLowerCase()) ||
      q.clientName.toLowerCase().includes(search.toLowerCase()) ||
      q.clientCompany.toLowerCase().includes(search.toLowerCase()) ||
      q.id.toLowerCase().includes(search.toLowerCase());
    const matchesCountry =
      filterCountry === "all" || q.country === filterCountry;
    return matchesSearch && matchesCountry;
  });

  const getTierBadge = (total: number, currency: string) => {
    return (
      <span className="text-sm font-semibold text-text-primary font-mono">
        {formatCurrency(total, currency as any)}
      </span>
    );
  };

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-text-primary">Quotations</h1>
          <p className="text-sm text-text-secondary mt-0.5">
            {quotations.length} quotation{quotations.length !== 1 ? "s" : ""}{" "}
            created
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        <div className="relative flex-1 sm:max-w-md">
          <Search
            size={16}
            className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-tertiary"
          />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search quotations..."
            className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 bg-white"
          />
        </div>

        <div className="flex items-center bg-white rounded-lg border border-border p-0.5 overflow-x-auto">
          <button
            onClick={() => setFilterCountry("all")}
            className={`px-3 py-2 rounded-md text-xs font-medium transition-colors ${
              filterCountry === "all"
                ? "bg-teal-500 text-white"
                : "text-text-secondary hover:text-text-primary"
            }`}
          >
            All
          </button>
          {COUNTRIES.map((c) => (
            <button
              key={c.id}
              onClick={() => setFilterCountry(c.id)}
              className={`px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                filterCountry === c.id
                  ? "bg-teal-500 text-white"
                  : "text-text-secondary hover:text-text-primary"
              }`}
            >
              {c.flag} {c.name}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden overflow-x-auto">
        {filtered.length === 0 ? (
          <div className="px-6 py-16 text-center">
            <FileText
              size={40}
              className="mx-auto text-text-tertiary mb-3"
            />
            <p className="text-sm font-medium text-text-secondary">
              {quotations.length === 0
                ? "No quotations yet"
                : "No quotations match your filters"}
            </p>
            <p className="text-xs text-text-tertiary mt-1">
              {quotations.length === 0
                ? "Upload an RFP or create a quotation to get started."
                : "Try adjusting your search or filters."}
            </p>
          </div>
        ) : (
          <table className="w-full min-w-[700px]">
            <thead>
              <tr className="bg-surface-sunken border-b border-border">
                <th className="px-5 py-3 text-left text-xs font-semibold text-text-secondary uppercase tracking-wide">
                  Reference
                </th>
                <th className="px-5 py-3 text-left text-xs font-semibold text-text-secondary uppercase tracking-wide">
                  Event
                </th>
                <th className="px-5 py-3 text-left text-xs font-semibold text-text-secondary uppercase tracking-wide">
                  Client
                </th>
                <th className="px-5 py-3 text-center text-xs font-semibold text-text-secondary uppercase tracking-wide">
                  Country
                </th>
                <th className="px-5 py-3 text-right text-xs font-semibold text-text-secondary uppercase tracking-wide">
                  Grand Total
                </th>
                <th className="px-5 py-3 text-left text-xs font-semibold text-text-secondary uppercase tracking-wide">
                  Date
                </th>
                <th className="w-24 px-5 py-3"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {filtered.map((q) => {
                const t = calculateQuotationTotals(q);
                const country = COUNTRIES.find((c) => c.id === q.country);
                return (
                  <tr
                    key={q.id}
                    className="table-row-hover group cursor-pointer"
                    onClick={() => onView(q)}
                  >
                    <td className="px-5 py-3.5">
                      <span className="text-xs font-mono font-medium text-teal-600">
                        {q.id}
                      </span>
                    </td>
                    <td className="px-5 py-3.5">
                      <p className="text-sm font-medium text-text-primary">
                        {q.eventName || "Untitled Event"}
                      </p>
                      <p className="text-xs text-text-tertiary mt-0.5">
                        {q.eventDate || "TBD"} &middot;{" "}
                        {q.estimatedAttendance} pax
                      </p>
                    </td>
                    <td className="px-5 py-3.5">
                      <p className="text-sm text-text-primary">
                        {q.clientCompany || q.clientName || "—"}
                      </p>
                    </td>
                    <td className="px-5 py-3.5 text-center">
                      <span className="text-base" title={country?.name}>
                        {country?.flag}
                      </span>
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      {getTierBadge(t.grandTotal, q.currency)}
                    </td>
                    <td className="px-5 py-3.5">
                      <span className="text-xs text-text-secondary">
                        {q.createdAt}
                      </span>
                    </td>
                    <td className="px-5 py-3.5">
                      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onView(q);
                          }}
                          className="p-1.5 rounded-md hover:bg-teal-50 transition-colors"
                          title="View"
                        >
                          <Eye size={14} className="text-teal-600" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDuplicate(q);
                          }}
                          className="p-1.5 rounded-md hover:bg-surface-sunken transition-colors"
                          title="Duplicate"
                        >
                          <Copy size={14} className="text-text-tertiary" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDelete(q.id);
                          }}
                          className="p-1.5 rounded-md hover:bg-red-50 transition-colors"
                          title="Delete"
                        >
                          <Trash2 size={14} className="text-red-400" />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
