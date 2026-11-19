"use client";

import React from "react";
import { AdminShell } from "@/components/layout/AdminShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { StatCard } from "@/components/ui/StatCard";
import { Activity, Cpu, Zap, Globe2, ShieldCheck, Server } from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

export default function AdminAnalyticsPage() {
  const telemetryTimeline = [
    { time: "00:00", latency: 280, tokens: 4200 },
    { time: "04:00", latency: 260, tokens: 2100 },
    { time: "08:00", latency: 340, tokens: 8400 },
    { time: "12:00", latency: 390, tokens: 14200 },
    { time: "16:00", latency: 360, tokens: 16800 },
    { time: "20:00", latency: 310, tokens: 11200 },
    { time: "23:59", latency: 290, tokens: 6500 },
  ];

  return (
    <AdminShell>
      <div className="space-y-6">
        <PageHeader
          badge="AI Engine Telemetry"
          title="System Telemetry & Model Analytics"
          description="Realtime monitoring of token throughput, inference latencies, prompt accuracy regressions, and edge gateway status."
          variant="navy"
          actions={
            <div className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40">
              <Server className="w-4 h-4 text-[#D6A84B]" />
              <span>Gateway 99.98% SLA</span>
            </div>
          }
        />

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard
            title="Average Inference Latency"
            value="315 ms"
            subtitle="FastAPI + vLLM backend"
            icon={<Zap className="w-5 h-5 text-[#D6A84B]" />}
            trend={{ value: "-45ms", isPositive: true }}
            glow="gold"
          />
          <StatCard
            title="Daily Token Consumption"
            value="1.84M"
            subtitle="9 Prompt pipelines active"
            icon={<Cpu className="w-5 h-5 text-[#7355D9]" />}
            trend={{ value: "+12%", isPositive: true }}
            glow="violet"
          />
          <StatCard
            title="API Uptime (30 Days)"
            value="99.98%"
            subtitle="0 Critical Incidents"
            icon={<Server className="w-5 h-5 text-[#27856B]" />}
            trend={{ value: "Stable", isPositive: true }}
            glow="sage"
          />
          <StatCard
            title="JSON Syntax Pass Rate"
            value="100.0%"
            subtitle="Guardrail verified"
            icon={<ShieldCheck className="w-5 h-5 text-[#17233F]" />}
            trend={{ value: "Zero parse errors", isPositive: true }}
            glow="subtle"
          />
        </div>

        <div className="p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-[#17233F]">24-Hour Inference Latency Distribution (Milliseconds)</h3>
            <span className="text-xs text-[#17233F] font-mono font-bold bg-[#F0D99B]/40 px-3 py-1 rounded-full border border-[#D6A84B]">
              P95 SLA &lt; 450ms
            </span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={telemetryTimeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E6DFD1" />
                <XAxis dataKey="time" stroke="#687187" fontSize={11} />
                <YAxis stroke="#687187" fontSize={11} domain={[200, 500]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#17233F",
                    borderColor: "#D6A84B",
                    borderRadius: "12px",
                    color: "#F5F0E6",
                    fontSize: "12px",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="latency"
                  stroke="#D6A84B"
                  strokeWidth={3}
                  dot={{ r: 4, fill: "#17233F", stroke: "#D6A84B", strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </AdminShell>
  );
}
