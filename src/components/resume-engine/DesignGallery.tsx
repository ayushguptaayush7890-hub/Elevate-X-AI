"use client";

import React, { useState, useMemo, useEffect, useCallback } from "react";
import { ResumeFullData } from "@/types/resume-generator";
import {
  DesignSpecification,
  DesignCategory,
  TargetRole,
  AIRecommendationResult,
} from "@/types/resume-design-engine";
import {
  getCuratedSixBatch,
  getDesignById,
  getRandomDesign,
  getFallbackAIRecommendation,
  TOTAL_DESIGNS_COUNT,
} from "@/services/resume-design-engine";
import { UniversalResumeRenderer } from "./UniversalResumeRenderer";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import {
  Sparkles,
  Search,
  Check,
  Heart,
  Shuffle,
  ShieldCheck,
  ChevronRight,
  SlidersHorizontal,
  Layers,
  ArrowRight,
  RotateCw,
  Eye,
  Bot,
  AlertCircle,
  Award,
  Zap,
  Info,
} from "lucide-react";

interface Props {
  resume: ResumeFullData;
  selectedDesignId: string;
  onSelectDesign: (design: DesignSpecification) => void;
  onContinueToStudio: () => void;
  onBackToEdit: () => void;
}

const SESSION_SEEN_KEY = "elevate_x_session_seen_designs";
const FAVORITES_KEY = "elevate_x_favorite_designs";

