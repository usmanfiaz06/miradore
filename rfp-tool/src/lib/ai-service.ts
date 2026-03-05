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
      throw new Error("AI request timed out after 30s. Please try again.");
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

Respond ONLY with valid JSON in this exact format:
{
  "clientName": "string",
  "rfpSummary": "string",
  "requirements": ["string"],
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
  };
}

export interface TechnicalProposalData {
  id: string;
  rfpFileName: string;
  clientName: string;
  clientCompany: string;
  eventName: string;
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
 * Use AI to generate a comprehensive technical proposal.
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

  const prompt = `You are an expert event management proposal writer for Miradore, a premium event management, production, and creative agency operating in Pakistan, Saudi Arabia, and Dubai/UAE.

Write a comprehensive, professional TECHNICAL PROPOSAL for the following RFP:

CLIENT: ${rfpData.clientName || "The Client"}
EVENT(S):
${eventsDesc}
${rfpData.rfpSummary ? `\nRFP SUMMARY: ${rfpData.rfpSummary}` : ""}
${rfpData.requirements?.length ? `\nKEY REQUIREMENTS:\n${rfpData.requirements.map((r, i) => `${i + 1}. ${r}`).join("\n")}` : ""}
${rfpContext}

Generate these sections with rich, professional content. Be specific to the events and requirements described. Include concrete deliverables and methodologies.

Respond ONLY with valid JSON array of sections:
[
  {
    "title": "Executive Summary",
    "content": "2-3 paragraphs summarizing our understanding, approach, and why Miradore is the right partner..."
  },
  {
    "title": "Company Profile",
    "content": "About Miradore - our expertise in event management, production, and creative services across Pakistan, KSA, and UAE. Mention our track record with similar events..."
  },
  {
    "title": "Understanding of Requirements",
    "content": "Detailed analysis of the client's needs based on the RFP. Show deep understanding of each event and its objectives..."
  },
  {
    "title": "Proposed Methodology & Approach",
    "content": "Our step-by-step approach to planning and executing the events. Include phases: Discovery, Planning, Pre-production, Execution, Post-event..."
  },
  {
    "title": "Event Concepts & Creative Direction",
    "content": "Creative vision for each event. Include themes, staging concepts, visual identity, and experience design..."
  },
  {
    "title": "Technical Production Plan",
    "content": "Detailed production specifications including AV equipment, staging, lighting, sound, and technical infrastructure..."
  },
  {
    "title": "Project Team & Staffing",
    "content": "Key team members and roles. Include Project Director, Creative Director, Production Manager, Event Coordinators, and support staff..."
  },
  {
    "title": "Timeline & Milestones",
    "content": "Detailed project timeline from contract signing through post-event. Include key milestones and deliverable dates..."
  },
  {
    "title": "Quality Assurance & Risk Management",
    "content": "Our quality control processes, risk mitigation strategies, contingency plans, and safety protocols..."
  },
  {
    "title": "Value-Added Services",
    "content": "Additional services we offer that add value: digital/social media coverage, sustainability practices, VIP management, post-event analytics..."
  },
  {
    "title": "Terms & Conditions",
    "content": "Standard terms including payment schedule, cancellation policy, intellectual property, confidentiality, and liability..."
  }
]

Make the content specific, detailed, and compelling. Each section should be 150-300 words. Use professional language suitable for a formal proposal document.`;

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
