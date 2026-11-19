"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { BrandButton } from "@/components/ui/BrandButton";
import { mockApplications } from "@/data/mock-data";
import { JobApplication } from "@/types";
import { toast } from "sonner";
import {
  Kanban,
  Plus,
  Building2,
  Trash2,
  Briefcase
} from "lucide-react";

type ColumnKey = "saved" | "applied" | "interview" | "shortlisted" | "rejected" | "offer";

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<JobApplication[]>(mockApplications);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newAppTitle, setNewAppTitle] = useState("");
  const [newAppCompany, setNewAppCompany] = useState("");
  const [newAppSalary, setNewAppSalary] = useState("₹40,000 / month");
  const [newAppLocation, setNewAppLocation] = useState("Delhi NCR");

  const columns: { key: ColumnKey; label: string; tagClass: string }[] = [
    { key: "saved", label: "Saved Jobs", tagClass: "bg-[#F5F0E6] text-[#17233F] border-[#E6DFD1]" },
    { key: "applied", label: "Applied", tagClass: "bg-[#17233F] text-white border-[#17233F]" },
    { key: "interview", label: "Interview", tagClass: "bg-[#7355D9]/15 text-[#7355D9] border-[#7355D9]/30" },
    { key: "shortlisted", label: "Shortlisted", tagClass: "bg-[#F0D99B]/40 text-[#17233F] border-[#D6A84B]" },
    { key: "offer", label: "Offer Received", tagClass: "bg-[#DCEAE6] text-[#27856B] border-[#27856B]/30" },
    { key: "rejected", label: "Archived", tagClass: "bg-[#FBF8F1] text-[#687187] border-[#E6DFD1]" },
  ];

  const handleMoveStatus = (appId: string, nextStatus: ColumnKey) => {
    setApplications((prev) =>
      prev.map((app) => (app.id === appId ? { ...app, status: nextStatus, lastUpdated: "Just now" } : app))
    );
    toast.success(`Application updated to ${nextStatus.toUpperCase()}`);
  };

  const handleDelete = (appId: string) => {
    setApplications((prev) => prev.filter((a) => a.id !== appId));
    toast.info("Application deleted.");
  };

  const handleAddApplication = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAppTitle || !newAppCompany) return;

    const newApp: JobApplication = {
      id: `app-${Date.now()}`,
      jobId: `job-${Date.now()}`,
      jobTitle: newAppTitle,
      company: newAppCompany,
      location: newAppLocation,
      salary: newAppSalary,
      status: "saved",
      appliedDate: "—",
      lastUpdated: "Just now",
      matchScore: 88,
      notes: "Custom entry created in application tracker.",
    };

    setApplications([...applications, newApp]);
    setShowAddModal(false);
    setNewAppTitle("");
    setNewAppCompany("");
    toast.success("New job application added to board.");
  };

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          badge="Pipeline Management"
          title="Job Application Kanban Tracker"
          description="Manage your formal recruitment pipeline, track scheduled interview rounds, record notes, and monitor offers."
          variant="navy"
          actions={
            <BrandButton
              variant="gold"
              size="sm"
              onClick={() => setShowAddModal(true)}
            >
              <Plus className="w-4 h-4 mr-1.5" />
              <span>Add Custom Application</span>
            </BrandButton>
          }
        />

        {/* Kanban Board Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 overflow-x-auto pb-6">
          {columns.map((col) => {
            const colApps = applications.filter((a) => a.status === col.key);
            return (
              <div
                key={col.key}
                className="space-y-3 min-w-[200px] p-3.5 rounded-2xl bg-white border border-[#E6DFD1] shadow-xs flex flex-col"
              >
                {/* Column Header */}
                <div className="flex items-center justify-between pb-2.5 border-b border-[#E6DFD1]">
                  <span className={`text-[11px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded-md border ${col.tagClass}`}>
                    {col.label}
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#17233F] text-[#F0D99B]">
                    {colApps.length}
                  </span>
                </div>

                {/* Cards in Column */}
                <div className="space-y-3 flex-1">
                  {colApps.map((app) => (
                    <div
                      key={app.id}
                      className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] space-y-2.5 text-xs hover:border-[#D6A84B] transition-all shadow-xs"
                    >
                      <div className="flex items-start justify-between gap-1">
                        <h4 className="font-bold text-[#17233F] text-xs leading-snug">{app.jobTitle}</h4>
                        <button
                          onClick={() => handleDelete(app.id)}
                          className="text-[#687187] hover:text-[#C77B54] transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>

                      <p className="text-xs text-[#20243A] flex items-center gap-1 font-medium">
                        <Building2 className="w-3.5 h-3.5 text-[#D6A84B]" /> {app.company}
                      </p>

                      <div className="flex items-center justify-between text-[11px] text-[#687187] pt-1.5 border-t border-[#E6DFD1]">
                        <span className="font-bold text-[#17233F]">{app.salary}</span>
                        <span className="font-bold text-[#7355D9]">{app.matchScore}% Fit</span>
                      </div>

                      {app.notes && (
                        <p className="text-[10px] text-[#20243A] bg-white p-2 rounded-lg border border-[#E6DFD1] italic">
                          {app.notes}
                        </p>
                      )}

                      {/* Quick Move Action */}
                      <div className="pt-1 flex items-center gap-1.5 text-xs">
                        <span className="text-[#687187] text-[11px]">Move:</span>
                        <select
                          value={app.status}
                          onChange={(e) => handleMoveStatus(app.id, e.target.value as ColumnKey)}
                          className="bg-white border border-[#E6DFD1] text-[#20243A] rounded-lg px-2 py-0.5 text-xs focus:outline-none focus:border-[#D6A84B]"
                        >
                          {columns.map((c) => (
                            <option key={c.key} value={c.key}>
                              {c.label}
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>
                  ))}

                  {colApps.length === 0 && (
                    <div className="p-4 rounded-xl border border-dashed border-[#E6DFD1] text-center text-xs text-[#687187]">
                      No applications
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Add Modal */}
        {showAddModal && (
          <div className="fixed inset-0 z-50 bg-[#10192D]/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="max-w-md w-full p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-2xl space-y-4">
              <h3 className="text-base font-bold text-[#17233F]">Add Job Application</h3>
              <form onSubmit={handleAddApplication} className="space-y-3 text-xs">
                <div className="space-y-1">
                  <label className="text-[#687187] font-semibold">Job Title</label>
                  <input
                    type="text"
                    required
                    value={newAppTitle}
                    onChange={(e) => setNewAppTitle(e.target.value)}
                    placeholder="e.g. Master Tailor or QA Inspector"
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[#687187] font-semibold">Company Name</label>
                  <input
                    type="text"
                    required
                    value={newAppCompany}
                    onChange={(e) => setNewAppCompany(e.target.value)}
                    placeholder="e.g. Raymond Lifestyle Exports"
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                  />
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div className="space-y-1">
                    <label className="text-[#687187] font-semibold">Location</label>
                    <input
                      type="text"
                      value={newAppLocation}
                      onChange={(e) => setNewAppLocation(e.target.value)}
                      className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-[#687187] font-semibold">Offered / Target Salary</label>
                    <input
                      type="text"
                      value={newAppSalary}
                      onChange={(e) => setNewAppSalary(e.target.value)}
                      className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                    />
                  </div>
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="px-4 py-2 rounded-xl text-[#687187] font-semibold hover:text-[#17233F]"
                  >
                    Cancel
                  </button>
                  <BrandButton type="submit" variant="gold" size="sm">
                    Save to Pipeline
                  </BrandButton>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