export function DesignGallery({
  resume,
  selectedDesignId,
  onSelectDesign,
  onContinueToStudio,
  onBackToEdit,
}: Props) {
  // Filters
  const [selectedCategory, setSelectedCategory] = useState<DesignCategory | "all">("all");
  const [selectedRole, setSelectedRole] = useState<TargetRole | "all">("all");
  const [atsOnly, setAtsOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  // AI Recommendation State
  const [aiRecommendation, setAiRecommendation] = useState<AIRecommendationResult | null>(null);
  const [isLoadingAI, setIsLoadingAI] = useState<boolean>(true);

  // Six-Design Curated Batch State
  const [displayedBatch, setDisplayedBatch] = useState<DesignSpecification[]>([]);
  const [seenIds, setSeenIds] = useState<string[]>([]);
  const [totalMatchingCount, setTotalMatchingCount] = useState<number>(TOTAL_DESIGNS_COUNT);
  const [batchCycleCount, setBatchCycleCount] = useState<number>(1);

  // Favorites & Preview Modal
  const [favorites, setFavorites] = useState<string[]>([]);
  const [previewModalDesign, setPreviewModalDesign] = useState<DesignSpecification | null>(null);

  // 1. Load Session History & Favorites on Mount
  useEffect(() => {
    try {
      const savedFavs = localStorage.getItem(FAVORITES_KEY);
      if (savedFavs) {
        setFavorites(JSON.parse(savedFavs));
      }
      const savedSeen = sessionStorage.getItem(SESSION_SEEN_KEY);
      if (savedSeen) {
        const parsed = JSON.parse(savedSeen);
        if (Array.isArray(parsed)) {
          setSeenIds(parsed);
        }
      }
    } catch {
      // Non-fatal
    }
  }, []);

  // 2. Fetch Genuine AI Recommendation from Local Qwen2.5-1.5B MLX Model
  const fetchAIRecommendation = useCallback(async () => {
    setIsLoadingAI(true);
    try {
      const res = await apiService.recommendResumeDesign({
        resumeData: resume,
        targetRole: resume.personalInfo.professionalTitle,
      });

      if (res.data) {
        const rec = res.data;
        setAiRecommendation(rec);

        // Auto-select the AI recommended design if current selection is default
        if (!selectedDesignId || selectedDesignId === "des-0001") {
          const recDesign = getDesignById(rec.recommendedDesignId);
          onSelectDesign(recDesign);
        }
        return rec.recommendedDesignId;
      }
    } catch (err: any) {
      // Explicitly state AI recommendation is unavailable - NEVER pretend it came from AI
      setAiRecommendation({
        recommendedDesignId: "des-0001",
        explanation: "AI recommendation could not be generated at this time.",
        matchingProfileCharacteristics: [],
        whyAppropriate: "",
        isFallback: true,
        fallbackReason: `Local Qwen2.5-1.5B MLX inference unavailable: ${err?.message || "Service not responding"}. Showing standard design catalog below.`,
      });
      return "des-0001";
    } finally {
      setIsLoadingAI(false);
    }
    return "des-0001";
  }, [resume, selectedDesignId, onSelectDesign]);

  // 3. Initial Load: Fetch AI recommendation and then generate first 6-design batch
  useEffect(() => {
    let isMounted = true;
    async function init() {
      const recId = await fetchAIRecommendation();
      if (!isMounted) return;

      const initialSeen = (() => {
        try {
          const s = sessionStorage.getItem(SESSION_SEEN_KEY);
          return s ? JSON.parse(s) : [];
        } catch {
          return [];
        }
      })();

      const result = getCuratedSixBatch(
        {
          category: selectedCategory,
          targetRole: selectedRole,
          atsOnly,
          searchQuery,
        },
        initialSeen,
        recId,
        true // Include recommended design in slot 1
      );

      setDisplayedBatch(result.designs);
      setTotalMatchingCount(result.totalMatching);
      setSeenIds(result.newSeenIds);
      try {
        sessionStorage.setItem(SESSION_SEEN_KEY, JSON.stringify(result.newSeenIds));
      } catch {
        // ignore
      }
    }
    init();
    return () => {
      isMounted = false;
    };
  }, []); // Run once on mount

  // 4. "Show 6 New Designs" Handler
  const handleShowSixNewDesigns = () => {
    const recId = aiRecommendation?.recommendedDesignId;
    const result = getCuratedSixBatch(
      {
        category: selectedCategory,
        targetRole: selectedRole,
        atsOnly,
        searchQuery,
      },
      seenIds,
      recId,
      false // New batch prioritizes fresh unseen designs
    );

    setDisplayedBatch(result.designs);
    setTotalMatchingCount(result.totalMatching);
    setSeenIds(result.newSeenIds);
    setBatchCycleCount((prev) => prev + 1);

    try {
      sessionStorage.setItem(SESSION_SEEN_KEY, JSON.stringify(result.newSeenIds));
    } catch {
      // ignore
    }

    toast.info(`Loaded batch #${batchCycleCount + 1}: 6 fresh designs from ${result.totalMatching} total matches.`);
  };

  // 5. Handle Filter Changes: Filter across complete catalog, but return exactly 6 matching designs
  const applyFilter = (newCategory: DesignCategory | "all", newRole: TargetRole | "all", newAts: boolean, newSearch: string) => {
    setSelectedCategory(newCategory);
    setSelectedRole(newRole);
    setAtsOnly(newAts);
    setSearchQuery(newSearch);

    const recId = aiRecommendation?.recommendedDesignId;
    const result = getCuratedSixBatch(
      {
        category: newCategory,
        targetRole: newRole,
        atsOnly: newAts,
        searchQuery: newSearch,
      },
      [], // Reset seen pool for new filter view so user sees top matches first
      recId,
      true
    );

    setDisplayedBatch(result.designs);
    setTotalMatchingCount(result.totalMatching);
    setSeenIds(result.newSeenIds);
    setBatchCycleCount(1);
  };

  // 6. Favorites Toggle
  const toggleFavorite = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setFavorites((prev) => {
      const next = prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id];
      try {
        localStorage.setItem(FAVORITES_KEY, JSON.stringify(next));
      } catch {
        // ignore
      }
      return next;
    });
  };

  const categories: { id: DesignCategory | "all"; label: string }[] = [
    { id: "all", label: "All Categories" },
    { id: "ats_friendly", label: "ATS-Friendly" },
    { id: "technical", label: "Technical / Dev" },
    { id: "corporate", label: "Corporate Executive" },
    { id: "modern", label: "Modern Split" },
    { id: "minimal", label: "Minimal Clean" },
    { id: "elegant", label: "Elegant Editorial" },
    { id: "creative", label: "Creative & Visual" },
  ];

  const roles: { id: TargetRole | "all"; label: string }[] = [
    { id: "all", label: "All Professions" },
    { id: "developer", label: "Software Engineer / Developer" },
    { id: "data_science", label: "AI & Data Scientist" },
    { id: "fresher", label: "Student & College Fresher" },
    { id: "executive", label: "Lead & Director" },
    { id: "creative", label: "Creative & Designer" },
  ];

  const recDesign = aiRecommendation ? getDesignById(aiRecommendation.recommendedDesignId) : null;

  return (
    <div className="space-y-8 pb-32">
      {/* Gallery Header Banner */}
      <div className="bg-gradient-to-r from-[#17233F] via-[#241E4E] to-[#17233F] rounded-3xl p-6 sm:p-8 text-white shadow-xl border border-[#D6A84B]/20 relative overflow-hidden">
        <div className="relative z-10 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#D6A84B]/20 border border-[#D6A84B]/40 text-[#D6A84B] text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5" /> Curated 6-Design Discovery Engine
            </div>
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight">
              Personalized Resume Design Recommendations
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              Discover a focused batch of 6 handcrafted designs from our 1,024-configuration catalog.
              The AI highlights the ideal design tailored to your career milestones, while 5 distinct alternatives offer diverse layouts.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <button
              onClick={handleShowSixNewDesigns}
              className="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-xs flex items-center gap-2 transition-all cursor-pointer shadow-sm hover:scale-[1.02]"
              title="Cycles to the next 6 unseen designs"
            >
              <RotateCw className="w-4 h-4 text-[#D6A84B]" /> Show 6 New Designs
            </button>
            <button
              onClick={onContinueToStudio}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#D6A84B] to-[#F0D99B] text-[#17233F] font-black text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-[#D6A84B]/25 hover:opacity-95 transition-all cursor-pointer hover:scale-[1.02]"
            >
              Open Resume Studio <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* AI RECOMMENDATION SPOTLIGHT CARD */}
      {aiRecommendation && (
        <div
          className={`p-6 rounded-3xl border-2 transition-all shadow-md ${
            aiRecommendation.isFallback
              ? "bg-amber-50/60 border-amber-200 text-[#17233F]"
              : "bg-gradient-to-br from-indigo-50/80 via-white to-purple-50/60 border-[#7355D9]/40 shadow-[#7355D9]/5 text-[#17233F]"
          }`}
        >
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-200/60 pb-4">
            <div className="flex items-center gap-3">
              <div
                className={`w-10 h-10 rounded-2xl flex items-center justify-center font-bold shadow-xs ${
                  aiRecommendation.isFallback
                    ? "bg-amber-100 text-amber-800"
                    : "bg-[#7355D9] text-[#F0D99B]"
                }`}
              >
                {aiRecommendation.isFallback ? <Bot className="w-5 h-5" /> : <Sparkles className="w-5 h-5" />}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-black uppercase tracking-wider text-[#17233F]">
                    {aiRecommendation.isFallback
                      ? "Algorithmic Heuristic Recommendation"
                      : "Genuine AI Personalized Recommendation"}
                  </span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      aiRecommendation.isFallback
                        ? "bg-amber-200 text-amber-900"
                        : "bg-purple-100 text-[#7355D9] border border-purple-200"
                    }`}
                  >
                    {aiRecommendation.isFallback ? "Fallback Mode" : "Qwen2.5-1.5B MLX"}
                  </span>
                </div>
                <div className="text-sm font-black text-[#17233F] mt-0.5">
                  Recommended Design: <span className="text-[#7355D9]">{recDesign?.name || aiRecommendation.recommendedDesignId}</span> ({aiRecommendation.recommendedDesignId})
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  if (recDesign) onSelectDesign(recDesign);
                }}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
                  selectedDesignId === aiRecommendation.recommendedDesignId
                    ? "bg-emerald-600 text-white shadow-xs"
                    : "bg-[#17233F] text-[#F0D99B] hover:bg-[#202E4E]"
                }`}
              >
                {selectedDesignId === aiRecommendation.recommendedDesignId ? (
                  <>
                    <Check className="w-3.5 h-3.5" /> Selected
                  </>
                ) : (
                  <>Select AI Design</>
                )}
              </button>
            </div>
          </div>

          <div className="pt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            {/* Explanation */}
            <div className="space-y-1">
              <div className="font-bold text-slate-700 flex items-center gap-1">
                <Info className="w-3.5 h-3.5 text-slate-400" /> Recommendation Rationale:
              </div>
              <p className="text-slate-600 leading-relaxed">{aiRecommendation.explanation}</p>
            </div>

            {/* Matching Profile Characteristics */}
            <div className="space-y-1.5">
              <div className="font-bold text-slate-700 flex items-center gap-1">
                <Zap className="w-3.5 h-3.5 text-amber-500" /> Matching Profile Traits:
              </div>
              <div className="flex flex-wrap gap-1.5">
                {aiRecommendation.matchingProfileCharacteristics.map((trait, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 rounded-lg bg-white border border-slate-200 text-[11px] font-semibold text-slate-700"
                  >
                    {trait}
                  </span>
                ))}
              </div>
            </div>

            {/* Why Appropriate */}
            <div className="space-y-1">
              <div className="font-bold text-slate-700 flex items-center gap-1">
                <Award className="w-3.5 h-3.5 text-[#7355D9]" /> Visual Hierarchy Fit:
              </div>
              <p className="text-slate-600 leading-relaxed">{aiRecommendation.whyAppropriate}</p>
            </div>
          </div>

          {aiRecommendation.isFallback && aiRecommendation.fallbackReason && (
            <div className="mt-3 pt-2 border-t border-amber-200/60 text-[11px] text-amber-800 flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0" />
              <span>Note: {aiRecommendation.fallbackReason}</span>
            </div>
          )}
        </div>
      )}

      {/* FILTER & CONTROL TOOLBAR */}
      <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
          {/* Search Bar */}
          <div className="relative flex-1 max-w-md">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => applyFilter(selectedCategory, selectedRole, atsOnly, e.target.value)}
              placeholder="Search across all 1,024 designs (e.g. Apex, Terminal, des-0042)..."
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder:text-slate-400 focus:outline-hidden focus:ring-2 focus:ring-[#7355D9]/30 focus:border-[#7355D9]"
            />
          </div>

          {/* Profession Dropdown & ATS Toggle */}
          <div className="flex items-center gap-3">
            <select
              value={selectedRole}
              onChange={(e) => applyFilter(selectedCategory, e.target.value as TargetRole | "all", atsOnly, searchQuery)}
              aria-label="Filter by target role"
              className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 font-semibold focus:outline-hidden focus:border-[#7355D9]"
            >
              {roles.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.label}
                </option>
              ))}
            </select>

            <label className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 cursor-pointer text-xs font-semibold text-slate-700 select-none">
              <input
                type="checkbox"
                checked={atsOnly}
                onChange={(e) => applyFilter(selectedCategory, selectedRole, e.target.checked, searchQuery)}
                className="w-4 h-4 text-[#7355D9] rounded border-slate-300 focus:ring-[#7355D9]"
              />
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>ATS Only</span>
            </label>
          </div>
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs scrollbar-none">
          {categories.map((cat) => {
            const isSelected = selectedCategory === cat.id;
            return (
              <button
                key={cat.id}
                onClick={() => applyFilter(cat.id, selectedRole, atsOnly, searchQuery)}
                className={`px-3 py-1.5 rounded-lg font-bold shrink-0 transition-all cursor-pointer ${
                  isSelected
                    ? "bg-[#17233F] text-[#F0D99B] shadow-xs"
                    : "bg-slate-100 hover:bg-slate-200 text-slate-600"
                }`}
              >
                {cat.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* ACTIVE BATCH STATUS & BATCH NAVIGATION STRIP */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs border-b border-slate-200 pb-3">
        <div className="flex items-center gap-2">
          <span className="font-black text-[#17233F]">
            Showing 6 of {totalMatchingCount} matching designs
          </span>
          <span className="text-slate-400">•</span>
          <span className="text-slate-500 font-medium">Batch #{batchCycleCount}</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleShowSixNewDesigns}
            className="px-4 py-1.5 rounded-xl bg-white border border-[#D6A84B] text-[#17233F] hover:bg-[#FBF8F1] font-bold text-xs flex items-center gap-1.5 transition-all cursor-pointer shadow-2xs hover:scale-[1.01]"
          >
            <RotateCw className="w-3.5 h-3.5 text-[#D6A84B]" />
            <span>Show 6 New Designs</span>
          </button>
        </div>
      </div>

      {/* CURATED SIX DESIGNS GRID (EXACTLY 6 CARDS) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {displayedBatch.map((design, index) => {
          const isSelected = design.id === selectedDesignId;
          const isRecommended = design.id === aiRecommendation?.recommendedDesignId;
          const isFav = favorites.includes(design.id);

          return (
            <div
              key={design.id}
              onClick={() => onSelectDesign(design)}
              className={`group bg-white rounded-3xl border-2 transition-all duration-200 cursor-pointer overflow-hidden flex flex-col justify-between hover:shadow-xl relative ${
                isSelected
                  ? "border-[#D6A84B] ring-4 ring-[#D6A84B]/20 shadow-lg scale-[1.01]"
                  : isRecommended
                  ? "border-[#7355D9] ring-2 ring-[#7355D9]/20"
                  : "border-slate-200 hover:border-slate-400"
              }`}
            >
              {/* Card Header Info */}
              <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/80">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <span className="font-black text-xs text-slate-900 group-hover:text-[#7355D9] transition-colors">
                      {design.name}
                    </span>
                    {isRecommended && (
                      <span className="text-[9px] font-black px-2 py-0.5 rounded-full bg-[#7355D9] text-[#F0D99B] flex items-center gap-1 shadow-xs">
                        <Sparkles className="w-2.5 h-2.5" /> AI Pick
                      </span>
                    )}
                    {design.atsCompatibility === "strict_ats" && (
                      <span className="text-[9px] font-black px-1.5 py-0.2 rounded bg-emerald-100 text-emerald-700">
                        ATS
                      </span>
                    )}
                  </div>
                  <div className="text-[10px] text-slate-500 font-mono">
                    {design.id} • {design.category} • {design.targetRole}
                  </div>
                </div>

                <div className="flex items-center gap-1.5">
                  <button
                    onClick={(e) => toggleFavorite(design.id, e)}
                    aria-label={isFav ? "Remove from favorites" : "Save to favorites"}
                    className={`p-1.5 rounded-full transition-colors cursor-pointer ${
                      isFav ? "text-rose-500 bg-rose-50" : "text-slate-400 hover:text-slate-600"
                    }`}
                  >
                    <Heart className={`w-3.5 h-3.5 ${isFav ? "fill-rose-500" : ""}`} />
                  </button>
                  {isSelected && (
                    <div className="w-6 h-6 rounded-full bg-[#D6A84B] text-[#17233F] flex items-center justify-center font-bold">
                      <Check className="w-3.5 h-3.5 stroke-[3]" />
                    </div>
                  )}
                </div>
              </div>

              {/* Live Scaled Preview Window with User's Genuine Data */}
              <div className="relative h-[360px] bg-slate-100/60 overflow-hidden flex items-start justify-center p-3">
                <div className="w-[850px] shrink-0 pointer-events-none select-none origin-top transition-transform group-hover:scale-[0.38] scale-[0.36]">
                  <UniversalResumeRenderer
                    resume={resume}
                    design={design}
                    isThumbnail={true}
                  />
                </div>

                {/* Hover Action Overlay */}
                <div className="absolute inset-0 bg-slate-900/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2.5 backdrop-blur-[1px]">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setPreviewModalDesign(design);
                    }}
                    className="px-3.5 py-2 rounded-xl bg-white/95 text-slate-800 text-xs font-bold hover:bg-white shadow-md cursor-pointer flex items-center gap-1"
                  >
                    <Eye className="w-3.5 h-3.5" /> Preview
                  </button>
                  <button
                    onClick={() => {
                      onSelectDesign(design);
                      onContinueToStudio();
                    }}
                    className="px-4 py-2 rounded-xl bg-[#D6A84B] text-[#17233F] text-xs font-black hover:bg-[#F0D99B] shadow-md cursor-pointer"
                  >
                    Select & Open
                  </button>
                </div>
              </div>

              {/* Card Footer Features */}
              <div className="p-3.5 bg-white text-[11px] text-slate-500 border-t border-slate-100 flex items-center justify-between">
                <div className="flex items-center gap-1.5">
                  <span
                    className="w-2.5 h-2.5 rounded-full inline-block shrink-0"
                    style={{ backgroundColor: design.palette.primary }}
                  />
                  <span className="font-medium truncate max-w-[140px]">{design.palette.name}</span>
                </div>
                <span className="font-mono text-[10px] uppercase font-bold text-slate-400">
                  {design.layout.replace(/_/g, " ").slice(0, 16)}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* BOTTOM ACTION STRIP: "SHOW 6 NEW DESIGNS" */}
      <div className="text-center pt-2 pb-6 space-y-2">
        <button
          onClick={handleShowSixNewDesigns}
          className="px-8 py-3.5 rounded-2xl bg-white hover:bg-slate-50 border-2 border-slate-200 hover:border-[#D6A84B] text-[#17233F] font-black text-xs uppercase tracking-wider shadow-sm transition-all cursor-pointer inline-flex items-center gap-2.5 hover:scale-[1.01]"
        >
          <RotateCw className="w-4 h-4 text-[#D6A84B]" />
          <span>Show 6 New Designs (from {totalMatchingCount} total)</span>
        </button>
        <p className="text-[11px] text-slate-400">
          Cycles to the next unseen batch while preserving your resume data and AI enhancements.
        </p>
      </div>

      {/* Fixed Bottom Dock Bar when a design is selected (Non-obstructing, clear of cards) */}
      <div className="fixed bottom-4 left-0 right-0 z-30 pointer-events-none flex justify-center px-4">
        <div className="pointer-events-auto max-w-2xl w-full bg-[#17233F]/95 text-white backdrop-blur-md rounded-2xl p-4 shadow-2xl border border-[#D6A84B]/40 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#D6A84B]/20 border border-[#D6A84B]/40 flex items-center justify-center text-[#D6A84B] font-black text-xs">
              {selectedDesignId.replace("des-", "#")}
            </div>
            <div>
              <div className="text-xs font-bold text-white">
                Selected: {getDesignById(selectedDesignId).name}
              </div>
              <div className="text-[10px] text-slate-300">
                {getDesignById(selectedDesignId).category.toUpperCase()} • {getDesignById(selectedDesignId).layout.replace(/_/g, " ")}
              </div>
            </div>
          </div>

          <button
            onClick={onContinueToStudio}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#D6A84B] to-[#F0D99B] text-[#17233F] font-black text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-[#D6A84B]/25 hover:opacity-95 transition-all cursor-pointer"
          >
            Open in Studio <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Full Preview Modal */}
      {previewModalDesign && (
        <div
          className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto"
          onClick={() => setPreviewModalDesign(null)}
        >
          <div
            className="bg-white rounded-3xl max-w-4xl w-full p-6 space-y-4 shadow-2xl border border-slate-200 max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center border-b border-slate-100 pb-3">
              <div>
                <h3 className="font-black text-lg text-slate-900">{previewModalDesign.name}</h3>
                <span className="text-xs text-slate-500 font-mono">
                  {previewModalDesign.id} • {previewModalDesign.category} • {previewModalDesign.targetRole}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    onSelectDesign(previewModalDesign);
                    setPreviewModalDesign(null);
                    onContinueToStudio();
                  }}
                  className="px-5 py-2 rounded-xl bg-[#D6A84B] text-[#17233F] text-xs font-black cursor-pointer hover:bg-[#F0D99B]"
                >
                  Select & Open in Studio
                </button>
                <button
                  onClick={() => setPreviewModalDesign(null)}
                  className="p-2 text-slate-400 hover:text-slate-600 cursor-pointer font-bold"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="overflow-x-auto p-4 bg-slate-100/50 rounded-2xl flex justify-center">
              <div className="w-[850px] shrink-0">
                <UniversalResumeRenderer
                  resume={resume}
                  design={previewModalDesign}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
