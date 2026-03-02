"use client";

import * as pdfjs from "pdfjs-dist";
import { RFPEvent, UploadedRFP } from "@/types";

if (typeof window !== "undefined") {
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";
  pdfjs.GlobalWorkerOptions.workerSrc = `${basePath}/pdf.worker.min.mjs`;
}

export async function parsePDFFile(file: File): Promise<UploadedRFP> {
  const arrayBuffer = await file.arrayBuffer();
  const pdf = await pdfjs.getDocument({ data: new Uint8Array(arrayBuffer) }).promise;

  // Extract text from all pages
  const pages: string[] = [];
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    const text = content.items
      .map((item) => ("str" in item ? item.str : ""))
      .join(" ");
    pages.push(text);
  }

  const fullText = pages.join("\n");
  const lines = fullText
    .split(/\n/)
    .map((l) => l.trim())
    .filter(Boolean);

  // Try to extract client name from the first few lines
  let clientName = "";
  for (const line of lines.slice(0, 10)) {
    if (
      line.toLowerCase().includes("rfp") ||
      line.toLowerCase().includes("request for proposal") ||
      line.toLowerCase().includes("client")
    ) {
      clientName = line.replace(/^(rfp|request for proposal|client)[:\s-]*/i, "").trim();
      if (clientName) break;
    }
  }
  if (!clientName && lines.length > 0) {
    clientName = lines[0].substring(0, 80);
  }

  // Parse events from structured table-like content
  const events: RFPEvent[] = [];
  let eventNumber = 1;

  // Strategy 1: Look for numbered events or rows with event-like patterns
  const eventPatterns = [
    // "1. Event Name - Date - Category"
    /^(\d+)[.\)\-]\s*(.+)/,
    // "Event Name | Date | Category"  (table rows)
    /^(.+?)\s*[|\t]\s*(.+)/,
  ];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Skip header-like lines
    if (
      line.toLowerCase().includes("event name") &&
      (line.toLowerCase().includes("date") || line.toLowerCase().includes("category"))
    ) {
      continue;
    }

    for (const pattern of eventPatterns) {
      const match = line.match(pattern);
      if (match) {
        const parts = line.split(/[|\t]+/).map((p) => p.trim());

        if (parts.length >= 2) {
          const rawNumber = parts[0].match(/^(\d+)/);
          const name = rawNumber
            ? parts[0].replace(/^\d+[.\)\-\s]*/, "").trim()
            : parts[0];

          if (!name || name.length < 2) continue;

          // Skip if it looks like a header/title row
          if (
            name.toLowerCase() === "event" ||
            name.toLowerCase() === "event name" ||
            name.toLowerCase() === "description"
          )
            continue;

          const event: RFPEvent = {
            number: rawNumber ? parseInt(rawNumber[1]) : eventNumber,
            eventName: name,
            arabicName: "",
            date: extractDate(parts.slice(1).join(" ")) || "TBD",
            quarter: extractQuarter(parts.slice(1).join(" ")),
            category: extractCategory(parts.slice(1).join(" ")),
            estimatedAttendance: extractNumber(parts.slice(1).join(" ")),
            eventTier: extractTier(parts.slice(1).join(" ")),
          };

          events.push(event);
          eventNumber++;
          break;
        }
      }
    }
  }

  // Strategy 2: If no events found via patterns, look for keyword-based extraction
  if (events.length === 0) {
    const eventKeywords = [
      "conference",
      "seminar",
      "workshop",
      "gala",
      "ceremony",
      "launch",
      "summit",
      "forum",
      "exhibition",
      "festival",
      "concert",
      "meeting",
      "reception",
      "dinner",
      "celebration",
      "awards",
    ];

    for (const line of lines) {
      const lower = line.toLowerCase();
      if (eventKeywords.some((kw) => lower.includes(kw))) {
        // Avoid duplicates
        if (events.some((e) => e.eventName === line.trim())) continue;

        events.push({
          number: eventNumber,
          eventName: line.trim().substring(0, 120),
          arabicName: "",
          date: "TBD",
          quarter: "",
          category: detectCategory(line),
          estimatedAttendance: 0,
          eventTier: "Light",
        });
        eventNumber++;
      }
    }
  }

  // If still no events, create a single event from the document
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
  };
}

function extractDate(text: string): string {
  // Match common date formats
  const datePatterns = [
    /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/,
    /(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{2,4})/i,
    /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{2,4})/i,
    /(Q[1-4]\s+\d{4})/i,
  ];

  for (const pattern of datePatterns) {
    const match = text.match(pattern);
    if (match) return match[1];
  }
  return "";
}

function extractQuarter(text: string): string {
  const match = text.match(/Q([1-4])/i);
  return match ? `Q${match[1]}` : "";
}

function extractCategory(text: string): string {
  return detectCategory(text) || "General";
}

function detectCategory(text: string): string {
  const lower = text.toLowerCase();
  if (lower.includes("corporate") || lower.includes("business"))
    return "Corporate";
  if (lower.includes("cultural") || lower.includes("heritage"))
    return "Cultural";
  if (lower.includes("sport") || lower.includes("athletic")) return "Sports";
  if (lower.includes("entertainment") || lower.includes("concert"))
    return "Entertainment";
  if (lower.includes("government") || lower.includes("national"))
    return "Government";
  if (lower.includes("social") || lower.includes("community"))
    return "Social";
  return "General";
}

function extractNumber(text: string): number {
  const match = text.match(/(\d{2,6})\s*(?:attendees|guests|people|pax)?/i);
  return match ? parseInt(match[1]) : 0;
}

function extractTier(text: string): string {
  const lower = text.toLowerCase();
  if (lower.includes("major") || lower.includes("vip") || lower.includes("premium"))
    return "Major";
  if (lower.includes("medium") || lower.includes("mid")) return "Medium";
  return "Light";
}
