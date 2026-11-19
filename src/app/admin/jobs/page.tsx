"use client";

import React, { useState } from "react";
import { AdminShell } from "@/components/layout/AdminShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { BrandButton } from "@/components/ui/BrandButton";
import { mockJobListings } from "@/data/mock-data";
import { JobListing } from "@/types";
import { toast } from "sonner";
import { Briefcase, Plus, CheckCircle2, Trash2, Edit2, ExternalLink } from "lucide-react";

export default function AdminJobsPage() {
  const [jobs, setJobs] = useState<JobListing[]>(mockJobListings);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newCompany, setNewCompany] = useState("");
  const [newLocation, setNewLocation] = useState("Noida, NCR");
  const [newSalary, setNewSalary] = useState("₹45,000 - ₹55,000 / month");

  const handleDeleteJob = (id: string) => {
    setJobs(jobs.filter((j) => j.id !== id));
    toast.info("Job listing removed from verified pool.");
  };

  const handleAddJob = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle || !newCompany) return;

    const newJob: JobListing = {
      id: `job-${Date.now()}`,
      title: newTitle,
      company: newCompany,
      location: newLocation,
      salaryRange: newSalary,
      employmentType: "Full-time",
      experienceLevel: "2-4 years",
      requiredSkills: ["Quality Inspection", "Lockstitch Operation"],
      source: "Manual Admin Verified Listing",
      postedDate: new Date().toISOString().split("T")[0],
      matchScore: 90,
      matchingSkills: ["Quality Inspection"],
      missingSkills: [],
      matchExplanation: "Manually entered job listing.",
      description: "Direct recruitment for verified vocational graduates.",
      responsibilities: ["Supervise line operations", "Maintain stitch specs"],
      qualifications: ["Hands-on trade experience recognized by Elevate X"],
      benefits: ["PF", "Health insurance"],
      employerInfo: {
        name: newCompany,
        about: "Verified hiring partner.",
        size: "500+ employees",
        industry: "Manufacturing",
      },
    };

    setJobs([newJob, ...jobs]);
    setShowAddModal(false);
    setNewTitle("");
    setNewCompany("");
    toast.success("New verified job listing published!");
  };

  return (
    <AdminShell>
      <div className="space-y-6">
        <PageHeader
          badge="Employer Opportunities"
          title="Verified Job Directory & Postings"
          description="Publish, audit, and calibrate formal sector opportunities tailored for candidates with verified trade experience."
          variant="navy"
          actions={
            <BrandButton
              variant="gold"
              size="sm"
              onClick={() => setShowAddModal(true)}
            >
              <Plus className="w-4 h-4 mr-1.5" />
              <span>Publish Verified Job</span>
            </BrandButton>
          }
        />

        <div className="space-y-3">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-xs flex items-center justify-between hover:border-[#D6A84B] transition-all"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-[#17233F]">{job.title}</h3>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30">
                    Verified Source
                  </span>
                </div>
                <p className="text-xs text-[#687187]">
                  {job.company} • {job.location} • <strong className="text-[#17233F]">{job.salaryRange}</strong>
                </p>
                <p className="text-[10px] text-[#687187]">Source: {job.source} • Posted: {job.postedDate}</p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleDeleteJob(job.id)}
                  className="p-2 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-[#687187] hover:text-[#C77B54] transition-colors"
                  title="Delete Listing"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {showAddModal && (
          <div className="fixed inset-0 z-50 bg-[#10192D]/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="max-w-md w-full p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-2xl space-y-4">
              <h3 className="text-base font-bold text-[#17233F]">Create Verified Job Listing</h3>
              <form onSubmit={handleAddJob} className="space-y-3 text-xs">
                <div className="space-y-1">
                  <label className="text-[#687187] font-semibold">Job Title</label>
                  <input
                    type="text"
                    required
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                    placeholder="e.g. Apparel Quality Assurance Specialist"
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[#687187] font-semibold">Company Name</label>
                  <input
                    type="text"
                    required
                    value={newCompany}
                    onChange={(e) => setNewCompany(e.target.value)}
                    placeholder="e.g. Raymond Lifestyle Exports"
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[#687187] font-semibold">Salary Range</label>
                  <input
                    type="text"
                    value={newSalary}
                    onChange={(e) => setNewSalary(e.target.value)}
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="px-4 py-2 rounded-xl text-xs font-semibold text-[#687187] hover:text-[#17233F]"
                  >
                    Cancel
                  </button>
                  <BrandButton type="submit" variant="gold" size="sm">
                    Publish Listing
                  </BrandButton>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AdminShell>
  );
}
