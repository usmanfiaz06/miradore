"use client";

import { RFPEvent, UploadedRFP } from "@/types";
import { extractRFPWithAI, getApiKey } from "./ai-service";

/**
 * Parse a .docx/.doc file using mammoth for text extraction.
 * Uses AI if API key is configured, otherwise falls back to regex.
 */
export async function parseDocxFile(file: File): Promise<UploadedRFP> {
  const mammoth = await import("mammoth");
  const arrayBuffer = await file.arrayBuffer();

  const result = await mammoth.extractRawText({ arrayBuffer });
  const fullText = result.value;

  if (!fullText || fullText.trim().length < 20) {
    throw new Error(
      "Could not extract readable text from this document. The file may be empty or corrupted."
    );
  }

  // Try AI parsing first if API key is configured
  const apiKey = getApiKey();
  if (apiKey) {
    try {
      const rfp = await extractRFPWithAI(fullText, file.name, apiKey);
      rfp.aiParsed = true;
      return rfp;
    } catch (err) {
      console.warn("AI parsing failed for DOCX, falling back to regex:", err);
    }
  }

  // Regex-based fallback
  const lines = fullText
    .split(/[\n\r]+/)
    .map((l) => l.trim())
    .filter((l) => l.length > 1);

  const clientName = extractClientName(lines);
  const events = parseDocxEvents(lines);

  if (events.length === 0) {
    events.push({
      number: 1,
      eventName: clientName || file.name.replace(/\.(docx?|doc)$/i, ""),
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

function extractClientName(lines: string[]): string {
  const patterns = [
    /(?:prepared\s+for|client|company|organization|submitted\s+to)[:\s\-]+(.{3,})/i,
    /(?:rfp|request\s+for\s+proposal)[:\s\-]+(.{3,})/i,
  ];

  for (const line of lines.slice(0, 30)) {
    for (const pat of patterns) {
      const m = line.match(pat);
      if (m && m[1].trim().length > 2) return m[1].trim().substring(0, 100);
    }
  }

  for (const line of lines.slice(0, 5)) {
    if (line.length >= 5 && line.length <= 120) return line;
  }
  return "";
}

function parseDocxEvents(lines: string[]): RFPEvent[] {
  const events: RFPEvent[] = [];
  const seen = new Set<string>();

  const eventKeywords = [
    "conference", "seminar", "workshop", "gala", "ceremony",
    "launch", "summit", "forum", "exhibition", "festival",
    "concert", "meeting", "reception", "dinner", "celebration",
    "awards", "opening", "inauguration", "symposium", "convention",
    "retreat", "hackathon", "townhall", "town hall",
    "activation", "roadshow", "premiere", "show",
  ];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Strategy 1: Numbered items (e.g. "1. Grand Gala Dinner")
    const numberedMatch = line.match(/^(\d{1,3})[.\)]\s+(.{3,})/);
    if (numberedMatch) {
      const name = numberedMatch[2].trim();
      const lower = name.toLowerCase();
      const skipNames = [
        "event name", "description", "introduction", "background",
        "objective", "scope", "overview", "table of contents",
        "appendix", "terms", "conditions", "requirements",
      ];
      if (skipNames.some((s) => lower.startsWith(s))) continue;

      const key = lower.substring(0, 50);
      if (!seen.has(key)) {
        seen.add(key);
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
      continue;
    }

    // Strategy 2: Lines with event keywords
    const lower = line.toLowerCase();
    if (line.length < 5 || line.length > 200) continue;
    if (!eventKeywords.some((kw) => lower.includes(kw))) continue;
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
  if (lower.includes("entertainment") || lower.includes("concert")) return "Entertainment";
  if (lower.includes("government") || lower.includes("national")) return "Government";
  if (lower.includes("conference") || lower.includes("summit")) return "Conference";
  if (lower.includes("launch") || lower.includes("opening")) return "Launch";
  if (lower.includes("gala") || lower.includes("dinner")) return "Gala";
  if (lower.includes("workshop") || lower.includes("seminar")) return "Workshop";
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
