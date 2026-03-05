"use client";

import { useState, useCallback } from "react";
import {
  ArrowLeft,
  Sparkles,
  Loader2,
  Eye,
  Save,
  GripVertical,
  Trash2,
  Plus,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  FileText,
  Wand2,
} from "lucide-react";
import { UploadedRFP } from "@/types";
import {
  generateTechnicalProposal,
  getApiKey,
  hasApiKey,
  TechnicalProposalData,
  ProposalSection,
} from "@/lib/ai-service";
import { generateId } from "@/lib/utils";
import TechnicalProposalPreview from "./TechnicalProposalPreview";

interface TechnicalProposalBuilderProps {
  uploadedRFP: UploadedRFP;
  onBack: () => void;
  onSave: (proposal: TechnicalProposalData) => void;
  existingProposal?: TechnicalProposalData | null;
}

export default function TechnicalProposalBuilder({
  uploadedRFP,
  onBack,
  onSave,
  existingProposal,
}: TechnicalProposalBuilderProps) {
  const [proposal, setProposal] = useState<TechnicalProposalData>(
    existingProposal || {
      id: `TP-${generateId()}`,
      rfpFileName: uploadedRFP.fileName,
      rfpReference: "",
      clientName: uploadedRFP.clientName || "",
      clientCompany: "",
      eventName: uploadedRFP.events[0]?.eventName || "",
      contractTitle: "",
      contractPeriod: "",
      submittedTo: uploadedRFP.clientName || "",
      createdAt: new Date().toISOString().split("T")[0],
      sections: [],
    }
  );
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPreview, setShowPreview] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());
  const [generationProgress, setGenerationProgress] = useState("");

  const toggleSection = (id: string) => {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const handleGenerate = useCallback(async () => {
    if (!hasApiKey()) {
      setError("Please configure your Gemini API key in Settings first.");
      return;
    }

    setIsGenerating(true);
    setError(null);
    setGenerationProgress("Analyzing RFP document...");

    try {
      setTimeout(() => setGenerationProgress("Generating proposal sections..."), 2000);
      setTimeout(() => setGenerationProgress("Writing technical details..."), 5000);
      setTimeout(() => setGenerationProgress("Finalizing proposal..."), 8000);

      const sections = await generateTechnicalProposal(
        {
          clientName: proposal.clientName || uploadedRFP.clientName,
          eventName: proposal.eventName,
          events: uploadedRFP.events,
          rfpSummary: uploadedRFP.rfpSummary,
          requirements: uploadedRFP.requirements,
          rawText: uploadedRFP.rawText,
        },
        getApiKey()
      );

      setProposal((prev) => ({ ...prev, sections }));
      // Expand all sections after generation
      setExpandedSections(new Set(sections.map((s) => s.id)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate proposal");
    } finally {
      setIsGenerating(false);
      setGenerationProgress("");
    }
  }, [proposal.clientName, proposal.eventName, uploadedRFP]);

  const updateSection = (id: string, field: keyof ProposalSection, value: string) => {
    setProposal((prev) => ({
      ...prev,
      sections: prev.sections.map((s) =>
        s.id === id ? { ...s, [field]: value } : s
      ),
    }));
  };

  const removeSection = (id: string) => {
    setProposal((prev) => ({
      ...prev,
      sections: prev.sections.filter((s) => s.id !== id),
    }));
  };

  const addSection = () => {
    const newSection: ProposalSection = {
      id: `section-${Date.now()}`,
      title: "New Section",
      content: "",
      order: proposal.sections.length,
    };
    setProposal((prev) => ({
      ...prev,
      sections: [...prev.sections, newSection],
    }));
    setExpandedSections((prev) => new Set([...prev, newSection.id]));
  };

  const handleSave = () => {
    onSave(proposal);
  };

  if (showPreview) {
    return (
      <TechnicalProposalPreview
        proposal={proposal}
        onClose={() => setShowPreview(false)}
      />
    );
  }

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          <button
            onClick={onBack}
            className="p-2 rounded-lg hover:bg-surface-sunken transition-colors flex-shrink-0"
          >
            <ArrowLeft size={20} className="text-text-secondary" />
          </button>
          <div className="min-w-0">
            <h1 className="text-lg sm:text-xl font-bold text-text-primary truncate flex items-center gap-2">
              <Sparkles size={20} className="text-orange-500 flex-shrink-0" />
              Technical Proposal
            </h1>
            <p className="text-xs sm:text-sm text-text-secondary mt-0.5">
              {uploadedRFP.fileName} &middot; AI-powered proposal builder
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 flex-shrink-0">
          {proposal.sections.length > 0 && (
            <>
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
                Save
              </button>
            </>
          )}
        </div>
      </div>

      {/* Client Details */}
      <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-border-subtle">
          <h2 className="text-base font-semibold text-text-primary flex items-center gap-2">
            <FileText size={18} className="text-teal-500" />
            Proposal Details
          </h2>
        </div>
        <div className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              RFP Reference
            </label>
            <input
              type="text"
              value={proposal.rfpReference}
              onChange={(e) => setProposal((p) => ({ ...p, rfpReference: e.target.value }))}
              placeholder="e.g. RFP-DEPO-IDEAS-2026-001"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Submitted To
            </label>
            <input
              type="text"
              value={proposal.submittedTo}
              onChange={(e) => setProposal((p) => ({ ...p, submittedTo: e.target.value }))}
              placeholder="e.g. Defence Export Promotion Organisation (DEPO)"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Client Name
            </label>
            <input
              type="text"
              value={proposal.clientName}
              onChange={(e) => setProposal((p) => ({ ...p, clientName: e.target.value }))}
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
              value={proposal.clientCompany}
              onChange={(e) => setProposal((p) => ({ ...p, clientCompany: e.target.value }))}
              placeholder="Enter company name"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Contract Title
            </label>
            <input
              type="text"
              value={proposal.contractTitle}
              onChange={(e) => setProposal((p) => ({ ...p, contractTitle: e.target.value }))}
              placeholder="e.g. Integrated Communications, Media & Production"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Contract Period
            </label>
            <input
              type="text"
              value={proposal.contractPeriod}
              onChange={(e) => setProposal((p) => ({ ...p, contractPeriod: e.target.value }))}
              placeholder="e.g. 12 Months: March 2026 - February 2027"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
          <div className="sm:col-span-2">
            <label className="block text-xs font-medium text-text-secondary mb-1.5 uppercase tracking-wide">
              Event / Project Name
            </label>
            <input
              type="text"
              value={proposal.eventName}
              onChange={(e) => setProposal((p) => ({ ...p, eventName: e.target.value }))}
              placeholder="Enter event or project name"
              className="w-full px-3.5 py-2.5 rounded-lg border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
            />
          </div>
        </div>
      </div>

      {/* RFP Summary (if AI-parsed) */}
      {uploadedRFP.rfpSummary && (
        <div className="bg-gradient-to-r from-teal-50 to-orange-50 rounded-2xl border border-teal-100 p-5">
          <div className="flex items-start gap-3">
            <Sparkles size={18} className="text-teal-500 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-xs font-semibold text-teal-700 uppercase tracking-wide mb-1.5">
                AI Summary of RFP
              </p>
              <p className="text-sm text-text-secondary leading-relaxed">
                {uploadedRFP.rfpSummary}
              </p>
              {uploadedRFP.requirements && uploadedRFP.requirements.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {uploadedRFP.requirements.slice(0, 5).map((req, i) => (
                    <span
                      key={i}
                      className="text-[10px] font-medium px-2.5 py-1 rounded-full bg-white border border-teal-200 text-teal-700"
                    >
                      {req.length > 60 ? req.substring(0, 60) + "..." : req}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Generate Button */}
      {proposal.sections.length === 0 && !isGenerating && (
        <div className="bg-white rounded-2xl border-2 border-dashed border-teal-200 p-8 sm:p-12 text-center">
          <div className="max-w-md mx-auto">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-teal-500 to-orange-500 flex items-center justify-center mx-auto mb-4">
              <Wand2 size={28} className="text-white" />
            </div>
            <h3 className="text-lg font-bold text-text-primary mb-2">
              Generate Technical Proposal
            </h3>
            <p className="text-sm text-text-secondary mb-6">
              AI will analyze the uploaded RFP and generate a comprehensive, professional technical proposal
              with all key sections — executive summary, methodology, team structure, timeline, and more.
            </p>
            <button
              onClick={handleGenerate}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-teal-500 to-teal-600 text-white font-semibold hover:from-teal-600 hover:to-teal-700 transition-all shadow-lg shadow-teal-500/25"
            >
              <Sparkles size={18} />
              Generate with AI
            </button>
            {!hasApiKey() && (
              <p className="mt-3 text-xs text-orange-600 font-medium">
                Configure your Gemini API key in Settings first
              </p>
            )}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isGenerating && (
        <div className="bg-white rounded-2xl border border-border shadow-sm p-12 text-center">
          <div className="relative w-16 h-16 mx-auto mb-5">
            <div className="absolute inset-0 rounded-full border-4 border-teal-100" />
            <div className="absolute inset-0 rounded-full border-4 border-teal-500 border-t-transparent animate-spin" />
            <Sparkles size={20} className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-teal-500" />
          </div>
          <h3 className="text-base font-bold text-text-primary mb-2">
            Generating Your Proposal
          </h3>
          <p className="text-sm text-text-secondary animate-pulse">
            {generationProgress}
          </p>
          <div className="mt-4 w-48 h-1.5 bg-teal-100 rounded-full mx-auto overflow-hidden">
            <div className="h-full bg-gradient-to-r from-teal-500 to-orange-500 rounded-full animate-[shimmer_2s_ease-in-out_infinite]"
              style={{ width: "70%", animation: "shimmer 2s ease-in-out infinite" }} />
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex items-center gap-3 text-sm bg-red-50 rounded-xl px-5 py-4 border border-red-200">
          <AlertCircle size={18} className="text-red-500 flex-shrink-0" />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Sections Editor */}
      {proposal.sections.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-semibold text-text-primary">
              Proposal Sections ({proposal.sections.length})
            </h2>
            <div className="flex items-center gap-2">
              <button
                onClick={addSection}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-teal-50 text-teal-700 text-xs font-medium hover:bg-teal-100 transition-colors"
              >
                <Plus size={14} />
                Add Section
              </button>
              <button
                onClick={handleGenerate}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-orange-50 text-orange-700 text-xs font-medium hover:bg-orange-100 transition-colors"
              >
                <Sparkles size={14} />
                Regenerate
              </button>
            </div>
          </div>

          {proposal.sections.map((section, index) => (
            <div
              key={section.id}
              className="bg-white rounded-xl border border-border shadow-sm overflow-hidden group"
            >
              {/* Section Header */}
              <button
                onClick={() => toggleSection(section.id)}
                className="w-full px-5 py-3.5 flex items-center gap-3 hover:bg-surface-sunken/50 transition-colors text-left"
              >
                <GripVertical size={14} className="text-text-tertiary flex-shrink-0" />
                <span className="w-7 h-7 rounded-lg bg-teal-50 flex items-center justify-center flex-shrink-0">
                  <span className="text-xs font-bold text-teal-700">{index + 1}</span>
                </span>
                <span className="flex-1 text-sm font-semibold text-text-primary truncate">
                  {section.title}
                </span>
                <div className="flex items-center gap-2">
                  <button
                    onClick={(e) => { e.stopPropagation(); removeSection(section.id); }}
                    className="p-1.5 rounded-md hover:bg-red-50 transition-colors opacity-0 group-hover:opacity-100"
                  >
                    <Trash2 size={13} className="text-red-400" />
                  </button>
                  {expandedSections.has(section.id) ? (
                    <ChevronUp size={16} className="text-text-tertiary" />
                  ) : (
                    <ChevronDown size={16} className="text-text-tertiary" />
                  )}
                </div>
              </button>

              {/* Section Content */}
              {expandedSections.has(section.id) && (
                <div className="px-5 pb-5 space-y-3 border-t border-border-subtle">
                  <div className="pt-3">
                    <label className="block text-[10px] font-medium text-text-tertiary uppercase tracking-wide mb-1">
                      Section Title
                    </label>
                    <input
                      type="text"
                      value={section.title}
                      onChange={(e) => updateSection(section.id, "title", e.target.value)}
                      className="w-full px-3 py-2 rounded-lg border border-border text-sm font-medium text-text-primary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-medium text-text-tertiary uppercase tracking-wide mb-1">
                      Content
                    </label>
                    <textarea
                      value={section.content}
                      onChange={(e) => updateSection(section.id, "content", e.target.value)}
                      rows={8}
                      className="w-full px-3 py-2.5 rounded-lg border border-border text-sm text-text-primary leading-relaxed hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 resize-y"
                    />
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
