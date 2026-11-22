"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";

export function ATSFriendly({ resume }: { resume: ResumeFullData }) {
  const { personalInfo: info, skills, education, experience, internships, projects, certifications, additional } = resume;

  return (
    <div className="bg-white text-black max-w-[850px] mx-auto min-h-[1050px] p-8 font-serif leading-normal border border-gray-300 print:border-none print:m-0 print:p-4 print:w-full">
      {/* ATS Header: Name and Contact centered, standard text */}
      <div className="text-center border-b pb-2 mb-4">
        <h1 className="text-xl font-bold uppercase tracking-wide">{info.fullName || "Candidate Name"}</h1>
        {info.professionalTitle && <p className="text-sm italic">{info.professionalTitle}</p>}
        <p className="text-xs mt-1">
          {[
            info.location,
            info.phone,
            info.email,
            info.linkedIn && `LinkedIn: ${info.linkedIn}`,
            info.gitHub && `GitHub: ${info.gitHub}`,
            info.portfolio && `Portfolio: ${info.portfolio}`
          ].filter(Boolean).join(" | ")}
        </p>
      </div>

      <div className="space-y-4 text-xs">
        {/* Professional Summary */}
        {info.summary && (
          <div>
            <h2 className="font-bold uppercase tracking-wider text-xs border-b border-black pb-0.5 mb-1.5">
              Professional Summary
            </h2>
            <p className="text-justify">{info.summary}</p>
          </div>
        )}

        {/* Technical Skills */}
        <div>
          <h2 className="font-bold uppercase tracking-wider text-xs border-b border-black pb-0.5 mb-1.5">
            Technical Skills
          </h2>
          <div className="space-y-0.5">
            {skills.programmingLanguages.length > 0 && (
              <p><strong>Languages:</strong> {skills.programmingLanguages.join(", ")}</p>
            )}
            {skills.frameworks.length > 0 && (
              <p><strong>Frameworks & Libraries:</strong> {skills.frameworks.join(", ")}</p>
            )}
            {skills.databases.length > 0 && (
              <p><strong>Databases:</strong> {skills.databases.join(", ")}</p>
            )}
            {skills.developerTools.length > 0 && (
              <p><strong>Tools & Platforms:</strong> {skills.developerTools.join(", ")}</p>
            )}
            {skills.aiMlSkills.length > 0 && (
              <p><strong>AI & Machine Learning:</strong> {skills.aiMlSkills.join(", ")}</p>
            )}
            {skills.otherSkills.length > 0 && (
              <p><strong>Other Skills:</strong> {skills.otherSkills.join(", ")}</p>
            )}
          </div>
        </div>

        {/* Experience */}
        {experience.length > 0 && (
          <div>
            <h2 className="font-bold uppercase tracking-wider text-xs border-b border-black pb-0.5 mb-1.5">
              Professional Experience
            </h2>
            <div className="space-y-3">
              {experience.map((exp) => (
                <div key={exp.id}>
                  <div className="flex justify-between font-bold">
                    <span>{exp.role} – {exp.company}</span>
                    <span>{exp.startDate} – {exp.endDate || "Present"}</span>
                  </div>
                  {exp.location && <div className="italic text-[11px] mb-1">{exp.location}</div>}
                  {exp.responsibilities.length > 0 && (
                    <ul className="list-disc pl-5 space-y-0.5">
                      {exp.responsibilities.map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Projects */}
        {projects.length > 0 && (
          <div>
            <h2 className="font-bold uppercase tracking-wider text-xs border-b border-black pb-0.5 mb-1.5">
              Technical Projects
            </h2>
            <div className="space-y-2.5">
              {projects.map((proj) => (
                <div key={proj.id}>
                  <div className="flex justify-between font-bold">
                    <span>{proj.title} {proj.technologies.length > 0 && `(${proj.technologies.join(", ")})`}</span>
                    {proj.githubUrl && <span className="text-[11px] font-normal">{proj.githubUrl}</span>}
                  </div>
                  {proj.description && <p className="mb-0.5">{proj.description}</p>}
                  {proj.contributions.length > 0 && (
                    <ul className="list-disc pl-5 space-y-0.5">
                      {proj.contributions.map((c, i) => (
                        <li key={i}>{c}</li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Education */}
        {education.length > 0 && (
          <div>
            <h2 className="font-bold uppercase tracking-wider text-xs border-b border-black pb-0.5 mb-1.5">
              Education
            </h2>
            <div className="space-y-1.5">
              {education.map((edu) => (
                <div key={edu.id}>
                  <div className="flex justify-between font-bold">
                    <span>{edu.degree} in {edu.fieldOfStudy}</span>
                    <span>{edu.startDate} – {edu.endDate}</span>
                  </div>
                  <div className="flex justify-between italic text-[11px]">
                    <span>{edu.institution}</span>
                    {edu.grade && <span>Grade: {edu.grade}</span>}
                  </div>
                  {edu.coursework.length > 0 && (
                    <p className="text-[11px]">Relevant Coursework: {edu.coursework.join(", ")}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Certifications & Additional */}
        {(certifications.length > 0 || additional.achievements.length > 0) && (
          <div>
            <h2 className="font-bold uppercase tracking-wider text-xs border-b border-black pb-0.5 mb-1.5">
              Certifications & Honors
            </h2>
            <ul className="list-disc pl-5 space-y-0.5">
              {certifications.map((c) => (
                <li key={c.id}>{c.name} – {c.issuingOrganization} ({c.issueDate})</li>
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
