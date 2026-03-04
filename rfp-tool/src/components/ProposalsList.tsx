"use client";

import {
  BookOpen,
  Eye,
  Trash2,
  Search,
  Sparkles,
  Wand2,
  Calendar,
} from "lucide-react";
import { TechnicalProposalData } from "@/lib/ai-service";
import { useState } from "react";

interface ProposalsListProps {
  proposals: TechnicalProposalData[];
  onView: (proposal: TechnicalProposalData) => void;
  onDelete: (id: string) => void;
  onNavigateUpload: () => void;
}

export default function ProposalsList({
  proposals,
  onView,
  onDelete,
  onNavigateUpload,
}: ProposalsListProps) {
  const [search, setSearch] = useState("");

  const filtered = proposals.filter((p) => {
    const q = search.toLowerCase();
    return (
      p.eventName.toLowerCase().includes(q) ||
      p.clientName.toLowerCase().includes(q) ||
      p.clientCompany.toLowerCase().includes(q) ||
      p.id.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-bold text-text-primary flex items-center gap-2">
            <BookOpen size={22} className="text-teal-500" />
            Technical Proposals
          </h1>
          <p className="text-sm text-text-secondary mt-0.5">
            {proposals.length} proposal{proposals.length !== 1 ? "s" : ""} generated
          </p>
        </div>

        <button
          onClick={onNavigateUpload}
          className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-gradient-to-r from-teal-500 to-teal-600 text-white text-sm font-medium hover:from-teal-600 hover:to-teal-700 transition-all shadow-sm"
        >
          <Wand2 size={16} />
          New Proposal
        </button>
      </div>

      {/* Search */}
      {proposals.length > 0 && (
        <div className="relative">
          <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-tertiary" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search proposals..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 bg-white"
          />
        </div>
      )}

      {/* List */}
      <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
        {filtered.length === 0 ? (
          <div className="px-6 py-16 text-center">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-teal-50 to-orange-50 flex items-center justify-center mx-auto mb-4">
              <BookOpen size={28} className="text-teal-400" />
            </div>
            <h3 className="text-base font-semibold text-text-primary mb-1">
              {search ? "No matching proposals" : "No proposals yet"}
            </h3>
            <p className="text-sm text-text-secondary max-w-sm mx-auto">
              {search
                ? "Try a different search term."
                : "Upload an RFP document and use AI to generate a professional technical proposal."}
            </p>
            {!search && (
              <button
                onClick={onNavigateUpload}
                className="mt-4 inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-teal-50 text-teal-700 text-sm font-medium hover:bg-teal-100 transition-colors"
              >
                <Sparkles size={16} />
                Upload RFP to Get Started
              </button>
            )}
          </div>
        ) : (
          <div className="divide-y divide-border-subtle">
            {filtered.map((proposal) => (
              <div
                key={proposal.id}
                className="px-6 py-4 flex items-center gap-4 hover:bg-teal-50/30 transition-colors group"
              >
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-50 to-orange-50 flex items-center justify-center flex-shrink-0">
                  <BookOpen size={18} className="text-teal-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-text-primary truncate">
                    {proposal.eventName || "Untitled Proposal"}
                  </p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <p className="text-xs text-text-secondary truncate">
                      {proposal.clientName || "No client"}{proposal.clientCompany && ` — ${proposal.clientCompany}`}
                    </p>
                    <span className="text-xs text-text-tertiary flex items-center gap-1">
                      <Calendar size={10} />
                      {proposal.createdAt}
                    </span>
                  </div>
                  <p className="text-[10px] text-text-tertiary mt-0.5">
                    {proposal.sections.length} sections &middot; {proposal.rfpFileName}
                  </p>
                </div>
                <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={() => onView(proposal)}
                    className="p-2 rounded-lg hover:bg-teal-100 transition-colors"
                    title="View"
                  >
                    <Eye size={16} className="text-teal-600" />
                  </button>
                  <button
                    onClick={() => onDelete(proposal.id)}
                    className="p-2 rounded-lg hover:bg-red-50 transition-colors"
                    title="Delete"
                  >
                    <Trash2 size={16} className="text-red-400" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
