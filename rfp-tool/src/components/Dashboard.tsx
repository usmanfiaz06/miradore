"use client";

import {
  FileText,
  Upload,
  Globe,
  ArrowRight,
  Calendar,
  DollarSign,
  Sparkles,
  BookOpen,
  Wand2,
} from "lucide-react";
import { QuotationData } from "@/types";
import { TechnicalProposalData } from "@/lib/ai-service";
import { formatCurrency, calculateQuotationTotals } from "@/lib/utils";

interface DashboardProps {
  quotations: QuotationData[];
  proposals: TechnicalProposalData[];
  onNavigate: (view: string) => void;
}

export default function Dashboard({
  quotations,
  proposals,
  onNavigate,
}: DashboardProps) {
  const totalValue = quotations.reduce((sum, q) => {
    const totals = calculateQuotationTotals(q);
    return sum + totals.grandTotal;
  }, 0);

  const countByCountry = {
    pakistan: quotations.filter((q) => q.country === "pakistan").length,
    ksa: quotations.filter((q) => q.country === "ksa").length,
    dubai: quotations.filter((q) => q.country === "dubai").length,
  };

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Welcome */}
      <div className="bg-gradient-to-br from-teal-600 to-teal-800 rounded-2xl p-5 sm:p-8 text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/3"></div>
        <div className="absolute bottom-0 left-1/2 w-48 h-48 bg-orange-500/10 rounded-full translate-y-1/2"></div>
        <div className="relative">
          <h1 className="text-2xl font-bold">Welcome to Miradore RFP Tool</h1>
          <p className="text-teal-100 mt-2 text-sm max-w-lg">
            Upload RFPs, generate AI-powered technical proposals and professional
            quotations across Pakistan, Saudi Arabia, and Dubai.
          </p>
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 mt-6">
            <button
              onClick={() => onNavigate("upload")}
              className="flex items-center gap-2 px-5 py-2.5 bg-white text-teal-700 rounded-lg text-sm font-semibold hover:bg-teal-50 transition-colors shadow-sm"
            >
              <Upload size={16} />
              Upload RFP
            </button>
            <button
              onClick={() => onNavigate("quotations")}
              className="flex items-center gap-2 px-5 py-2.5 bg-white/15 text-white rounded-lg text-sm font-medium hover:bg-white/25 transition-colors border border-white/20"
            >
              <FileText size={16} />
              View Quotations
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-border p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-lg bg-teal-50 flex items-center justify-center">
              <FileText size={20} className="text-teal-600" />
            </div>
            <span className="text-xs font-medium text-text-tertiary">
              Total
            </span>
          </div>
          <p className="text-2xl font-bold text-text-primary mt-3">
            {quotations.length}
          </p>
          <p className="text-xs text-text-secondary mt-0.5">
            Quotations created
          </p>
        </div>

        <div className="bg-white rounded-xl border border-border p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-lg bg-orange-50 flex items-center justify-center">
              <DollarSign size={20} className="text-orange-600" />
            </div>
            <span className="text-xs font-medium text-text-tertiary">
              Value
            </span>
          </div>
          <p className="text-2xl font-bold text-text-primary mt-3">
            {quotations.length > 0
              ? formatCurrency(totalValue, quotations[0].currency)
              : "—"}
          </p>
          <p className="text-xs text-text-secondary mt-0.5">
            Total quoted value
          </p>
        </div>

        <div className="bg-white rounded-xl border border-border p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-lg bg-emerald-50 flex items-center justify-center">
              <Globe size={20} className="text-emerald-600" />
            </div>
            <span className="text-xs font-medium text-text-tertiary">
              Countries
            </span>
          </div>
          <p className="text-2xl font-bold text-text-primary mt-3">
            {Object.values(countByCountry).filter((c) => c > 0).length}
          </p>
          <p className="text-xs text-text-secondary mt-0.5">
            Active markets
          </p>
        </div>

        <div className="bg-white rounded-xl border border-border p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-lg bg-purple-50 flex items-center justify-center">
              <BookOpen size={20} className="text-purple-600" />
            </div>
            <span className="text-xs font-medium text-text-tertiary">
              Proposals
            </span>
          </div>
          <p className="text-2xl font-bold text-text-primary mt-3">
            {proposals.length}
          </p>
          <p className="text-xs text-text-secondary mt-0.5">
            Technical proposals
          </p>
        </div>
      </div>

      {/* Quick Actions & Recent */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-border-subtle">
            <h2 className="text-base font-semibold text-text-primary flex items-center gap-2">
              <Sparkles size={18} className="text-orange-500" />
              Quick Actions
            </h2>
          </div>
          <div className="p-4 space-y-2">
            <button
              onClick={() => onNavigate("upload")}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-teal-50 transition-colors group text-left"
            >
              <div className="w-9 h-9 rounded-lg bg-teal-50 flex items-center justify-center group-hover:bg-teal-100 transition-colors">
                <Upload size={16} className="text-teal-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-text-primary">
                  Upload New RFP
                </p>
                <p className="text-xs text-text-secondary">
                  Import from Excel
                </p>
              </div>
              <ArrowRight
                size={14}
                className="text-text-tertiary group-hover:text-teal-500 transition-colors"
              />
            </button>
            <button
              onClick={() => onNavigate("new-quotation")}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-orange-50 transition-colors group text-left"
            >
              <div className="w-9 h-9 rounded-lg bg-orange-50 flex items-center justify-center group-hover:bg-orange-100 transition-colors">
                <FileText size={16} className="text-orange-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-text-primary">
                  Create Quotation
                </p>
                <p className="text-xs text-text-secondary">
                  Start from scratch
                </p>
              </div>
              <ArrowRight
                size={14}
                className="text-text-tertiary group-hover:text-orange-500 transition-colors"
              />
            </button>
            <button
              onClick={() => onNavigate("proposals")}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-purple-50 transition-colors group text-left"
            >
              <div className="w-9 h-9 rounded-lg bg-purple-50 flex items-center justify-center group-hover:bg-purple-100 transition-colors">
                <Wand2 size={16} className="text-purple-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-text-primary">
                  Technical Proposals
                </p>
                <p className="text-xs text-text-secondary">
                  AI-powered generation
                </p>
              </div>
              <ArrowRight
                size={14}
                className="text-text-tertiary group-hover:text-purple-500 transition-colors"
              />
            </button>
          </div>
        </div>

        {/* Recent Quotations */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-border-subtle flex items-center justify-between">
            <h2 className="text-base font-semibold text-text-primary flex items-center gap-2">
              <Calendar size={18} className="text-teal-500" />
              Recent Quotations
            </h2>
            {quotations.length > 0 && (
              <button
                onClick={() => onNavigate("quotations")}
                className="text-xs font-medium text-teal-600 hover:text-teal-700 transition-colors"
              >
                View All
              </button>
            )}
          </div>
          <div className="divide-y divide-border-subtle">
            {quotations.length === 0 ? (
              <div className="px-6 py-12 text-center">
                <FileText
                  size={32}
                  className="mx-auto text-text-tertiary mb-3"
                />
                <p className="text-sm text-text-secondary">
                  No quotations yet. Upload an RFP to get started.
                </p>
              </div>
            ) : (
              quotations.slice(0, 5).map((q) => {
                const t = calculateQuotationTotals(q);
                return (
                  <div
                    key={q.id}
                    className="px-6 py-3.5 flex items-center gap-4 hover:bg-surface-sunken transition-colors"
                  >
                    <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center flex-shrink-0">
                      <FileText size={14} className="text-teal-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-text-primary truncate">
                        {q.eventName || "Untitled"}
                      </p>
                      <p className="text-xs text-text-secondary">
                        {q.id} &middot; {q.clientCompany || "No client"}
                      </p>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <p className="text-sm font-semibold text-text-primary font-mono">
                        {formatCurrency(t.grandTotal, q.currency)}
                      </p>
                      <p className="text-xs text-text-tertiary">
                        {q.country.toUpperCase()}
                      </p>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
