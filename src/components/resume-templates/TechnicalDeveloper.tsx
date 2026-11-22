"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";
import { Terminal, GitBranch, ExternalLink, Code2, Server, Database, Wrench } from "lucide-react";

export function TechnicalDeveloper({ resume }: { resume: ResumeFullData }) {
  const accent = resume.accentColor || "#1E293B";
  const { personalInfo: info, skills, education, experience, projects, certifications, additional } = resume;

  return (
    <div className="bg-[#0F172A] text-slate-200 shadow-2xl max-w-[850px] mx-auto min-h-[1050px] p-8 font-mono border border-slate-700 print:bg-white print:text-black print:border-none print:shadow-none print:m-0 print:p-4 print:w-full">
      {/* Code Terminal Style Header */}
      <div className="border border-slate-700 rounded-2xl bg-slate-900/90 p-6 mb-6 space-y-3">
        <div className="flex items-center gap-2 border-b border-slate-700/60 pb-3">
          <div className="flex gap-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500/80 inline-block" />
            <span className="w-3 h-3 rounded-full bg-amber-500/80 inline-block" />
            <span className="w-3 h-3 rounded-full bg-emerald-500/80 inline-block" />
          </div>
          <span className="text-[11px] text-slate-400 font-bold ml-2 flex items-center gap-1.5">
            <Terminal className="w-3.5 h-3.5 text-emerald-400" /> ~/developer/profile.ts
          </span>
        </div>

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-baseline gap-2">
          <div>
            <h1 className="text-2xl font-black text-white tracking-tight">{info.fullName || "Developer Name"}</h1>
            <p className="text-xs font-semibold text-emerald-400 mt-0.5">{`const role: string = "${info.professionalTitle || "Software Engineer"}";`}</p>
          </div>
          <div className="text-right text-[11px] text-slate-400 space-y-0.5 font-sans">
            <div>{[info.email, info.phone, info.location].filter(Boolean).join(" | ")}</div>
            <div className="flex justify-end gap-3 text-emerald-400 font-mono text-[11px]">
              {info.gitHub && (
                <a href={info.gitHub} target="_blank" rel="noreferrer" className="hover:underline flex items-center gap-1">
                  <GitBranch className="w-3 h-3" /> github
                </a>
              )}
              {info.portfolio && (
                <a href={info.portfolio} target="_blank" rel="noreferrer" className="hover:underline flex items-center gap-1">
                  <ExternalLink className="w-3 h-3" /> website
                </a>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-6 text-xs font-sans">
        {/* Technical Summary */}
        {info.summary && (
          <div className="space-y-1">
            <div className="font-mono text-emerald-400 font-bold text-[11px] flex items-center gap-1">
              <span>// 01. EXECUTIVE_OVERVIEW</span>
            </div>
            <p className="text-slate-300 leading-relaxed font-sans text-justify bg-slate-900/40 p-3 rounded-xl border border-slate-800">
              {info.summary}
            </p>
          </div>
        )}

        {/* Categorized Tech Stack */}
        <div className="space-y-2">
          <div className="font-mono text-emerald-400 font-bold text-[11px]">
            <span>// 02. CORE_STACK_CAPABILITIES</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono">
            {skills.programmingLanguages.length > 0 && (
              <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-[10px] text-indigo-400 font-bold uppercase block mb-1 flex items-center gap-1">
                  <Code2 className="w-3 h-3" /> Languages
                </span>
                <span className="text-slate-200">{skills.programmingLanguages.join(", ")}</span>
              </div>
            )}
            {skills.frameworks.length > 0 && (
              <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-[10px] text-indigo-400 font-bold uppercase block mb-1 flex items-center gap-1">
                  <Server className="w-3 h-3" /> Frameworks & Libs
                </span>
                <span className="text-slate-200">{skills.frameworks.join(", ")}</span>
              </div>
            )}
            {skills.databases.length > 0 && (
              <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-[10px] text-indigo-400 font-bold uppercase block mb-1 flex items-center gap-1">
                  <Database className="w-3 h-3" /> Storage & Cache
                </span>
                <span className="text-slate-200">{skills.databases.join(", ")}</span>
              </div>
            )}
            {skills.developerTools.length > 0 && (
              <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                <span className="text-[10px] text-indigo-400 font-bold uppercase block mb-1 flex items-center gap-1">
                  <Wrench className="w-3 h-3" /> Cloud & DevOps
                </span>
                <span className="text-slate-200">{skills.developerTools.join(", ")}</span>
              </div>
            )}
          </div>
        </div>

        {/* Experience */}
        {experience.length > 0 && (
          <div className="space-y-4">
            <div className="font-mono text-emerald-400 font-bold text-[11px]">
              <span>// 03. PRODUCTION_ENGINEERING_EXPERIENCE</span>
            </div>
            {experience.map((exp) => (
              <div key={exp.id} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1.5">
                <div className="flex justify-between items-baseline font-mono">
                  <span className="text-xs font-bold text-white">{exp.role}</span>
                  <span className="text-[10px] text-emerald-400">{exp.startDate} – {exp.endDate || "Present"}</span>
                </div>
                <div className="text-[11px] text-indigo-300 font-mono">@{exp.company} {exp.location && `[${exp.location}]`}</div>
                {exp.responsibilities.length > 0 && (
                  <ul className="list-disc pl-4 space-y-1 text-slate-300 font-sans text-xs">
                    {exp.responsibilities.map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Projects */}
        {projects.length > 0 && (
          <div className="space-y-3">
            <div className="font-mono text-emerald-400 font-bold text-[11px]">
              <span>// 04. OPEN_SOURCE_AND_SYSTEM_BUILDS</span>
            </div>
            {projects.map((proj) => (
              <div key={proj.id} className="p-3 rounded-xl bg-slate-900/40 border border-slate-800 space-y-1">
                <div className="flex justify-between items-baseline font-mono">
                  <span className="font-bold text-white flex items-center gap-1.5">
                    {proj.title}
                    {proj.githubUrl && (
                      <a href={proj.githubUrl} target="_blank" rel="noreferrer" className="text-slate-400 hover:text-emerald-400">
                        <GitBranch className="w-3 h-3" />
                      </a>
                    )}
                  </span>
                  {proj.technologies.length > 0 && (
                    <span className="text-[10px] text-emerald-300">{proj.technologies.join(" • ")}</span>
                  )}
                </div>
                {proj.description && <p className="text-slate-400 text-xs">{proj.description}</p>}
                {proj.contributions.length > 0 && (
                  <ul className="list-disc pl-4 space-y-0.5 text-slate-300 text-xs">
                    {proj.contributions.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Education & Certs */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {education.length > 0 && (
            <div>
              <div className="font-mono text-emerald-400 font-bold text-[11px] mb-1">
                <span>// 05. ACADEMIC_CREDENTIALS</span>
              </div>
              {education.map((edu) => (
                <div key={edu.id} className="text-xs p-2.5 rounded-xl bg-slate-900/40 border border-slate-800">
                  <div className="font-bold text-white">{edu.degree} in {edu.fieldOfStudy}</div>
                  <div className="text-slate-400 text-[11px]">{edu.institution} ({edu.startDate} – {edu.endDate})</div>
                  {edu.grade && <div className="text-emerald-400 text-[10px] mt-0.5">Grade: {edu.grade}</div>}
                </div>
              ))}
            </div>
          )}

          {certifications.length > 0 && (
            <div>
              <div className="font-mono text-emerald-400 font-bold text-[11px] mb-1">
                <span>// 06. VERIFIED_CERTIFICATIONS</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-900/40 border border-slate-800 space-y-1">
                {certifications.map((c) => (
                  <div key={c.id} className="text-[11px] text-slate-300">
                    • <strong className="text-white">{c.name}</strong> – {c.issuingOrganization}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
