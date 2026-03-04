"use client";

import { RFPEvent, UploadedRFP } from "@/types";
import { extractRFPWithAI, getApiKey } from "./ai-service";

/**
 * Extract text from a PDF using pdfjs-dist (Mozilla PDF.js).
 */
async function extractPagesFromPDF(buffer: ArrayBuffer): Promise<string[]> {
  const pdfjs = await import("pdfjs-dist");

  // Use CDN-hosted worker — reliable in static exports / GitHub Pages
  pdfjs.GlobalWorkerOptions.workerSrc =
    `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.mjs`;

  const pdf = await pdfjs.getDocument({ data: new Uint8Array(buffer) }).promise;
  const pages: string[] = [];

  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    // Join items preserving spacing, insert newlines for significant Y-gaps
    let prevY: number | null = null;
    const parts: string[] = [];
    for (const item of content.items) {
      if (!("str" in item)) continue;
      const y = (item as { transform: number[] }).transform[5];
      if (prevY !== null && Math.abs(y - prevY) > 5) {
        parts.push("\n");
      }
      parts.push(item.str);
      prevY = y;
    }
    pages.push(parts.join(" "));
  }

  return pages;
}

export async function parsePDFFile(file: File): Promise<UploadedRFP> {
  const buffer = await file.arrayBuffer();

  let pages: string[];
  try {
    pages = await extractPagesFromPDF(buffer);
  } catch (err) {
    console.error("PDF.js extraction failed:", err);
    throw new Error(
      "Failed to extract text from PDF. Please try converting it to Excel (.xlsx) first, or ensure the PDF contains selectable text (not scanned images)."
    );
  }

  const fullText = pages.join("\n\n");

  // Sanity check
  const printable = fullText.replace(/[^\x20-\x7E\u00A0-\uFFFF]/g, "").trim();
  if (printable.length < 20) {
    throw new Error(
      "Could not extract readable text from this PDF. It may be a scanned/image-based PDF. Please try uploading an Excel (.xlsx) file instead."
    );
  }

  // Try AI parsing first if API key is configured
  const apiKey = getApiKey();
  if (apiKey) {
    try {
      const result = await extractRFPWithAI(fullText, file.name, apiKey);
      result.aiParsed = true;
      return result;
    } catch (err) {
      console.warn("AI parsing failed, falling back to regex:", err);
    }
  }

  // Regex-based parsing fallback
  const lines = fullText
    .split(/[\n\r]+/)
    .map((l) => l.trim())
    .filter((l) => l.length > 1);

  const clientName = extractClientName(lines);

  let events = parseTableEvents(lines);
  if (events.length === 0) events = parseNumberedEvents(lines);
  if (events.length === 0) events = parseKeywordEvents(lines);

  if (events.length === 0) {
    events.push({
      number: 1,
      eventName: clientName || file.name.replace(/\.pdf$/i, ""),
      arabicName: "",
      date: "TBD",
      quarter: "",
      category: "General",
      estimatedAttendance: 0,
      eventTier: "Light",
    });
  }

  return {
    fileName: file.name,
    events,
    clientName,
    uploadedAt: new Date().toISOString(),
    rawText: fullText.substring(0, 12000),
  };
}

/**
 * Extract the client/organization name from the document header.
 */
function extractClientName(lines: string[]): string {
  const clientPatterns = [
    /(?:prepared\s+for|client|company|organization|submitted\s+to)[:\s\-]+(.{3,})/i,
    /(?:rfp|request\s+for\s+proposal)[:\s\-]+(.{3,})/i,
  ];

  for (const line of lines.slice(0, 30)) {
    for (const pat of clientPatterns) {
      const m = line.match(pat);
      if (m && m[1].trim().length > 2) return m[1].trim().substring(0, 100);
    }
  }

  // Use first non-trivial line
  for (const line of lines.slice(0, 5)) {
    if (line.length >= 5 && line.length <= 120) return line;
  }
  return "";
}

/**
 * Strategy 1: Detect tabular data — rows with consistent column counts
 * (common in RFP event calendars).
 */
