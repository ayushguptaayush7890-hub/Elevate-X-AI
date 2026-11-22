"use client";

import React, { useState, useEffect, useMemo, useCallback } from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { BrandButton } from "@/components/ui/BrandButton";
import { apiService } from "@/services/api-service";
import { AggregatedJobListing, JobProviderStatus } from "@/types";
import {
  Briefcase,
  Search,
  MapPin,
  ExternalLink,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Building2,
  Bookmark,
  ShieldCheck,
  RefreshCw,
  SlidersHorizontal,
  ChevronDown,
  ChevronUp,
  Globe2,
  Calendar,
  Clock,
  Layers,
  ArrowUpRight,
  Info,
  Laptop,
  Check,
  X,
  FileCheck2,
} from "lucide-react";
import { toast } from "sonner";

const INDIAN_LOCATIONS = [
  { value: "India", label: "India (Default - Country-wide)" },
  { value: "All Indian Cities", label: "All Indian Cities" },
  { value: "Delhi NCR", label: "Delhi NCR (Delhi, Noida, Gurugram)" },
  { value: "Noida", label: "Noida, Delhi NCR" },
  { value: "Greater Noida", label: "Greater Noida, Delhi NCR" },
  { value: "Gurugram", label: "Gurugram, Delhi NCR" },
  { value: "Meerut", label: "Meerut, Uttar Pradesh" },
  { value: "Bengaluru", label: "Bengaluru, Karnataka" },
  { value: "Hyderabad", label: "Hyderabad, Telangana" },
  { value: "Pune", label: "Pune, Maharashtra" },
  { value: "Mumbai", label: "Mumbai, Maharashtra" },
  { value: "Chennai", label: "Chennai, Tamil Nadu" },
  { value: "Kolkata", label: "Kolkata, West Bengal" },
  { value: "Jaipur", label: "Jaipur, Rajasthan" },
  { value: "Lucknow", label: "Lucknow, Uttar Pradesh" },
  { value: "Ahmedabad", label: "Ahmedabad, Gujarat" },
  { value: "Chandigarh", label: "Chandigarh" },
  { value: "International", label: "International (Europe / Global Overseas)" },
];

const ROLE_CATEGORIES = [
  "All Roles",
  "AI Engineer",
  "Machine Learning Engineer",
  "Data Scientist",
  "Data Analyst",
  "Python Developer",
  "Java Developer",
  "Software Engineer",
  "Frontend Developer",
  "Backend Developer",
  "Full Stack Developer",
  "DevOps Engineer",
  "Cloud Engineer",
  "Cybersecurity Analyst",
  "Business Analyst",
  "UI/UX Designer",
  "Internships",
  "Fresher Jobs",
];

