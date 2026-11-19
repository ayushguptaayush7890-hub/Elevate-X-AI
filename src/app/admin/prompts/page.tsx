"use client";

import React, { useState } from "react";
import { AdminShell } from "@/components/layout/AdminShell";
import { PageHeader } from "@/components/ui/PageHeader";
import { BrandButton } from "@/components/ui/BrandButton";
import { mockPromptEvaluations } from "@/data/mock-data";
import { PromptEvaluationItem, PromptTechnique } from "@/types";
import { toast } from "sonner";
import {
  Terminal,
  Sparkles,
  Play,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  ShieldAlert,
  Code,
  Layers,
  Zap,
  BarChart2
} from "lucide-react";
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  Tooltip
} from "recharts";

export default function PromptEngineeringModulePage() {
  const [selectedPromptId, setSelectedPromptId] = useState(mockPromptEvaluations[0].id);
  const [isRunningEval, setIsRunningEval] = useState(false);

  const activePrompt: PromptEvaluationItem =
    mockPromptEvaluations.find((p) => p.id === selectedPromptId) || mockPromptEvaluations[0];

  const techniques: PromptTechnique[] = [
    "Zero-Shot",
    "Few-Shot",
    "Role-Based",
    "Structured JSON",
    "Multi-Step",
    "Context-Aware",
    "RAG-Grounded",
    "Guardrail",
    "Adaptive",
  ];

  // Radar chart data comparing Baseline vs Improved Prompt
  const radarComparisonData = [
    {
      subject: "Extraction Accuracy",
      Baseline: activePrompt.baselineMetrics.extractionAccuracy,
      Improved: activePrompt.metrics.extractionAccuracy,
      fullMark: 100,
    },
    {
      subject: "Evidence Validation",
      Baseline: activePrompt.baselineMetrics.evidenceValidation,
      Improved: activePrompt.metrics.evidenceValidation,
      fullMark: 100,
    },
    {
      subject: "Job Relevance",
      Baseline: activePrompt.baselineMetrics.jobRelevance,
      Improved: activePrompt.metrics.jobRelevance,
      fullMark: 100,
    },
    {
      subject: "Factuality Guardrail",
      Baseline: activePrompt.baselineMetrics.factuality,
      Improved: activePrompt.metrics.factuality,
      fullMark: 100,
    },
    {
      subject: "JSON Syntax Validity",
      Baseline: activePrompt.baselineMetrics.jsonValidity,
      Improved: activePrompt.metrics.jsonValidity,
      fullMark: 100,
    },
  ];

  const handleRunEvaluation = () => {
    setIsRunningEval(true);
    setTimeout(() => {
      setIsRunningEval(false);
      toast.success(
        `Benchmark evaluated across 50 informal trade test cases. Improved prompt scored ${activePrompt.metrics.factuality}% Factuality!`
      );
    }, 700);
  };

  return (
    <AdminShell>
      <div className="space-y-6">
        {/* Top Header */}
        <PageHeader
          badge="Prompt Engineering Benchmarking Studio"
          title="Prompt Engineering & Model Evaluation Lab"
          description="Evaluate 9 specialized prompt techniques against informal workforce colloquialisms, factuality guardrails, and structured JSON extraction benchmarks."
          variant="navy"
          actions={
            <BrandButton
              variant="gold"
              onClick={handleRunEvaluation}
              disabled={isRunningEval}
              size="md"
            >
              <Play className="w-4 h-4 mr-1.5" />
              <span>{isRunningEval ? "Running Test Suite..." : "Run Test Benchmark"}</span>
            </BrandButton>
          }
        />

        {/* 9 Prompt Techniques Pills */}
        <div className="p-4 rounded-2xl bg-white border border-[#E6DFD1] shadow-xs space-y-2">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[#687187] block px-1">
            Specialized Prompt Engineering Paradigms:
          </span>
          <div className="flex flex-wrap gap-1.5">
            {techniques.map((tech) => (
              <span
                key={tech}
                className={`text-xs px-3 py-1 rounded-xl font-medium border transition-colors ${
                  activePrompt.technique === tech
                    ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] shadow-xs font-bold"
                    : "bg-[#FBF8F1] text-[#20243A] border-[#E6DFD1]"
                }`}
              >
                {tech}
              </span>
            ))}
          </div>
        </div>

        {/* Selector & Prompt Metadata */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-5 rounded-2xl bg-white border border-[#E6DFD1] space-y-2 md:col-span-1 shadow-xs">
            <label className="text-xs font-bold text-[#17233F] uppercase">Select Production Prompt</label>
            <select
              value={selectedPromptId}
              onChange={(e) => setSelectedPromptId(e.target.value)}
              className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3 py-2 text-xs sm:text-sm text-[#20243A] font-semibold focus:outline-none focus:border-[#D6A84B]"
            >
              {mockPromptEvaluations.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.version})
                </option>
              ))}
            </select>
            <div className="pt-2 text-xs text-[#687187] space-y-1">
              <p>Category: <strong className="text-[#17233F]">{activePrompt.category}</strong></p>
              <p>Technique: <strong className="text-[#7355D9]">{activePrompt.technique}</strong></p>
              <p>Status: <strong className="text-[#27856B]">{activePrompt.status}</strong></p>
            </div>
          </div>

          {/* Benchmark Metric Highlights */}
          <div className="md:col-span-2 grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div className="p-4 rounded-2xl bg-white border border-[#E6DFD1] text-center space-y-1 shadow-xs">
              <p className="text-[10px] text-[#687187] uppercase font-semibold">Extraction Accuracy</p>
              <p className="text-2xl font-black text-[#17233F]">{activePrompt.metrics.extractionAccuracy}%</p>
              <p className="text-[10px] text-[#27856B] font-bold">
                +{activePrompt.metrics.extractionAccuracy - activePrompt.baselineMetrics.extractionAccuracy}% vs Baseline
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-white border border-[#E6DFD1] text-center space-y-1 shadow-xs">
              <p className="text-[10px] text-[#687187] uppercase font-semibold">Factuality Score</p>
              <p className="text-2xl font-black text-[#27856B]">{activePrompt.metrics.factuality}%</p>
              <p className="text-[10px] text-[#27856B] font-bold">0% Hallucination</p>
            </div>

            <div className="p-4 rounded-2xl bg-white border border-[#E6DFD1] text-center space-y-1 col-span-2 sm:col-span-1 shadow-xs">
              <p className="text-[10px] text-[#687187] uppercase font-semibold">Latency (ms)</p>
              <p className="text-2xl font-black text-[#7355D9]">{activePrompt.metrics.latencyMs}ms</p>
              <p className="text-[10px] text-[#687187] font-mono">FastAPI Calibrated</p>
            </div>
          </div>
        </div>

        {/* Radar Chart: Baseline vs Improved Prompt Performance */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-6 p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-[#17233F] flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-[#D6A84B]" /> Multi-Dimensional Evaluation Radar
              </h3>
              <span className="text-xs text-[#687187] font-mono">N = 50 Test Cases</span>
            </div>

            <div className="h-72 w-full pt-2">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarComparisonData}>
                  <PolarGrid stroke="#E6DFD1" />
                  <PolarAngleAxis dataKey="subject" stroke="#687187" fontSize={10} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#E6DFD1" fontSize={9} />
                  <Radar
                    name="Baseline Prompt"
                    dataKey="Baseline"
                    stroke="#C77B54"
                    fill="#C77B54"
                    fillOpacity={0.2}
                  />
                  <Radar
                    name="Improved Prompt"
                    dataKey="Improved"
                    stroke="#D6A84B"
                    fill="#D6A84B"
                    fillOpacity={0.4}
                  />
                  <Legend
                    wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#17233F",
                      borderColor: "#D6A84B",
                      borderRadius: "12px",
                      color: "#F5F0E6",
                      fontSize: "12px",
                    }}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* System Prompt View & Test Case */}
          <div className="lg:col-span-6 p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-xs space-y-4">
            <div className="space-y-1.5">
              <span className="text-xs font-bold text-[#17233F] uppercase tracking-wider">
                System Prompt & Guardrails ({activePrompt.technique})
              </span>
              <div className="p-4 rounded-xl bg-[#10192D] border border-[#D6A84B]/30 text-xs font-mono text-[#F0D99B] max-h-36 overflow-y-auto leading-relaxed">
                {activePrompt.systemPrompt}
              </div>
            </div>

            <div className="space-y-1.5">
              <span className="text-xs font-bold text-[#17233F] uppercase tracking-wider">
                Colloquial Test Narrative (Informal Worker Input)
              </span>
              <div className="p-3.5 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-xs text-[#20243A] italic">
                {activePrompt.testInput}
              </div>
            </div>
          </div>
        </div>

        {/* Direct Comparison: Baseline vs Improved Output */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="p-6 rounded-2xl bg-white border border-[#C77B54]/30 shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-[#C77B54]/10 text-[#C77B54] border border-[#C77B54]/30">
                Baseline Zero-Shot Prompt Output
              </span>
              <span className="text-xs text-[#C77B54] font-mono font-bold">Accuracy: {activePrompt.baselineMetrics.extractionAccuracy}%</span>
            </div>
            <pre className="p-4 rounded-xl bg-[#10192D] border border-slate-700 text-xs text-[#F5F0E6] font-mono whitespace-pre-wrap overflow-x-auto leading-relaxed">
              {activePrompt.baselineOutput}
            </pre>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-[#D6A84B] shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]">
                Improved {activePrompt.technique} Prompt Output
              </span>
              <span className="text-xs text-[#17233F] font-mono font-bold">Accuracy: {activePrompt.metrics.extractionAccuracy}%</span>
            </div>
            <pre className="p-4 rounded-xl bg-[#10192D] border border-[#D6A84B]/40 text-xs text-[#F0D99B] font-mono whitespace-pre-wrap overflow-x-auto leading-relaxed">
              {activePrompt.improvedOutput}
            </pre>
          </div>
        </div>
      </div>
    </AdminShell>
  );
}
