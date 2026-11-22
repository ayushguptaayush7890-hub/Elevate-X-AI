"use client";

import React from "react";
import { ResumeFullData } from "@/types/resume-generator";
import { DesignSpecification } from "@/types/resume-design-engine";
import {
  Mail,
  Phone,
  MapPin,
  Globe,
  ExternalLink,
  GitBranch,
  Terminal,
  Calendar,
  Briefcase,
  GraduationCap,
  Award,
  Code2,
  BookOpen,
  Sparkles,
  Layers,
} from "lucide-react";

interface Props {
  resume: ResumeFullData;
  design: DesignSpecification;
  scale?: number;
  isThumbnail?: boolean;
}

export function UniversalResumeRenderer({
  resume,
  design,
  scale = 1,
  isThumbnail = false,
}: Props) {
  const { personalInfo: info, skills, education, experience, internships, projects, certifications, additional } = resume;
  const p = design.palette;

  // Typography helper classes
  const getFontFamilyClass = () => {
    switch (design.typography) {
      case "classic_serif":
        return "font-serif";
      case "technical_mono":
        return "font-mono";
      case "display_serif_body_sans":
        return "font-sans";
      case "display_sans_body_serif":
        return "font-serif";
      case "modern_sans":
      default:
        return "font-sans";
    }
  };

  const getHeaderFontClass = () => {
    switch (design.typography) {
      case "classic_serif":
      case "display_serif_body_sans":
        return "font-serif";
      case "technical_mono":
        return "font-mono";
      case "modern_sans":
      case "display_sans_body_serif":
      default:
        return "font-sans";
    }
  };

  // Spacing helper classes
  const spacingClass =
    design.spacing === "compact"
      ? "space-y-3 text-[11px] leading-snug"
      : design.spacing === "spacious"
      ? "space-y-6 text-sm leading-relaxed"
      : "space-y-4.5 text-xs leading-normal";

  const sectionHeadingCase = (text: string) => {
    if (design.headingCase === "uppercase_tracked") return text.toUpperCase();
    if (design.headingCase === "code_style") return `// ${text.toUpperCase().replace(/\s+/g, "_")}`;
    if (design.headingCase === "small_caps") return text.toUpperCase();
    return text;
  };

  // Section Header Component
  const SectionHeader = ({ title, icon }: { title: string; icon?: React.ReactNode }) => {
    const formatted = sectionHeadingCase(title);

    if (design.sectionHeaderStyle === "left_accent_bar") {
      return (
        <div className="flex items-center gap-2 mb-2 pb-0.5">
          <div className="w-1.5 h-4 rounded-xs shrink-0" style={{ backgroundColor: p.primary }} />
          <h2
            className={`font-black tracking-wider text-xs ${getHeaderFontClass()}`}
            style={{ color: p.isDark ? p.secondary : p.primary }}
          >
            {formatted}
          </h2>
        </div>
      );
    }

    if (design.sectionHeaderStyle === "pill_badge") {
      return (
        <div className="mb-2">
          <span
            className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-black tracking-wider uppercase shadow-2xs"
            style={{
              backgroundColor: `${p.primary}18`,
              color: p.isDark ? p.secondary : p.primary,
              border: `1px solid ${p.primary}40`,
            }}
          >
            {icon}
            {formatted}
          </span>
        </div>
      );
    }

    if (design.sectionHeaderStyle === "terminal_comment") {
      return (
        <div className="font-mono text-[11px] font-bold mb-2 flex items-center gap-1.5" style={{ color: p.secondary }}>
          <span>{formatted}</span>
        </div>
      );
    }

    if (design.sectionHeaderStyle === "boxed_shaded") {
      return (
        <div
          className="px-3 py-1.5 rounded-lg mb-2 flex items-center justify-between"
          style={{ backgroundColor: p.isDark ? "#1E293B" : `${p.primary}12` }}
        >
          <h2
            className={`font-black text-xs tracking-wider uppercase ${getHeaderFontClass()}`}
            style={{ color: p.isDark ? p.secondary : p.primary }}
          >
            {formatted}
          </h2>
        </div>
      );
    }

    if (design.sectionHeaderStyle === "clean_minimal") {
      return (
        <div className="mb-2">
          <h2
            className={`font-black text-xs tracking-widest uppercase flex items-center gap-2 ${getHeaderFontClass()}`}
            style={{ color: p.isDark ? p.secondary : p.primary }}
          >
            <span>{formatted}</span>
            <span className="h-px flex-1" style={{ backgroundColor: `${p.border}` }} />
          </h2>
        </div>
      );
    }

    // Default: underline_solid
    return (
      <div className="mb-2 pb-1 border-b" style={{ borderColor: `${p.primary}40` }}>
        <h2
          className={`font-black tracking-wider text-xs uppercase flex items-center gap-1.5 ${getHeaderFontClass()}`}
          style={{ color: p.isDark ? p.secondary : p.primary }}
        >
          {icon}
          {formatted}
        </h2>
      </div>
    );
  };

  // Bullet point symbol
  const BulletIcon = () => {
    if (design.bulletStyle === "code_arrow") return <span className="font-mono text-emerald-400 font-bold mr-1.5">❯</span>;
    if (design.bulletStyle === "diamond") return <span className="text-[9px] mr-1.5" style={{ color: p.secondary }}>◆</span>;
    if (design.bulletStyle === "dash") return <span className="mr-1.5 font-bold">–</span>;
    return <span className="mr-1.5 text-xs">•</span>;
  };

  // -------------------------------------------------------------
  // Section Blocks (Strictly Actual User Content Only)
  // -------------------------------------------------------------

  const SummarySection = () => {
    if (!info.summary || !info.summary.trim()) return null;
    return (
      <section className="space-y-1">
        <SectionHeader title="Professional Summary" icon={<BookOpen className="w-3.5 h-3.5" />} />
        <p className="text-justify leading-relaxed opacity-90">{info.summary}</p>
      </section>
    );
  };

  const ExperienceSection = ({ timeline = false }: { timeline?: boolean }) => {
    if (!experience || experience.length === 0) return null;
    return (
      <section className="space-y-3">
        <SectionHeader title="Work Experience" icon={<Briefcase className="w-3.5 h-3.5" />} />
        <div className={`space-y-3 ${timeline ? "relative pl-4 border-l-2 ml-1" : ""}`} style={{ borderColor: `${p.primary}40` }}>
          {experience.map((exp) => (
            <div key={exp.id} className="space-y-1 relative">
              {timeline && (
                <span
                  className="w-2.5 h-2.5 rounded-full absolute -left-[21px] top-1.5 border-2 border-white"
                  style={{ backgroundColor: p.primary }}
                />
              )}
              <div className="flex justify-between items-baseline font-semibold">
                <span className="font-bold" style={{ color: p.isDark ? "#FFFFFF" : p.textPrimary }}>
                  {exp.role}
                </span>
                <span className="text-[10px] opacity-75 font-mono">
                  {exp.startDate} – {exp.current ? "Present" : exp.endDate}
                </span>
              </div>
              <div className="flex justify-between text-[11px] font-medium" style={{ color: p.secondary }}>
                <span>{exp.company}</span>
                {exp.location && <span className="opacity-75">{exp.location}</span>}
              </div>
              {exp.responsibilities && exp.responsibilities.length > 0 && (
                <ul className="space-y-0.5 mt-1 pl-1">
                  {exp.responsibilities.map((resp, i) => (
                    <li key={i} className="flex items-start opacity-90">
                      <BulletIcon />
                      <span className="flex-1">{resp}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </section>
    );
  };

  const InternshipsSection = () => {
    if (!internships || internships.length === 0) return null;
    return (
      <section className="space-y-3">
        <SectionHeader title="Internships" icon={<Briefcase className="w-3.5 h-3.5" />} />
        <div className="space-y-3">
          {internships.map((intern) => (
            <div key={intern.id} className="space-y-1">
              <div className="flex justify-between items-baseline font-semibold">
                <span className="font-bold" style={{ color: p.isDark ? "#FFFFFF" : p.textPrimary }}>
                  {intern.role}
                </span>
                <span className="text-[10px] opacity-75 font-mono">{intern.duration}</span>
              </div>
              <div className="text-[11px] font-medium" style={{ color: p.secondary }}>
                {intern.organization}
              </div>
              {intern.workPerformed && intern.workPerformed.length > 0 && (
                <ul className="space-y-0.5 mt-1 pl-1">
                  {intern.workPerformed.map((item, i) => (
                    <li key={i} className="flex items-start opacity-90">
                      <BulletIcon />
                      <span className="flex-1">{item}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </section>
    );
  };

  const ProjectsSection = () => {
    if (!projects || projects.length === 0) return null;
    return (
      <section className="space-y-3">
        <SectionHeader title="Notable Projects" icon={<Code2 className="w-3.5 h-3.5" />} />
        <div className="space-y-3">
          {projects.map((proj) => (
            <div key={proj.id} className="space-y-1">
              <div className="flex justify-between items-baseline font-semibold">
                <div className="flex items-center gap-1.5">
                  <span className="font-bold" style={{ color: p.isDark ? "#FFFFFF" : p.textPrimary }}>
                    {proj.title}
                  </span>
                  {proj.githubUrl && (
                    <a href={proj.githubUrl} target="_blank" rel="noreferrer" className="opacity-70 hover:opacity-100">
                      <GitBranch className="w-3 h-3 inline" />
                    </a>
                  )}
                  {proj.projectUrl && (
                    <a href={proj.projectUrl} target="_blank" rel="noreferrer" className="opacity-70 hover:opacity-100">
                      <ExternalLink className="w-3 h-3 inline" />
                    </a>
                  )}
                </div>
                {proj.technologies && proj.technologies.length > 0 && (
                  <span className="text-[10px] font-mono" style={{ color: p.secondary }}>
                    {proj.technologies.slice(0, 4).join(" • ")}
                  </span>
                )}
              </div>
              {proj.description && <p className="opacity-90">{proj.description}</p>}
              {proj.contributions && proj.contributions.length > 0 && (
                <ul className="space-y-0.5 mt-0.5 pl-1">
                  {proj.contributions.map((c, i) => (
                    <li key={i} className="flex items-start opacity-90">
                      <BulletIcon />
                      <span className="flex-1">{c}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </section>
    );
  };

  const SkillsSection = ({ compact = false }: { compact?: boolean }) => {
    const hasAnySkills =
      (skills?.programmingLanguages?.length || 0) > 0 ||
      (skills?.frameworks?.length || 0) > 0 ||
      (skills?.databases?.length || 0) > 0 ||
      (skills?.developerTools?.length || 0) > 0 ||
      (skills?.aiMlSkills?.length || 0) > 0 ||
      (skills?.otherSkills?.length || 0) > 0;

    if (!hasAnySkills) return null;

    const categories = [
      { label: "Languages", items: skills?.programmingLanguages || [] },
      { label: "Frameworks", items: skills?.frameworks || [] },
      { label: "AI & ML", items: skills?.aiMlSkills || [] },
      { label: "Databases", items: skills?.databases || [] },
      { label: "Tools", items: skills?.developerTools || [] },
      { label: "Other", items: skills?.otherSkills || [] },
    ].filter((c) => c.items && c.items.length > 0);

    return (
      <section className="space-y-2">
        <SectionHeader title="Technical Skills" icon={<Code2 className="w-3.5 h-3.5" />} />
        <div className={`space-y-1.5 ${compact ? "text-[11px]" : "text-xs"}`}>
          {categories.map((cat, i) => (
            <div key={i} className={compact ? "space-y-0.5" : "flex items-baseline gap-2"}>
              <span className="font-bold shrink-0 min-w-[80px]" style={{ color: p.isDark ? p.secondary : p.primary }}>
                {cat.label}:
              </span>
              <span className="opacity-90">{cat.items.join(", ")}</span>
            </div>
          ))}
        </div>
      </section>
    );
  };

  const EducationSection = () => {
    if (!education || education.length === 0) return null;
    return (
      <section className="space-y-2.5">
        <SectionHeader title="Education" icon={<GraduationCap className="w-3.5 h-3.5" />} />
        <div className="space-y-2">
          {education.map((edu) => (
            <div key={edu.id} className="space-y-0.5">
              <div className="flex justify-between items-baseline font-semibold">
                <span className="font-bold" style={{ color: p.isDark ? "#FFFFFF" : p.textPrimary }}>
                  {edu.degree} {edu.fieldOfStudy && `in ${edu.fieldOfStudy}`}
                </span>
                <span className="text-[10px] opacity-75 font-mono">
                  {edu.startDate} – {edu.endDate}
                </span>
              </div>
              <div className="flex justify-between text-[11px]">
                <span style={{ color: p.secondary }}>{edu.institution}</span>
                {edu.grade && <span className="font-semibold text-emerald-600 dark:text-emerald-400">CGPA: {edu.grade}</span>}
              </div>
              {edu.coursework && edu.coursework.length > 0 && (
                <div className="text-[10px] opacity-75">Coursework: {edu.coursework.join(", ")}</div>
              )}
            </div>
          ))}
        </div>
      </section>
    );
  };

  const CertificationsSection = () => {
    if (!certifications || certifications.length === 0) return null;
    return (
      <section className="space-y-2">
        <SectionHeader title="Certifications" icon={<Award className="w-3.5 h-3.5" />} />
        <div className="space-y-1 text-xs">
          {certifications.map((cert) => (
            <div key={cert.id} className="flex justify-between items-baseline">
              <div>
                <span className="font-bold">{cert.name}</span>
                {cert.issuingOrganization && (
                  <span className="opacity-75 text-[11px] ml-1.5">– {cert.issuingOrganization}</span>
                )}
              </div>
              <span className="text-[10px] opacity-75 font-mono">{cert.issueDate}</span>
            </div>
          ))}
        </div>
      </section>
    );
  };

  const AdditionalSection = () => {
    const hasAdditional =
      (additional?.achievements?.length || 0) > 0 ||
      (additional?.publications?.length || 0) > 0 ||
      (additional?.languages?.length || 0) > 0;

    if (!hasAdditional) return null;

    return (
      <section className="space-y-2">
        <SectionHeader title="Honors & Achievements" icon={<Award className="w-3.5 h-3.5" />} />
        {(additional?.achievements?.length || 0) > 0 && (
          <ul className="space-y-0.5 pl-1">
            {additional.achievements.map((ach, i) => (
              <li key={i} className="flex items-start opacity-90">
                <BulletIcon />
                <span className="flex-1">{ach}</span>
              </li>
            ))}
          </ul>
        )}
        {(additional?.languages?.length || 0) > 0 && (
          <div className="text-[11px] mt-1 pt-1 border-t" style={{ borderColor: `${p.border}` }}>
            <span className="font-bold" style={{ color: p.primary }}>Languages: </span>
            <span className="opacity-90">{additional.languages.join(", ")}</span>
          </div>
        )}
      </section>
    );
  };

  // Header Component (No fake placeholder strings!)
  const RenderHeader = () => {
    const contactItems = [info.email, info.phone, info.location].filter(Boolean);
    const socialLinks = [
      info.linkedIn && { label: "LinkedIn", url: info.linkedIn, icon: <ExternalLink className="w-3 h-3" /> },
      info.gitHub && { label: "GitHub", url: info.gitHub, icon: <GitBranch className="w-3 h-3" /> },
      info.portfolio && { label: "Portfolio", url: info.portfolio, icon: <Globe className="w-3 h-3" /> },
    ].filter(Boolean) as { label: string; url: string; icon: React.ReactNode }[];

    if (!info.fullName && contactItems.length === 0) return null;

    if (design.headerStyle === "banner_accent") {
      return (
        <div className="-mx-8 -mt-8 p-6 text-white mb-6" style={{ backgroundColor: p.primary }}>
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
            <div>
              <h1 className={`text-2xl font-black tracking-tight text-white ${getHeaderFontClass()}`}>
                {info.fullName}
              </h1>
              {info.professionalTitle && (
                <p className="text-xs font-semibold tracking-wide uppercase mt-0.5 opacity-90" style={{ color: p.secondary }}>
                  {info.professionalTitle}
                </p>
              )}
            </div>
            <div className="text-right text-[11px] space-y-0.5 opacity-90 font-mono">
              <div>{contactItems.join(" • ")}</div>
              <div className="flex justify-end gap-3 text-white/90">
                {socialLinks.map((s, idx) => (
                  <a key={idx} href={s.url} target="_blank" rel="noreferrer" className="hover:underline flex items-center gap-1">
                    {s.icon} {s.label}
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      );
    }

    if (design.headerStyle === "terminal_code") {
      return (
        <div className="border border-slate-700 rounded-xl bg-slate-900/90 p-5 mb-5 space-y-3 font-mono">
          <div className="flex items-center gap-1.5 border-b border-slate-800 pb-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block" />
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block" />
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block" />
            <span className="text-[10px] text-slate-400 font-bold ml-2 flex items-center gap-1">
              <Terminal className="w-3 h-3 text-emerald-400" /> ~/profile.ts
            </span>
          </div>
          <div className="flex flex-col md:flex-row justify-between items-start md:items-baseline gap-2">
            <div>
              <h1 className="text-xl font-black text-white">{info.fullName}</h1>
              {info.professionalTitle && (
                <p className="text-xs text-emerald-400 mt-0.5">{`const role: string = "${info.professionalTitle}";`}</p>
              )}
            </div>
            <div className="text-right text-[11px] text-slate-400 space-y-0.5">
              <div>{contactItems.join(" | ")}</div>
              <div className="flex justify-end gap-2.5 text-emerald-400">
                {socialLinks.map((s, idx) => (
                  <a key={idx} href={s.url} target="_blank" rel="noreferrer" className="hover:underline flex items-center gap-1">
                    {s.icon} {s.label.toLowerCase()}
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      );
    }

    if (design.headerStyle === "centered_classic") {
      return (
        <div className="text-center space-y-1.5 mb-5 pb-4 border-b" style={{ borderColor: `${p.primary}30` }}>
          <h1 className={`text-2xl font-black tracking-tight ${getHeaderFontClass()}`} style={{ color: p.isDark ? "#FFFFFF" : p.primary }}>
            {info.fullName}
          </h1>
          {info.professionalTitle && (
            <p className="text-xs font-semibold uppercase tracking-widest" style={{ color: p.secondary }}>
              {info.professionalTitle}
            </p>
          )}
          <div className="text-[11px] opacity-80 flex flex-wrap justify-center items-center gap-x-3 gap-y-1 pt-0.5">
            {contactItems.map((c, i) => (
              <span key={i} className="flex items-center gap-1">
                {c}
              </span>
            ))}
            {socialLinks.map((s, idx) => (
              <a key={idx} href={s.url} target="_blank" rel="noreferrer" className="hover:underline flex items-center gap-1" style={{ color: p.primary }}>
                {s.icon} {s.label}
              </a>
            ))}
          </div>
        </div>
      );
    }

    // Default: minimal_inline
    return (
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-baseline pb-4 mb-5 border-b gap-3" style={{ borderColor: `${p.primary}30` }}>
        <div>
          <h1 className={`text-2xl font-black tracking-tight leading-tight ${getHeaderFontClass()}`} style={{ color: p.isDark ? "#FFFFFF" : p.primary }}>
            {info.fullName}
          </h1>
          {info.professionalTitle && (
            <p className="text-xs font-bold tracking-wide uppercase mt-0.5" style={{ color: p.secondary }}>
              {info.professionalTitle}
            </p>
          )}
        </div>
        <div className="text-right text-[11px] opacity-85 space-y-0.5 font-sans">
          <div>{contactItems.join(" • ")}</div>
          <div className="flex justify-end gap-3 font-medium" style={{ color: p.primary }}>
            {socialLinks.map((s, idx) => (
              <a key={idx} href={s.url} target="_blank" rel="noreferrer" className="hover:underline flex items-center gap-1">
                {s.icon} {s.label}
              </a>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Section Ordering Matrix
  const renderOrderedSections = () => {
    if (design.sectionOrder === "skills_first") {
      return (
        <>
          <SkillsSection />
          <ProjectsSection />
          <ExperienceSection />
          <InternshipsSection />
          <EducationSection />
          <CertificationsSection />
          <AdditionalSection />
        </>
      );
    }

    if (design.sectionOrder === "education_first") {
      return (
        <>
          <EducationSection />
          <ProjectsSection />
          <SkillsSection />
          <InternshipsSection />
          <ExperienceSection />
          <CertificationsSection />
          <AdditionalSection />
        </>
      );
    }

    if (design.sectionOrder === "projects_first") {
      return (
        <>
          <ProjectsSection />
          <SkillsSection />
          <ExperienceSection />
          <InternshipsSection />
          <EducationSection />
          <CertificationsSection />
          <AdditionalSection />
        </>
      );
    }

    // Default: experience_first
    return (
      <>
        <ExperienceSection />
        <InternshipsSection />
        <ProjectsSection />
        <SkillsSection />
        <EducationSection />
        <CertificationsSection />
        <AdditionalSection />
      </>
    );
  };

  // -------------------------------------------------------------
  // DISTINCT BASE LAYOUT ARCHITECTURES (8 Genuinely Diverse Compositions)
  // -------------------------------------------------------------

  // LAYOUT 1: Two-Column Left Sidebar (35 / 65 Asymmetric)
  if (design.layout === "two_column_left_sidebar") {
    return (
      <div
        className={`shadow-xl rounded-xl overflow-hidden max-w-[850px] mx-auto min-h-[1050px] border flex flex-col ${getFontFamilyClass()}`}
        style={{
          backgroundColor: p.background,
          borderColor: p.border,
          color: p.textPrimary,
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: "top center",
        }}
      >
        <div className="grid grid-cols-12 flex-1">
          {/* Left Sidebar (35%) */}
          <div
            className="col-span-12 md:col-span-4 p-6 space-y-5 flex flex-col justify-between"
            style={{ backgroundColor: p.isDark ? "#1E293B" : p.primary, color: "#FFFFFF" }}
          >
            <div className="space-y-5">
              <div className="border-b border-white/20 pb-4">
                <h1 className={`text-xl font-black text-white ${getHeaderFontClass()}`}>{info.fullName}</h1>
                {info.professionalTitle && (
                  <p className="text-xs uppercase tracking-wider font-semibold opacity-85 mt-0.5" style={{ color: p.secondary }}>
                    {info.professionalTitle}
                  </p>
                )}
              </div>

              {/* Contact */}
              <div className="space-y-1.5 text-xs opacity-90">
                <div className="text-[10px] font-black uppercase tracking-widest" style={{ color: p.secondary }}>
                  Contact
                </div>
                {info.email && <div className="break-all flex items-center gap-1.5"><Mail className="w-3 h-3 shrink-0" /> {info.email}</div>}
                {info.phone && <div className="flex items-center gap-1.5"><Phone className="w-3 h-3 shrink-0" /> {info.phone}</div>}
                {info.location && <div className="flex items-center gap-1.5"><MapPin className="w-3 h-3 shrink-0" /> {info.location}</div>}
              </div>

              {/* Skills */}
              <SkillsSection compact />

              {/* Education in sidebar */}
              <EducationSection />
            </div>
          </div>

          {/* Right Main Pane (65%) */}
          <div className="col-span-12 md:col-span-8 p-6 space-y-5">
            <SummarySection />
            <ExperienceSection />
            <InternshipsSection />
            <ProjectsSection />
            <CertificationsSection />
            <AdditionalSection />
          </div>
        </div>
      </div>
    );
  }

  // LAYOUT 2: Two-Column Right Sidebar (65 / 35 Asymmetric)
  if (design.layout === "two_column_right_sidebar") {
    return (
      <div
        className={`shadow-xl rounded-xl overflow-hidden max-w-[850px] mx-auto min-h-[1050px] border flex flex-col ${getFontFamilyClass()}`}
        style={{
          backgroundColor: p.background,
          borderColor: p.border,
          color: p.textPrimary,
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: "top center",
        }}
      >
        <div className="p-6 border-b" style={{ borderColor: `${p.primary}30` }}>
          <RenderHeader />
        </div>
        <div className="grid grid-cols-12 flex-1">
          {/* Main Left Content Pane (65%) */}
          <div className="col-span-12 md:col-span-8 p-6 space-y-5 border-r" style={{ borderColor: `${p.primary}20` }}>
            <SummarySection />
            <ExperienceSection />
            <InternshipsSection />
            <ProjectsSection />
          </div>

          {/* Right Sidebar (35%) */}
          <div
            className="col-span-12 md:col-span-4 p-6 space-y-5"
            style={{ backgroundColor: p.cardBg }}
          >
            <SkillsSection compact />
            <EducationSection />
            <CertificationsSection />
            <AdditionalSection />
          </div>
        </div>
      </div>
    );
  }

  // LAYOUT 3: Two-Column Balanced (50 / 50 Dual Column Grid)
  if (design.layout === "two_column_balanced") {
    return (
      <div
        className={`shadow-xl rounded-xl max-w-[850px] mx-auto min-h-[1050px] p-8 border ${getFontFamilyClass()}`}
        style={{
          backgroundColor: p.background,
          borderColor: p.border,
          color: p.textPrimary,
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: "top center",
        }}
      >
        <RenderHeader />
        <SummarySection />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          {/* Left Column */}
          <div className="space-y-5">
            <ExperienceSection timeline={true} />
            <InternshipsSection />
          </div>

          {/* Right Column */}
          <div className="space-y-5">
            <ProjectsSection />
            <SkillsSection />
            <EducationSection />
            <CertificationsSection />
            <AdditionalSection />
          </div>
        </div>
      </div>
    );
  }

  // LAYOUT 4: Compact Technical Terminal (Dark Console Matrix)
  if (design.layout === "compact_technical_terminal") {
    return (
      <div
        className={`shadow-2xl rounded-2xl max-w-[850px] mx-auto min-h-[1050px] p-6 border font-mono ${spacingClass}`}
        style={{
          backgroundColor: "#0B0F19",
          borderColor: "#1E293B",
          color: "#E2E8F0",
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: "top center",
        }}
      >
        <div className="border border-slate-800 rounded-xl bg-slate-900/90 p-4 mb-4">
          <div className="flex items-center gap-1.5 pb-2 border-b border-slate-800 text-[10px] text-slate-400">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500/80 inline-block" />
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500/80 inline-block" />
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/80 inline-block" />
            <span className="ml-2 text-emerald-400 font-bold">bash: ~/profile.sh --render-json</span>
          </div>
          <div className="pt-3 flex flex-col md:flex-row justify-between items-start md:items-baseline gap-2">
            <div>
              <h1 className="text-xl font-black text-white">{info.fullName}</h1>
              {info.professionalTitle && (
                <p className="text-xs text-emerald-400 font-bold mt-0.5">{`> ${info.professionalTitle}`}</p>
              )}
            </div>
            <div className="text-right text-[11px] text-slate-400">
              {[info.email, info.phone, info.location].filter(Boolean).join(" • ")}
            </div>
          </div>
        </div>

        <SummarySection />
        <div className="space-y-4">
          <ProjectsSection />
          <SkillsSection />
          <ExperienceSection />
          <InternshipsSection />
          <EducationSection />
          <CertificationsSection />
          <AdditionalSection />
        </div>
      </div>
    );
  }

  // LAYOUT 5: Executive Bordered Frame (Leadership Elegance)
  if (design.layout === "executive_bordered_frame") {
    return (
      <div
        className={`shadow-2xl max-w-[850px] mx-auto min-h-[1050px] p-8 border-4 border-double ${spacingClass} ${getFontFamilyClass()}`}
        style={{
          backgroundColor: p.background,
          borderColor: p.primary,
          color: p.textPrimary,
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: "top center",
        }}
      >
        <div className="text-center space-y-1.5 pb-4 mb-6 border-b-2" style={{ borderColor: `${p.primary}` }}>
          <h1 className={`text-2xl font-black tracking-wider uppercase ${getHeaderFontClass()}`} style={{ color: p.primary }}>
            {info.fullName}
          </h1>
          {info.professionalTitle && (
            <p className="text-xs font-bold uppercase tracking-widest" style={{ color: p.secondary }}>
              {info.professionalTitle}
            </p>
          )}
          <div className="text-[11px] opacity-80 flex flex-wrap justify-center gap-3 pt-1">
            {[info.email, info.phone, info.location].filter(Boolean).join(" | ")}
          </div>
        </div>

        <SummarySection />
        <ExperienceSection timeline={true} />
        <InternshipsSection />
        <ProjectsSection />
        <SkillsSection />
        <EducationSection />
        <CertificationsSection />
        <AdditionalSection />
      </div>
    );
  }

  // LAYOUT 6: Split Header Single (Creative Portfolio Banner)
  if (design.layout === "split_header_single") {
    return (
      <div
        className={`shadow-xl rounded-xl max-w-[850px] mx-auto min-h-[1050px] overflow-hidden border ${getFontFamilyClass()}`}
        style={{
          backgroundColor: p.background,
          borderColor: p.border,
          color: p.textPrimary,
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: "top center",
        }}
      >
        <div className="p-8 text-white" style={{ background: `linear-gradient(135deg, ${p.primary} 0%, ${p.secondary} 100%)` }}>
          <h1 className={`text-3xl font-black tracking-tight text-white ${getHeaderFontClass()}`}>
            {info.fullName}
          </h1>
          {info.professionalTitle && (
            <p className="text-sm font-bold uppercase tracking-wider text-white/90 mt-1">
              {info.professionalTitle}
            </p>
          )}
          <div className="flex flex-wrap gap-4 text-xs text-white/80 pt-3">
            {[info.email, info.phone, info.location].filter(Boolean).map((c, i) => (
              <span key={i} className="flex items-center gap-1">{c}</span>
            ))}
          </div>
        </div>

        <div className={`p-8 ${spacingClass}`}>
          <SummarySection />
          {renderOrderedSections()}
        </div>
      </div>
    );
  }

  // LAYOUT 7: Single Column Modern (Clean Offset Minimal)
  if (design.layout === "single_column_modern") {
    return (
      <div
        className={`shadow-xl rounded-xl max-w-[850px] mx-auto min-h-[1050px] p-8 border ${spacingClass} ${getFontFamilyClass()}`}
        style={{
          backgroundColor: p.background,
          borderColor: p.border,
          color: p.textPrimary,
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: "top center",
        }}
      >
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-baseline pb-4 mb-4 border-b-2" style={{ borderColor: p.primary }}>
          <div>
            <h1 className={`text-2xl font-black tracking-tight ${getHeaderFontClass()}`} style={{ color: p.primary }}>
              {info.fullName}
            </h1>
            {info.professionalTitle && (
              <p className="text-xs font-bold uppercase tracking-wide mt-0.5" style={{ color: p.secondary }}>
                {info.professionalTitle}
              </p>
            )}
          </div>
          <div className="text-right text-[11px] opacity-80">
            {[info.email, info.phone, info.location].filter(Boolean).join(" • ")}
          </div>
        </div>

        <SummarySection />
        {renderOrderedSections()}
      </div>
    );
  }

  // LAYOUT 8: Single Column Classic (Standard ATS Parser Safe)
  return (
    <div
      className={`shadow-xl rounded-xl max-w-[850px] mx-auto min-h-[1050px] p-8 border ${spacingClass} ${getFontFamilyClass()}`}
      style={{
        backgroundColor: p.background,
        borderColor: p.border,
        color: p.textPrimary,
        transform: scale !== 1 ? `scale(${scale})` : undefined,
        transformOrigin: "top center",
      }}
    >
      <div className="text-center pb-3 mb-4 border-b" style={{ borderColor: `${p.primary}40` }}>
        <h1 className={`text-2xl font-black tracking-tight ${getHeaderFontClass()}`} style={{ color: p.primary }}>
          {info.fullName}
        </h1>
        {info.professionalTitle && (
          <p className="text-xs font-semibold tracking-wider uppercase mt-0.5" style={{ color: p.secondary }}>
            {info.professionalTitle}
          </p>
        )}
        <div className="text-[11px] opacity-80 flex flex-wrap justify-center gap-3 pt-1">
          {[info.email, info.phone, info.location].filter(Boolean).join(" | ")}
        </div>
      </div>

      <SummarySection />
      {renderOrderedSections()}
    </div>
  );
}
