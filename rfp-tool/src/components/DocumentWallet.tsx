"use client";

import { useState, useCallback, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import {
  FolderOpen,
  Upload,
  Trash2,
  FileText,
  Download,
  Search,
  Tag,
  Plus,
} from "lucide-react";
import { WalletDocument } from "@/types";

const STORAGE_KEY = "miradore_document_wallet";

const DOCUMENT_CATEGORIES = [
  "Company Registration",
  "Financial Documents",
  "Tax & Compliance",
  "Insurance",
  "Past Projects / References",
  "Team CVs / Resumes",
  "Certifications",
  "Bank Details",
  "Legal / NDA",
  "Brochures / Profiles",
  "Other",
];

interface DocumentWalletProps {
  highlightDocuments?: string[];
}

export function getWalletDocuments(): WalletDocument[] {
  if (typeof window === "undefined") return [];
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

function saveWalletDocuments(docs: WalletDocument[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(docs));
}

export default function DocumentWallet({ highlightDocuments = [] }: DocumentWalletProps) {
  const [documents, setDocuments] = useState<WalletDocument[]>([]);
  const [filter, setFilter] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    setDocuments(getWalletDocuments());
  }, []);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setIsUploading(true);
    const newDocs: WalletDocument[] = [];

    for (const file of acceptedFiles) {
      const dataUrl = await new Promise<string>((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result as string);
        reader.readAsDataURL(file);
      });

      newDocs.push({
        id: `doc-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
        name: file.name.replace(/\.[^/.]+$/, ""),
        fileName: file.name,
        category: "Other",
        uploadedAt: new Date().toISOString(),
        fileSize: file.size,
        dataUrl,
      });
    }

    setDocuments((prev) => {
      const updated = [...newDocs, ...prev];
      saveWalletDocuments(updated);
      return updated;
    });
    setIsUploading(false);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: true,
  });

  const handleDelete = (id: string) => {
    setDocuments((prev) => {
      const updated = prev.filter((d) => d.id !== id);
      saveWalletDocuments(updated);
      return updated;
    });
  };

  const handleCategoryChange = (id: string, category: string) => {
    setDocuments((prev) => {
      const updated = prev.map((d) => (d.id === id ? { ...d, category } : d));
      saveWalletDocuments(updated);
      return updated;
    });
  };

  const handleRename = (id: string, name: string) => {
    setDocuments((prev) => {
      const updated = prev.map((d) => (d.id === id ? { ...d, name } : d));
      saveWalletDocuments(updated);
      return updated;
    });
  };

  const handleDownload = (doc: WalletDocument) => {
    const link = document.createElement("a");
    link.href = doc.dataUrl;
    link.download = doc.fileName;
    link.click();
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const filtered = documents.filter((d) => {
    const matchesText =
      !filter ||
      d.name.toLowerCase().includes(filter.toLowerCase()) ||
      d.fileName.toLowerCase().includes(filter.toLowerCase());
    const matchesCategory = categoryFilter === "All" || d.category === categoryFilter;
    return matchesText && matchesCategory;
  });

  const categories = ["All", ...DOCUMENT_CATEGORIES];
  const highlightLower = highlightDocuments.map((d) => d.toLowerCase());

  const isHighlighted = (doc: WalletDocument) =>
    highlightLower.some(
      (h) =>
        doc.name.toLowerCase().includes(h) ||
        doc.category.toLowerCase().includes(h) ||
        h.includes(doc.name.toLowerCase())
    );

  return (
    <div className="space-y-6 animate-slide-in">
      {/* Header */}
      <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-border-subtle">
          <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
            <FolderOpen size={20} className="text-teal-500" />
            Document Wallet
          </h2>
          <p className="text-sm text-text-secondary mt-1">
            Upload company documents once. They&apos;ll be linked automatically when an RFP requires supporting documents.
          </p>
        </div>

        {/* Upload Area */}
        <div className="p-6">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
              isDragActive
                ? "border-teal-400 bg-teal-50"
                : "border-border hover:border-teal-300 hover:bg-teal-50/30"
            }`}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 rounded-xl bg-teal-50 flex items-center justify-center">
                {isUploading ? (
                  <Plus size={24} className="text-teal-500 animate-spin" />
                ) : (
                  <Upload size={24} className="text-teal-500" />
                )}
              </div>
              <p className="text-sm font-medium text-text-primary">
                {isDragActive ? "Drop files here" : "Drag & drop company documents"}
              </p>
              <p className="text-xs text-text-secondary">
                or click to browse &middot; PDF, Word, Images, any format
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Documents List */}
      {documents.length > 0 && (
        <div className="bg-white rounded-2xl border border-border shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-border-subtle flex flex-col sm:flex-row gap-3">
            {/* Search */}
            <div className="relative flex-1">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary" />
              <input
                type="text"
                placeholder="Search documents..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="w-full pl-8 pr-3 py-2 text-sm border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-400"
              />
            </div>
            {/* Category Filter */}
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="text-sm border border-border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-teal-500/20 focus:border-teal-400"
            >
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          <div className="divide-y divide-border-subtle max-h-[500px] overflow-y-auto">
            {filtered.map((doc) => (
              <div
                key={doc.id}
                className={`px-6 py-3 flex items-center gap-3 hover:bg-slate-50 transition-colors ${
                  isHighlighted(doc) ? "bg-green-50 border-l-4 border-green-500" : ""
                }`}
              >
                <div className="w-9 h-9 rounded-lg bg-teal-50 flex items-center justify-center flex-shrink-0">
                  <FileText size={18} className="text-teal-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <input
                    type="text"
                    value={doc.name}
                    onChange={(e) => handleRename(doc.id, e.target.value)}
                    className="text-sm font-medium text-text-primary bg-transparent border-none outline-none w-full truncate hover:bg-slate-100 rounded px-1 -ml-1 focus:bg-slate-100"
                  />
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-xs text-text-tertiary">{doc.fileName}</span>
                    <span className="text-xs text-text-tertiary">&middot;</span>
                    <span className="text-xs text-text-tertiary">{formatSize(doc.fileSize)}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  <div className="flex items-center gap-1">
                    <Tag size={12} className="text-text-tertiary" />
                    <select
                      value={doc.category}
                      onChange={(e) => handleCategoryChange(doc.id, e.target.value)}
                      className="text-xs border border-border rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-teal-400"
                    >
                      {DOCUMENT_CATEGORIES.map((c) => (
                        <option key={c} value={c}>
                          {c}
                        </option>
                      ))}
                    </select>
                  </div>
                  <button
                    onClick={() => handleDownload(doc)}
                    className="p-1.5 rounded-lg text-text-tertiary hover:bg-teal-50 hover:text-teal-600 transition-colors"
                    title="Download"
                  >
                    <Download size={14} />
                  </button>
                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="p-1.5 rounded-lg text-text-tertiary hover:bg-red-50 hover:text-red-600 transition-colors"
                    title="Delete"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="px-6 py-3 border-t border-border-subtle bg-slate-50">
            <p className="text-xs text-text-tertiary">
              {documents.length} document{documents.length !== 1 ? "s" : ""} in wallet
              {highlightDocuments.length > 0 && (
                <span className="ml-2 text-green-600 font-medium">
                  &middot; {documents.filter(isHighlighted).length} matched to RFP requirements
                </span>
              )}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
