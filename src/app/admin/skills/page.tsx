"use client";

import React, { useState } from "react";
import { AdminShell } from "@/components/layout/AdminShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { BrandButton } from "@/components/ui/BrandButton";
import { toast } from "sonner";
import { Layers, Plus, Search, Tag, CheckCircle2 } from "lucide-react";

export default function AdminSkillsPage() {
  const [categories, setCategories] = useState([
    {
      name: "Textiles, Apparel & Tailoring",
      skillsCount: 142,
      occupations: ["Master Tailor", "Pattern Maker", "Sewing Operator", "Apparel QA"],
      nsqfLevel: "Level 4 - 6",
    },
    {
      name: "Automotive & Mechanical Maintenance",
      skillsCount: 185,
      occupations: ["Diesel Mechanic", "Auto Electrician", "Hydraulics Tech"],
      nsqfLevel: "Level 3 - 5",
    },
    {
      name: "Electrical, Solar & Power Electronics",
      skillsCount: 120,
      occupations: ["Domestic Wireman", "Solar Inverter Technician", "Control Panel Fitter"],
      nsqfLevel: "Level 4 - 5",
    },
    {
      name: "Food Production & Commercial Culinary",
      skillsCount: 95,
      occupations: ["Bakery Production Artisan", "Food Safety Inspector", "Kitchen Lead"],
      nsqfLevel: "Level 3 - 4",
    },
  ]);

  return (
    <AdminShell>
      <div className="space-y-6">
        <PageHeader
          badge="Taxonomy & NSQF Standards"
          title="Skill Taxonomy & Occupational Framework"
          description="Standardize informal competencies into international vocational frameworks and National Skills Qualification Frameworks (NSQF)."
          variant="navy"
          actions={
            <BrandButton
              variant="gold"
              size="sm"
              onClick={() => toast.info("New skill category creator dialog opened.")}
            >
              <Plus className="w-4 h-4 mr-1.5" />
              <span>Add Skill Category</span>
            </BrandButton>
          }
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {categories.map((cat, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-xs space-y-4 hover:border-[#D6A84B] transition-all"
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]">
                    {cat.nsqfLevel}
                  </span>
                  <h3 className="text-base font-bold text-[#17233F] mt-2">{cat.name}</h3>
                </div>
                <span className="text-xs font-bold text-[#17233F] bg-[#F0D99B]/40 px-2.5 py-1 rounded-full border border-[#D6A84B]">
                  {cat.skillsCount} Skills Mapped
                </span>
              </div>

              <div className="space-y-2 pt-3 border-t border-[#E6DFD1] text-xs">
                <span className="text-[10px] font-bold uppercase text-[#687187] tracking-wider">
                  Associated Occupations
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {cat.occupations.map((occ, oIdx) => (
                    <span
                      key={oIdx}
                      className="text-[11px] px-2.5 py-0.5 rounded-full bg-[#FBF8F1] text-[#20243A] border border-[#E6DFD1] font-medium"
                    >
                      {occ}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AdminShell>
  );
}
