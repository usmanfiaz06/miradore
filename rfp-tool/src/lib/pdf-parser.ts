"use client";

import { RFPEvent, UploadedRFP } from "@/types";

/**
 * Extract text from a PDF file using raw binary parsing.
 * No external dependencies — parses PDF text operators directly.
 */
function extractTextFromPDF(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  const raw = new TextDecoder("latin1").decode(bytes);
  const extracted: string[] = [];

  // Strategy 1: Extract text between BT (begin text) and ET (end text) operators
  const btEtRegex = /BT\s([\s\S]*?)ET/g;
  let match;
  while ((match = btEtRegex.exec(raw)) !== null) {
    const block = match[1];

    // Extract Tj strings: (text) Tj
    const tjRegex = /\(([^)]*)\)\s*(?:Tj|')/g;
    let tjMatch;
    while ((tjMatch = tjRegex.exec(block)) !== null) {
      const decoded = decodePDFString(tjMatch[1]);
      if (decoded.trim()) extracted.push(decoded);
    }

    // Extract TJ array strings: [(text) kern (text)] TJ
    const tjArrayRegex = /\[((?:\([^)]*\)|[^[\]])*?)\]\s*TJ/gi;
    let arrMatch;
    while ((arrMatch = tjArrayRegex.exec(block)) !== null) {
      const parts: string[] = [];
      const partRegex = /\(([^)]*)\)/g;
      let partMatch;
      while ((partMatch = partRegex.exec(arrMatch[1])) !== null) {
        parts.push(decodePDFString(partMatch[1]));
      }
      if (parts.length > 0) extracted.push(parts.join(""));
    }
  }

  // Strategy 2: If BT/ET extraction yields little, fall back to readable ASCII runs
  if (extracted.join("").replace(/\s/g, "").length < 30) {
    const runs: string[] = [];
    let current = "";
    for (let i = 0; i < bytes.length; i++) {
      const ch = bytes[i];
      if (ch >= 32 && ch <= 126) {
        current += String.fromCharCode(ch);
      } else {
        if (current.length >= 4) runs.push(current);
        current = "";
      }
    }
    if (current.length >= 4) runs.push(current);

    const pdfNoise = /^(stream|endstream|endobj|obj|xref|trailer|startxref|null|true|false)$/i;
    for (const run of runs) {
      const clean = run.trim();
      if (
        clean.length >= 4 &&
        !pdfNoise.test(clean) &&
        !clean.startsWith("/") &&
        !clean.startsWith("<<") &&
        !/^\d+\s+\d+\s+(obj|R)$/.test(clean) &&
        !/^[\d.]+$/.test(clean)
      ) {
        extracted.push(clean);
      }
    }
  }

  return extracted.join(" ");
}

function decodePDFString(s: string): string {
  return s
    .replace(/\\n/g, "\n")
    .replace(/\\r/g, "\r")
    .replace(/\\t/g, "\t")
    .replace(/\\\(/g, "(")
    .replace(/\\\)/g, ")")
    .replace(/\\\\/g, "\\");
}

export async function parsePDFFile(file: File): Promise<UploadedRFP> {
  const buffer = await file.arrayBuffer();
  const fullText = extractTextFromPDF(buffer);

  const lines = fullText
    .split(/[\n\r]+|(?:\s{3,})/)
    .map((l) => l.trim())
    .filter((l) => l.length > 1);

  // Extract client name
  let clientName = "";
  for (const line of lines.slice(0, 20)) {
    const lower = line.toLowerCase();
    if (
      lower.includes("rfp") ||
      lower.includes("request for proposal") ||
      lower.includes("client") ||
      lower.includes("prepared for")
    ) {
      clientName = line
        .replace(/^(rfp|request for proposal|client|prepared for)[:\s\-]*/i, "")
        .trim();
      if (clientName && clientName.length > 2) break;
    }
  }
  if (!clientName && lines.length > 0) {
    clientName = lines[0].substring(0, 80);
  }

  // Parse events
  const events: RFPEvent[] = [];
  let eventNumber = 1;

  // Strategy 1: Numbered event patterns
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.length < 3) continue;

    const numberedMatch = line.match(/^(\d+)[.\)]\s+(.{3,})/);
    if (numberedMatch) {
      const name = numberedMatch[2].trim();
      const skipNames = ["event name", "description", "introduction", "background", "objective"];
      if (skipNames.includes(name.toLowerCase())) continue;

      events.push({
        number: parseInt(numberedMatch[1]),
        eventName: name.substring(0, 120),
        arabicName: "",
        date: extractDate(lines.slice(i, i + 3).join(" ")) || "TBD",
        quarter: extractQuarter(lines.slice(i, i + 3).join(" ")),
        category: detectCategory(name),
        estimatedAttendance: extractNumber(lines.slice(i, i + 3).join(" ")),
        eventTier: extractTier(name),
      });
      eventNumber++;
    }
  }

  // Strategy 2: Keyword-based event detection
  if (events.length === 0) {
    const keywords = [
      "conference", "seminar", "workshop", "gala", "ceremony",
      "launch", "summit", "forum", "exhibition", "festival",
      "concert", "meeting", "reception", "dinner", "celebration",
      "awards", "opening", "inauguration", "symposium", "convention",
    ];

    for (const line of lines) {
      const lower = line.toLowerCase();
      if (
        keywords.some((kw) => lower.includes(kw)) &&
        line.length >= 5 &&
        line.length <= 150
      ) {
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

  // Strategy 3: Fallback
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
  const patterns = [
    /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/,
    /(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{2,4})/i,
    /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{2,4})/i,
    /(Q[1-4]\s+\d{4})/i,
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
  if (lower.includes("social") || lower.includes("community")) return "Social";
  return "General";
}

function extractNumber(text: string): number {
  const m = text.match(/(\d{2,6})\s*(?:attendees|guests|people|pax|persons?)?/i);
  return m ? parseInt(m[1]) : 0;
}

function extractTier(text: string): string {
  const lower = text.toLowerCase();
  if (lower.includes("major") || lower.includes("vip") || lower.includes("premium") || lower.includes("gala"))
    return "Major";
  if (lower.includes("medium") || lower.includes("mid") || lower.includes("conference"))
    return "Medium";
  return "Light";
}
