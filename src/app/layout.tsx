import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export const metadata: Metadata = {
  title: "Elevate X AI — Your Experience. Your Skills. Your Future.",
  description: "Transforming real-world informal experience into recognized skills, verified credentials, and high-growth careers through adaptive AI.",
  keywords: [
    "AI career ecosystem",
    "informal skills recognition",
    "vocational AI",
    "resume builder",
    "skill assessment",
    "job matching"
  ],
  authors: [{ name: "Elevate X AI Team" }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} scroll-smooth`}>
      <body className="min-h-screen bg-[#FAFAFF] text-[#17152B] antialiased selection:bg-purple-600/20 selection:text-purple-900">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
