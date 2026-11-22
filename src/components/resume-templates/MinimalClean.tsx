"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";

export function MinimalClean({ resume }: { resume: ResumeFullData }) {
  const { personalInfo: info, skills, education, experience, internships, projects, certifications, additional } = resume;

  return (
    <div className="bg-white text-zinc-900 shadow-sm max-w-[850px] mx-auto min-h-[1050px] p-10 font-sans border border-zinc-200 print:shadow-none print:border-none print:m-0 print:p-6 print:w-full">
      {/* Centered Minimal Header */}
      <div className="text-center space-y-2 border-b border-zinc-200 pb-6 mb-6">
        <h1 className="text-2xl font-light tracking-widest text-zinc-950 uppercase">
          {info.fullName || "Your Full Name"}
        </h1>
        <p className="text-xs text-zinc-500 tracking-wider uppercase font-medium">
          {info.professionalTitle || "Professional Title"}
        </p>
        <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1 text-xs text-zinc-600 pt-1">
          {info.email && <span>{info.email}</span>}
          {info.phone && <span>• {info.phone}</span>}
          {info.location && <span>• {info.location}</span>}
          {info.linkedIn && (
            <span>• <a href={info.linkedIn} target="_blank" rel="noreferrer" className="underline hover:text-zinc-900">LinkedIn</a></span>
          )}
          {info.gitHub && (
            <span>• <a href={info.gitHub} target="_blank" rel="noreferrer" className="underline hover:text-zinc-900">GitHub</a></span>
          )}
          {info.portfolio && (
            <span>• <a href={info.portfolio} target="_blank" rel="noreferrer" className="underline hover:text-zinc-900">Portfolio</a></span>
          )}
        </div>
      </div>

      <div className="space-y-6 text-xs leading-relaxed">
        {/* Summary */}
        {info.summary && (
          <div className="space-y-2">
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-zinc-400">Profile</h2>
            <p className="text-zinc-700 leading-normal">{info.summary}</p>
          </div>
        )}

        {/* Experience */}
        {experience.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-zinc-400">Experience</h2>
            {experience.map((exp) => (
              <div key={exp.id} className="space-y-1">
                <div className="flex justify-between items-baseline">
                  <div className="font-semibold text-zinc-900">
                    {exp.role} <span className="font-normal text-zinc-500">— {exp.company}</span>
                  </div>
                  <div className="text-[11px] text-zinc-400 tabular-nums">
                    {exp.startDate} – {exp.endDate || "Present"}
                  </div>
                </div>
                {exp.responsibilities.length > 0 && (
                  <ul className="list-disc list-outside pl-4 space-y-0.5 text-zinc-600">
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
          <div className="space-y-4">
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-zinc-400">Projects</h2>
            {projects.map((proj) => (
              <div key={proj.id} className="space-y-1">
                <div className="flex justify-between items-baseline">
                  <div className="font-semibold text-zinc-900">
                    {proj.title}
                    {proj.technologies.length > 0 && (
                      <span className="font-normal text-zinc-500 text-[11px]"> ({proj.technologies.join(", ")})</span>
                    )}
                  </div>
                  {proj.githubUrl && (
                    <a href={proj.githubUrl} target="_blank" rel="noreferrer" className="text-zinc-400 hover:text-zinc-800 underline text-[11px]">
                      View Code
                    </a>
                  )}
                </div>
                {proj.description && <p className="text-zinc-600">{proj.description}</p>}
                {proj.contributions.length > 0 && (
                  <ul className="list-disc list-outside pl-4 space-y-0.5 text-zinc-600">
                    {proj.contributions.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Education */}
        {education.length > 0 && (
          <div className="space-y-3">
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-zinc-400">Education</h2>
            {education.map((edu) => (
              <div key={edu.id} className="flex justify-between items-baseline">
                <div>
                  <div className="font-semibold text-zinc-900">{edu.degree} in {edu.fieldOfStudy}</div>
                  <div className="text-zinc-500">{edu.institution} {edu.grade && `• Grade: ${edu.grade}`}</div>
                </div>
                <div className="text-zinc-400 text-[11px] tabular-nums">{edu.startDate} – {edu.endDate}</div>
              </div>
            ))}
          </div>
        )}

        {/* Skills */}
        <div className="space-y-2">
          <h2 className="text-[11px] font-bold uppercase tracking-widest text-zinc-400">Skills</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-zinc-700">
            {skills.programmingLanguages.length > 0 && (
              <div><strong className="font-semibold">Languages:</strong> {skills.programmingLanguages.join(", ")}</div>
            )}
            {skills.frameworks.length > 0 && (
              <div><strong className="font-semibold">Frameworks:</strong> {skills.frameworks.join(", ")}</div>
            )}
            {skills.databases.length > 0 && (
              <div><strong className="font-semibold">Databases:</strong> {skills.databases.join(", ")}</div>
            )}
            {skills.developerTools.length > 0 && (
              <div><strong className="font-semibold">Tools:</strong> {skills.developerTools.join(", ")}</div>
            )}
            {skills.aiMlSkills.length > 0 && (
              <div><strong className="font-semibold">AI/ML:</strong> {skills.aiMlSkills.join(", ")}</div>
            )}
          </div>
        </div>

        {/* Certifications & Additional */}
        {(certifications.length > 0 || additional.achievements.length > 0) && (
          <div className="space-y-2 pt-2 border-t border-zinc-100">
            <h2 className="text-[11px] font-bold uppercase tracking-widest text-zinc-400">Certifications & Honors</h2>
            <ul className="list-disc list-outside pl-4 space-y-0.5 text-zinc-600">
              {certifications.map((c) => (
                <li key={c.id}>{c.name} — {c.issuingOrganization} ({c.issueDate})</li>
              ))}
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
