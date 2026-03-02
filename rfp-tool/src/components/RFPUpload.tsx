"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  Upload,
  FileSpreadsheet,
  CheckCircle2,
  AlertCircle,
  Loader2,
  FileText,
  Calendar,
  Users,
  Sparkles,
} from "lucide-react";
import { UploadedRFP, RFPEvent } from "@/types";
import { parseRFPFile } from "@/lib/xlsx-parser";

interface RFPUploadProps {
  onRFPParsed: (rfp: UploadedRFP) => void;
  onSelectEvent: (event: RFPEvent) => void;
  uploadedRFP: UploadedRFP | null;
}

export default function RFPUpload({
  onRFPParsed,
  onSelectEvent,
  uploadedRFP,
}: RFPUploadProps) {
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const allowedExtensions = [".xlsx", ".xls", ".csv", ".pdf"];

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      const ext = file.name.toLowerCase().slice(file.name.lastIndexOf("."));
      if (!allowedExtensions.includes(ext)) {
        setError(`Unsupported file type. Please upload ${allowedExtensions.join(", ")} files.`);
        return;
      }

      setIsProcessing(true);
      setError(null);

      try {
        const rfp = await parseRFPFile(file);
        onRFPParsed(rfp);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to parse file"
        );
      } finally {
        setIsProcessing(false);
      }
    },
    [onRFPParsed]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    multiple: false,
  });

  const getTierColor = (tier: string) => {
    switch (tier.toLowerCase()) {
      case "major":
        return "bg-orange-100 text-orange-700 border-orange-200";
      case "medium":
        return "bg-teal-100 text-teal-700 border-teal-200";
      case "light":
        return "bg-slate-100 text-slate-600 border-slate-200";
      default:
        return "bg-gray-100 text-gray-600 border-gray-200";
    }
  };

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Upload Area */}
      <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-border-subtle">
          <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
            <Upload size={20} className="text-teal-500" />
            Upload RFP Document
          </h2>
          <p className="text-sm text-text-secondary mt-1">
            Upload an Excel or PDF file containing event details to generate quotations
          </p>
        </div>

        <div className="p-6">
          <div
            {...getRootProps()}
            className={`relative border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
              isDragActive
                ? "border-teal-400 bg-teal-50"
                : error
                ? "border-error/30 bg-red-50/50"
                : "border-border hover:border-teal-300 hover:bg-teal-50/30"
            }`}
          >
            <input {...getInputProps()} />

            {isProcessing ? (
              <div className="flex flex-col items-center gap-3">
                <Loader2
                  size={40}
                  className="text-teal-500 animate-spin"
                />
                <p className="text-sm font-medium text-text-primary">
                  Processing your RFP...
                </p>
                <p className="text-xs text-text-secondary">
                  Extracting event details and specifications
                </p>
              </div>
            ) : uploadedRFP ? (
              <div className="flex flex-col items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
                  <CheckCircle2 size={24} className="text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-text-primary">
                    {uploadedRFP.fileName}
                  </p>
                  <p className="text-xs text-text-secondary mt-1">
                    {uploadedRFP.events.length} events extracted &middot;
                    Drop a new file to replace
                  </p>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-3">
                <div className="w-14 h-14 rounded-2xl bg-teal-50 flex items-center justify-center">
                  <FileSpreadsheet
                    size={28}
                    className="text-teal-500"
                  />
                </div>
                <div>
                  <p className="text-sm font-medium text-text-primary">
                    {isDragActive
                      ? "Drop your file here"
                      : "Drag & drop your RFP file here"}
                  </p>
                  <p className="text-xs text-text-secondary mt-1">
                    or click to browse &middot; Supports .xlsx, .xls, .csv, .pdf
                  </p>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="mt-4 flex items-center gap-2 text-sm text-error bg-red-50 rounded-lg px-4 py-3 border border-red-200">
              <AlertCircle size={16} />
              {error}
            </div>
          )}
        </div>
      </div>

      {/* Events List */}
      {uploadedRFP && uploadedRFP.events.length > 0 && (
        <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden animate-slide-in">
          <div className="px-6 py-4 border-b border-border-subtle flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
                <Calendar size={20} className="text-teal-500" />
                Extracted Events
              </h2>
              <p className="text-sm text-text-secondary mt-0.5">
                {uploadedRFP.clientName || "Imported RFP"} &middot;{" "}
                {uploadedRFP.events.length} events found
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-text-secondary bg-surface-sunken px-3 py-1.5 rounded-full">
                Click an event to create a quotation
              </span>
            </div>
          </div>

          <div className="divide-y divide-border-subtle max-h-[520px] overflow-y-auto">
            {uploadedRFP.events.map((event, index) => (
              <button
                key={index}
                onClick={() => onSelectEvent(event)}
                className="w-full px-6 py-4 flex items-center gap-4 hover:bg-teal-50/50 transition-colors group text-left"
              >
                {/* Number */}
                <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center flex-shrink-0 group-hover:bg-teal-100 transition-colors">
                  <span className="text-xs font-bold text-teal-700">
                    {event.number}
                  </span>
                </div>

                {/* Event Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-medium text-text-primary truncate">
                      {event.eventName}
                    </p>
                    {event.arabicName && (
                      <p className="text-xs text-text-tertiary font-medium" dir="rtl">
                        {event.arabicName}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-3 mt-1">
                    <span className="text-xs text-text-secondary">
                      {event.date}
                    </span>
                    <span className="text-xs text-text-tertiary">
                      {event.category}
                    </span>
                  </div>
                </div>

                {/* Meta */}
                <div className="flex items-center gap-3 flex-shrink-0">
                  <div className="flex items-center gap-1 text-xs text-text-secondary">
                    <Users size={12} />
                    <span>{event.estimatedAttendance}</span>
                  </div>
                  <span
                    className={`text-xs font-medium px-2.5 py-1 rounded-full border ${getTierColor(
                      event.eventTier
                    )}`}
                  >
                    {event.eventTier}
                  </span>
                  <Sparkles
                    size={16}
                    className="text-teal-400 opacity-0 group-hover:opacity-100 transition-opacity"
                  />
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
