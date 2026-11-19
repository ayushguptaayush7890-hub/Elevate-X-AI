"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { PageHeader } from "@/components/ui/PageHeader";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { mockRoadmapMilestones } from "@/data/mock-data";
import { RoadmapMilestone } from "@/types";
import { toast } from "sonner";
import {
  MapPin,
  CheckCircle2,
  BookOpen,
  RefreshCw,
  Sparkles,
  ArrowRight,
  Compass
} from "lucide-react";

export default function RoadmapPage() {
  const [stages, setStages] = useState<RoadmapMilestone[]>(mockRoadmapMilestones);
  const [targetGoal, setTargetGoal] = useState("Apparel Quality Assurance Specialist (Export Standard)");
  const [isRegenerating, setIsRegenerating] = useState(false);

  const completedStagesCount = stages.filter((s) => s.status === "completed").length;
  const roadmapProgress = Math.round((completedStagesCount / stages.length) * 100);

  const toggleStageStatus = (stageId: string) => {
    setStages((prev) =>
      prev.map((s) => {
        if (s.id === stageId) {
          const nextStatus = s.status === "completed" ? "in_progress" : "completed";
          toast.success(`Stage ${s.stageNumber} marked as ${nextStatus.replace("_", " ")}.`);
          return { ...s, status: nextStatus };
        }
        return s;
      })
    );
  };

  const handleRegenerate = () => {
    setIsRegenerating(true);
    setTimeout(() => {
      setIsRegenerating(false);
      toast.success("Roadmap regenerated and adapted to your latest assessment results!");
    }, 800);
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          badge="Adaptive Vocational Pathways"
          title="Personalized Career Roadmap"
          description={`Target Goal: ${targetGoal}. Track structured vocational milestones, hands-on tasks, and curated free resources calibrated for rapid promotion.`}
          variant="navy"
          actions={
            <button
              onClick={handleRegenerate}
              disabled={isRegenerating}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-[#F0D99B] bg-[#10192D] border border-[#D6A84B]/40 hover:bg-[#17233F] transition-all"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRegenerating ? "animate-spin text-[#D6A84B]" : ""}`} />
              <span>Recalibrate Roadmap</span>
            </button>
          }
        />

        {/* Progress Metric Banner */}
        <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 className="text-sm font-bold text-[#17233F]">Milestone Advancement Index</h3>
              <p className="text-xs text-[#687187]">
                {completedStagesCount} of {stages.length} Stages Completed • Estimated achievement timeline: 4 weeks
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-base font-extrabold text-[#17233F] font-mono px-3 py-1 rounded-xl bg-[#F0D99B] border border-[#D6A84B]">
                {roadmapProgress}% Completed
              </span>
            </div>
          </div>
          <ProgressBar value={roadmapProgress} size="md" color="gold" />
        </div>

        {/* Vertical Interactive Timeline */}
        <div className="space-y-6 relative before:absolute before:inset-0 before:left-7 sm:before:left-8 before:w-0.5 before:bg-[#D6A84B]/40">
          {stages.map((stage) => {
            const isDone = stage.status === "completed";
            const isInProgress = stage.status === "in_progress";

            return (
              <div key={stage.id} className="relative flex items-start gap-4 sm:gap-6 group">
                {/* Timeline Icon Node */}
                <div
                  onClick={() => toggleStageStatus(stage.id)}
                  className={`w-14 sm:w-16 h-14 sm:h-16 rounded-2xl flex items-center justify-center shrink-0 cursor-pointer transition-all z-10 font-bold text-xs select-none ${
                    isDone
                      ? "bg-[#27856B] text-white shadow-lg shadow-[#27856B]/30 ring-4 ring-[#DCEAE6]"
                      : isInProgress
                      ? "bg-[#17233F] text-[#F0D99B] border-2 border-[#D6A84B] shadow-lg shadow-[#17233F]/30 ring-4 ring-[#F0D99B]/30"
                      : "bg-[#FBF8F1] border-2 border-[#E6DFD1] text-[#687187]"
                  }`}
                  title="Click to toggle completion"
                >
                  {isDone ? <CheckCircle2 className="w-6 h-6" /> : `Stage ${stage.stageNumber}`}
                </div>

                {/* Stage Content Card */}
                <div
                  className={`flex-1 p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm hover:shadow-md transition-all space-y-4 ${
                    isInProgress ? "border-[#D6A84B] ring-2 ring-[#D6A84B]/20" : ""
                  }`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-[#F5F0E6] text-[#17233F] border border-[#E6DFD1]">
                          {stage.timeEstimate}
                        </span>
                        <span
                          className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                            isDone
                              ? "bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30"
                              : isInProgress
                              ? "bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]"
                              : "bg-[#FBF8F1] text-[#687187] border border-[#E6DFD1]"
                          }`}
                        >
                          {isDone ? "Completed" : isInProgress ? "Active Milestone" : "Upcoming"}
                        </span>
                      </div>
                      <h3 className="text-base font-bold text-[#17233F] mt-2">{stage.title}</h3>
                    </div>

                    <button
                      onClick={() => toggleStageStatus(stage.id)}
                      className="text-xs font-semibold px-3 py-1.5 rounded-xl border border-[#E6DFD1] bg-[#FBF8F1] hover:bg-[#F5F0E6] text-[#20243A] transition-colors w-fit"
                    >
                      {isDone ? "Mark Incomplete" : "Mark as Finished"}
                    </button>
                  </div>

                  <p className="text-xs sm:text-sm text-[#20243A] leading-relaxed">{stage.description}</p>

                  {/* Skills to Learn */}
                  <div className="space-y-1.5">
                    <span className="text-[10px] uppercase font-bold text-[#687187] tracking-wider">
                      Target Competencies
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {stage.skillsToAcquire.map((sk, i) => (
                        <span
                          key={i}
                          className="text-[11px] px-2.5 py-0.5 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]/30 font-medium"
                        >
                          {sk}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Practical Tasks */}
                  <div className="space-y-1.5">
                    <span className="text-[10px] uppercase font-bold text-[#687187] tracking-wider">
                      Practical Hands-on Tasks
                    </span>
                    <ul className="space-y-1.5 text-xs text-[#20243A]">
                      {stage.practicalTasks.map((task, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-[#D6A84B] font-bold">›</span>
                          <span>{task}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Free Resources */}
                  <div className="pt-3 border-t border-[#E6DFD1] flex flex-wrap items-center gap-3 text-xs">
                    {stage.resources.map((res, i) => (
                      <div
                        key={i}
                        className="flex items-center gap-1.5 text-[#17233F] bg-[#F5F0E6] px-3 py-1.5 rounded-xl border border-[#E6DFD1] font-medium"
                      >
                        <BookOpen className="w-3.5 h-3.5 text-[#7355D9]" />
                        <span>
                          {res.name} ({res.duration})
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AppShell>
  );
}
