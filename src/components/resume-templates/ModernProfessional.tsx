"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";
import { Mail, Phone, MapPin, Globe, ExternalLink, GitBranch } from "lucide-react";

export function ModernProfessional({ resume }: { resume: ResumeFullData }) {
  const accent = resume.accentColor || "#17233F";
  const { personalInfo: info, skills, education, experience, internships, projects, certifications, additional } = resume;

  return (
    <div className="bg-white text-[#1E293B] shadow-lg rounded-xl overflow-hidden max-w-[850px] mx-auto min-h-[1050px] flex flex-col font-sans border border-slate-200 print:shadow-none print:border-none print:m-0 print:w-full print:max-w-none">
      {/* 2-Column Split: Left Sidebar (35%) & Right Main Pane (65%) */}
      <div className="grid grid-cols-12 flex-1">
        {/* Left Sidebar */}
        <div 
          className="col-span-12 md:col-span-4 p-6 text-white space-y-6 flex flex-col justify-between"
          style={{ backgroundColor: accent }}
        >
          <div className="space-y-6">
            {/* Header info in sidebar */}
            <div className="space-y-2 border-b border-white/20 pb-4">
              <h1 className="text-xl font-black tracking-tight text-white leading-tight">
                {info.fullName || "Your Full Name"}
              </h1>
              <p className="text-xs font-semibold text-white/80 tracking-wide uppercase">
                {info.professionalTitle || "Professional Title"}
              </p>
            </div>

            {/* Contact Details */}
            <div className="space-y-2.5 text-xs text-white/90">
              <span className="text-[10px] font-black uppercase tracking-widest text-[#D6A84B] block">
                Contact
              </span>
              {info.email && (
                <div className="flex items-center gap-2 break-all">
                  <Mail className="w-3.5 h-3.5 text-[#D6A84B] shrink-0" />
                  <span>{info.email}</span>
                </div>
              )}
              {info.phone && (
                <div className="flex items-center gap-2">
                  <Phone className="w-3.5 h-3.5 text-[#D6A84B] shrink-0" />
                  <span>{info.phone}</span>
                </div>
              )}
              {info.location && (
                <div className="flex items-center gap-2">
                  <MapPin className="w-3.5 h-3.5 text-[#D6A84B] shrink-0" />
                  <span>{info.location}</span>
                </div>
              )}
              {info.linkedIn && (
                <div className="flex items-center gap-2 break-all">
                  <ExternalLink className="w-3.5 h-3.5 text-[#D6A84B] shrink-0" />
                  <a href={info.linkedIn} target="_blank" rel="noreferrer" className="hover:underline">
                    {info.linkedIn.replace(/^https?:\/\/(www\.)?linkedin\.com\/in\//, "")}
                  </a>
                </div>
              )}
              {info.gitHub && (
                <div className="flex items-center gap-2 break-all">
                  <GitBranch className="w-3.5 h-3.5 text-[#D6A84B] shrink-0" />
                  <a href={info.gitHub} target="_blank" rel="noreferrer" className="hover:underline">
                    {info.gitHub.replace(/^https?:\/\/(www\.)?github\.com\//, "")}
                  </a>
                </div>
              )}
              {info.portfolio && (
                <div className="flex items-center gap-2 break-all">
                  <Globe className="w-3.5 h-3.5 text-[#D6A84B] shrink-0" />
                  <a href={info.portfolio} target="_blank" rel="noreferrer" className="hover:underline">
                    {info.portfolio.replace(/^https?:\/\//, "")}
                  </a>
                </div>
              )}
            </div>

            {/* Technical Skills */}
            <div className="space-y-3 pt-2">
              <span className="text-[10px] font-black uppercase tracking-widest text-[#D6A84B] block border-b border-white/20 pb-1">
                Technical Skills
              </span>

              {skills.programmingLanguages.length > 0 && (
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-white/70 uppercase">Languages</span>
                  <div className="flex flex-wrap gap-1">
                    {skills.programmingLanguages.map((s, i) => (
                      <span key={i} className="text-[10px] px-1.5 py-0.5 rounded bg-white/15 text-white font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {skills.frameworks.length > 0 && (
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-white/70 uppercase">Frameworks</span>
                  <div className="flex flex-wrap gap-1">
                    {skills.frameworks.map((s, i) => (
                      <span key={i} className="text-[10px] px-1.5 py-0.5 rounded bg-white/15 text-white font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {skills.databases.length > 0 && (
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-white/70 uppercase">Databases</span>
                  <div className="flex flex-wrap gap-1">
                    {skills.databases.map((s, i) => (
                      <span key={i} className="text-[10px] px-1.5 py-0.5 rounded bg-white/15 text-white font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {skills.developerTools.length > 0 && (
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-white/70 uppercase">Tools & Cloud</span>
                  <div className="flex flex-wrap gap-1">
                    {skills.developerTools.map((s, i) => (
                      <span key={i} className="text-[10px] px-1.5 py-0.5 rounded bg-white/15 text-white font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {skills.aiMlSkills.length > 0 && (
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-white/70 uppercase">AI / ML</span>
                  <div className="flex flex-wrap gap-1">
                    {skills.aiMlSkills.map((s, i) => (
                      <span key={i} className="text-[10px] px-1.5 py-0.5 rounded bg-white/15 text-white font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Education */}
            {education.length > 0 && (
              <div className="space-y-3 pt-2">
                <span className="text-[10px] font-black uppercase tracking-widest text-[#D6A84B] block border-b border-white/20 pb-1">
                  Education
                </span>
                {education.map((edu) => (
                  <div key={edu.id} className="space-y-0.5 text-xs">
                    <div className="font-bold text-white leading-tight">{edu.degree}</div>
                    <div className="text-white/80 text-[11px]">{edu.fieldOfStudy}</div>
                    <div className="text-[10px] text-white/60">{edu.institution}</div>
                    <div className="text-[9px] text-[#D6A84B]">{edu.startDate} – {edu.endDate} {edu.grade && `• ${edu.grade}`}</div>
                  </div>
                ))}
              </div>
            )}

            {/* Certifications */}
            {certifications.length > 0 && (
              <div className="space-y-2 pt-2">
                <span className="text-[10px] font-black uppercase tracking-widest text-[#D6A84B] block border-b border-white/20 pb-1">
                  Certifications
                </span>
                {certifications.map((c) => (
                  <div key={c.id} className="text-xs space-y-0.5">
                    <div className="font-semibold text-white leading-tight">{c.name}</div>
                    <div className="text-[10px] text-white/70">{c.issuingOrganization} ({c.issueDate})</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Languages in Sidebar footer */}
          {additional.languages.length > 0 && (
            <div className="pt-4 border-t border-white/20 text-xs">
              <span className="text-[9px] font-black uppercase tracking-wider text-[#D6A84B] block mb-1">
                Languages
              </span>
              <p className="text-[11px] text-white/80">{additional.languages.join(", ")}</p>
            </div>
          )}
        </div>

        {/* Right Main Pane */}
        <div className="col-span-12 md:col-span-8 p-8 space-y-6">
          {/* Summary */}
          {info.summary && (
            <div className="space-y-2">
              <h2 className="text-xs font-black uppercase tracking-wider text-[#17233F] border-b-2 pb-1" style={{ borderColor: accent }}>
                Professional Profile
              </h2>
              <p className="text-xs text-slate-700 leading-relaxed text-justify">
                {info.summary}
              </p>
            </div>
          )}

          {/* Experience */}
          {experience.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-xs font-black uppercase tracking-wider text-[#17233F] border-b-2 pb-1" style={{ borderColor: accent }}>
                Work Experience
              </h2>
              {experience.map((exp) => (
                <div key={exp.id} className="space-y-1.5">
                  <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1">
                    <div>
                      <span className="text-xs font-black text-slate-900">{exp.role}</span>
                      <span className="text-xs font-bold text-slate-500"> | {exp.company}</span>
                    </div>
                    <span className="text-[10px] font-bold text-slate-400">
                      {exp.startDate} – {exp.endDate || "Present"} {exp.location && `(${exp.location})`}
                    </span>
                  </div>
                  {exp.responsibilities.length > 0 && (
                    <ul className="list-disc list-outside pl-4 space-y-1 text-xs text-slate-600">
                      {exp.responsibilities.map((r, i) => (
                        <li key={i} className="leading-snug">{r}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Internships */}
          {internships.length > 0 && (
            <div className="space-y-3">
              <h2 className="text-xs font-black uppercase tracking-wider text-[#17233F] border-b-2 pb-1" style={{ borderColor: accent }}>
                Internships
              </h2>
              {internships.map((intn) => (
                <div key={intn.id} className="space-y-1">
                  <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1">
                    <div>
                      <span className="text-xs font-black text-slate-900">{intn.role}</span>
                      <span className="text-xs font-bold text-slate-500"> | {intn.organization}</span>
                    </div>
                    <span className="text-[10px] font-bold text-slate-400">{intn.duration}</span>
                  </div>
                  <ul className="list-disc list-outside pl-4 space-y-0.5 text-xs text-slate-600">
                    {[...intn.workPerformed, ...intn.achievements].map((p, i) => (
                      <li key={i} className="leading-snug">{p}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}

          {/* Projects */}
          {projects.length > 0 && (
            <div className="space-y-3">
              <h2 className="text-xs font-black uppercase tracking-wider text-[#17233F] border-b-2 pb-1" style={{ borderColor: accent }}>
                Technical Projects
              </h2>
              {projects.map((proj) => (
                <div key={proj.id} className="space-y-1">
                  <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-black text-slate-900">{proj.title}</span>
                      {proj.githubUrl && (
                        <a href={proj.githubUrl} target="_blank" rel="noreferrer" className="text-slate-400 hover:text-slate-700">
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                    {proj.technologies.length > 0 && (
                      <span className="text-[9px] font-semibold text-[#7355D9] bg-[#7355D9]/10 px-1.5 py-0.5 rounded">
                        {proj.technologies.join(", ")}
                      </span>
                    )}
                  </div>
                  {proj.description && (
                    <p className="text-xs text-slate-600">{proj.description}</p>
                  )}
                  {proj.contributions.length > 0 && (
                    <ul className="list-disc list-outside pl-4 space-y-0.5 text-xs text-slate-600">
                      {proj.contributions.map((c, i) => (
                        <li key={i} className="leading-snug">{c}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Additional Sections */}
          {additional.achievements.length > 0 && (
            <div className="space-y-2">
              <h2 className="text-xs font-black uppercase tracking-wider text-[#17233F] border-b-2 pb-1" style={{ borderColor: accent }}>
                Key Achievements
              </h2>
              <ul className="list-disc list-outside pl-4 space-y-1 text-xs text-slate-600">
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
