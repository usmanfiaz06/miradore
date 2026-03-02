"use client";

import { Country, Currency } from "@/types";
import { COUNTRIES, CURRENCIES } from "@/lib/constants";
import { ChevronDown } from "lucide-react";

interface CountryTabsProps {
  activeCountry: Country;
  currency: Currency;
  onCountryChange: (country: Country) => void;
  onCurrencyChange: (currency: Currency) => void;
}

export default function CountryTabs({
  activeCountry,
  currency,
  onCountryChange,
  onCurrencyChange,
}: CountryTabsProps) {
  return (
    <div className="flex items-center justify-between gap-4 mb-6">
      {/* Country Tabs */}
      <div className="flex items-center bg-white rounded-xl p-1 shadow-sm border border-border">
        {COUNTRIES.map((country) => {
          const isActive = activeCountry === country.id;
          return (
            <button
              key={country.id}
              onClick={() => onCountryChange(country.id)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? "bg-teal-500 text-white shadow-md"
                  : "text-text-secondary hover:text-text-primary hover:bg-surface-sunken"
              }`}
            >
              <span className="text-base">{country.flag}</span>
              <span>{country.name}</span>
            </button>
          );
        })}
      </div>

      {/* Currency Selector */}
      <div className="relative">
        <select
          value={currency}
          onChange={(e) => onCurrencyChange(e.target.value as Currency)}
          className="appearance-none bg-white border border-border rounded-lg px-4 py-2.5 pr-10 text-sm font-medium text-text-primary shadow-sm hover:border-teal-300 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 cursor-pointer"
        >
          {CURRENCIES.map((c) => (
            <option key={c.code} value={c.code}>
              {c.symbol} {c.code} — {c.name}
            </option>
          ))}
        </select>
        <ChevronDown
          size={16}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-text-tertiary pointer-events-none"
        />
      </div>
    </div>
  );
}
