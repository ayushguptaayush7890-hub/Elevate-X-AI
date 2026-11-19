"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { BrandButton } from "@/components/ui/BrandButton";
import { mockJobListings } from "@/data/mock-data";
import { JobListing } from "@/types";
import {
  Briefcase,
  Search,
  MapPin,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Building2,
  Bookmark,
  ShieldCheck
} from "lucide-react";
import { toast } from "sonner";

export default function JobsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedLocation, setSelectedLocation] = useState("All");
  const [selectedType, setSelectedType] = useState("All");
  const [minMatchScore, setMinMatchScore] = useState(70);
  const [savedJobs, setSavedJobs] = useState<string[]>([]);

  const toggleSaveJob = (id: string, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (savedJobs.includes(id)) {
      setSavedJobs(savedJobs.filter((jId) => jId !== id));
      toast.info("Job removed from saved list.");
    } else {
      setSavedJobs([...savedJobs, id]);
      toast.success("Job saved to your application tracker!");
    }
  };

  const filteredJobs = useMemo(() => {
    return mockJobListings.filter((job) => {
      const matchesSearch =
        job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.requiredSkills.some((s) => s.toLowerCase().includes(searchQuery.toLowerCase()));

      const matchesLocation =
        selectedLocation === "All" || job.location.includes(selectedLocation);

      const matchesType =
        selectedType === "All" || job.employmentType === selectedType;

      const matchesScore = job.matchScore >= minMatchScore;

      return matchesSearch && matchesLocation && matchesType && matchesScore;
    });
  }, [searchQuery, selectedLocation, selectedType, minMatchScore]);

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          badge="Explainable Career Matching"
          title="AI-Matched Career Opportunities"
          description="Curated formal sector positions evaluated against your verified and inferred trade competencies. Every match provides transparent, objective compatibility benchmarks."
          variant="navy"
          actions={
            <div className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40">
              <ShieldCheck className="w-4 h-4 text-[#D6A84B]" />
              <span>Vetted Formal Employers</span>
            </div>
          }
        />

        {/* Search & Multi-Criteria Filter Bar */}
        <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            {/* Keyword Search */}
            <div className="md:col-span-2 relative">
              <Search className="w-4 h-4 text-[#687187] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by job title, trade skill, or employer..."
                className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl pl-10 pr-4 py-2.5 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
              />
            </div>

            {/* Location Filter */}
            <div className="relative">
              <MapPin className="w-4 h-4 text-[#687187] absolute left-3.5 top-1/2 -translate-y-1/2" />
              <select
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl pl-10 pr-3 py-2.5 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
              >
                <option value="All">All Locations</option>
                <option value="Delhi">Delhi NCR</option>
                <option value="Noida">Noida</option>
                <option value="Gurugram">Gurugram</option>
              </select>
            </div>

            {/* Minimum Match Score Slider */}
            <div className="flex flex-col justify-center px-2">
              <div className="flex justify-between text-xs text-[#687187] mb-1">
                <span>Min Compatibility:</span>
                <span className="font-bold text-[#17233F]">{minMatchScore}%</span>
              </div>
              <input
                type="range"
                min={60}
                max={95}
                step={5}
                value={minMatchScore}
                onChange={(e) => setMinMatchScore(Number(e.target.value))}
                className="w-full accent-[#17233F] cursor-pointer"
              />
            </div>
          </div>
        </div>

        {/* Notice on Indicative Match */}
        <div className="text-xs text-[#687187] flex items-center gap-2 px-2">
          <Sparkles className="w-3.5 h-3.5 text-[#D6A84B] shrink-0" />
          <span>
            Compatibility ratings reflect algorithmic skill alignment and are objective benchmarks. Verified profiles receive priority employer visibility.
          </span>
        </div>

        {/* Jobs Listing Grid */}
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-[#687187] px-1">
            <span>
              Showing <strong className="text-[#17233F]">{filteredJobs.length}</strong> matched positions
            </span>
            <span>Sorted by Skill Compatibility</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredJobs.map((job) => (
              <Link key={job.id} href={`/jobs/${job.id}`} className="block group">
                <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm hover:border-[#D6A84B] hover:shadow-md transition-all space-y-4 h-full flex flex-col justify-between">
                  <div className="space-y-3">
                    {/* Top Bar: Title, Company, Match Badge */}
                    <div className="flex items-start justify-between gap-3">
                      <div className="space-y-1">
                        <h3 className="text-base font-bold text-[#17233F] group-hover:text-[#7355D9] transition-colors">
                          {job.title}
                        </h3>
                        <div className="flex items-center gap-2 text-xs text-[#687187]">
                          <span className="font-semibold text-[#20243A] flex items-center gap-1">
                            <Building2 className="w-3.5 h-3.5 text-[#D6A84B]" />
                            {job.company}
                          </span>
                          <span>•</span>
                          <span>{job.location}</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className="text-xs font-extrabold px-3 py-1 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]/40 shrink-0">
                          {job.matchScore}% Match
                        </span>
                        <button
                          onClick={(e) => toggleSaveJob(job.id, e)}
                          className={`p-2 rounded-xl border transition-colors ${
                            savedJobs.includes(job.id)
                              ? "bg-[#17233F] border-[#D6A84B] text-[#F0D99B]"
                              : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                          }`}
                          title="Save Job"
                        >
                          <Bookmark className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>

                    {/* Salary & Details */}
                    <div className="flex flex-wrap items-center gap-2 text-xs">
                      <span className="font-bold text-[#17233F] bg-[#F0D99B]/40 px-2.5 py-0.5 rounded-full border border-[#D6A84B]">
                        {job.salaryRange}
                      </span>
                      <span className="text-[#E6DFD1]">•</span>
                      <span className="text-[#687187] font-medium">{job.employmentType}</span>
                      <span className="text-[#E6DFD1]">•</span>
                      <span className="text-[#687187] font-medium">{job.experienceLevel} exp</span>
                    </div>

                    {/* Explainable Skill Alignment */}
                    <div className="p-4 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] space-y-2.5 text-xs">
                      <div className="space-y-1.5">
                        <span className="text-[10px] uppercase font-bold text-[#27856B] flex items-center gap-1 tracking-wider">
                          <CheckCircle2 className="w-3 h-3 text-[#27856B]" /> Matching Verified Skills:
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {job.matchingSkills.map((sk, i) => (
                            <span
                              key={i}
                              className="text-[11px] px-2.5 py-0.5 rounded-full bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30 font-medium"
                            >
                              {sk}
                            </span>
                          ))}
                        </div>
                      </div>

                      {job.missingSkills.length > 0 && (
                        <div className="space-y-1.5 pt-2 border-t border-[#E6DFD1]">
                          <span className="text-[10px] uppercase font-bold text-[#C77B54] flex items-center gap-1 tracking-wider">
                            <AlertCircle className="w-3 h-3 text-[#C77B54]" /> Bridgeable Gap Skills:
                          </span>
                          <div className="flex flex-wrap gap-1.5">
                            {job.missingSkills.map((sk, i) => (
                              <span
                                key={i}
                                className="text-[11px] px-2.5 py-0.5 rounded-full bg-[#C77B54]/10 text-[#C77B54] border border-[#C77B54]/20 font-medium"
                              >
                                {sk}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="pt-3 border-t border-[#E6DFD1] flex items-center justify-between text-xs font-bold text-[#7355D9] group-hover:text-[#17233F]">
                    <span>View Role Specifications</span>
                    <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
