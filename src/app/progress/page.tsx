"use client";

import React from "react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { StatCard } from "@/components/ui/StatCard";
import {
  BarChart3,
  Award,
  Sparkles,
  CheckCircle2,
  Clock,
  Briefcase,
  FileText,
  TrendingUp,
  ShieldCheck
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

export default function ProgressPage() {
  const weeklyHours = [
    { day: "Mon", hours: 1.5 },
    { day: "Tue", hours: 2.0 },
    { day: "Wed", hours: 3.5 },
    { day: "Thu", hours: 2.0 },
    { day: "Fri", hours: 4.0 },
    { day: "Sat", hours: 5.0 },
    { day: "Sun", hours: 3.0 },
  ];

  const milestonesHistory = [
    {
      id: "act-1",
      title: "Passed Industrial Sewing Diagnostics",
      desc: "Earned verified score badge (92/100).",
      time: "2 days ago",
      icon: <Award className="w-4 h-4 text-[#27856B]" />,
    },
    {
      id: "act-2",
      title: "Applied to Raymond Lifestyle Exports",
      desc: "Application submitted for QA Specialist with verified portfolio.",
      time: "3 days ago",
      icon: <Briefcase className="w-4 h-4 text-[#17233F]" />,
    },
    {
      id: "act-3",
      title: "Generated ATS Resume v2.4",
      desc: "Summary updated with verified action keywords.",
      time: "5 days ago",
      icon: <FileText className="w-4 h-4 text-[#7355D9]" />,
    },
    {
      id: "act-4",
      title: "Completed Stage 1 Roadmap",
      desc: "Garment Defect Taxonomy masterclass finished.",
      time: "1 week ago",
      icon: <CheckCircle2 className="w-4 h-4 text-[#D6A84B]" />,
    },
  ];

  return (
    <AppShell>
      <div className="space-y-6">
        <PageHeader
          badge="Career Analytics & Telemetry"
          title="Career Progress & Learning Analytics"
          description="Track verified skill development, practical study hours logged, diagnostic assessment trajectories, and vocational milestone achievements."
          variant="navy"
          actions={
            <div className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40">
              <ShieldCheck className="w-4 h-4 text-[#D6A84B]" />
              <span>Verified Trajectory</span>
            </div>
          }
        />

        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard
            title="Skills Acquired"
            value="6 Skills"
            subtitle="4 verified via diagnostics"
            icon={<Sparkles className="w-5 h-5 text-[#D6A84B]" />}
            trend={{ value: "+2 this month", isPositive: true }}
            glow="gold"
          />
          <StatCard
            title="Learning Hours Logged"
            value="21.0 Hrs"
            subtitle="Interactive modules"
            icon={<Clock className="w-5 h-5 text-[#17233F]" />}
            trend={{ value: "+6.5 hrs vs last wk", isPositive: true }}
            glow="subtle"
          />
          <StatCard
            title="Roadmap Completed"
            value="25%"
            subtitle="Stage 2 in progress"
            icon={<TrendingUp className="w-5 h-5 text-[#27856B]" />}
            trend={{ value: "On schedule", isPositive: true }}
            glow="sage"
          />
          <StatCard
            title="Active Applications"
            value="4 Positions"
            subtitle="1 Interview Scheduled"
            icon={<Briefcase className="w-5 h-5 text-[#7355D9]" />}
            trend={{ value: "High compatibility", isPositive: true }}
            glow="violet"
          />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Weekly Learning Hours Chart */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-[#17233F]">Weekly Learning Dedication</h3>
              <span className="text-xs text-[#17233F] font-bold bg-[#F0D99B]/40 px-2.5 py-1 rounded-full border border-[#D6A84B]">
                21 hrs total this week
              </span>
            </div>

            <div className="h-64 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={weeklyHours}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E6DFD1" vertical={false} />
                  <XAxis dataKey="day" stroke="#687187" fontSize={11} tickLine={false} />
                  <YAxis stroke="#687187" fontSize={11} tickLine={false} axisLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#17233F",
                      borderColor: "#D6A84B",
                      borderRadius: "12px",
                      color: "#F5F0E6",
                      fontSize: "12px",
                      boxShadow: "0 4px 12px rgba(16, 25, 45, 0.2)",
                    }}
                  />
                  <Bar dataKey="hours" fill="#D6A84B" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Activity Timeline */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <h3 className="text-base font-bold text-[#17233F]">Vocational Milestone Timeline</h3>

            <div className="space-y-3">
              {milestonesHistory.map((act) => (
                <div
                  key={act.id}
                  className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] flex items-start gap-3 hover:border-[#D6A84B]/60 transition-all"
                >
                  <div className="p-2.5 rounded-xl bg-white shadow-xs border border-[#E6DFD1] shrink-0 mt-0.5">
                    {act.icon}
                  </div>
                  <div className="flex-1 space-y-0.5">
                    <div className="flex items-center justify-between">
                      <p className="text-xs sm:text-sm font-bold text-[#17233F]">{act.title}</p>
                      <span className="text-[10px] text-[#687187] font-medium">{act.time}</span>
                    </div>
                    <p className="text-xs text-[#687187]">{act.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
