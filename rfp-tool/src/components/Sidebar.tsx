"use client";

import {
  FileText,
  Upload,
  LayoutDashboard,
  HelpCircle,
  ChevronRight,
  Menu,
  X,
  Sparkles,
  BookOpen,
} from "lucide-react";

interface SidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
  quotationCount: number;
  proposalCount: number;
  isOpen: boolean;
  onToggle: () => void;
  onOpenSettings: () => void;
}

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "upload", label: "Upload RFP", icon: Upload },
  { id: "quotations", label: "Quotations", icon: FileText, countKey: "quotations" as const },
  { id: "proposals", label: "Proposals", icon: BookOpen, countKey: "proposals" as const },
];

export default function Sidebar({
  activeView,
  onViewChange,
  quotationCount,
  proposalCount,
  isOpen,
  onToggle,
  onOpenSettings,
}: SidebarProps) {
  const counts = { quotations: quotationCount, proposals: proposalCount };
  const handleNavClick = (id: string) => {
    onViewChange(id);
    // Close sidebar on mobile after navigation
    if (window.innerWidth < 1024) {
      onToggle();
    }
  };

  return (
    <>
      {/* Mobile header bar */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-40 bg-teal-800 text-white flex items-center gap-3 px-4 py-3">
        <button onClick={onToggle} className="p-1">
          <Menu size={22} />
        </button>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`${process.env.NEXT_PUBLIC_BASE_PATH || ""}/images/miradore-logo.png`}
          alt="Miradore"
          width={120}
          height={33}
          className="brightness-0 invert"
        />
      </div>

      {/* Overlay */}
      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/40 z-40"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`w-64 bg-teal-800 text-white flex flex-col h-screen fixed left-0 top-0 z-50 transition-transform duration-200 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } lg:translate-x-0`}
      >
        {/* Logo */}
        <div className="px-6 py-5 border-b border-teal-700/50 flex items-center justify-between">
          <div>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`${process.env.NEXT_PUBLIC_BASE_PATH || ""}/images/miradore-logo.png`}
              alt="Miradore"
              width={160}
              height={44}
              className="brightness-0 invert"
            />
            <p className="text-teal-300 text-xs mt-1.5 font-medium tracking-wide uppercase">
              RFP Quotation Tool
            </p>
          </div>
          <button onClick={onToggle} className="lg:hidden p-1 text-teal-300 hover:text-white">
            <X size={20} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all group ${
                  isActive
                    ? "bg-white/15 text-white shadow-sm"
                    : "text-teal-200 hover:bg-white/8 hover:text-white"
                }`}
              >
                <Icon size={18} className={isActive ? "text-orange-400" : ""} />
                <span className="flex-1 text-left">{item.label}</span>
                {item.countKey && counts[item.countKey] > 0 && (
                  <span className="bg-orange-500 text-white text-xs font-bold px-2 py-0.5 rounded-full min-w-[20px] text-center">
                    {counts[item.countKey]}
                  </span>
                )}
                {isActive && (
                  <ChevronRight size={14} className="text-teal-300" />
                )}
              </button>
            );
          })}
        </nav>

        {/* Bottom nav */}
        <div className="px-3 py-4 border-t border-teal-700/50 space-y-1">
          <button
            onClick={() => { onOpenSettings(); if (window.innerWidth < 1024) onToggle(); }}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-teal-300 hover:bg-white/8 hover:text-white transition-all"
          >
            <Sparkles size={18} />
            <span>AI Settings</span>
          </button>
          <button
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-teal-300 hover:bg-white/8 hover:text-white transition-all"
          >
            <HelpCircle size={18} />
            <span>Help & Support</span>
          </button>
        </div>

        {/* Version */}
        <div className="px-6 py-3 text-teal-500 text-xs">
          v2.0.0 &middot; Miradore Events
        </div>
      </aside>
    </>
  );
}
