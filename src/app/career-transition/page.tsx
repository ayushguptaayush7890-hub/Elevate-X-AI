"use client";

import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { PageHeader } from "@/components/ui/PageHeader";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import {
  TrendingUp,
  ArrowRight,
  Compass,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Briefcase,
  Search,
  BookOpen,
  DollarSign,
  Award,
  Layers,
  ChevronRight,
  Loader2,
  ExternalLink,
  ShieldCheck,
  FileText,
  GraduationCap,
  HelpCircle,
  Check,
  X,
  RefreshCw,
  Clock
} from "lucide-react";

interface OccupationOption {
  canonical_id: string;
  title: string;
  source: string;
  code?: string;
  description?: string;
  isco_group?: string;
}

interface TransitionRec {
  target_occupation_id: string;
  target_title: string;
  target_source: string;
  target_code?: string;
  target_description?: string;
  fit_percentage: number;
  transition_delta: number;
  difficulty_category: string;
  estimated_months: number;
  salary_range?: string;
  demand_level: string;
  demand_postings_count: number;
  transferable_skills_count: number;
  bridgeable_skills_count: number;
  missing_skills_count: number;
  academic_relevance_score?: number;
  academic_matched_skills_count?: number;
  scoring_basis?: string;
  transferable_competencies_preview: string[];
  bridgeable_competencies_preview: string[];
}

interface CompetencyItem {
  name: string;
  skill_id?: string;
  evidence_state: string;
  evidence_score: number;
  importance: string;
  notes?: string;
  requires_practical_validation?: boolean;
}

interface AcademicCompetencyItem {
  competency_name: string;
  original_evidence: string;
  evidence_type: string;
  source_record: string;
  confidence_score: number;
  requires_practical_validation: boolean;
  matched_target_skills?: string[];
  semantic_similarity?: number;
}

interface AcademicProfileSummary {
  has_academic_profile: boolean;
  institution?: string;
  degree?: string;
  field_of_study?: string;
  academic_competencies: AcademicCompetencyItem[];
  academic_projects: string[];
  source_notice?: string;
}

interface AnalysisData {
  from_occupation_id: string;
  from_occupation_title: string;
  to_occupation_id: string;
  to_occupation_title: string;
  to_taxonomy: string;
  fit_percentage: number;
  transition_delta: number;
  difficulty_category: string;
  estimated_months: number;
  salary_range?: string;
  demand_level: string;
  demand_postings_count: number;
  transferable_competencies: CompetencyItem[];
  bridgeable_competencies: CompetencyItem[];
  missing_competencies: CompetencyItem[];
  academic_profile?: AcademicProfileSummary;
  academic_matches?: AcademicCompetencyItem[];
  scoring_explanation?: {
    methodology: string;
    components: Record<string, any>;
    provenance: Record<string, any>;
  };
}

interface BlueprintStage {
  stage_id?: string;
  stage_number: number;
  stage_name: string;
  timeframe: string;
  duration_weeks?: number;
  workload_hours_per_week?: number;
  objective: string;
  target_competencies?: string[];
  competency_ids?: string[];
  candidate_evidence?: string;
  practical_tasks?: string[];
  milestones: string[];
  tasks: string[];
  measurable_deliverables?: string[];
  recommended_resources: Array<{
    id?: string;
    title?: string;
    name?: string;
    url?: string;
    provider?: string;
    type?: string;
    source_domain?: string;
    difficulty?: string;
  }>;
}

interface BlueprintData {
  transition_id: string;
  from_occupation_id?: string;
  from_occupation: string;
  target_occupation_id?: string;
  target_occupation: string;
  overall_fit: number;
  total_estimated_weeks: number;
  stages: BlueprintStage[];
  generated_by: string;
  model_used: string;
  blueprint_version?: string;
  evidence_fingerprint?: string;
  personalization_summary?: string;
  cached?: boolean;
}

