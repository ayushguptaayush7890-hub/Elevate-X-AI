"use client";

import React, { useState, useRef } from "react";
import { ResumeFullData } from "@/types/resume-generator";
import { DesignSpecification, TypographySystem } from "@/types/resume-design-engine";
import { UniversalResumeRenderer } from "./UniversalResumeRenderer";
import { PALETTES } from "@/services/resume-design-engine";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import {
  Download,
  FileText,
  Save,
  CheckCircle2,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Palette,
  Type,
  LayoutGrid,
  ArrowLeft,
  ChevronDown,
  Sparkles,
  Edit3,
  Sliders,
  Check,
} from "lucide-react";

interface Props {
  resume: ResumeFullData;
  design: DesignSpecification;
  onChangeDesign: (newDesign: DesignSpecification) => void;
  onUpdateResume: (updated: ResumeFullData) => void;
  onBackToGallery: () => void;
  onBackToForm: () => void;
}

export function ResumeStudio({
  resume,
  design,
  onChangeDesign,
  onUpdateResume,
  onBackToGallery,
  onBackToForm,
}: Props) {
  const [zoom, setZoom] = useState(100);
  const [activeTab, setActiveTab] = useState<"design" | "content">("design");
  const [isExportingDocx, setIsExportingDocx] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const printRef = useRef<HTMLDivElement>(null);

  // PDF Export via native print stylesheet
  const handlePrintPdf = () => {
    window.print();
  };

  // Word Export (.docx) via backend service
  const handleExportDocx = async () => {
    try {
      setIsExportingDocx(true);
      toast.info("Generating Word (.docx) document...");
      const blob = await apiService.exportResumeDocx(resume);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${resume.personalInfo.fullName.replace(/\s+/g, "_") || "Resume"}_ElevateX.docx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success("Word document downloaded successfully!");
    } catch (err: any) {
      console.error(err);
      toast.error(err.message || "Failed to export Word document");
    } finally {
      setIsExportingDocx(false);
    }
  };

  // Database Save
  const handleSaveToDb = async () => {
    try {
      setIsSaving(true);
      const saved = await apiService.saveResume({
        title: `${resume.personalInfo.fullName || "My"} Resume`,
        template_id: design.id,
        resume_data: resume,
        is_primary: true,
      });
      toast.success("Resume saved successfully to your profile!");
    } catch (err: any) {
      console.error(err);
      toast.error(err.message || "Failed to save resume");
    } finally {
      setIsSaving(false);
    }
  };

  // Palette switcher
  const handleSelectPalette = (palette: typeof PALETTES[0]) => {
    onChangeDesign({
      ...design,
      palette,
    });
    onUpdateResume({
      ...resume,
      accentColor: palette.primary,
    });
  };

  // Typography switcher
  const handleSelectTypography = (typography: TypographySystem) => {
    onChangeDesign({
      ...design,
      typography,
    });
  };

  // Spacing switcher
  const handleSelectSpacing = (spacing: "compact" | "normal" | "spacious") => {
    onChangeDesign({
      ...design,
      spacing,
    });
  };

  return (
    <div className="space-y-6">
      {/* Studio Top Action Bar */}
      <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4 print:hidden">
        <div className="flex items-center gap-3">
          <button
            onClick={onBackToGallery}
            className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors cursor-pointer flex items-center gap-1.5 text-xs font-bold"
          >
            <ArrowLeft className="w-4 h-4" /> Switch Design
          </button>
          <div className="h-6 w-px bg-slate-200" />
          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-black text-sm text-slate-900">{design.name}</h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-bold">
                {design.id}
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              {design.category.toUpperCase()} • {design.targetRole.toUpperCase()}
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto justify-end">
          {/* Zoom controls */}
          <div className="hidden sm:flex items-center gap-1 bg-slate-100 rounded-xl p-1 border border-slate-200 text-xs font-mono">
            <button
              onClick={() => setZoom((prev) => Math.max(50, prev - 15))}
              className="p-1.5 hover:bg-white rounded-lg text-slate-600 cursor-pointer"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="px-2 font-bold text-slate-700">{zoom}%</span>
            <button
              onClick={() => setZoom((prev) => Math.min(150, prev + 15))}
              className="p-1.5 hover:bg-white rounded-lg text-slate-600 cursor-pointer"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setZoom(100)}
              className="p-1.5 hover:bg-white rounded-lg text-slate-600 cursor-pointer"
              title="Reset Zoom"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Save to DB */}
          <button
            onClick={handleSaveToDb}
            disabled={isSaving}
            className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <Save className="w-3.5 h-3.5 text-slate-600" />
            {isSaving ? "Saving..." : "Save"}
          </button>

          {/* Word Export (.docx) */}
          <button
            onClick={handleExportDocx}
            disabled={isExportingDocx}
            className="px-4 py-2 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-xs font-bold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <FileText className="w-3.5 h-3.5" />
            {isExportingDocx ? "Exporting..." : "Word (.docx)"}
          </button>

          {/* PDF Download */}
          <button
            onClick={handlePrintPdf}
            className="px-5 py-2 rounded-xl bg-gradient-to-r from-[#D6A84B] to-[#F0D99B] text-[#17233F] text-xs font-black uppercase tracking-wider flex items-center gap-2 shadow-md shadow-[#D6A84B]/20 hover:opacity-95 transition-all cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" /> Download PDF
          </button>
        </div>
      </div>

      {/* Main Studio Workspace: Controls Sidebar + Canvas */}
      <div className="grid grid-cols-12 gap-6 items-start">
        {/* Controls Panel (4 Cols on Desktop) */}
        <div className="col-span-12 lg:col-span-4 space-y-5 print:hidden">
          {/* Tabs */}
          <div className="flex bg-slate-200/80 p-1 rounded-xl">
            <button
              onClick={() => setActiveTab("design")}
              className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer flex items-center justify-center gap-1.5 ${
                activeTab === "design" ? "bg-white text-slate-900 shadow-xs" : "text-slate-600 hover:text-slate-900"
              }`}
            >
              <Palette className="w-3.5 h-3.5" /> Style & Palette
            </button>
            <button
              onClick={() => setActiveTab("content")}
              className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer flex items-center justify-center gap-1.5 ${
                activeTab === "content" ? "bg-white text-slate-900 shadow-xs" : "text-slate-600 hover:text-slate-900"
              }`}
            >
              <Edit3 className="w-3.5 h-3.5" /> Edit Content
            </button>
          </div>

          {/* Design Controls */}
          {activeTab === "design" && (
            <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-6">
              {/* Color Palettes */}
              <div className="space-y-2.5">
                <label className="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                  <Palette className="w-3.5 h-3.5 text-[#7355D9]" /> Color Theme
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {PALETTES.map((pal, idx) => {
                    const isSelected = design.palette.name === pal.name;
                    return (
                      <button
                        key={idx}
                        onClick={() => handleSelectPalette(pal)}
                        className={`p-2 rounded-xl border text-left text-[11px] transition-all cursor-pointer flex items-center gap-2 ${
                          isSelected
                            ? "border-[#D6A84B] bg-[#D6A84B]/10 font-bold"
                            : "border-slate-200 hover:border-slate-300"
                        }`}
                      >
                        <div
                          className="w-4 h-4 rounded-full shrink-0 border border-black/10"
                          style={{ backgroundColor: pal.primary }}
                        />
                        <span className="truncate">{pal.name.split("&")[0].trim()}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Typography */}
              <div className="space-y-2.5">
                <label className="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                  <Type className="w-3.5 h-3.5 text-[#7355D9]" /> Typography System
                </label>
                <div className="space-y-1.5">
                  {[
                    { id: "modern_sans", label: "Modern Geometric Sans (Inter)", font: "font-sans" },
                    { id: "classic_serif", label: "Classic Editorial Serif (Georgia)", font: "font-serif" },
                    { id: "technical_mono", label: "Technical Engineering Mono", font: "font-mono" },
                    { id: "display_serif_body_sans", label: "Executive Display Serif + Sans Body", font: "font-sans" },
                  ].map((t) => (
                    <button
                      key={t.id}
                      onClick={() => handleSelectTypography(t.id as TypographySystem)}
                      className={`w-full p-2.5 rounded-xl border text-left text-xs transition-all cursor-pointer flex items-center justify-between ${
                        design.typography === t.id
                          ? "border-[#7355D9] bg-[#7355D9]/10 font-bold text-[#7355D9]"
                          : "border-slate-200 hover:border-slate-300 text-slate-700"
                      }`}
                    >
                      <span className={t.font}>{t.label}</span>
                      {design.typography === t.id && <Check className="w-3.5 h-3.5" />}
                    </button>
                  ))}
                </div>
              </div>

              {/* Spacing Density */}
              <div className="space-y-2.5">
                <label className="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                  <Sliders className="w-3.5 h-3.5 text-[#7355D9]" /> Spacing Density
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {(["compact", "normal", "spacious"] as const).map((s) => (
                    <button
                      key={s}
                      onClick={() => handleSelectSpacing(s)}
                      className={`py-2 rounded-xl border text-center text-xs font-bold uppercase transition-all cursor-pointer ${
                        design.spacing === s
                          ? "border-[#17233F] bg-[#17233F] text-white"
                          : "border-slate-200 hover:bg-slate-50 text-slate-700"
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Quick Content Editor */}
          {activeTab === "content" && (
            <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-4 max-h-[700px] overflow-y-auto">
              <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                <span className="font-black text-xs uppercase tracking-wider text-slate-800">
                  Quick Content Adjuster
                </span>
                <button
                  onClick={onBackToForm}
                  className="text-[11px] font-bold text-[#7355D9] hover:underline cursor-pointer"
                >
                  Full 7-Step Wizard ↗
                </button>
              </div>

              {/* Name & Title */}
              <div className="space-y-2">
                <label className="text-[11px] font-bold text-slate-600">Full Name</label>
                <input
                  type="text"
                  value={resume.personalInfo.fullName}
                  onChange={(e) =>
                    onUpdateResume({
                      ...resume,
                      personalInfo: { ...resume.personalInfo, fullName: e.target.value },
                    })
                  }
                  className="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs"
                />
              </div>

              <div className="space-y-2">
                <label className="text-[11px] font-bold text-slate-600">Professional Title</label>
                <input
                  type="text"
                  value={resume.personalInfo.professionalTitle}
                  onChange={(e) =>
                    onUpdateResume({
                      ...resume,
                      personalInfo: { ...resume.personalInfo, professionalTitle: e.target.value },
                    })
                  }
                  className="w-full px-3 py-1.5 border border-slate-200 rounded-lg text-xs"
                />
              </div>

              <div className="space-y-2">
                <label className="text-[11px] font-bold text-slate-600">Professional Summary</label>
                <textarea
                  rows={4}
                  value={resume.personalInfo.summary}
                  onChange={(e) =>
                    onUpdateResume({
                      ...resume,
                      personalInfo: { ...resume.personalInfo, summary: e.target.value },
                    })
                  }
                  className="w-full p-2.5 border border-slate-200 rounded-lg text-xs leading-relaxed"
                />
              </div>
            </div>
          )}
        </div>

        {/* Live Resume Canvas Preview (8 Cols on Desktop) */}
        <div className="col-span-12 lg:col-span-8 flex justify-center overflow-x-auto p-4 bg-slate-200/50 rounded-3xl border border-slate-300/60 shadow-inner">
          <div
            ref={printRef}
            className="transition-transform duration-200 origin-top"
            style={{ transform: `scale(${zoom / 100})` }}
          >
            <UniversalResumeRenderer
              resume={resume}
              design={design}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
