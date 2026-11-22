"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";
import { ExternalLink, Sparkles } from "lucide-react";

export function CreativePortfolio({ resume }: { resume: ResumeFullData }) {
  const accent = resume.accentColor || "#7355D9";
  const { personalInfo: info, skills, education, experience, projects, certifications, additional } = resume;

  return (
    <div className="bg-[#FAF9FF] text-slate-900 shadow-xl max-w-[850px] mx-auto min-h-[1050px] p-8 font-sans border border-purple-100 print:shadow-none print:border-none print:m-0 print:p-4 print:w-full">
      {/* Bold Card Header */}
      <div 
        className="p-8 rounded-3xl text-white space-y-4 mb-8 shadow-md"
        style={{ background: `linear-gradient(135deg, ${accent} 0%, #17233F 100%)` }}
      >
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 text-[10px] font-black uppercase tracking-wider mb-2">
              <Sparkles className="w-3 h-3 text-[#F0D99B]" /> Creative Tech Portfolio
            </div>
            <h1 className="text-3xl font-black tracking-tight">{info.fullName || "Your Name"}</h1>
            <p className="text-sm font-medium text-white/80 mt-0.5">{info.professionalTitle || "Creative Technologist"}</p>
          </div>
          <div className="text-xs text-white/90 text-right space-y-1">
            {info.email && <div>{info.email}</div>}
            {info.phone && <div>{info.phone}</div>}
            {info.location && <div>{info.location}</div>}
            {info.portfolio && (
              <a href={info.portfolio} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-[#F0D99B] hover:underline font-bold">
                <span>Live Portfolio</span> <ExternalLink className="w-3 h-3" />
              </a>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-8 text-xs">
        {/* Left Column: Featured Projects & Experience (7 cols) */}
        <div className="md:col-span-7 space-y-6">
          {info.summary && (
            <div className="p-4 rounded-2xl bg-white border border-purple-50 shadow-2xs space-y-1.5">
              <span className="text-[10px] font-black uppercase tracking-wider text-purple-900">About Me</span>
              <p className="text-slate-600 leading-relaxed">{info.summary}</p>
            </div>
          )}

          {projects.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-xs font-black uppercase tracking-wider text-slate-900 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: accent }} />
                Featured Creative Projects
              </h2>
              {projects.map((proj) => (
                <div key={proj.id} className="p-4 rounded-2xl bg-white border border-slate-200/80 hover:border-purple-300 transition-all space-y-2 shadow-2xs">
                  <div className="flex justify-between items-baseline">
                    <h3 className="font-bold text-slate-900">{proj.title}</h3>
                    {proj.projectUrl && (
                      <a href={proj.projectUrl} target="_blank" rel="noreferrer" className="text-purple-600 hover:underline flex items-center gap-1 text-[10px]">
                        Demo <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    )}
                  </div>
                  {proj.description && <p className="text-slate-600 text-[11px]">{proj.description}</p>}
                  {proj.technologies.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {proj.technologies.map((t, i) => (
                        <span key={i} className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-purple-50 text-purple-700">
                          {t}
                        </span>
                      ))}
                    </div>
                  )}
                  {proj.contributions.length > 0 && (
                    <ul className="list-disc pl-4 space-y-0.5 text-slate-600 text-[11px]">
                      {proj.contributions.map((c, i) => (
                        <li key={i}>{c}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

          {experience.length > 0 && (
            <div className="space-y-3">
              <h2 className="text-xs font-black uppercase tracking-wider text-slate-900 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: accent }} />
                Experience
              </h2>
              {experience.map((exp) => (
                <div key={exp.id} className="p-3.5 rounded-xl bg-white border border-slate-200/60 space-y-1">
                  <div className="flex justify-between font-bold text-slate-800">
                    <span>{exp.role}</span>
                    <span className="text-[10px] text-slate-400 font-normal">{exp.startDate} – {exp.endDate || "Present"}</span>
                  </div>
                  <div className="text-[11px] text-purple-700 font-semibold">{exp.company}</div>
                  {exp.responsibilities.length > 0 && (
                    <ul className="list-disc pl-4 space-y-0.5 text-slate-600 text-[11px]">
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

        {/* Right Column: Skills, Education, Achievements (5 cols) */}
        <div className="md:col-span-5 space-y-6">
          {/* Skill Tag Cloud */}
          <div className="p-5 rounded-2xl bg-white border border-slate-200/80 space-y-3 shadow-2xs">
            <h2 className="text-xs font-black uppercase tracking-wider text-slate-900">Creative Stack</h2>
            <div className="space-y-2">
              {skills.frameworks.length > 0 && (
                <div>
                  <span className="text-[10px] font-bold text-slate-400 uppercase">Frameworks</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {skills.frameworks.map((s, i) => (
                      <span key={i} className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-purple-100 text-purple-900">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {skills.programmingLanguages.length > 0 && (
                <div>
                  <span className="text-[10px] font-bold text-slate-400 uppercase">Languages</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {skills.programmingLanguages.map((s, i) => (
                      <span key={i} className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-slate-100 text-slate-800">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {skills.developerTools.length > 0 && (
                <div>
                  <span className="text-[10px] font-bold text-slate-400 uppercase">Tools</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {skills.developerTools.map((s, i) => (
                      <span key={i} className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-amber-50 text-amber-800">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Education Card */}
          {education.length > 0 && (
            <div className="p-5 rounded-2xl bg-white border border-slate-200/80 space-y-2 shadow-2xs">
              <h2 className="text-xs font-black uppercase tracking-wider text-slate-900">Education</h2>
              {education.map((edu) => (
                <div key={edu.id} className="space-y-0.5">
                  <div className="font-bold text-slate-800">{edu.degree}</div>
                  <div className="text-[11px] text-purple-700">{edu.fieldOfStudy}</div>
                  <div className="text-[10px] text-slate-500">{edu.institution} ({edu.startDate} – {edu.endDate})</div>
                </div>
              ))}
            </div>
          )}

          {/* Achievements */}
          {additional.achievements.length > 0 && (
            <div className="p-5 rounded-2xl bg-white border border-slate-200/80 space-y-2 shadow-2xs">
              <h2 className="text-xs font-black uppercase tracking-wider text-slate-900">Accolades</h2>
              <ul className="space-y-1.5 text-[11px] text-slate-600">
                {additional.achievements.map((ach, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    <span className="text-purple-600 font-bold">•</span>
                    <span>{ach}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
