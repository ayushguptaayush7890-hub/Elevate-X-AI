"use client";

import React from "react";
import { TemplateId } from "@/types/resume-generator";
import { TEMPLATE_LIST } from "./TemplateRenderer";
import { Check, Palette } from "lucide-react";

const ACCENT_COLORS = [
  { name: "Elevate Navy", hex: "#17233F" },
  { name: "Royal Blue", hex: "#1E3A8A" },
  { name: "Teal Emerald", hex: "#0F766E" },
  { name: "Vibrant Indigo", hex: "#4F46E5" },
  { name: "Electric Purple", hex: "#7355D9" },
  { name: "Deep Crimson", hex: "#991B1B" },
  { name: "Charcoal Slate", hex: "#1F2937" },
];

interface TemplateGalleryProps {
  selectedTemplate: TemplateId;
  selectedColor: string;
  onSelectTemplate: (id: TemplateId) => void;
  onSelectColor: (hex: string) => void;
}

export function TemplateGallery({
  selectedTemplate,
  selectedColor,
  onSelectTemplate,
  onSelectColor,
}: TemplateGalleryProps) {
  return (
    <div className="space-y-6">
      {/* Accent Color Palette Selector */}
      <div className="p-4 rounded-2xl bg-white border border-[#E6DFD1] shadow-2xs space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-[#17233F] flex items-center gap-1.5 uppercase tracking-wider">
            <Palette className="w-3.5 h-3.5 text-[#7355D9]" /> Accent Color Palette
          </span>
          <span className="text-[11px] text-[#687187]">Applies to headings & highlights</span>
        </div>
        <div className="flex flex-wrap gap-2 pt-1">
          {ACCENT_COLORS.map((col) => (
            <button
              key={col.hex}
              onClick={() => onSelectColor(col.hex)}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold border transition-all cursor-pointer ${
                selectedColor.toLowerCase() === col.hex.toLowerCase()
                  ? "border-[#17233F] bg-slate-100 shadow-xs"
                  : "border-slate-200 hover:border-slate-400 bg-white"
              }`}
            >
              <span
                className="w-3.5 h-3.5 rounded-full border border-black/10 shrink-0 flex items-center justify-center text-white"
                style={{ backgroundColor: col.hex }}
              >
                {selectedColor.toLowerCase() === col.hex.toLowerCase() && (
                  <Check className="w-2.5 h-2.5 stroke-[3]" />
                )}
              </span>
              <span className="text-[11px] text-slate-700">{col.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* 10 Professional Templates Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-black uppercase text-[#17233F] tracking-wider">
            Choose Resume Template (10 Distinct Layouts)
          </span>
          <span className="text-[11px] font-bold text-[#7355D9] bg-purple-50 px-2 py-0.5 rounded-full">
            Switch anytime without losing data
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {TEMPLATE_LIST.map((tmpl) => {
            const isSelected = selectedTemplate === tmpl.id;
            return (
              <div
                key={tmpl.id}
                onClick={() => onSelectTemplate(tmpl.id)}
                className={`p-3.5 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between text-left ${
                  isSelected
                    ? "bg-[#FBF8F1] border-[#D6A84B] ring-2 ring-[#D6A84B]/40 shadow-sm"
                    : "bg-white border-[#E6DFD1] hover:border-slate-400 shadow-2xs hover:shadow-xs"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[9px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-100 text-slate-700">
                      {tmpl.tag}
                    </span>
                    {isSelected && (
                      <span className="w-4 h-4 rounded-full bg-[#17233F] text-[#F0D99B] flex items-center justify-center">
                        <Check className="w-2.5 h-2.5 stroke-[3]" />
                      </span>
                    )}
                  </div>
                  <h4 className="text-xs font-bold text-[#17233F] leading-snug">{tmpl.name}</h4>
                  <p className="text-[10px] text-slate-500 mt-1 leading-normal line-clamp-2">
                    {tmpl.description}
                  </p>
                </div>

                <div className="pt-3 mt-2 border-t border-slate-100">
                  <span className={`text-[10px] font-bold ${isSelected ? "text-[#D6A84B]" : "text-slate-400"}`}>
                    {isSelected ? "Active Template" : "Click to Apply"}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
