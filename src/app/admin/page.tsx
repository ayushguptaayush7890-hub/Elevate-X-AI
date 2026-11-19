"use client";

import React from "react";
import Link from "next/link";
import { AdminShell } from "@/components/layout/AdminShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { StatCard } from "@/components/ui/StatCard";
import { mockAdminStats } from "@/data/mock-data";
import {
  Users,
  Award,
  Briefcase,
  Terminal,
  Activity,
  Layers,
  Sparkles,
  ArrowRight,
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
  CartesianGrid,
  AreaChart,
  Area
} from "recharts";

export default function AdminOverviewPage() {
  return (
    <AdminShell>
      <div className="space-y-6">
        {/* Top Banner */}
        <PageHeader
          badge="Superadmin Control Plane"
          title="Elevate X AI Platform Overview"
          description="System health telemetry, AI model extraction benchmarks, candidate skill evaluations, and employer hiring activities."
          variant="navy"
          actions={
            <Link
              href="/admin/prompts"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold text-[#10192D] bg-[#D6A84B] hover:bg-[#F0D99B] shadow-md transition-all"
            >
              <Terminal className="w-4 h-4 text-[#10192D]" /> Open Prompt Lab
            </Link>
          }
        />

        {/* KPI Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="Total Registered Workers"
            value={mockAdminStats.totalRegisteredUsers.toLocaleString()}
            subtitle="Informal & vocational talent"
            icon={<Users className="w-5 h-5 text-[#17233F]" />}
            trend={{ value: "+14% MoM", isPositive: true }}
            glow="subtle"
          />
          <StatCard
            title="Active Monthly Users"
            value={mockAdminStats.activeMonthlyUsers.toLocaleString()}
            subtitle="69% Retention Rate"
            icon={<Activity className="w-5 h-5 text-[#7355D9]" />}
            trend={{ value: "+8%", isPositive: true }}
            glow="violet"
          />
          <StatCard
            title="Assessments Passed"
            value={mockAdminStats.assessmentsCompleted.toLocaleString()}
            subtitle="Verifiable skill badges issued"
            icon={<Award className="w-5 h-5 text-[#27856B]" />}
            trend={{ value: "+21%", isPositive: true }}
            glow="sage"
          />
          <StatCard
            title="Curated Job Listings"
            value={mockAdminStats.curatedJobListings.toLocaleString()}
            subtitle="Verified export & retail partners"
            icon={<Briefcase className="w-5 h-5 text-[#D6A84B]" />}
            trend={{ value: "100% active", isPositive: true }}
            glow="gold"
          />
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Daily Platform Activity Area Chart */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-[#17233F]">Daily Platform Invocations & Skill Extractions</h3>
              <span className="text-xs text-[#7355D9] font-mono font-bold bg-[#FBF8F1] px-2.5 py-1 rounded-md border border-[#E6DFD1]">
                Realtime Pipeline
              </span>
            </div>

            <div className="h-64 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={mockAdminStats.dailyPlatformActivity}>
                  <defs>
                    <linearGradient id="queryGradGold" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#D6A84B" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#D6A84B" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E6DFD1" />
                  <XAxis dataKey="day" stroke="#687187" fontSize={11} />
                  <YAxis stroke="#687187" fontSize={11} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#17233F",
                      borderColor: "#D6A84B",
                      borderRadius: "12px",
                      color: "#F5F0E6",
                      fontSize: "12px",
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="queries"
                    stroke="#D6A84B"
                    strokeWidth={2.5}
                    fillOpacity={1}
                    fill="url(#queryGradGold)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Assessment Completion by Day */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-[#17233F]">Assessment Volume by Day</h3>
              <span className="text-xs text-[#27856B] font-mono font-bold bg-[#DCEAE6] px-2.5 py-1 rounded-md border border-[#27856B]/30">
                92% Average Pass Rate
              </span>
            </div>

            <div className="h-64 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={mockAdminStats.dailyPlatformActivity}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E6DFD1" />
                  <XAxis dataKey="day" stroke="#687187" fontSize={11} />
                  <YAxis stroke="#687187" fontSize={11} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#17233F",
                      borderColor: "#27856B",
                      borderRadius: "12px",
                      color: "#F5F0E6",
                      fontSize: "12px",
                    }}
                  />
                  <Bar dataKey="assessments" fill="#17233F" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Navigation Shortcuts to Admin Modules */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Link href="/admin/users" className="group">
            <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] hover:border-[#D6A84B] space-y-2 transition-all shadow-xs">
              <div className="flex items-center justify-between">
                <Users className="w-5 h-5 text-[#17233F]" />
                <ArrowRight className="w-4 h-4 text-[#687187] group-hover:translate-x-1 transition-transform" />
              </div>
              <h4 className="text-xs font-bold text-[#17233F]">User Management</h4>
              <p className="text-[11px] text-[#687187]">Search 14,280+ worker and recruiter profiles</p>
            </div>
          </Link>

          <Link href="/admin/prompts" className="group">
            <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] hover:border-[#D6A84B] space-y-2 transition-all shadow-xs">
              <div className="flex items-center justify-between">
                <Terminal className="w-5 h-5 text-[#7355D9]" />
                <ArrowRight className="w-4 h-4 text-[#687187] group-hover:translate-x-1 transition-transform" />
              </div>
              <h4 className="text-xs font-bold text-[#17233F]">Prompt Engineering Lab</h4>
              <p className="text-[11px] text-[#687187]">Evaluate prompt techniques with radar & factuality benchmarks</p>
            </div>
          </Link>

          <Link href="/admin/skills" className="group">
            <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] hover:border-[#D6A84B] space-y-2 transition-all shadow-xs">
              <div className="flex items-center justify-between">
                <Layers className="w-5 h-5 text-[#D6A84B]" />
                <ArrowRight className="w-4 h-4 text-[#687187] group-hover:translate-x-1 transition-transform" />
              </div>
              <h4 className="text-xs font-bold text-[#17233F]">Skill Taxonomy</h4>
              <p className="text-[11px] text-[#687187]">Manage vocational trade categories and standard NSQF mappings</p>
            </div>
          </Link>
        </div>
      </div>
    </AdminShell>
  );
}
