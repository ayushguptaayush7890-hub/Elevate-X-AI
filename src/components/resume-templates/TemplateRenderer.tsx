"use client";

import React from "react";
import { ResumeFullData, TemplateId } from "@/types/resume-generator";
import { ModernProfessional } from "./ModernProfessional";
import { MinimalClean } from "./MinimalClean";
import { ATSFriendly } from "./ATSFriendly";
import { CorporateExecutive } from "./CorporateExecutive";
import { CreativePortfolio } from "./CreativePortfolio";
import { TechnicalDeveloper } from "./TechnicalDeveloper";
import { DataScience } from "./DataScience";
import { FresherResume } from "./FresherResume";
import { ExperiencedProfessional } from "./ExperiencedProfessional";
import { ElegantProfessional } from "./ElegantProfessional";

export const TEMPLATE_LIST: { id: TemplateId; name: string; tag: string; description: string }[] = [
  { id: "modern", name: "Modern Professional", tag: "Split Layout", description: "Two-column design with dark left sidebar and crisp right content pane." },
  { id: "minimal", name: "Minimal Clean", tag: "Monochrome", description: "Minimalist aesthetic with high whitespace and fine dividing rules." },
  { id: "ats_friendly", name: "ATS-Friendly", tag: "100% Parser Compliant", description: "Standard single-column format optimized for corporate ATS parsers." },
  { id: "corporate_executive", name: "Corporate Executive", tag: "Executive", description: "Formal serif typography with gold and navy dividing accents." },
  { id: "creative_portfolio", name: "Creative Portfolio", tag: "Vibrant & Visual", description: "Gradient banner header with project cards and skill badge cloud." },
  { id: "technical", name: "Technical / Software Dev", tag: "Developer Terminal", description: "Monospace accents, code snippet boxes, and categorized tech badges." },
  { id: "data_science", name: "AI / Data Science", tag: "Research & ML", description: "Structured research format highlighting AI/ML models and publications." },
  { id: "fresher", name: "Fresher / Student", tag: "Entry-Level", description: "Prioritizes academic coursework, degree GPA, and hands-on projects." },
  { id: "experienced", name: "Experienced Lead", tag: "Leadership First", description: "Chronological leadership progression and business impact metrics." },
  { id: "elegant", name: "Elegant Professional", tag: "Editorial", description: "Timeless serif typography, refined borders, and understated luxury." },
];

export function TemplateRenderer({ resume }: { resume: ResumeFullData }) {
  switch (resume.templateId) {
    case "minimal":
      return <MinimalClean resume={resume} />;
    case "ats_friendly":
      return <ATSFriendly resume={resume} />;
    case "corporate_executive":
      return <CorporateExecutive resume={resume} />;
    case "creative_portfolio":
      return <CreativePortfolio resume={resume} />;
    case "technical":
      return <TechnicalDeveloper resume={resume} />;
    case "data_science":
      return <DataScience resume={resume} />;
    case "fresher":
      return <FresherResume resume={resume} />;
    case "experienced":
      return <ExperiencedProfessional resume={resume} />;
    case "elegant":
      return <ElegantProfessional resume={resume} />;
    case "modern":
    default:
      return <ModernProfessional resume={resume} />;
  }
}
