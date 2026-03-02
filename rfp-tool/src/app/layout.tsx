import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Miradore — RFP Quotation Tool",
  description:
    "Internal tool for managing RFP uploads and generating professional event quotations across Pakistan, KSA, and Dubai.",
  icons: {
    icon: "/images/miradore-logo.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
