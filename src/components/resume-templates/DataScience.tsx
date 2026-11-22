"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";
import { Cpu, BookOpen, Award, ExternalLink } from "lucide-react";

export function DataScience({ resume }: { resume: ResumeFullData }) {
  const accent = resume.accentColor || "#0F766E";
  const { personalInfo: info, skills, education, internships, projects, certifications, additional } = resume;

  return (
    <div className="bg-white text-slate-800 shadow-xl max-w-[850px] mx-auto min-h-[1050px] p-8 font-sans border-t-8 border-teal-700 print:shadow-none print:border-none print:m-0 print:p-4 print:w-full" style={{ borderTopColor: accent }}>
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-baseline border-b border-slate-200 pb-4 mb-6">
        <div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">{info.fullName || "Candidate Name"}</h1>
          <p className="text-xs font-bold text-teal-700 uppercase tracking-wider mt-0.5">{info.professionalTitle || "AI / Data Science Specialist"}</p>
        </div>
        <div className="text-right text-xs text-slate-500 space-y-0.5">
          <div>{[info.location, info.phone, info.email].filter(Boolean).join(" • ")}</div>
          <div className="flex justify-end gap-3 text-teal-700 font-medium">
            {info.gitHub && <a href={info.gitHub} target="_blank" rel="noreferrer" className="hover:underline">GitHub</a>}
            {info.linkedIn && <a href={info.linkedIn} target="_blank" rel="noreferrer" className="hover:underline">LinkedIn</a>}
            {info.portfolio && <a href={info.portfolio} target="_blank" rel="noreferrer" className="hover:underline">Scholar / Blog</a>}
          </div>
        </div>
      </div>

      <div className="space-y-6 text-xs leading-relaxed">
        {/* Research / Professional Abstract */}
        {info.summary && (
          <div className="space-y-1">
            <h2 className="text-xs font-bold uppercase tracking-wider text-teal-900 border-b border-teal-200 pb-0.5 flex items-center gap-1.5">
              <Cpu className="w-3.5 h-3.5 text-teal-700" /> Research & Technical Abstract
            </h2>
            <p className="text-slate-700 text-justify leading-normal">{info.summary}</p>
          </div>
        )}

        {/* AI & ML Core Frameworks */}
        <div className="space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-teal-900 border-b border-teal-200 pb-0.5">
            Machine Learning Competencies & Tooling
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {skills.aiMlSkills.length > 0 && (
              <div className="p-2.5 rounded-lg bg-teal-50/50 border border-teal-100">
                <span className="text-[10px] font-bold text-teal-900 uppercase block mb-0.5">AI / Deep Learning</span>
                <span className="text-slate-800">{skills.aiMlSkills.join(", ")}</span>
              </div>
            )}
            {skills.frameworks.length > 0 && (
              <div className="p-2.5 rounded-lg bg-teal-50/50 border border-teal-100">
                <span className="text-[10px] font-bold text-teal-900 uppercase block mb-0.5">Frameworks & Libraries</span>
                <span className="text-slate-800">{skills.frameworks.join(", ")}</span>
              </div>
            )}
            {skills.programmingLanguages.length > 0 && (
              <div className="p-2.5 rounded-lg bg-teal-50/50 border border-teal-100">
                <span className="text-[10px] font-bold text-teal-900 uppercase block mb-0.5">Languages & Analysis</span>
                <span className="text-slate-800">{skills.programmingLanguages.join(", ")}</span>
              </div>
            )}
            {skills.databases.length > 0 && (
              <div className="p-2.5 rounded-lg bg-teal-50/50 border border-teal-100">
                <span className="text-[10px] font-bold text-teal-900 uppercase block mb-0.5">Vector Stores & Databases</span>
                <span className="text-slate-800">{skills.databases.join(", ")}</span>
              </div>
            )}
          </div>
        </div>

        {/* Research Projects */}
        {projects.length > 0 && (
          <div className="space-y-3">
            <h2 className="text-xs font-bold uppercase tracking-wider text-teal-900 border-b border-teal-200 pb-0.5">
              Machine Learning Research & Implementations
            </h2>
            {projects.map((proj) => (
              <div key={proj.id} className="space-y-1">
                <div className="flex justify-between items-baseline font-semibold">
                  <span className="text-slate-900 text-xs">{proj.title}</span>
                  {proj.technologies.length > 0 && (
                    <span className="text-[10px] text-teal-700 bg-teal-50 px-1.5 py-0.2 rounded border border-teal-200 font-mono">
                      {proj.technologies.join(", ")}
                    </span>
                  )}
                </div>
                {proj.description && <p className="text-slate-600 italic text-[11px]">{proj.description}</p>}
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

        {/* Research Internships */}
        {internships.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-teal-900 border-b border-teal-200 pb-0.5">
              Research & Industry Internships
            </h2>
            {internships.map((intn) => (
              <div key={intn.id} className="space-y-0.5">
                <div className="flex justify-between font-bold">
                  <span>{intn.role} — {intn.organization}</span>
                  <span className="text-slate-400 font-normal">{intn.duration}</span>
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

        {/* Publications */}
        {additional.publications.length > 0 && (
          <div className="space-y-1.5">
            <h2 className="text-xs font-bold uppercase tracking-wider text-teal-900 border-b border-teal-200 pb-0.5 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-teal-700" /> Publications & Technical Papers
            </h2>
            <ul className="list-disc pl-4 space-y-1 text-slate-700">
              {additional.publications.map((pub, i) => (
                <li key={i} className="leading-snug">{pub}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Education */}
        {education.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-teal-900 border-b border-teal-200 pb-0.5">
              Education
            </h2>
            <div className="space-y-2">
              {education.map((edu) => (
                <div key={edu.id} className="flex justify-between items-baseline">
                  <div>
                    <span className="font-bold text-slate-900">{edu.degree} in {edu.fieldOfStudy}</span>
                    <span className="text-slate-500"> — {edu.institution}</span>
                    {edu.coursework.length > 0 && (
                      <div className="text-[10px] text-slate-500 mt-0.5">Coursework: {edu.coursework.join(", ")}</div>
                    )}
                  </div>
                  <div className="text-right">
                    <span className="text-slate-500 text-[11px]">{edu.startDate} – {edu.endDate}</span>
                    {edu.grade && <div className="text-teal-700 font-bold text-[10px]">GPA: {edu.grade}</div>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Accolades */}
        {additional.achievements.length > 0 && (
          <div className="space-y-1">
            <h2 className="text-xs font-bold uppercase tracking-wider text-teal-900 border-b border-teal-200 pb-0.5 flex items-center gap-1.5">
              <Award className="w-3.5 h-3.5 text-teal-700" /> Honors & Competitions
            </h2>
            <ul className="list-disc pl-4 space-y-0.5 text-slate-700">
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
