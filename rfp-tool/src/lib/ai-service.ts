"use client";

import { RFPEvent, UploadedRFP } from "@/types";

const GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent";
const REQUEST_TIMEOUT_MS = 60000; // 60 second timeout for large proposals

export function getApiKey(): string {
  if (typeof window === "undefined") return "";
  return localStorage.getItem("miradore_gemini_api_key") || "";
}

export function setApiKey(key: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem("miradore_gemini_api_key", key.trim());
}

export function hasApiKey(): boolean {
  return getApiKey().length > 0;
}

async function callGemini(prompt: string, apiKey: string): Promise<string> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const res = await fetch(`${GEMINI_API_URL}?key=${apiKey}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0.3,
          maxOutputTokens: 8192,
        },
      }),
    });

    if (!res.ok) {
      let errorDetail = "";
      try {
        const errBody = await res.json();
        errorDetail = errBody?.error?.message || JSON.stringify(errBody?.error || errBody).substring(0, 200);
      } catch {
        // ignore parse errors
      }

      if (res.status === 401 || res.status === 403) {
        throw new Error("Invalid or restricted API key. Check your Gemini API key in Settings.");
      }
      if (res.status === 429) {
        throw new Error("AI rate limit exceeded. Please wait a moment and try again.");
      }
      if (res.status === 404) {
        throw new Error("AI model not available. The Gemini model may not be accessible in your region.");
      }
      if (res.status === 400) {
        throw new Error(`AI request error: ${errorDetail || "Bad request. The document may be too large."}`);
      }
      throw new Error(`AI request failed (${res.status}): ${errorDetail || "Unknown error"}`);
    }

    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!text) throw new Error("Empty response from AI");
    return text;
  } catch (err: unknown) {
    if (err instanceof DOMException && err.name === "AbortError") {
      throw new Error("AI request timed out after 60s. Please try again.");
    }
    throw err;
  } finally {
    clearTimeout(timeoutId);
  }
}

function extractJSON(text: string): string {
  // Try to extract JSON from markdown code blocks or raw JSON
  const codeBlockMatch = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (codeBlockMatch) return codeBlockMatch[1].trim();
  // Try to find raw JSON object/array
  const jsonMatch = text.match(/(\{[\s\S]*\}|\[[\s\S]*\])/);
  if (jsonMatch) return jsonMatch[1].trim();
  return text.trim();
}

/**
 * Use AI to extract structured RFP data from raw text.
 */
export async function extractRFPWithAI(
  rawText: string,
  fileName: string,
  apiKey: string
): Promise<UploadedRFP> {
  const truncated = rawText.substring(0, 12000); // keep within token limits

  const prompt = `You are an expert RFP document parser. Extract structured event data from the following RFP document text.

DOCUMENT TEXT:
---
${truncated}
---

Extract ALL events/activities mentioned in this document. For each event, identify:
- eventName: The name or title of the event
- arabicName: Arabic name if present (empty string if not)
- date: The date or timeframe (e.g., "March 2026", "Q1 2026", "TBD")
- quarter: Quarter (Q1, Q2, Q3, Q4) if mentioned
- category: Category type (Corporate, Cultural, Sports, Entertainment, Government, Social, Conference, Launch, Gala, Workshop, General)
- estimatedAttendance: Number of expected attendees (0 if not mentioned)
- eventTier: "Major" for large/flagship/VIP events, "Medium" for mid-size conferences/summits, "Light" for small/internal events
- venue: Venue if mentioned
- keyServices: Key services required (comma-separated)

Also extract:
- clientName: The client or organization name
- rfpSummary: A 2-3 sentence summary of the entire RFP
- requirements: Array of key requirements/objectives mentioned in the RFP
- requiredDocuments: Array of documents that must be submitted with the proposal/bid (e.g., "Company Registration Certificate", "Financial Statements", "Tax Compliance Certificate", "Insurance Certificate", "Past Project References", "Team CVs", "Bank Guarantee", "Bid Bond", "Technical Proposal", "Financial Proposal", "NDA/Confidentiality Agreement"). Look for submission requirements, mandatory documents, eligibility criteria, compliance documents, or any annexures/attachments the bidder must provide.

Respond ONLY with valid JSON in this exact format:
{
  "clientName": "string",
  "rfpSummary": "string",
  "requirements": ["string"],
  "requiredDocuments": ["string"],
  "events": [
    {
      "eventName": "string",
      "arabicName": "string",
      "date": "string",
      "quarter": "string",
      "category": "string",
      "estimatedAttendance": 0,
      "eventTier": "string",
      "venue": "string",
      "keyServices": "string"
    }
  ]
}`;

  const response = await callGemini(prompt, apiKey);
  const jsonStr = extractJSON(response);
  const parsed = JSON.parse(jsonStr);

  const events: RFPEvent[] = (parsed.events || []).map((e: Record<string, unknown>, i: number) => ({
    number: i + 1,
    eventName: String(e.eventName || "Untitled Event"),
    arabicName: String(e.arabicName || ""),
    date: String(e.date || "TBD"),
    quarter: String(e.quarter || ""),
    category: String(e.category || "General"),
    estimatedAttendance: Number(e.estimatedAttendance) || 0,
    eventTier: String(e.eventTier || "Light"),
    venue: String(e.venue || ""),
    keyServices: String(e.keyServices || ""),
  }));

  if (events.length === 0) {
    throw new Error("AI could not identify any events in this document.");
  }

  return {
    fileName,
    events,
    clientName: String(parsed.clientName || ""),
    uploadedAt: new Date().toISOString(),
    rawText: truncated,
    rfpSummary: String(parsed.rfpSummary || ""),
    requirements: Array.isArray(parsed.requirements)
      ? parsed.requirements.map(String)
      : [],
    requiredDocuments: Array.isArray(parsed.requiredDocuments)
      ? parsed.requiredDocuments.map(String)
      : [],
  };
}

export interface TechnicalProposalData {
  id: string;
  rfpFileName: string;
  rfpReference: string;
  clientName: string;
  clientCompany: string;
  eventName: string;
  contractTitle: string;
  contractPeriod: string;
  submittedTo: string;
  createdAt: string;
  sections: ProposalSection[];
}

export interface ProposalSection {
  id: string;
  title: string;
  content: string;
  order: number;
}

/**
 * Use AI to generate a comprehensive technical proposal matching the IDEAS format.
 */
export async function generateTechnicalProposal(
  rfpData: {
    clientName: string;
    eventName: string;
    events: RFPEvent[];
    rfpSummary?: string;
    requirements?: string[];
    rawText?: string;
  },
  apiKey: string
): Promise<ProposalSection[]> {
  const eventsDesc = rfpData.events
    .map((e, i) => `${i + 1}. ${e.eventName} (${e.category}, ${e.eventTier} tier, ~${e.estimatedAttendance} attendees, ${e.date})${e.keyServices ? ` - Services: ${e.keyServices}` : ""}`)
    .join("\n");

  const rfpContext = rfpData.rawText
    ? `\n\nORIGINAL RFP TEXT (excerpt):\n${rfpData.rawText.substring(0, 6000)}`
    : "";

  const prompt = `You are an expert event management proposal writer for Miradore Experiences, a premium event management, production, and creative agency with offices in Riyadh (KSA) and Karachi (Pakistan).

Write a comprehensive, professional TECHNICAL PROPOSAL for the following RFP. Follow the exact structure used in professional government/B2G proposals.

CLIENT: ${rfpData.clientName || "The Client"}
EVENT(S):
${eventsDesc}
${rfpData.rfpSummary ? `\nRFP SUMMARY: ${rfpData.rfpSummary}` : ""}
${rfpData.requirements?.length ? `\nKEY REQUIREMENTS:\n${rfpData.requirements.map((r, i) => `${i + 1}. ${r}`).join("\n")}` : ""}
${rfpContext}

Generate these EXACT sections. Each section must be detailed, specific to this RFP, and written in formal proposal language:

1. "Cover Letter" — Formal letter addressed to the client (2-3 paragraphs). Reference the RFP, state Miradore's qualifications, confirm acceptance of terms. Sign off as "Adeel Ahmed, Director, Miradore Experiences".

2. "Company Overview & Ownership Structure" — About Miradore Experiences: dual-market presence (Riyadh KSA + Karachi Pakistan), founded 2019, 35+ staff, core verticals (Government Events, Defence & Security, Technology, Cultural Diplomacy, Corporate Communications). Include service capabilities list. End with "Why Miradore" paragraph.

3. "Understanding of Scope & Strategic Approach" — Show deep understanding of the client's event/project. Outline strategic vision with 2-3 pillars. Include campaign architecture (phases), measurement approach. Be specific to the events described.

4. "Section-by-Section Methodology" — For EACH major scope area/event/service requirement identified in the RFP, provide bullet-point methodology: approach, key deliverables, quality assurance. Use numbered sub-sections (Section 1, Section 2, etc.). This should be the longest section.

5. "Proposed Team Structure & Key Personnel" — Propose a dedicated team with roles, names (use realistic names), years of experience, and engagement type (Dedicated/Part-time). Format as numbered list. Include an org chart description.

6. "Portfolio & Case Studies" — 3-5 relevant case studies. Each with: Client, Scope, and 3-4 bullet points of deliverables. Include events similar to what's being proposed.

7. "Subcontractors & Partner Agencies" — List specialist partners for areas like international PR, OOH advertising, influencer management, printing. Note that Miradore retains full accountability.

8. "AI-Augmented Delivery Capability" — List AI tools used in workflow: content generation, media planning, pre-visualisation, analytics, design acceleration, translation QA. Include estimated productivity gains.

9. "Declarations" — Include: No Conflict of Interest, No Pending Litigation, NDA Acknowledgement, Acceptance of RFP Terms, Proposal Validity (90 days).

Respond ONLY with valid JSON array:
[
  {"title": "Cover Letter", "content": "..."},
  {"title": "Company Overview & Ownership Structure", "content": "..."},
  ...
]

Make content specific, detailed, and compelling. Each section should be 200-500 words. Use professional language suitable for a government/B2G proposal document.`;

  const response = await callGemini(prompt, apiKey);
  const jsonStr = extractJSON(response);
  const sections: { title: string; content: string }[] = JSON.parse(jsonStr);

  return sections.map((s, i) => ({
    id: `section-${Date.now()}-${i}`,
    title: s.title,
    content: s.content,
    order: i,
  }));
}
