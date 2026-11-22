"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";
import {
  CheckCircle2,
  AlertTriangle,
  Edit2,
  Sparkles,
  ArrowLeft,
  User,
  GraduationCap,
  Code2,
  Briefcase,
  FolderGit2,
  Award,
  Layers,
  ArrowRight,
} from "lucide-react";

interface Props {
  resume: ResumeFullData;
  onEditStep: (stepNumber: number) => void;
  onGenerateAI: () => void;
  onBackToStep7: () => void;
  isGenerating: boolean;
}

export function ResumeReviewStep({
  resume,
  onEditStep,
  onGenerateAI,
  onBackToStep7,
  isGenerating,
}: Props) {
  const info = resume?.personalInfo || ({} as any);
  const education = resume?.education || [];
  const skills = resume?.skills || ({} as any);
  const experience = resume?.experience || [];
  const internships = resume?.internships || [];
  const projects = resume?.projects || [];
  const certifications = resume?.certifications || [];
  const additional = resume?.additional || ({} as any);

  // Validation
  const errors: string[] = [];
  if (!info?.fullName?.trim()) errors.push("Full Name is required.");
  if (!info?.email?.trim()) errors.push("Contact Email is required.");
  if (!info?.phone?.trim()) errors.push("Contact Phone number is required.");
  if (!info?.professionalTitle?.trim()) errors.push("Professional Title is required.");

  const hasSkills =
    (skills?.programmingLanguages?.length || 0) > 0 ||
    (skills?.frameworks?.length || 0) > 0 ||
    (skills?.databases?.length || 0) > 0 ||
    (skills?.developerTools?.length || 0) > 0 ||
    (skills?.aiMlSkills?.length || 0) > 0 ||
    (skills?.otherSkills?.length || 0) > 0;

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Review Header Banner */}
      <div className="bg-gradient-to-r from-[#17233F] via-[#241E4E] to-[#17233F] rounded-3xl p-6 sm:p-8 text-white shadow-xl border border-[#D6A84B]/20">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#D6A84B]/20 border border-[#D6A84B]/40 text-[#D6A84B] text-xs font-bold uppercase tracking-wider">
              <CheckCircle2 className="w-3.5 h-3.5" /> Step 8 of 8 • Information Review
            </div>
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight">
              Review Your Information Before Generation
            </h1>
            <p className="text-sm text-slate-300 leading-relaxed max-w-2xl">
              Inspect your verified facts below. Missing optional fields are left empty and will never be fabricated.
              When ready, click <strong>Generate My Resume</strong> to format summaries, craft STAR bullet points, and explore 1000+ tailored designs.
            </p>
          </div>

          <button
            onClick={onGenerateAI}
            disabled={errors.length > 0 || isGenerating}
            className={`px-8 py-4 rounded-2xl font-black text-xs uppercase tracking-wider flex items-center gap-3 transition-all cursor-pointer shadow-xl shrink-0 ${
              errors.length > 0 || isGenerating
                ? "bg-slate-700 text-slate-400 cursor-not-allowed opacity-60"
                : "bg-gradient-to-r from-[#D6A84B] via-[#F0D99B] to-[#D6A84B] text-[#17233F] hover:shadow-[#D6A84B]/30 hover:scale-[1.02] shadow-[#D6A84B]/20"
            }`}
          >
            {isGenerating ? (
              <>
                <div className="w-4 h-4 border-2 border-[#17233F] border-t-transparent rounded-full animate-spin" />
                Generating with AI...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-[#7355D9]" />
                Generate My Resume <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Validation Warnings if any */}
      {errors.length > 0 && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-xs uppercase tracking-wider">Missing Required Fields</h4>
            <ul className="list-disc pl-4 text-xs mt-1 space-y-0.5">
              {errors.map((err, idx) => (
                <li key={idx}>{err}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Review Cards Grid */}
      <div className="space-y-4">
        {/* Section 1: Personal Information */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <User className="w-4 h-4 text-[#7355D9]" />
              <h3 className="font-black text-xs uppercase tracking-wider text-slate-800">1. Personal Details</h3>
            </div>
            <button
              onClick={() => onEditStep(1)}
              className="px-2.5 py-1 rounded-lg text-[11px] font-bold text-[#7355D9] hover:bg-[#7355D9]/10 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Edit2 className="w-3 h-3" /> Edit
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
            <div><span className="text-slate-400 block text-[10px] uppercase font-bold">Full Name</span><span className="font-semibold text-slate-800">{info.fullName || "—"}</span></div>
            <div><span className="text-slate-400 block text-[10px] uppercase font-bold">Title</span><span className="font-semibold text-slate-800">{info.professionalTitle || "—"}</span></div>
            <div><span className="text-slate-400 block text-[10px] uppercase font-bold">Email</span><span className="font-semibold text-slate-800">{info.email || "—"}</span></div>
            <div><span className="text-slate-400 block text-[10px] uppercase font-bold">Phone</span><span className="font-semibold text-slate-800">{info.phone || "—"}</span></div>
            <div><span className="text-slate-400 block text-[10px] uppercase font-bold">Location</span><span className="font-semibold text-slate-800">{info.location || "—"}</span></div>
            <div><span className="text-slate-400 block text-[10px] uppercase font-bold">LinkedIn</span><span className="font-semibold text-slate-800 truncate block">{info.linkedIn || "—"}</span></div>
          </div>
          {info.summary && (
            <div className="pt-2 border-t border-slate-100">
              <span className="text-slate-400 block text-[10px] uppercase font-bold mb-1">Summary</span>
              <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">{info.summary}</p>
            </div>
          )}
        </div>

        {/* Section 2: Education */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <GraduationCap className="w-4 h-4 text-[#7355D9]" />
              <h3 className="font-black text-xs uppercase tracking-wider text-slate-800">
                2. Education ({education.length} {education.length === 1 ? "Entry" : "Entries"})
              </h3>
            </div>
            <button
              onClick={() => onEditStep(2)}
              className="px-2.5 py-1 rounded-lg text-[11px] font-bold text-[#7355D9] hover:bg-[#7355D9]/10 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Edit2 className="w-3 h-3" /> Edit
            </button>
          </div>
          {education.length === 0 ? (
            <p className="text-xs text-slate-400 italic">No education entries added.</p>
          ) : (
            <div className="space-y-2">
              {education.map((edu) => (
                <div key={edu.id} className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs flex justify-between items-start">
                  <div>
                    <span className="font-bold text-slate-900">{edu.degree} in {edu.fieldOfStudy}</span>
                    <div className="text-[11px] text-slate-600">{edu.institution} {edu.grade && `• Grade: ${edu.grade}`}</div>
                  </div>
                  <span className="text-[10px] font-mono text-slate-500">{edu.startDate} – {edu.endDate}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Section 3: Technical Skills */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <Code2 className="w-4 h-4 text-[#7355D9]" />
              <h3 className="font-black text-xs uppercase tracking-wider text-slate-800">3. Technical Skills</h3>
            </div>
            <button
              onClick={() => onEditStep(3)}
              className="px-2.5 py-1 rounded-lg text-[11px] font-bold text-[#7355D9] hover:bg-[#7355D9]/10 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Edit2 className="w-3 h-3" /> Edit
            </button>
          </div>
          {!hasSkills ? (
            <p className="text-xs text-slate-400 italic">No skills added yet.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              {(skills?.programmingLanguages?.length || 0) > 0 && (
                <div><span className="text-slate-400 text-[10px] uppercase font-bold block">Languages</span><span className="text-slate-800 font-medium">{skills.programmingLanguages.join(", ")}</span></div>
              )}
              {(skills?.frameworks?.length || 0) > 0 && (
                <div><span className="text-slate-400 text-[10px] uppercase font-bold block">Frameworks</span><span className="text-slate-800 font-medium">{skills.frameworks.join(", ")}</span></div>
              )}
              {(skills?.aiMlSkills?.length || 0) > 0 && (
                <div><span className="text-slate-400 text-[10px] uppercase font-bold block">AI / ML</span><span className="text-slate-800 font-medium">{skills.aiMlSkills.join(", ")}</span></div>
              )}
              {(skills?.databases?.length || 0) > 0 && (
                <div><span className="text-slate-400 text-[10px] uppercase font-bold block">Databases</span><span className="text-slate-800 font-medium">{skills.databases.join(", ")}</span></div>
              )}
              {(skills?.developerTools?.length || 0) > 0 && (
                <div><span className="text-slate-400 text-[10px] uppercase font-bold block">Tools & DevOps</span><span className="text-slate-800 font-medium">{skills.developerTools.join(", ")}</span></div>
              )}
            </div>
          )}
        </div>

        {/* Section 4: Work Experience */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-[#7355D9]" />
              <h3 className="font-black text-xs uppercase tracking-wider text-slate-800">
                4. Work Experience ({experience.length} {experience.length === 1 ? "Role" : "Roles"})
              </h3>
            </div>
            <button
              onClick={() => onEditStep(4)}
              className="px-2.5 py-1 rounded-lg text-[11px] font-bold text-[#7355D9] hover:bg-[#7355D9]/10 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Edit2 className="w-3 h-3" /> Edit
            </button>
          </div>
          {experience.length === 0 ? (
            <p className="text-xs text-slate-400 italic">No work experience entries added.</p>
          ) : (
            <div className="space-y-3">
              {experience.map((exp) => (
                <div key={exp.id} className="p-3.5 rounded-xl bg-slate-50 border border-slate-100 text-xs space-y-1">
                  <div className="flex justify-between font-bold text-slate-900">
                    <span>{exp.role} @ {exp.company}</span>
                    <span className="text-[10px] font-mono text-slate-500">{exp.startDate} – {exp.current ? "Present" : exp.endDate}</span>
                  </div>
                  {(exp.responsibilities?.length || 0) > 0 && (
                    <ul className="list-disc pl-4 text-slate-700 text-[11px] space-y-0.5">
                      {exp.responsibilities.map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Section 5: Internships */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-[#7355D9]" />
              <h3 className="font-black text-xs uppercase tracking-wider text-slate-800">
                5. Internships ({internships.length})
              </h3>
            </div>
            <button
              onClick={() => onEditStep(5)}
              className="px-2.5 py-1 rounded-lg text-[11px] font-bold text-[#7355D9] hover:bg-[#7355D9]/10 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Edit2 className="w-3 h-3" /> Edit
            </button>
          </div>
          {internships.length === 0 ? (
            <p className="text-xs text-slate-400 italic">No internships listed.</p>
          ) : (
            <div className="space-y-2">
              {internships.map((intn) => (
                <div key={intn.id} className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs">
                  <div className="flex justify-between font-bold text-slate-900">
                    <span>{intn.role} @ {intn.organization}</span>
                    <span className="text-[10px] font-mono text-slate-500">{intn.duration}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Section 6: Projects */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <FolderGit2 className="w-4 h-4 text-[#7355D9]" />
              <h3 className="font-black text-xs uppercase tracking-wider text-slate-800">
                6. Projects ({projects.length})
              </h3>
            </div>
            <button
              onClick={() => onEditStep(6)}
              className="px-2.5 py-1 rounded-lg text-[11px] font-bold text-[#7355D9] hover:bg-[#7355D9]/10 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Edit2 className="w-3 h-3" /> Edit
            </button>
          </div>
          {projects.length === 0 ? (
            <p className="text-xs text-slate-400 italic">No projects listed.</p>
          ) : (
            <div className="space-y-2">
              {projects.map((proj) => (
                <div key={proj.id} className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs space-y-1">
                  <div className="flex justify-between font-bold text-slate-900">
                    <span>{proj.title}</span>
                    <span className="text-[10px] font-mono text-emerald-600">{proj.technologies?.join(" • ") || ""}</span>
                  </div>
                  {proj.description && <p className="text-slate-600 text-[11px]">{proj.description}</p>}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Section 7: Certifications & Additional */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-3">
          <div className="flex justify-between items-center border-b border-slate-100 pb-2.5">
            <div className="flex items-center gap-2">
              <Award className="w-4 h-4 text-[#7355D9]" />
              <h3 className="font-black text-xs uppercase tracking-wider text-slate-800">
                7. Certifications & Additional Info
              </h3>
            </div>
            <button
              onClick={() => onEditStep(7)}
              className="px-2.5 py-1 rounded-lg text-[11px] font-bold text-[#7355D9] hover:bg-[#7355D9]/10 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Edit2 className="w-3 h-3" /> Edit
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div>
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Certifications</span>
              <span className="text-slate-800 font-medium">
                {(certifications?.length || 0) > 0 ? certifications.map((c) => c.name).join(", ") : "None added"}
              </span>
            </div>
            <div>
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Languages</span>
              <span className="text-slate-800 font-medium">
                {(additional?.languages?.length || 0) > 0 ? additional.languages.join(", ") : "None added"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Sticky Action Bar */}
      <div className="sticky bottom-6 z-40 bg-white/95 backdrop-blur-md p-4 rounded-2xl border border-slate-200 shadow-2xl flex items-center justify-between gap-4">
        <button
          onClick={onBackToStep7}
          className="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 text-xs font-bold flex items-center gap-2 cursor-pointer transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Step 7
        </button>

        <button
          onClick={onGenerateAI}
          disabled={errors.length > 0 || isGenerating}
          className={`px-8 py-3 rounded-xl font-black text-xs uppercase tracking-wider flex items-center gap-2 transition-all cursor-pointer shadow-lg ${
            errors.length > 0 || isGenerating
              ? "bg-slate-300 text-slate-500 cursor-not-allowed"
              : "bg-gradient-to-r from-[#D6A84B] via-[#F0D99B] to-[#D6A84B] text-[#17233F] shadow-[#D6A84B]/25 hover:opacity-95 hover:scale-[1.01]"
          }`}
        >
          {isGenerating ? (
            <>
              <div className="w-4 h-4 border-2 border-[#17233F] border-t-transparent rounded-full animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 text-[#7355D9]" />
              Generate My Resume With AI <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
