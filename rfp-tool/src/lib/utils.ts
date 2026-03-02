import { Currency, CurrencyConfig, LineItem, QuotationData } from "@/types";
import { CURRENCIES } from "./constants";

export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

export function getCurrencyConfig(code: Currency): CurrencyConfig {
  return CURRENCIES.find((c) => c.code === code) || CURRENCIES[0];
}

export function formatCurrency(amount: number, currency: Currency): string {
  const config = getCurrencyConfig(currency);
  const formatted = new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
  return `${config.symbol} ${formatted}`;
}

export function formatNumber(num: number): string {
  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num);
}

export function calculateSubtotal(items: LineItem[]): number {
  return items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0);
}

export function calculateCommission(
  subtotal: number,
  rate: number
): number {
  return subtotal * (rate / 100);
}

export function calculateTax(
  amount: number,
  rate: number
): number {
  return amount * (rate / 100);
}

export function calculateQuotationTotals(quotation: QuotationData) {
  const subtotal = calculateSubtotal(quotation.lineItems);
  const commission = calculateCommission(subtotal, quotation.agencyCommissionRate);
  const subtotalWithCommission = subtotal + commission;
  const discountAmount = quotation.discount;
  const afterDiscount = subtotalWithCommission - discountAmount;
  const tax = calculateTax(afterDiscount, quotation.taxRate);
  const grandTotal = afterDiscount + tax;

  return {
    subtotal,
    commission,
    subtotalWithCommission,
    discountAmount,
    afterDiscount,
    tax,
    grandTotal,
  };
}

export function generateQuotationNumber(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const seq = String(Math.floor(Math.random() * 9999)).padStart(4, "0");
  return `MRD-${year}${month}-${seq}`;
}

export function getDateString(daysFromNow: number = 0): string {
  const date = new Date();
  date.setDate(date.getDate() + daysFromNow);
  return date.toISOString().split("T")[0];
}
