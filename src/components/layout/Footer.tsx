"use client";

import React from "react";
import Link from "next/link";
import { Logo } from "@/components/ui/Logo";
import { ShieldCheck, Sparkles, ArrowUpRight, Globe, Share2, MessageCircle } from "lucide-react";

export function Footer() {
  const currentYear = 2026;

  return (
    <footer className="bg-[#10192D] border-t border-[#D6A84B]/20 text-[#E6DFD1] text-sm relative overflow-hidden">
      {/* Background ambient gold/violet glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-28 bg-[#D6A84B]/5 blur-[100px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10">
          {/* Brand Info */}
          <div className="lg:col-span-2 space-y-4">
            <Logo size="md" lightText={true} />
            <p className="text-[#8E97AB] text-xs sm:text-sm max-w-sm leading-relaxed">
              Elevate X AI transforms informal work experience into structured, verified skills. Bridging non-traditional talent with formal, high-growth career opportunities through adaptive AI.
            </p>
            <div className="flex items-center gap-2.5 pt-2 text-[#E6DFD1]">
              <a
                href="#"
                className="p-2.5 rounded-xl bg-[#17233F] border border-[#D6A84B]/20 hover:text-[#F0D99B] hover:border-[#D6A84B]/50 transition-colors shadow-xs"
                aria-label="Global Community"
              >
                <Globe className="w-4 h-4 text-[#36D6E8]" />
              </a>
              <a
                href="#"
                className="p-2.5 rounded-xl bg-[#17233F] border border-[#D6A84B]/20 hover:text-[#F0D99B] hover:border-[#D6A84B]/50 transition-colors shadow-xs"
                aria-label="Social Network"
              >
                <Share2 className="w-4 h-4 text-[#D6A84B]" />
              </a>
              <a
                href="#"
                className="p-2.5 rounded-xl bg-[#17233F] border border-[#D6A84B]/20 hover:text-[#F0D99B] hover:border-[#D6A84B]/50 transition-colors shadow-xs"
                aria-label="Discussions"
              >
                <MessageCircle className="w-4 h-4 text-[#7355D9]" />
              </a>
            </div>
            <div className="pt-2 flex items-center gap-2 text-xs text-[#8E97AB] font-semibold">
              <ShieldCheck className="w-4 h-4 text-[#27856B]" />
              <span>Ethical AI & Data Privacy Guarantee</span>
            </div>
          </div>

          {/* Quick Links: Platform */}
          <div className="space-y-3">
            <p className="text-xs font-black uppercase tracking-wider text-[#F0D99B]">Platform Modules</p>
            <ul className="space-y-2 text-xs text-[#8E97AB]">
              <li>
                <Link href="/experience" className="hover:text-[#F0D99B] transition-colors">
                  Experience Recognition
                </Link>
              </li>
              <li>
                <Link href="/assessment" className="hover:text-[#F0D99B] transition-colors">
                  Adaptive AI Assessment
                </Link>
              </li>
              <li>
                <Link href="/jobs" className="hover:text-[#F0D99B] transition-colors">
                  Smart Job Discovery
                </Link>
              </li>
              <li>
                <Link href="/skill-gap" className="hover:text-[#F0D99B] transition-colors">
                  Skill Gap Analyzer
                </Link>
              </li>
              <li>
                <Link href="/resume" className="hover:text-[#F0D99B] transition-colors">
                  AI Resume Studio
                </Link>
              </li>
              <li>
                <Link href="/roadmap" className="hover:text-[#F0D99B] transition-colors">
                  Personalized Roadmap
                </Link>
              </li>
            </ul>
          </div>

          {/* Quick Links: Career Tools */}
          <div className="space-y-3">
            <p className="text-xs font-black uppercase tracking-wider text-[#F0D99B]">Career Tools</p>
            <ul className="space-y-2 text-xs text-[#8E97AB]">
              <li>
                <Link href="/career-transition" className="hover:text-[#F0D99B] transition-colors">
                  Career Transition Pathways
                </Link>
              </li>
              <li>
                <Link href="/interview" className="hover:text-[#F0D99B] transition-colors">
                  AI Mock Interview Lab
                </Link>
              </li>
              <li>
                <Link href="/assistant" className="hover:text-[#F0D99B] transition-colors">
                  Multilingual AI Assistant
                </Link>
              </li>
              <li>
                <Link href="/applications" className="hover:text-[#F0D99B] transition-colors">
                  Application Kanban Tracker
                </Link>
              </li>
              <li>
                <Link href="/progress" className="hover:text-[#F0D99B] transition-colors">
                  Progress Tracker
                </Link>
              </li>
            </ul>
          </div>

          {/* Quick Links: Company */}
          <div className="space-y-3">
            <p className="text-xs font-black uppercase tracking-wider text-[#F0D99B]">Company & Admin</p>
            <ul className="space-y-2 text-xs text-[#8E97AB]">
              <li>
                <Link href="/about" className="hover:text-[#F0D99B] transition-colors">
                  Our Mission & Story
                </Link>
              </li>
              <li>
                <Link href="/contact" className="hover:text-[#F0D99B] transition-colors">
                  Contact & Support
                </Link>
              </li>
              <li>
                <span className="text-[#687187] cursor-not-allowed">
                  Privacy Policy
                </span>
              </li>
              <li>
                <span className="text-[#687187] cursor-not-allowed">
                  Terms of Service
                </span>
              </li>
              <li>
                <Link href="/admin" className="text-[#D6A84B] hover:text-[#F0D99B] transition-colors flex items-center gap-1 font-bold">
                  <Sparkles className="w-3.5 h-3.5" /> Admin Portal
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Disclaimer */}
        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-[#8E97AB]">
          <p>© {currentYear} ELEVATE X AI Inc. All rights reserved.</p>
          <p className="text-center md:text-right max-w-xl">
            Notice: Compatibility scores and skill assessments are indicative platform benchmarks intended for vocational career planning, not official trade licensing or employment guarantees.
          </p>
        </div>
      </div>
    </footer>
  );
}
