"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/AppShell";
import { GlassCard } from "@/components/ui/GlassCard";
import { ResumeReviewStep } from "@/components/resume-engine/ResumeReviewStep";
import { DesignGallery } from "@/components/resume-engine/DesignGallery";
import { ResumeStudio } from "@/components/resume-engine/ResumeStudio";
import {
  ResumeFullData,
  EducationEntry,
  ExperienceEntry,
  InternshipEntry,
  ProjectEntry,
  CertificationEntry,
} from "@/types/resume-generator";
import { DesignSpecification } from "@/types/resume-design-engine";
import {
  getRecommendedDesign,
  getDesignById,
} from "@/services/resume-design-engine";
import {
  fresherProfile,
  aimlStudentProfile,
  softwareDevProfile,
  experiencedLeadProfile,
} from "@/data/resume-sample-profiles";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import {
  User,
  GraduationCap,
  Wrench,
  Briefcase,
  Zap,
  FolderGit2,
  Award,
  Sparkles,
  ChevronRight,
  ChevronLeft,
  Plus,
  Trash2,
  ArrowUp,
  ArrowDown,
  RefreshCw,
  FolderOpen,
  X,
  Info,
  Check,
  CheckCircle2,
  Layers,
  ArrowRight,
  SlidersHorizontal,
  FileText,
  FileCheck,
} from "lucide-react";

// Clean initial empty resume - no fake or prefilled data for real users
const initialEmptyResume: ResumeFullData = {
  personalInfo: {
    fullName: "",
    professionalTitle: "",
    email: "",
    phone: "",
    location: "",
    linkedIn: "",
    gitHub: "",
    portfolio: "",
    summary: "",
  },
  education: [],
  skills: {
    programmingLanguages: [],
    frameworks: [],
    databases: [],
    developerTools: [],
    aiMlSkills: [],
    otherSkills: [],
  },
  experience: [],
  internships: [],
  projects: [],
  certifications: [],
  additional: {
    achievements: [],
    awards: [],
    publications: [],
    volunteerExperience: [],
    extracurricular: [],
    languages: [],
    interests: [],
  },
  templateId: "modern",
  accentColor: "#17233F",
  typography: "sans",
  spacing: "normal",
};

type WorkflowPhase = "wizard" | "review" | "gallery" | "studio";

