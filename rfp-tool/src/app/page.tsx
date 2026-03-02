"use client";

import { useState, useCallback } from "react";
import Sidebar from "@/components/Sidebar";
import Dashboard from "@/components/Dashboard";
import RFPUpload from "@/components/RFPUpload";
import QuotationBuilder from "@/components/QuotationBuilder";
import QuotationsList from "@/components/QuotationsList";
import QuotationPreview from "@/components/QuotationPreview";
import { QuotationData, RFPEvent, UploadedRFP } from "@/types";
import { calculateQuotationTotals, generateQuotationNumber } from "@/lib/utils";

export default function Home() {
  const [activeView, setActiveView] = useState("dashboard");
  const [quotations, setQuotations] = useState<QuotationData[]>([]);
  const [uploadedRFP, setUploadedRFP] = useState<UploadedRFP | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<RFPEvent | null>(null);
  const [viewingQuotation, setViewingQuotation] = useState<QuotationData | null>(null);

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
          <Dashboard quotations={quotations} onNavigate={handleNavigate} />
        );
      case "upload":
        return (
          <RFPUpload
            onRFPParsed={handleRFPParsed}
            onSelectEvent={handleSelectEvent}
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
      default:
        return (
          <Dashboard quotations={quotations} onNavigate={handleNavigate} />
        );
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Sidebar
        activeView={activeView}
        onViewChange={setActiveView}
        quotationCount={quotations.length}
      />
      <main className="ml-64 p-8">{renderContent()}</main>
    </div>
  );
}
