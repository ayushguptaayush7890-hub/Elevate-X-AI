"use client";

import React, { useState, useRef } from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/AppShell";
import { GlassCard } from "@/components/ui/GlassCard";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import {
  FileText,
  Upload,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ArrowRight,
  ShieldCheck,
  RefreshCw,
  Download,
  Printer,
  ChevronRight,
  Search,
  Check,
  X,
  HelpCircle,
  Briefcase,
  GraduationCap,
  Layers,
  BarChart3,
  Cpu,
  FileCheck2,
} from "lucide-react";
import { ResumeFullData } from "@/types/resume-generator";

const EMPTY_RESUME: ResumeFullData = {
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
  skills: {
    programmingLanguages: [],
    frameworks: [],
    databases: [],
    developerTools: [],
    aiMlSkills: [],
    otherSkills: [],
  },
  education: [],
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
  templateId: "ats_friendly",
  accentColor: "#17233F",
  typography: "sans",
  spacing: "normal",
};

const SAMPLE_JOB_DESCRIPTIONS = [
  {
    title: "Senior Full Stack Engineer",
    company: "TechCorp Global",
    text: `Job Title: Senior Full Stack Engineer
Seniority: Senior
Location: Remote / Hybrid

About Us:
TechCorp Global builds enterprise-scale cloud microservices powering mission-critical workflows.

Requirements:
- 5+ years of experience in full-stack software development
- Strong proficiency in TypeScript, React, Next.js, and Node.js
- In-depth hands-on experience with Python, FastAPI, and PostgreSQL
- Demonstrated experience architecting RESTful and GraphQL APIs
- Proficient in Docker, containerization, and CI/CD pipelines
- Bachelor's or Master's degree in Computer Science, Software Engineering, or equivalent experience

Preferred Qualifications:
- Experience with Kubernetes orchestration and AWS cloud infrastructure
- Familiarity with Redis caching and distributed task queues
- Prior experience optimizing database queries and reducing p99 latency

Responsibilities:
- Architect and develop scalable web applications with sub-100ms response times
- Spearhead technical initiatives across front-end rendering and backend services
- Collaborate with product designers and engineers to deliver robust features
- Mentor junior engineers and champion rigorous automated testing practices`
  },
  {
    title: "AI / Machine Learning Engineer",
    company: "NeuralDynamics AI",
    text: `Job Title: AI / Machine Learning Engineer
Seniority: Mid-Senior
Location: San Francisco, CA / Remote

Overview:
NeuralDynamics builds next-generation generative AI and natural language processing applications.

Requirements:
- Strong programming proficiency in Python, PyTorch, and Hugging Face Transformers
- Experience training and fine-tuning neural networks (NLP, classification, LLMs)
- Solid understanding of linear algebra, calculus, and probability
- Hands-on experience building model evaluation pipelines and computing metrics (F1, nDCG, accuracy)
- Bachelor's or Master's degree in Computer Science, Data Science, or related field

Preferred Qualifications:
- Experience with Apple MLX, ONNX, or TensorRT model quantization and inference acceleration
- Familiarity with vector databases, semantic search, and retrieval-augmented generation (RAG)
- Track record of open-source contributions or research publications

Responsibilities:
- Train, fine-tune, and deploy instruction-following language models
- Design rigorous evaluation benchmarks to measure model performance and latency
- Implement semantic search and document parsing microservices
- Collaborate with backend engineers to integrate ML models into production APIs`
  },
  {
    title: "Senior AI & Full Stack Machine Learning Engineer",
    company: "Elevate NextGen AI",
    text: `Job Title: Senior AI & Full Stack Machine Learning Engineer
Seniority: Senior
Location: Remote

Overview:
Build cutting-edge generative AI, RAG systems, and scalable full-stack applications.

Requirements:
- Strong programming proficiency in Python and C++
- Solid foundation in Machine Learning and Deep Learning architectures
- Hands-on experience developing LLM and RAG pipelines
- Deep expertise in NLP (Natural Language Processing) and Computer Vision
- Backend API development using Flask and FastAPI
- Deep learning frameworks including PyTorch and TensorFlow
- Numerical computing and data manipulation with NumPy and Pandas
- Containerization and deployment using Docker
- API testing and contract validation with Postman
- Frontend web development using React.js and backend services with Node.js
- Relational database management with SQL
- Version control and collaborative development via Git and GitHub
- Strong background in Data Structures and Algorithms

Preferred Qualifications:
- Experience with Scikit-learn and automated evaluation pipelines
- Familiarity with cloud platforms such as AWS or GCP
- Continuous integration and deployment (CI/CD)

Key Responsibilities:
- Design, train, and deploy production machine learning models and LLM solutions
- Develop high-performance REST APIs and integrate backend microservices
- Build responsive interactive dashboards and frontend components
- Optimize model latency, throughput, and system resource utilization
- Collaborate in agile cross-functional engineering teams

Educational Requirements:
- Bachelor's or Master's degree in Computer Science, Data Science, or related engineering discipline`
  }
];

