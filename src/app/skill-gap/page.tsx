"use client";

import React, { useState, useEffect } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import {
  GitCompare,
  Sparkles,
  BookOpen,
  Download,
  ArrowRight,
  TrendingUp,
  Target,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  ExternalLink,
  RefreshCw,
  Upload,
  Cpu,
  Layers,
  ShieldCheck,
  Calendar,
  Check,
  Award,
} from "lucide-react";

import {
  deduplicateSkills,
  normalizeSkillKey,
  createSkillId,
  generateCandidateSkillId,
  deduplicateCandidateSkills,
  CANONICAL_SKILL_SYNONYMS,
} from "@/utils/skill-normalization";

export interface CandidateSkill {
  id: string;
  name: string;
  source: "resume_extracted" | "profile_verified" | "user_added";
  sourceId?: string;
  canonicalSkillId?: string;
  confidence?: number;
  evidence?: string;
}

const TARGET_ROLE_OPTIONS = [
  { id: "ai_ml", title: "AI / Machine Learning Engineer", source: "esco", desc: "European ESCO standard profile for AI and ML systems engineering." },
  { id: "swe", title: "Software Engineer", source: "esco", desc: "ESCO full-stack and systems engineering profile." },
  { id: "ds", title: "Data Scientist", source: "esco", desc: "ESCO statistical modeling, predictive analytics and ML." },
  { id: "devops", title: "DevOps Engineer", source: "esco", desc: "ESCO CI/CD automation, containerization and cloud infrastructure." },
  { id: "cloud", title: "Cloud Solutions Architect", source: "esco", desc: "ESCO enterprise distributed systems and cloud governance." },
  { id: "sec", title: "Cybersecurity Analyst", source: "esco", desc: "ESCO threat detection, security hardening and compliance." },
  { id: "backend", title: "Backend Developer", source: "esco", desc: "ESCO microservices, API architecture and database persistence." },
  { id: "frontend", title: "Frontend Developer", source: "esco", desc: "ESCO responsive UI, modern JS frameworks and state management." },
];

