"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";

export function CorporateExecutive({ resume }: { resume: ResumeFullData }) {
  const accent = resume.accentColor || "#17233F";
  const { personalInfo: info, skills, education, experience, projects, certifications, additional } = resume;

  return (
    <div className="bg-[#FAF8F5] text-[#1E293B] shadow-lg max-w-[850px] mx-auto min-h-[1050px] p-10 font-serif border-t-8 border-b-8 border-slate-300 print:shadow-none print:border-none print:m-0 print:p-6 print:w-full" style={{ borderTopColor: accent, borderBottomColor: accent }}>
      {/* Formal Header with Gold / Navy Separator */}
      <div className="border-b-2 pb-5 mb-6" style={{ borderColor: accent }}>
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-2">
          <div>
            <h1 className="text-2xl font-bold tracking-tight uppercase" style={{ color: accent }}>
              {info.fullName || "Candidate Name"}
            </h1>
            <p className="text-sm font-semibold tracking-wide text-[#B8860B] mt-0.5">
              {info.professionalTitle || "Executive Leader"}
            </p>
          </div>
          <div className="text-right text-xs text-slate-600 font-sans space-y-0.5">
            <div>{[info.location, info.phone].filter(Boolean).join(" • ")}</div>
            <div>{info.email}</div>
            {info.linkedIn && <div className="text-slate-500">{info.linkedIn}</div>}
          </div>
        </div>
      </div>

      <div className="space-y-6 text-xs leading-relaxed">
        {/* Executive Summary */}
        {info.summary && (
          <div className="space-y-1.5">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b pb-0.5" style={{ borderColor: accent }}>
              Executive Summary
            </h2>
            <p className="text-slate-700 text-justify font-sans">{info.summary}</p>
          </div>
        )}

        {/* Core Competencies Matrix */}
        <div className="space-y-1.5">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b pb-0.5" style={{ borderColor: accent }}>
            Core Competencies & Strategic Domains
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2 font-sans text-xs">
            {skills.otherSkills.map((s, i) => (
              <div key={i} className="flex items-center gap-1.5 text-slate-800">
                <span className="w-1.5 h-1.5 rounded-full bg-[#B8860B]" />
                <span className="font-medium">{s}</span>
              </div>
            ))}
            {skills.programmingLanguages.map((s, i) => (
              <div key={i} className="flex items-center gap-1.5 text-slate-800">
                <span className="w-1.5 h-1.5 rounded-full bg-[#B8860B]" />
                <span className="font-medium">{s}</span>
              </div>
            ))}
            {skills.frameworks.map((s, i) => (
              <div key={i} className="flex items-center gap-1.5 text-slate-800">
                <span className="w-1.5 h-1.5 rounded-full bg-[#B8860B]" />
                <span className="font-medium">{s}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Executive Experience */}
        {experience.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b pb-0.5" style={{ borderColor: accent }}>
              Leadership Progression
            </h2>
            {experience.map((exp) => (
              <div key={exp.id} className="space-y-1">
                <div className="flex justify-between items-baseline font-sans">
                  <span className="text-xs font-bold text-slate-900">{exp.role}</span>
                  <span className="text-[11px] font-semibold text-slate-500">{exp.startDate} – {exp.endDate || "Present"}</span>
                </div>
                <div className="text-xs font-serif italic text-[#B8860B]">{exp.company} {exp.location && `— ${exp.location}`}</div>
                {exp.responsibilities.length > 0 && (
                  <ul className="list-disc list-outside pl-4 space-y-1 font-sans text-xs text-slate-700">
                    {exp.responsibilities.map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Education & Credentials */}
        {education.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b pb-0.5" style={{ borderColor: accent }}>
              Education & Academic Credentials
            </h2>
            <div className="space-y-2 font-sans">
              {education.map((edu) => (
                <div key={edu.id} className="flex justify-between items-baseline">
                  <div>
                    <span className="font-bold text-slate-900">{edu.degree} in {edu.fieldOfStudy}</span>
                    <span className="text-slate-500"> — {edu.institution}</span>
                  </div>
                  <span className="text-[11px] text-slate-500">{edu.startDate} – {edu.endDate}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Honors & Affiliations */}
        {additional.achievements.length > 0 && (
          <div className="space-y-1.5">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b pb-0.5" style={{ borderColor: accent }}>
              Key Accomplishments & Board Affiliations
            </h2>
            <ul className="list-disc list-outside pl-4 space-y-0.5 font-sans text-xs text-slate-700">
              {additional.achievements.map((ach, i) => (
                <li key={i}>{ach}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
