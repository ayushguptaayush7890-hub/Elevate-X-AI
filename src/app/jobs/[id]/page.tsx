"use client";

import React, { useState, Suspense } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { mockJobListings } from "@/data/mock-data";
import { toast } from "sonner";
import {
  Briefcase,
  MapPin,
  Building2,
  CheckCircle2,
  AlertCircle,
  ArrowLeft,
  Sparkles,
  GitCompare,
  Mic,
  Bookmark,
  Send,
  ShieldCheck
} from "lucide-react";

function JobDetailsContent() {
  const params = useParams();
  const jobId = (params?.id as string) || "job-1";
  const [isApplied, setIsApplied] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [showApplyModal, setShowApplyModal] = useState(false);

  const job = mockJobListings.find((j) => j.id === jobId) || mockJobListings[0];

  const handleApply = () => {
    setIsApplied(true);
    setShowApplyModal(false);
    toast.success(`Application submitted to ${job.company} with your Elevate X verified profile!`);
  };

  return (
    <div className="space-y-6">
      {/* Back Link */}
      <Link
        href="/jobs"
        className="inline-flex items-center gap-2 text-xs font-bold text-[#687187] hover:text-[#17233F] transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Job Discovery
      </Link>

      {/* Main Header Card */}
      <div className="p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-5">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold px-3 py-1 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]">
                {job.matchScore}% Skills Match
              </span>
              <span className="text-xs text-[#687187]">
                Source: {job.source}
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-[#17233F] tracking-tight">
              {job.title}
            </h1>
            <div className="flex flex-wrap items-center gap-3 text-xs sm:text-sm text-[#687187]">
              <span className="font-bold text-[#17233F] flex items-center gap-1.5">
                <Building2 className="w-4 h-4 text-[#D6A84B]" /> {job.company}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1.5 text-[#687187]">
                <MapPin className="w-4 h-4 text-[#687187]" /> {job.location}
              </span>
              <span>•</span>
              <span className="font-extrabold text-[#17233F] bg-[#F0D99B]/40 px-2.5 py-0.5 rounded-full border border-[#D6A84B]">
                {job.salaryRange}
              </span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={() => {
                setIsSaved(!isSaved);
                toast.info(isSaved ? "Removed from saved" : "Job saved");
              }}
              className={`p-2.5 rounded-xl border transition-colors ${
                isSaved
                  ? "bg-[#17233F] border-[#D6A84B] text-[#F0D99B]"
                  : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
              }`}
              title="Save Job"
            >
              <Bookmark className="w-4 h-4" />
            </button>

            <BrandButton
              variant={isApplied ? "navy" : "gold"}
              onClick={() => setShowApplyModal(true)}
              size="md"
              disabled={isApplied}
            >
              <Send className="w-4 h-4 mr-1.5" />
              <span>{isApplied ? "Application Submitted" : "Apply with Verified Profile"}</span>
            </BrandButton>
          </div>
        </div>

        {/* Explainable Match Breakdown */}
        <div className="p-5 rounded-2xl bg-[#17233F] text-white border border-[#D6A84B]/30 space-y-2.5">
          <div className="flex items-center gap-2 text-xs font-bold text-[#F0D99B]">
            <Sparkles className="w-4 h-4 text-[#D6A84B]" /> Explainable Skill Match Analysis
          </div>
          <p className="text-xs sm:text-sm text-[#F5F0E6] leading-relaxed">
            {job.matchExplanation}
          </p>
          <div className="flex flex-wrap gap-4 pt-1 text-xs font-semibold">
            <Link href="/skill-gap" className="text-[#F0D99B] hover:underline flex items-center gap-1">
              <GitCompare className="w-3.5 h-3.5 text-[#D6A84B]" /> Analyze Skill Gap ({job.missingSkills.length} missing)
            </Link>
            <Link href="/interview" className="text-[#F5F0E6] hover:underline flex items-center gap-1">
              <Mic className="w-3.5 h-3.5 text-[#7355D9]" /> Prepare with AI Interview Lab
            </Link>
          </div>
        </div>
      </div>

      {/* Two Column Layout: Description & Sidebar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-6">
            <div className="space-y-3">
              <h2 className="text-sm font-bold text-[#17233F] uppercase tracking-wider">About the Role</h2>
              <p className="text-xs sm:text-sm text-[#20243A] leading-relaxed">{job.description}</p>
            </div>

            <div className="space-y-3">
              <h2 className="text-sm font-bold text-[#17233F] uppercase tracking-wider">Key Responsibilities</h2>
              <ul className="space-y-2 text-xs sm:text-sm text-[#20243A]">
                {job.responsibilities.map((resp, i) => (
                  <li key={i} className="flex items-start gap-2.5">
                    <span className="text-[#D6A84B] font-bold">›</span>
                    <span className="leading-relaxed">{resp}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h2 className="text-sm font-bold text-[#17233F] uppercase tracking-wider">Qualifications & Vocational Credentials</h2>
              <ul className="space-y-2 text-xs sm:text-sm text-[#20243A]">
                {job.qualifications.map((qual, i) => (
                  <li key={i} className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-[#27856B] shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{qual}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <h2 className="text-sm font-bold text-[#17233F] uppercase tracking-wider">Benefits & Compensation Perks</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-[#20243A]">
                {job.benefits.map((b, i) => (
                  <div key={i} className="p-3 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] flex items-center gap-2">
                    <span className="text-[#27856B] font-bold">✓</span> {b}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-5">
          <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <h3 className="text-xs font-bold text-[#17233F] uppercase tracking-wider">Employer Profile</h3>
            <div className="space-y-2 text-xs text-[#687187]">
              <p className="font-bold text-[#17233F] text-sm">{job.employerInfo.name}</p>
              <p className="leading-relaxed text-[#20243A]">{job.employerInfo.about}</p>
              <div className="pt-2 border-t border-[#E6DFD1] space-y-1 text-[#687187]">
                <p>Company Size: <strong className="text-[#17233F]">{job.employerInfo.size}</strong></p>
                <p>Industry: <strong className="text-[#17233F]">{job.employerInfo.industry}</strong></p>
              </div>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
            <h3 className="text-xs font-bold text-[#17233F] uppercase tracking-wider">Skill Matching Summary</h3>
            <div className="space-y-2">
              <div className="text-xs text-[#27856B] font-semibold flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#27856B]" /> {job.matchingSkills.length} Matching Verified Skills
              </div>
              <div className="text-xs text-[#C77B54] font-semibold flex items-center gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 text-[#C77B54]" /> {job.missingSkills.length} Suggested Additions
              </div>
            </div>
            <div className="pt-2">
              <BrandButton href="/skill-gap" variant="navy" fullWidth size="sm">
                Review Skill Gap Plan
              </BrandButton>
            </div>
          </div>
        </div>
      </div>

      {showApplyModal && (
        <div className="fixed inset-0 z-50 bg-[#10192D]/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="max-w-md w-full p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-2xl space-y-4 animate-in zoom-in-95 duration-200">
            <h3 className="text-lg font-bold text-[#17233F]">Confirm Job Application</h3>
            <p className="text-xs sm:text-sm text-[#687187] leading-relaxed">
              You are applying for <strong className="text-[#17233F]">{job.title}</strong> at <strong className="text-[#17233F]">{job.company}</strong>.
              Your Elevate X verified trade skills portfolio and latest ATS resume will be submitted directly to the hiring desk.
            </p>
            <div className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-xs text-[#20243A] space-y-1.5">
              <p>• <strong>Verified Competencies:</strong> Industrial Lockstitch (96%), Pattern Grading (90%)</p>
              <p>• <strong>Candidate Contact:</strong> ramesh.sharma@example.com</p>
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setShowApplyModal(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-[#687187] hover:text-[#17233F]"
              >
                Cancel
              </button>
              <BrandButton variant="gold" onClick={handleApply} size="sm">
                Confirm & Submit Application
              </BrandButton>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function JobDetailsPage() {
  return (
    <AppShell>
      <Suspense fallback={<div className="p-12 text-center text-xs text-[#687187]">Loading Job Specifications...</div>}>
        <JobDetailsContent />
      </Suspense>
    </AppShell>
  );
}
