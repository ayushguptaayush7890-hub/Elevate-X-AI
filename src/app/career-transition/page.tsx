"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { PageHeader } from "@/components/ui/PageHeader";
import { mockCareerTransitions } from "@/data/mock-data";
import { CareerTransitionPath } from "@/types";
import { toast } from "sonner";
import {
  TrendingUp,
  ArrowRight,
  Compass,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Briefcase
} from "lucide-react";

export default function CareerTransitionPage() {
  const [currentTrade, setCurrentTrade] = useState("Custom Tailor & Artisan");
  const [pathways] = useState<CareerTransitionPath[]>(mockCareerTransitions);
  const [selectedPath, setSelectedPath] = useState<CareerTransitionPath>(mockCareerTransitions[0]);

  const handleSimulateTrade = (tradeName: string) => {
    setCurrentTrade(tradeName);
    toast.success(`Career transition pathways recomputed for ${tradeName}`);
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          badge="Occupational Mobility Engine"
          title="Career Transition & Skill Transferability"
          description="Discover how your hands-on trade craftsmanship bridges into high-demand formal sector positions with greater stability, benefits, and compensation growth."
          variant="navy"
          actions={
            <div className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40">
              <Compass className="w-4 h-4 text-[#D6A84B]" />
              <span>{pathways.length} Pathways Identified</span>
            </div>
          }
        />

        {/* Current Trade Selector & Simulation Chips */}
        <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <span className="text-xs font-bold text-[#17233F]">Current Trade Background:</span>
              <input
                type="text"
                value={currentTrade}
                onChange={(e) => setCurrentTrade(e.target.value)}
                className="bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-1.5 text-xs sm:text-sm text-[#20243A] font-medium focus:outline-none focus:border-[#D6A84B]"
              />
            </div>
            <span className="text-xs text-[#17233F] font-bold px-3 py-1 rounded-full bg-[#F0D99B] border border-[#D6A84B]">
              Algorithmic Mobility Mapping Active
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="text-xs text-[#687187]">Explore alternative trades:</span>
            {["Custom Tailor", "Automotive Mechanic", "Domestic Electrician", "Carpentry & Joinery"].map((trade) => (
              <button
                key={trade}
                onClick={() => handleSimulateTrade(trade)}
                className="text-xs px-2.5 py-1 rounded-lg bg-[#FBF8F1] border border-[#E6DFD1] text-[#20243A] hover:text-[#17233F] hover:border-[#D6A84B] transition-colors"
              >
                {trade}
              </button>
            ))}
          </div>
        </div>

        {/* Pathways Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {pathways.map((path) => (
            <div
              key={path.id}
              className={`p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm hover:shadow-md space-y-4 cursor-pointer transition-all ${
                selectedPath.id === path.id ? "ring-2 ring-[#D6A84B] border-[#D6A84B]" : ""
              }`}
              onClick={() => setSelectedPath(path)}
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-[#F5F0E6] text-[#17233F] border border-[#E6DFD1]">
                    {path.industry}
                  </span>
                  <h3 className="text-base font-bold text-[#17233F] mt-2">{path.targetRole}</h3>
                </div>
                <div className="text-right">
                  <span className="text-xs font-black px-3 py-1 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]">
                    {path.suitabilityScore}% Fit
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-3 text-xs">
                <span className="text-[#17233F] font-bold bg-[#F0D99B]/40 px-2.5 py-0.5 rounded-full border border-[#D6A84B]">
                  {path.averageSalaryIncrease}
                </span>
                <span className="text-[#E6DFD1]">•</span>
                <span className="text-[#687187]">
                  Transition Delta:{" "}
                  <strong className={path.transitionDifficulty === "Low" ? "text-[#27856B]" : "text-[#C77B54]"}>
                    {path.transitionDifficulty}
                  </strong>
                </span>
                <span className="text-[#E6DFD1]">•</span>
                <span className="text-[#687187]">
                  Demand: <strong className="text-[#17233F]">{path.demandLevel}</strong>
                </span>
              </div>

              {/* Transferable Skills */}
              <div className="space-y-1.5 p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-xs">
                <span className="text-[10px] font-bold uppercase text-[#27856B] block tracking-wider">
                  Transferable From Your Trade
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {path.transferableSkills.map((sk, i) => (
                    <span
                      key={i}
                      className="text-[11px] px-2.5 py-0.5 rounded-full bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30 font-medium"
                    >
                      {sk}
                    </span>
                  ))}
                </div>
              </div>

              {/* Additional Skills Required */}
              <div className="space-y-1.5 text-xs">
                <span className="text-[10px] font-bold uppercase text-[#C77B54] block tracking-wider">
                  Bridgeable Competencies
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {path.skillsToAcquire.map((sk, i) => (
                    <span
                      key={i}
                      className="text-[11px] px-2.5 py-0.5 rounded-full bg-[#C77B54]/10 text-[#C77B54] border border-[#C77B54]/30 font-medium"
                    >
                      {sk}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-2 border-t border-[#E6DFD1] flex items-center justify-between text-xs font-bold text-[#7355D9]">
                <span>View Transition Bridge Blueprint</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>

        {/* Selected Pathway Deep-Dive Modal / Expansion */}
        {selectedPath && (
          <div className="p-6 sm:p-8 rounded-2xl bg-[#17233F] text-white border border-[#D6A84B]/30 shadow-lg space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <span className="text-xs text-[#D6A84B] font-bold uppercase tracking-wider">
                  Transition Roadmap Blueprint
                </span>
                <h2 className="text-xl font-extrabold text-white mt-1">
                  How to Transition into: {selectedPath.targetRole}
                </h2>
              </div>
              <BrandButton variant="gold" href="/roadmap" size="sm">
                Adopt as Career Goal
              </BrandButton>
            </div>

            <div className="space-y-3 pt-2">
              <h3 className="text-xs font-bold text-[#F0D99B] uppercase tracking-wider">
                3-Step Practical Execution Bridge
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                {selectedPath.bridgeSteps.map((step, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl bg-[#10192D] border border-[#D6A84B]/30 space-y-1.5"
                  >
                    <span className="text-[#D6A84B] font-bold text-sm block">Step {i + 1}</span>
                    <p className="text-[#F5F0E6] leading-relaxed text-xs sm:text-sm">{step}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
