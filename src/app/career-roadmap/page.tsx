"use client";

import React, { useState, useEffect, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { RoadmapMilestone, CareerRoadmapData, RoadmapTaskItem } from "@/types";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import {
  CheckCircle2,
  Circle,
  BookOpen,
  RefreshCw,
  Sparkles,
  ExternalLink,
  Target,
  Clock,
  Layers,
  ChevronDown,
  Printer,
  ShieldCheck,
  Lock,
  AlertCircle
} from "lucide-react";

const STANDARD_GOAL_PRESETS = [
  "AI Engineer",
  "Data Scientist",
  "Backend Developer",
  "Software Developer",
  "Apparel Quality Assurance Specialist (Export Standard)"
];

/**
 * Sanitizes milestone descriptions, removing redundant prompt echoes or raw markdown bullet prefixes.
 */
function cleanMarkdownDescription(raw: string): string {
  if (!raw) return "";
  let text = raw.trim();
  // Strip leading bullet prefixes like "- ", "* ", "• " applied to the whole block
  text = text.replace(/^(?:[-*•]\s+)+/, "");
  // Strip echoes like "- **Why this milestone is vital for [Role]:**" or "**Technical Summary:**"
  text = text.replace(/^(?:\*\*)?(?:Technical Summary|Why this milestone is vital(?: for [^:*]+)?)(?:\*\*)?[:*]*\s*/i, "");
  text = text.replace(/^(?:[-*•]\s+)+/, "");
  return text.trim();
}

/**
 * Derives a reliable, non-null, non-undefined stage number.
 */
function getStageNumber(stage: RoadmapMilestone, index: number): number {
  const val = stage.stageNumber ?? stage.stage_number ?? stage.order_index;
  if (typeof val === "number" && !isNaN(val) && val > 0) return val;
  return index + 1;
}

export default function CareerRoadmapPage() {
  const [roadmap, setRoadmap] = useState<CareerRoadmapData | null>(null);
  const [stages, setStages] = useState<RoadmapMilestone[]>([]);
  const [targetGoal, setTargetGoal] = useState<string>("AI Engineer");
  const [customGoalInput, setCustomGoalInput] = useState<string>("");
  const [isCustomInputOpen, setIsCustomInputOpen] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isRegenerating, setIsRegenerating] = useState<boolean>(false);
  const [updatingTaskId, setUpdatingTaskId] = useState<string | null>(null);

  // Load active roadmap on mount
  const loadRoadmap = useCallback(async (preferredGoal?: string) => {
    setIsLoading(true);
    try {
      const res = await apiService.getCurrentRoadmap();
      if (res && res.data && res.data.milestones && res.data.milestones.length > 0) {
        setRoadmap(res.data);
        setStages(res.data.milestones);
        setTargetGoal(res.data.target_role || "AI Engineer");
      } else {
        // Generate initial roadmap
        const initialGoal = preferredGoal || "AI Engineer";
        const genRes = await apiService.generateRoadmap(initialGoal);
        if (genRes && genRes.data) {
          setRoadmap(genRes.data);
          setStages(genRes.data.milestones);
          setTargetGoal(genRes.data.target_role || initialGoal);
        }
      }
    } catch (err: any) {
      console.warn("Could not fetch remote roadmap, generating fallback:", err);
      try {
        const genRes = await apiService.generateRoadmap(preferredGoal || "AI Engineer");
        if (genRes && genRes.data) {
          setRoadmap(genRes.data);
          setStages(genRes.data.milestones);
          setTargetGoal(genRes.data.target_role || "AI Engineer");
        }
      } catch (genErr) {
        toast.error("Failed to load or initialize career roadmap.");
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadRoadmap();
  }, [loadRoadmap]);

  // Handle changing target career goal
  const handleSelectGoal = async (newGoal: string) => {
    if (newGoal.toLowerCase() === targetGoal.toLowerCase() && !isRegenerating) return;
    setIsRegenerating(true);
    try {
      const res = await apiService.updateCareerGoal(newGoal);
      if (res && res.data) {
        setRoadmap(res.data);
        setStages(res.data.milestones || []);
        setTargetGoal(res.data.target_role);
        toast.success(`Target career goal updated to ${res.data.target_role}. Milestones recalibrated!`);
      }
    } catch (err: any) {
      toast.error(err?.message || "Failed to update career goal. Please select from standard benchmarks.");
    } finally {
      setIsRegenerating(false);
      setIsCustomInputOpen(false);
    }
  };

  // Recalibrate current roadmap
  const handleRecalibrate = async () => {
    setIsRegenerating(true);
    try {
      const res = await apiService.recalibrateRoadmap(targetGoal);
      if (res && res.data) {
        setRoadmap(res.data);
        setStages(res.data.milestones || []);
        toast.success("Roadmap recalibrated with latest assessment criteria & ML models!");
      }
    } catch (err: any) {
      toast.error(err?.message || "Failed to recalibrate roadmap.");
    } finally {
      setIsRegenerating(false);
    }
  };

  // Toggle stage completion adhering strictly to required practical tasks
  const handleToggleStage = async (stage: RoadmapMilestone, index: number) => {
    const stageNum = getStageNumber(stage, index);
    const stageTasks = stage.tasks || [];
    const incompleteTasks = stageTasks.filter((t) => !t.is_completed);

    if (!stage.is_completed && incompleteTasks.length > 0) {
      toast.error(
        `Cannot complete Stage ${stageNum}: ${incompleteTasks.length} required practical task(s) remain incomplete. Complete all tasks first.`
      );
      return;
    }

    try {
      const res = await apiService.toggleMilestone(stage.id);
      if (res && res.data) {
        setRoadmap(res.data);
        setStages(res.data.milestones || []);
        const updated = res.data.milestones?.find((m) => m.id === stage.id);
        const isNowCompleted = updated?.is_completed;
        toast.success(
          isNowCompleted
            ? `Stage ${stageNum} marked Completed!`
            : `Stage ${stageNum} marked Incomplete.`
        );
      }
    } catch (err: any) {
      toast.error(err?.message || "Failed to update milestone status.");
    }
  };

  // Toggle individual task completion
  const handleToggleTask = async (taskId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (updatingTaskId) return;
    setUpdatingTaskId(taskId);
    try {
      const res = await apiService.toggleTask(taskId);
      if (res && res.data) {
        setRoadmap(res.data);
        setStages(res.data.milestones || []);
      }
    } catch (err: any) {
      toast.error(err?.message || "Failed to update task state.");
    } finally {
      setUpdatingTaskId(null);
    }
  };

  const completedStagesCount = stages.filter((s) => s.status === "completed" || s.is_completed).length;
  const roadmapProgress = roadmap?.progress_percentage ?? Math.round((completedStagesCount / Math.max(1, stages.length)) * 100);

  return (
    <AppShell>
      <div className="space-y-6 max-w-5xl mx-auto pb-12">
        {/* Top Header */}
        <PageHeader
          badge="Adaptive Vocational & Technical Pathways"
          title="Personalized Career Roadmap"
          description={`Target Goal: ${targetGoal}. Dynamically calibrated learning milestones, rigorous hands-on tasks, and verified public resources powered by AI.`}
          variant="navy"
          actions={
            <div className="flex items-center gap-2">
              <button
                onClick={() => window.print()}
                className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold text-[#17233F] bg-white border border-[#E6DFD1] hover:bg-[#F5F0E6] transition-all"
                title="Print or Export Roadmap"
              >
                <Printer className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Export</span>
              </button>
              <button
                onClick={handleRecalibrate}
                disabled={isRegenerating || isLoading}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-[#F0D99B] bg-[#10192D] border border-[#D6A84B]/40 hover:bg-[#17233F] transition-all disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isRegenerating ? "animate-spin text-[#D6A84B]" : ""}`} />
                <span>{isRegenerating ? "Recalibrating..." : "Recalibrate Roadmap"}</span>
              </button>
            </div>
          }
        />

        {/* Goal Selector Card */}
        <div className="p-4 sm:p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-lg bg-[#F5F0E6] text-[#D6A84B]">
                <Target className="w-4 h-4 text-[#17233F]" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-[#17233F] uppercase tracking-wider">
                  Target Career Occupation
                </h3>
                <p className="text-sm font-semibold text-[#20243A]">
                  {targetGoal}
                </p>
              </div>
            </div>

            <button
              onClick={() => setIsCustomInputOpen(!isCustomInputOpen)}
              className="text-xs font-semibold text-[#7355D9] hover:text-[#5B3FB8] flex items-center gap-1 self-start sm:self-auto"
            >
              <span>{isCustomInputOpen ? "Close Custom Role" : "Custom Occupation"}</span>
              <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isCustomInputOpen ? "rotate-180" : ""}`} />
            </button>
          </div>

          {/* Quick Presets */}
          <div className="flex flex-wrap gap-2 pt-2 border-t border-[#E6DFD1]">
            {STANDARD_GOAL_PRESETS.map((preset) => {
              const isActive = targetGoal.toLowerCase() === preset.toLowerCase();
              return (
                <button
                  key={preset}
                  onClick={() => handleSelectGoal(preset)}
                  disabled={isRegenerating}
                  className={`text-xs px-3 py-1.5 rounded-xl font-medium transition-all ${
                    isActive
                      ? "bg-[#17233F] text-[#F0D99B] border border-[#D6A84B] shadow-sm"
                      : "bg-[#FBF8F1] text-[#20243A] border border-[#E6DFD1] hover:bg-[#F5F0E6]"
                  }`}
                >
                  {preset}
                </button>
              );
            })}
          </div>

          {/* Custom Occupation Input Drawer */}
          {isCustomInputOpen && (
            <div className="pt-3 flex gap-2">
              <input
                type="text"
                placeholder="Enter custom occupation title (e.g. Robotics Engineer, Solar PV Installer)..."
                value={customGoalInput}
                onChange={(e) => setCustomGoalInput(e.target.value)}
                className="flex-1 px-3 py-2 text-xs rounded-xl border border-[#E6DFD1] bg-[#FBF8F1] focus:outline-none focus:border-[#D6A84B]"
              />
              <button
                onClick={() => {
                  if (customGoalInput.trim()) {
                    handleSelectGoal(customGoalInput.trim());
                    setCustomGoalInput("");
                  }
                }}
                disabled={!customGoalInput.trim() || isRegenerating}
                className="px-4 py-2 text-xs font-semibold bg-[#17233F] text-[#F0D99B] rounded-xl hover:bg-[#20243A] disabled:opacity-50"
              >
                Set Goal
              </button>
            </div>
          )}
        </div>

        {/* Progress Metric Banner */}
        <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-[#17233F]">Milestone Advancement Index</h3>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-[#DCEAE6] text-[#27856B]">
                  Live Synchronized
                </span>
              </div>
              <p className="text-xs text-[#687187] mt-1">
                {completedStagesCount} of {stages.length} Stages Completed
                {roadmap?.total_tasks ? ` • ${roadmap.completed_tasks} of ${roadmap.total_tasks} Hands-on Tasks Finished` : ""}
                {roadmap?.estimated_duration_weeks ? ` • ${roadmap.estimated_duration_weeks} Weeks Estimated Pathway` : ""}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-base font-extrabold text-[#17233F] font-mono px-3.5 py-1.5 rounded-xl bg-[#F0D99B] border border-[#D6A84B]">
                {roadmapProgress}% Completed
              </span>
            </div>
          </div>
          <ProgressBar value={roadmapProgress} size="md" color="gold" />
        </div>

        {/* Loading Skeleton */}
        {isLoading && (
          <div className="space-y-4 animate-pulse">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-44 rounded-2xl bg-[#F5F0E6]/50 border border-[#E6DFD1]" />
            ))}
          </div>
        )}

        {/* Vertical Interactive Timeline */}
        {!isLoading && (
          <div className="space-y-6 relative before:absolute before:inset-0 before:left-7 sm:before:left-8 before:w-0.5 before:bg-[#D6A84B]/40">
            {stages.map((stage, idx) => {
              const stageNum = getStageNumber(stage, idx);
              const isDone = stage.status === "completed" || stage.is_completed;
              const isBlocked = stage.status === "blocked";
              const isInProgress = stage.status === "in_progress" || (!isDone && !isBlocked && idx === 0);
              const stageTasks = stage.tasks || [];
              const completedTasksCount = stageTasks.filter((t) => t.is_completed).length;
              const allTasksCompleted = stageTasks.length > 0 ? completedTasksCount === stageTasks.length : isDone;
              const cleanedDesc = cleanMarkdownDescription(stage.description);
              const timeEst = stage.timeEstimate || stage.time_estimate || "3-4 Weeks";
              const competencies = stage.skillsToAcquire || stage.skills_to_acquire || [];

              return (
                <div key={stage.id || `stage-${stageNum}`} className="relative flex items-start gap-4 sm:gap-6 group">
                  {/* Timeline Icon Node */}
                  <div
                    onClick={() => handleToggleStage(stage, idx)}
                    className={`w-14 sm:w-16 h-14 sm:h-16 rounded-2xl flex items-center justify-center shrink-0 cursor-pointer transition-all z-10 font-bold text-xs select-none ${
                      isDone
                        ? "bg-[#27856B] text-white shadow-lg shadow-[#27856B]/30 ring-4 ring-[#DCEAE6]"
                        : isInProgress
                        ? "bg-[#17233F] text-[#F0D99B] border-2 border-[#D6A84B] shadow-lg shadow-[#17233F]/30 ring-4 ring-[#F0D99B]/30"
                        : isBlocked
                        ? "bg-[#FBF8F1] border-2 border-[#E6DFD1] text-[#9EA7B8] hover:border-[#D6A84B]/60"
                        : "bg-[#FBF8F1] border-2 border-[#E6DFD1] text-[#687187]"
                    }`}
                    title={
                      isDone
                        ? "Stage completed. Click to mark incomplete."
                        : isBlocked
                        ? `Prerequisite Stage ${stageNum - 1} incomplete.`
                        : "Active milestone. Click to verify completion."
                    }
                  >
                    {isDone ? (
                      <CheckCircle2 className="w-6 h-6" />
                    ) : isBlocked ? (
                      <div className="flex flex-col items-center justify-center">
                        <Lock className="w-4 h-4 mb-0.5 text-[#9EA7B8]" />
                        <span className="text-[10px]">Stage {stageNum}</span>
                      </div>
                    ) : (
                      `Stage ${stageNum}`
                    )}
                  </div>

                  {/* Stage Content Card */}
                  <div
                    className={`flex-1 p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm hover:shadow-md transition-all space-y-4 ${
                      isInProgress ? "border-[#D6A84B] ring-2 ring-[#D6A84B]/20" : ""
                    }`}
                  >
                    {/* Header */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-[#F5F0E6] text-[#17233F] border border-[#E6DFD1] flex items-center gap-1">
                            <Clock className="w-3 h-3 text-[#D6A84B]" />
                            {timeEst}
                          </span>
                          <span
                            className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full flex items-center gap-1 ${
                              isDone
                                ? "bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30"
                                : isInProgress
                                ? "bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]"
                                : isBlocked
                                ? "bg-[#F5F0E6] text-[#687187] border border-[#E6DFD1]"
                                : "bg-[#FBF8F1] text-[#687187] border border-[#E6DFD1]"
                            }`}
                          >
                            {isBlocked && <Lock className="w-2.5 h-2.5" />}
                            {isDone
                              ? "Completed"
                              : isInProgress
                              ? "Active Milestone"
                              : isBlocked
                              ? `Blocked (Prereq Stage ${stageNum - 1})`
                              : "Upcoming"}
                          </span>
                        </div>
                        <h3 className="text-base font-bold text-[#17233F] mt-2">
                          Stage {stageNum}: {stage.title}
                        </h3>
                      </div>

                      {/* Stage Completion Action Button */}
                      <button
                        onClick={() => handleToggleStage(stage, idx)}
                        className={`text-xs font-semibold px-3 py-1.5 rounded-xl border transition-colors w-fit flex items-center gap-1.5 ${
                          isDone
                            ? "border-[#27856B]/40 bg-[#DCEAE6]/40 text-[#27856B] hover:bg-[#DCEAE6]"
                            : stageTasks.length > 0 && !allTasksCompleted
                            ? "border-[#E6DFD1] bg-[#FBF8F1] text-[#687187] hover:bg-[#F5F0E6]"
                            : "border-[#D6A84B] bg-[#17233F] text-[#F0D99B] hover:bg-[#20243A]"
                        }`}
                        title={
                          stageTasks.length > 0 && !allTasksCompleted
                            ? `Finish all tasks (${completedTasksCount}/${stageTasks.length}) before marking complete.`
                            : "Toggle stage completion."
                        }
                      >
                        {isDone ? (
                          <>
                            <CheckCircle2 className="w-3.5 h-3.5 text-[#27856B]" />
                            <span>Mark Stage Incomplete</span>
                          </>
                        ) : stageTasks.length > 0 && !allTasksCompleted ? (
                          <>
                            <AlertCircle className="w-3.5 h-3.5 text-[#D6A84B]" />
                            <span>Tasks Pending ({completedTasksCount}/{stageTasks.length})</span>
                          </>
                        ) : (
                          <>
                            <CheckCircle2 className="w-3.5 h-3.5 text-[#F0D99B]" />
                            <span>Mark Stage Finished</span>
                          </>
                        )}
                      </button>
                    </div>

                    {/* AI-Personalized Narrative Rendered with Clean Markdown */}
                    <div className="prose prose-sm max-w-none text-xs sm:text-sm text-[#20243A] leading-relaxed">
                      <ReactMarkdown
                        components={{
                          p: ({ children }) => <p className="mb-2 last:mb-0 text-[#20243A] leading-relaxed">{children}</p>,
                          strong: ({ children }) => <strong className="font-bold text-[#17233F]">{children}</strong>,
                          ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-1 text-[#20243A]">{children}</ul>,
                          ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-1 text-[#20243A]">{children}</ol>,
                          li: ({ children }) => <li className="text-[#20243A]">{children}</li>,
                        }}
                      >
                        {cleanedDesc}
                      </ReactMarkdown>
                    </div>

                    {/* Target Competencies */}
                    {competencies.length > 0 && (
                      <div className="space-y-1.5 pt-1">
                        <span className="text-[10px] uppercase font-bold text-[#687187] tracking-wider flex items-center gap-1">
                          <Layers className="w-3 h-3 text-[#D6A84B]" />
                          Target Competencies
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {competencies.map((sk, i) => {
                            const evidence = (stage as any).competencyEvidence?.[sk] || (stage as any).competency_evidence?.[sk];
                            const isResume = evidence === "mentioned_in_resume";
                            const isVerified = evidence === "assessment_verified";
                            const isDemonstrated = evidence === "practically_demonstrated";
                            return (
                              <span
                                key={i}
                                className="inline-flex items-center gap-1.5 text-[11px] px-2.5 py-0.5 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]/30 font-medium"
                              >
                                <span>{sk}</span>
                                {isVerified && (
                                  <span className="text-[9px] bg-[#27856B] text-white px-1.5 rounded font-bold">
                                    Verified
                                  </span>
                                )}
                                {isDemonstrated && (
                                  <span className="text-[9px] bg-[#27856B]/40 text-emerald-200 px-1.5 rounded">
                                    Demonstrated
                                  </span>
                                )}
                                {isResume && (
                                  <span className="text-[9px] bg-[#D6A84B]/20 text-[#D6A84B] px-1.5 rounded">
                                    Resume
                                  </span>
                                )}
                              </span>
                            );
                          })}
                        </div>
                      </div>
                    )}

                    {/* Practical Hands-on Tasks with Interactive Checkboxes */}
                    <div className="space-y-2 pt-1">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-bold text-[#687187] tracking-wider flex items-center gap-1">
                          <Sparkles className="w-3 h-3 text-[#D6A84B]" />
                          Practical Hands-on Deliverables
                        </span>
                        {stageTasks.length > 0 && (
                          <span className="text-[10px] font-mono text-[#687187]">
                            {completedTasksCount} / {stageTasks.length} Completed
                          </span>
                        )}
                      </div>

                      <div className="space-y-2">
                        {stageTasks.length > 0 ? (
                          stageTasks.map((task) => (
                            <div
                              key={task.id}
                              onClick={(e) => handleToggleTask(task.id, e)}
                              className={`flex items-start gap-2.5 p-2.5 rounded-xl border transition-all cursor-pointer text-xs ${
                                task.is_completed
                                  ? "bg-[#DCEAE6]/40 border-[#27856B]/30 text-[#17233F]"
                                  : "bg-[#FBF8F1] border-[#E6DFD1] hover:bg-[#F5F0E6] text-[#20243A]"
                              }`}
                            >
                              <button
                                type="button"
                                className="mt-0.5 shrink-0 text-[#27856B]"
                                disabled={updatingTaskId === task.id}
                              >
                                {task.is_completed ? (
                                  <CheckCircle2 className="w-4 h-4 text-[#27856B]" />
                                ) : (
                                  <Circle className="w-4 h-4 text-[#687187]" />
                                )}
                              </button>
                              <div className="flex-1">
                                <span className={task.is_completed ? "line-through text-[#687187]" : "font-medium"}>
                                  {task.title}
                                </span>
                              </div>
                              <span className="text-[10px] text-[#687187] font-mono shrink-0">
                                {task.estimated_hours || 4.0}h
                              </span>
                            </div>
                          ))
                        ) : (
                          <ul className="space-y-1.5 text-xs text-[#20243A]">
                            {(stage.practicalTasks || stage.practical_tasks || []).map((task, i) => (
                              <li key={i} className="flex items-start gap-2">
                                <span className="text-[#D6A84B] font-bold">›</span>
                                <span>{task}</span>
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
                    </div>

                    {/* Curated Verified Free Resources */}
                    {stage.resources && stage.resources.length > 0 && (
                      <div className="pt-3 border-t border-[#E6DFD1] space-y-2">
                        <div className="flex items-center gap-1 text-[10px] uppercase font-bold text-[#687187] tracking-wider">
                          <ShieldCheck className="w-3.5 h-3.5 text-[#27856B]" />
                          <span>Verified Public Learning Resources & Standards</span>
                        </div>
                        <div className="flex flex-wrap gap-2.5">
                          {stage.resources.map((res, i) => (
                            <a
                              key={i}
                              href={res.url || "#"}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center gap-2 text-[#17233F] bg-[#F5F0E6] hover:bg-[#EBDDC5] px-3 py-1.5 rounded-xl border border-[#E6DFD1] font-medium text-xs transition-colors group/link"
                            >
                              <BookOpen className="w-3.5 h-3.5 text-[#7355D9] shrink-0" />
                              <span className="line-clamp-1 max-w-[280px]">
                                {res.name || res.title}
                              </span>
                              <ExternalLink className="w-3 h-3 text-[#687187] group-hover/link:text-[#17233F] shrink-0" />
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </AppShell>
  );
}
