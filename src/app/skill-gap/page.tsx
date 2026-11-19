"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { PageHeader } from "@/components/ui/PageHeader";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { mockSkillGaps, mockJobListings } from "@/data/mock-data";
import { toast } from "sonner";
import {
  GitCompare,
  Sparkles,
  BookOpen,
  Download,
  MessageSquare,
  ArrowRight,
  TrendingUp,
  Target,
  CheckCircle2
} from "lucide-react";

export default function SkillGapPage() {
  const [selectedJobId, setSelectedJobId] = useState("job-1");
  const [aiExplanation, setAiExplanation] = useState<string | null>(null);
  const [isExplaining, setIsExplaining] = useState(false);

  const selectedJob = mockJobListings.find((j) => j.id === selectedJobId) || mockJobListings[0];

  const handleExplainGap = () => {
    setIsExplaining(true);
    setTimeout(() => {
      setIsExplaining(false);
      setAiExplanation(
        `For the target role of ${selectedJob.title} at ${selectedJob.company}, your trade craftsmanship is exceptional. The primary competency delta is focused in export standard protocols: specifically AQL 2.5 Sampling Acceptance and Tablet-based ERP Logging. Completing the recommended micro-modules will position your profile in the top tier for interview shortlisting.`
      );
      toast.success("AI Skill Gap Analysis synthesized.");
    }, 600);
  };

  const handleDownloadReport = () => {
    window.print();
    toast.success("Skill Gap Diagnostic summary generated.");
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          badge="Delta Diagnostic Engine"
          title="Skill Gap & Competency Analyzer"
          description="Understand what you know and discover what you need. Compare your verified capabilities against specific employer requirements to prioritize high-value micro-learning."
          variant="navy"
          actions={
            <button
              onClick={handleDownloadReport}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-[#F0D99B] bg-[#10192D] border border-[#D6A84B]/40 hover:bg-[#17233F] transition-all"
            >
              <Download className="w-3.5 h-3.5" /> Export Diagnostic
            </button>
          }
        />

        {/* Target Job Selector */}
        <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold text-[#17233F]">Target Role Benchmark:</span>
            <select
              value={selectedJobId}
              onChange={(e) => {
                setSelectedJobId(e.target.value);
                setAiExplanation(null);
              }}
              className="bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3.5 py-2 text-xs sm:text-sm text-[#20243A] font-semibold focus:outline-none focus:border-[#D6A84B]"
            >
              {mockJobListings.map((j) => (
                <option key={j.id} value={j.id}>
                  {j.title} ({j.company})
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-[#687187]">Benchmark Fit:</span>
            <span className="text-xs font-extrabold text-[#17233F] px-3.5 py-1 rounded-full bg-[#F0D99B] border border-[#D6A84B] shadow-sm">
              {selectedJob.matchScore}% Compatibility
            </span>
          </div>
        </div>

        {/* Visual Competency Delta Comparison Cards */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-[#17233F] uppercase tracking-wider">
              Competency Gap Breakdown ({mockSkillGaps.length} Target Areas)
            </h2>
            <span className="text-xs text-[#687187]">Ranked by impact on compensation</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mockSkillGaps.map((gap) => (
              <div
                key={gap.id}
                className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm hover:border-[#D6A84B]/60 hover:shadow-md transition-all space-y-4"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-[#17233F]">{gap.skillName}</h3>
                    <span className="text-xs text-[#687187]">{gap.category}</span>
                  </div>
                  <span
                    className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                      gap.importance === "High"
                        ? "bg-[#C77B54]/15 text-[#C77B54] border border-[#C77B54]/30"
                        : "bg-[#F0D99B]/40 text-[#17233F] border border-[#D6A84B]/40"
                    }`}
                  >
                    {gap.importance} Priority Gap
                  </span>
                </div>

                {/* Delta Comparison Bar */}
                <div className="space-y-2 p-4 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-xs">
                  <div className="flex justify-between text-xs">
                    <span className="text-[#687187]">Current Evaluated Level:</span>
                    <span className="font-semibold text-[#17233F]">{gap.currentLevel}</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-[#687187]">Employer Specification:</span>
                    <span className="font-bold text-[#7355D9]">{gap.requiredLevel}</span>
                  </div>
                  <div className="pt-1.5">
                    <ProgressBar value={gap.gapScore} size="sm" color="gold" />
                  </div>
                </div>

                <p className="text-xs text-[#20243A] leading-relaxed">
                  {gap.learningRecommendation}
                </p>

                {/* Resource Recommendation */}
                <div className="pt-3 border-t border-[#E6DFD1] flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1.5 text-[#17233F] font-semibold">
                    <BookOpen className="w-3.5 h-3.5 text-[#7355D9]" />
                    <span className="truncate max-w-[210px]">{gap.recommendedResource.title}</span>
                  </div>
                  <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30 font-bold">
                    Curated ({gap.recommendedResource.duration})
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Assistant Explanation Panel */}
        <div className="p-6 sm:p-8 rounded-2xl bg-[#17233F] text-white border border-[#D6A84B]/30 shadow-lg space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-[#10192D] text-[#D6A84B] border border-[#D6A84B]/30">
                <Sparkles className="w-5 h-5 text-[#D6A84B]" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Synthesize Actionable Transition Advice</h3>
                <p className="text-xs text-[#F0D99B]">Get plain-language strategic guidance on bridging these exact skill targets</p>
              </div>
            </div>

            <BrandButton
              variant="gold"
              size="sm"
              onClick={handleExplainGap}
              disabled={isExplaining}
            >
              <MessageSquare className="w-3.5 h-3.5 mr-1.5" />
              <span>{isExplaining ? "Synthesizing Insights..." : "Generate AI Strategy"}</span>
            </BrandButton>
          </div>

          {aiExplanation && (
            <div className="p-5 rounded-xl bg-[#10192D] border border-[#D6A84B]/40 text-xs sm:text-sm text-[#F5F0E6] leading-relaxed animate-in fade-in duration-200 space-y-3">
              <p className="whitespace-pre-line">{aiExplanation}</p>
              <div className="flex justify-end pt-2">
                <BrandButton variant="violet" href="/roadmap" size="sm">
                  <span>Add to My Career Roadmap</span>
                  <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                </BrandButton>
              </div>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
