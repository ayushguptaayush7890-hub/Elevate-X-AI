"use client";

import React from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/AppShell";
import { GlassCard } from "@/components/ui/GlassCard";
import { StatCard } from "@/components/ui/StatCard";
import { ProgressBar, CircularProgress } from "@/components/ui/ProgressBar";
import { useAuth } from "@/context/AuthContext";
import { mockJobListings, mockSkillGaps, mockRoadmapMilestones } from "@/data/mock-data";
import {
  Sparkles,
  Award,
  Briefcase,
  GitCompare,
  TrendingUp,
  ArrowRight,
  CheckCircle2,
  Clock,
  ExternalLink,
  Target
} from "lucide-react";
import {
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  AreaChart,
  Area
} from "recharts";

export default function DashboardPage() {
  const { user } = useAuth();

  const skillGrowthData = [
    { month: "Jun", skills: 2, score: 70 },
    { month: "Jul", skills: 3, score: 76 },
    { month: "Aug", skills: 4, score: 81 },
    { month: "Sep", skills: 5, score: 85 },
    { month: "Oct", skills: 5, score: 89 },
    { month: "Nov", skills: 6, score: 92 },
  ];

  return (
    <AppShell>
      {/* Welcome Hero Banner: Royal Navy & Champagne Gold */}
      <div className="relative rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-[#17233F] via-[#10192D] to-[#1F2F54] text-[#F5F0E6] overflow-hidden shadow-xl border border-[#D6A84B]/25">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-[#D6A84B]/10 to-transparent pointer-events-none" />
        <div className="absolute -top-10 -right-10 w-48 h-48 bg-[#7355D9]/20 blur-3xl rounded-full pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#D6A84B]/20 backdrop-blur-md text-[#F0D99B] border border-[#D6A84B]/40 text-xs font-bold">
              <Sparkles className="w-3.5 h-3.5 text-[#D6A84B]" /> Candidate Readiness Profile
            </div>
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
              Welcome back, {user.fullName}
            </h1>
            <p className="text-xs sm:text-sm text-[#E6DFD1]/85 max-w-xl leading-relaxed">
              Continue your vocational advancement pathway. You have verified trade skills and active matching corporate openings.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/experience"
              className="btn-gold inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold shadow-md hover:scale-105 transition-all"
            >
              <Sparkles className="w-4 h-4 text-[#10192D]" />
              <span>Recognize New Skills</span>
            </Link>
            <Link
              href="/assessment"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold bg-[#17233F] hover:bg-[#10192D] text-[#F0D99B] border border-[#D6A84B]/35 transition-all"
            >
              <Award className="w-4 h-4 text-[#D6A84B]" />
              <span>Take Diagnostic</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Summary KPI Cards in Royal Gold Style */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Profile Completeness"
          value={`${user.profileCompleteness}%`}
          subtitle="Candidate profile active"
          icon={<CheckCircle2 className="w-5 h-5 text-[#27856B]" />}
          trend={{ value: "+8%", isPositive: true }}
          glow="sage"
        />
        <StatCard
          title="Skills Identified"
          value="6 Skills"
          subtitle="Demonstrated in practice"
          icon={<Sparkles className="w-5 h-5 text-[#7355D9]" />}
          trend={{ value: "+2 new", isPositive: true }}
          glow="violet"
        />
        <StatCard
          title="Assessments Passed"
          value="2 Diagnostics"
          subtitle="Verified trade know-how"
          icon={<Award className="w-5 h-5 text-[#D6A84B]" />}
          trend={{ value: "Validated", isPositive: true }}
          glow="gold"
        />
        <StatCard
          title="Curated Job Matches"
          value={`${mockJobListings.length} Active`}
          subtitle="Aligned with your abilities"
          icon={<Briefcase className="w-5 h-5 text-[#3478F6]" />}
          trend={{ value: "High demand", isPositive: true }}
          glow="blue"
        />
      </div>

      {/* Two Column Section: Readiness Gauge & Skill Growth Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Career Readiness Gauge Card */}
        <GlassCard padding="lg" className="space-y-5 bg-white border border-[#E6DFD1]">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-black text-[#17233F] flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-[#D6A84B]" /> Vocational Readiness
            </h3>
            <span className="text-[10px] text-[#27856B] bg-[#27856B]/15 font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider border border-[#27856B]/30">
              Formal Sector
            </span>
          </div>

          <div className="py-2 flex justify-center">
            <CircularProgress
              value={88}
              size={120}
              strokeWidth={10}
              label="Qualified"
              subtitle="Target: Apparel QA Specialist"
            />
          </div>

          <div className="space-y-2 pt-2 border-t border-[#E6DFD1] text-xs">
            <div className="flex justify-between text-[#20243A]">
              <span>Lockstitch Machine Operation:</span>
              <span className="font-bold text-[#27856B]">Demonstrated</span>
            </div>
            <div className="flex justify-between text-[#20243A]">
              <span>Pattern Drafting & Grading:</span>
              <span className="font-bold text-[#27856B]">Demonstrated</span>
            </div>
            <div className="flex justify-between text-[#20243A]">
              <span>AQL 2.5 Sampling Bridge:</span>
              <span className="font-bold text-[#D6A84B]">In Progress</span>
            </div>
          </div>

          <Link
            href="/roadmap"
            className="w-full btn-gold py-2 rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 shadow-sm"
          >
            <span>View Career Roadmap</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </GlassCard>

        {/* Skill Growth Diagnostic Curve */}
        <GlassCard padding="lg" className="lg:col-span-2 space-y-4 bg-white border border-[#E6DFD1]">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-black text-[#17233F]">Skill Growth & Diagnostic Curve</h3>
              <p className="text-xs text-[#687187]">Progressive diagnostic score over the last 6 months</p>
            </div>
            <span className="text-[11px] font-bold text-[#27856B] bg-[#27856B]/10 px-2.5 py-1 rounded-full border border-[#27856B]/25">
              +22% Overall Growth
            </span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={skillGrowthData}>
                <defs>
                  <linearGradient id="goldGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#D6A84B" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#D6A84B" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#E6DFD1" vertical={false} />
                <XAxis dataKey="month" stroke="#8E97AB" fontSize={11} tickLine={false} />
                <YAxis stroke="#8E97AB" fontSize={11} domain={[50, 100]} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#17233F",
                    borderRadius: "12px",
                    border: "1px solid #D6A84B",
                    color: "#F5F0E6",
                    fontSize: "11px",
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="score"
                  stroke="#D6A84B"
                  strokeWidth={3}
                  fillOpacity={1}
                  fill="url(#goldGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>

      {/* Two Column Bottom Modules: Curated Matches & Priority Skill Gaps */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Curated Opportunities */}
        <GlassCard padding="lg" className="space-y-4 bg-white border border-[#E6DFD1]">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-black text-[#17233F] flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-[#D6A84B]" /> Top Matched Opportunities
            </h3>
            <Link href="/jobs" className="text-xs font-bold text-[#7355D9] hover:underline flex items-center gap-1">
              View all ({mockJobListings.length}) <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="space-y-3">
            {mockJobListings.slice(0, 3).map((job) => (
              <div
                key={job.id}
                className="p-3.5 rounded-2xl bg-[#FBF8F1] border border-[#E6DFD1] hover:border-[#D6A84B] transition-all flex items-center justify-between"
              >
                <div>
                  <h4 className="text-xs font-bold text-[#17233F]">{job.title}</h4>
                  <p className="text-[11px] text-[#687187]">{job.company} • {job.location}</p>
                  <p className="text-[11px] font-black text-[#27856B] mt-0.5">{job.salaryRange}</p>
                </div>
                <div className="text-right space-y-1">
                  <span className="text-[10px] font-black px-2 py-0.5 rounded-full bg-[#D6A84B]/15 text-[#9A7320] border border-[#D6A84B]/40">
                    High Compatibility
                  </span>
                  <Link
                    href={`/jobs/${job.id}`}
                    className="block text-[11px] font-bold text-[#7355D9] hover:underline"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        {/* Priority Skill Gaps to Bridge */}
        <GlassCard padding="lg" className="space-y-4 bg-white border border-[#E6DFD1]">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-black text-[#17233F] flex items-center gap-2">
              <GitCompare className="w-4 h-4 text-[#C77B54]" /> Priority Skill Gaps to Bridge
            </h3>
            <Link href="/skill-gap" className="text-xs font-bold text-[#7355D9] hover:underline flex items-center gap-1">
              Full Analyzer <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="space-y-3">
            {mockSkillGaps.slice(0, 3).map((gap) => (
              <div
                key={gap.id}
                className="p-3.5 rounded-2xl bg-[#FBF8F1] border border-[#E6DFD1] hover:border-[#C77B54] transition-all space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-[#17233F]">{gap.skillName}</span>
                  <span
                    className={`text-[9px] font-extrabold uppercase px-2 py-0.5 rounded-full ${
                      gap.importance === "High"
                        ? "bg-[#C77B54]/15 text-[#9E5632] border border-[#C77B54]/30"
                        : "bg-[#D6A84B]/15 text-[#9A7320]"
                    }`}
                  >
                    {gap.importance} Priority
                  </span>
                </div>
                <p className="text-[11px] text-[#687187] leading-relaxed">
                  {gap.learningRecommendation}
                </p>
                <div className="flex items-center justify-between pt-1 text-[11px]">
                  <span className="text-[#8E97AB]">{gap.recommendedResource.title}</span>
                  <Link
                    href="/roadmap"
                    className="font-bold text-[#7355D9] hover:underline flex items-center gap-1"
                  >
                    Bridge Gap <ArrowRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </AppShell>
  );
}