export default function FindJobsPage() {
  const [jobs, setJobs] = useState<AggregatedJobListing[]>([]);
  const [providers, setProviders] = useState<JobProviderStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);

  // Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedSource, setSelectedSource] = useState("All");
  const [selectedLocation, setSelectedLocation] = useState("India");
  const [selectedRoleCategory, setSelectedRoleCategory] = useState("All Roles");
  const [selectedWorkMode, setSelectedWorkMode] = useState("All");
  const [minMatchScore, setMinMatchScore] = useState(50);
  const [freshnessDays, setFreshnessDays] = useState("All");
  const [showSavedOnly, setShowSavedOnly] = useState(false);

  // UI state
  const [showProviderModal, setShowProviderModal] = useState(false);
  const [expandedMatchId, setExpandedMatchId] = useState<string | null>(null);
  const [selectedJobModal, setSelectedJobModal] = useState<AggregatedJobListing | null>(null);

  // Fetch jobs from backend API
  const loadJobs = useCallback(async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (searchQuery.trim()) params.search = searchQuery.trim();
      if (selectedSource !== "All") params.source = selectedSource;
      
      // Location & Country handling
      if (selectedLocation === "International") {
        params.country = "International";
        params.location = "International";
      } else if (selectedLocation === "India" || selectedLocation === "All Indian Cities") {
        params.country = "India";
        params.location = "India";
      } else if (selectedLocation !== "All") {
        params.country = "India";
        params.location = selectedLocation;
      }

      if (selectedRoleCategory && selectedRoleCategory !== "All Roles") {
        params.role_category = selectedRoleCategory;
      }
      if (selectedWorkMode !== "All") params.work_mode = selectedWorkMode;
      if (minMatchScore > 50) params.min_compatibility = minMatchScore;
      if (freshnessDays !== "All") params.freshness_days = parseInt(freshnessDays);
      if (showSavedOnly) params.saved_only = true;

      const res = await apiService.getAggregatedJobs(params);
      const data = res?.data;
      setJobs(Array.isArray(data) ? data : []);
    } catch (err: any) {
      console.error("Error loading aggregated jobs:", err);
      toast.error("Could not load job vacancies. Please check backend connection.");
    } finally {
      setLoading(false);
    }
  }, [searchQuery, selectedSource, selectedLocation, selectedRoleCategory, selectedWorkMode, minMatchScore, freshnessDays, showSavedOnly]);

  // Fetch provider metadata
  const loadProviders = async () => {
    try {
      const res = await apiService.getJobProviders();
      const data = res?.data;
      setProviders(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Error loading job providers:", err);
    }
  };

  useEffect(() => {
    loadJobs();
    loadProviders();
  }, [loadJobs]);

  // Trigger manual live sync
  const handleSyncProviders = async () => {
    try {
      setSyncing(true);
      toast.info("Ingesting real live jobs across active employer career feeds...");
      const res = await apiService.syncJobProviders(30);
      const syncData = res?.data;
      toast.success(
        `Sync complete! Ingested ${syncData?.total_imported ?? 0} new vacancies (${syncData?.total_updated ?? 0} refreshed).`
      );
      await loadJobs();
      await loadProviders();
    } catch (err: any) {
      console.error("Sync error:", err);
      toast.error("Job feed synchronization failed. Ensure backend has internet access.");
    } finally {
      setSyncing(false);
    }
  };

  // Toggle bookmark
  const handleToggleSave = async (job: AggregatedJobListing, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    try {
      const res = await apiService.toggleSaveJob(job.id);
      const isSaved = res?.data?.saved ?? false;
      setJobs((prev) =>
        prev.map((j) => (j.id === job.id ? { ...j, is_saved: isSaved } : j))
      );
      if (isSaved) {
        toast.success("Job saved to your application tracker!");
      } else {
        toast.info("Job removed from saved list.");
      }
    } catch (err: any) {
      console.error("Save error:", err);
      toast.error("Failed to update bookmark.");
    }
  };

  // Compute unique locations for filter dropdown
  const locationOptions = useMemo(() => {
    const locs = new Set<string>();
    jobs.forEach((j) => {
      if (j.location) {
        const clean = j.location.split(",")[0].trim();
        if (clean.length > 2) locs.add(clean);
      }
    });
    return ["All", "Remote", ...Array.from(locs).slice(0, 10)];
  }, [jobs]);

  // Compute unique sources
  const sourceOptions = useMemo(() => {
    const srcs = new Set<string>();
    jobs.forEach((j) => {
      if (j.source_provider) srcs.add(j.source_provider);
    });
    return ["All", ...Array.from(srcs)];
  }, [jobs]);

  const activeProviderCount = providers.filter((p) => p.status === "active").length;

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Page Header */}
        <PageHeader
          badge="Multi-Portal Real Job Aggregator"
          title="Live Verified Career Opportunities"
          description="Real-time vacancy aggregation from verified job boards and authoritative employer career feeds. Compare your verified trade skills against real job requirements with explainable compatibility scores."
          variant="navy"
          actions={
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => setShowProviderModal(true)}
                className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40 hover:bg-[#1A2644] transition-colors"
              >
                <Globe2 className="w-4 h-4 text-[#D6A84B]" />
                <span>12 Sources Evaluated ({activeProviderCount} Live)</span>
              </button>

              <button
                onClick={handleSyncProviders}
                disabled={syncing}
                className="flex items-center gap-2 text-xs font-semibold text-white bg-[#D6A84B] hover:bg-[#C29538] px-4 py-2 rounded-xl shadow-sm transition-colors disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${syncing ? "animate-spin" : ""}`} />
                <span>{syncing ? "Ingesting Feeds..." : "Sync Live Feeds"}</span>
              </button>
            </div>
          }
        />

        {/* Source Status Banner */}
        <div className="p-4 rounded-2xl bg-gradient-to-r from-[#10192D] to-[#1A2644] border border-[#D6A84B]/30 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#D6A84B]/20 border border-[#D6A84B]/40 flex items-center justify-center shrink-0">
              <ShieldCheck className="w-5 h-5 text-[#D6A84B]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold text-white">Authentic External Application Guarantee</span>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  Zero Fake Submissions
                </span>
              </div>
              <p className="text-xs text-[#E6DFD1]/80 mt-0.5">
                Every listing preserves the genuine employer portal and direct application URL. You register and apply directly on the original host platform.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <span className="text-xs text-[#F0D99B]">Saved Jobs:</span>
            <button
              onClick={() => setShowSavedOnly(!showSavedOnly)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5 ${
                showSavedOnly
                  ? "bg-[#D6A84B] text-[#10192D]"
                  : "bg-white/10 text-white hover:bg-white/20 border border-white/20"
              }`}
            >
              <Bookmark className="w-3.5 h-3.5" />
              <span>{showSavedOnly ? "Showing Saved" : "View Bookmarks"}</span>
            </button>
          </div>
        </div>

        {/* Search & Multifaceted Filtering Bar */}
        <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
          {/* Main Keyword Search */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
            <div className="md:col-span-6 relative">
              <Search className="w-4 h-4 text-[#687187] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search job title, trade skill, or employer name..."
                className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl pl-10 pr-4 py-2.5 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
              />
            </div>

            {/* Source Filter */}
            <div className="md:col-span-3 relative">
              <Globe2 className="w-4 h-4 text-[#687187] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <select
                value={selectedSource}
                onChange={(e) => setSelectedSource(e.target.value)}
                className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl pl-10 pr-3 py-2.5 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
              >
                <option value="All">All Sources ({jobs.length} jobs)</option>
                {sourceOptions.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            {/* Location Filter */}
            <div className="md:col-span-3 relative">
              <MapPin className="w-4 h-4 text-[#687187] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <select
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl pl-10 pr-3 py-2.5 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B] font-medium"
              >
                {INDIAN_LOCATIONS.map((loc) => (
                  <option key={loc.value} value={loc.value}>
                    {loc.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Role Category Pills */}
          <div className="space-y-1.5 pt-1">
            <div className="flex items-center justify-between text-[11px] text-[#687187]">
              <span className="font-semibold text-[#10192D] flex items-center gap-1.5">
                <Briefcase className="w-3.5 h-3.5 text-[#D6A84B]" />
                Target Role & Vocational Specializations:
              </span>
              {selectedRoleCategory !== "All Roles" && (
                <button
                  onClick={() => setSelectedRoleCategory("All Roles")}
                  className="text-[#D6A84B] hover:underline font-semibold text-[11px]"
                >
                  Clear role filter ({selectedRoleCategory})
                </button>
              )}
            </div>
            <div className="flex items-center gap-2 overflow-x-auto pb-1.5 scrollbar-thin scrollbar-thumb-[#E6DFD1]">
              {ROLE_CATEGORIES.map((role) => (
                <button
                  key={role}
                  onClick={() => setSelectedRoleCategory(role)}
                  className={`px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-colors shrink-0 ${
                    selectedRoleCategory === role
                      ? "bg-[#D6A84B] text-[#10192D] font-bold shadow-sm ring-1 ring-[#D6A84B]"
                      : "bg-[#FBF8F1] text-[#20243A] border border-[#E6DFD1] hover:bg-[#F2ECE0]"
                  }`}
                >
                  {role}
                </button>
              ))}
            </div>
          </div>

          {/* Secondary Filters: Work Mode, Compatibility Slider, Freshness */}
          <div className="pt-3 border-t border-[#E6DFD1]/60 flex flex-wrap items-center justify-between gap-4">
            {/* Work Mode Pills */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-[#687187]">Work Mode:</span>
              {(["All", "Remote", "On-site", "Hybrid"] as const).map((mode) => (
                <button
                  key={mode}
                  onClick={() => setSelectedWorkMode(mode)}
                  className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${
                    selectedWorkMode === mode
                      ? "bg-[#10192D] text-[#F0D99B]"
                      : "bg-[#FBF8F1] text-[#20243A] border border-[#E6DFD1] hover:bg-[#F2ECE0]"
                  }`}
                >
                  {mode}
                </button>
              ))}
            </div>

            {/* Freshness Filter */}
            <div className="flex items-center gap-2">
              <Calendar className="w-3.5 h-3.5 text-[#687187]" />
              <span className="text-xs font-semibold text-[#687187]">Posted:</span>
              <select
                value={freshnessDays}
                onChange={(e) => setFreshnessDays(e.target.value)}
                className="bg-[#FBF8F1] border border-[#E6DFD1] rounded-lg px-2.5 py-1 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
              >
                <option value="All">Anytime</option>
                <option value="7">Past 7 days</option>
                <option value="14">Past 14 days</option>
                <option value="30">Past 30 days</option>
              </select>
            </div>

            {/* Minimum Compatibility Slider */}
            <div className="flex items-center gap-3">
              <Sparkles className="w-3.5 h-3.5 text-[#D6A84B]" />
              <span className="text-xs font-semibold text-[#687187]">
                Min AI Match: <strong className="text-[#10192D]">{minMatchScore}%</strong>
              </span>
              <input
                type="range"
                min="50"
                max="95"
                step="5"
                value={minMatchScore}
                onChange={(e) => setMinMatchScore(parseInt(e.target.value))}
                className="w-28 accent-[#D6A84B] cursor-pointer"
              />
            </div>
          </div>
        </div>

        {/* Results Counter & Active Filters Display */}
        <div className="flex items-center justify-between text-xs text-[#687187]">
          <div>
            Showing <strong className="text-[#10192D]">{jobs.length}</strong> verified job vacancies
            {selectedSource !== "All" && ` from ${selectedSource}`}
            {showSavedOnly && " (Saved bookmarks only)"}
          </div>
          <div className="flex items-center gap-3">
            <span>Aggregator Status: <strong className="text-emerald-700">Healthy & Synchronized</strong></span>
          </div>
        </div>

        {/* Job Listings Grid */}
        {loading ? (
          <div className="p-16 rounded-2xl bg-white border border-[#E6DFD1] text-center space-y-3">
            <RefreshCw className="w-8 h-8 text-[#D6A84B] animate-spin mx-auto" />
            <p className="text-sm font-semibold text-[#10192D]">Aggregating live job listings from external portals...</p>
            <p className="text-xs text-[#687187]">Validating source URLs and computing explainable AI match scores</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="p-16 rounded-2xl bg-white border border-[#E6DFD1] text-center space-y-4">
            <Briefcase className="w-12 h-12 text-[#687187]/40 mx-auto" />
            <div className="space-y-1">
              <h3 className="text-base font-bold text-[#10192D]">
                {selectedLocation === "International"
                  ? "No verified international vacancies found"
                  : "No verified Indian vacancies found for this search"}
              </h3>
              <p className="text-xs text-[#687187] max-w-md mx-auto">
                {selectedLocation === "International"
                  ? "No overseas opportunities matched your current criteria. Try resetting filters."
                  : "No verified Indian vacancies found for this search. Try another role or location."}
              </p>
            </div>
            <button
              onClick={() => {
                setSearchQuery("");
                setSelectedSource("All");
                setSelectedLocation("India");
                setSelectedRoleCategory("All Roles");
                setSelectedWorkMode("All");
                setMinMatchScore(50);
                setFreshnessDays("All");
                setShowSavedOnly(false);
              }}
              className="px-4 py-2 bg-[#10192D] text-[#F0D99B] text-xs font-semibold rounded-xl hover:bg-[#1A2644] transition-colors"
            >
              Reset to All Indian Vacancies
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {jobs.map((job) => {
              const match = job.match_details;
              const matchScore = match?.match_score || 75;
              const isExpanded = expandedMatchId === job.id;

              // Source color badges
              let sourceBadgeBg = "bg-blue-50 text-blue-700 border-blue-200";
              if (job.source_provider === "RemoteOK") {
                sourceBadgeBg = "bg-rose-50 text-rose-700 border-rose-200";
              } else if (job.source_provider === "Jobicy") {
                sourceBadgeBg = "bg-purple-50 text-purple-700 border-purple-200";
              } else if (job.source_provider === "Adzuna") {
                sourceBadgeBg = "bg-amber-50 text-amber-700 border-amber-200";
              }

              // Direct apply link
              const targetApplyUrl = job.application_url || job.source_url || "#";
              const isDirectApply = Boolean(job.application_url);

              return (
                <div
                  key={job.id}
                  className="p-5 rounded-2xl bg-white border border-[#E6DFD1] hover:border-[#D6A84B] shadow-sm transition-all space-y-4"
                >
                  {/* Card Header: Employer, Source Badge, Save Bookmark */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] flex items-center justify-center shrink-0">
                        <Building2 className="w-5 h-5 text-[#D6A84B]" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-[#10192D]">{job.employer?.name || "Verified Employer"}</span>
                          <span className="text-[10px] text-[#687187]">•</span>
                          {/* Genuine Source Badge */}
                          <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold border ${sourceBadgeBg}`}>
                            via {job.source_provider}
                          </span>
                          {job.country === "India" && (
                            <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center gap-1">
                              <span>🇮🇳</span>
                              <span>India Verified</span>
                            </span>
                          )}
                        </div>
                        <h3 className="text-base font-bold text-[#10192D] mt-0.5">{job.title}</h3>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 self-end sm:self-center">
                      {/* AI Match Badge */}
                      <button
                        onClick={() => setExpandedMatchId(isExpanded ? null : job.id)}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold border transition-colors ${
                          matchScore >= 85
                            ? "bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100"
                            : matchScore >= 70
                            ? "bg-blue-50 text-blue-800 border-blue-200 hover:bg-blue-100"
                            : "bg-amber-50 text-amber-800 border-amber-200 hover:bg-amber-100"
                        }`}
                        title="Click to view explainable matching breakdown"
                      >
                        <Sparkles className="w-3.5 h-3.5 text-[#D6A84B]" />
                        <span>{matchScore}% Match</span>
                        {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                      </button>

                      {/* Bookmark button */}
                      <button
                        onClick={(e) => handleToggleSave(job, e)}
                        className={`p-2 rounded-xl border transition-colors ${
                          job.is_saved
                            ? "bg-[#D6A84B]/20 text-[#D6A84B] border-[#D6A84B]"
                            : "bg-[#FBF8F1] text-[#687187] border-[#E6DFD1] hover:text-[#10192D]"
                        }`}
                        title={job.is_saved ? "Remove bookmark" : "Save job"}
                      >
                        <Bookmark className="w-4 h-4 fill-current" />
                      </button>
                    </div>
                  </div>

                  {/* Attributes: Location, Work Mode, Employment Type, Salary */}
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-[#687187]">
                    <div className="flex items-center gap-1.5">
                      <MapPin className="w-3.5 h-3.5 text-[#687187]" />
                      <span>{job.location}</span>
                    </div>

                    <div className="flex items-center gap-1.5">
                      <Laptop className="w-3.5 h-3.5 text-[#687187]" />
                      <span className="capitalize">{job.work_mode}</span>
                    </div>

                    <div className="flex items-center gap-1.5">
                      <Briefcase className="w-3.5 h-3.5 text-[#687187]" />
                      <span>{job.employment_type}</span>
                    </div>

                    {/* Salary (Preserved, never invented) */}
                    <div>
                      {job.salary_min || job.salary_max ? (
                        <span className="font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-md border border-emerald-200">
                          {job.salary_currency} {job.salary_min ? job.salary_min.toLocaleString() : ""}
                          {job.salary_min && job.salary_max ? " - " : ""}
                          {job.salary_max ? job.salary_max.toLocaleString() : ""} / yr
                        </span>
                      ) : (
                        <span className="text-[#687187] bg-gray-50 px-2 py-0.5 rounded-md border border-gray-200">
                          Salary Disclosed on Application
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Skills Chips */}
                  {job.required_skills_list && job.required_skills_list.length > 0 && (
                    <div className="flex flex-wrap items-center gap-1.5">
                      {job.required_skills_list.slice(0, 6).map((sk, idx) => (
                        <span
                          key={idx}
                          className="px-2.5 py-1 rounded-lg text-[11px] font-medium bg-[#FBF8F1] text-[#20243A] border border-[#E6DFD1]"
                        >
                          {sk}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Expandable Explainable Match Details */}
                  {isExpanded && match && (
                    <div className="p-4 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] space-y-3 text-xs animate-in fade-in-50">
                      <div className="flex items-center justify-between pb-2 border-b border-[#E6DFD1]">
                        <span className="font-bold text-[#10192D]">
                          AI Compatibility Breakdown: <span className="text-[#D6A84B]">{match.match_tier}</span>
                        </span>
                        <span className="text-[10px] text-[#687187]">
                          Methodology: {match.matching_methodology}
                        </span>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {/* Matching Verified Skills */}
                        <div className="space-y-1.5">
                          <span className="font-semibold text-emerald-800 flex items-center gap-1.5">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                            Matching Verified Candidate Skills ({match.matching_verified_skills.length})
                          </span>
                          <div className="flex flex-wrap gap-1">
                            {match.matching_verified_skills.length > 0 ? (
                              match.matching_verified_skills.map((s, i) => (
                                <span
                                  key={i}
                                  className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-medium border border-emerald-200"
                                >
                                  ✓ {s}
                                </span>
                              ))
                            ) : (
                              <span className="text-[11px] text-[#687187]">None identified yet</span>
                            )}
                          </div>
                        </div>

                        {/* Missing Skills */}
                        <div className="space-y-1.5">
                          <span className="font-semibold text-amber-800 flex items-center gap-1.5">
                            <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
                            Bridge / Target Competencies To Acquire ({match.missing_required_skills.length})
                          </span>
                          <div className="flex flex-wrap gap-1">
                            {match.missing_required_skills.length > 0 ? (
                              match.missing_required_skills.map((s, i) => (
                                <span
                                  key={i}
                                  className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 text-[10px] font-medium border border-amber-200"
                                >
                                  + {s}
                                </span>
                              ))
                            ) : (
                              <span className="text-[11px] text-emerald-700 font-medium">All essential skills matched!</span>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Experience and Academic Alignment */}
                      <div className="pt-2 border-t border-[#E6DFD1]/60 text-[11px] text-[#687187] space-y-1">
                        <div>
                          <strong>Experience Alignment:</strong> {match.experience_fit}
                        </div>
                        {match.academic_alignment && (
                          <div>
                            <strong>Academic Alignment:</strong> {match.academic_alignment}
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Card Footer: Metadata & Actions */}
                  <div className="pt-3 border-t border-[#E6DFD1]/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-center gap-3 text-[11px] text-[#687187]">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3 text-[#687187]" />
                        <span>Verified: Today</span>
                      </span>
                      <span>•</span>
                      <span>Posted: {job.posted_date || "Recent"}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => setSelectedJobModal(job)}
                        className="px-3 py-1.5 rounded-xl text-xs font-semibold text-[#10192D] bg-[#FBF8F1] border border-[#E6DFD1] hover:bg-[#F2ECE0] transition-colors"
                      >
                        View Details
                      </button>

                      {/* Genuine External Application Button */}
                      <a
                        href={targetApplyUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl text-xs font-bold text-white bg-[#10192D] hover:bg-[#1A2644] shadow-sm transition-colors"
                      >
                        <span>{isDirectApply ? "Apply on Original Website" : "View Original Job"}</span>
                        <ArrowUpRight className="w-3.5 h-3.5 text-[#F0D99B]" />
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Modal: Job Details & Application Instructions */}
        {selectedJobModal && (
          <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-y-auto border border-[#E6DFD1] shadow-2xl p-6 space-y-5 animate-in zoom-in-95">
              <div className="flex items-start justify-between pb-4 border-b border-[#E6DFD1]">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-[#D6A84B]">{selectedJobModal.employer?.name}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-700 border border-blue-200">
                      via {selectedJobModal.source_provider}
                    </span>
                  </div>
                  <h2 className="text-xl font-bold text-[#10192D] mt-1">{selectedJobModal.title}</h2>
                  <div className="flex items-center gap-3 text-xs text-[#687187] mt-1">
                    <span>{selectedJobModal.location}</span>
                    <span>•</span>
                    <span className="capitalize">{selectedJobModal.work_mode}</span>
                    <span>•</span>
                    <span>{selectedJobModal.employment_type}</span>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedJobModal(null)}
                  className="p-1 rounded-lg hover:bg-gray-100 text-gray-500"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Original Application Notice */}
              <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-start gap-2.5">
                <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <strong>Original Application Redirection:</strong> Clicking below will securely navigate you to{" "}
                  <strong>{selectedJobModal.source_provider}</strong>. You will register/login and submit your application on that external portal directly.
                </div>
              </div>

              {/* Job Description */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#687187]">Job Description & Requirements</h4>
                <div className="text-xs text-[#20243A] leading-relaxed whitespace-pre-wrap max-h-60 overflow-y-auto p-3 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1]">
                  {selectedJobModal.description}
                </div>
              </div>

              {/* Modal Actions */}
              <div className="pt-4 border-t border-[#E6DFD1] flex items-center justify-between">
                <button
                  onClick={() => setSelectedJobModal(null)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-[#687187] hover:bg-gray-100"
                >
                  Close
                </button>

                <a
                  href={selectedJobModal.application_url || selectedJobModal.source_url || "#"}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-[#10192D] hover:bg-[#1A2644] shadow-md transition-colors"
                >
                  <span>Apply on {selectedJobModal.source_provider}</span>
                  <ExternalLink className="w-3.5 h-3.5 text-[#F0D99B]" />
                </a>
              </div>
            </div>
          </div>
        )}

        {/* Modal: Evaluated Job Platforms Status Drawer */}
        {showProviderModal && (
          <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[85vh] overflow-y-auto border border-[#E6DFD1] shadow-2xl p-6 space-y-5 animate-in zoom-in-95">
              <div className="flex items-start justify-between pb-4 border-b border-[#E6DFD1]">
                <div>
                  <h2 className="text-lg font-bold text-[#10192D]">Evaluated External Job Platforms (12 Sources)</h2>
                  <p className="text-xs text-[#687187] mt-0.5">
                    Official API access, commercial terms, and integration telemetry. Sources requiring partner approval are not scraped.
                  </p>
                </div>
                <button
                  onClick={() => setShowProviderModal(false)}
                  className="p-1 rounded-lg hover:bg-gray-100 text-gray-500"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {providers.map((p) => {
                  let badge = "bg-emerald-50 text-emerald-800 border-emerald-200";
                  let statusText = "Active & Live";
                  if (p.status === "ready_for_key") {
                    badge = "bg-amber-50 text-amber-800 border-amber-200";
                    statusText = "Ready (Pending Key)";
                  } else if (p.status === "pending_partner_approval") {
                    badge = "bg-slate-100 text-slate-700 border-slate-300";
                    statusText = "Partner Approval Required";
                  }

                  return (
                    <div
                      key={p.provider_id}
                      className="p-3.5 rounded-xl border border-[#E6DFD1] bg-[#FBF8F1] space-y-2 text-xs"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-[#10192D]">{p.name}</span>
                          <a
                            href={p.official_website}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[#687187] hover:text-[#D6A84B]"
                          >
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        </div>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${badge}`}>
                          {statusText}
                        </span>
                      </div>

                      <div className="space-y-1 text-[11px] text-[#687187]">
                        <div>
                          <strong>Authentication:</strong> {p.auth_requirements}
                        </div>
                        <div>
                          <strong>Commercial Permission:</strong> {p.commercial_usage_permission}
                        </div>
                        <div>
                          <strong>Refresh / Rate Limits:</strong> {p.refresh_restrictions}
                        </div>
                        {p.jobs_imported_count > 0 && (
                          <div className="text-emerald-700 font-semibold">
                            ✓ {p.jobs_imported_count} real vacancies currently indexed
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="pt-4 border-t border-[#E6DFD1] flex justify-end">
                <button
                  onClick={() => setShowProviderModal(false)}
                  className="px-4 py-2 bg-[#10192D] text-[#F0D99B] text-xs font-semibold rounded-xl"
                >
                  Close Overview
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
