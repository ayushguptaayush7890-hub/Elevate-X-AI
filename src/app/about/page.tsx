"use client";

import React from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { BrandButton } from "@/components/ui/BrandButton";
import {
  Sparkles,
  ShieldCheck,
  Target,
  Award,
  Globe2,
  Users2,
  Building2,
  CheckCircle2,
  Compass
} from "lucide-react";

export default function AboutPage() {
  const pillars = [
    {
      title: "Recognizing Real-World Mastery",
      description: "Over 60% of the global workforce operates in informal trades. Years of hands-on fabrication, precision machinery operation, and on-site problem-solving represent deep practical rigor that traditional resumes often fail to capture.",
      icon: <Sparkles className="w-5 h-5 text-[#D6A84B]" />,
    },
    {
      title: "Scenario-Driven Diagnostics",
      description: "Instead of abstract academic tests, our adaptive skill assessments evaluate actual tactile knowledge, machine calibrations, and workplace decision-making benchmarked against formal industrial requirements.",
      icon: <Award className="w-5 h-5 text-[#27856B]" />,
    },
    {
      title: "Ethical & Explainable AI",
      description: "Our career matching algorithms provide transparent, explainable compatibility benchmarks without arbitrary rejections. We strictly distinguish verified assessments from self-reported claims.",
      icon: <ShieldCheck className="w-5 h-5 text-[#7355D9]" />,
    },
  ];

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A]">
      <Navbar />

      {/* Hero Header Banner */}
      <section className="pt-32 pb-20 bg-gradient-to-b from-[#10192D] via-[#17233F] to-[#10192D] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-4">
          <span className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-widest text-[#F0D99B] px-3.5 py-1 rounded-full bg-[#10192D] border border-[#D6A84B]/40">
            <Compass className="w-3.5 h-3.5 text-[#D6A84B]" />
            Our Mission & Purpose
          </span>
          <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight max-w-3xl mx-auto">
            Bridging Informal Talent with Dignified Formal Careers
          </h1>
          <p className="text-[#F5F0E6]/80 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
            Elevate X AI solves a profound vocational gap: while industrial and commercial enterprises face acute shortages of experienced craftspeople, millions of artisans remain trapped in precarious, under-recognized informal work.
          </p>
        </div>
      </section>

      <main className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-20">
        {/* Pillars Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {pillars.map((pillar, i) => (
            <div
              key={i}
              className="p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm hover:border-[#D6A84B]/60 hover:shadow-md transition-all space-y-4"
            >
              <div className="p-3 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] w-fit">
                {pillar.icon}
              </div>
              <h3 className="text-lg font-bold text-[#17233F]">{pillar.title}</h3>
              <p className="text-xs sm:text-sm text-[#687187] leading-relaxed">{pillar.description}</p>
            </div>
          ))}
        </div>

        {/* Global Landscape Statistics */}
        <div className="p-8 sm:p-12 rounded-3xl bg-[#17233F] text-white border border-[#D6A84B]/30 shadow-xl">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-[#D6A84B]/20">
            <div className="space-y-1.5">
              <p className="text-3xl sm:text-4xl font-extrabold text-[#F0D99B]">2 Billion+</p>
              <p className="text-sm font-bold text-white">Global Informal Workers</p>
              <p className="text-xs text-[#F5F0E6]/70">The world&apos;s largest underserved talent backbone (ILO data)</p>
            </div>
            <div className="space-y-1.5 pt-6 md:pt-0">
              <p className="text-3xl sm:text-4xl font-extrabold text-[#D6A84B]">Zero Cost</p>
              <p className="text-sm font-bold text-white">Skill Verification for Candidates</p>
              <p className="text-xs text-[#F5F0E6]/70">Democratizing career advancement and credentialing</p>
            </div>
            <div className="space-y-1.5 pt-6 md:pt-0">
              <p className="text-3xl sm:text-4xl font-extrabold text-[#27856B]">100% Explainable</p>
              <p className="text-sm font-bold text-white">Objective Match Criteria</p>
              <p className="text-xs text-[#F5F0E6]/70">Transparent gap diagnostics without black-box rejections</p>
            </div>
          </div>
        </div>

        {/* Call to action */}
        <div className="text-center max-w-xl mx-auto space-y-5 pt-6">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#17233F]">
            Ready to Translate Your Experience?
          </h2>
          <p className="text-xs sm:text-sm text-[#687187]">
            Whether you are a craftsperson seeking formal verification or an employer searching for verified trade talent, Elevate X AI is engineered for you.
          </p>
          <div className="flex justify-center gap-3">
            <BrandButton href="/onboarding" variant="gold" size="md">
              Start Free Skill Assessment
            </BrandButton>
            <BrandButton href="/contact" variant="navy" size="md">
              Partner With Us
            </BrandButton>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
