"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/layout/AppShell";
import { GlassCard } from "@/components/ui/GlassCard";
import { BrandButton } from "@/components/ui/BrandButton";
import { GoldBadge } from "@/components/ui/GoldBadge";
import { PageHeader } from "@/components/ui/PageHeader";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { useAuth } from "@/context/AuthContext";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import {
  Award,
  Play,
  CheckCircle2,
  XCircle,
  Clock,
  HelpCircle,
  ArrowRight,
  ArrowLeft,
  RotateCcw,
  Sparkles,
  AlertTriangle,
  BookOpen,
  ShieldCheck,
  Target,
  Code,
  Database,
  Terminal,
  Cpu,
  Layers,
  ChevronRight,
  History,
  TrendingUp,
  ExternalLink,
  Zap,
  Lock,
  UserCheck,
  LogIn,
} from "lucide-react";

interface RoleSummary {
  role_id: string;
  title: string;
  category: string;
  description: string;
  skill_count: number;
}

interface RoleDetail {
  role_id: string;
  title: string;
  category: string;
  description: string;
  skills: Array<{ skill_id: string; name: string; subtopics: string[] }>;
}

export default function AssessmentPage() {
  const router = useRouter();
  const { user, isAuthenticated } = useAuth();

  // Navigation & View State
  const [viewState, setViewState] = useState<"catalog" | "in_progress" | "result" | "history">("catalog");
  const [loading, setLoading] = useState(false);
  const [hasToken, setHasToken] = useState<boolean>(false);

  // Catalog State
  const [roles, setRoles] = useState<RoleSummary[]>([]);
  const [selectedRole, setSelectedRole] = useState<RoleDetail | null>(null);
  const [selectedSkillId, setSelectedSkillId] = useState<string>("");
  const [selectedType, setSelectedType] = useState<string>("");
  const [difficultyMode, setDifficultyMode] = useState<string>("adaptive");
  const [questionCount, setQuestionCount] = useState<number>(10);

  // Active Assessment State
  const [sessionId, setSessionId] = useState<string>("");
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [timeLeftSeconds, setTimeLeftSeconds] = useState<number>(1200);

  // Sandbox State
  const [sandboxOutput, setSandboxOutput] = useState<{ [qid: string]: any }>({});
  const [runningSandbox, setRunningSandbox] = useState(false);

  // Results State
  const [activeResult, setActiveResult] = useState<any>(null);
  const [historyList, setHistoryList] = useState<any[]>([]);

  // Check token existence in localStorage
  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("elevate_auth_token") : null;
    setHasToken(Boolean(token));
  }, [isAuthenticated]);

  // 1. Load initial roles list
  useEffect(() => {
    loadRoles();
  }, []);

  const loadRoles = async () => {
    setLoading(true);
    try {
      const res = await apiService.getTechnicalRoles();
      if (res.data && res.data.length > 0) {
        setRoles(res.data);
        // Automatically select the first role
        loadRoleDetails(res.data[0].role_id);
      }
    } catch (err: any) {
      toast.error("Failed to load technical roles: " + (err.message || "Network error"));
    } finally {
      setLoading(false);
    }
  };

  const loadRoleDetails = async (roleId: string) => {
    try {
      const res = await apiService.getTechnicalRoleDetails(roleId);
      if (res.data) {
        setSelectedRole(res.data);
        setSelectedSkillId(""); // Reset skill filter
      }
    } catch (err: any) {
      toast.error("Failed to load role details");
    }
  };

  // Timer loop for active assessment
  useEffect(() => {
    if (viewState !== "in_progress") return;
    const interval = setInterval(() => {
      setTimeLeftSeconds((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          handleSubmitAssessment();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [viewState]);

  // 2. Start Assessment
  const handleStartAssessment = async () => {
    if (!selectedRole) return;

    // Check token authentication before initiating network request
    const token = typeof window !== "undefined" ? localStorage.getItem("elevate_auth_token") : null;
    if (!token) {
      toast.error("Authentication required. Please sign in to start your technical assessment.");
      router.push("/login?from=/assessment");
      return;
    }

    setLoading(true);
    try {
      const res = await apiService.startTechnicalAssessment({
        role_id: selectedRole.role_id,
        skill_id: selectedSkillId || undefined,
        assessment_type: selectedType || undefined,
        difficulty: difficultyMode,
        question_count: questionCount,
      });

      if (res.data && res.data.questions && res.data.questions.length > 0) {
        setSessionId(res.data.session_id);
        setQuestions(res.data.questions);
        setCurrentIndex(0);
        setAnswers({});
        setSandboxOutput({});
        setTimeLeftSeconds(res.data.duration_minutes * 60);
        setViewState("in_progress");
        toast.success(`Assessment started: ${res.data.total_questions} questions loaded`);
      } else {
        toast.error("No questions available matching your filters");
      }
    } catch (err: any) {
      if (err.message?.includes("401") || err.message?.includes("Unauthorized")) {
        toast.error("Your session has expired. Please sign in again.");
        router.push("/login?from=/assessment");
      } else {
        toast.error(err.message || "Failed to start assessment");
      }
    } finally {
      setLoading(false);
    }
  };

  // 3. Interactive Sandbox Execution
  const handleRunCode = async (code: string, qid: string) => {
    setRunningSandbox(true);
    try {
      const currentQ = questions[currentIndex];
      const res = await apiService.runCodeSandbox({
        question_id: qid,
        language: currentQ.coding_language || "python",
        code: code,
        visible_test_cases: currentQ.visible_test_cases || [],
      });
      setSandboxOutput((prev) => ({ ...prev, [qid]: res.data }));
      if (res.data.passed) {
        toast.success(`All visible tests passed (${res.data.passed_tests}/${res.data.total_tests})!`);
      } else {
        toast.error(res.data.error || "Some tests failed");
      }
    } catch (err: any) {
      toast.error("Sandbox error: " + err.message);
    } finally {
      setRunningSandbox(false);
    }
  };

  const handleRunSQL = async (query: string, qid: string) => {
    setRunningSandbox(true);
    try {
      const currentQ = questions[currentIndex];
      const res = await apiService.runSQLSandbox({
        question_id: qid,
        candidate_query: query,
        schema_sql: currentQ.SQL_schema,
        sample_db_sql: currentQ.sample_database,
      });
      setSandboxOutput((prev) => ({ ...prev, [qid]: res.data }));
      if (res.data.passed) {
        toast.success("Query executed successfully!");
      } else {
        toast.error(res.data.error || "Query result mismatch");
      }
    } catch (err: any) {
      toast.error("SQL error: " + err.message);
    } finally {
      setRunningSandbox(false);
    }
  };

  // 4. Submit Assessment
  const handleSubmitAssessment = async () => {
    if (!selectedRole || !sessionId) return;
    setLoading(true);
    try {
      const payloadAnswers = questions.map((q) => ({
        question_id: q.question_id,
        answer: answers[q.question_id] || "",
        language: q.coding_language || "python",
        time_taken_seconds: 60,
      }));

      const res = await apiService.submitTechnicalAssessment({
        session_id: sessionId,
        role_id: selectedRole.role_id,
        answers: payloadAnswers,
      });

      if (res.data) {
        setActiveResult(res.data);
        setViewState("result");
        toast.success(`Assessment submitted! Score: ${res.data.overall_score_percentage}%`);
      }
    } catch (err: any) {
      toast.error("Failed to submit assessment: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // 5. Load History
  const handleLoadHistory = async () => {
    const token = typeof window !== "undefined" ? localStorage.getItem("elevate_auth_token") : null;
    if (!token) {
      toast.error("Please sign in to view past assessment attempts.");
      router.push("/login?from=/assessment");
      return;
    }

    setLoading(true);
    try {
      const res = await apiService.getTechnicalAssessmentHistory();
      setHistoryList(res.data || []);
      setViewState("history");
    } catch (err: any) {
      toast.error("Failed to load history: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const currentQ = questions[currentIndex];

  return (
    <AppShell>
      <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Navigation & Header with Authentication Status */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#E6DFD1] pb-6">
          <div>
            <PageHeader
              title="Technical Assessment & Career Intelligence"
              description="Evaluate production-grade IT competencies across 9 technical roles with secure sandboxes, adaptive evaluation, and custom roadmaps."
            />
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            {/* Auth Status Pill */}
            {hasToken ? (
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#27856B]/10 border border-[#27856B]/30 text-xs font-bold text-[#1e6b56]">
                <UserCheck className="w-3.5 h-3.5 text-[#27856B]" />
                <span>Verified Candidate</span>
              </div>
            ) : (
              <Link
                href="/login?from=/assessment"
                className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#D6A84B]/15 border border-[#D6A84B] text-xs font-bold text-[#92400E] hover:bg-[#D6A84B]/25 transition-all"
              >
                <LogIn className="w-3.5 h-3.5 text-[#D6A84B]" />
                <span>Sign In to Save Results</span>
              </Link>
            )}

            {viewState !== "catalog" && (
              <BrandButton
                variant="navy"
                size="sm"
                onClick={() => setViewState("catalog")}
                className="gap-2 text-xs font-bold"
              >
                <Layers className="w-4 h-4" /> Role Explorer
              </BrandButton>
            )}
            <BrandButton
              variant="navy"
              size="sm"
              onClick={handleLoadHistory}
              className="gap-2 text-xs font-bold"
            >
              <History className="w-4 h-4" /> Past Attempts
            </BrandButton>
          </div>
        </div>

        {/* ------------------------------------------------------------- */}
        {/* VIEW 1: CATALOG & ROLE EXPLORER */}
        {/* ------------------------------------------------------------- */}
        {viewState === "catalog" && (
          <div className="space-y-8">
            {/* Role Cards Grid */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-black text-[#17233F] tracking-tight flex items-center gap-2">
                  <Target className="w-5 h-5 text-[#D6A84B]" />
                  Select Target Technical Career Role
                </h2>
                <span className="text-xs font-bold text-[#4B5563]">9 Professional Tracks</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {roles.map((r) => {
                  const isSelected = selectedRole?.role_id === r.role_id;
                  return (
                    <GlassCard
                      key={r.role_id}
                      onClick={() => loadRoleDetails(r.role_id)}
                      className={`cursor-pointer transition-all p-5 bg-white border-2 hover:border-[#D6A84B] shadow-sm ${
                        isSelected
                          ? "border-[#D6A84B] ring-2 ring-[#D6A84B]/25 bg-[#FFFDF9]"
                          : "border-[#E6DFD1] hover:shadow-md"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-[#17233F]/5 text-[#17233F] border border-[#17233F]/10">
                            {r.category}
                          </span>
                          <h3 className="text-base font-black text-[#17233F] mt-2.5">{r.title}</h3>
                          <p className="text-xs text-[#374151] line-clamp-2 mt-1 leading-relaxed">
                            {r.description}
                          </p>
                        </div>
                        <GoldBadge size="sm">{r.skill_count} Skills</GoldBadge>
                      </div>
                    </GlassCard>
                  );
                })}
              </div>
            </div>

            {/* Selected Role Skill Breakdown & Configuration */}
            {selectedRole && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left 2 Cols: Role Skills Explorer */}
                <div className="lg:col-span-2 space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-black text-[#17233F] flex items-center gap-2">
                      <BookOpen className="w-5 h-5 text-[#D6A84B]" />
                      Required Competencies for {selectedRole.title}
                    </h3>
                    <span className="text-xs font-semibold text-[#4B5563]">
                      Click any skill to filter questions
                    </span>
                  </div>

                  <div className="space-y-3">
                    {selectedRole.skills.map((skill, sIdx) => {
                      const isSkillSelected = selectedSkillId === skill.skill_id;
                      return (
                        <GlassCard
                          key={`${skill.skill_id}-${sIdx}`}
                          onClick={() =>
                            setSelectedSkillId(isSkillSelected ? "" : skill.skill_id)
                          }
                          className={`p-5 cursor-pointer transition-all border-2 bg-white shadow-xs ${
                            isSkillSelected
                              ? "border-[#D6A84B] bg-[#FFFDF9] ring-1 ring-[#D6A84B]/40"
                              : "border-[#E6DFD1] hover:border-[#D6A84B]/60"
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <span className="w-8 h-8 rounded-full bg-[#17233F] flex items-center justify-center text-xs font-bold text-[#F0D99B] shrink-0">
                                {sIdx + 1}
                              </span>
                              <div>
                                <h4 className="font-bold text-[#17233F] text-sm">{skill.name}</h4>
                                <p className="text-xs text-[#4B5563] mt-0.5">
                                  {skill.subtopics.length} key competencies defined
                                </p>
                              </div>
                            </div>
                            <span
                              className={`text-xs font-bold px-3 py-1 rounded-full border transition-all ${
                                isSkillSelected
                                  ? "bg-[#D6A84B] text-[#17233F] border-[#D6A84B]"
                                  : "bg-[#F5F0E6] text-[#7355D9] border-[#E6DFD1]"
                              }`}
                            >
                              {isSkillSelected ? "Selected for Drill ✓" : "Click to Filter"}
                            </span>
                          </div>

                          <div className="mt-3.5 flex flex-wrap gap-2 pl-11">
                            {skill.subtopics.map((sub, i) => (
                              <span
                                key={i}
                                className="text-xs bg-[#FBF8F1] border border-[#E6DFD1] text-[#17233F] font-semibold px-2.5 py-1 rounded-md shadow-2xs"
                              >
                                {sub}
                              </span>
                            ))}
                          </div>
                        </GlassCard>
                      );
                    })}
                  </div>
                </div>

                {/* Right Col: Assessment Configuration Card */}
                <div className="space-y-4">
                  <h3 className="text-lg font-black text-[#17233F] flex items-center gap-2">
                    <Zap className="w-5 h-5 text-[#D6A84B]" />
                    Assessment Setup
                  </h3>

                  <GlassCard className="p-6 space-y-5 bg-white border-2 border-[#E6DFD1] shadow-md">
                    {/* Assessment Type Filter */}
                    <div className="space-y-1.5">
                      <label className="text-xs font-black text-[#17233F] block uppercase tracking-wider">
                        Assessment Type
                      </label>
                      <select
                        value={selectedType}
                        onChange={(e) => setSelectedType(e.target.value)}
                        className="w-full bg-[#FBF8F1] border-2 border-[#E6DFD1] rounded-xl px-3.5 py-2.5 text-sm text-[#17233F] font-bold focus:outline-none focus:border-[#D6A84B] transition-all"
                      >
                        <option value="">All Types (Comprehensive Diagnostic)</option>
                        <option value="mcq">Multiple Choice (MCQ)</option>
                        <option value="coding">Coding Challenges (Python / JS)</option>
                        <option value="debugging">Code Debugging Challenges</option>
                        <option value="scenario">Production Incident Scenarios</option>
                        <option value="sql">SQL Data Challenges</option>
                        <option value="system_design">System Design Architecture</option>
                      </select>
                    </div>

                    {/* Difficulty Mode */}
                    <div className="space-y-1.5">
                      <label className="text-xs font-black text-[#17233F] block uppercase tracking-wider">
                        Difficulty Engine
                      </label>
                      <div className="grid grid-cols-2 gap-2">
                        {[
                          { id: "adaptive", label: "Adaptive (IRT)" },
                          { id: "easy", label: "Easy" },
                          { id: "medium", label: "Medium" },
                          { id: "hard", label: "Hard" },
                        ].map((d) => (
                          <button
                            key={d.id}
                            type="button"
                            onClick={() => setDifficultyMode(d.id)}
                            className={`py-2 px-3 text-xs font-bold rounded-xl border-2 transition-all cursor-pointer ${
                              difficultyMode === d.id
                                ? "bg-[#17233F] border-[#17233F] text-[#F0D99B] shadow-sm"
                                : "border-[#E6DFD1] bg-[#FBF8F1] text-[#374151] hover:border-[#D6A84B]"
                            }`}
                          >
                            {d.label}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Question Count */}
                    <div className="space-y-1.5">
                      <label className="text-xs font-black text-[#17233F] block uppercase tracking-wider">
                        Question Volume
                      </label>
                      <div className="flex gap-2">
                        {[5, 10, 15, 20].map((count) => (
                          <button
                            key={count}
                            type="button"
                            onClick={() => setQuestionCount(count)}
                            className={`flex-1 py-2 text-xs font-bold rounded-xl border-2 transition-all cursor-pointer ${
                              questionCount === count
                                ? "bg-[#17233F] border-[#17233F] text-[#F0D99B] shadow-sm"
                                : "border-[#E6DFD1] bg-[#FBF8F1] text-[#374151] hover:border-[#D6A84B]"
                            }`}
                          >
                            {count} Qs
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Authentication Status Banner on Setup Card */}
                    {!hasToken && (
                      <div className="p-3.5 rounded-xl bg-[#FFFDF0] border border-[#D6A84B] space-y-2">
                        <div className="flex items-center gap-2 text-xs font-bold text-[#92400E]">
                          <Lock className="w-4 h-4 text-[#D6A84B] shrink-0" />
                          <span>Candidate Authentication Required</span>
                        </div>
                        <p className="text-[11px] text-[#78350F] leading-relaxed">
                          Assessments are scored server-side and recorded to your candidate profile. Please sign in to activate the assessment runner.
                        </p>
                        <Link
                          href="/login?from=/assessment"
                          className="btn-violet block text-center py-2 rounded-lg text-xs font-bold shadow-xs hover:scale-[1.01] transition-all"
                        >
                          Sign In with Verified Account →
                        </Link>
                      </div>
                    )}

                    {/* Start Assessment CTA */}
                    <div className="pt-2">
                      <BrandButton
                        variant="gold"
                        onClick={handleStartAssessment}
                        disabled={loading}
                        className="w-full gap-2 py-3.5 justify-center text-sm font-black shadow-md cursor-pointer hover:scale-[1.01] transition-all"
                      >
                        <Play className="w-4 h-4 fill-current" />
                        {loading
                          ? "Loading Assessment Dataset..."
                          : `Start ${selectedRole.title} Assessment`}
                      </BrandButton>
                    </div>

                    <div className="text-center pt-1">
                      <p className="text-[11px] text-[#4B5563] font-medium leading-relaxed">
                        Server-side IRT ability estimation & isolated sandbox evaluation.
                      </p>
                    </div>
                  </GlassCard>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* VIEW 2: ACTIVE ASSESSMENT RUNNER */}
        {/* ------------------------------------------------------------- */}
        {viewState === "in_progress" && currentQ && (
          <div className="space-y-6">
            {/* Runner Control Header */}
            <GlassCard className="p-5 bg-white border-2 border-[#E6DFD1] shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="flex items-center gap-3 flex-wrap">
                <span className="px-3 py-1 rounded-full bg-[#17233F] text-[#F0D99B] text-xs font-bold uppercase tracking-wider">
                  {currentQ.assessment_type.replace("_", " ")}
                </span>
                <span className="text-sm font-black text-[#17233F]">
                  Question {currentIndex + 1} of {questions.length}
                </span>
                <span className="text-xs text-[#4B5563] font-semibold">
                  ({currentQ.skill_name} • {currentQ.difficulty.toUpperCase()})
                </span>
              </div>

              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-[#17233F] font-mono text-sm font-bold bg-[#F5F0E6] px-3.5 py-1.5 rounded-xl border border-[#D6A84B]">
                  <Clock className="w-4 h-4 text-[#D6A84B] animate-pulse" />
                  <span>
                    {Math.floor(timeLeftSeconds / 60)}:
                    {(timeLeftSeconds % 60).toString().padStart(2, "0")}
                  </span>
                </div>
                <BrandButton
                  variant="violet"
                  size="sm"
                  onClick={handleSubmitAssessment}
                  className="text-xs font-bold"
                >
                  Submit Final Test
                </BrandButton>
              </div>
            </GlassCard>

            <ProgressBar
              value={Math.round(((currentIndex + 1) / questions.length) * 100)}
              label={`Progress: ${currentIndex + 1} / ${questions.length} answered`}
            />

            {/* Question Workspace Card */}
            <GlassCard className="p-6 md:p-8 space-y-6 bg-white border-2 border-[#E6DFD1] shadow-md">
              {/* Question Text */}
              <div className="space-y-2 border-b border-[#E6DFD1] pb-4">
                <h3 className="text-lg md:text-xl font-bold text-[#17233F] leading-relaxed whitespace-pre-line">
                  {currentQ.question_text}
                </h3>
              </div>

              {/* A. MCQ & Scenario Options */}
              {["mcq", "scenario"].includes(currentQ.assessment_type) && currentQ.options && (
                <div className="space-y-3 pt-2">
                  {currentQ.options.map((opt: any) => {
                    const isSelected = answers[currentQ.question_id] === opt.id;
                    return (
                      <div
                        key={opt.id}
                        onClick={() =>
                          setAnswers((prev) => ({
                            ...prev,
                            [currentQ.question_id]: opt.id,
                          }))
                        }
                        className={`p-4 rounded-xl border-2 cursor-pointer transition-all flex items-start gap-3.5 ${
                          isSelected
                            ? "bg-[#FFFDF5] border-[#D6A84B] shadow-sm ring-1 ring-[#D6A84B]/30"
                            : "bg-[#FBF8F1] border-[#E6DFD1] hover:border-[#D6A84B] hover:bg-white"
                        }`}
                      >
                        <span
                          className={`w-7 h-7 rounded-lg flex items-center justify-center font-black text-xs shrink-0 transition-all ${
                            isSelected
                              ? "bg-[#17233F] text-[#F0D99B]"
                              : "bg-[#E6DFD1] text-[#17233F]"
                          }`}
                        >
                          {opt.id}
                        </span>
                        <span className="text-sm pt-0.5 leading-relaxed font-semibold text-[#17233F]">
                          {opt.text}
                        </span>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* B. Coding & Debugging Sandbox Editor */}
              {["coding", "debugging"].includes(currentQ.assessment_type) && (
                <div className="space-y-4 pt-2">
                  {currentQ.sample_input && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
                      <div className="p-3 bg-[#10192D] rounded-xl border border-slate-700">
                        <span className="text-[#F0D99B] block mb-1 font-sans font-bold">Sample Input:</span>
                        <pre className="text-white whitespace-pre-wrap">{currentQ.sample_input}</pre>
                      </div>
                      <div className="p-3 bg-[#10192D] rounded-xl border border-slate-700">
                        <span className="text-[#34D399] block mb-1 font-sans font-bold">Expected Output:</span>
                        <pre className="text-white whitespace-pre-wrap">{currentQ.expected_output}</pre>
                      </div>
                    </div>
                  )}

                  <div>
                    <div className="flex items-center justify-between pb-2">
                      <span className="text-xs font-bold text-[#17233F] flex items-center gap-1.5">
                        <Terminal className="w-4 h-4 text-[#D6A84B]" />
                        Code Editor ({currentQ.coding_language || "python"})
                      </span>
                      <BrandButton
                        variant="violet"
                        size="sm"
                        disabled={runningSandbox}
                        onClick={() =>
                          handleRunCode(
                            answers[currentQ.question_id] || "",
                            currentQ.question_id
                          )
                        }
                        className="gap-2 text-xs font-bold"
                      >
                        <Play className="w-3.5 h-3.5 fill-current" />
                        {runningSandbox ? "Executing..." : "Run Test Sandbox"}
                      </BrandButton>
                    </div>

                    <textarea
                      rows={12}
                      value={answers[currentQ.question_id] || ""}
                      onChange={(e) =>
                        setAnswers((prev) => ({
                          ...prev,
                          [currentQ.question_id]: e.target.value,
                        }))
                      }
                      placeholder="# Write your implementation here in Python..."
                      className="w-full bg-[#10192D] border-2 border-slate-700 rounded-xl p-4 font-mono text-sm text-[#F5F0E6] focus:outline-none focus:border-[#D6A84B] transition-all"
                    />
                  </div>

                  {/* Sandbox Run Feedback */}
                  {sandboxOutput[currentQ.question_id] && (
                    <div className="p-4 bg-[#10192D] rounded-xl border border-slate-700 font-mono text-xs space-y-2">
                      <div className="flex items-center justify-between font-sans">
                        <span className="font-bold text-[#F0D99B]">Sandbox Test Results</span>
                        <span className="text-slate-400">
                          Execution: {sandboxOutput[currentQ.question_id].execution_time_ms} ms
                        </span>
                      </div>
                      {sandboxOutput[currentQ.question_id].error && (
                        <p className="text-rose-400 font-bold">{sandboxOutput[currentQ.question_id].error}</p>
                      )}
                      {sandboxOutput[currentQ.question_id].test_results?.map((tr: any, i: number) => (
                        <div key={i} className="flex items-center justify-between text-slate-200">
                          <span>{tr.test}</span>
                          <span
                            className={
                              tr.status.includes("PASSED")
                                ? "text-emerald-400 font-bold"
                                : "text-rose-400 font-bold"
                            }
                          >
                            {tr.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* C. SQL Challenge Sandbox Editor */}
              {currentQ.assessment_type === "sql" && (
                <div className="space-y-4 pt-2">
                  {currentQ.SQL_schema && (
                    <div className="p-3.5 bg-[#10192D] rounded-xl border border-slate-700 font-mono text-xs">
                      <span className="text-[#F0D99B] block mb-1 font-sans font-bold">Table Schema:</span>
                      <pre className="text-white whitespace-pre-wrap">{currentQ.SQL_schema}</pre>
                    </div>
                  )}

                  <div>
                    <div className="flex items-center justify-between pb-2">
                      <span className="text-xs font-bold text-[#17233F] flex items-center gap-1.5">
                        <Database className="w-4 h-4 text-[#D6A84B]" /> SQL Query Editor (ANSI SQL)
                      </span>
                      <BrandButton
                        variant="violet"
                        size="sm"
                        disabled={runningSandbox}
                        onClick={() =>
                          handleRunSQL(
                            answers[currentQ.question_id] || "",
                            currentQ.question_id
                          )
                        }
                        className="gap-2 text-xs font-bold"
                      >
                        <Play className="w-3.5 h-3.5 fill-current" />
                        {runningSandbox ? "Executing..." : "Execute Query"}
                      </BrandButton>
                    </div>

                    <textarea
                      rows={8}
                      value={answers[currentQ.question_id] || ""}
                      onChange={(e) =>
                        setAnswers((prev) => ({
                          ...prev,
                          [currentQ.question_id]: e.target.value,
                        }))
                      }
                      placeholder="SELECT ... FROM ... WHERE ...;"
                      className="w-full bg-[#10192D] border-2 border-slate-700 rounded-xl p-4 font-mono text-sm text-[#F5F0E6] focus:outline-none focus:border-[#D6A84B] transition-all"
                    />
                  </div>

                  {/* SQL Run Output */}
                  {sandboxOutput[currentQ.question_id] && (
                    <div className="p-4 bg-[#10192D] rounded-xl border border-slate-700 font-mono text-xs space-y-2 overflow-x-auto">
                      <div className="flex items-center justify-between font-sans">
                        <span className="font-bold text-[#F0D99B]">Query Output</span>
                        <span className="text-slate-400">
                          {sandboxOutput[currentQ.question_id].actual_rows?.length || 0} rows (
                          {sandboxOutput[currentQ.question_id].execution_time_ms} ms)
                        </span>
                      </div>
                      {sandboxOutput[currentQ.question_id].error && (
                        <p className="text-rose-400 font-bold">{sandboxOutput[currentQ.question_id].error}</p>
                      )}
                      {sandboxOutput[currentQ.question_id].actual_rows?.length > 0 && (
                        <table className="w-full text-left border-collapse border border-slate-700 text-slate-200">
                          <thead>
                            <tr className="bg-slate-800 border-b border-slate-700">
                              {Object.keys(sandboxOutput[currentQ.question_id].actual_rows[0]).map(
                                (col) => (
                                  <th key={col} className="p-2 border-r border-slate-700 font-bold text-[#F0D99B]">
                                    {col}
                                  </th>
                                )
                              )}
                            </tr>
                          </thead>
                          <tbody>
                            {sandboxOutput[currentQ.question_id].actual_rows.map(
                              (row: any, i: number) => (
                                <tr key={i} className="border-b border-slate-800 hover:bg-slate-800/40">
                                  {Object.values(row).map((val: any, j: number) => (
                                    <td key={j} className="p-2 border-r border-slate-800">
                                      {String(val)}
                                    </td>
                                  ))}
                                </tr>
                              )
                            )}
                          </tbody>
                        </table>
                      )}
                    </div>
                  )}
                </div>
              )}

              {/* D. System Design Architecture Response */}
              {currentQ.assessment_type === "system_design" && (
                <div className="space-y-4 pt-2">
                  <div className="text-xs text-[#374151] font-sans bg-[#F5F0E6] p-3.5 rounded-xl border border-[#E6DFD1]">
                    <span className="font-bold text-[#17233F] block mb-1">
                      Rubric Scoring Guidelines:
                    </span>
                    Explain component topology, data storage models, scaling strategies, latency bottlenecks, and trade-off considerations.
                  </div>

                  <textarea
                    rows={12}
                    value={answers[currentQ.question_id] || ""}
                    onChange={(e) =>
                      setAnswers((prev) => ({
                        ...prev,
                        [currentQ.question_id]: e.target.value,
                      }))
                    }
                    placeholder="Describe your distributed system architecture, load balancer placement, cache invalidation strategy, and database replication..."
                    className="w-full bg-[#10192D] border-2 border-slate-700 rounded-xl p-4 text-sm text-[#F5F0E6] focus:outline-none focus:border-[#D6A84B] transition-all"
                  />
                </div>
              )}

              {/* Question Navigation Controls */}
              <div className="flex items-center justify-between pt-6 border-t border-[#E6DFD1]">
                <BrandButton
                  variant="navy"
                  size="sm"
                  disabled={currentIndex === 0}
                  onClick={() => setCurrentIndex((prev) => prev - 1)}
                  className="gap-2 font-bold"
                >
                  <ArrowLeft className="w-4 h-4" /> Previous
                </BrandButton>

                {currentIndex < questions.length - 1 ? (
                  <BrandButton
                    variant="gold"
                    size="sm"
                    onClick={() => setCurrentIndex((prev) => prev + 1)}
                    className="gap-2 font-bold"
                  >
                    Next Question <ArrowRight className="w-4 h-4" />
                  </BrandButton>
                ) : (
                  <BrandButton
                    variant="gold"
                    size="sm"
                    onClick={handleSubmitAssessment}
                    className="gap-2 bg-emerald-600 hover:bg-emerald-500 font-bold"
                  >
                    <CheckCircle2 className="w-4 h-4" /> Complete & Submit
                  </BrandButton>
                )}
              </div>
            </GlassCard>
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* VIEW 3: RESULTS, SKILL GAPS & CAREER ROADMAP */}
        {/* ------------------------------------------------------------- */}
        {viewState === "result" && activeResult && (
          <div className="space-y-8">
            {/* Top Scorecard Hero Card */}
            <GlassCard className="p-8 bg-[#10192D] border-2 border-[#D6A84B]/40 shadow-xl text-white">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div className="space-y-2">
                  <div className="flex items-center gap-3">
                    <span className="text-xs uppercase font-bold tracking-wider px-2.5 py-1 rounded bg-[#D6A84B]/20 text-[#F0D99B] border border-[#D6A84B]/30">
                      Diagnostic Assessment Completed
                    </span>
                    <GoldBadge
                      variant={activeResult.passed ? "sage" : "terracotta"}
                    >
                      {activeResult.passed ? "VERIFIED PROFICIENT" : "NEEDS REFINEMENT"}
                    </GoldBadge>
                  </div>
                  <h2 className="text-2xl md:text-3xl font-black text-white tracking-tight">
                    {activeResult.role_title} Capability Score
                  </h2>
                  <p className="text-xs md:text-sm text-[#E6DFD1]/80 max-w-xl leading-relaxed">
                    Evaluated across all test categories via 1PL Item Response Theory & Sandbox Verification.
                  </p>
                </div>

                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <span className="text-5xl md:text-6xl font-black text-[#F0D99B] font-mono tracking-tight">
                      {activeResult.overall_score_percentage}%
                    </span>
                    <span className="text-xs text-[#E6DFD1] block mt-1 font-bold">
                      {activeResult.points_awarded} / {activeResult.total_points} Points Awarded
                    </span>
                  </div>
                </div>
              </div>

              {/* AI Narrative Assessment Feedback */}
              {activeResult.narrative_summary && (
                <div className="mt-6 p-4 rounded-xl bg-[#17233F] border border-[#D6A84B]/30 space-y-2">
                  <div className="flex items-center gap-2 text-[#F0D99B] text-xs font-bold uppercase tracking-wider">
                    <Sparkles className="w-4 h-4 text-[#D6A84B]" /> AI Capability Intelligence
                  </div>
                  <p className="text-sm text-[#F5F0E6] leading-relaxed font-medium">
                    {activeResult.narrative_summary.narrative_assessment}
                  </p>
                </div>
              )}
            </GlassCard>

            {/* Skill Mastery Breakdown */}
            <div className="space-y-4">
              <h3 className="text-lg font-black text-[#17233F] flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-[#D6A84B]" />
                Skill-by-Skill Competency Mastery
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {activeResult.skill_performances?.map((sp: any, idx: number) => (
                  <GlassCard key={`${sp.skill_id}-${idx}`} className="p-5 bg-white border-2 border-[#E6DFD1] shadow-xs space-y-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-bold text-[#17233F] text-sm">{sp.skill_name}</h4>
                        <span className="text-xs text-[#4B5563] font-medium">
                          {sp.correct_count} of {sp.evidence_count} items correct
                        </span>
                      </div>
                      <span
                        className={`text-xs px-2.5 py-0.5 rounded-full font-bold uppercase ${
                          sp.status === "proficient"
                            ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                            : sp.status === "developing"
                            ? "bg-amber-50 text-amber-700 border border-amber-200"
                            : "bg-rose-50 text-rose-700 border border-rose-200"
                        }`}
                      >
                        {sp.status.replace("_", " ")}
                      </span>
                    </div>
                    <ProgressBar
                      value={sp.mastery_percentage}
                      label={`Mastery: ${sp.mastery_percentage}%`}
                    />
                    <div className="text-right text-xs font-bold text-[#4B5563]">
                      Confidence: {Math.round(sp.confidence * 100)}%
                    </div>
                  </GlassCard>
                ))}
              </div>
            </div>

            {/* Identified Skill Gaps */}
            {activeResult.skill_gaps?.length > 0 && (
              <div className="space-y-4">
                <h3 className="text-lg font-black text-[#17233F] flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-[#D6A84B]" />
                  Identified Technical Skill Gaps
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {activeResult.skill_gaps.map((gap: any, idx: number) => (
                    <GlassCard key={`${gap.skill_id}-${idx}`} className="p-4 bg-white border-2 border-[#E6DFD1] shadow-xs space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200">
                          {gap.priority} PRIORITY GAP
                        </span>
                        <span className="text-xs text-rose-600 font-bold font-mono">
                          -{gap.gap_delta}% Delta
                        </span>
                      </div>
                      <h4 className="font-bold text-[#17233F] text-sm mt-1">{gap.skill_name}</h4>
                      <p className="text-xs text-[#4B5563] font-medium">
                        Current: {gap.current_level}% • Target: {gap.target_level}%
                      </p>
                    </GlassCard>
                  ))}
                </div>
              </div>
            )}

            {/* Personalized Career Roadmap Milestones */}
            {activeResult.roadmap_milestones?.length > 0 && (
              <div className="space-y-4">
                <h3 className="text-lg font-black text-[#17233F] flex items-center gap-2">
                  <Cpu className="w-5 h-5 text-[#D6A84B]" />
                  Targeted Career Growth Roadmap
                </h3>
                <div className="space-y-3">
                  {activeResult.roadmap_milestones.map((m: any) => (
                    <GlassCard key={m.milestone_id} className="p-5 bg-white border-2 border-[#E6DFD1] shadow-xs space-y-3">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div className="flex items-center gap-3">
                          <span className="w-8 h-8 rounded-full bg-[#17233F] flex items-center justify-center font-bold text-xs text-[#F0D99B] shrink-0">
                            {m.order_index}
                          </span>
                          <div>
                            <h4 className="font-bold text-[#17233F] text-base">{m.skill_name}</h4>
                            <p className="text-xs text-[#4B5563] mt-0.5">{m.reason}</p>
                          </div>
                        </div>
                        <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-[#F5F0E6] border border-[#E6DFD1] text-[#17233F]">
                          Est: {m.estimated_hours} hrs
                        </span>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 text-xs">
                        <div className="p-3 bg-[#FBF8F1] rounded-xl border border-[#E6DFD1]">
                          <span className="text-[#17233F] font-bold block mb-1">
                            Learning Objective:
                          </span>
                          <p className="text-[#374151] leading-relaxed">{m.learning_objective}</p>
                        </div>
                        <div className="p-3 bg-[#FBF8F1] rounded-xl border border-[#E6DFD1]">
                          <span className="text-[#17233F] font-bold block mb-1">
                            Hands-On Project Task:
                          </span>
                          <p className="text-[#374151] leading-relaxed">{m.hands_on_task}</p>
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-1">
                        <span className="text-xs text-[#4B5563]">
                          Curated Resource: <strong className="text-[#17233F]">{m.resource_title}</strong> ({m.resource_type})
                        </span>
                        {m.resource_url && (
                          <a
                            href={m.resource_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs text-[#7355D9] hover:underline flex items-center gap-1 font-bold"
                          >
                            Access Module <ExternalLink className="w-3 h-3" />
                          </a>
                        )}
                      </div>
                    </GlassCard>
                  ))}
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center justify-center gap-4 pt-4">
              <BrandButton
                variant="gold"
                onClick={() => setViewState("catalog")}
                className="gap-2 font-bold py-3 px-6 shadow-md"
              >
                <RotateCcw className="w-4 h-4" /> Start New Assessment
              </BrandButton>
            </div>
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* VIEW 4: ASSESSMENT HISTORY */}
        {/* ------------------------------------------------------------- */}
        {viewState === "history" && (
          <div className="space-y-6">
            <h2 className="text-xl font-black text-[#17233F] flex items-center gap-2">
              <History className="w-5 h-5 text-[#D6A84B]" />
              Your Technical Assessment History
            </h2>

            {historyList.length === 0 ? (
              <GlassCard className="p-8 text-center text-[#4B5563] bg-white border-2 border-[#E6DFD1]">
                No technical assessments recorded yet. Select a career role to begin your first diagnostic attempt!
              </GlassCard>
            ) : (
              <div className="space-y-3">
                {historyList.map((item) => (
                  <GlassCard
                    key={item.result_id}
                    className="p-5 bg-white border-2 border-[#E6DFD1] flex items-center justify-between hover:border-[#D6A84B] shadow-xs transition-all"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-bold text-[#17233F] text-base">{item.role_title}</h3>
                        <GoldBadge
                          variant={item.passed ? "sage" : "terracotta"}
                          size="sm"
                        >
                          {item.passed ? "PASSED" : "REVIEW"}
                        </GoldBadge>
                      </div>
                      <p className="text-xs text-[#4B5563] mt-1 font-medium">
                        Completed: {new Date(item.completed_at).toLocaleString()} • {item.difficulty_mode.toUpperCase()}
                      </p>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <span className="text-xl font-black font-mono text-[#D6A84B]">
                          {item.overall_score_percentage}%
                        </span>
                        <span className="text-xs text-[#4B5563] font-bold block">
                          {item.points_awarded}/{item.total_points} pts
                        </span>
                      </div>
                      <BrandButton
                        variant="navy"
                        size="sm"
                        onClick={() => {
                          setActiveResult(item);
                          setViewState("result");
                        }}
                        className="font-bold text-xs"
                      >
                        View Report
                      </BrandButton>
                    </div>
                  </GlassCard>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