function parseTableEvents(lines: string[]): RFPEvent[] {
  const events: RFPEvent[] = [];

  // Find header row with event-related columns
  let headerIdx = -1;
  let headerParts: string[] = [];
  for (let i = 0; i < Math.min(lines.length, 40); i++) {
    const lower = lines[i].toLowerCase();
    // Look for header rows containing "event" AND at least one more keyword
    const hasEvent = /event\s*name|event\s*title|event/i.test(lower);
    const hasOther = /date|quarter|category|attendance|tier|type|venue/i.test(lower);
    if (hasEvent && hasOther) {
      headerIdx = i;
      // Split by tabs, multiple spaces, or pipe
      headerParts = lines[i].split(/\t|\s{3,}|\|/).map((s) => s.trim()).filter(Boolean);
      break;
    }
  }

  if (headerIdx < 0) return events;

  // Find column indices
  const colMap = mapColumns(headerParts);

  // Parse data rows after header
  for (let i = headerIdx + 1; i < lines.length; i++) {
    const line = lines[i];
    if (!line || line.length < 3) continue;

    // Stop on summary/total/budget rows
    if (/^\s*(total|budget|summary|notes?:|end|page\s+\d)/i.test(line)) break;

    const cols = line.split(/\t|\s{3,}|\|/).map((s) => s.trim()).filter(Boolean);
    if (cols.length < 2) continue;

    // Try to extract event name from mapped column, fall back to 2nd column
    const nameCol = colMap.name >= 0 && colMap.name < cols.length ? colMap.name : 1;
    const name = (cols[nameCol] || "").trim();
    if (!name || name.length < 3) continue;

    // Skip if it looks like a sub-header
    if (/^(event\s*name|#|no\.?|s\.?n\.?|category)$/i.test(name)) continue;

    const numCol = colMap.number >= 0 && colMap.number < cols.length ? colMap.number : 0;
    const rawNum = cols[numCol];
    const num = /^\d+$/.test(rawNum) ? parseInt(rawNum) : events.length + 1;

    const dateCol = colMap.date >= 0 && colMap.date < cols.length ? colMap.date : -1;
    const qtrCol = colMap.quarter >= 0 && colMap.quarter < cols.length ? colMap.quarter : -1;
    const catCol = colMap.category >= 0 && colMap.category < cols.length ? colMap.category : -1;
    const attCol = colMap.attendance >= 0 && colMap.attendance < cols.length ? colMap.attendance : -1;
    const tierCol = colMap.tier >= 0 && colMap.tier < cols.length ? colMap.tier : -1;

    events.push({
      number: num,
      eventName: name.substring(0, 150),
      arabicName: "",
      date: dateCol >= 0 ? (cols[dateCol] || "TBD") : extractDate(cols.join(" ")) || "TBD",
      quarter: qtrCol >= 0 ? (cols[qtrCol] || "") : extractQuarter(cols.join(" ")),
      category: catCol >= 0 ? (cols[catCol] || "") : detectCategory(name),
      estimatedAttendance: attCol >= 0 ? (parseInt(cols[attCol]) || 0) : extractNumber(cols.join(" ")),
      eventTier: tierCol >= 0 ? (cols[tierCol] || "Light") : extractTier(name),
    });
  }

  return events;
}

function mapColumns(headers: string[]): {
  number: number; name: number; date: number; quarter: number;
  category: number; attendance: number; tier: number;
} {
  const m = { number: -1, name: -1, date: -1, quarter: -1, category: -1, attendance: -1, tier: -1 };
  headers.forEach((h, i) => {
    const l = h.toLowerCase();
    if (/^(#|no\.?|s\.?n\.?|number)$/i.test(l)) m.number = i;
    else if (/event\s*name|event\s*title|event$/i.test(l)) m.name = i;
    else if (/date|when/i.test(l)) m.date = i;
    else if (/quarter|qtr/i.test(l)) m.quarter = i;
    else if (/category|type/i.test(l)) m.category = i;
    else if (/attend|guest|pax|people|capacity/i.test(l)) m.attendance = i;
    else if (/tier|level|scale|size/i.test(l)) m.tier = i;
  });
  return m;
}

/**
 * Strategy 2: Numbered list patterns (e.g., "1. Grand Opening Ceremony")
 */
function parseNumberedEvents(lines: string[]): RFPEvent[] {
  const events: RFPEvent[] = [];
  const seen = new Set<string>();

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.length < 5) continue;

    const numberedMatch = line.match(/^(\d{1,3})[.\)]\s+(.{3,})/);
    if (!numberedMatch) continue;

    const name = numberedMatch[2].trim();
    const lower = name.toLowerCase();

    // Skip generic headers
    const skipNames = [
      "event name", "description", "introduction", "background",
      "objective", "scope", "overview", "table of contents",
      "appendix", "terms", "conditions", "requirements",
    ];
    if (skipNames.some((s) => lower.startsWith(s))) continue;

    const key = lower.substring(0, 50);
    if (seen.has(key)) continue;
    seen.add(key);

    // Gather context from nearby lines
    const context = lines.slice(i, Math.min(i + 4, lines.length)).join(" ");

    events.push({
      number: parseInt(numberedMatch[1]),
      eventName: name.substring(0, 150),
      arabicName: "",
      date: extractDate(context) || "TBD",
      quarter: extractQuarter(context),
      category: detectCategory(name),
      estimatedAttendance: extractNumber(context),
      eventTier: extractTier(name),
    });
  }

  return events;
}

/**
 * Strategy 3: Lines containing event-type keywords
 */
function parseKeywordEvents(lines: string[]): RFPEvent[] {
  const events: RFPEvent[] = [];
  const seen = new Set<string>();

  const eventKeywords = [
    "conference", "seminar", "workshop", "gala", "ceremony",
    "launch", "summit", "forum", "exhibition", "festival",
    "concert", "meeting", "reception", "dinner", "celebration",
    "awards", "opening", "inauguration", "symposium", "convention",
    "retreat", "briefing", "hackathon", "townhall", "town hall",
    "activation", "roadshow", "premiere", "show",
  ];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lower = line.toLowerCase();

    if (line.length < 5 || line.length > 200) continue;
    if (!eventKeywords.some((kw) => lower.includes(kw))) continue;

    // Skip if it looks like a sentence/paragraph rather than an event name
    if (line.split(" ").length > 15) continue;

    const key = lower.substring(0, 50);
    if (seen.has(key)) continue;
    seen.add(key);

    const context = lines.slice(i, Math.min(i + 4, lines.length)).join(" ");

    events.push({
      number: events.length + 1,
      eventName: line.trim().substring(0, 150),
      arabicName: "",
      date: extractDate(context) || "TBD",
      quarter: extractQuarter(context),
      category: detectCategory(line),
      estimatedAttendance: extractNumber(context),
      eventTier: extractTier(line),
    });
  }

  return events;
}

