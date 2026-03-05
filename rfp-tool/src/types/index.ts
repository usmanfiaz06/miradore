export type Country = "pakistan" | "ksa" | "dubai";

export type Currency = "PKR" | "SAR" | "AED" | "USD";

export interface CountryConfig {
  id: Country;
  name: string;
  flag: string;
  defaultCurrency: Currency;
  defaultTaxRate: number;
  taxLabel: string;
}

export interface CurrencyConfig {
  code: Currency;
  symbol: string;
  name: string;
}

export interface LineItem {
  id: string;
  category: string;
  description: string;
  quantity: number;
  unitPrice: number;
  notes: string;
}

export interface BankDetails {
  bankName: string;
  accountTitle: string;
  accountNumber: string;
  iban: string;
  swiftCode: string;
  branchName: string;
}

export interface PaymentTranche {
  id: string;
  label: string;
  percentage: number;
  description: string;
  dueDate: string;
}

export interface QuotationData {
  id: string;
  clientName: string;
  clientCompany: string;
  eventName: string;
  eventDate: string;
  eventVenue: string;
  eventType: string;
  estimatedAttendance: number;
  country: Country;
  currency: Currency;
  lineItems: LineItem[];
  agencyCommissionRate: number;
  taxRate: number;
  discount: number;
  notes: string;
  createdAt: string;
  validUntil: string;
  bankDetails: BankDetails;
  paymentTerms: string;
  tranches: PaymentTranche[];
}

export interface RFPEvent {
  number: number | string;
  eventName: string;
  arabicName: string;
  date: string;
  quarter: string;
  category: string;
  estimatedAttendance: number;
  eventTier: string;
  venue?: string;
  stageDecor?: string;
  avRequirements?: string;
  keyServices?: string;
}

export interface UploadedRFP {
  fileName: string;
  events: RFPEvent[];
  clientName: string;
  uploadedAt: string;
  rawText?: string;
  rfpSummary?: string;
  requirements?: string[];
  requiredDocuments?: string[];
  aiParsed?: boolean;
}

export interface WalletDocument {
  id: string;
  name: string;
  fileName: string;
  category: string;
  uploadedAt: string;
  fileSize: number;
  dataUrl: string;
}
