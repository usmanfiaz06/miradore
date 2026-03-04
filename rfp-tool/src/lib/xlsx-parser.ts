"use client";

import * as XLSX from "xlsx";
import { RFPEvent, UploadedRFP } from "@/types";
import { parsePDFFile } from "./pdf-parser";
import { parseDocxFile } from "./docx-parser";

export async function parseRFPFile(file: File): Promise<UploadedRFP> {
  const name = file.name.toLowerCase();

  // Route PDF files to the dedicated PDF parser
  if (name.endsWith(".pdf") || file.type === "application/pdf") {
    return parsePDFFile(file);
  }

  // Route Word documents to the DOCX parser
  if (
    name.endsWith(".docx") ||
    name.endsWith(".doc") ||
    file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ||
    file.type === "application/msword"
  ) {
    return parseDocxFile(file);
  }

  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        const workbook = XLSX.read(data, { type: "array" });

        const events: RFPEvent[] = [];
        let clientName = "";

        // Try to parse Event Calendar sheet
        const calendarSheet =
          workbook.Sheets["Event Calendar"] ||
          workbook.Sheets[workbook.SheetNames[0]];

        if (calendarSheet) {
          const jsonData = XLSX.utils.sheet_to_json(calendarSheet, {
            header: 1,
          }) as unknown[][];

          // Extract client info from first rows
          if (jsonData[0] && typeof jsonData[0][0] === "string") {
            clientName = jsonData[0][0];
          }

          // Find header row
          let headerRowIndex = -1;
          for (let i = 0; i < Math.min(jsonData.length, 10); i++) {
            const row = jsonData[i] as string[];
            if (
              row &&
              row.some(
                (cell) =>
                  typeof cell === "string" &&
                  (cell.toLowerCase().includes("event name") ||
                    cell.toLowerCase().includes("event"))
              )
            ) {
              headerRowIndex = i;
              break;
            }
          }

          if (headerRowIndex === -1) headerRowIndex = 3; // Default fallback

          // Parse events from rows after header
          for (let i = headerRowIndex + 1; i < jsonData.length; i++) {
            const row = jsonData[i] as (string | number)[];
            if (!row || !row[1]) continue; // Skip empty rows

            // Stop at summary sections
            if (
              typeof row[0] === "string" &&
              (row[0].toLowerCase().includes("budget") ||
                row[0].toLowerCase().includes("total") ||
                row[0].toLowerCase().includes("summary"))
            ) {
              break;
            }

            const event: RFPEvent = {
              number: row[0] || i - headerRowIndex,
              eventName: String(row[1] || ""),
              arabicName: String(row[2] || ""),
              date: String(row[3] || "TBD"),
              quarter: String(row[4] || ""),
              category: String(row[5] || ""),
              estimatedAttendance: Number(row[6]) || 0,
              eventTier: String(row[7] || "Light"),
            };

            if (event.eventName.trim()) {
              events.push(event);
            }
          }

          // Try to parse Technical Proposal for additional details
          const techSheet = workbook.Sheets["Technical Proposal"];
          if (techSheet) {
            const techData = XLSX.utils.sheet_to_json(techSheet, {
              header: 1,
            }) as unknown[][];

            let techHeaderIndex = -1;
            for (let i = 0; i < Math.min(techData.length, 10); i++) {
              const row = techData[i] as string[];
              if (
                row &&
                row.some(
                  (cell) =>
                    typeof cell === "string" &&
                    cell.toLowerCase().includes("event name")
                )
              ) {
                techHeaderIndex = i;
                break;
              }
            }

            if (techHeaderIndex >= 0) {
              for (
                let i = techHeaderIndex + 1;
                i < techData.length;
                i++
              ) {
                const row = techData[i] as string[];
                if (!row || !row[1]) continue;

                const matchingEvent = events.find(
                  (e) =>
                    e.eventName.toLowerCase() ===
                    String(row[1]).toLowerCase()
                );

                if (matchingEvent) {
                  matchingEvent.venue = String(row[3] || "");
                  matchingEvent.stageDecor = String(row[4] || "");
                  matchingEvent.avRequirements = String(row[5] || "");
                  matchingEvent.keyServices = String(row[6] || "");
                }
              }
            }
          }
        }

        resolve({
          fileName: file.name,
          events,
          clientName,
          uploadedAt: new Date().toISOString(),
        });
      } catch (error) {
        reject(new Error("Failed to parse file. Please ensure it's a valid Excel file."));
      }
    };

    reader.onerror = () => reject(new Error("Failed to read file."));
    reader.readAsArrayBuffer(file);
  });
}
