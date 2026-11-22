"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";
import { GraduationCap, Code, Rocket, Award } from "lucide-react";

export function FresherResume({ resume }: { resume: ResumeFullData }) {
  const accent = resume.accentColor || "#1E3A8A";
  const { personalInfo: info, skills, education, internships, projects, certifications, additional } = resume;

  return (
    <div className="bg-white text-slate-900 shadow-lg max-w-[850px] mx-auto min-h-[1050px] p-8 font-sans border border-slate-200 print:shadow-none print:border-none print:m-0 print:p-4 print:w-full">
      {/* Top Banner Header */}
      <div className="border-b-2 pb-4 mb-5" style={{ borderColor: accent }}>
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-2">
          <div>
            <h1 className="text-2xl font-black tracking-tight" style={{ color: accent }}>
              {info.fullName || "Your Name"}
            </h1>
            <p className="text-xs font-bold text-slate-600 uppercase tracking-wider mt-0.5">
              {info.professionalTitle || "Entry-Level Software Engineer"}
            </p>
          </div>
          <div className="text-right text-xs text-slate-600 space-y-0.5">
            <div>{[info.email, info.phone, info.location].filter(Boolean).join(" • ")}</div>
            <div className="flex justify-end gap-2.5 font-medium" style={{ color: accent }}>
              {info.gitHub && <a href={info.gitHub} target="_blank" rel="noreferrer" className="hover:underline">GitHub</a>}
              {info.linkedIn && <a href={info.linkedIn} target="_blank" rel="noreferrer" className="hover:underline">LinkedIn</a>}
              {info.portfolio && <a href={info.portfolio} target="_blank" rel="noreferrer" className="hover:underline">Portfolio</a>}
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-5 text-xs">
        {/* Career Objective */}
        {info.summary && (
          <div className="space-y-1">
            <h2 className="text-xs font-black uppercase tracking-wider border-b pb-0.5 flex items-center gap-1.5" style={{ color: accent, borderColor: `${accent}40` }}>
              Objective & Profile
            </h2>
            <p className="text-slate-700 leading-relaxed text-justify">{info.summary}</p>
          </div>
        )}

        {/* 1. Education FIRST for Freshers */}
        {education.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-xs font-black uppercase tracking-wider border-b pb-0.5 flex items-center gap-1.5" style={{ color: accent, borderColor: `${accent}40` }}>
              <GraduationCap className="w-3.5 h-3.5" /> Education
            </h2>
            {education.map((edu) => (
              <div key={edu.id} className="p-2.5 rounded-xl bg-slate-50 border border-slate-100 space-y-1">
                <div className="flex justify-between font-bold text-slate-900">
                  <span>{edu.degree} in {edu.fieldOfStudy}</span>
                  <span className="text-slate-500 font-normal">{edu.startDate} – {edu.endDate}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>{edu.institution}</span>
                  {edu.grade && <span className="font-bold text-blue-900">CGPA: {edu.grade}</span>}
                </div>
                {edu.coursework.length > 0 && (
                  <div className="text-[11px] text-slate-500 pt-0.5">
                    <strong className="text-slate-700 font-semibold">Coursework:</strong> {edu.coursework.join(", ")}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* 2. Technical Skills */}
        <div className="space-y-1.5">
          <h2 className="text-xs font-black uppercase tracking-wider border-b pb-0.5 flex items-center gap-1.5" style={{ color: accent, borderColor: `${accent}40` }}>
            <Code className="w-3.5 h-3.5" /> Technical Skills
          </h2>
          <div className="space-y-1 bg-slate-50 p-3 rounded-xl border border-slate-100">
            {skills.programmingLanguages.length > 0 && (
              <div><strong className="font-semibold text-slate-800">Programming Languages:</strong> {skills.programmingLanguages.join(", ")}</div>
            )}
            {skills.frameworks.length > 0 && (
              <div><strong className="font-semibold text-slate-800">Frameworks & Web:</strong> {skills.frameworks.join(", ")}</div>
            )}
            {skills.databases.length > 0 && (
              <div><strong className="font-semibold text-slate-800">Databases:</strong> {skills.databases.join(", ")}</div>
            )}
            {skills.developerTools.length > 0 && (
              <div><strong className="font-semibold text-slate-800">Developer Tools:</strong> {skills.developerTools.join(", ")}</div>
            )}
          </div>
        </div>

        {/* 3. Academic & Personal Projects */}
        {projects.length > 0 && (
          <div className="space-y-2.5">
            <h2 className="text-xs font-black uppercase tracking-wider border-b pb-0.5 flex items-center gap-1.5" style={{ color: accent, borderColor: `${accent}40` }}>
              <Rocket className="w-3.5 h-3.5" /> Key Projects
            </h2>
            {projects.map((proj) => (
              <div key={proj.id} className="space-y-1">
                <div className="flex justify-between items-baseline font-bold">
                  <span className="text-slate-900">{proj.title}</span>
                  {proj.technologies.length > 0 && (
                    <span className="text-[10px] font-mono text-blue-800 bg-blue-50 px-1.5 py-0.5 rounded">
                      [{proj.technologies.join(", ")}]
                    </span>
                  )}
                </div>
                {proj.description && <p className="text-slate-600 text-[11px]">{proj.description}</p>}
                {proj.contributions.length > 0 && (
                  <ul className="list-disc pl-4 space-y-0.5 text-slate-700">
                    {proj.contributions.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}

        {/* 4. Internships */}
        {internships.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-xs font-black uppercase tracking-wider border-b pb-0.5" style={{ color: accent, borderColor: `${accent}40` }}>
              Internship Experience
            </h2>
            {internships.map((intn) => (
              <div key={intn.id} className="space-y-0.5">
                <div className="flex justify-between font-bold">
                  <span className="text-slate-900">{intn.role} — {intn.organization}</span>
                  <span className="text-slate-500 font-normal">{intn.duration}</span>
                </div>
                <ul className="list-disc pl-4 space-y-0.5 text-slate-700">
                  {[...intn.workPerformed, ...intn.achievements].map((p, i) => (
                    <li key={i}>{p}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}

        {/* 5. Certifications & Achievements */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {certifications.length > 0 && (
            <div className="space-y-1">
              <h2 className="text-xs font-black uppercase tracking-wider border-b pb-0.5" style={{ color: accent, borderColor: `${accent}40` }}>
                Certifications
              </h2>
              <ul className="list-disc pl-4 space-y-0.5 text-slate-700 text-[11px]">
                {certifications.map((c) => (
                  <li key={c.id}>{c.name} ({c.issuingOrganization})</li>
                ))}
              </ul>
            </div>
          )}

          {additional.achievements.length > 0 && (
            <div className="space-y-1">
              <h2 className="text-xs font-black uppercase tracking-wider border-b pb-0.5 flex items-center gap-1.5" style={{ color: accent, borderColor: `${accent}40` }}>
                <Award className="w-3.5 h-3.5" /> Achievements
              </h2>
              <ul className="list-disc pl-4 space-y-0.5 text-slate-700 text-[11px]">
                {additional.achievements.map((ach, i) => (
                  <li key={i}>{ach}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