export default function ResumeGeneratorPage() {
  // Main Data State (Clean empty state by default)
  const [resumeData, setResumeData] = useState<ResumeFullData>(initialEmptyResume);

  // Workflow Phase & Stepper
  const [phase, setPhase] = useState<WorkflowPhase>("wizard");
  const [currentStep, setCurrentStep] = useState<number>(1);

  // Selected Design (from 1000+ catalog)
  const [selectedDesign, setSelectedDesign] = useState<DesignSpecification>(() =>
    getDesignById("des-0001")
  );

  // AI Loading & Logs
  const [isGeneratingAI, setIsGeneratingAI] = useState<boolean>(false);
  const [isPolishingText, setIsPolishingText] = useState<string | null>(null);
  const [aiModifications, setAiModifications] = useState<string[]>([]);
  const [aiLatency, setAiLatency] = useState<number | null>(null);

  // Database Persistence
  const [savedResumesList, setSavedResumesList] = useState<any[]>([]);
  const [showSavedModal, setShowSavedModal] = useState<boolean>(false);
  const [activeResumeId, setActiveResumeId] = useState<string | null>(null);
  const [showDevProfiles, setShowDevProfiles] = useState<boolean>(false);

  // Fetch saved resumes on load
  useEffect(() => {
    loadSavedResumes();
  }, []);

  const loadSavedResumes = async () => {
    try {
      const res = await apiService.listSavedResumes();
      if (res.data) {
        setSavedResumesList(res.data);
      }
    } catch {
      // Offline or guest mode
    }
  };

  // Optional Dev Profile Loader (explicit action only)
  const handleLoadSample = (profileKey: "fresher" | "aiml" | "dev" | "lead") => {
    let selected: ResumeFullData;
    let label = "";
    if (profileKey === "fresher") {
      selected = fresherProfile;
      label = "College Fresher (CS/IT)";
    } else if (profileKey === "aiml") {
      selected = aimlStudentProfile;
      label = "AI / ML Graduate Student";
    } else if (profileKey === "dev") {
      selected = softwareDevProfile;
      label = "Full-Stack Software Engineer";
    } else {
      selected = experiencedLeadProfile;
      label = "Experienced Engineering Director";
    }
    setResumeData(selected);
    setShowDevProfiles(false);
    toast.success(`Loaded dev profile: "${label}"`);
  };

  // AI Generation Pipeline: Sends user's entered data to local Qwen2.5-1.5B model
  const handleAIGenerateFull = async () => {
    setIsGeneratingAI(true);
    setAiModifications([]);
    try {
      toast.info("Sending your entered data to local Qwen2.5-1.5B MLX model...");
      const res = await apiService.aiGenerateResume({
        rawResumeData: resumeData,
        targetRole: resumeData.personalInfo.professionalTitle || "Software Engineer",
      });

      if (res.data) {
        const enhanced = res.data.enhancedResumeData;
        setResumeData(enhanced);
        setAiModifications(res.data.modificationsSummary);
        setAiLatency(res.data.generationLatencyMs);

        // Intelligently select recommended design based on user profile
        const recommended = getRecommendedDesign(enhanced);
        setSelectedDesign(recommended);

        toast.success(
          `AI Generation complete in ${(res.data.generationLatencyMs / 1000).toFixed(1)}s! Opening Design Gallery.`
        );

        // Move to Gallery phase
        setPhase("gallery");
      }
    } catch (err: any) {
      toast.error(`AI Generation Error: ${err.message || "Failed to reach AI model"}`);
      // Even if AI model fails, allow proceeding to gallery with user's current data
      const recommended = getRecommendedDesign(resumeData);
      setSelectedDesign(recommended);
      setPhase("gallery");
    } finally {
      setIsGeneratingAI(false);
    }
  };

  // Inline AI Polish for Specific Snippets
  const handlePolishSnippet = async (fieldKey: string, text: string, sectionType: string) => {
    if (!text || text.trim().length < 5) {
      toast.error("Please enter some text to polish first.");
      return;
    }
    setIsPolishingText(fieldKey);
    try {
      const res = await apiService.aiEnhanceText({
        text,
        sectionType,
        contextRole: resumeData.personalInfo.professionalTitle,
      });
      if (res.data) {
        toast.success("Bullet point enhanced with strong action verbs!");
        return res.data.enhancedText;
      }
    } catch (err: any) {
      toast.error(`Polish error: ${err.message}`);
    } finally {
      setIsPolishingText(null);
    }
    return text;
  };

  // Stepper Items (7 core information steps)
  const formSteps = [
    { num: 1, label: "Personal Info", icon: User },
    { num: 2, label: "Education", icon: GraduationCap },
    { num: 3, label: "Technical Skills", icon: Wrench },
    { num: 4, label: "Work Experience", icon: Briefcase },
    { num: 5, label: "Internships", icon: Zap },
    { num: 6, label: "Projects", icon: FolderGit2 },
    { num: 7, label: "Certifications", icon: Award },
  ];

  // Helper reorder array
  const moveItem = <T,>(arr: T[], index: number, direction: "up" | "down"): T[] => {
    const copy = [...arr];
    const targetIndex = direction === "up" ? index - 1 : index + 1;
    if (targetIndex < 0 || targetIndex >= copy.length) return copy;
    const temp = copy[index];
    copy[index] = copy[targetIndex];
    copy[targetIndex] = temp;
    return copy;
  };

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Phase Progress Header */}
        <div className="no-print p-6 rounded-3xl bg-white border border-[#E6DFD1] shadow-xs space-y-4">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#17233F] text-[#F0D99B] text-[10px] font-black uppercase tracking-wider mb-1.5">
                <Sparkles className="w-3.5 h-3.5" /> Feature 3: Complete Resume Journey
              </div>
              <h1 className="text-xl sm:text-2xl font-black text-[#17233F] tracking-tight">
                {phase === "wizard" && "Step 1 of 3: Enter Your Credentials"}
                {phase === "review" && "Step 2 of 3: Review & Validate Your Data"}
                {phase === "gallery" && "Step 3 of 3: Choose from 1000+ Resume Designs"}
                {phase === "studio" && "Final Resume Studio: Customize & Export"}
              </h1>
              <p className="text-xs text-[#687187] mt-0.5 max-w-2xl leading-relaxed">
                {phase === "wizard" &&
                  "Enter your genuine factual background across the 7 structured steps below. No preview or fake content is shown while entering data."}
                {phase === "review" &&
                  "Review all your entered information. Missing optional fields remain cleanly blank. When ready, trigger genuine local Qwen2.5-1.5B AI generation."}
                {phase === "gallery" &&
                  "Explore over 1,000 algorithmic designs rendered dynamically with your actual profile. Filter by style, role, or ATS compatibility."}
                {phase === "studio" &&
                  "Adjust styling, typography, spacing, or edit wording directly. Export in 100% vector PDF or ATS Word (.docx)."}
              </p>
            </div>

            {/* Workflow Breadcrumbs & Utilities */}
            <div className="flex flex-wrap items-center gap-2">
              <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-2xl text-xs font-bold text-slate-600">
                <button
                  onClick={() => setPhase("wizard")}
                  className={`px-3 py-1.5 rounded-xl transition-all cursor-pointer flex items-center gap-1 ${
                    phase === "wizard" ? "bg-[#17233F] text-[#F0D99B] shadow-xs" : "hover:text-slate-900"
                  }`}
                >
                  <FileText className="w-3.5 h-3.5" /> 1. Input Form
                </button>
                <ChevronRight className="w-3 h-3 text-slate-400" />
                <button
                  onClick={() => setPhase("review")}
                  className={`px-3 py-1.5 rounded-xl transition-all cursor-pointer flex items-center gap-1 ${
                    phase === "review" ? "bg-[#17233F] text-[#F0D99B] shadow-xs" : "hover:text-slate-900"
                  }`}
                >
                  <FileCheck className="w-3.5 h-3.5" /> 2. Review
                </button>
                <ChevronRight className="w-3 h-3 text-slate-400" />
                <button
                  onClick={() => setPhase("gallery")}
                  className={`px-3 py-1.5 rounded-xl transition-all cursor-pointer flex items-center gap-1 ${
                    phase === "gallery" ? "bg-[#17233F] text-[#F0D99B] shadow-xs" : "hover:text-slate-900"
                  }`}
                >
                  <Layers className="w-3.5 h-3.5" /> 3. 1000+ Designs
                </button>
              </div>

              {/* Dev Profiles Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setShowDevProfiles(!showDevProfiles)}
                  className="px-3 py-2 rounded-xl text-xs font-bold bg-amber-50 hover:bg-amber-100 border border-amber-200 text-amber-900 flex items-center gap-1.5 transition-all cursor-pointer"
                  title="Dev testing utility only"
                >
                  <span>🧪 Dev Profiles</span>
                </button>
                {showDevProfiles && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-xl border border-slate-200 p-2 z-50 space-y-1">
                    <div className="text-[10px] font-black uppercase text-slate-400 px-2 py-1">
                      Dev Testing Only (Pre-fill)
                    </div>
                    <button
                      onClick={() => handleLoadSample("fresher")}
                      className="w-full text-left px-2.5 py-1.5 rounded-lg text-xs hover:bg-slate-50 font-medium text-slate-700"
                    >
                      🎓 College Fresher
                    </button>
                    <button
                      onClick={() => handleLoadSample("aiml")}
                      className="w-full text-left px-2.5 py-1.5 rounded-lg text-xs hover:bg-slate-50 font-medium text-slate-700"
                    >
                      🤖 AI / ML Graduate
                    </button>
                    <button
                      onClick={() => handleLoadSample("dev")}
                      className="w-full text-left px-2.5 py-1.5 rounded-lg text-xs hover:bg-slate-50 font-medium text-slate-700"
                    >
                      💻 Software Developer
                    </button>
                    <button
                      onClick={() => handleLoadSample("lead")}
                      className="w-full text-left px-2.5 py-1.5 rounded-lg text-xs hover:bg-slate-50 font-medium text-slate-700"
                    >
                      👔 Engineering Director
                    </button>
                    <button
                      onClick={() => {
                        setResumeData(initialEmptyResume);
                        setShowDevProfiles(false);
                        toast.info("Cleared resume data to empty form.");
                      }}
                      className="w-full text-left px-2.5 py-1.5 rounded-lg text-xs hover:bg-rose-50 text-rose-600 font-bold border-t border-slate-100 mt-1"
                    >
                      🗑️ Clear Form (Empty)
                    </button>
                  </div>
                )}
              </div>

              {/* AI ATS Intelligence Link */}
              <Link
                href="/resume/ats-checker"
                className="px-3 py-2 rounded-xl text-xs font-bold bg-[#7355D9]/10 hover:bg-[#7355D9]/20 text-[#7355D9] border border-[#7355D9]/30 flex items-center gap-1.5 transition-all cursor-pointer"
              >
                <Sparkles className="w-3.5 h-3.5 text-[#7355D9]" />
                <span>AI ATS Intelligence</span>
              </Link>

              {/* Saved Resumes Button */}
              <button
                onClick={() => setShowSavedModal(true)}
                className="px-3 py-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center gap-1.5 transition-all cursor-pointer"
              >
                <FolderOpen className="w-3.5 h-3.5" />
                <span>Saved ({savedResumesList.length})</span>
              </button>
            </div>
          </div>
        </div>

        {/* PHASE 1: STRICT 7-STEP WIZARD (Form-Only, Full Width, No Preview) */}
        {phase === "wizard" && (
          <div className="max-w-4xl mx-auto space-y-6">
            <div className="p-6 sm:p-8 rounded-3xl bg-white border border-[#E6DFD1] shadow-xs space-y-6">
              {/* Stepper Navigation */}
              <div className="flex items-center justify-between border-b border-slate-100 pb-4 overflow-x-auto gap-2">
                {formSteps.map((s) => {
                  const Icon = s.icon;
                  const isActive = currentStep === s.num;
                  const isDone = currentStep > s.num;
                  return (
                    <button
                      key={s.num}
                      onClick={() => setCurrentStep(s.num)}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold shrink-0 transition-all cursor-pointer ${
                        isActive
                          ? "bg-[#17233F] text-[#F0D99B] shadow-xs"
                          : isDone
                          ? "bg-emerald-50 text-emerald-800 border border-emerald-200"
                          : "text-slate-400 hover:text-slate-700 bg-slate-50"
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      <span>
                        {s.num}. {s.label}
                      </span>
                    </button>
                  );
                })}
              </div>

              {/* STEP 1: Personal Information */}
              {currentStep === 1 && (
                <div className="space-y-4">
                  <div className="border-b border-slate-100 pb-2">
                    <h3 className="text-sm font-black text-[#17233F]">1. Personal & Contact Information</h3>
                    <p className="text-xs text-slate-500">Provide your basic contact details and target professional title.</p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Full Name *</label>
                      <input
                        type="text"
                        value={resumeData.personalInfo.fullName}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            personalInfo: { ...resumeData.personalInfo, fullName: e.target.value },
                          })
                        }
                        placeholder="e.g. Rohan Verma"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Professional Title *</label>
                      <input
                        type="text"
                        value={resumeData.personalInfo.professionalTitle}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            personalInfo: { ...resumeData.personalInfo, professionalTitle: e.target.value },
                          })
                        }
                        placeholder="e.g. Senior Software Engineer"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Email Address *</label>
                      <input
                        type="email"
                        value={resumeData.personalInfo.email}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            personalInfo: { ...resumeData.personalInfo, email: e.target.value },
                          })
                        }
                        placeholder="rohan@example.com"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Phone Number *</label>
                      <input
                        type="text"
                        value={resumeData.personalInfo.phone}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            personalInfo: { ...resumeData.personalInfo, phone: e.target.value },
                          })
                        }
                        placeholder="+91 98765 43210"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Location *</label>
                      <input
                        type="text"
                        value={resumeData.personalInfo.location}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            personalInfo: { ...resumeData.personalInfo, location: e.target.value },
                          })
                        }
                        placeholder="e.g. Bengaluru, India"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">LinkedIn Profile</label>
                      <input
                        type="text"
                        value={resumeData.personalInfo.linkedIn || ""}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            personalInfo: { ...resumeData.personalInfo, linkedIn: e.target.value },
                          })
                        }
                        placeholder="https://linkedin.com/in/username"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">GitHub Profile</label>
                      <input
                        type="text"
                        value={resumeData.personalInfo.gitHub || ""}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            personalInfo: { ...resumeData.personalInfo, gitHub: e.target.value },
                          })
                        }
                        placeholder="https://github.com/username"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Portfolio / Website</label>
                      <input
                        type="text"
                        value={resumeData.personalInfo.portfolio || ""}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            personalInfo: { ...resumeData.personalInfo, portfolio: e.target.value },
                          })
                        }
                        placeholder="https://myportfolio.dev"
                        className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                      />
                    </div>
                  </div>

                  {/* Summary Field */}
                  <div className="pt-2">
                    <div className="flex items-center justify-between mb-1">
                      <label className="text-xs font-bold text-slate-700">Executive Summary</label>
                      <button
                        type="button"
                        onClick={async () => {
                          const elevated = await handlePolishSnippet(
                            "summary",
                            resumeData.personalInfo.summary,
                            "summary"
                          );
                          if (elevated) {
                            setResumeData({
                              ...resumeData,
                              personalInfo: { ...resumeData.personalInfo, summary: elevated },
                            });
                          }
                        }}
                        disabled={isPolishingText === "summary"}
                        className="text-[11px] font-bold text-[#7355D9] hover:underline flex items-center gap-1 cursor-pointer disabled:opacity-50"
                      >
                        <Sparkles className="w-3 h-3" />
                        {isPolishingText === "summary" ? "Polishing..." : "AI Polish"}
                      </button>
                    </div>
                    <textarea
                      rows={4}
                      value={resumeData.personalInfo.summary}
                      onChange={(e) =>
                        setResumeData({
                          ...resumeData,
                          personalInfo: { ...resumeData.personalInfo, summary: e.target.value },
                        })
                      }
                      placeholder="High-impact 2-4 sentence summary of your career focus, technical competencies, and quantifiable achievements..."
                      className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-[#7355D9] outline-none"
                    />
                  </div>
                </div>
              )}

              {/* STEP 2: Education */}
              {currentStep === 2 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                    <div>
                      <h3 className="text-sm font-black text-[#17233F]">2. Academic Credentials</h3>
                      <p className="text-xs text-slate-500">Add degrees, institutions, graduation dates and coursework.</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        const newEdu: EducationEntry = {
                          id: `edu-${Date.now()}`,
                          institution: "",
                          degree: "",
                          fieldOfStudy: "",
                          startDate: "",
                          endDate: "",
                          grade: "",
                          coursework: [],
                        };
                        setResumeData({
                          ...resumeData,
                          education: [...resumeData.education, newEdu],
                        });
                      }}
                      className="btn-violet px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1 cursor-pointer"
                    >
                      <Plus className="w-3.5 h-3.5" /> Add Degree
                    </button>
                  </div>

                  {resumeData.education.length === 0 ? (
                    <div className="p-8 text-center border-2 border-dashed border-slate-200 rounded-2xl space-y-2">
                      <GraduationCap className="w-8 h-8 text-slate-300 mx-auto" />
                      <p className="text-xs font-bold text-slate-600">No education entries added yet.</p>
                      <p className="text-[11px] text-slate-400">Click &quot;Add Degree&quot; above to add your university or college details.</p>
                    </div>
                  ) : (
                    resumeData.education.map((edu, idx) => (
                      <div
                        key={edu.id}
                        className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3 relative group"
                      >
                        <div className="flex items-center justify-between border-b border-slate-200/60 pb-2">
                          <span className="text-xs font-black text-[#17233F]">Degree #{idx + 1}</span>
                          <div className="flex items-center gap-1">
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  education: moveItem(resumeData.education, idx, "up"),
                                })
                              }
                              disabled={idx === 0}
                              className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-20 cursor-pointer"
                              title="Move Up"
                            >
                              <ArrowUp className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  education: moveItem(resumeData.education, idx, "down"),
                                })
                              }
                              disabled={idx === resumeData.education.length - 1}
                              className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-20 cursor-pointer"
                              title="Move Down"
                            >
                              <ArrowDown className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  education: resumeData.education.filter((_, i) => i !== idx),
                                })
                              }
                              className="p-1 text-rose-500 hover:text-rose-700 cursor-pointer"
                              title="Delete Degree"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Institution *</label>
                            <input
                              type="text"
                              value={edu.institution}
                              onChange={(e) => {
                                const copy = [...resumeData.education];
                                copy[idx].institution = e.target.value;
                                setResumeData({ ...resumeData, education: copy });
                              }}
                              placeholder="e.g. Indian Institute of Technology"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Degree *</label>
                            <input
                              type="text"
                              value={edu.degree}
                              onChange={(e) => {
                                const copy = [...resumeData.education];
                                copy[idx].degree = e.target.value;
                                setResumeData({ ...resumeData, education: copy });
                              }}
                              placeholder="e.g. Bachelor of Technology"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Field of Study</label>
                            <input
                              type="text"
                              value={edu.fieldOfStudy}
                              onChange={(e) => {
                                const copy = [...resumeData.education];
                                copy[idx].fieldOfStudy = e.target.value;
                                setResumeData({ ...resumeData, education: copy });
                              }}
                              placeholder="e.g. Computer Science and Engineering"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Grade / CGPA</label>
                            <input
                              type="text"
                              value={edu.grade || ""}
                              onChange={(e) => {
                                const copy = [...resumeData.education];
                                copy[idx].grade = e.target.value;
                                setResumeData({ ...resumeData, education: copy });
                              }}
                              placeholder="e.g. 8.9 / 10.0"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Start Date</label>
                            <input
                              type="text"
                              value={edu.startDate}
                              onChange={(e) => {
                                const copy = [...resumeData.education];
                                copy[idx].startDate = e.target.value;
                                setResumeData({ ...resumeData, education: copy });
                              }}
                              placeholder="e.g. Aug 2020"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">End Date</label>
                            <input
                              type="text"
                              value={edu.endDate}
                              onChange={(e) => {
                                const copy = [...resumeData.education];
                                copy[idx].endDate = e.target.value;
                                setResumeData({ ...resumeData, education: copy });
                              }}
                              placeholder="e.g. May 2024"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>
                        </div>

                        <div>
                          <label className="text-[11px] font-bold text-slate-700 block mb-0.5">
                            Key Coursework (Comma-separated)
                          </label>
                          <input
                            type="text"
                            value={edu.coursework.join(", ")}
                            onChange={(e) => {
                              const copy = [...resumeData.education];
                              copy[idx].coursework = e.target.value
                                .split(",")
                                .map((s) => s.trim())
                                .filter(Boolean);
                              setResumeData({ ...resumeData, education: copy });
                            }}
                            placeholder="Data Structures, Algorithms, Operating Systems, Machine Learning"
                            className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                          />
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* STEP 3: Technical Skills */}
              {currentStep === 3 && (
                <div className="space-y-4">
                  <div className="border-b border-slate-100 pb-2">
                    <h3 className="text-sm font-black text-[#17233F]">3. Categorized Technical Skills</h3>
                    <p className="text-xs text-slate-500">
                      Organize your skills by domain so ATS parsers and technical interviewers easily scan your stack.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">
                        Programming Languages (Comma-separated)
                      </label>
                      <input
                        type="text"
                        value={resumeData.skills.programmingLanguages.join(", ")}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            skills: {
                              ...resumeData.skills,
                              programmingLanguages: e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
                            },
                          })
                        }
                        placeholder="Python, TypeScript, JavaScript, C++, Java, Go"
                        className="w-full px-3 py-2 rounded-xl border text-xs"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">
                        Frameworks & Libraries (Comma-separated)
                      </label>
                      <input
                        type="text"
                        value={resumeData.skills.frameworks.join(", ")}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            skills: {
                              ...resumeData.skills,
                              frameworks: e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
                            },
                          })
                        }
                        placeholder="React, Next.js, Node.js, FastAPI, Django, PyTorch"
                        className="w-full px-3 py-2 rounded-xl border text-xs"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Databases (Comma-separated)</label>
                      <input
                        type="text"
                        value={resumeData.skills.databases.join(", ")}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            skills: {
                              ...resumeData.skills,
                              databases: e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
                            },
                          })
                        }
                        placeholder="PostgreSQL, MongoDB, Redis, SQLite, Pinecone"
                        className="w-full px-3 py-2 rounded-xl border text-xs"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Developer Tools & Cloud</label>
                      <input
                        type="text"
                        value={resumeData.skills.developerTools.join(", ")}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            skills: {
                              ...resumeData.skills,
                              developerTools: e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
                            },
                          })
                        }
                        placeholder="Docker, Git, AWS, GCP, GitHub Actions, Linux, Kubernetes"
                        className="w-full px-3 py-2 rounded-xl border text-xs"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">AI / ML & Data Skills</label>
                      <input
                        type="text"
                        value={resumeData.skills.aiMlSkills.join(", ")}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            skills: {
                              ...resumeData.skills,
                              aiMlSkills: e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
                            },
                          })
                        }
                        placeholder="MLX, Hugging Face, LLMs, RAG, Transformers, Scikit-Learn"
                        className="w-full px-3 py-2 rounded-xl border text-xs"
                      />
                    </div>

                    <div>
                      <label className="text-xs font-bold text-slate-700 block mb-1">Other Professional Skills</label>
                      <input
                        type="text"
                        value={resumeData.skills.otherSkills.join(", ")}
                        onChange={(e) =>
                          setResumeData({
                            ...resumeData,
                            skills: {
                              ...resumeData.skills,
                              otherSkills: e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
                            },
                          })
                        }
                        placeholder="REST APIs, Microservices, System Architecture, Agile/Scrum"
                        className="w-full px-3 py-2 rounded-xl border text-xs"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 4: Work Experience */}
              {currentStep === 4 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                    <div>
                      <h3 className="text-sm font-black text-[#17233F]">4. Work Experience</h3>
                      <p className="text-xs text-slate-500">Add full-time and contractual work positions with quantifiable bullets.</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        const newExp: ExperienceEntry = {
                          id: `exp-${Date.now()}`,
                          company: "",
                          role: "",
                          employmentType: "Full-Time",
                          location: "",
                          startDate: "",
                          endDate: "Present",
                          current: true,
                          responsibilities: [""],
                        };
                        setResumeData({
                          ...resumeData,
                          experience: [...resumeData.experience, newExp],
                        });
                      }}
                      className="btn-violet px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1 cursor-pointer"
                    >
                      <Plus className="w-3.5 h-3.5" /> Add Experience
                    </button>
                  </div>

                  {resumeData.experience.length === 0 ? (
                    <div className="p-8 text-center border-2 border-dashed border-slate-200 rounded-2xl space-y-2">
                      <Briefcase className="w-8 h-8 text-slate-300 mx-auto" />
                      <p className="text-xs font-bold text-slate-600">No work experience entries added yet.</p>
                      <p className="text-[11px] text-slate-400">
                        If you are a student or fresher, feel free to skip to Internships & Projects.
                      </p>
                    </div>
                  ) : (
                    resumeData.experience.map((exp, idx) => (
                      <div
                        key={exp.id}
                        className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3 relative group"
                      >
                        <div className="flex items-center justify-between border-b border-slate-200/60 pb-2">
                          <span className="text-xs font-black text-[#17233F]">Position #{idx + 1}</span>
                          <div className="flex items-center gap-1">
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  experience: moveItem(resumeData.experience, idx, "up"),
                                })
                              }
                              disabled={idx === 0}
                              className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-20 cursor-pointer"
                              title="Move Up"
                            >
                              <ArrowUp className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  experience: moveItem(resumeData.experience, idx, "down"),
                                })
                              }
                              disabled={idx === resumeData.experience.length - 1}
                              className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-20 cursor-pointer"
                              title="Move Down"
                            >
                              <ArrowDown className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  experience: resumeData.experience.filter((_, i) => i !== idx),
                                })
                              }
                              className="p-1 text-rose-500 hover:text-rose-700 cursor-pointer"
                              title="Delete Position"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Company *</label>
                            <input
                              type="text"
                              value={exp.company}
                              onChange={(e) => {
                                const copy = [...resumeData.experience];
                                copy[idx].company = e.target.value;
                                setResumeData({ ...resumeData, experience: copy });
                              }}
                              placeholder="e.g. Google / Microsoft"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Role / Title *</label>
                            <input
                              type="text"
                              value={exp.role}
                              onChange={(e) => {
                                const copy = [...resumeData.experience];
                                copy[idx].role = e.target.value;
                                setResumeData({ ...resumeData, experience: copy });
                              }}
                              placeholder="e.g. Software Engineer II"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Start Date</label>
                            <input
                              type="text"
                              value={exp.startDate}
                              onChange={(e) => {
                                const copy = [...resumeData.experience];
                                copy[idx].startDate = e.target.value;
                                setResumeData({ ...resumeData, experience: copy });
                              }}
                              placeholder="e.g. Jul 2022"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">End Date</label>
                            <input
                              type="text"
                              value={exp.endDate}
                              onChange={(e) => {
                                const copy = [...resumeData.experience];
                                copy[idx].endDate = e.target.value;
                                setResumeData({ ...resumeData, experience: copy });
                              }}
                              placeholder="e.g. Present"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>
                        </div>

                        {/* Bullet Points */}
                        <div className="space-y-1.5 pt-1">
                          <label className="text-[11px] font-bold text-slate-700 block">
                            Bullet Points (One per line, STAR format)
                          </label>
                          <textarea
                            rows={3}
                            value={exp.responsibilities.join("\n")}
                            onChange={(e) => {
                              const copy = [...resumeData.experience];
                              copy[idx].responsibilities = e.target.value.split("\n").filter(Boolean);
                              setResumeData({ ...resumeData, experience: copy });
                            }}
                            placeholder="- Architected high-throughput microservices handling 50k requests/sec&#10;- Reduced API latency by 35% using Redis caching"
                            className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                          />
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* STEP 5: Internships */}
              {currentStep === 5 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                    <div>
                      <h3 className="text-sm font-black text-[#17233F]">5. Internships & Fellowships</h3>
                      <p className="text-xs text-slate-500">Add industry internships, research apprenticeships, or co-ops.</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        const newInt: InternshipEntry = {
                          id: `int-${Date.now()}`,
                          organization: "",
                          role: "",
                          duration: "",
                          workPerformed: [""],
                          achievements: [],
                        };
                        setResumeData({
                          ...resumeData,
                          internships: [...resumeData.internships, newInt],
                        });
                      }}
                      className="btn-violet px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1 cursor-pointer"
                    >
                      <Plus className="w-3.5 h-3.5" /> Add Internship
                    </button>
                  </div>

                  {resumeData.internships.length === 0 ? (
                    <div className="p-8 text-center border-2 border-dashed border-slate-200 rounded-2xl space-y-2">
                      <Zap className="w-8 h-8 text-slate-300 mx-auto" />
                      <p className="text-xs font-bold text-slate-600">No internship entries added yet.</p>
                      <p className="text-[11px] text-slate-400">
                        Optional section: click &quot;Add Internship&quot; if applicable, or proceed to Projects.
                      </p>
                    </div>
                  ) : (
                    resumeData.internships.map((intEntry, idx) => (
                      <div
                        key={intEntry.id}
                        className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3 relative group"
                      >
                        <div className="flex items-center justify-between border-b border-slate-200/60 pb-2">
                          <span className="text-xs font-black text-[#17233F]">Internship #{idx + 1}</span>
                          <div className="flex items-center gap-1">
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  internships: moveItem(resumeData.internships, idx, "up"),
                                })
                              }
                              disabled={idx === 0}
                              className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-20 cursor-pointer"
                              title="Move Up"
                            >
                              <ArrowUp className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  internships: moveItem(resumeData.internships, idx, "down"),
                                })
                              }
                              disabled={idx === resumeData.internships.length - 1}
                              className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-20 cursor-pointer"
                              title="Move Down"
                            >
                              <ArrowDown className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  internships: resumeData.internships.filter((_, i) => i !== idx),
                                })
                              }
                              className="p-1 text-rose-500 hover:text-rose-700 cursor-pointer"
                              title="Delete Internship"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Organization *</label>
                            <input
                              type="text"
                              value={intEntry.organization}
                              onChange={(e) => {
                                const copy = [...resumeData.internships];
                                copy[idx].organization = e.target.value;
                                setResumeData({ ...resumeData, internships: copy });
                              }}
                              placeholder="e.g. Amazon / Start-up"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Role *</label>
                            <input
                              type="text"
                              value={intEntry.role}
                              onChange={(e) => {
                                const copy = [...resumeData.internships];
                                copy[idx].role = e.target.value;
                                setResumeData({ ...resumeData, internships: copy });
                              }}
                              placeholder="e.g. Software Engineering Intern"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div className="sm:col-span-2">
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Duration</label>
                            <input
                              type="text"
                              value={intEntry.duration}
                              onChange={(e) => {
                                const copy = [...resumeData.internships];
                                copy[idx].duration = e.target.value;
                                setResumeData({ ...resumeData, internships: copy });
                              }}
                              placeholder="e.g. May 2023 - Jul 2023 (3 Months)"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>
                        </div>

                        <div>
                          <label className="text-[11px] font-bold text-slate-700 block mb-0.5">
                            Work Performed & Impact (One per line)
                          </label>
                          <textarea
                            rows={3}
                            value={intEntry.workPerformed.join("\n")}
                            onChange={(e) => {
                              const copy = [...resumeData.internships];
                              copy[idx].workPerformed = e.target.value.split("\n").filter(Boolean);
                              setResumeData({ ...resumeData, internships: copy });
                            }}
                            placeholder="- Built an automated data pipeline using Python and AWS Lambda&#10;- Delivered feature demo directly to engineering leadership"
                            className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                          />
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* STEP 6: Projects */}
              {currentStep === 6 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                    <div>
                      <h3 className="text-sm font-black text-[#17233F]">6. Notable Projects</h3>
                      <p className="text-xs text-slate-500">Showcase technical projects, GitHub repositories, and live links.</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        const newProj: ProjectEntry = {
                          id: `proj-${Date.now()}`,
                          title: "",
                          description: "",
                          technologies: [],
                          contributions: [""],
                          githubUrl: "",
                          projectUrl: "",
                        };
                        setResumeData({
                          ...resumeData,
                          projects: [...resumeData.projects, newProj],
                        });
                      }}
                      className="btn-violet px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1 cursor-pointer"
                    >
                      <Plus className="w-3.5 h-3.5" /> Add Project
                    </button>
                  </div>

                  {resumeData.projects.length === 0 ? (
                    <div className="p-8 text-center border-2 border-dashed border-slate-200 rounded-2xl space-y-2">
                      <FolderGit2 className="w-8 h-8 text-slate-300 mx-auto" />
                      <p className="text-xs font-bold text-slate-600">No projects added yet.</p>
                      <p className="text-[11px] text-slate-400">Click &quot;Add Project&quot; above to add your key technical projects.</p>
                    </div>
                  ) : (
                    resumeData.projects.map((proj, idx) => (
                      <div
                        key={proj.id}
                        className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3 relative group"
                      >
                        <div className="flex items-center justify-between border-b border-slate-200/60 pb-2">
                          <span className="text-xs font-black text-[#17233F]">Project #{idx + 1}</span>
                          <div className="flex items-center gap-1">
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  projects: moveItem(resumeData.projects, idx, "up"),
                                })
                              }
                              disabled={idx === 0}
                              className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-20 cursor-pointer"
                              title="Move Up"
                            >
                              <ArrowUp className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  projects: moveItem(resumeData.projects, idx, "down"),
                                })
                              }
                              disabled={idx === resumeData.projects.length - 1}
                              className="p-1 text-slate-400 hover:text-slate-700 disabled:opacity-20 cursor-pointer"
                              title="Move Down"
                            >
                              <ArrowDown className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={() =>
                                setResumeData({
                                  ...resumeData,
                                  projects: resumeData.projects.filter((_, i) => i !== idx),
                                })
                              }
                              className="p-1 text-rose-500 hover:text-rose-700 cursor-pointer"
                              title="Delete Project"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Project Title *</label>
                            <input
                              type="text"
                              value={proj.title}
                              onChange={(e) => {
                                const copy = [...resumeData.projects];
                                copy[idx].title = e.target.value;
                                setResumeData({ ...resumeData, projects: copy });
                              }}
                              placeholder="e.g. Neural Search Engine"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Technologies Used</label>
                            <input
                              type="text"
                              value={proj.technologies.join(", ")}
                              onChange={(e) => {
                                const copy = [...resumeData.projects];
                                copy[idx].technologies = e.target.value
                                  .split(",")
                                  .map((s) => s.trim())
                                  .filter(Boolean);
                                setResumeData({ ...resumeData, projects: copy });
                              }}
                              placeholder="Python, FastAPI, PyTorch, React"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">GitHub URL</label>
                            <input
                              type="text"
                              value={proj.githubUrl || ""}
                              onChange={(e) => {
                                const copy = [...resumeData.projects];
                                copy[idx].githubUrl = e.target.value;
                                setResumeData({ ...resumeData, projects: copy });
                              }}
                              placeholder="https://github.com/user/project"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>

                          <div>
                            <label className="text-[11px] font-bold text-slate-700 block mb-0.5">Live Demo URL</label>
                            <input
                              type="text"
                              value={proj.projectUrl || ""}
                              onChange={(e) => {
                                const copy = [...resumeData.projects];
                                copy[idx].projectUrl = e.target.value;
                                setResumeData({ ...resumeData, projects: copy });
                              }}
                              placeholder="https://project-demo.vercel.app"
                              className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                            />
                          </div>
                        </div>

                        <div>
                          <label className="text-[11px] font-bold text-slate-700 block mb-0.5">
                            Key Features & Bullet Points (One per line)
                          </label>
                          <textarea
                            rows={3}
                            value={proj.contributions.join("\n")}
                            onChange={(e) => {
                              const copy = [...resumeData.projects];
                              copy[idx].contributions = e.target.value.split("\n").filter(Boolean);
                              setResumeData({ ...resumeData, projects: copy });
                            }}
                            placeholder="- Built semantic embedding pipeline with cosine similarity search&#10;- Designed responsive UI with dark/light themes"
                            className="w-full px-2.5 py-1.5 rounded-lg border text-xs bg-white"
                          />
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* STEP 7: Certifications & Additional Sections */}
              {currentStep === 7 && (
                <div className="space-y-4">
                  <div className="border-b border-slate-100 pb-2">
                    <h3 className="text-sm font-black text-[#17233F]">7. Certifications & Additional Sections</h3>
                    <p className="text-xs text-slate-500">
                      Add verified credentials, honors, hackathons, publications, and languages.
                    </p>
                  </div>

                  {/* Certifications List */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <label className="text-xs font-bold text-slate-700">Certificates & Licenses</label>
                      <button
                        type="button"
                        onClick={() => {
                          const newCert: CertificationEntry = {
                            id: `cert-${Date.now()}`,
                            name: "",
                            issuingOrganization: "",
                            issueDate: "",
                          };
                          setResumeData({
                            ...resumeData,
                            certifications: [...resumeData.certifications, newCert],
                          });
                        }}
                        className="text-[11px] font-bold text-[#7355D9] flex items-center gap-1 cursor-pointer"
                      >
                        <Plus className="w-3.5 h-3.5" /> Add Certificate
                      </button>
                    </div>

                    {resumeData.certifications.length === 0 ? (
                      <p className="text-[11px] text-slate-400 italic">No certifications added. (Optional)</p>
                    ) : (
                      resumeData.certifications.map((c, i) => (
                        <div key={c.id} className="flex gap-2 items-center">
                          <input
                            type="text"
                            value={c.name}
                            onChange={(e) => {
                              const copy = [...resumeData.certifications];
                              copy[i].name = e.target.value;
                              setResumeData({ ...resumeData, certifications: copy });
                            }}
                            placeholder="e.g. AWS Certified Solutions Architect"
                            className="flex-1 px-2.5 py-1.5 rounded-lg border text-xs"
                          />
                          <input
                            type="text"
                            value={c.issuingOrganization}
                            onChange={(e) => {
                              const copy = [...resumeData.certifications];
                              copy[i].issuingOrganization = e.target.value;
                              setResumeData({ ...resumeData, certifications: copy });
                            }}
                            placeholder="Issuer (e.g. Amazon)"
                            className="w-32 px-2.5 py-1.5 rounded-lg border text-xs"
                          />
                          <input
                            type="text"
                            value={c.issueDate}
                            onChange={(e) => {
                              const copy = [...resumeData.certifications];
                              copy[i].issueDate = e.target.value;
                              setResumeData({ ...resumeData, certifications: copy });
                            }}
                            placeholder="Year"
                            className="w-20 px-2.5 py-1.5 rounded-lg border text-xs"
                          />
                          <button
                            type="button"
                            onClick={() => {
                              setResumeData({
                                ...resumeData,
                                certifications: resumeData.certifications.filter((_, idx) => idx !== i),
                              });
                            }}
                            className="text-rose-500 hover:text-rose-700 p-1"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      ))
                    )}
                  </div>

                  {/* Key Achievements */}
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-slate-700 block">
                      Key Honors & Achievements (One per line)
                    </label>
                    <textarea
                      rows={2}
                      value={resumeData.additional.achievements.join("\n")}
                      onChange={(e) =>
                        setResumeData({
                          ...resumeData,
                          additional: {
                            ...resumeData.additional,
                            achievements: e.target.value.split("\n").filter(Boolean),
                          },
                        })
                      }
                      placeholder="- 1st place in Smart India Hackathon 2023&#10;- Top 5% in LeetCode Global Contest"
                      className="w-full px-3 py-2 rounded-xl border text-xs"
                    />
                  </div>

                  {/* Publications */}
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-slate-700 block">
                      Publications & Research Papers (One per line)
                    </label>
                    <textarea
                      rows={2}
                      value={resumeData.additional.publications.join("\n")}
                      onChange={(e) =>
                        setResumeData({
                          ...resumeData,
                          additional: {
                            ...resumeData.additional,
                            publications: e.target.value.split("\n").filter(Boolean),
                          },
                        })
                      }
                      placeholder="- Author, Title of Paper, Journal / Conference Name (Year)"
                      className="w-full px-3 py-2 rounded-xl border text-xs"
                    />
                  </div>

                  {/* Languages */}
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-slate-700 block">
                      Languages (Comma-separated)
                    </label>
                    <input
                      type="text"
                      value={resumeData.additional.languages.join(", ")}
                      onChange={(e) =>
                        setResumeData({
                          ...resumeData,
                          additional: {
                            ...resumeData.additional,
                            languages: e.target.value.split(",").map((s) => s.trim()).filter(Boolean),
                          },
                        })
                      }
                      placeholder="English (Fluent), Hindi (Native), Spanish (Basic)"
                      className="w-full px-3 py-2 rounded-xl border text-xs"
                    />
                  </div>
                </div>
              )}

              {/* Stepper Navigation Controls */}
              <div className="flex items-center justify-between border-t border-slate-100 pt-4">
                <button
                  type="button"
                  disabled={currentStep === 1}
                  onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
                  className="px-3.5 py-1.5 rounded-xl border text-xs font-bold text-slate-600 disabled:opacity-30 flex items-center gap-1 cursor-pointer"
                >
                  <ChevronLeft className="w-3.5 h-3.5" /> Previous
                </button>

                <div className="text-xs font-bold text-slate-400">
                  Step {currentStep} of {formSteps.length}
                </div>

                {currentStep < formSteps.length ? (
                  <button
                    type="button"
                    onClick={() => setCurrentStep(currentStep + 1)}
                    className="btn-violet px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-1 cursor-pointer"
                  >
                    <span>Next</span> <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={() => setPhase("review")}
                    className="px-5 py-2 rounded-xl text-xs font-bold bg-[#17233F] hover:bg-[#202E4E] text-[#F0D99B] flex items-center gap-2 shadow-md transition-all cursor-pointer"
                  >
                    <span>Review Information</span>
                    <ArrowRight className="w-4 h-4 text-[#F0D99B]" />
                  </button>
                )}
              </div>
            </div>
          </div>
        )}

        {/* PHASE 2: REVIEW & VALIDATION (Step 8) */}
        {phase === "review" && (
          <ResumeReviewStep
            resume={resumeData}
            onEditStep={(stepNum) => {
              setCurrentStep(stepNum);
              setPhase("wizard");
            }}
            onBackToStep7={() => {
              setCurrentStep(7);
              setPhase("wizard");
            }}
            onGenerateAI={handleAIGenerateFull}
            isGenerating={isGeneratingAI}
          />
        )}

        {/* PHASE 3: 1000+ DESIGN GALLERY */}
        {phase === "gallery" && (
          <DesignGallery
            resume={resumeData}
            selectedDesignId={selectedDesign.id}
            onSelectDesign={(d) => setSelectedDesign(d)}
            onContinueToStudio={() => setPhase("studio")}
            onBackToEdit={() => setPhase("review")}
          />
        )}

        {/* PHASE 4: FINAL RESUME STUDIO */}
        {phase === "studio" && (
          <ResumeStudio
            resume={resumeData}
            design={selectedDesign}
            onChangeDesign={(d) => setSelectedDesign(d)}
            onUpdateResume={(updated) => setResumeData(updated)}
            onBackToGallery={() => setPhase("gallery")}
            onBackToForm={() => {
              setCurrentStep(1);
              setPhase("wizard");
            }}
          />
        )}

        {/* Modal: Saved Resumes */}
        {showSavedModal && (
          <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-slate-200">
              <div className="flex items-center justify-between border-b pb-3">
                <h3 className="text-sm font-black text-[#17233F] flex items-center gap-2">
                  <FolderOpen className="w-4 h-4 text-[#7355D9]" /> Saved Portfolios ({savedResumesList.length})
                </h3>
                <button
                  onClick={() => setShowSavedModal(false)}
                  className="text-slate-400 hover:text-slate-700"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {savedResumesList.length === 0 ? (
                <div className="py-8 text-center text-xs text-slate-500 space-y-1">
                  <Info className="w-6 h-6 text-slate-300 mx-auto" />
                  <p>No saved resumes found in database.</p>
                  <p className="text-[11px] text-slate-400">Save your resume in the Studio to view it here anytime.</p>
                </div>
              ) : (
                <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                  {savedResumesList.map((doc) => (
                    <div
                      key={doc.id}
                      className="p-3 rounded-2xl bg-slate-50 hover:bg-[#FBF8F1] border border-slate-200 hover:border-[#D6A84B] transition-all flex items-center justify-between text-xs"
                    >
                      <div>
                        <div className="font-bold text-[#17233F]">{doc.title}</div>
                        <div className="text-[10px] text-slate-400">
                          Created {new Date(doc.created_at).toLocaleDateString()}
                        </div>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <button
                          onClick={async () => {
                            try {
                              const res = await apiService.getResumeJson(doc.id);
                              if (res.data) {
                                setResumeData(res.data);
                                setActiveResumeId(doc.id);
                                setShowSavedModal(false);
                                setPhase("studio");
                                toast.success(`Loaded saved resume: ${doc.title}`);
                              }
                            } catch (err: any) {
                              toast.error(`Failed to load: ${err.message}`);
                            }
                          }}
                          className="px-2.5 py-1 rounded-lg bg-[#17233F] text-white font-bold text-[11px] hover:bg-[#202E4E] cursor-pointer"
                        >
                          Open in Studio
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