// --- Helper functions ---

function extractDate(text: string): string {
  const patterns = [
    /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/,
    /(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{2,4})/i,
    /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{2,4})/i,
    /(Q[1-4]\s+\d{4})/i,
    /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4})/i,
  ];
  for (const p of patterns) {
    const m = text.match(p);
    if (m) return m[1];
  }
  return "";
}

function extractQuarter(text: string): string {
  const m = text.match(/Q([1-4])/i);
  return m ? `Q${m[1]}` : "";
}

function detectCategory(text: string): string {
  const lower = text.toLowerCase();
  if (lower.includes("corporate") || lower.includes("business")) return "Corporate";
  if (lower.includes("cultural") || lower.includes("heritage")) return "Cultural";
  if (lower.includes("sport") || lower.includes("athletic")) return "Sports";
  if (lower.includes("entertainment") || lower.includes("concert") || lower.includes("show")) return "Entertainment";
  if (lower.includes("government") || lower.includes("national") || lower.includes("public")) return "Government";
  if (lower.includes("social") || lower.includes("community") || lower.includes("charity")) return "Social";
  if (lower.includes("conference") || lower.includes("summit") || lower.includes("forum")) return "Conference";
  if (lower.includes("launch") || lower.includes("opening") || lower.includes("inaugur")) return "Launch";
  if (lower.includes("gala") || lower.includes("dinner") || lower.includes("reception")) return "Gala";
  if (lower.includes("workshop") || lower.includes("training") || lower.includes("seminar")) return "Workshop";
  return "General";
}

function extractNumber(text: string): number {
  const m = text.match(/(\d{2,6})\s*(?:attendees|guests|people|pax|persons?|participants?|invitees?)?/i);
  return m ? parseInt(m[1]) : 0;
}

function extractTier(text: string): string {
  const lower = text.toLowerCase();
  if (
    lower.includes("major") || lower.includes("vip") || lower.includes("premium") ||
    lower.includes("gala") || lower.includes("grand") || lower.includes("flagship")
  ) return "Major";
  if (
    lower.includes("medium") || lower.includes("mid") || lower.includes("conference") ||
    lower.includes("summit") || lower.includes("forum")
  ) return "Medium";
  return "Light";
}
