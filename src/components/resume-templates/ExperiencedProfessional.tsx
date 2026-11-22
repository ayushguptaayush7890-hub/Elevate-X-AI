"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";
import { Briefcase, TrendingUp, Award } from "lucide-react";

export function ExperiencedProfessional({ resume }: { resume: ResumeFullData }) {
  const accent = resume.accentColor || "#1E293B";
  const { personalInfo: info, skills, education, experience, projects, certifications, additional } = resume;

  return (
    <div className="bg-white text-slate-900 shadow-xl max-w-[850px] mx-auto min-h-[1050px] p-9 font-sans border border-slate-200 print:shadow-none print:border-none print:m-0 print:p-4 print:w-full">
      {/* Executive Clean Header */}
      <div className="border-b-2 border-slate-900 pb-4 mb-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-2">
          <div>
            <h1 className="text-3xl font-black text-slate-950 tracking-tight">{info.fullName || "Candidate Name"}</h1>
            <p className="text-xs font-bold text-slate-600 uppercase tracking-widest mt-1">
              {info.professionalTitle || "Senior Technology Executive"}
            </p>
          </div>
          <div className="text-right text-xs text-slate-600 space-y-0.5">
            <div>{[info.location, info.phone, info.email].filter(Boolean).join("  |  ")}</div>
            {info.linkedIn && <div className="text-slate-500 font-medium">{info.linkedIn}</div>}
          </div>
        </div>
      </div>

      <div className="space-y-6 text-xs">
        {/* Executive Impact Summary */}
        {info.summary && (
          <div className="space-y-1">
            <h2 className="text-xs font-black uppercase tracking-wider text-slate-900 border-b pb-0.5">
              Executive Profile & Leadership Scope
            </h2>
            <p className="text-slate-700 leading-relaxed text-justify">{info.summary}</p>
          </div>
        )}

        {/* Core Competencies Box */}
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
          <span className="text-[10px] font-black uppercase tracking-widest text-slate-900 block">
            Areas of Strategic Mastery & Leadership
          </span>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-slate-800">
            {skills.otherSkills.map((s, i) => (
              <div key={i} className="flex items-center gap-1.5 font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-slate-900" />
                <span>{s}</span>
              </div>
            ))}
            {skills.developerTools.slice(0, 3).map((s, i) => (
              <div key={i} className="flex items-center gap-1.5 font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-slate-900" />
                <span>{s}</span>
              </div>
            ))}
          </div>
        </div>

        {/* 1. Professional Career Progression FIRST */}
        {experience.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-xs font-black uppercase tracking-wider text-slate-900 border-b pb-0.5 flex items-center gap-1.5">
              <Briefcase className="w-3.5 h-3.5" /> Career History & Strategic Accomplishments
            </h2>
            {experience.map((exp) => (
              <div key={exp.id} className="space-y-1">
                <div className="flex justify-between items-baseline font-bold text-slate-900">
                  <span className="text-xs">{exp.role}</span>
                  <span className="text-[11px] text-slate-500 font-normal">{exp.startDate} – {exp.endDate || "Present"}</span>
                </div>
                <div className="text-[11px] font-bold text-slate-600">{exp.company} {exp.location && `• ${exp.location}`}</div>
                {exp.responsibilities.length > 0 && (
                  <ul className="list-disc pl-4 space-y-1 text-slate-700 leading-snug">
                    {exp.responsibilities.map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}

        {/* 2. Technical Capabilities Grid */}
        <div className="space-y-2">
          <h2 className="text-xs font-black uppercase tracking-wider text-slate-900 border-b pb-0.5">
            Technical Stack & Tooling
          </h2>
          <div className="space-y-1 text-slate-700">
            {skills.programmingLanguages.length > 0 && (
              <div><strong>Languages:</strong> {skills.programmingLanguages.join(", ")}</div>
            )}
            {skills.frameworks.length > 0 && (
              <div><strong>Frameworks & Architecture:</strong> {skills.frameworks.join(", ")}</div>
            )}
            {skills.databases.length > 0 && (
              <div><strong>Data Infrastructure:</strong> {skills.databases.join(", ")}</div>
            )}
          </div>
        </div>

        {/* 3. Education & Certifications */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {education.length > 0 && (
            <div className="space-y-1">
              <h2 className="text-xs font-black uppercase tracking-wider text-slate-900 border-b pb-0.5">
                Education
              </h2>
              {education.map((edu) => (
                <div key={edu.id} className="text-[11px]">
                  <div className="font-bold text-slate-900">{edu.degree} in {edu.fieldOfStudy}</div>
                  <div className="text-slate-600">{edu.institution} ({edu.startDate} – {edu.endDate})</div>
                </div>
              ))}
            </div>
          )}

          {certifications.length > 0 && (
            <div className="space-y-1">
              <h2 className="text-xs font-black uppercase tracking-wider text-slate-900 border-b pb-0.5">
                Credentials
              </h2>
              <ul className="list-disc pl-4 space-y-0.5 text-slate-700 text-[11px]">
                {certifications.map((c) => (
                  <li key={c.id}><strong>{c.name}</strong> – {c.issuingOrganization}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
