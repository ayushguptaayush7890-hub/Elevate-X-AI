"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { GlassCard } from "@/components/ui/GlassCard";
import { CircularProgress } from "@/components/ui/ProgressBar";
import { useAuth } from "@/context/AuthContext";
import { toast } from "sonner";
import {
  User,
  Award,
  Sparkles,
  Edit2,
  Save,
  CheckCircle2,
  Mail,
  Phone,
  MapPin,
  Briefcase,
  Layers,
  ShieldCheck
} from "lucide-react";

export default function ProfilePage() {
  const { user, updateUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    fullName: user.fullName,
    email: user.email,
    phone: user.phone,
    location: user.location,
    currentOccupation: user.currentOccupation,
    yearsOfExperience: user.yearsOfExperience,
    workDescription: user.workDescription,
    desiredSalaryMin: user.desiredSalaryMin,
    desiredSalaryMax: user.desiredSalaryMax,
  });

  const handleSave = () => {
    updateUser(formData);
    setIsEditing(false);
    toast.success("Profile saved with latest trade credentials!");
  };

  return (
    <AppShell>
      {/* 1. Royal Navy Profile Master Header */}
      <div className="relative rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-[#17233F] via-[#10192D] to-[#1F2F54] text-[#F5F0E6] overflow-hidden shadow-xl border border-[#D6A84B]/30">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-[#D6A84B]/10 to-transparent pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="flex flex-col sm:flex-row items-center sm:items-start gap-5">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-[#D6A84B] to-[#7355D9] flex items-center justify-center text-3xl font-black text-[#10192D] shrink-0 shadow-lg shadow-[#D6A84B]/20">
              {user.fullName.charAt(0)}
            </div>

            <div className="space-y-1.5 text-center sm:text-left">
              <div className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-[#D6A84B]/20 text-[#F0D99B] border border-[#D6A84B]/40 text-xs font-bold">
                <ShieldCheck className="w-3.5 h-3.5 text-[#D6A84B]" /> Candidate Master Record
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
                {formData.fullName}
              </h1>
              <p className="text-xs sm:text-sm text-[#D6A84B] font-bold">
                {formData.currentOccupation} • {formData.yearsOfExperience} Years Experience
              </p>

              <div className="flex flex-wrap items-center justify-center sm:justify-start gap-4 text-xs text-[#E6DFD1]/80 pt-1">
                <span className="flex items-center gap-1">
                  <Mail className="w-3.5 h-3.5 text-[#D6A84B]" /> {formData.email}
                </span>
                <span className="flex items-center gap-1">
                  <Phone className="w-3.5 h-3.5 text-[#D6A84B]" /> {formData.phone}
                </span>
                <span className="flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-[#D6A84B]" /> {formData.location}
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3 shrink-0 justify-center">
            {isEditing ? (
              <button
                onClick={handleSave}
                className="btn-gold px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-md cursor-pointer"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Save Profile</span>
              </button>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="btn-navy px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-1.5 cursor-pointer"
              >
                <Edit2 className="w-3.5 h-3.5 text-[#D6A84B]" />
                <span>Edit Details</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* 2. Gold Completion Ring & Overview Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Gold Completion Ring Card */}
        <GlassCard padding="lg" className="bg-white border border-[#E6DFD1] text-center space-y-4">
          <h3 className="text-sm font-black text-[#17233F]">Profile Readiness Score</h3>
          <div className="py-2 flex justify-center">
            <CircularProgress
              value={user.profileCompleteness}
              size={130}
              strokeWidth={10}
              label={`${user.profileCompleteness}%`}
              subtitle="Profile Complete"
            />
          </div>
          <p className="text-xs text-[#687187] leading-relaxed">
            Your profile details and verified trade accomplishments qualify for corporate export recruiters.
          </p>
        </GlassCard>

        {/* Cream Information Panels */}
        <GlassCard padding="lg" className="lg:col-span-2 bg-white border border-[#E6DFD1] space-y-5">
          <h3 className="text-sm font-black text-[#17233F] pb-2 border-b border-[#E6DFD1]">
            Workplace Experience & Scope
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs font-bold text-[#687187]">Current Role</label>
              {isEditing ? (
                <input
                  type="text"
                  value={formData.currentOccupation}
                  onChange={(e) => setFormData({ ...formData, currentOccupation: e.target.value })}
                  className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs text-[#17233F] focus:border-[#D6A84B] focus:outline-none"
                />
              ) : (
                <p className="text-xs font-black text-[#17233F] bg-[#FBF8F1] p-2.5 rounded-xl border border-[#E6DFD1]">
                  {formData.currentOccupation}
                </p>
              )}
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-[#687187]">Years of Hands-on Practice</label>
              {isEditing ? (
                <input
                  type="number"
                  value={formData.yearsOfExperience}
                  onChange={(e) => setFormData({ ...formData, yearsOfExperience: Number(e.target.value) })}
                  className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs text-[#17233F] focus:border-[#D6A84B] focus:outline-none"
                />
              ) : (
                <p className="text-xs font-black text-[#17233F] bg-[#FBF8F1] p-2.5 rounded-xl border border-[#E6DFD1]">
                  {formData.yearsOfExperience} Years Dedicated Trade Work
                </p>
              )}
            </div>

            <div className="space-y-1 sm:col-span-2">
              <label className="text-xs font-bold text-[#687187]">Tactile Work Description</label>
              {isEditing ? (
                <textarea
                  rows={3}
                  value={formData.workDescription}
                  onChange={(e) => setFormData({ ...formData, workDescription: e.target.value })}
                  className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs text-[#17233F] focus:border-[#D6A84B] focus:outline-none"
                />
              ) : (
                <p className="text-xs text-[#20243A] leading-relaxed bg-[#FBF8F1] p-3 rounded-xl border border-[#E6DFD1]">
                  {formData.workDescription}
                </p>
              )}
            </div>
          </div>
        </GlassCard>
      </div>

      {/* 3. Violet Skill Indicators Panel */}
      <GlassCard padding="lg" className="bg-white border border-[#E6DFD1] space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-[#E6DFD1]">
          <div>
            <h3 className="text-sm font-black text-[#17233F]">Identified Trade Competencies</h3>
            <p className="text-xs text-[#687187]">Recognized competencies aligned to NSQF and international standards</p>
          </div>
          <span className="text-xs font-bold text-[#D6A84B] bg-[#D6A84B]/15 px-3 py-1 rounded-full border border-[#D6A84B]/35">
            {user.skills.length} Validated Skills
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          {user.skills.map((skill) => (
            <div
              key={skill.id}
              className="p-3.5 rounded-2xl bg-[#FBF8F1] border border-[#E6DFD1] hover:border-[#7355D9] transition-all space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-md bg-[#7355D9]/15 text-[#5838BF] border border-[#7355D9]/30">
                  {skill.category}
                </span>
                <span className="text-[10px] font-black text-[#27856B] bg-[#27856B]/10 px-2 py-0.5 rounded-md">
                  {skill.confidence}% Verified
                </span>
              </div>
              <p className="text-xs font-black text-[#17233F]">{skill.name}</p>
              <p className="text-[10px] text-[#687187] line-clamp-1">{skill.evidence}</p>
            </div>
          ))}
        </div>
      </GlassCard>
    </AppShell>
  );
}