export default function CareerTransitionPage() {
  const router = useRouter();

  // State: separate state for searchQuery, selectedOccupation, and searchResults
  const [selectedOccupation, setSelectedOccupation] = useState<string>("Software Developer");
  const [searchQuery, setSearchQuery] = useState<string>("Software Developer");
  const [searchResults, setSearchResults] = useState<OccupationOption[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showSearchDropdown, setShowSearchDropdown] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [candidateSkills, setCandidateSkills] = useState<string[]>([]);

  // Academic Profile State
  const [academicProfile, setAcademicProfile] = useState<AcademicProfileSummary | null>(null);
  const [isLoadingAcademic, setIsLoadingAcademic] = useState(false);

  // Recommendations and Analysis
  const [recommendations, setRecommendations] = useState<TransitionRec[]>([]);
  const [selectedTarget, setSelectedTarget] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [blueprint, setBlueprint] = useState<BlueprintData | null>(null);

  // Loading flags
  const [isLoadingRecs, setIsLoadingRecs] = useState(false);
  const [isLoadingAnalysis, setIsLoadingAnalysis] = useState(false);
  const [isAdoptingGoal, setIsAdoptingGoal] = useState(false);
  const [isRecalibratingBlueprint, setIsRecalibratingBlueprint] = useState(false);

  const searchContainerRef = useRef<HTMLDivElement>(null);
  const searchRequestIdRef = useRef(0);

  // Load candidate profile and academic background on mount
  useEffect(() => {
    async function loadCandidateProfile() {
      try {
        const [profileRes, academicRes] = await Promise.all([
          apiService.getProfile(),
          apiService.getAcademicProfile()
        ]);

        if (profileRes?.data) {
          const prof = profileRes.data;
          const userTrade = prof.trade_category || prof.currentOccupation;
          if (userTrade) {
            setSelectedOccupation(userTrade);
            setSearchQuery(userTrade);
          }
          if (prof.skills && Array.isArray(prof.skills)) {
            const skillNames = prof.skills.map((s: any) =>
              typeof s === "string" ? s : s.name || s.skill_name || ""
            ).filter(Boolean);
            setCandidateSkills(skillNames);
          }
        }

        if (academicRes?.data) {
          setAcademicProfile(academicRes.data);
        }
      } catch (err) {
        console.warn("Could not load user profile or academic data:", err);
      }
    }
    loadCandidateProfile();
  }, []);

  // Fetch recommendations whenever selectedOccupation changes
  useEffect(() => {
    if (!selectedOccupation || !selectedOccupation.trim()) {
      setRecommendations([]);
      setSelectedTarget(null);
      setAnalysis(null);
      setBlueprint(null);
      return;
    }

    let isMounted = true;
    async function fetchRecommendations() {
      setIsLoadingRecs(true);
      try {
        const res = await apiService.getCareerTransitionRecommendations(
          selectedOccupation,
          candidateSkills.length > 0 ? candidateSkills : undefined,
          6
        );
        if (isMounted && res?.data && Array.isArray(res.data)) {
          setRecommendations(res.data);
          if (res.data.length > 0) {
            setSelectedTarget(res.data[0].target_title);
          } else {
            setSelectedTarget(null);
          }
        }
      } catch (err) {
        console.error("Failed to load transition recommendations:", err);
        if (isMounted) setRecommendations([]);
      } finally {
        if (isMounted) setIsLoadingRecs(false);
      }
    }

    fetchRecommendations();
    return () => {
      isMounted = false;
    };
  }, [selectedOccupation, candidateSkills]);

  // Fetch Deep-Dive and Blueprint when selectedTarget or selectedOccupation changes
  useEffect(() => {
    let isMounted = true;

    async function fetchDeepDive() {
      const target = selectedTarget;
      if (!target || !selectedOccupation || !selectedOccupation.trim()) {
        setAnalysis(null);
        setBlueprint(null);
        return;
      }

      setIsLoadingAnalysis(true);
      try {
        const [analysisRes, blueprintRes] = await Promise.all([
          apiService.analyzeCareerTransition(
            selectedOccupation,
            target,
            candidateSkills.length > 0 ? candidateSkills : undefined
          ),
          apiService.generateTransitionBlueprint(
            selectedOccupation,
            target,
            candidateSkills.length > 0 ? candidateSkills : undefined
          )
        ]);

        if (isMounted) {
          if (analysisRes?.data) setAnalysis(analysisRes.data);
          if (blueprintRes?.data) setBlueprint(blueprintRes.data);
        }
      } catch (err) {
        console.error("Failed to load transition deep-dive:", err);
      } finally {
        if (isMounted) setIsLoadingAnalysis(false);
      }
    }

    fetchDeepDive();
    return () => {
      isMounted = false;
    };
  }, [selectedTarget, selectedOccupation, candidateSkills]);

  // Handle Occupation Autocomplete Search with race condition protection
  useEffect(() => {
    const trimmed = searchQuery.trim();
    if (trimmed.length < 2) {
      setSearchResults([]);
      setIsSearching(false);
      return;
    }

    const currentReqId = ++searchRequestIdRef.current;

    const timer = setTimeout(async () => {
      setIsSearching(true);
      try {
        const res = await apiService.searchOccupations(trimmed, 8);
        if (currentReqId === searchRequestIdRef.current) {
          if (res?.data && Array.isArray(res.data)) {
            setSearchResults(res.data);
            setShowSearchDropdown(true);
          } else {
            setSearchResults([]);
          }
        }
      } catch (err) {
        if (currentReqId === searchRequestIdRef.current) {
          console.warn("Search occupations failed:", err);
          setSearchError("Failed to fetch occupations. Please try again.");
          setSearchResults([]);
        }
      } finally {
        if (currentReqId === searchRequestIdRef.current) {
          setIsSearching(false);
        }
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Close dropdown on outside click without reverting user's typed search query
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target as Node)) {
        setShowSearchDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSearchInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchQuery(value);
    setSearchError(null);

    // Requirement 4: Clearing the input clears previous selected occupation where appropriate
    if (value.trim().length === 0) {
      setSelectedOccupation("");
      setSearchResults([]);
      setShowSearchDropdown(false);
      return;
    }

    setShowSearchDropdown(true);
  };

  const handleClearSearch = () => {
    setSearchQuery("");
    setSelectedOccupation("");
    setSearchResults([]);
    setShowSearchDropdown(false);
    setSearchError(null);
  };

  const handleSelectOccupation = (occ: OccupationOption) => {
    setSelectedOccupation(occ.title);
    setSearchQuery(occ.title);
    setShowSearchDropdown(false);
    setSearchResults([]);
    setSearchError(null);
    toast.success(`Trade background updated to: ${occ.title}`);
  };

  const handleSearchKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      if (searchResults.length > 0) {
        handleSelectOccupation(searchResults[0]);
      } else if (searchQuery.trim().length >= 2) {
        setSelectedOccupation(searchQuery.trim());
        setShowSearchDropdown(false);
        toast.success(`Analyzing transitions for: ${searchQuery.trim()}`);
      }
    } else if (e.key === "Escape") {
      setShowSearchDropdown(false);
    }
  };

  const handleRecalibrateBlueprint = async () => {
    if (!selectedTarget || !selectedOccupation || !selectedOccupation.trim()) return;
    setIsRecalibratingBlueprint(true);
    try {
      const res = await apiService.generateTransitionBlueprint(
        selectedOccupation,
        selectedTarget,
        candidateSkills.length > 0 ? candidateSkills : undefined,
        true
      );
      if (res?.data) {
        setBlueprint(res.data);
        toast.success(`Blueprint recalibrated with fresh model inference for ${selectedTarget}`);
      }
    } catch (err) {
      console.error("Recalibrate failed:", err);
      toast.error("Failed to recalibrate blueprint.");
    } finally {
      setIsRecalibratingBlueprint(false);
    }
  };

  const handleAdoptGoal = async () => {
    if (!selectedTarget || !analysis) return;

    setIsAdoptingGoal(true);
    try {
      const res = await apiService.adoptTransitionGoal({
        from_occupation_title: analysis.from_occupation_title,
        target_occupation_id: analysis.to_occupation_id,
        target_occupation_title: analysis.to_occupation_title,
        fit_percentage: analysis.fit_percentage,
        transition_delta: analysis.transition_delta,
        difficulty_category: analysis.difficulty_category,
        blueprint: blueprint || undefined
      });

      if (res?.data?.success) {
        toast.success(res.data.message || `Goal adopted: ${analysis.to_occupation_title}`);
        router.push(`/career-roadmap?role=${encodeURIComponent(analysis.to_occupation_title)}`);
      } else {
        toast.success(`Adopted ${analysis.to_occupation_title} as your career goal!`);
        router.push(`/career-roadmap?role=${encodeURIComponent(analysis.to_occupation_title)}`);
      }
    } catch (err) {
      console.error("Adopt goal failed:", err);
      toast.error("Failed to adopt career goal. Please retry.");
    } finally {
      setIsAdoptingGoal(false);
    }
  };

  const renderEvidenceBadge = (state: string, score: number, requiresPractical?: boolean) => {
    switch (state) {
      case "assessment_verified":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
            <ShieldCheck className="w-3 h-3 text-emerald-600" />
            Verified Assessment (100%)
          </span>
        );
      case "practically_demonstrated":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-teal-50 text-teal-700 border border-teal-200">
            <Briefcase className="w-3 h-3 text-teal-600" />
            Workplace Demonstrated (90%)
          </span>
        );
      case "academic_evidence":
        return (
          <div className="flex flex-col items-end gap-1">
            <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
              <GraduationCap className="w-3 h-3 text-indigo-600" />
              Academic Theoretical ({Math.round(score * 100)}%)
            </span>
            {requiresPractical && (
              <span className="text-[9px] font-semibold text-amber-700 bg-amber-50 px-1.5 py-0.2 rounded border border-amber-200">
                Requires Practical Validation
              </span>
            )}
          </div>
        );
      case "mentioned_in_resume":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-sky-50 text-sky-700 border border-sky-200">
            <FileText className="w-3 h-3 text-sky-600" />
            Resume Extracted (80%)
          </span>
        );
      case "self_reported":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
            <CheckCircle2 className="w-3 h-3 text-amber-600" />
            Self Reported (75%)
          </span>
        );
      case "related_taxonomy_evidence":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-50 text-purple-700 border border-purple-200">
            <Layers className="w-3 h-3 text-purple-600" />
            Taxonomy Aligned ({Math.round(score * 100)}%)
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
            Not Assessed
          </span>
        );
    }
  };

  return (
    <AppShell>
      <div className="space-y-6 pb-12">
        <PageHeader
          badge="Authentic Occupational Mobility Engine"
          title="Career Transition & Skill Transferability"
          description="Discover explainable mobility corridors bridging your craftsmanship and academic foundation into high-demand careers. Grounded in ESCO v1.2.1, O*NET 28.1, India NCO-2015, and authentic job postings."
          variant="navy"
          actions={
            <div className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40">
              <Compass className="w-4 h-4 text-[#D6A84B]" />
              <span>{recommendations.length} Verified Corridors</span>
            </div>
          }
        />

        {/* Current Trade Selector & Autocomplete Search */}
        <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex-1 space-y-1">
              <label htmlFor="career-transition-search-input" className="text-xs font-bold text-[#17233F] block">
                Current Trade Background &amp; Occupation:
              </label>
              <div ref={searchContainerRef} className="relative max-w-xl">
                <div className="relative flex items-center">
                  <Search className="w-4 h-4 text-slate-400 absolute left-3 pointer-events-none" />
                  <input
                    id="career-transition-search-input"
                    type="text"
                    value={searchQuery}
                    onChange={handleSearchInputChange}
                    onKeyDown={handleSearchKeyDown}
                    onFocus={() => {
                      if (searchResults.length > 0 || searchQuery.trim().length >= 2) {
                        setShowSearchDropdown(true);
                      }
                    }}
                    placeholder="Search an occupation, e.g. Data Scientist, Electrician, or Software Developer..."
                    className="w-full pl-9 pr-14 py-2 text-xs sm:text-sm bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl text-[#20243A] font-medium focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all shadow-inner"
                    autoComplete="off"
                  />
                  <div className="absolute right-3 flex items-center gap-1.5">
                    {isSearching && (
                      <Loader2 className="w-4 h-4 text-[#D6A84B] animate-spin" />
                    )}
                    {searchQuery.length > 0 && (
                      <button
                        type="button"
                        onClick={handleClearSearch}
                        className="p-1 rounded-lg hover:bg-slate-200/60 text-slate-400 hover:text-slate-700 transition-colors"
                        title="Clear search input"
                        aria-label="Clear search input"
                      >
                        <X className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                </div>

                {/* Dropdown Suggestions */}
                {showSearchDropdown && (
                  <div className="absolute z-30 left-0 right-0 mt-1.5 bg-white border border-[#E6DFD1] rounded-xl shadow-xl max-h-72 overflow-y-auto divide-y divide-slate-100">
                    {searchResults.length > 0 ? (
                      searchResults.map((occ) => (
                        <button
                          key={occ.canonical_id}
                          type="button"
                          onClick={() => handleSelectOccupation(occ)}
                          className="w-full text-left px-4 py-2.5 hover:bg-[#FBF8F1] transition-colors flex items-center justify-between gap-3 group"
                        >
                          <div className="min-w-0 flex-1">
                            <div className="text-xs sm:text-sm font-semibold text-[#17233F] group-hover:text-[#7355D9] transition-colors flex items-center gap-2">
                              <span className="truncate">{occ.title}</span>
                              {selectedOccupation.toLowerCase() === occ.title.toLowerCase() && (
                                <span className="text-[10px] text-emerald-700 bg-emerald-50 px-1.5 py-0.2 rounded font-bold border border-emerald-200 shrink-0">
                                  Current
                                </span>
                              )}
                            </div>
                            <div className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">
                              {occ.description || `Verified occupational profile in ${occ.source}`}
                            </div>
                            <div className="flex items-center gap-2 mt-0.5 text-[10px] text-slate-400 font-mono">
                              {occ.code && <span className="truncate max-w-[180px]">Code: {occ.code}</span>}
                              {occ.canonical_id && <span>ID: {occ.canonical_id}</span>}
                            </div>
                          </div>
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#17233F]/5 text-[#17233F] border border-[#17233F]/10 shrink-0">
                            {occ.source}
                          </span>
                        </button>
                      ))
                    ) : !isSearching && searchQuery.trim().length >= 2 ? (
                      <div className="p-4 text-center text-xs text-slate-500">
                        No occupations found matching &ldquo;{searchQuery}&rdquo; in ESCO, O*NET, or NCO catalogs.
                      </div>
                    ) : null}
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <span className="text-xs text-[#17233F] font-bold px-3 py-1.5 rounded-xl bg-[#F0D99B]/60 border border-[#D6A84B] flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-[#8F6B17]" />
                BGE Semantic + Node2Vec Graph Engine
              </span>
            </div>
          </div>

          {/* Active Occupation Status Bar (Quick trade presets row removed) */}
          <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-xs">
            {selectedOccupation ? (
              <div className="flex items-center gap-2">
                <span className="text-[#687187] font-medium">Active Origin Occupation:</span>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#17233F] text-[#F0D99B] font-bold shadow-sm">
                  <Briefcase className="w-3.5 h-3.5 text-[#D6A84B]" />
                  {selectedOccupation}
                </span>
                <span className="text-[11px] text-slate-400 hidden sm:inline">
                  (Corridors automatically recomputed via graph similarity)
                </span>
              </div>
            ) : (
              <div className="flex items-center gap-2 text-amber-700 bg-amber-50 px-3 py-1.5 rounded-lg border border-amber-200">
                <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                <span>Search and select an origin occupation above to analyze career transition corridors.</span>
              </div>
            )}
          </div>
        </div>

        {/* Phase 9 Prominent Requirement: Academic Background & Competency Match */}
        <div className="p-5 sm:p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div>
              <span className="text-[10px] font-bold uppercase text-[#7355D9] tracking-wider flex items-center gap-1.5">
                <GraduationCap className="w-3.5 h-3.5 text-[#7355D9]" />
                Academic Provenance Integration
              </span>
              <h3 className="text-base font-bold text-[#17233F] mt-0.5">
                Academic Background & Competency Match
              </h3>
            </div>
            {academicProfile?.has_academic_profile && (
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
                {academicProfile.academic_competencies.length} Academic Competencies Extracted
              </span>
            )}
          </div>

          {academicProfile?.has_academic_profile ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1]">
                  <span className="text-[10px] font-bold uppercase text-slate-500 block">Degree / Qualification</span>
                  <span className="text-xs sm:text-sm font-bold text-[#17233F] mt-0.5 block truncate">
                    {academicProfile.degree || "Formal Degree On File"}
                  </span>
                </div>
                <div className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1]">
                  <span className="text-[10px] font-bold uppercase text-slate-500 block">Field / Specialization</span>
                  <span className="text-xs sm:text-sm font-bold text-[#17233F] mt-0.5 block truncate">
                    {academicProfile.field_of_study || "General Technical Study"}
                  </span>
                </div>
                <div className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1]">
                  <span className="text-[10px] font-bold uppercase text-slate-500 block">Institution / University</span>
                  <span className="text-xs sm:text-sm font-bold text-[#17233F] mt-0.5 block truncate">
                    {academicProfile.institution || "Accredited University"}
                  </span>
                </div>
              </div>

              {/* Competencies Extracted with Evidence */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-[#17233F]">
                    Extracted Academic Theoretical Competencies:
                  </span>
                  <span className="text-[11px] text-amber-700 font-medium">
                    * Academic competencies require practical workplace demonstration
                  </span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                  {academicProfile.academic_competencies.map((ac, idx) => (
                    <div
                      key={idx}
                      className="p-2.5 rounded-xl bg-indigo-50/40 border border-indigo-200 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between gap-1">
                          <span className="text-xs font-bold text-indigo-950 block truncate">
                            {ac.competency_name}
                          </span>
                          <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-indigo-100 text-indigo-700 whitespace-nowrap">
                            {Math.round(ac.confidence_score * 100)}%
                          </span>
                        </div>
                        <span className="text-[10px] text-slate-500 line-clamp-1 mt-0.5">
                          {ac.original_evidence}
                        </span>
                      </div>
                      <div className="pt-2 mt-1 border-t border-indigo-100 flex items-center justify-between text-[9px] text-amber-800 font-semibold">
                        <span>Requires Practical Demo</span>
                        <span className="text-slate-400 capitalize">{ac.evidence_type.replace("academic_", "")}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {academicProfile.academic_projects.length > 0 && (
                <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center gap-1.5 text-xs">
                  <span className="text-[11px] font-bold text-slate-600">Academic Project Evidence:</span>
                  {academicProfile.academic_projects.map((proj, pidx) => (
                    <span
                      key={pidx}
                      className="text-[10px] px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200 font-medium"
                    >
                      {proj}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-center space-y-1">
              <p className="text-xs font-semibold text-[#17233F]">
                No Formal Academic Records on File
              </p>
              <p className="text-[11px] text-slate-500 max-w-lg mx-auto">
                Transition corridor recommendations and fit percentages are calculated strictly from your verified vocational assessments, demonstrated work tools, and occupational taxonomy graphs.
              </p>
            </div>
          )}
        </div>

        {/* Pathways Grid */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-[#17233F] flex items-center gap-2">
              <Compass className="w-4 h-4 text-[#D6A84B]" />
              Recommended Career Corridors {selectedOccupation ? `from “${selectedOccupation}”` : ""}
            </h2>
            {isLoadingRecs && (
              <span className="text-xs text-[#687187] flex items-center gap-1.5">
                <Loader2 className="w-3.5 h-3.5 animate-spin text-[#D6A84B]" />
                Recomputing structural graph fit & semantic alignment...
              </span>
            )}
          </div>

          {!selectedOccupation ? (
            <div className="p-10 text-center rounded-2xl bg-white border border-[#E6DFD1] space-y-2">
              <Search className="w-8 h-8 text-slate-400 mx-auto" />
              <h3 className="text-sm font-bold text-[#17233F]">No Origin Occupation Selected</h3>
              <p className="text-xs text-slate-500 max-w-md mx-auto">
                Search and select an origin occupation in the search field above to calculate transferability matrices, BGE semantic alignment, and verified career corridors.
              </p>
            </div>
          ) : isLoadingRecs ? (
            <div className="p-12 text-center rounded-2xl bg-white border border-[#E6DFD1] space-y-3">
              <Loader2 className="w-8 h-8 animate-spin text-[#D6A84B] mx-auto" />
              <p className="text-sm font-medium text-[#17233F]">
                Analyzing occupational transitions using PyTorch graph embeddings, BGE semantic calibration, and academic evidence...
              </p>
            </div>
          ) : recommendations.length === 0 ? (
            <div className="p-8 text-center rounded-2xl bg-white border border-[#E6DFD1]">
              <AlertCircle className="w-6 h-6 text-[#C77B54] mx-auto mb-2" />
              <p className="text-sm font-medium text-[#17233F]">
                No transition pathways found for &ldquo;{selectedOccupation}&rdquo;. Try another occupation or trade keyword above.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recommendations.map((path) => {
                const isSelected = selectedTarget === path.target_title;
                const isLowFriction = path.difficulty_category === "Low Friction";
                const isModerate = path.difficulty_category === "Moderate Bridge";

                return (
                  <div
                    key={path.target_occupation_id}
                    onClick={() => setSelectedTarget(path.target_title)}
                    className={`p-5 rounded-2xl bg-white border cursor-pointer transition-all flex flex-col justify-between ${
                      isSelected
                        ? "ring-2 ring-[#D6A84B] border-[#D6A84B] shadow-md bg-amber-50/10"
                        : "border-[#E6DFD1] hover:shadow-md hover:border-[#D6A84B]/60"
                    }`}
                  >
                    <div className="space-y-3">
                      <div className="flex items-start justify-between gap-2">
                        <div>
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#F5F0E6] text-[#17233F] border border-[#E6DFD1]">
                            {path.target_source}
                          </span>
                          <h3 className="text-sm font-bold text-[#17233F] mt-1.5 line-clamp-1">
                            {path.target_title}
                          </h3>
                        </div>
                        <span className="text-xs font-black px-2.5 py-0.5 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B] whitespace-nowrap">
                          {path.fit_percentage}% Fit
                        </span>
                      </div>

                      <div className="flex flex-wrap items-center gap-2 text-xs">
                        <span
                          className={`font-bold px-2 py-0.5 rounded-full text-[11px] ${
                            isLowFriction
                              ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                              : isModerate
                              ? "bg-amber-50 text-amber-700 border border-amber-200"
                              : "bg-orange-50 text-orange-700 border border-orange-200"
                          }`}
                        >
                          Delta: {path.difficulty_category}
                        </span>
                        <span className="text-slate-300">•</span>
                        <span className="text-slate-600 font-medium">
                          Est: {path.estimated_months} mos
                        </span>
                      </div>

                      {/* Academic Contribution Badge */}
                      {path.academic_matched_skills_count !== undefined && path.academic_matched_skills_count > 0 && (
                        <div className="text-[11px] text-indigo-700 bg-indigo-50/60 px-2.5 py-1 rounded-lg border border-indigo-200/60 flex items-center justify-between">
                          <span className="font-semibold flex items-center gap-1">
                            <GraduationCap className="w-3.5 h-3.5 text-indigo-600" />
                            Academic Alignment
                          </span>
                          <span className="font-bold">
                            {path.academic_matched_skills_count} Skills Matched
                          </span>
                        </div>
                      )}

                      {path.salary_range && (
                        <div className="text-xs text-slate-700 bg-[#FBF8F1] px-2.5 py-1.5 rounded-lg border border-[#E6DFD1]/60 flex items-center justify-between gap-1.5">
                          <div className="flex items-center gap-1.5 truncate">
                            <Briefcase className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                            <span className="truncate text-[11px] font-medium text-slate-600">
                              Market: {path.salary_range}
                            </span>
                          </div>
                          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 whitespace-nowrap">
                            {path.demand_level} Demand
                          </span>
                        </div>
                      )}

                      {/* Transferable Skills Preview */}
                      <div className="space-y-1 text-xs">
                        <span className="text-[10px] font-bold uppercase text-emerald-700 block tracking-wider">
                          Transferable Skills ({path.transferable_skills_count})
                        </span>
                        <div className="flex flex-wrap gap-1">
                          {path.transferable_competencies_preview.map((sk, i) => (
                            <span
                              key={i}
                              className="text-[10px] px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 font-medium truncate max-w-[150px]"
                            >
                              {sk}
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* Bridgeable Skills Preview */}
                      {path.bridgeable_competencies_preview.length > 0 && (
                        <div className="space-y-1 text-xs">
                          <span className="text-[10px] font-bold uppercase text-amber-700 block tracking-wider">
                            Bridgeable Skills ({path.bridgeable_skills_count})
                          </span>
                          <div className="flex flex-wrap gap-1">
                            {path.bridgeable_competencies_preview.map((sk, i) => (
                              <span
                                key={i}
                                className="text-[10px] px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-200 font-medium truncate max-w-[150px]"
                              >
                                {sk}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="pt-3 mt-3 border-t border-[#E6DFD1] flex items-center justify-between text-xs font-bold text-[#7355D9]">
                      <span>{isSelected ? "Active Corridor Deep-Dive" : "Select Corridor"}</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Selected Pathway Deep-Dive: Transferability Breakdown & Blueprint */}
        {selectedTarget && (
          <div className="space-y-6 pt-4">
            {/* Header & Adopt CTA */}
            <div className="p-6 sm:p-8 rounded-2xl bg-[#17233F] text-white border border-[#D6A84B]/40 shadow-xl space-y-5">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-[#D6A84B] font-bold uppercase tracking-wider">
                      Occupational Mobility Specification
                    </span>
                    {analysis && (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-white/10 text-[#F0D99B]">
                        Taxonomy: {analysis.to_taxonomy}
                      </span>
                    )}
                  </div>
                  <h2 className="text-xl sm:text-2xl font-black text-white mt-1">
                    {selectedOccupation} <span className="text-[#D6A84B]">➔</span> {selectedTarget}
                  </h2>
                  {analysis && (
                    <div className="flex flex-wrap items-center gap-3 text-xs text-[#F5F0E6] mt-2">
                      <span className="font-bold text-[#F0D99B]">
                        Overall Fit: {analysis.fit_percentage}%
                      </span>
                      <span>•</span>
                      <span>Transition Delta: {analysis.difficulty_category}</span>
                      <span>•</span>
                      <span>Target Market Demand: {analysis.demand_level} ({analysis.demand_postings_count} Postings)</span>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  <BrandButton
                    variant="gold"
                    size="md"
                    onClick={handleAdoptGoal}
                    disabled={isAdoptingGoal}
                    className="shadow-md whitespace-nowrap"
                  >
                    {isAdoptingGoal ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin mr-1.5" />
                        Adopting Goal...
                      </>
                    ) : (
                      <>
                        <Award className="w-4 h-4 mr-1.5" />
                        Adopt as Career Goal
                      </>
                    )}
                  </BrandButton>
                </div>
              </div>

              {/* Transferability Breakdown Accordions */}
              {isLoadingAnalysis ? (
                <div className="p-8 text-center rounded-xl bg-[#10192D] space-y-2">
                  <Loader2 className="w-6 h-6 animate-spin text-[#D6A84B] mx-auto" />
                  <p className="text-xs text-[#F0D99B]">
                    Evaluating BGE semantic embeddings, academic evidence, and graph transferability...
                  </p>
                </div>
              ) : analysis ? (
                <div className="space-y-4 pt-2">
                  {/* Academic Matches Banner */}
                  {analysis.academic_matches && analysis.academic_matches.length > 0 && (
                    <div className="p-4 rounded-xl bg-[#10192D] border border-indigo-400/40 space-y-2">
                      <div className="flex items-center justify-between">
                        <h4 className="text-xs font-bold uppercase text-indigo-300 tracking-wider flex items-center gap-1.5">
                          <GraduationCap className="w-4 h-4 text-indigo-400" />
                          Academic Competencies Grounding Target Occupation ({analysis.academic_matches.length})
                        </h4>
                        <span className="text-[11px] text-indigo-200">
                          Theoretical coursework & projects applied to destination role
                        </span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs pt-1">
                        {analysis.academic_matches.map((am, i) => (
                          <div
                            key={i}
                            className="p-2.5 rounded-lg bg-white/5 border border-indigo-500/20 flex items-center justify-between gap-2"
                          >
                            <div>
                              <span className="font-semibold text-white block text-xs">{am.competency_name}</span>
                              <span className="text-[10px] text-indigo-200 line-clamp-1">
                                Matched to: {am.matched_target_skills?.join(", ")}
                              </span>
                            </div>
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-400/30 whitespace-nowrap">
                              Sim: {Math.round((am.semantic_similarity || 0.8) * 100)}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Direct Transferable */}
                  <div className="p-4 rounded-xl bg-[#10192D] border border-emerald-500/30 space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold uppercase text-emerald-400 tracking-wider flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                        Direct Transferable Competencies ({analysis.transferable_competencies.length})
                      </h4>
                      <span className="text-[11px] text-emerald-300">
                        Carry directly into destination role without retraining
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs pt-1">
                      {analysis.transferable_competencies.map((c, i) => (
                        <div
                          key={i}
                          className="p-2.5 rounded-lg bg-white/5 border border-white/10 flex items-center justify-between gap-2"
                        >
                          <div>
                            <span className="font-semibold text-white block text-xs">{c.name}</span>
                            {c.notes && (
                              <span className="text-[10px] text-slate-400 line-clamp-1">
                                {c.notes}
                              </span>
                            )}
                          </div>
                          {renderEvidenceBadge(c.evidence_state, c.evidence_score, c.requires_practical_validation)}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Bridgeable Competencies */}
                  {analysis.bridgeable_competencies.length > 0 && (
                    <div className="p-4 rounded-xl bg-[#10192D] border border-amber-500/30 space-y-2">
                      <div className="flex items-center justify-between">
                        <h4 className="text-xs font-bold uppercase text-amber-400 tracking-wider flex items-center gap-1.5">
                          <Layers className="w-3.5 h-3.5 text-amber-400" />
                          Bridgeable / Adjacent Competencies ({analysis.bridgeable_competencies.length})
                        </h4>
                        <span className="text-[11px] text-amber-300">
                          Rapidly upgradeable via targeted short modules & practical demonstration
                        </span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs pt-1">
                        {analysis.bridgeable_competencies.map((c, i) => (
                          <div
                            key={i}
                            className="p-2.5 rounded-lg bg-white/5 border border-white/10 flex items-center justify-between gap-2"
                          >
                            <div>
                              <span className="font-semibold text-white block text-xs">{c.name}</span>
                              {c.notes && (
                                <span className="text-[10px] text-slate-400 line-clamp-1">
                                  {c.notes}
                                </span>
                              )}
                            </div>
                            {renderEvidenceBadge(c.evidence_state, c.evidence_score, c.requires_practical_validation)}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Missing Competencies */}
                  {analysis.missing_competencies.length > 0 && (
                    <div className="p-4 rounded-xl bg-[#10192D] border border-orange-500/30 space-y-2">
                      <div className="flex items-center justify-between">
                        <h4 className="text-xs font-bold uppercase text-orange-400 tracking-wider flex items-center gap-1.5">
                          <AlertCircle className="w-3.5 h-3.5 text-orange-400" />
                          Destination Competency Gaps ({analysis.missing_competencies.length})
                        </h4>
                        <span className="text-[11px] text-orange-300">
                          Addressed in personalized transition blueprint below
                        </span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs pt-1">
                        {analysis.missing_competencies.map((c, i) => (
                          <div
                            key={i}
                            className="p-2.5 rounded-lg bg-white/5 border border-white/10 flex items-center justify-between gap-2"
                          >
                            <span className="font-semibold text-white block text-xs">{c.name}</span>
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-orange-500/20 text-orange-300 border border-orange-500/30">
                              Priority Bridge
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Methodology Transparency Card */}
                  {analysis.scoring_explanation && (
                    <div className="p-3.5 rounded-xl bg-white/5 border border-white/10 text-xs text-slate-300 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div>
                        <span className="font-bold text-[#F0D99B] block">Fit Calculation Methodology:</span>
                        <span className="text-[11px] text-slate-400">
                          {analysis.scoring_explanation.methodology}
                        </span>
                      </div>
                      <div className="text-right whitespace-nowrap">
                        <span className="text-[11px] text-slate-400 block">Structural Weights:</span>
                        <span className="font-semibold text-[#D6A84B] text-[11px]">
                          {analysis.scoring_explanation.components?.weights}
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              ) : null}
            </div>

            {/* 4-Stage Transition Bridge Blueprint (Model-Powered) */}
            {blueprint && (
              <div className="p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-[#D6A84B] uppercase tracking-wider">
                        Model-Personalized Learning & Execution Roadmap
                      </span>
                      {blueprint.cached && (
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                          Cached Plan
                        </span>
                      )}
                    </div>
                    <h3 className="text-lg font-bold text-[#17233F] mt-0.5">
                      4-Stage Transition Bridge: {blueprint.from_occupation} → {blueprint.target_occupation} ({blueprint.total_estimated_weeks} Weeks Total)
                    </h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={handleRecalibrateBlueprint}
                      disabled={isRecalibratingBlueprint}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#E6DFD1] bg-[#FBF8F1] hover:bg-white text-xs font-semibold text-[#17233F] hover:border-[#D6A84B] transition-all disabled:opacity-50"
                      title="Force fresh model inference and invalidate cache"
                    >
                      <RefreshCw className={`w-3.5 h-3.5 ${isRecalibratingBlueprint ? "animate-spin text-[#D6A84B]" : "text-slate-500"}`} />
                      <span>{isRecalibratingBlueprint ? "Recalibrating..." : "Recalibrate Plan"}</span>
                    </button>
                    <span className="text-xs text-slate-600 bg-[#FBF8F1] border border-[#E6DFD1] px-3 py-1.5 rounded-lg font-medium hidden md:inline-block">
                      Inference: {blueprint.model_used}
                    </span>
                  </div>
                </div>

                {blueprint.personalization_summary && (
                  <div className="p-4 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-xs text-slate-700 leading-relaxed">
                    <span className="font-bold text-[#17233F] block mb-1">Transition Rationale & Synthesis:</span>
                    {blueprint.personalization_summary}
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {blueprint.stages.map((stg) => (
                    <div
                      key={stg.stage_number}
                      className="p-5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] space-y-3.5 flex flex-col justify-between"
                    >
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-black px-2.5 py-0.5 rounded-full bg-[#17233F] text-[#F0D99B]">
                            Stage {stg.stage_number}
                          </span>
                          <div className="flex items-center gap-2">
                            {stg.workload_hours_per_week && (
                              <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-slate-200/60 text-slate-700 flex items-center gap-1">
                                <Clock className="w-3 h-3 text-slate-500" />
                                {stg.workload_hours_per_week} hrs/wk
                              </span>
                            )}
                            <span className="text-xs font-bold text-[#D6A84B]">
                              {stg.timeframe}
                            </span>
                          </div>
                        </div>

                        <div>
                          <h4 className="text-sm font-bold text-[#17233F]">
                            {stg.stage_name}
                          </h4>
                          <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                            {stg.objective}
                          </p>
                        </div>

                        {/* Target Competencies */}
                        {stg.target_competencies && stg.target_competencies.length > 0 && (
                          <div className="space-y-1 pt-1">
                            <span className="text-[10px] font-bold uppercase text-[#17233F] block tracking-wider">
                              Target Competencies
                            </span>
                            <div className="flex flex-wrap gap-1.5">
                              {stg.target_competencies.map((comp, cIdx) => (
                                <span
                                  key={cIdx}
                                  className="text-[10px] font-medium px-2 py-0.5 rounded bg-amber-50 text-amber-900 border border-amber-200"
                                >
                                  {comp}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Practical Action Tasks */}
                        <div className="space-y-1.5 pt-1">
                          <span className="text-[10px] font-bold uppercase text-[#17233F] block tracking-wider">
                            Practical Action Tasks
                          </span>
                          {(stg.practical_tasks && stg.practical_tasks.length > 0 ? stg.practical_tasks : stg.tasks).map((t, idx) => (
                            <div key={idx} className="flex items-start gap-1.5 text-xs text-slate-700">
                              <span className="text-[#D6A84B] font-bold shrink-0">•</span>
                              <span>{t}</span>
                            </div>
                          ))}
                        </div>

                        {/* Measurable Deliverables */}
                        {stg.measurable_deliverables && stg.measurable_deliverables.length > 0 && (
                          <div className="space-y-1.5 pt-1">
                            <span className="text-[10px] font-bold uppercase text-emerald-700 block tracking-wider">
                              Measurable Deliverables
                            </span>
                            {stg.measurable_deliverables.map((d, dIdx) => (
                              <div key={dIdx} className="flex items-start gap-1.5 text-xs text-slate-700">
                                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                                <span className="font-medium text-slate-800">{d}</span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Recommended Authentic Resources */}
                      {stg.recommended_resources && stg.recommended_resources.length > 0 && (
                        <div className="space-y-1.5 pt-2 border-t border-[#E6DFD1]">
                          <span className="text-[10px] font-bold uppercase text-[#7355D9] block tracking-wider flex items-center gap-1">
                            <BookOpen className="w-3 h-3 text-[#7355D9]" />
                            Verified Learning Resources
                          </span>
                          {stg.recommended_resources.map((res, idx) => (
                            <a
                              key={idx}
                              href={res.url || "#"}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="p-2 rounded-lg bg-white border border-[#E6DFD1] flex items-center justify-between text-xs text-slate-800 hover:border-[#D6A84B] transition-colors"
                            >
                              <div className="truncate pr-2">
                                <span className="font-semibold block truncate">
                                  {res.title || res.name}
                                </span>
                                <span className="text-[10px] text-slate-500">
                                  {res.provider || "Official Authority"} • {res.type || "Official Guide"}
                                </span>
                              </div>
                              <ExternalLink className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                            </a>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