export default function ATSCheckerPage() {
  // Step workflow
  const [activeTab, setActiveTab] = useState<"upload" | "jd" | "match" | "improve">("upload");

  // Ingested resume state - starts with clean authentic empty state (NO preset candidates)
  const [resumeData, setResumeData] = useState<ResumeFullData>(EMPTY_RESUME);
  const [hasUploadedResume, setHasUploadedResume] = useState(false);
  const [parsedDocInfo, setParsedDocInfo] = useState<any>(null);
  const [uploadLoading, setUploadLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Job description state
  const [jobTitle, setJobTitle] = useState("Senior Full Stack Engineer");
  const [jdText, setJdText] = useState(SAMPLE_JOB_DESCRIPTIONS[0].text);
  const [jdAnalysis, setJdAnalysis] = useState<any>(null);
  const [analyzingJd, setAnalyzingJd] = useState(false);

  // ATS Matching state
  const [matchLoading, setMatchLoading] = useState(false);
  const [matchResult, setMatchResult] = useState<any>(null);
  const [gapFilter, setGapFilter] = useState<"all" | "explicit" | "partial" | "not_found" | "uncertain">("all");

  // AI Improvements state
  const [improveLoading, setImproveLoading] = useState(false);
  const [improvements, setImprovements] = useState<any[]>([]);
  const [targetedQuestions, setTargetedQuestions] = useState<string[]>([]);
  const [acceptedIds, setAcceptedIds] = useState<Set<string>>(new Set());
  const [rejectedIds, setRejectedIds] = useState<Set<string>>(new Set());

  // Handle File Upload - Ingest authentic document directly into active candidate state
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadLoading(true);
    try {
      toast.info(`Parsing ${file.name} with neural section segmenter...`);
      const parsed = await apiService.uploadResumeFile(file);
      setParsedDocInfo(parsed);
      setHasUploadedResume(true);

      // Hydrate candidate data solely from parsed document with zero preset mixing
      if (parsed.structuredResume) {
        setResumeData(parsed.structuredResume);
      } else {
        const newResume: ResumeFullData = {
          ...EMPTY_RESUME,
          personalInfo: {
            fullName: parsed.personalInfo?.fullName || "Candidate",
            professionalTitle: parsed.personalInfo?.professionalTitle || "",
            email: parsed.personalInfo?.email || "",
            phone: parsed.personalInfo?.phone || "",
            location: parsed.personalInfo?.location || "",
            linkedIn: parsed.personalInfo?.linkedIn || "",
            gitHub: parsed.personalInfo?.gitHub || "",
            portfolio: parsed.personalInfo?.portfolio || "",
            summary: parsed.personalInfo?.summary || "",
          },
          skills: parsed.categorizedSkills || EMPTY_RESUME.skills,
          education: parsed.education || [],
          experience: parsed.experience || [],
          internships: parsed.internships || [],
          projects: parsed.projects || [],
          certifications: parsed.certifications || [],
        };
        setResumeData(newResume);
      }

      // Reset previous analysis for session isolation
      setMatchResult(null);
      setJdAnalysis(null);
      setImprovements([]);
      setTargetedQuestions([]);

      toast.success(`Successfully parsed ${parsed.documentMetadata?.totalLines || 0} lines for ${parsed.personalInfo?.fullName || "candidate"}!`);
      setActiveTab("jd");
    } catch (err: any) {
      toast.error(err.message || "Failed to parse document");
    } finally {
      setUploadLoading(false);
    }
  };

  // Analyze Job Description
  const handleAnalyzeJD = async () => {
    if (!jdText.trim() || jdText.length < 20) {
      toast.error("Please enter a comprehensive job description (at least 20 characters).");
      return;
    }
    setAnalyzingJd(true);
    try {
      const res = await apiService.analyzeJobDescription(jdText, jobTitle);
      setJdAnalysis(res);
      toast.success(`Job analyzed: ${res.requiredSkills.length} required skills, ${res.keyResponsibilities.length} responsibilities identified.`);
      setActiveTab("match");
      runATSMatch(res);
    } catch (err: any) {
      toast.error(err.message || "Failed to analyze job description");
    } finally {
      setAnalyzingJd(false);
    }
  };

  // Run Semantic ATS Match
  const runATSMatch = async (customAnalysis?: any) => {
    setMatchLoading(true);
    try {
      const res = await apiService.matchResumeAts({
        resumeData: resumeData,
        parsedResume: parsedDocInfo,
        jobDescription: jdText,
        jobTitle: jobTitle
      });
      setMatchResult(res);
      toast.success(`ATS Audit Complete: Overall Score ${res.overallScore}/100`);
    } catch (err: any) {
      toast.error(err.message || "Failed to calculate ATS match");
    } finally {
      setMatchLoading(false);
    }
  };

  // Run AI Improvements
  const handleGenerateImprovements = async () => {
    setImproveLoading(true);
    try {
      const missingList = (matchResult?.missingRequirements || []).map((m: any) => m.requirement);
      const res = await apiService.improveResumeAts({
        resumeData: resumeData,
        jobDescription: jdText,
        gapRequirements: missingList,
      });
      setImprovements(res.suggestions || []);
      setTargetedQuestions(res.targetedQuestions || []);
      toast.success(`Generated ${res.suggestions?.length || 0} grounded STAR improvements.`);
      setActiveTab("improve");
    } catch (err: any) {
      toast.error(err.message || "Failed to generate AI improvements");
    } finally {
      setImproveLoading(false);
    }
  };

  // Accept a STAR suggestion
  const handleAcceptSuggestion = (sug: any) => {
    setAcceptedIds(prev => new Set(prev).add(sug.id));
    setRejectedIds(prev => {
      const next = new Set(prev);
      next.delete(sug.id);
      return next;
    });

    // Patch the resume in-memory
    const updatedExp = resumeData.experience.map(exp => ({
      ...exp,
      responsibilities: exp.responsibilities.map(r => r === sug.originalText ? sug.suggestedText : r)
    }));
    const updatedProj = resumeData.projects.map(p => ({
      ...p,
      contributions: p.contributions.map(c => c === sug.originalText ? sug.suggestedText : c)
    }));

    setResumeData({
      ...resumeData,
      experience: updatedExp,
      projects: updatedProj,
    });
    toast.success("Applied elevated STAR bullet to active resume!");
  };

  // Reject a STAR suggestion
  const handleRejectSuggestion = (sugId: string) => {
    setRejectedIds(prev => new Set(prev).add(sugId));
    setAcceptedIds(prev => {
      const next = new Set(prev);
      next.delete(sugId);
      return next;
    });
    toast.info("Suggestion dismissed.");
  };

  // Export DOCX
  const handleExportDocx = async () => {
    try {
      const candidateName = resumeData?.personalInfo?.fullName?.trim() || "Candidate";
      toast.info("Generating ATS-Optimized Word Document (.docx)...");
      const exportPayload: ResumeFullData = {
        ...resumeData,
        personalInfo: {
          ...resumeData.personalInfo,
          fullName: candidateName,
          professionalTitle: resumeData?.personalInfo?.professionalTitle || "",
          email: resumeData?.personalInfo?.email || "",
          phone: resumeData?.personalInfo?.phone || "",
          location: resumeData?.personalInfo?.location || "",
          summary: resumeData?.personalInfo?.summary || "",
        },
        templateId: resumeData?.templateId || "ats_friendly",
        accentColor: resumeData?.accentColor || "#17233F",
        typography: resumeData?.typography || "sans",
        spacing: resumeData?.spacing || "normal",
      };
      const blob = await apiService.exportResumeDocx(exportPayload);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const safeName = candidateName.replace(/[^a-zA-Z0-9_\.-]/g, "_");
      a.download = `${safeName}_ATS_Optimized.docx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success("Downloaded DOCX successfully!");
    } catch (err: any) {
      toast.error(err.message || "DOCX generation failed");
    }
  };

  return (
    <AppShell>
      <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Top Header & Navigation Banner */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border/40 pb-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-2">
              <Cpu className="w-3.5 h-3.5" />
              Feature 3: Resume Intelligence & ATS Matching
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
              AI ATS Audit & Resume Optimization
            </h1>
            <p className="text-sm text-muted-foreground mt-1">
              Upload your PDF/DOCX resume, evaluate against target job descriptions with mathematical precision, and elevate with grounded STAR improvements.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/resume"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-border/80 bg-card/60 hover:bg-card text-xs font-semibold transition"
            >
              <Layers className="w-4 h-4 text-primary" />
              Resume Builder Studio
            </Link>
            <button
              onClick={handleExportDocx}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold shadow hover:bg-primary/90 transition"
            >
              <Download className="w-4 h-4" />
              Export ATS DOCX
            </button>
          </div>
        </div>

        {/* Phase Navigation Tabs */}
        <div className="flex border-b border-border/60 gap-2 overflow-x-auto pb-1">
          <button
            onClick={() => setActiveTab("upload")}
            className={`px-4 py-2.5 rounded-t-lg text-xs font-bold transition flex items-center gap-2 ${
              activeTab === "upload"
                ? "bg-primary/15 text-primary border-b-2 border-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Upload className="w-4 h-4" />
            1. Ingest Resume (PDF / DOCX)
          </button>
          <button
            onClick={() => setActiveTab("jd")}
            className={`px-4 py-2.5 rounded-t-lg text-xs font-bold transition flex items-center gap-2 ${
              activeTab === "jd"
                ? "bg-primary/15 text-primary border-b-2 border-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Briefcase className="w-4 h-4" />
            2. Target Job Description
          </button>
          <button
            onClick={() => {
              setActiveTab("match");
              if (!matchResult) runATSMatch();
            }}
            className={`px-4 py-2.5 rounded-t-lg text-xs font-bold transition flex items-center gap-2 ${
              activeTab === "match"
                ? "bg-primary/15 text-primary border-b-2 border-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            3. Semantic ATS Match & Scores
            {matchResult && (
              <span className="px-1.5 py-0.5 rounded-full text-[10px] bg-primary text-primary-foreground font-black">
                {matchResult.overallScore}
              </span>
            )}
          </button>
          <button
            onClick={() => {
              setActiveTab("improve");
              if (improvements.length === 0) handleGenerateImprovements();
            }}
            className={`px-4 py-2.5 rounded-t-lg text-xs font-bold transition flex items-center gap-2 ${
              activeTab === "improve"
                ? "bg-primary/15 text-primary border-b-2 border-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Sparkles className="w-4 h-4" />
            4. AI STAR Elevation & Gap Prompts
          </button>
        </div>

        {/* ========================================================================= */}
        {/* TAB 1: RESUME INGESTION & DOCUMENT PARSING */}
        {/* ========================================================================= */}
        {activeTab === "upload" && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-6 space-y-6">
              <GlassCard className="p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-base font-bold text-foreground flex items-center gap-2">
                      <FileCheck2 className="w-4 h-4 text-primary" />
                      Upload Existing Resume
                    </h2>
                    <p className="text-xs text-muted-foreground">
                      Upload your PDF or DOCX file to extract text with neural section classification.
                    </p>
                  </div>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-600 font-semibold">
                    MPS Neural Model Active
                  </span>
                </div>

                {/* Upload Drag Drop Area */}
                <div
                  onClick={() => fileInputRef.current?.click()}
                  className="border-2 border-dashed border-border/80 hover:border-primary/60 rounded-2xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition bg-card/40 hover:bg-card/70 group"
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf,.docx"
                    className="hidden"
                    onChange={handleFileUpload}
                  />
                  <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center text-primary group-hover:scale-110 transition mb-3">
                    <Upload className="w-6 h-6" />
                  </div>
                  <p className="text-sm font-semibold text-foreground">
                    Click to select or drag and drop your resume
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Accepts native PDF or DOCX files up to 15MB
                  </p>
                </div>

                {uploadLoading && (
                  <div className="p-4 rounded-xl bg-primary/5 border border-primary/20 flex items-center gap-3">
                    <RefreshCw className="w-5 h-5 text-primary animate-spin" />
                    <div>
                      <p className="text-xs font-semibold text-foreground">Parsing document structure...</p>
                      <p className="text-[11px] text-muted-foreground">Running ResumeSectionNeuralClassifier on Apple Silicon Metal.</p>
                    </div>
                  </div>
                )}

                {/* Real-time Ingestion Security Verification */}
                <div className="pt-4 border-t border-border/40 text-[11px] text-muted-foreground space-y-1.5">
                  <div className="flex items-center gap-1.5 text-foreground font-semibold">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                    Authentic Ingestion Pipeline
                  </div>
                  <p>
                    All entities are parsed verbatim from your uploaded document via stream text extraction and neural section classification. Preset demo candidates have been completely disabled.
                  </p>
                </div>
              </GlassCard>
            </div>

            {/* Ingestion & Extracted Profile Preview */}
            <div className="lg:col-span-6 space-y-6">
              <GlassCard className="p-6 space-y-4">
                <div className="flex items-center justify-between border-b border-border/40 pb-3">
                  <div>
                    <h2 className="text-base font-bold text-foreground">Active Candidate Profile</h2>
                    <p className="text-xs text-muted-foreground">
                      Structured entity state extracted directly from your document.
                    </p>
                  </div>
                  {hasUploadedResume && (
                    <button
                      onClick={() => setActiveTab("jd")}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition"
                    >
                      Next: Job Description
                      <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>

                {!hasUploadedResume && !resumeData.personalInfo?.fullName ? (
                  <div className="text-center py-16 text-muted-foreground text-xs space-y-3">
                    <FileText className="w-12 h-12 mx-auto text-muted-foreground/30" />
                    <p className="font-semibold text-foreground text-sm">No Resume Ingested Yet</p>
                    <p className="max-w-xs mx-auto leading-relaxed">
                      Upload your PDF or DOCX file to extract verified candidate entities, review structured credentials, and proceed to the ATS semantic audit.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4 text-xs">
                    <div className="p-3 rounded-xl bg-card/50 border border-border/60 space-y-1">
                      <p className="text-sm font-bold text-foreground">{resumeData.personalInfo.fullName || "Candidate"}</p>
                      {resumeData.personalInfo.professionalTitle && (
                        <p className="text-muted-foreground font-medium">{resumeData.personalInfo.professionalTitle}</p>
                      )}
                      <div className="flex flex-wrap gap-3 text-muted-foreground text-[11px] pt-1">
                        {resumeData.personalInfo.email && <span>{resumeData.personalInfo.email}</span>}
                        {resumeData.personalInfo.phone && <span>• {resumeData.personalInfo.phone}</span>}
                        {resumeData.personalInfo.location && <span>• {resumeData.personalInfo.location}</span>}
                      </div>
                    </div>

                    {/* Candidate Skills Inventory - Complete Dynamic Categorized View */}
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <p className="font-semibold text-foreground flex items-center gap-1.5">
                          <Sparkles className="w-3.5 h-3.5 text-primary" />
                          Candidate Skills Inventory ({
                            (resumeData?.skills?.programmingLanguages?.length || 0) +
                            (resumeData?.skills?.aiMlSkills?.length || 0) +
                            (resumeData?.skills?.frameworks?.length || 0) +
                            (resumeData?.skills?.databases?.length || 0) +
                            (resumeData?.skills?.developerTools?.length || 0) +
                            (resumeData?.skills?.otherSkills?.length || 0)
                          } extracted skills):
                        </p>
                      </div>

                      <div className="space-y-2 text-xs">
                        {/* Programming Languages */}
                        {(resumeData?.skills?.programmingLanguages?.length || 0) > 0 && (
                          <div>
                            <span className="text-[10px] uppercase font-bold text-muted-foreground block mb-1">
                              Programming Languages ({resumeData.skills.programmingLanguages.length})
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeData.skills.programmingLanguages.map((s, idx) => (
                                <span key={idx} className="px-2 py-0.5 rounded-md bg-blue-500/10 text-blue-700 dark:text-blue-300 border border-blue-500/20 text-[11px] font-medium">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Machine Learning / AI */}
                        {(resumeData?.skills?.aiMlSkills?.length || 0) > 0 && (
                          <div>
                            <span className="text-[10px] uppercase font-bold text-muted-foreground block mb-1">
                              Machine Learning & AI ({resumeData.skills.aiMlSkills.length})
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeData.skills.aiMlSkills.map((s, idx) => (
                                <span key={idx} className="px-2 py-0.5 rounded-md bg-purple-500/10 text-purple-700 dark:text-purple-300 border border-purple-500/20 text-[11px] font-medium">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Frameworks & Libraries */}
                        {(resumeData?.skills?.frameworks?.length || 0) > 0 && (
                          <div>
                            <span className="text-[10px] uppercase font-bold text-muted-foreground block mb-1">
                              Frameworks & Libraries ({resumeData.skills.frameworks.length})
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeData.skills.frameworks.map((s, idx) => (
                                <span key={idx} className="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20 text-[11px] font-medium">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Databases */}
                        {(resumeData?.skills?.databases?.length || 0) > 0 && (
                          <div>
                            <span className="text-[10px] uppercase font-bold text-muted-foreground block mb-1">
                              Databases ({resumeData.skills.databases.length})
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeData.skills.databases.map((s, idx) => (
                                <span key={idx} className="px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20 text-[11px] font-medium">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Tools & Platforms */}
                        {(resumeData?.skills?.developerTools?.length || 0) > 0 && (
                          <div>
                            <span className="text-[10px] uppercase font-bold text-muted-foreground block mb-1">
                              Tools & Platforms ({resumeData.skills.developerTools.length})
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeData.skills.developerTools.map((s, idx) => (
                                <span key={idx} className="px-2 py-0.5 rounded-md bg-sky-500/10 text-sky-700 dark:text-sky-300 border border-sky-500/20 text-[11px] font-medium">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Other Skills */}
                        {(resumeData?.skills?.otherSkills?.length || 0) > 0 && (
                          <div>
                            <span className="text-[10px] uppercase font-bold text-muted-foreground block mb-1">
                              Other Technical Skills ({resumeData.skills.otherSkills.length})
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeData.skills.otherSkills.map((s, idx) => (
                                <span key={idx} className="px-2 py-0.5 rounded-md bg-secondary text-secondary-foreground text-[11px] font-medium">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Relevant Coursework */}
                        {((parsedDocInfo?.relevantCoursework?.length || 0) > 0 || (resumeData?.education?.[0]?.coursework?.length || 0) > 0) && (
                          <div>
                            <span className="text-[10px] uppercase font-bold text-muted-foreground block mb-1">
                              Academic Coursework ({parsedDocInfo?.relevantCoursework?.length || resumeData.education[0]?.coursework?.length})
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {(parsedDocInfo?.relevantCoursework || resumeData.education[0]?.coursework || []).map((s: string, idx: number) => (
                                <span key={idx} className="px-2 py-0.5 rounded-md bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 border border-indigo-500/20 text-[11px] font-medium">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Experience summary */}
                    <div>
                      <p className="font-semibold text-foreground mb-1.5 flex items-center gap-1.5">
                        <Briefcase className="w-3.5 h-3.5 text-primary" />
                        Work Experience ({resumeData?.experience?.length || 0} roles):
                      </p>
                      <div className="space-y-2">
                        {(resumeData?.experience || []).slice(0, 2).map((exp, idx) => (
                          <div key={idx} className="p-2.5 rounded-lg bg-card/40 border border-border/40">
                            <p className="font-bold text-foreground">{exp.role} <span className="font-normal text-muted-foreground">at {exp.company}</span></p>
                            <p className="text-[10px] text-muted-foreground">{exp.startDate} - {exp.endDate}</p>
                            <ul className="list-disc pl-4 mt-1 space-y-0.5 text-muted-foreground text-[11px]">
                              {(exp.responsibilities || []).slice(0, 2).map((r, rIdx) => (
                                <li key={rIdx}>{r}</li>
                              ))}
                            </ul>
                          </div>
                        ))}
                      </div>
                    </div>

                  {/* Source Evidence Lines if parsed from file */}
                  {parsedDocInfo?.evidenceLines && (
                    <div className="pt-2">
                      <p className="font-semibold text-foreground mb-1 flex items-center gap-1.5">
                        <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                        Verified Source Lines ({parsedDocInfo.documentMetadata?.totalLines} total):
                      </p>
                      <div className="max-h-36 overflow-y-auto space-y-1 font-mono text-[10px] p-2 bg-muted/40 rounded-lg border border-border/40">
                        {parsedDocInfo.evidenceLines.slice(0, 8).map((el: any, idx: number) => (
                          <div key={idx} className="flex gap-2">
                            <span className="text-muted-foreground select-none">L{el.line_num}:</span>
                            <span className="text-foreground">{el.text}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
                )}
              </GlassCard>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 2: TARGET JOB DESCRIPTION & AI ANALYSIS */}
        {/* ========================================================================= */}
        {activeTab === "jd" && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-7 space-y-6">
              <GlassCard className="p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-base font-bold text-foreground">Target Job Description</h2>
                    <p className="text-xs text-muted-foreground">
                      Paste the JD text to extract required skills, qualifications, and responsibilities.
                    </p>
                  </div>
                  {/* Preset JD buttons */}
                  <div className="flex gap-2">
                    {SAMPLE_JOB_DESCRIPTIONS.map((preset, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          setJobTitle(preset.title);
                          setJdText(preset.text);
                          toast.info(`Loaded sample JD: ${preset.title}`);
                        }}
                        className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-primary/10 text-primary hover:bg-primary/20 transition"
                      >
                        {preset.title.split(" ")[0]} Role
                      </button>
                    ))}
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-semibold text-muted-foreground block mb-1">
                      Target Role Title
                    </label>
                    <input
                      type="text"
                      value={jobTitle}
                      onChange={(e) => setJobTitle(e.target.value)}
                      placeholder="e.g. Senior Full Stack Engineer"
                      className="w-full px-3 py-2 rounded-xl bg-card/60 border border-border/80 text-foreground text-xs focus:outline-none focus:ring-2 focus:ring-primary/40"
                    />
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-muted-foreground block mb-1">
                      Job Description Raw Content
                    </label>
                    <textarea
                      rows={12}
                      value={jdText}
                      onChange={(e) => setJdText(e.target.value)}
                      placeholder="Paste complete job description here..."
                      className="w-full px-3 py-2 rounded-xl bg-card/60 border border-border/80 text-foreground text-xs font-mono focus:outline-none focus:ring-2 focus:ring-primary/40"
                    />
                  </div>

                  <button
                    onClick={handleAnalyzeJD}
                    disabled={analyzingJd}
                    className="w-full py-2.5 rounded-xl bg-primary text-primary-foreground text-xs font-bold flex items-center justify-center gap-2 hover:bg-primary/90 transition shadow"
                  >
                    {analyzingJd ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        Analyzing Job Requirements...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4" />
                        Analyze Requirements & Match Resume
                      </>
                    )}
                  </button>
                </div>
              </GlassCard>
            </div>

            {/* Extracted JD Requirements View */}
            <div className="lg:col-span-5 space-y-6">
              <GlassCard className="p-6 space-y-4">
                <div className="flex items-center justify-between border-b border-border/40 pb-3">
                  <div>
                    <h3 className="text-base font-bold text-foreground">Extracted JD Architecture</h3>
                    <p className="text-xs text-muted-foreground">
                      Structured criteria for the ATS semantic matching engine.
                    </p>
                  </div>
                  {jdAnalysis && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-primary/10 text-primary">
                      {jdAnalysis.seniorityLevel}
                    </span>
                  )}
                </div>

                {jdAnalysis ? (
                  <div className="space-y-4 text-xs">
                    <div>
                      <p className="font-bold text-foreground mb-1.5 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        Required Skills ({jdAnalysis.requiredSkills?.length || 0}):
                      </p>
                      <div className="flex flex-wrap gap-1.5">
                        {jdAnalysis.requiredSkills?.map((s: string, idx: number) => (
                          <span key={idx} className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 text-[11px] font-medium border border-emerald-500/20">
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div>
                      <p className="font-bold text-foreground mb-1.5 flex items-center gap-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
                        Preferred Skills ({jdAnalysis.preferredSkills?.length || 0}):
                      </p>
                      <div className="flex flex-wrap gap-1.5">
                        {jdAnalysis.preferredSkills?.map((s: string, idx: number) => (
                          <span key={idx} className="px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-700 dark:text-indigo-400 text-[11px] font-medium border border-indigo-500/20">
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div>
                      <p className="font-bold text-foreground mb-1.5 flex items-center gap-1.5">
                        <Briefcase className="w-3.5 h-3.5 text-primary" />
                        Key Responsibilities ({jdAnalysis.keyResponsibilities?.length || 0}):
                      </p>
                      <ul className="list-disc pl-4 space-y-1 text-muted-foreground text-[11px]">
                        {jdAnalysis.keyResponsibilities?.slice(0, 4).map((r: string, idx: number) => (
                          <li key={idx}>{r}</li>
                        ))}
                      </ul>
                    </div>

                    <button
                      onClick={() => {
                        setActiveTab("match");
                        runATSMatch();
                      }}
                      className="w-full mt-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:bg-primary/90 transition flex items-center justify-center gap-2"
                    >
                      Proceed to Full ATS Audit
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ) : (
                  <div className="text-center py-12 text-muted-foreground text-xs space-y-2">
                    <Search className="w-8 h-8 mx-auto text-muted-foreground/40" />
                    <p>Click "Analyze Requirements" to segment the job description into structured criteria.</p>
                  </div>
                )}
              </GlassCard>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 3: ATS COMPATIBILITY SCORE & SEMANTIC MATCH BREAKDOWN */}
        {/* ========================================================================= */}
        {activeTab === "match" && (
          <div className="space-y-6">
            {matchLoading ? (
              <GlassCard className="p-12 text-center space-y-4">
                <RefreshCw className="w-8 h-8 mx-auto text-primary animate-spin" />
                <h3 className="text-base font-bold text-foreground">Computing Exact ATS Match Breakdown...</h3>
                <p className="text-xs text-muted-foreground max-w-md mx-auto">
                  Running cosine similarity matrix across candidate resume snippets and target JD requirements with evidence citation tracking.
                </p>
              </GlassCard>
            ) : matchResult ? (
              <>
                {/* Top Score Cards Grid */}
                <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                  {/* Big Circular / Metric Card */}
                  <GlassCard className="md:col-span-4 p-6 flex flex-col items-center justify-center text-center space-y-3">
                    <div className="relative w-36 h-36 flex items-center justify-center rounded-full border-8 border-primary/20 bg-primary/5">
                      <div className="text-center">
                        <span className="text-4xl font-black text-foreground">
                          {matchResult.overallScore}
                        </span>
                        <span className="text-xs font-bold text-muted-foreground block">/ 100</span>
                      </div>
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-foreground">ATS Compatibility Score</h3>
                      <p className="text-xs text-muted-foreground">
                        {matchResult.overallScore >= 75
                          ? "High Interview Probability — Excellent Alignment"
                          : matchResult.overallScore >= 55
                          ? "Moderate Alignment — Key Gaps Can Be Resolved"
                          : "Low Alignment — Critical Skills Missing"}
                      </p>
                    </div>
                  </GlassCard>

                  {/* Part A & Part B Mathematical Breakdown */}
                  <GlassCard className="md:col-span-8 p-6 space-y-4">
                    <div className="flex items-center justify-between border-b border-border/40 pb-2">
                      <h3 className="text-sm font-bold text-foreground">
                        Mathematical Score Breakdown (Explainable Formula)
                      </h3>
                      <span className="text-xs font-mono text-muted-foreground">
                        Part A (60 pts) + Part B (40 pts)
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {/* Part A Card */}
                      <div className="p-4 rounded-xl bg-card/60 border border-border/60 space-y-2.5">
                        <div className="flex justify-between items-center">
                          <span className="text-xs font-bold text-primary">Part A: JD Requirement Alignment</span>
                          <span className="text-xs font-black font-mono text-foreground">
                            {matchResult.breakdown.partAScore} / 60
                          </span>
                        </div>
                        <div className="space-y-1.5 text-[11px] text-muted-foreground">
                          <div className="flex justify-between">
                            <span>Required Skills Coverage</span>
                            <span className="font-semibold text-foreground">
                              {matchResult.breakdown.partADetails.requiredSkillsScore} / 25
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Preferred Skills Coverage</span>
                            <span className="font-semibold text-foreground">
                              {matchResult.breakdown.partADetails.preferredSkillsScore} / 10
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Responsibilities Alignment</span>
                            <span className="font-semibold text-foreground">
                              {matchResult.breakdown.partADetails.responsibilitiesScore} / 15
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Qualifications Alignment</span>
                            <span className="font-semibold text-foreground">
                              {matchResult.breakdown.partADetails.qualificationsScore} / 10
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Part B Card */}
                      <div className="p-4 rounded-xl bg-card/60 border border-border/60 space-y-2.5">
                        <div className="flex justify-between items-center">
                          <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400">Part B: Resume Document Quality</span>
                          <span className="text-xs font-black font-mono text-foreground">
                            {matchResult.breakdown.partBScore} / 40
                          </span>
                        </div>
                        <div className="space-y-1.5 text-[11px] text-muted-foreground">
                          <div className="flex justify-between">
                            <span>Action Verbs & Impact Metrics</span>
                            <span className="font-semibold text-foreground">
                              {matchResult.breakdown.partBDetails.actionVerbsAndImpactScore} / 15
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>ATS Parseability & Standards</span>
                            <span className="font-semibold text-foreground">
                              {matchResult.breakdown.partBDetails.formattingAndParseabilityScore} / 10
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Section Completeness & Balance</span>
                            <span className="font-semibold text-foreground">
                              {matchResult.breakdown.partBDetails.sectionCompletenessScore} / 15
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <p className="text-xs text-muted-foreground leading-relaxed pt-1">
                      {matchResult.breakdown.explanation}
                    </p>
                  </GlassCard>
                </div>

                {/* Strengths & Critical Gaps Summary */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <GlassCard className="p-5 space-y-3">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4" />
                      Identified Strengths ({matchResult.strengthsSummary?.length || 0})
                    </h4>
                    <ul className="space-y-2 text-xs text-muted-foreground">
                      {(matchResult.strengthsSummary || []).map((str: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-emerald-500 font-bold">•</span>
                          <span>{str}</span>
                        </li>
                      ))}
                    </ul>
                  </GlassCard>

                  <GlassCard className="p-5 space-y-3">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400 flex items-center gap-1.5">
                      <AlertTriangle className="w-4 h-4" />
                      Critical Gaps to Address ({matchResult.criticalGapsSummary?.length || 0})
                    </h4>
                    <ul className="space-y-2 text-xs text-muted-foreground">
                      {(matchResult.criticalGapsSummary || []).map((gap: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-rose-500 font-bold">•</span>
                          <span>{gap}</span>
                        </li>
                      ))}
                    </ul>
                  </GlassCard>
                </div>

                {/* Detailed Requirement Match Table with Evidence Citations */}
                <GlassCard className="p-6 space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-border/40 pb-3">
                    <div>
                      <h3 className="text-base font-bold text-foreground">
                        Semantic Requirement Evidence Ledger
                      </h3>
                      <p className="text-xs text-muted-foreground">
                        Inspect exact cosine similarity scores and line evidence extracted from both documents.
                      </p>
                    </div>

                    {/* Filter buttons */}
                    <div className="flex flex-wrap gap-1.5">
                      <button
                        onClick={() => setGapFilter("all")}
                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                          gapFilter === "all" ? "bg-primary text-primary-foreground" : "bg-card/60 text-muted-foreground"
                        }`}
                      >
                        All
                      </button>
                      <button
                        onClick={() => setGapFilter("explicit")}
                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                          gapFilter === "explicit" ? "bg-emerald-600 text-white" : "bg-card/60 text-muted-foreground"
                        }`}
                      >
                        Explicit ({matchResult.explicitMatches?.length ?? matchResult.strongMatches?.length ?? 0})
                      </button>
                      <button
                        onClick={() => setGapFilter("partial")}
                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                          gapFilter === "partial" ? "bg-amber-600 text-white" : "bg-card/60 text-muted-foreground"
                        }`}
                      >
                        Partial ({matchResult.partialMatches?.length || 0})
                      </button>
                      <button
                        onClick={() => setGapFilter("not_found")}
                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                          gapFilter === "not_found" ? "bg-rose-600 text-white" : "bg-card/60 text-muted-foreground"
                        }`}
                      >
                        Not in Text ({matchResult.notFoundRequirements?.length ?? matchResult.missingRequirements?.length ?? 0})
                      </button>
                      {(matchResult.uncertainExtractions?.length || 0) > 0 && (
                        <button
                          onClick={() => setGapFilter("uncertain")}
                          className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                            gapFilter === "uncertain" ? "bg-sky-600 text-white" : "bg-card/60 text-muted-foreground"
                          }`}
                        >
                          Uncertain ({matchResult.uncertainExtractions?.length || 0})
                        </button>
                      )}
                    </div>
                  </div>

                  {/* List of matched items */}
                  <div className="space-y-2.5">
                    {[
                      ...(gapFilter === "all" || gapFilter === "explicit" ? (matchResult.explicitMatches || matchResult.strongMatches || []) : []),
                      ...(gapFilter === "all" || gapFilter === "partial" ? (matchResult.partialMatches || []) : []),
                      ...(gapFilter === "all" || gapFilter === "not_found" ? (matchResult.notFoundRequirements || matchResult.missingRequirements || []) : []),
                      ...(gapFilter === "all" || gapFilter === "uncertain" ? (matchResult.uncertainExtractions || []) : []),
                    ].map((m: any, idx: number) => (
                      <div
                        key={idx}
                        className={`p-3.5 rounded-xl border transition ${
                          m.status === "explicitly_matched" || m.status === "strong"
                            ? "bg-emerald-500/5 border-emerald-500/30"
                            : m.status === "partially_supported" || m.status === "partial"
                            ? "bg-amber-500/5 border-amber-500/30"
                            : m.status === "uncertain_extraction"
                            ? "bg-sky-500/5 border-sky-500/30"
                            : "bg-rose-500/5 border-rose-500/30"
                        }`}
                      >
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                          <div className="flex items-center gap-2">
                            {m.status === "explicitly_matched" || m.status === "strong" ? (
                              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                            ) : m.status === "partially_supported" || m.status === "partial" ? (
                              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                            ) : m.status === "uncertain_extraction" ? (
                              <HelpCircle className="w-4 h-4 text-sky-600 shrink-0" />
                            ) : (
                              <XCircle className="w-4 h-4 text-rose-600 shrink-0" />
                            )}
                            <span className="text-xs font-bold text-foreground">{m.requirement}</span>
                            <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
                              {m.category.replace("_", " ")}
                            </span>
                          </div>

                          <div className="flex items-center gap-2">
                            <span className="text-xs font-mono font-bold text-foreground">
                              Sim: {m.similarityScore}
                            </span>
                            <span
                              className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
                                m.status === "explicitly_matched" || m.status === "strong"
                                  ? "bg-emerald-600 text-white"
                                  : m.status === "partially_supported" || m.status === "partial"
                                  ? "bg-amber-600 text-white"
                                  : m.status === "uncertain_extraction"
                                  ? "bg-sky-600 text-white"
                                  : "bg-rose-600 text-white"
                              }`}
                            >
                              {m.statusLabel || m.status}
                            </span>
                          </div>
                        </div>

                        {/* Audit Note & Evidence */}
                        {m.auditNote && (
                          <p className="mt-1.5 text-[11px] text-muted-foreground italic">
                            {m.auditNote}
                          </p>
                        )}
                        {m.resumeEvidence && (
                          <div className="mt-2 text-[11px] p-2 rounded-lg bg-card/60 border border-border/40 text-muted-foreground">
                            <span className="font-semibold text-foreground">Resume Evidence: </span>
                            {m.resumeEvidence}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>

                  <div className="pt-4 border-t border-border/40 flex justify-end">
                    <button
                      onClick={() => {
                        setActiveTab("improve");
                        handleGenerateImprovements();
                      }}
                      className="px-5 py-2.5 rounded-xl bg-primary text-primary-foreground text-xs font-bold hover:bg-primary/90 transition shadow flex items-center gap-2"
                    >
                      <Sparkles className="w-4 h-4" />
                      Generate Grounded AI Improvements
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                </GlassCard>
              </>
            ) : (
              <GlassCard className="p-12 text-center space-y-3">
                <BarChart3 className="w-8 h-8 mx-auto text-muted-foreground/40" />
                <p className="text-xs text-muted-foreground">No ATS match computed yet.</p>
                <button
                  onClick={() => runATSMatch()}
                  className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-bold"
                >
                  Run Semantic Match Audit
                </button>
              </GlassCard>
            )}
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 4: AI IMPROVEMENT ENGINE (STAR BULLETS & INTERVIEW PROMPTS) */}
        {/* ========================================================================= */}
        {activeTab === "improve" && (
          <div className="space-y-6">
            {/* Grounding & Integrity Banner */}
            <div className="p-4 rounded-2xl bg-primary/10 border border-primary/20 flex items-start gap-3">
              <ShieldCheck className="w-5 h-5 text-primary shrink-0 mt-0.5" />
              <div>
                <p className="text-xs font-bold text-foreground">Strict Grounding & Zero Hallucination Guarantee</p>
                <p className="text-[11px] text-muted-foreground mt-0.5">
                  The AI model (Qwen2.5-1.5B MLX) is instructed to never fabricate metrics, employers, or skills.
                  For critical missing requirements, targeted interview questions are generated to collect your genuine experiences.
                </p>
              </div>
            </div>

            {improveLoading ? (
              <GlassCard className="p-12 text-center space-y-4">
                <RefreshCw className="w-8 h-8 mx-auto text-primary animate-spin" />
                <h3 className="text-base font-bold text-foreground">Generating STAR Bullet Elevations...</h3>
                <p className="text-xs text-muted-foreground max-w-md mx-auto">
                  Applying Situation-Task-Action-Result restructuring with strong action verbs to your existing project and experience statements.
                </p>
              </GlassCard>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* Left: Interactive Suggestions (Accept / Reject) */}
                <div className="lg:col-span-7 space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-base font-bold text-foreground">
                      Grounded STAR Bullet Improvements ({improvements.length})
                    </h3>
                    <button
                      onClick={handleGenerateImprovements}
                      className="inline-flex items-center gap-1.5 text-xs text-primary font-semibold hover:underline"
                    >
                      <RefreshCw className="w-3.5 h-3.5" />
                      Regenerate
                    </button>
                  </div>

                  {improvements.map((sug) => {
                    const isAccepted = acceptedIds.has(sug.id);
                    const isRejected = rejectedIds.has(sug.id);

                    return (
                      <GlassCard
                        key={sug.id}
                        className={`p-5 space-y-3 transition border-2 ${
                          isAccepted
                            ? "border-emerald-500/60 bg-emerald-500/5"
                            : isRejected
                            ? "border-rose-500/40 opacity-60"
                            : "border-border/60"
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-[11px] font-bold text-primary font-mono uppercase">
                            {sug.targetSection}
                          </span>
                          {isAccepted && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-600 text-white flex items-center gap-1">
                              <Check className="w-3 h-3" /> Accepted
                            </span>
                          )}
                          {isRejected && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-600 text-white flex items-center gap-1">
                              <X className="w-3 h-3" /> Dismissed
                            </span>
                          )}
                        </div>

                        {/* Original vs Suggested */}
                        <div className="space-y-2 text-xs">
                          <div className="p-2.5 rounded-lg bg-card/40 border border-border/40 text-muted-foreground">
                            <span className="font-semibold text-foreground block text-[10px] uppercase mb-0.5">Original Phrasing:</span>
                            {sug.originalText}
                          </div>
                          <div className="p-2.5 rounded-lg bg-primary/5 border border-primary/20 text-foreground font-medium">
                            <span className="font-bold text-primary block text-[10px] uppercase mb-0.5">Elevated STAR Bullet:</span>
                            {sug.suggestedText}
                          </div>
                        </div>

                        <p className="text-[11px] text-muted-foreground italic">
                          Rationale: {sug.rationale}
                        </p>

                        {/* Missing evidence question if any */}
                        {sug.missingEvidenceQuestion && (
                          <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-800 dark:text-amber-300 text-[11px] flex items-start gap-2">
                            <HelpCircle className="w-4 h-4 shrink-0 mt-0.5" />
                            <span>{sug.missingEvidenceQuestion}</span>
                          </div>
                        )}

                        {/* Actions */}
                        {!isAccepted && !isRejected && (
                          <div className="flex justify-end gap-2 pt-2 border-t border-border/40">
                            <button
                              onClick={() => handleRejectSuggestion(sug.id)}
                              className="px-3 py-1.5 rounded-lg border border-border/80 text-xs font-semibold hover:bg-card transition"
                            >
                              Dismiss
                            </button>
                            <button
                              onClick={() => handleAcceptSuggestion(sug)}
                              className="px-4 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs font-bold hover:bg-primary/90 transition shadow flex items-center gap-1.5"
                            >
                              <Check className="w-3.5 h-3.5" />
                              Apply to Resume
                            </button>
                          </div>
                        )}
                      </GlassCard>
                    );
                  })}
                </div>

                {/* Right: Targeted Missing Evidence Interview Questions */}
                <div className="lg:col-span-5 space-y-4">
                  <h3 className="text-base font-bold text-foreground">
                    Missing Evidence Interview Questions
                  </h3>
                  <GlassCard className="p-5 space-y-4">
                    <p className="text-xs text-muted-foreground">
                      Rather than fabricating false qualifications, provide genuine details for these identified gaps to incorporate them truthfully into your resume:
                    </p>

                    <div className="space-y-3">
                      {targetedQuestions.map((q, idx) => (
                        <div key={idx} className="p-3.5 rounded-xl bg-card/60 border border-border/60 text-xs space-y-2">
                          <p className="font-semibold text-foreground flex items-start gap-2">
                            <span className="w-5 h-5 rounded-full bg-primary/10 text-primary text-[10px] font-black flex items-center justify-center shrink-0">
                              {idx + 1}
                            </span>
                            <span>{q}</span>
                          </p>
                          <textarea
                            rows={2}
                            placeholder="Type your authentic experience, tools, and outcomes here..."
                            className="w-full px-2.5 py-1.5 rounded-lg bg-background/80 border border-border/60 text-xs text-foreground focus:outline-none focus:ring-1 focus:ring-primary/40"
                          />
                        </div>
                      ))}
                    </div>
                  </GlassCard>

                  {/* Multi-Format Export Action Card */}
                  <GlassCard className="p-5 space-y-3">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-foreground">
                      Ready to Apply?
                    </h4>
                    <p className="text-xs text-muted-foreground">
                      Export your upgraded resume with all accepted STAR bullets and ATS structural enhancements.
                    </p>
                    <div className="flex gap-2 pt-1">
                      <button
                        onClick={handleExportDocx}
                        className="flex-1 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-bold hover:bg-primary/90 transition shadow flex items-center justify-center gap-2"
                      >
                        <Download className="w-3.5 h-3.5" />
                        Download DOCX
                      </button>
                      <button
                        onClick={() => window.print()}
                        className="flex-1 py-2 rounded-xl border border-border/80 text-foreground text-xs font-bold hover:bg-card transition flex items-center justify-center gap-2"
                      >
                        <Printer className="w-3.5 h-3.5" />
                        Print / PDF
                      </button>
                    </div>
                  </GlassCard>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
