"use client";

import React from "react";
import Link from "next/link";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { FullScreenHeroSection } from "@/components/landing/FullScreenHeroSection";
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Award,
  Briefcase,
  GitCompare,
  FileText,
  MapPin,
  TrendingUp,
  CheckCircle2,
  Users,
  Compass,
  ArrowUpRight,
  Zap,
  Target,
  Cpu,
  Layers,
  Clock
} from "lucide-react";

export default function LandingPage() {
  // Realistic Vocational Trade Profiles (Demonstrating informal-to-formal gap)
  const workerProfiles = [
    {
      title: "Ramesh Sharma",
      trade: "Master Tailor & Pattern Artisan",
      experience: "5 Years Hands-on",
      barrier: "Extensive lockstitch machine mastery and pattern grading unrecognized by formal corporate export recruiters.",
      icon: "✂️",
      accent: "border-[#D6A84B]/40 bg-white shadow-xs",
    },
    {
      title: "Sunita Verma",
      trade: "Commercial Baker & Confectioner",
      experience: "4 Years Workshop",
      barrier: "Managed workshop recipes and food safety standards; lacks formal culinary arts certification on paper.",
      icon: "🍞",
      accent: "border-[#C77B54]/40 bg-white shadow-xs",
    },
    {
      title: "Mohd. Arif",
      trade: "Domestic & Solar Electrician",
      experience: "6 Years Fieldwork",
      barrier: "Wired 150+ residential systems; seeks validation to qualify for industrial electrical and solar installations.",
      icon: "⚡",
      accent: "border-[#3478F6]/40 bg-white shadow-xs",
    },
    {
      title: "Rajesh Kumar",
      trade: "Heavy Automotive Technician",
      experience: "7 Years Garage",
      barrier: "Overhauls diesel engines and hydraulic assemblies daily; no formal digital resume for fleet operations.",
      icon: "🔧",
      accent: "border-[#7355D9]/40 bg-white shadow-xs",
    },
    {
      title: "Anita Devi",
      trade: "Handloom Weaving Supervisor",
      experience: "8 Years Craft Guild",
      barrier: "Coordinates warp tension, dye matching, and apprenticeships; formal brands require structured credentialing.",
      icon: "🎨",
      accent: "border-[#D6A84B]/40 bg-white shadow-xs",
    },
    {
      title: "Vikas Singh",
      trade: "Cold-Chain Logistics Handler",
      experience: "3 Years Route Dispatch",
      barrier: "Operates temperature-sensitive logistics corridors; seeks recognized certification for national carriers.",
      icon: "📦",
      accent: "border-[#27856B]/40 bg-white shadow-xs",
    },
  ];

  // 6 Solution Modules (Royal Gold Edition)
  const solutions = [
    {
      title: "Recognize Experience",
      description: "Convert colloquial spoken trade descriptions into standardized NSQF and O*NET vocational competencies.",
      href: "/experience",
      icon: <Sparkles className="w-6 h-6 text-[#7355D9]" />,
      badge: "Voice & Text AI",
      borderGlow: "hover:border-[#7355D9]",
    },
    {
      title: "Assess Skills",
      description: "Complete scenario-based diagnostic assessments that demonstrate tactile know-how with verifiable badges.",
      href: "/assessment",
      icon: <Award className="w-6 h-6 text-[#3478F6]" />,
      badge: "Adaptive Diagnostics",
      borderGlow: "hover:border-[#3478F6]",
    },
    {
      title: "Discover Opportunities",
      description: "Review curated formal sector job listings with transparent, explainable skill compatibility criteria.",
      href: "/jobs",
      icon: <Briefcase className="w-6 h-6 text-[#D6A84B]" />,
      badge: "Curated Directory",
      borderGlow: "hover:border-[#D6A84B]",
    },
    {
      title: "Analyze Skill Gaps",
      description: "Identify the exact delta between your current practice and what higher-paying export roles require.",
      href: "/skill-gap",
      icon: <GitCompare className="w-6 h-6 text-[#C77B54]" />,
      badge: "Delta Visualizer",
      borderGlow: "hover:border-[#C77B54]",
    },
    {
      title: "Build Your Resume",
      description: "Generate corporate ATS-ready resumes highlighting verified trade achievements without fabricating claims.",
      href: "/resume",
      icon: <FileText className="w-6 h-6 text-[#7355D9]" />,
      badge: "ATS Studio",
      borderGlow: "hover:border-[#7355D9]",
    },
    {
      title: "Plan Your Future",
      description: "Follow customized weekly roadmaps featuring hands-on milestones and free vocational learning resources.",
      href: "/roadmap",
      icon: <MapPin className="w-6 h-6 text-[#27856B]" />,
      badge: "Roadmap Engine",
      borderGlow: "hover:border-[#27856B]",
    },
  ];

  // 6-Step Career Journey
  const journeySteps = [
    { step: "01", title: "Real Experience", desc: "Speak or type your trade background in everyday conversational language." },
    { step: "02", title: "Skill Recognition", desc: "AI maps your tactile work to formal occupational and vocational standards." },
    { step: "03", title: "Skill Assessment", desc: "Complete practical scenario tests to earn verifiable capability badges." },
    { step: "04", title: "Job Matching", desc: "Review vetted openings with clear, transparent compatibility breakdowns." },
    { step: "05", title: "Targeted Learning", desc: "Bridge identified gaps through targeted exercises and learning sandboxes." },
    { step: "06", title: "Career Growth", desc: "Deploy your verified resume into higher-paying formal employment." },
  ];

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A] selection:bg-[#D6A84B]/30 selection:text-[#17233F] relative overflow-x-hidden">
      <Navbar />

      {/* =========================================================================
          SECTION 1: FULL-SCREEN IMMERSIVE ANIMATED HERO (100vw x 100svh)
          Existing 190-Frame JPG Sequence + Dark Translucent Vignette + Holographic Glass Cards
         ========================================================================= */}
      <FullScreenHeroSection />

      {/* =========================================================================
          SECTION 2: THE PROBLEM ("Millions Have Practical Know-How.")
         ========================================================================= */}
      <section className="py-24 relative bg-[#F5F0E6] border-t border-[#E6DFD1]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-3 mb-16">
            <span className="text-xs font-black uppercase tracking-widest text-[#9A7320] bg-[#D6A84B]/15 border border-[#D6A84B]/35 px-3.5 py-1 rounded-full">
              The Real-World Reality
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#17233F] tracking-tight">
              Millions Have Practical Know-How. <br />
              <span className="gradient-sunset-text">
                Traditional Systems Overlook It.
              </span>
            </h2>
            <p className="text-[#687187] text-sm sm:text-base leading-relaxed">
              Craftsmen, technicians, mechanics, and culinary artisans build deep tactile expertise on the job. Yet conventional HR filters reject them without formal diplomas.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {workerProfiles.map((wp, i) => (
              <div
                key={i}
                className={`rounded-3xl p-6 border shadow-xs transition-all duration-300 hover:shadow-xl hover:-translate-y-1.5 ${wp.accent} flex flex-col justify-between`}
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-3xl">{wp.icon}</span>
                    <span className="text-[11px] font-bold text-[#17233F] bg-[#F5F0E6] px-2.5 py-1 rounded-full border border-[#E6DFD1]">
                      {wp.experience}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-base font-black text-[#17233F]">{wp.title}</h3>
                    <p className="text-xs font-bold text-[#D6A84B]">{wp.trade}</p>
                  </div>
                  <p className="text-xs text-[#687187] leading-relaxed pt-1">
                    {wp.barrier}
                  </p>
                </div>

                <div className="pt-4 mt-3 border-t border-[#E6DFD1] flex items-center justify-between text-[11px] font-bold text-[#17233F]">
                  <span>Elevate X AI bridges this gap</span>
                  <ArrowRight className="w-3.5 h-3.5 text-[#D6A84B]" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 3: INTELLIGENT CAREER ARCHITECTURE (6 Core Modules)
         ========================================================================= */}
      <section id="features" className="py-24 relative overflow-hidden bg-white border-t border-[#E6DFD1]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto space-y-3 mb-16">
            <span className="text-xs font-black uppercase tracking-widest text-[#7355D9] bg-[#7355D9]/10 border border-[#7355D9]/30 px-3.5 py-1 rounded-full">
              Intelligent Career Architecture
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#17233F] tracking-tight">
              One Unified Platform. Real Career Growth.
            </h2>
            <p className="text-[#687187] text-sm sm:text-base leading-relaxed">
              Six synchronized engines transforming everyday informal work into structured credentials, targeted upskilling, and formal employment.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {solutions.map((sol, i) => (
              <Link key={i} href={sol.href} className="group block">
                <div
                  className={`glass-card-ivory-interactive rounded-3xl p-7 h-full flex flex-col justify-between space-y-5 bg-[#FBF8F1] border border-[#E6DFD1] shadow-xs ${sol.borderGlow} transition-all`}
                >
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="w-12 h-12 rounded-2xl bg-white flex items-center justify-center border border-[#E6DFD1] shadow-xs group-hover:scale-110 transition-transform">
                        {sol.icon}
                      </div>
                      <span className="text-[10px] font-extrabold uppercase tracking-wider text-[#17233F] bg-white px-2.5 py-1 rounded-full border border-[#E6DFD1]">
                        {sol.badge}
                      </span>
                    </div>

                    <h3 className="text-lg font-black text-[#17233F] group-hover:text-[#D6A84B] transition-colors flex items-center gap-1.5">
                      {sol.title} <ArrowUpRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity text-[#D6A84B]" />
                    </h3>

                    <p className="text-xs text-[#687187] leading-relaxed">
                      {sol.description}
                    </p>
                  </div>

                  <div className="pt-2 text-xs font-bold text-[#D6A84B] flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                    <span>Explore Module</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 4: 6-STEP CAREER JOURNEY
         ========================================================================= */}
      <section id="how-it-works" className="py-24 relative bg-[#F5F0E6] border-t border-[#E6DFD1]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-3 mb-16">
            <span className="text-xs font-black uppercase tracking-widest text-[#27856B] bg-[#27856B]/10 border border-[#27856B]/30 px-3.5 py-1 rounded-full">
              Structured Progression
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#17233F] tracking-tight">
              From Informal Practice to Formal Growth
            </h2>
            <p className="text-[#687187] text-sm sm:text-base leading-relaxed">
              A transparent, step-by-step roadmap guiding trade workers from unverified local roles to corporate employment tracks.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
            {journeySteps.map((step, idx) => (
              <div
                key={idx}
                className="glass-card-ivory rounded-3xl p-5 border border-[#E6DFD1] bg-white flex flex-col justify-between space-y-4 hover:border-[#D6A84B] transition-all hover:-translate-y-1 shadow-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-black gradient-gold-text font-mono">
                    {step.step}
                  </span>
                  <div className="w-2.5 h-2.5 rounded-full bg-[#D6A84B]" />
                </div>
                <div>
                  <h3 className="text-xs font-bold text-[#17233F]">{step.title}</h3>
                  <p className="text-[11px] text-[#687187] leading-relaxed mt-1">
                    {step.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 5: LIVE AI TRANSFORMATION ENGINE (Interactive Demo Showcase)
         ========================================================================= */}
      <section className="py-24 relative bg-white border-t border-[#E6DFD1]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-3 mb-16">
            <span className="text-xs font-black uppercase tracking-widest text-[#7355D9] bg-[#7355D9]/10 border border-[#7355D9]/30 px-3.5 py-1 rounded-full">
              Live AI Transformation
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#17233F] tracking-tight">
              Everyday Testimony Turned Into Standardized Skills
            </h2>
            <p className="text-[#687187] text-sm sm:text-base leading-relaxed">
              Watch how conversational worker descriptions are structured and mapped into recognized industry taxonomy in real time.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
            {/* Left: Real Worker Narrative */}
            <div className="rounded-3xl p-8 border border-[#E6DFD1] bg-[#FBF8F1] space-y-5 flex flex-col justify-between shadow-xs">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-black text-[#17233F] uppercase tracking-wider flex items-center gap-2">
                    <Users className="w-4 h-4 text-[#D6A84B]" /> Everyday Worker Description
                  </span>
                  <span className="text-[11px] font-bold text-[#687187] bg-white px-2.5 py-0.5 rounded-full border border-[#E6DFD1]">
                    Ramesh • Tailor & Patternmaker
                  </span>
                </div>

                <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] text-xs text-[#20243A] leading-relaxed italic shadow-inner">
                  &ldquo;I have worked as a custom tailor for five years in Delhi. I operate single-needle lockstitch machines, draft bespoke blazer patterns, take precise measurements, and check seams for puckering before finishing.&rdquo;
                </div>
              </div>

              <div className="pt-2 flex items-center justify-between text-xs">
                <span className="text-[#687187]">Input: Spoken or Typed English & Hindi</span>
                <span className="text-xs font-bold text-[#27856B] flex items-center gap-1">
                  <CheckCircle2 className="w-4 h-4" /> Validated Narrative
                </span>
              </div>
            </div>

            {/* Right: AI Output Transformation */}
            <div className="rounded-3xl p-8 border border-[#D6A84B]/40 bg-gradient-to-br from-[#FFFDF8] via-[#FBF4E7] to-white space-y-4 shadow-sm">
              <div className="flex items-center justify-between">
                <span className="text-xs font-black text-[#9A7320] uppercase tracking-wider flex items-center gap-1.5">
                  <Cpu className="w-4 h-4 text-[#7355D9]" /> Standardized Vocational Mapping
                </span>
                <span className="text-xs font-bold text-[#17233F] bg-white px-2.5 py-0.5 rounded-full border border-[#D6A84B]/40">
                  NSQF Level 5 Alignment
                </span>
              </div>

              <div className="space-y-2.5 text-xs">
                <div className="p-3.5 rounded-xl bg-white border border-[#E6DFD1] flex items-center justify-between shadow-xs">
                  <div>
                    <p className="font-bold text-[#17233F]">Industrial Lockstitch Machine Operation</p>
                    <p className="text-[10px] text-[#687187]">Machinery & Tooling • 5 Years Experience</p>
                  </div>
                  <span className="text-[11px] font-black text-[#27856B] bg-[#27856B]/10 px-2 py-0.5 rounded-md">
                    Verified Competency
                  </span>
                </div>

                <div className="p-3.5 rounded-xl bg-white border border-[#E6DFD1] flex items-center justify-between shadow-xs">
                  <div>
                    <p className="font-bold text-[#17233F]">Bespoke Pattern Drafting & Marker Grading</p>
                    <p className="text-[10px] text-[#687187]">Technical Skill • Fabric yield optimization</p>
                  </div>
                  <span className="text-[11px] font-black text-[#D6A84B] bg-[#D6A84B]/15 px-2 py-0.5 rounded-md">
                    Demonstrated Know-how
                  </span>
                </div>

                <div className="p-3.5 rounded-xl bg-white border border-[#E6DFD1] flex items-center justify-between shadow-xs">
                  <div>
                    <p className="font-bold text-[#17233F]">Client Specification & Garment Fitting</p>
                    <p className="text-[10px] text-[#687187]">Transferable Skill • Client communication</p>
                  </div>
                  <span className="text-[11px] font-black text-[#7355D9] bg-[#7355D9]/10 px-2 py-0.5 rounded-md">
                    Customer Experience
                  </span>
                </div>
              </div>

              <div className="pt-2 flex justify-end">
                <Link
                  href="/experience"
                  className="text-xs font-bold text-[#17233F] hover:text-[#D6A84B] flex items-center gap-1 transition-colors"
                >
                  Test Your Own Experience in Workspace <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 6: REALISTIC BEFORE & AFTER TRANSFORMATION
         ========================================================================= */}
      <section className="py-24 relative bg-[#F5F0E6] border-t border-[#E6DFD1]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-3 mb-16">
            <span className="text-xs font-black uppercase tracking-widest text-[#27856B] bg-[#27856B]/10 border border-[#27856B]/30 px-3.5 py-1 rounded-full">
              Career Trajectory
            </span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#17233F] tracking-tight">
              The Journey to Formal Dignity & Security
            </h2>
            <p className="text-[#687187] text-sm sm:text-base leading-relaxed">
              How informal workers transition from unverified cash earnings to structured corporate employment with verifiable credentials.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
            {/* Before Card */}
            <div className="rounded-3xl p-8 border border-[#C77B54]/30 bg-white space-y-5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-[#C77B54]/15 text-[#9E5632] border border-[#C77B54]/30">
                  INFORMAL SECTOR STATUS
                </span>
                <span className="text-xs text-[#8E97AB] font-semibold">Uncertified Trade Worker</span>
              </div>
              <h3 className="text-xl font-black text-[#17233F]">Local Workshop Experience</h3>
              <ul className="space-y-3 text-xs text-[#687187]">
                <li className="flex items-start gap-2.5">
                  <span className="text-[#C77B54] font-bold">✕</span>
                  <span>Skills validated solely by neighborhood word-of-mouth</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <span className="text-[#C77B54] font-bold">✕</span>
                  <span>No digital resume; automatically filtered out by recruitment screening</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <span className="text-[#C77B54] font-bold">✕</span>
                  <span>Unaware of formal industry quality sampling standards</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <span className="text-[#C77B54] font-bold">✕</span>
                  <span>Volatile daily wages without health coverage or benefits</span>
                </li>
              </ul>
            </div>

            {/* After Card */}
            <div className="rounded-3xl p-8 border-2 border-[#D6A84B] bg-gradient-to-br from-white via-[#FFFDF8] to-[#FBF4E7] space-y-5 shadow-lg">
              <div className="flex items-center justify-between">
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]/40 shadow-xs">
                  FORMAL SECTOR PATHWAY
                </span>
                <span className="text-xs text-[#27856B] font-bold bg-[#27856B]/15 border border-[#27856B]/30 px-2.5 py-0.5 rounded-full">
                  Verified Candidate
                </span>
              </div>
              <h3 className="text-xl font-black text-[#17233F]">Recognized Trade Professional</h3>
              <ul className="space-y-3 text-xs text-[#20243A] font-medium">
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-[#27856B] shrink-0" />
                  <span>Hands-on practice mapped and validated against NSQF standards</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-[#27856B] shrink-0" />
                  <span>Pinpointed skill gaps bridged through targeted hands-on modules</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-[#27856B] shrink-0" />
                  <span>ATS-compliant resume built from genuine demonstrated abilities</span>
                </li>
                <li className="flex items-start gap-2.5">
                  <CheckCircle2 className="w-4 h-4 text-[#27856B] shrink-0" />
                  <span>Connected to vetted corporate employers with formal benefits</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 7: FINAL CTA BANNER (Royal Navy & Champagne Gold)
         ========================================================================= */}
      <section className="py-24 relative overflow-hidden bg-gradient-to-r from-[#17233F] via-[#10192D] to-[#1F2F54] text-[#F5F0E6] shadow-2xl border-t border-[#D6A84B]/25">
        <div className="absolute top-0 right-1/4 w-[400px] h-[400px] bg-[#D6A84B]/15 blur-[100px] rounded-full pointer-events-none" />

        <div className="max-w-4xl mx-auto px-4 sm:px-6 text-center space-y-6 relative z-10">
          <span className="px-4 py-1.5 rounded-full bg-[#D6A84B]/20 backdrop-blur-md text-[#F0D99B] border border-[#D6A84B]/40 text-xs font-bold uppercase tracking-wider">
            Your Next Chapter Begins Now
          </span>

          <h2 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-tight text-white">
            Your Next Opportunity Starts With What You Already Know.
          </h2>

          <p className="text-[#E6DFD1]/85 text-sm sm:text-base max-w-xl mx-auto leading-relaxed">
            Turn years of hard work into recognized credentials, verified capabilities, and formal career advancement.
          </p>

          <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/onboarding"
              className="btn-gold w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-2xl text-sm font-bold shadow-2xl hover:scale-105 transition-all"
            >
              <Sparkles className="w-4 h-4 text-[#10192D]" />
              <span>Start Your Career Journey</span>
            </Link>

            <Link
              href="/dashboard"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-2xl text-sm font-bold bg-[#17233F] hover:bg-[#1f2f54] text-[#F0D99B] border border-[#D6A84B]/35 backdrop-blur-md transition-all hover:border-[#D6A84B]"
            >
              <span>Explore Candidate Dashboard</span>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
