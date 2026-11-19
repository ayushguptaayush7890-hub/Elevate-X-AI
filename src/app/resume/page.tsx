"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { PageHeader } from "@/components/ui/PageHeader";
import { defaultResumeData } from "@/data/mock-data";
import { ResumeData } from "@/types";
import { toast } from "sonner";
import {
  FileText,
  Sparkles,
  Download,
  CheckCircle2,
  Sliders,
  Layers,
  Award
} from "lucide-react";

export default function ResumeBuilderPage() {
  const [resume, setResume] = useState<ResumeData>(defaultResumeData);
  const [selectedTemplate, setSelectedTemplate] = useState<"modern" | "minimal" | "skills_focused">("modern");
  const [isImproving, setIsImproving] = useState(false);

  const handleImproveSummary = () => {
    setIsImproving(true);
    setTimeout(() => {
      setIsImproving(false);
      setResume((prev) => ({
        ...prev,
        summary:
          "High-precision Garment Artisan and QA Specialist with 5+ years of demonstrable mastery in high-speed industrial lockstitch machinery, bespoke pattern grading, and defect minimization. Recognized by Elevate X AI with advanced scores in stitch balance and tolerance accuracy. Dedicated to delivering zero-defect manufacturing standards for global export apparel lines.",
      }));
      toast.success("Professional summary enhanced with high-impact action keywords.");
    }, 600);
  };

  const handleDownloadPdf = () => {
    window.print();
    toast.success("Printing / PDF export triggered for ATS resume.");
  };

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Top Header */}
        <div className="no-print">
          <PageHeader
            badge="ATS Document Engineering"
            title="AI Professional Resume Builder"
            description="Translate informal trade craftsmanship into structured, ATS-compliant resumes tailored with verified skills and export industry standards."
            variant="navy"
            actions={
              <BrandButton
                variant="gold"
                size="md"
                onClick={handleDownloadPdf}
              >
                <Download className="w-4 h-4 mr-1.5" />
                <span>Export ATS PDF</span>
              </BrandButton>
            }
          />
        </div>

        {/* Main Two-Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column: Editor Controls (5 cols) */}
          <div className="lg:col-span-5 space-y-5 no-print">
            {/* Template Switcher */}
            <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
              <span className="text-xs font-bold text-[#17233F] uppercase tracking-wider block">
                ATS Layout Template
              </span>
              <div className="grid grid-cols-3 gap-2 text-xs">
                <button
                  type="button"
                  onClick={() => setSelectedTemplate("modern")}
                  className={`py-2 px-2.5 rounded-xl border text-center transition-all ${
                    selectedTemplate === "modern"
                      ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                      : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                  }`}
                >
                  Royal Modern
                </button>
                <button
                  type="button"
                  onClick={() => setSelectedTemplate("minimal")}
                  className={`py-2 px-2.5 rounded-xl border text-center transition-all ${
                    selectedTemplate === "minimal"
                      ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                      : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                  }`}
                >
                  Executive Ivory
                </button>
                <button
                  type="button"
                  onClick={() => setSelectedTemplate("skills_focused")}
                  className={`py-2 px-2.5 rounded-xl border text-center transition-all ${
                    selectedTemplate === "skills_focused"
                      ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                      : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                  }`}
                >
                  Skills-First
                </button>
              </div>
            </div>

            {/* AI Tailoring Assistant */}
            <div className="p-5 rounded-2xl bg-[#17233F] text-white border border-[#D6A84B]/30 shadow-md space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-[#F0D99B] flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-[#D6A84B]" /> AI Resume Optimizer
                </span>
                <button
                  type="button"
                  onClick={handleImproveSummary}
                  disabled={isImproving}
                  className="text-xs font-bold text-[#D6A84B] hover:text-[#F0D99B] underline"
                >
                  {isImproving ? "Rewriting..." : "Enhance Summary"}
                </button>
              </div>
              <p className="text-xs text-[#F5F0E6]/80 leading-relaxed">
                Auto-rewrite informal duties using verified metric verbs without exaggerating qualifications.
              </p>
            </div>

            {/* Edit Fields */}
            <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
              <h3 className="text-xs font-bold text-[#17233F] uppercase tracking-wider">Candidate Profile Fields</h3>

              <div className="space-y-3">
                <div className="space-y-1">
                  <label className="text-xs font-semibold text-[#687187]">Full Name</label>
                  <input
                    type="text"
                    value={resume.fullName}
                    onChange={(e) => setResume({ ...resume, fullName: e.target.value })}
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-semibold text-[#687187]">Professional Headline</label>
                  <input
                    type="text"
                    value={resume.headline}
                    onChange={(e) => setResume({ ...resume, headline: e.target.value })}
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-semibold text-[#687187]">Email & Phone</label>
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      type="text"
                      value={resume.email}
                      onChange={(e) => setResume({ ...resume, email: e.target.value })}
                      className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                    />
                    <input
                      type="text"
                      value={resume.phone}
                      onChange={(e) => setResume({ ...resume, phone: e.target.value })}
                      className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-semibold text-[#687187]">Executive Summary</label>
                  <textarea
                    rows={4}
                    value={resume.summary}
                    onChange={(e) => setResume({ ...resume, summary: e.target.value })}
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl p-3 text-xs sm:text-sm text-[#20243A] leading-relaxed resize-none focus:outline-none focus:border-[#D6A84B]"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Live ATS Resume Preview (7 cols) */}
          <div className="lg:col-span-7">
            <div className="p-8 sm:p-10 rounded-2xl bg-white text-[#20243A] border-2 border-[#E6DFD1] shadow-xl space-y-6 font-sans text-xs resume-print-area">
              {/* Template Header */}
              <div className="pb-4 border-b-2 border-[#17233F]">
                <h1 className="text-2xl font-black text-[#17233F] tracking-tight">{resume.fullName}</h1>
                <p className="text-sm font-bold text-[#7355D9] mt-0.5">{resume.headline}</p>
                <div className="flex flex-wrap gap-2.5 text-xs text-[#687187] mt-2">
                  <span>{resume.email}</span>
                  <span>•</span>
                  <span>{resume.phone}</span>
                  <span>•</span>
                  <span>{resume.location}</span>
                  <span>•</span>
                  <span className="font-bold text-[#27856B] bg-[#DCEAE6] px-2 py-0.5 rounded border border-[#27856B]/30">
                    Elevate X Verified Profile
                  </span>
                </div>
              </div>

              {/* Summary */}
              <div className="space-y-1.5">
                <h2 className="text-xs font-bold uppercase tracking-wider text-[#17233F] border-b border-[#E6DFD1] pb-1">
                  Professional Profile
                </h2>
                <p className="text-xs text-[#20243A] leading-relaxed">{resume.summary}</p>
              </div>

              {/* Verified Skills */}
              <div className="space-y-2">
                <h2 className="text-xs font-bold uppercase tracking-wider text-[#17233F] border-b border-[#E6DFD1] pb-1">
                  Verified Technical Competencies
                </h2>
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <strong className="text-[#17233F] block mb-1">Trade & Machinery:</strong>
                    <ul className="list-disc list-inside space-y-1 text-[#20243A]">
                      {resume.skills.technical.map((sk, i) => (
                        <li key={i}>{sk}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <strong className="text-[#17233F] block mb-1">Transferable Strengths:</strong>
                    <ul className="list-disc list-inside space-y-1 text-[#20243A]">
                      {resume.skills.transferable.map((sk, i) => (
                        <li key={i}>{sk}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* Experience */}
              <div className="space-y-3">
                <h2 className="text-xs font-bold uppercase tracking-wider text-[#17233F] border-b border-[#E6DFD1] pb-1">
                  Work Experience & Practical Mastery
                </h2>
                {resume.experience.map((exp) => (
                  <div key={exp.id} className="space-y-1">
                    <div className="flex justify-between font-bold text-[#17233F]">
                      <span>{exp.role}</span>
                      <span className="text-[#687187] font-normal">{exp.period}</span>
                    </div>
                    <p className="text-xs font-semibold text-[#7355D9]">{exp.organization}</p>
                    <ul className="list-disc list-inside space-y-1 text-xs text-[#20243A] pt-0.5">
                      {exp.highlights.map((h, i) => (
                        <li key={i}>{h}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>

              {/* Education & Credentials */}
              <div className="space-y-2">
                <h2 className="text-xs font-bold uppercase tracking-wider text-[#17233F] border-b border-[#E6DFD1] pb-1">
                  Education & Trade Certifications
                </h2>
                <div className="space-y-1 text-xs text-[#20243A]">
                  {resume.certifications.map((cert, i) => (
                    <p key={i} className="font-semibold text-[#27856B]">
                      ✓ {cert}
                    </p>
                  ))}
                  {resume.education.map((edu) => (
                    <p key={edu.id}>
                      {edu.degree} — <span className="text-[#687187]">{edu.institution} ({edu.year})</span>
                    </p>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