export default function SkillGapPage() {
  const [candidateSkills, setCandidateSkills] = useState<CandidateSkill[]>([]);
  const [newSkillInput, setNewSkillInput] = useState("");
  const [selectedRoleTitle, setSelectedRoleTitle] = useState("AI / Machine Learning Engineer");
  const [selectedRoleSource, setSelectedRoleSource] = useState("esco");
  const [activeFilter, setActiveFilter] = useState<"all" | "gaps" | "partial" | "verified">("all");
  
  // Loading & Data States
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [uploadLoading, setUploadLoading] = useState(false);

  // Initialize candidate skills from authentic session/profile (Zero fake fallback skills)
  useEffect(() => {
    try {
      const savedUserStr = localStorage.getItem("elevate_user_profile");
      if (savedUserStr) {
        const savedUser = JSON.parse(savedUserStr);
        // Only load skills if genuine user skills exist and are not demo placeholders
        if (Array.isArray(savedUser.skills) && savedUser.skills.length > 0) {
          const rawAuthentic: CandidateSkill[] = savedUser.skills
            .filter((s: any) => !s.isDemoData && s.name)
            .map((s: any) => ({
              id: s.id || generateCandidateSkillId(s.name, s.source || "profile_verified"),
              name: s.name,
              source: (s.source || "profile_verified") as "profile_verified" | "resume_extracted" | "user_added",
              sourceId: s.sourceId || s.spanId || (s.id && !s.id.startsWith("cand-") ? s.id : undefined),
              canonicalSkillId: s.canonicalSkillId,
              confidence: s.confidence,
              evidence: s.evidenceText || s.evidence,
            }));
          const authenticSkills: CandidateSkill[] = deduplicateCandidateSkills(rawAuthentic);
          if (authenticSkills.length > 0) {
            setCandidateSkills(authenticSkills);
            runSkillGapAnalysis(authenticSkills, selectedRoleTitle);
            return;
          }
        }
      }
    } catch {
      // Fallback safely to empty state
    }
    // New accounts start with zero candidate skills
    setCandidateSkills([]);
  }, []);

  const runSkillGapAnalysis = async (skillsToAnalyze: CandidateSkill[] = candidateSkills, roleTitle: string = selectedRoleTitle) => {
    if (skillsToAnalyze.length === 0) {
      setAnalysisResult(null);
      setIsAnalyzing(false);
      return;
    }

    setIsAnalyzing(true);
    setAnalysisError(null);
    try {
      const rawNames = skillsToAnalyze.map((s) => s.name);
      const deduplicated = deduplicateSkills(rawNames);
      const result = await apiService.analyzeSkillGap({
        candidateSkills: deduplicated,
        targetOccupationTitle: roleTitle,
        targetOccupationSource: selectedRoleSource,
        includeAiStrategy: true,
      });
      setAnalysisResult(result);
      setAnalysisError(null);
      toast.success(`Skill Gap Diagnostic complete: ${result.overallMatchScore}% match against authentic benchmark.`);
    } catch (err: any) {
      const msg = err.message || "Failed to compute skill gap analysis.";
      setAnalysisError(msg);
      toast.error(msg);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRoleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const title = e.target.value;
    setSelectedRoleTitle(title);
    if (candidateSkills.length > 0) {
      runSkillGapAnalysis(candidateSkills, title);
    }
  };

  const handleAddSkill = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = newSkillInput.trim();
    if (!trimmed) return;

    const candidateKey = normalizeSkillKey(trimmed);
    const alreadyExists = candidateSkills.some((s) => normalizeSkillKey(s.name) === candidateKey);
    if (alreadyExists) {
      toast.warning(`'${trimmed}' is already present in your skills inventory.`);
      setNewSkillInput("");
      return;
    }

    const preferredLabel = CANONICAL_SKILL_SYNONYMS[trimmed.toLowerCase()] || trimmed;
    const newSkillItem: CandidateSkill = {
      id: generateCandidateSkillId(preferredLabel, "user_added"),
      name: preferredLabel,
      source: "user_added",
    };
    const updated = deduplicateCandidateSkills([...candidateSkills, newSkillItem]);
    setCandidateSkills(updated);
    setNewSkillInput("");
    toast.success(`Added '${preferredLabel}' (manually entered).`);
    runSkillGapAnalysis(updated, selectedRoleTitle);
  };

  const handleRemoveSkill = (skillId: string) => {
    const updated = candidateSkills.filter((s) => s.id !== skillId);
    setCandidateSkills(updated);
    toast.info("Skill removed from inventory.");
    if (updated.length > 0) {
      runSkillGapAnalysis(updated, selectedRoleTitle);
    } else {
      setAnalysisResult(null);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploadLoading(true);
    try {
      toast.info(`Parsing ${file.name} to extract candidate skills...`);
      const parsed = await apiService.uploadResumeFile(file);
      const extracted: string[] = parsed.skills || [];
      if (extracted.length > 0) {
        const mappedItems: CandidateSkill[] = extracted.map((name) => ({
          id: generateCandidateSkillId(name, "resume_extracted"),
          name: name,
          source: "resume_extracted" as const,
          evidence: `Extracted from resume document: ${file.name}`,
        }));
        const updated = deduplicateCandidateSkills([...candidateSkills, ...mappedItems]);
        setCandidateSkills(updated);
        toast.success(`Extracted ${mappedItems.length} skills from ${file.name} (${updated.length} total in inventory)`);
        runSkillGapAnalysis(updated, selectedRoleTitle);
      } else {
        toast.warning("No skills could be extracted from this document. Please add your skills manually.");
      }
    } catch (err: any) {
      toast.error(err.message || "Failed to parse resume document. Please try again or add skills manually.");
    } finally {
      setUploadLoading(false);
    }
  };

  const handleDownloadReport = () => {
    window.print();
    toast.success("Skill Gap Diagnostic summary printed / exported.");
  };

  // Filter competencies based on active tab
  const filteredCompetencies = (analysisResult?.competencies || []).filter((comp: any) => {
    if (activeFilter === "gaps") return comp.status === "skill_gap";
    if (activeFilter === "partial") return comp.status === "partially_supported";
    if (activeFilter === "verified") return comp.status === "verified_match";
    return true;
  });

  return (
    <AppShell>
      <div className="space-y-6 max-w-7xl mx-auto pb-12">
        {/* Page Header */}
        <PageHeader
          badge="Delta Diagnostic Engine • BGE Dense Vectors"
          title="Skill Gap & Competency Analyzer"
          description="Identify exact competency deltas against official ESCO v1.1.1 and O*NET 31.0 benchmarks. Computes cosine similarities with BGE-Small (384-dim) and synthesizes personalized roadmaps with local Qwen2.5 LLM."
          variant="navy"
          actions={
            <div className="flex items-center gap-2">
              <button
                onClick={() => runSkillGapAnalysis()}
                disabled={isAnalyzing}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-200 bg-white/10 hover:bg-white/20 transition-all border border-white/10 disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isAnalyzing ? "animate-spin" : ""}`} /> Re-Analyze
              </button>
              <button
                onClick={handleDownloadReport}
                className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-[#F0D99B] bg-[#10192D] border border-[#D6A84B]/40 hover:bg-[#17233F] transition-all shadow-sm"
              >
                <Download className="w-3.5 h-3.5" /> Export Diagnostic
              </button>
            </div>
          }
        />

        {/* Section 1: Candidate Skills Inventory Bar */}
        <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-[#7355D9]" />
              <h2 className="text-xs font-bold text-[#17233F] uppercase tracking-wider">
                CANDIDATE SKILLS INVENTORY ({candidateSkills.length} SKILLS)
              </h2>
            </div>
            
            <div className="flex items-center gap-2">
              <label className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold text-[#17233F] bg-[#FBF8F1] border border-[#E6DFD1] hover:bg-white cursor-pointer transition-all">
                <Upload className="w-3.5 h-3.5 text-[#D6A84B]" />
                <span>{uploadLoading ? "Parsing..." : "Upload Resume (PDF/DOCX)"}</span>
                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileUpload}
                  disabled={uploadLoading}
                  className="hidden"
                />
              </label>
            </div>
          </div>

          {/* Interactive Skills Pill Bag with Source Badges OR Transparent Empty State */}
          {candidateSkills.length === 0 ? (
            <div className="p-6 rounded-xl bg-[#FBF8F1] border border-dashed border-[#D6A84B]/60 text-center space-y-3">
              <div className="w-10 h-10 rounded-xl bg-white border border-[#E6DFD1] flex items-center justify-center mx-auto text-[#7355D9] shadow-2xs">
                <Layers className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <h3 className="text-xs font-bold text-[#17233F]">No Candidate Skills Present</h3>
                <p className="text-xs text-[#687187] max-w-md mx-auto leading-relaxed">
                  No skills found yet. Upload your resume or add skills manually to begin your skill-gap analysis.
                </p>
              </div>
              <div className="flex flex-wrap items-center justify-center gap-3 pt-1">
                <label className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-[#17233F] bg-white border border-[#D6A84B] hover:bg-[#FFFDF8] cursor-pointer transition-all shadow-2xs">
                  <Upload className="w-3.5 h-3.5 text-[#D6A84B]" />
                  <span>{uploadLoading ? "Parsing..." : "Upload Resume (PDF/DOCX)"}</span>
                  <input
                    type="file"
                    accept=".pdf,.docx"
                    onChange={handleFileUpload}
                    disabled={uploadLoading}
                    className="hidden"
                  />
                </label>
                <button
                  type="button"
                  onClick={() => {
                    const inputEl = document.getElementById("manual-skill-input");
                    if (inputEl) inputEl.focus();
                  }}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-[#F0D99B] bg-[#17233F] hover:bg-[#20243A] transition-all"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Add Skills Manually</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="flex flex-wrap gap-1.5 max-h-36 overflow-y-auto p-3 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1]/60">
              {candidateSkills.map((skill) => {
                const sourceBadge = 
                  skill.source === "resume_extracted" 
                    ? { text: "Resume", cls: "bg-blue-100 text-blue-800 border-blue-200" }
                    : skill.source === "user_added"
                    ? { text: "Manual", cls: "bg-amber-100 text-amber-800 border-amber-200" }
                    : { text: "Profile", cls: "bg-purple-100 text-purple-800 border-purple-200" };

                const pillKey = `cand-pill-${skill.source}-${skill.id}`;

                return (
                  <span
                    key={pillKey}
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white border border-[#E6DFD1] text-[#17233F] shadow-2xs group"
                  >
                    <span>{skill.name}</span>
                    <span className={`text-[9px] px-1 py-0.2 rounded border font-medium ${sourceBadge.cls}`}>
                      {sourceBadge.text}
                    </span>
                    <button
                      type="button"
                      onClick={() => handleRemoveSkill(skill.id)}
                      className="text-slate-400 hover:text-rose-600 transition-colors ml-0.5"
                      title={`Remove ${skill.name}`}
                    >
                      &times;
                    </button>
                  </span>
                );
              })}
            </div>
          )}

          {/* Add skill input */}
          <form onSubmit={handleAddSkill} className="flex gap-2 pt-1">
            <input
              id="manual-skill-input"
              type="text"
              value={newSkillInput}
              onChange={(e) => setNewSkillInput(e.target.value)}
              placeholder="Add skill manually (e.g. Kubernetes, GraphQL, OpenCV, Python)..."
              className="flex-1 bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3.5 py-1.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
            />
            <button
              type="submit"
              className="px-4 py-1.5 text-xs font-bold rounded-xl bg-[#17233F] text-[#F0D99B] hover:bg-[#20243A] transition-all"
            >
              Add Skill
            </button>
          </form>
        </div>

        {/* Section 2: Target Role Selector Header */}
        <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-1 w-full md:w-auto flex-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-[#17233F] uppercase tracking-wider">Target Occupation Benchmark:</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#D6A84B]/15 text-[#17233F] border border-[#D6A84B]/40">
                {analysisResult?.sourceTaxonomy || "ESCO v1.1.1"}
              </span>
              {isAnalyzing && analysisResult && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#D6A84B]/20 text-[#17233F] border border-[#D6A84B]/40 animate-pulse">
                  <RefreshCw className="w-2.5 h-2.5 animate-spin text-[#7355D9]" /> Re-analyzing...
                </span>
              )}
            </div>
            <select
              value={selectedRoleTitle}
              onChange={handleRoleChange}
              className="w-full md:max-w-md bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-sm text-[#20243A] font-bold focus:outline-none focus:border-[#D6A84B] shadow-2xs"
            >
              {TARGET_ROLE_OPTIONS.map((r) => (
                <option key={r.id} value={r.title}>
                  {r.title} ({r.source.toUpperCase()})
                </option>
              ))}
            </select>
            <p className="text-xs text-[#687187]">
              {TARGET_ROLE_OPTIONS.find((r) => r.title === selectedRoleTitle)?.desc || "Official occupational competency profile."}
            </p>
          </div>

          {/* Compatibility Score Display (Only shown when results exist, preserved during re-analysis) */}
          {analysisResult && (
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 w-full md:w-auto justify-end border-t md:border-t-0 md:border-l border-[#E6DFD1] pt-4 md:pt-0 md:pl-6">
              <div className="text-left sm:text-right">
                <span className="text-xs text-[#687187] block font-semibold">Competency Coverage Score</span>
                <span className="text-3xl font-black text-[#17233F]">
                  {analysisResult.overallMatchScore}%
                </span>
                <span className="text-[10px] text-slate-400 block max-w-xs sm:ml-auto">
                  {analysisResult.coverageScoreExplanation || "Weighted coverage of authentic ESCO occupational requirements."}
                </span>
              </div>
              <div className="w-20">
                <ProgressBar
                  value={analysisResult.overallMatchScore}
                  size="md"
                  color={
                    analysisResult.overallMatchScore >= 70
                      ? "emerald"
                      : analysisResult.overallMatchScore >= 50
                      ? "gold"
                      : "navy"
                  }
                />
              </div>
            </div>
          )}
        </div>

        {/* Loading State: Initial Analysis in progress without prior results */}
        {isAnalyzing && !analysisResult && (
          <div className="p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm text-center space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-[#D6A84B]/15 text-[#17233F] border border-[#D6A84B]/40 flex items-center justify-center mx-auto">
              <RefreshCw className="w-6 h-6 animate-spin text-[#7355D9]" />
            </div>
            <div className="space-y-1">
              <h3 className="text-base font-bold text-[#17233F]">Running Deep Semantic Gap Diagnostic...</h3>
              <p className="text-xs text-[#687187] max-w-lg mx-auto">
                Comparing {candidateSkills.length} candidate skills against official {selectedRoleTitle} competencies using BGE-Small dense embeddings and local Qwen2.5 LLM.
              </p>
            </div>
            {/* Skeleton Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="p-4 rounded-2xl bg-slate-50 border border-slate-200 h-24 animate-pulse" />
              ))}
            </div>
          </div>
        )}

        {/* Error State: Analysis Failed without prior results */}
        {analysisError && !analysisResult && (
          <div className="p-6 rounded-2xl bg-rose-50 border border-rose-200 shadow-sm text-center space-y-3">
            <AlertTriangle className="w-8 h-8 text-rose-600 mx-auto" />
            <h3 className="text-sm font-bold text-rose-900">Analysis Request Failed</h3>
            <p className="text-xs text-rose-700 max-w-md mx-auto">{analysisError}</p>
            <button
              onClick={() => runSkillGapAnalysis()}
              className="px-4 py-2 rounded-xl text-xs font-bold bg-rose-700 text-white hover:bg-rose-800 transition-all shadow-sm"
            >
              Retry Analysis
            </button>
          </div>
        )}

        {/* Results Sections: Only rendered when authentic results exist */}
        {analysisResult && (
          <>
            {/* Section 3: Diagnostic Stat Badges */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-4 rounded-2xl bg-white border border-[#E6DFD1] shadow-2xs text-center space-y-1">
                <span className="text-[11px] font-bold text-[#687187] uppercase">Total Required</span>
                <div className="text-2xl font-black text-[#17233F]">
                  {analysisResult.totalCompetenciesRequired}
                </div>
                <span className="text-[10px] text-slate-400">Authentic Requirements</span>
              </div>

              <div className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-200/80 shadow-2xs text-center space-y-1">
                <span className="text-[11px] font-bold text-emerald-800 uppercase">Verified Matches</span>
                <div className="text-2xl font-black text-emerald-700">
                  {analysisResult.verifiedSkillsCount}
                </div>
                <span className="text-[10px] text-emerald-600 font-semibold">Direct Canonical Match</span>
              </div>

              <div className="p-4 rounded-2xl bg-amber-50/60 border border-amber-200/80 shadow-2xs text-center space-y-1">
                <span className="text-[11px] font-bold text-amber-800 uppercase">Partially Supported</span>
                <div className="text-2xl font-black text-amber-700">
                  {analysisResult.partialSkillsCount}
                </div>
                <span className="text-[10px] text-amber-600 font-semibold">Related Taxonomy Subfield</span>
              </div>

              <div className="p-4 rounded-2xl bg-rose-50/60 border border-rose-200/80 shadow-2xs text-center space-y-1">
                <span className="text-[11px] font-bold text-rose-800 uppercase">Critical Gaps</span>
                <div className="text-2xl font-black text-rose-700">
                  {analysisResult.gapSkillsCount}
                </div>
                <span className="text-[10px] text-rose-600 font-semibold">Unmatched Competencies</span>
              </div>
            </div>

            {/* Section 4: Competency Gap Breakdown Cards */}
            <div className="space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <Target className="w-4 h-4 text-[#7355D9]" />
                  <h2 className="text-sm font-bold text-[#17233F] uppercase tracking-wider">
                    Competency Delta Breakdown ({filteredCompetencies.length} Areas)
                  </h2>
                </div>

                {/* Filter Tabs */}
                <div className="flex items-center gap-1.5 p-1 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1]">
                  <button
                    onClick={() => setActiveFilter("all")}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                      activeFilter === "all" ? "bg-[#17233F] text-[#F0D99B]" : "text-[#687187] hover:text-[#17233F]"
                    }`}
                  >
                    All ({analysisResult.competencies?.length ?? 0})
                  </button>
                  <button
                    onClick={() => setActiveFilter("gaps")}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                      activeFilter === "gaps" ? "bg-rose-700 text-white" : "text-rose-700 hover:bg-rose-100/50"
                    }`}
                  >
                    Gaps ({analysisResult.gapSkillsCount})
                  </button>
                  <button
                    onClick={() => setActiveFilter("partial")}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                      activeFilter === "partial" ? "bg-amber-600 text-white" : "text-amber-700 hover:bg-amber-100/50"
                    }`}
                  >
                    Partial ({analysisResult.partialSkillsCount})
                  </button>
                  <button
                    onClick={() => setActiveFilter("verified")}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                      activeFilter === "verified" ? "bg-emerald-700 text-white" : "text-emerald-700 hover:bg-emerald-100/50"
                    }`}
                  >
                    Verified ({analysisResult.verifiedSkillsCount})
                  </button>
                </div>
              </div>

              {/* Cards Grid with Stable Unique Keys */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredCompetencies.map((comp: any, idx: number) => {
                  const isMatch = comp.status === "verified_match";
                  const isPartial = comp.status === "partially_supported";
                  const isGap = comp.status === "skill_gap";
                  const compCardKey = `card-${createSkillId(comp.skillName)}-${idx}`;

                  return (
                    <div
                      key={compCardKey}
                      className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-2xs hover:border-[#D6A84B]/60 hover:shadow-md transition-all space-y-3"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <div className="flex items-center gap-2">
                            {isMatch && <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />}
                            {isPartial && <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />}
                            {isGap && <XCircle className="w-4 h-4 text-rose-600 shrink-0" />}
                            <h3 className="text-sm font-bold text-[#17233F]">{comp.skillName}</h3>
                          </div>
                          <span className="text-[11px] text-[#687187] block pl-6">
                            {comp.category} • Canonical: {comp.canonicalName}
                          </span>
                        </div>

                        <div className="flex flex-col items-end gap-1">
                          <span
                            className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full ${
                              isMatch
                                ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                                : isPartial
                                ? "bg-amber-100 text-amber-800 border border-amber-300"
                                : "bg-rose-100 text-rose-800 border border-rose-300"
                            }`}
                          >
                            {isMatch ? "Verified Match" : isPartial ? "Partially Supported" : "Skill Gap"}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono">
                            BGE Sim: {(comp.similarityScore * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>

                      {/* Level & Evidence Comparison */}
                      <div className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1]/80 text-xs space-y-1.5">
                        <div className="flex justify-between">
                          <span className="text-[#687187]">Proficiency Assessment Status:</span>
                          <span className="font-semibold text-slate-600">
                            {comp.candidateLevel || "Not Assessed"}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-[#687187]">Target Requirement:</span>
                          <span className="font-semibold text-[#17233F]">
                            {comp.expectedLevel} ({comp.importance}) • {comp.competencySource || "ESCO"}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-[#687187]">Lexical Canonical Match:</span>
                          <span className="font-mono text-[11px] text-slate-600">
                            {comp.lexicalMatch ? "Yes (Canonical Match)" : "No"}
                          </span>
                        </div>
                        <div className="pt-1 text-[11px] text-slate-500 italic border-t border-[#E6DFD1]/60">
                          Evidence: {comp.evidence}
                        </div>
                      </div>

                      {/* Learning Resource recommendation */}
                      {comp.recommendedResources && comp.recommendedResources.length > 0 && (
                        <div className="pt-2 border-t border-[#E6DFD1] space-y-1.5">
                          <span className="text-[10px] font-bold text-[#687187] uppercase tracking-wider block">
                            Verified Official Learning Resource:
                          </span>
                          {comp.recommendedResources.map((res: any, rIdx: number) => (
                            <a
                              key={`res-${createSkillId(comp.skillName)}-${res.id || rIdx}`}
                              href={res.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center justify-between p-2 rounded-lg bg-slate-50 hover:bg-[#F0D99B]/20 border border-slate-200 hover:border-[#D6A84B] transition-all text-xs group"
                            >
                              <div className="flex items-center gap-2 truncate pr-2">
                                <BookOpen className="w-3.5 h-3.5 text-[#7355D9] shrink-0" />
                                <span className="font-semibold text-[#17233F] truncate">{res.title}</span>
                              </div>
                              <div className="flex items-center gap-1.5 shrink-0">
                                <span className="text-[10px] px-2 py-0.5 rounded bg-white text-slate-600 border border-slate-200">
                                  {res.provider}
                                </span>
                                <ExternalLink className="w-3 h-3 text-slate-400 group-hover:text-[#17233F]" />
                              </div>
                            </a>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Section 5: AI Learning Roadmap & Personalized Strategy (Qwen2.5-1.5B) */}
            {analysisResult.aiStrategy && (
              <div className="p-6 sm:p-8 rounded-2xl bg-[#17233F] text-white border border-[#D6A84B]/30 shadow-lg space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-[#10192D] text-[#D6A84B] border border-[#D6A84B]/30">
                      <Sparkles className="w-5 h-5" />
                    </div>
                    <div>
                      <h2 className="text-base font-bold text-white tracking-wide">
                        Personalized AI Career Strategy & 4-Week Roadmap
                      </h2>
                      <p className="text-xs text-slate-300">
                        Synthesized by local Qwen2.5-1.5B (Apple Silicon Metal) strictly grounded in verified competency gaps.
                      </p>
                    </div>
                  </div>
                  <div className="flex flex-col items-start sm:items-end gap-1.5">
                    <span className="text-xs font-bold text-[#F0D99B] bg-[#10192D] px-3.5 py-1.5 rounded-full border border-[#D6A84B]/40">
                      Target: {analysisResult.targetOccupation}
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">
                      Engine: {analysisResult.aiStrategy.generatedByModel} • {analysisResult.aiStrategy.validatedUrlsCount} Official Resources Validated
                    </span>
                  </div>
                </div>

                {analysisResult.aiStrategy.error && (
                  <div className="p-3 rounded-xl bg-amber-900/30 border border-amber-500/40 text-xs text-amber-200">
                    <span className="font-bold">Model Notice:</span> {analysisResult.aiStrategy.error}
                  </div>
                )}

                {/* Executive Synthesis */}
                <div className="p-4 rounded-xl bg-[#10192D]/70 border border-white/10 text-xs sm:text-sm text-slate-200 leading-relaxed">
                  <span className="font-bold text-[#F0D99B] block mb-1">Executive Diagnostic:</span>
                  {analysisResult.aiStrategy.executiveSummary}
                </div>

                {/* 4-Week Structured Milestones */}
                <div className="space-y-3">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-[#D6A84B]">
                    Curated 4-Week Sprint Curriculum
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                    {analysisResult.aiStrategy.weeklyMilestones.map((m: any) => (
                      <div
                        key={`milestone-week-${m.week}`}
                        className="p-4 rounded-xl bg-[#10192D] border border-white/10 space-y-2 flex flex-col justify-between"
                      >
                        <div className="space-y-1.5">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-[#D6A84B]/20 text-[#D6A84B] border border-[#D6A84B]/40">
                              Week {m.week}
                            </span>
                            <Calendar className="w-3.5 h-3.5 text-slate-400" />
                          </div>
                          <h4 className="text-xs font-bold text-white">{m.title}</h4>
                          <ul className="text-[11px] text-slate-300 space-y-1 pt-1 list-disc pl-3">
                            {m.actionItems.map((act: string, i: number) => (
                              <li key={`act-${m.week}-${i}`}>{act}</li>
                            ))}
                          </ul>
                        </div>
                        {m.suggestedResourceUrl && (
                          <a
                            href={m.suggestedResourceUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#F0D99B] hover:underline pt-2"
                          >
                            <span>Official Docs</span>
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Recommended Projects & Assessment */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                  <div className="p-4 rounded-xl bg-[#10192D] border border-white/10 space-y-2">
                    <h4 className="text-xs font-bold uppercase text-[#D6A84B] flex items-center gap-1.5">
                      <Cpu className="w-3.5 h-3.5" /> Practical Portfolio Capstones
                    </h4>
                    <ul className="text-xs text-slate-300 space-y-1.5 list-disc pl-4">
                      {analysisResult.aiStrategy.practicalProjects.map((p: string, i: number) => (
                        <li key={`project-${i}`}>{p}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-4 rounded-xl bg-[#10192D] border border-white/10 space-y-2">
                    <h4 className="text-xs font-bold uppercase text-[#D6A84B] flex items-center gap-1.5">
                      <Award className="w-3.5 h-3.5" /> Platform Assessment Milestones
                    </h4>
                    <ul className="text-xs text-slate-300 space-y-1.5 list-disc pl-4">
                      {analysisResult.aiStrategy.assessmentMilestones.map((a: string, i: number) => (
                        <li key={`assessment-${i}`}>{a}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Governance Disclaimer */}
                <div className="flex items-center gap-2 text-[10px] text-slate-400 pt-2 border-t border-white/10">
                  <ShieldCheck className="w-4 h-4 text-[#D6A84B] shrink-0" />
                  <span>{analysisResult.aiStrategy.groundingDisclaimer}</span>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </AppShell>
  );
}
