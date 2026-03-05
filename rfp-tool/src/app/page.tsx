"use client";

import { useState, useCallback } from "react";
import Sidebar from "@/components/Sidebar";
import Dashboard from "@/components/Dashboard";
import RFPUpload from "@/components/RFPUpload";
import QuotationBuilder from "@/components/QuotationBuilder";
import QuotationsList from "@/components/QuotationsList";
import QuotationPreview from "@/components/QuotationPreview";
import TechnicalProposalBuilder from "@/components/TechnicalProposalBuilder";
import TechnicalProposalPreview from "@/components/TechnicalProposalPreview";
import ProposalsList from "@/components/ProposalsList";
import AISettingsModal from "@/components/AISettingsModal";
import DocumentWallet from "@/components/DocumentWallet";
import { QuotationData, RFPEvent, UploadedRFP } from "@/types";
import { TechnicalProposalData } from "@/lib/ai-service";
import { calculateQuotationTotals, generateQuotationNumber } from "@/lib/utils";

export default function Home() {
  const [activeView, setActiveView] = useState("dashboard");
  const [quotations, setQuotations] = useState<QuotationData[]>([]);
  const [proposals, setProposals] = useState<TechnicalProposalData[]>([]);
  const [uploadedRFP, setUploadedRFP] = useState<UploadedRFP | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<RFPEvent | null>(null);
  const [viewingQuotation, setViewingQuotation] = useState<QuotationData | null>(null);
  const [viewingProposal, setViewingProposal] = useState<TechnicalProposalData | null>(null);
  const [showSettings, setShowSettings] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleRFPParsed = useCallback((rfp: UploadedRFP) => {
    setUploadedRFP(rfp);
  }, []);

  const handleSelectEvent = useCallback((event: RFPEvent) => {
    setSelectedEvent(event);
    setActiveView("builder");
  }, []);

  const handleSaveQuotation = useCallback((quotation: QuotationData) => {
    setQuotations((prev) => {
      const existing = prev.findIndex((q) => q.id === quotation.id);
      if (existing >= 0) {
        const updated = [...prev];
        updated[existing] = quotation;
        return updated;
      }
      return [quotation, ...prev];
    });
    setActiveView("quotations");
    setSelectedEvent(null);
  }, []);

  const handleDeleteQuotation = useCallback((id: string) => {
    setQuotations((prev) => prev.filter((q) => q.id !== id));
  }, []);

  const handleDuplicateQuotation = useCallback((quotation: QuotationData) => {
    const duplicate: QuotationData = {
      ...quotation,
      id: generateQuotationNumber(),
      createdAt: new Date().toISOString().split("T")[0],
    };
    setQuotations((prev) => [duplicate, ...prev]);
  }, []);

  const handleViewQuotation = useCallback((quotation: QuotationData) => {
    setViewingQuotation(quotation);
    setActiveView("preview");
  }, []);

  const handleSaveProposal = useCallback((proposal: TechnicalProposalData) => {
    setProposals((prev) => {
      const existing = prev.findIndex((p) => p.id === proposal.id);
      if (existing >= 0) {
        const updated = [...prev];
        updated[existing] = proposal;
        return updated;
      }
      return [proposal, ...prev];
    });
    setActiveView("proposals");
  }, []);

  const handleDeleteProposal = useCallback((id: string) => {
    setProposals((prev) => prev.filter((p) => p.id !== id));
  }, []);

  const handleViewProposal = useCallback((proposal: TechnicalProposalData) => {
    setViewingProposal(proposal);
    setActiveView("proposal-preview");
  }, []);

  const handleGenerateProposal = useCallback(() => {
    setActiveView("proposal-builder");
  }, []);

  const handleNavigate = useCallback((view: string) => {
    if (view === "new-quotation") {
      setSelectedEvent(null);
      setActiveView("builder");
    } else {
      setActiveView(view);
    }
  }, []);

  const handleBackFromBuilder = useCallback(() => {
    if (uploadedRFP) {
      setActiveView("upload");
    } else {
      setActiveView("dashboard");
    }
    setSelectedEvent(null);
  }, [uploadedRFP]);

  const renderContent = () => {
    switch (activeView) {
      case "dashboard":
        return (
          <Dashboard
            quotations={quotations}
            proposals={proposals}
            onNavigate={handleNavigate}
          />
        );
      case "upload":
        return (
          <RFPUpload
            onRFPParsed={handleRFPParsed}
            onSelectEvent={handleSelectEvent}
            onGenerateProposal={handleGenerateProposal}
            uploadedRFP={uploadedRFP}
          />
        );
      case "builder":
        return (
          <QuotationBuilder
            event={selectedEvent}
            onBack={handleBackFromBuilder}
            onSave={handleSaveQuotation}
          />
        );
      case "quotations":
        return (
          <QuotationsList
            quotations={quotations}
            onView={handleViewQuotation}
            onDelete={handleDeleteQuotation}
            onDuplicate={handleDuplicateQuotation}
          />
        );
      case "preview":
        if (viewingQuotation) {
          const totals = calculateQuotationTotals(viewingQuotation);
          return (
            <QuotationPreview
              quotation={viewingQuotation}
              totals={totals}
              onClose={() => setActiveView("quotations")}
            />
          );
        }
        return null;
      case "proposals":
        return (
          <ProposalsList
            proposals={proposals}
            onView={handleViewProposal}
            onDelete={handleDeleteProposal}
            onNavigateUpload={() => setActiveView("upload")}
          />
        );
      case "proposal-builder":
        if (uploadedRFP) {
          return (
            <TechnicalProposalBuilder
              uploadedRFP={uploadedRFP}
              onBack={() => setActiveView("upload")}
              onSave={handleSaveProposal}
            />
          );
        }
        setActiveView("upload");
        return null;
      case "proposal-preview":
        if (viewingProposal) {
          return (
            <TechnicalProposalPreview
              proposal={viewingProposal}
              onClose={() => setActiveView("proposals")}
            />
          );
        }
        return null;
      case "wallet":
        return (
          <DocumentWallet
            highlightDocuments={uploadedRFP?.requiredDocuments || []}
          />
        );
      default:
        return (
          <Dashboard
            quotations={quotations}
            proposals={proposals}
            onNavigate={handleNavigate}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Sidebar
        activeView={activeView}
        onViewChange={setActiveView}
        quotationCount={quotations.length}
        proposalCount={proposals.length}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen((prev) => !prev)}
        onOpenSettings={() => setShowSettings(true)}
      />
      <main className="pt-16 px-3 pb-4 sm:px-4 lg:pt-0 lg:ml-64 lg:p-8">
        {renderContent()}
      </main>
      <AISettingsModal
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
      />
    </div>
  );
}
