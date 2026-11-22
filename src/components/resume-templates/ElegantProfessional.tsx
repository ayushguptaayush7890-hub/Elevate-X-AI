"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";

export function ElegantProfessional({ resume }: { resume: ResumeFullData }) {
  const accent = resume.accentColor || "#17233F";
  const { personalInfo: info, skills, education, experience, internships, projects, certifications, additional } = resume;

  return (
    <div className="bg-[#FCFBF9] text-[#2C302E] shadow-xl max-w-[850px] mx-auto min-h-[1050px] p-10 font-serif border border-[#E8E4DF] print:shadow-none print:border-none print:m-0 print:p-4 print:w-full">
      {/* Refined Classical Header */}
      <div className="text-center pb-6 mb-6 border-b border-[#D4CEB8]">
        <h1 className="text-2xl font-normal tracking-wide text-[#1A1C1B] uppercase">{info.fullName || "Candidate Name"}</h1>
        <p className="text-xs text-[#7A7568] tracking-widest uppercase mt-1">{info.professionalTitle || "Professional Title"}</p>
        <div className="flex flex-wrap justify-center gap-x-4 gap-y-1 text-xs text-[#524E43] mt-2 font-sans">
          {info.email && <span>{info.email}</span>}
          {info.phone && <span>| {info.phone}</span>}
          {info.location && <span>| {info.location}</span>}
          {info.linkedIn && (
            <span>| <a href={info.linkedIn} target="_blank" rel="noreferrer" className="underline hover:text-black">LinkedIn</a></span>
          )}
          {info.portfolio && (
            <span>| <a href={info.portfolio} target="_blank" rel="noreferrer" className="underline hover:text-black">Portfolio</a></span>
          )}
        </div>
      </div>

      <div className="space-y-6 text-xs leading-relaxed">
        {/* Executive Abstract */}
        {info.summary && (
          <div className="space-y-1.5">
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-[#7A7568] text-center">
              — Executive Summary —
            </h2>
            <p className="text-[#3D3A33] text-justify leading-relaxed font-sans">{info.summary}</p>
          </div>
        )}

        {/* Experience */}
        {experience.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-[#7A7568] border-b border-[#E8E4DF] pb-1">
              Professional Engagements
            </h2>
            {experience.map((exp) => (
              <div key={exp.id} className="space-y-1">
                <div className="flex justify-between items-baseline">
                  <span className="font-bold text-sm text-[#1A1C1B]">{exp.role}</span>
                  <span className="text-[11px] text-[#7A7568] italic font-sans">{exp.startDate} – {exp.endDate || "Present"}</span>
                </div>
                <div className="text-xs text-[#8A6D3B] italic">{exp.company} {exp.location && `— ${exp.location}`}</div>
                {exp.responsibilities.length > 0 && (
                  <ul className="list-disc pl-4 space-y-1 text-[#3D3A33] font-sans">
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
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-[#7A7568] border-b border-[#E8E4DF] pb-1">
              Notable Initiatives & Systems
            </h2>
            {projects.map((proj) => (
              <div key={proj.id} className="space-y-0.5 font-sans">
                <div className="flex justify-between items-baseline font-bold text-xs text-[#1A1C1B]">
                  <span>{proj.title}</span>
                  {proj.technologies.length > 0 && (
                    <span className="text-[10px] text-[#8A6D3B] italic font-normal">({proj.technologies.join(", ")})</span>
                  )}
                </div>
                {proj.description && <p className="text-[#524E43] text-xs">{proj.description}</p>}
                {proj.contributions.length > 0 && (
                  <ul className="list-disc pl-4 space-y-0.5 text-[#3D3A33] text-xs">
                    {proj.contributions.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Education & Scholarly Qualifications */}
        {education.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-[#7A7568] border-b border-[#E8E4DF] pb-1">
              Education & Academic Foundation
            </h2>
            {education.map((edu) => (
              <div key={edu.id} className="flex justify-between items-baseline">
                <div>
                  <span className="font-bold text-[#1A1C1B]">{edu.degree} in {edu.fieldOfStudy}</span>
                  <span className="text-[#524E43] font-sans"> — {edu.institution}</span>
                </div>
                <span className="text-[11px] text-[#7A7568] italic font-sans">{edu.startDate} – {edu.endDate}</span>
              </div>
            ))}
          </div>
        )}

        {/* Competencies */}
        <div className="space-y-1.5 pt-2 border-t border-[#E8E4DF]">
          <h2 className="text-[11px] font-bold uppercase tracking-widest text-[#7A7568]">
            Key Competencies & Tooling
          </h2>
          <div className="text-xs font-sans text-[#3D3A33] space-y-1">
            {skills.programmingLanguages.length > 0 && (
              <div><strong>Core Languages:</strong> {skills.programmingLanguages.join(", ")}</div>
            )}
            {skills.frameworks.length > 0 && (
              <div><strong>Architectural Frameworks:</strong> {skills.frameworks.join(", ")}</div>
            )}
            {skills.developerTools.length > 0 && (
              <div><strong>Infrastructure & Tools:</strong> {skills.developerTools.join(", ")}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
