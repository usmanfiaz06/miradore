"use client";

import {
  FileText,
  Upload,
  LayoutDashboard,
  Settings,
  HelpCircle,
  ChevronRight,
} from "lucide-react";

interface SidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
  quotationCount: number;
}

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "upload", label: "Upload RFP", icon: Upload },
  { id: "quotations", label: "Quotations", icon: FileText },
];

const bottomItems = [
  { id: "settings", label: "Settings", icon: Settings },
  { id: "help", label: "Help & Support", icon: HelpCircle },
];

export default function Sidebar({
  activeView,
  onViewChange,
  quotationCount,
}: SidebarProps) {
  return (
    <aside className="w-64 bg-teal-800 text-white flex flex-col h-screen fixed left-0 top-0 z-30">
      {/* Logo */}
      <div className="px-6 py-5 border-b border-teal-700/50">
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

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onViewChange(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all group ${
                isActive
                  ? "bg-white/15 text-white shadow-sm"
                  : "text-teal-200 hover:bg-white/8 hover:text-white"
              }`}
            >
              <Icon size={18} className={isActive ? "text-orange-400" : ""} />
              <span className="flex-1 text-left">{item.label}</span>
              {item.id === "quotations" && quotationCount > 0 && (
                <span className="bg-orange-500 text-white text-xs font-bold px-2 py-0.5 rounded-full min-w-[20px] text-center">
                  {quotationCount}
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
        {bottomItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-teal-300 hover:bg-white/8 hover:text-white transition-all"
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      {/* Version */}
      <div className="px-6 py-3 text-teal-500 text-xs">
        v1.0.0 &middot; Miradore Events
      </div>
    </aside>
  );
}
