import { CountryConfig, CurrencyConfig, Country } from "@/types";

export const COUNTRIES: CountryConfig[] = [
  {
    id: "pakistan",
    name: "Pakistan",
    flag: "🇵🇰",
    defaultCurrency: "PKR",
    defaultTaxRate: 17,
    taxLabel: "Sales Tax",
  },
  {
    id: "ksa",
    name: "Saudi Arabia",
    flag: "🇸🇦",
    defaultCurrency: "SAR",
    defaultTaxRate: 15,
    taxLabel: "VAT",
  },
  {
    id: "dubai",
    name: "Dubai / UAE",
    flag: "🇦🇪",
    defaultCurrency: "AED",
    defaultTaxRate: 5,
    taxLabel: "VAT",
  },
];

export const CURRENCIES: CurrencyConfig[] = [
  { code: "PKR", symbol: "₨", name: "Pakistani Rupee" },
  { code: "SAR", symbol: "﷼", name: "Saudi Riyal" },
  { code: "AED", symbol: "د.إ", name: "UAE Dirham" },
  { code: "USD", symbol: "$", name: "US Dollar" },
];

export const EVENT_CATEGORIES = [
  "Venue & Hospitality",
  "Stage & Decor",
  "Audio Visual & Production",
  "Entertainment & Performers",
  "Catering & F&B",
  "Photography & Videography",
  "Printing & Branding",
  "Gifts & Giveaways",
  "Transportation & Logistics",
  "Staffing & Management",
  "Technology & Digital",
  "Miscellaneous",
];

export const TIER_PRICING: Record<string, Record<Country, number>> = {
  Major: {
    pakistan: 1500000,
    ksa: 150000,
    dubai: 120000,
  },
  Medium: {
    pakistan: 800000,
    ksa: 75000,
    dubai: 60000,
  },
  Light: {
    pakistan: 350000,
    ksa: 30000,
    dubai: 25000,
  },
};

export const DEFAULT_LINE_ITEMS_BY_TIER: Record<
  string,
  { category: string; description: string; quantity: number; priceMultiplier: number }[]
> = {
  Major: [
    { category: "Venue & Hospitality", description: "5-Star Hotel Ballroom / Premium Venue Rental", quantity: 1, priceMultiplier: 0.25 },
    { category: "Stage & Decor", description: "Main Stage Setup with Premium Decor & Branding", quantity: 1, priceMultiplier: 0.15 },
    { category: "Audio Visual & Production", description: "Full AV Production (LED Wall, Sound, Lighting)", quantity: 1, priceMultiplier: 0.18 },
    { category: "Catering & F&B", description: "Premium Catering & Beverage Service", quantity: 1, priceMultiplier: 0.15 },
    { category: "Entertainment & Performers", description: "Live Entertainment / Band / Cultural Acts", quantity: 1, priceMultiplier: 0.10 },
    { category: "Photography & Videography", description: "Professional Photo & Video Coverage", quantity: 1, priceMultiplier: 0.05 },
    { category: "Gifts & Giveaways", description: "Premium Gift Boxes / Giveaway Items", quantity: 1, priceMultiplier: 0.05 },
    { category: "Staffing & Management", description: "Event Management, MC & Support Staff", quantity: 1, priceMultiplier: 0.05 },
    { category: "Printing & Branding", description: "Printed Materials, Signage & Branding", quantity: 1, priceMultiplier: 0.02 },
  ],
  Medium: [
    { category: "Venue & Hospitality", description: "Conference Center / Hotel Event Space", quantity: 1, priceMultiplier: 0.25 },
    { category: "Stage & Decor", description: "Standard Stage Setup with Themed Decor", quantity: 1, priceMultiplier: 0.15 },
    { category: "Audio Visual & Production", description: "Conference AV Setup (Projector, Sound, Mics)", quantity: 1, priceMultiplier: 0.18 },
    { category: "Catering & F&B", description: "Standard Catering Service", quantity: 1, priceMultiplier: 0.15 },
    { category: "Photography & Videography", description: "Photo & Video Coverage", quantity: 1, priceMultiplier: 0.08 },
    { category: "Gifts & Giveaways", description: "Standard Gifts / Awards", quantity: 1, priceMultiplier: 0.07 },
    { category: "Staffing & Management", description: "Event Management & Support Staff", quantity: 1, priceMultiplier: 0.07 },
    { category: "Printing & Branding", description: "Printed Materials & Signage", quantity: 1, priceMultiplier: 0.05 },
  ],
  Light: [
    { category: "Venue & Hospitality", description: "Internal Venue / HQ Setup", quantity: 1, priceMultiplier: 0.20 },
    { category: "Stage & Decor", description: "Basic Decor & Themed Displays", quantity: 1, priceMultiplier: 0.18 },
    { category: "Audio Visual & Production", description: "Basic AV Setup (Presentation, Sound)", quantity: 1, priceMultiplier: 0.15 },
    { category: "Catering & F&B", description: "Light Refreshments & Beverages", quantity: 1, priceMultiplier: 0.20 },
    { category: "Photography & Videography", description: "Event Photography", quantity: 1, priceMultiplier: 0.08 },
    { category: "Gifts & Giveaways", description: "Awareness Materials / Small Giveaways", quantity: 1, priceMultiplier: 0.07 },
    { category: "Staffing & Management", description: "Event Coordination", quantity: 1, priceMultiplier: 0.07 },
    { category: "Printing & Branding", description: "Banners & Signage", quantity: 1, priceMultiplier: 0.05 },
  ],
};
