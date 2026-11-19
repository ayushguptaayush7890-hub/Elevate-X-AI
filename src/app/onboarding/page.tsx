"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Logo } from "@/components/ui/Logo";
import { useAuth } from "@/context/AuthContext";
import { toast } from "sonner";
import {
  User,
  GraduationCap,
  Briefcase,
  Sparkles,
  Target,
  CheckCircle2,
  ArrowRight,
  ArrowLeft,
  Save,
  Award
} from "lucide-react";

export default function OnboardingPage() {
  const router = useRouter();
  const { user, updateUser } = useAuth();
  const [currentStep, setCurrentStep] = useState(1);

  const [formData, setFormData] = useState({
    fullName: user.fullName || "Ramesh Sharma",
    ageRange: user.ageRange || "28-35",
    location: user.location || "New Delhi, India",
    preferredLanguage: user.preferredLanguage || "English",
    educationLevel: user.educationLevel || "Secondary School (10th Grade)",
    qualifications: "10th Matriculation, Workshop Apprenticeship",
    informalTraining: "Learned master tailoring from family workshop and local garment guild",
    currentOccupation: user.currentOccupation || "Master Tailor & Garment Artisan",
    yearsOfExperience: user.yearsOfExperience || 5,
    workDescription: user.workDescription || "Custom tailoring, pattern grading, machine maintenance, client consultations.",
    employmentType: user.employmentType || "Full-time",
    technicalSkills: "Industrial lockstitch machine, pattern drafting, measurement taking, seam troubleshooting",
    transferableSkills: "Client consultation, apprentice training, inventory management, bilingual communication",
    targetOccupation: "Apparel Quality Assurance Specialist",
    desiredSalaryMin: 35000,
    desiredSalaryMax: 55000,
    preferredWorkType: "Full-time",
  });

  const totalSteps = 6;
  const stepTitles = [
    "Personal Info",
    "Education",
    "Experience",
    "Skills",
    "Career Goals",
    "Review & Launch",
  ];

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    } else {
      updateUser({
        fullName: formData.fullName,
        location: formData.location,
        educationLevel: formData.educationLevel,
        currentOccupation: formData.currentOccupation,
        yearsOfExperience: Number(formData.yearsOfExperience),
        workDescription: formData.workDescription,
        desiredSalaryMin: Number(formData.desiredSalaryMin),
        desiredSalaryMax: Number(formData.desiredSalaryMax),
        profileCompleteness: 95,
      });
      toast.success("Profile setup complete! Welcome to your AI career dashboard.");
      router.push("/dashboard");
    }
  };

  const handleBack = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const handleSaveProgress = () => {
    toast.info("Progress saved to your browser session.");
  };

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A] py-10 px-4 sm:px-6 relative overflow-hidden">
      {/* Background Ambient Glows */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-[#D6A84B]/10 blur-[140px] pointer-events-none rounded-full" />
      <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-[#7355D9]/10 blur-[140px] pointer-events-none rounded-full" />

      <div className="max-w-3xl mx-auto space-y-8 relative z-10">
        {/* Top Header */}
        <div className="flex items-center justify-between">
          <Logo size="md" />
          <button
            onClick={handleSaveProgress}
            className="flex items-center gap-1.5 text-xs font-bold text-[#17233F] hover:text-[#D6A84B] px-3.5 py-1.5 rounded-xl border border-[#E6DFD1] bg-white shadow-xs transition-colors"
          >
            <Save className="w-3.5 h-3.5 text-[#D6A84B]" />
            <span>Save Progress</span>
          </button>
        </div>

        {/* Royal Gold Progress Timeline */}
        <div className="space-y-3">
          <div className="flex justify-between items-center text-xs font-bold">
            <span className="text-[#D6A84B]">
              Step {currentStep} of {totalSteps}: {stepTitles[currentStep - 1]}
            </span>
            <span className="text-[#687187] font-mono">
              {Math.round((currentStep / totalSteps) * 100)}% Complete
            </span>
          </div>

          {/* Timeline Nodes */}
          <div className="flex items-center gap-1.5 sm:gap-2">
            {[1, 2, 3, 4, 5, 6].map((step) => (
              <div
                key={step}
                className={`flex-1 h-2 rounded-full transition-all duration-300 ${
                  currentStep >= step
                    ? "bg-gradient-to-r from-[#D6A84B] to-[#F0D99B]"
                    : "bg-[#E6DFD1]"
                }`}
              />
            ))}
          </div>
        </div>

        {/* Step Content Card */}
        <div className="bg-white rounded-3xl p-6 sm:p-10 border border-[#E6DFD1] shadow-xl space-y-6">
          {/* STEP 1: Personal Information */}
          {currentStep === 1 && (
            <div className="space-y-5">
              <div className="flex items-center gap-3 pb-3 border-b border-[#E6DFD1]">
                <div className="p-2.5 rounded-xl bg-[#D6A84B]/15 text-[#D6A84B]">
                  <User className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-black text-[#17233F]">Personal Information</h2>
                  <p className="text-xs text-[#687187]">Tell us basic details so AI can localize opportunities</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Full Name</label>
                  <input
                    type="text"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Age Range</label>
                  <select
                    value={formData.ageRange}
                    onChange={(e) => setFormData({ ...formData, ageRange: e.target.value })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all cursor-pointer"
                  >
                    <option value="18-24">18 - 24 Years</option>
                    <option value="25-34">25 - 34 Years</option>
                    <option value="35-44">35 - 44 Years</option>
                    <option value="45+">45+ Years</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Primary City / Region</label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Language for Assessments</label>
                  <select
                    value={formData.preferredLanguage}
                    onChange={(e) => setFormData({ ...formData, preferredLanguage: e.target.value as "English" | "Hindi" })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all cursor-pointer"
                  >
                    <option value="English">English</option>
                    <option value="Hindi">हिन्दी (Hindi)</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* STEP 2: Education & Informal Training */}
          {currentStep === 2 && (
            <div className="space-y-5">
              <div className="flex items-center gap-3 pb-3 border-b border-[#E6DFD1]">
                <div className="p-2.5 rounded-xl bg-[#7355D9]/15 text-[#7355D9]">
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-black text-[#17233F]">Education & Apprenticeship</h2>
                  <p className="text-xs text-[#687187]">Formal schooling + workshop learning you received</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Highest Formal Schooling</label>
                  <select
                    value={formData.educationLevel}
                    onChange={(e) => setFormData({ ...formData, educationLevel: e.target.value })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all cursor-pointer"
                  >
                    <option value="No Formal Schooling">No Formal Schooling</option>
                    <option value="Primary (Up to 5th Grade)">Primary (Up to 5th Grade)</option>
                    <option value="Middle School (8th Grade)">Middle School (8th Grade)</option>
                    <option value="Secondary (10th Matric)">Secondary (10th Matric)</option>
                    <option value="Senior Secondary (12th)">Senior Secondary (12th)</option>
                    <option value="ITI / Vocational Diploma">ITI / Vocational Diploma</option>
                    <option value="Undergraduate Degree">Undergraduate Degree</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Informal Workshop or On-the-Job Apprenticeship</label>
                  <textarea
                    rows={3}
                    value={formData.informalTraining}
                    onChange={(e) => setFormData({ ...formData, informalTraining: e.target.value })}
                    placeholder="Describe how and where you learned your trade..."
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: Work Experience */}
          {currentStep === 3 && (
            <div className="space-y-5">
              <div className="flex items-center gap-3 pb-3 border-b border-[#E6DFD1]">
                <div className="p-2.5 rounded-xl bg-[#D6A84B]/15 text-[#D6A84B]">
                  <Briefcase className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-black text-[#17233F]">Work Experience</h2>
                  <p className="text-xs text-[#687187]">Tell us about your actual hands-on occupation</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Current Trade / Occupation</label>
                  <input
                    type="text"
                    value={formData.currentOccupation}
                    onChange={(e) => setFormData({ ...formData, currentOccupation: e.target.value })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Total Years in Practice</label>
                  <input
                    type="number"
                    min={0}
                    max={50}
                    value={formData.yearsOfExperience}
                    onChange={(e) => setFormData({ ...formData, yearsOfExperience: Number(e.target.value) })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-[#17233F]">Everyday Tasks & Responsibilities</label>
                <textarea
                  rows={3}
                  value={formData.workDescription}
                  onChange={(e) => setFormData({ ...formData, workDescription: e.target.value })}
                  className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                />
              </div>
            </div>
          )}

          {/* STEP 4: Practical Skills */}
          {currentStep === 4 && (
            <div className="space-y-5">
              <div className="flex items-center gap-3 pb-3 border-b border-[#E6DFD1]">
                <div className="p-2.5 rounded-xl bg-[#7355D9]/15 text-[#7355D9]">
                  <Sparkles className="w-5 h-5 text-[#36D6E8]" />
                </div>
                <div>
                  <h2 className="text-lg font-black text-[#17233F]">Practical & Tooling Skills</h2>
                  <p className="text-xs text-[#687187]">Machines, hand tools, and soft abilities you rely on</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Technical & Machine Skills</label>
                  <textarea
                    rows={2}
                    value={formData.technicalSkills}
                    onChange={(e) => setFormData({ ...formData, technicalSkills: e.target.value })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Communication & Problem Solving</label>
                  <textarea
                    rows={2}
                    value={formData.transferableSkills}
                    onChange={(e) => setFormData({ ...formData, transferableSkills: e.target.value })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 5: Career Goals */}
          {currentStep === 5 && (
            <div className="space-y-5">
              <div className="flex items-center gap-3 pb-3 border-b border-[#E6DFD1]">
                <div className="p-2.5 rounded-xl bg-[#27856B]/15 text-[#27856B]">
                  <Target className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-lg font-black text-[#17233F]">Career Transition Goals</h2>
                  <p className="text-xs text-[#687187]">What kind of formal role and wages are you targeting?</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5 sm:col-span-2">
                  <label className="text-xs font-bold text-[#17233F]">Target Formal Position</label>
                  <input
                    type="text"
                    value={formData.targetOccupation}
                    onChange={(e) => setFormData({ ...formData, targetOccupation: e.target.value })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Minimum Desired Salary (₹ / Mo)</label>
                  <input
                    type="number"
                    value={formData.desiredSalaryMin}
                    onChange={(e) => setFormData({ ...formData, desiredSalaryMin: Number(e.target.value) })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Expected Target Salary (₹ / Mo)</label>
                  <input
                    type="number"
                    value={formData.desiredSalaryMax}
                    onChange={(e) => setFormData({ ...formData, desiredSalaryMax: Number(e.target.value) })}
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>
              </div>
            </div>
          )}

          {/* STEP 6: Profile Review & Launch */}
          {currentStep === 6 && (
            <div className="space-y-5">
              <div className="flex items-center gap-3 pb-3 border-b border-[#E6DFD1]">
                <div className="p-2.5 rounded-xl bg-[#D6A84B]/15 text-[#D6A84B]">
                  <CheckCircle2 className="w-5 h-5 text-[#27856B]" />
                </div>
                <div>
                  <h2 className="text-lg font-black text-[#17233F]">Profile Review & Activation</h2>
                  <p className="text-xs text-[#687187]">Review your information before initializing AI models</p>
                </div>
              </div>

              <div className="space-y-3 text-xs divide-y divide-[#E6DFD1]">
                <div className="flex justify-between py-2">
                  <span className="text-[#687187]">Full Name:</span>
                  <span className="font-bold text-[#17233F]">{formData.fullName}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-[#687187]">Location:</span>
                  <span className="font-bold text-[#17233F]">{formData.location}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-[#687187]">Trade Experience:</span>
                  <span className="font-bold text-[#D6A84B]">{formData.currentOccupation} ({formData.yearsOfExperience} Years)</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-[#687187]">Target Transition Role:</span>
                  <span className="font-bold text-[#7355D9]">{formData.targetOccupation}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-[#687187]">Expected Monthly Range:</span>
                  <span className="font-bold text-[#27856B]">₹{formData.desiredSalaryMin.toLocaleString()} – ₹{formData.desiredSalaryMax.toLocaleString()}</span>
                </div>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="pt-4 border-t border-[#E6DFD1] flex items-center justify-between">
            {currentStep > 1 ? (
              <button
                type="button"
                onClick={handleBack}
                className="btn-navy px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-1.5 cursor-pointer"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Back</span>
              </button>
            ) : (
              <div />
            )}

            <button
              type="button"
              onClick={handleNext}
              className="btn-gold px-6 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 cursor-pointer shadow-md"
            >
              <span>{currentStep === totalSteps ? "Complete & Open Workspace" : "Continue"}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
