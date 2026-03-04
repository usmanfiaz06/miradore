"use client";

import { useState, useEffect } from "react";
import {
  X,
  Key,
  Sparkles,
  CheckCircle2,
  ExternalLink,
} from "lucide-react";
import { getApiKey, setApiKey, hasApiKey } from "@/lib/ai-service";

interface AISettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AISettingsModal({ isOpen, onClose }: AISettingsModalProps) {
  const [key, setKey] = useState("");
  const [saved, setSaved] = useState(false);
  const [hasKey, setHasKey] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const existing = getApiKey();
      setKey(existing);
      setHasKey(hasApiKey());
      setSaved(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSave = () => {
    setApiKey(key);
    setSaved(true);
    setHasKey(key.trim().length > 0);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleRemove = () => {
    setKey("");
    setApiKey("");
    setHasKey(false);
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg animate-slide-in overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-border-subtle bg-gradient-to-r from-teal-50 to-orange-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center">
                <Sparkles size={20} className="text-white" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-text-primary">AI Settings</h2>
                <p className="text-xs text-text-secondary">Configure AI-powered features</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-white/60 transition-colors"
            >
              <X size={18} className="text-text-secondary" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Status */}
          <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border ${
            hasKey
              ? "bg-green-50 border-green-200"
              : "bg-orange-50 border-orange-200"
          }`}>
            <div className={`w-2.5 h-2.5 rounded-full ${hasKey ? "bg-green-500" : "bg-orange-400"} animate-pulse`} />
            <p className="text-sm font-medium">
              {hasKey ? (
                <span className="text-green-700">AI features are enabled</span>
              ) : (
                <span className="text-orange-700">Add an API key to enable AI features</span>
              )}
            </p>
          </div>

          {/* API Key Input */}
          <div>
            <label className="block text-xs font-semibold text-text-secondary mb-2 uppercase tracking-wide">
              Google Gemini API Key
            </label>
            <div className="relative">
              <Key size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-tertiary" />
              <input
                type="password"
                value={key}
                onChange={(e) => { setKey(e.target.value); setSaved(false); }}
                placeholder="AIzaSy..."
                className="w-full pl-10 pr-4 py-3 rounded-xl border border-border text-sm text-text-primary placeholder-text-tertiary hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
              />
            </div>
            <p className="mt-2 text-xs text-text-tertiary">
              Get a free API key from{" "}
              <a
                href="https://aistudio.google.com/apikey"
                target="_blank"
                rel="noopener noreferrer"
                className="text-teal-600 hover:text-teal-700 font-medium inline-flex items-center gap-1"
              >
                Google AI Studio <ExternalLink size={10} />
              </a>
            </p>
          </div>

          {/* What AI enables */}
          <div className="bg-surface-sunken rounded-xl p-4 space-y-3">
            <p className="text-xs font-semibold text-text-secondary uppercase tracking-wide">
              AI-Powered Features
            </p>
            <div className="space-y-2.5">
              {[
                "Smart PDF/RFP parsing — accurately extracts events, dates, and details",
                "Technical Proposal generation — auto-creates professional proposals",
                "Intelligent event categorization and tier detection",
              ].map((feature, i) => (
                <div key={i} className="flex items-start gap-2.5">
                  <Sparkles size={14} className="text-teal-500 mt-0.5 flex-shrink-0" />
                  <p className="text-xs text-text-secondary">{feature}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-border-subtle bg-surface-sunken flex items-center justify-between gap-3">
          {hasKey && (
            <button
              onClick={handleRemove}
              className="text-xs font-medium text-red-500 hover:text-red-600 transition-colors"
            >
              Remove Key
            </button>
          )}
          <div className="flex items-center gap-3 ml-auto">
            <button
              onClick={onClose}
              className="px-4 py-2.5 rounded-lg border border-border text-sm font-medium text-text-primary hover:bg-white transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saved}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                saved
                  ? "bg-green-500 text-white"
                  : "bg-teal-500 text-white hover:bg-teal-600 shadow-sm"
              }`}
            >
              {saved ? (
                <>
                  <CheckCircle2 size={16} />
                  Saved
                </>
              ) : (
                "Save Key"
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
