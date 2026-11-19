"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { PageHeader } from "@/components/ui/PageHeader";
import { mockInterviewQuestions, mockInterviewSessions } from "@/data/mock-data";
import { InterviewQuestion } from "@/types";
import { toast } from "sonner";
import {
  Mic,
  MicOff,
  Bot,
  Play,
  CheckCircle2,
  ArrowRight,
  Send,
  Sparkles,
  ShieldCheck,
  RotateCcw
} from "lucide-react";

export default function InterviewLabPage() {
  const [interviewState, setInterviewState] = useState<"setup" | "room" | "feedback">("setup");
  const [selectedRole, setSelectedRole] = useState("Apparel Quality Assurance Specialist");
  const [interviewType, setInterviewType] = useState<"Technical" | "Situational" | "HR Behavioral">("Technical");
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswerText, setUserAnswerText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const questions: InterviewQuestion[] = mockInterviewQuestions;
  const currentQ = questions[currentQuestionIndex];

  const handleStartInterview = () => {
    setCurrentQuestionIndex(0);
    setUserAnswerText("");
    setInterviewState("room");
    toast.success(`AI Interview Room started for ${selectedRole}`);
  };

  const handleVoiceToggle = () => {
    if (!isRecording) {
      setIsRecording(true);
      toast.info("Microphone active... speak your answer clearly.");
      setTimeout(() => {
        setIsRecording(false);
        setUserAnswerText(currentQ.sampleAnswer.slice(0, 240) + "...");
        toast.success("Voice transcript captured.");
      }, 4000);
    } else {
      setIsRecording(false);
    }
  };

  const handleSubmitAnswer = () => {
    if (!userAnswerText.trim()) {
      toast.error("Please speak or type your answer before submitting.");
      return;
    }

    setIsEvaluating(true);
    setTimeout(() => {
      setIsEvaluating(false);
      setInterviewState("feedback");
      toast.success("AI Interviewer has analyzed your response!");
    }, 900);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setUserAnswerText("");
      setInterviewState("room");
    } else {
      toast.success("Full mock interview session completed!");
      setInterviewState("setup");
    }
  };

  return (
    <AppShell>
      {/* 1. Setup Screen */}
      {interviewState === "setup" && (
        <div className="space-y-6">
          <PageHeader
            badge="AI Interview Simulator"
            title="AI Mock Interview Preparation Lab"
            description="Practice trade-specific, technical, and client de-escalation interview scenarios with an empathetic AI mentor. Receive structured phrasing feedback and industry-benchmark model answers."
            variant="navy"
            actions={
              <div className="flex items-center gap-2 text-xs text-[#F0D99B] bg-[#10192D] px-3.5 py-2 rounded-xl border border-[#D6A84B]/40">
                <ShieldCheck className="w-4 h-4 text-[#D6A84B]" />
                <span>Calibrated to Formal Standards</span>
              </div>
            }
          />

          <div className="p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-5 max-w-2xl">
            <h2 className="text-base font-bold text-[#17233F]">Configure Your Practice Simulation</h2>

            <div className="space-y-4 text-xs">
              <div className="space-y-1.5">
                <label className="text-[#687187] font-semibold">Target Job Role</label>
                <select
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value)}
                  className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3.5 py-2.5 text-xs sm:text-sm text-[#20243A] font-medium focus:outline-none focus:border-[#D6A84B]"
                >
                  <option value="Apparel Quality Assurance Specialist">Apparel Quality Assurance Specialist (Raymond Lifestyle)</option>
                  <option value="Production Assistant - Garment Sampling">Production Assistant - Garment Sampling (FabIndia)</option>
                  <option value="Bespoke Master Tailor & Alteration Lead">Bespoke Master Tailor & Alteration Lead</option>
                  <option value="Technical Sewing Instructor">Technical Sewing Instructor (Vocational Skilling)</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-[#687187] font-semibold">Interview Focus Module</label>
                <div className="grid grid-cols-3 gap-2">
                  {(["Technical", "Situational", "HR Behavioral"] as const).map((type) => (
                    <button
                      key={type}
                      type="button"
                      onClick={() => setInterviewType(type)}
                      className={`py-2 px-3 rounded-xl border text-center transition-all ${
                        interviewType === type
                          ? "bg-[#17233F] border-[#D6A84B] text-[#F0D99B] font-bold shadow-sm"
                          : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-2">
              <BrandButton
                variant="gold"
                size="md"
                fullWidth
                onClick={handleStartInterview}
              >
                <Play className="w-4 h-4 mr-2" />
                <span>Enter AI Interview Simulation Room</span>
              </BrandButton>
            </div>
          </div>

          {/* Past Sessions History */}
          <div className="space-y-3 pt-4">
            <h3 className="text-xs font-bold text-[#687187] uppercase tracking-wider">
              Previous Practice Sessions
            </h3>
            {mockInterviewSessions.map((session) => (
              <div
                key={session.id}
                className="p-5 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm flex items-center justify-between hover:border-[#D6A84B]/60 transition-all"
              >
                <div>
                  <h4 className="text-sm font-bold text-[#17233F]">{session.targetJob}</h4>
                  <p className="text-xs text-[#687187] mt-0.5">
                    Date: {session.date} • Relevance: <strong className="text-[#7355D9]">{session.relevanceScore}%</strong> • Communication: <strong className="text-[#17233F]">{session.communicationScore}%</strong>
                  </p>
                </div>
                <span className="text-xs font-extrabold px-3 py-1 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]">
                  {session.overallScore}% Overall Score
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. Active Interview Room */}
      {interviewState === "room" && currentQ && (
        <div className="max-w-3xl mx-auto space-y-6">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#687187]">
              Question {currentQuestionIndex + 1} of {questions.length} • {currentQ.category}
            </span>
            <button
              onClick={() => setInterviewState("setup")}
              className="text-xs font-semibold text-[#687187] hover:text-[#C77B54] transition-colors"
            >
              Exit Interview
            </button>
          </div>

          {/* AI Interviewer Avatar & Question Box */}
          <div className="p-6 sm:p-8 rounded-2xl bg-[#17233F] text-white border border-[#D6A84B]/30 shadow-xl space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-[#10192D] border border-[#D6A84B]/40 flex items-center justify-center text-[#D6A84B] shadow-md">
                <Bot className="w-7 h-7 text-[#D6A84B]" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-[#F0D99B]">Elena — AI Senior Technical Recruiter</h3>
                <p className="text-xs text-[#F5F0E6]/80">Raymond Lifestyle Apparel Assessment Panel</p>
              </div>
            </div>

            <div className="p-5 rounded-2xl bg-[#10192D] border border-[#D6A84B]/20 text-sm sm:text-base text-[#F5F0E6] font-medium leading-relaxed">
              &ldquo;{currentQ.question}&rdquo;
            </div>
          </div>

          {/* Candidate Answer Workspace */}
          <div className="p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-[#17233F]">Your Response:</span>
              <button
                type="button"
                onClick={handleVoiceToggle}
                className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                  isRecording
                    ? "bg-[#C77B54] text-white animate-pulse"
                    : "bg-[#FBF8F1] border border-[#E6DFD1] text-[#20243A] hover:text-[#17233F]"
                }`}
              >
                {isRecording ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5 text-[#7355D9]" />}
                <span>{isRecording ? "Listening..." : "Speak Answer"}</span>
              </button>
            </div>

            <textarea
              rows={5}
              value={userAnswerText}
              onChange={(e) => setUserAnswerText(e.target.value)}
              placeholder="Speak via the microphone or type your response detailing your practical shop-floor steps..."
              className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-2xl p-4 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B] leading-relaxed resize-none"
            />

            <div className="flex justify-end pt-2">
              <BrandButton
                variant="gold"
                onClick={handleSubmitAnswer}
                disabled={isEvaluating}
                size="md"
              >
                <Send className="w-4 h-4 mr-1.5" />
                <span>{isEvaluating ? "Elena is Analyzing..." : "Submit Answer for Feedback"}</span>
              </BrandButton>
            </div>
          </div>
        </div>
      )}

      {/* 3. Question Feedback Screen */}
      {interviewState === "feedback" && currentQ && (
        <div className="max-w-3xl mx-auto space-y-6">
          <div className="p-6 sm:p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-md space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-[#27856B]" />
                <h2 className="text-base font-bold text-[#17233F]">Interview Response Evaluation</h2>
              </div>
              <span className="text-xs font-extrabold px-3 py-1 rounded-full bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]">
                Score: 89/100
              </span>
            </div>

            <div className="p-4 rounded-xl bg-[#FBF8F1] border border-[#E6DFD1] text-xs text-[#20243A] space-y-1">
              <span className="text-[10px] font-bold text-[#687187] uppercase tracking-wider">Target Question:</span>
              <p className="font-semibold text-[#17233F]">{currentQ.question}</p>
            </div>
          </div>

          {/* Breakdown: Strengths vs Polish */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-5 rounded-2xl bg-white border border-[#27856B]/30 shadow-sm space-y-2">
              <h3 className="text-xs font-bold text-[#27856B] uppercase tracking-wider">Strong Technical Points</h3>
              <ul className="space-y-1.5 text-xs text-[#20243A]">
                <li className="flex items-start gap-1.5">
                  <span className="text-[#27856B] font-bold">✓</span> Demonstrated hands-on physical testing method.
                </li>
                <li className="flex items-start gap-1.5">
                  <span className="text-[#27856B] font-bold">✓</span> Correct technical vocabulary for seam balance.
                </li>
              </ul>
            </div>

            <div className="p-5 rounded-2xl bg-white border border-[#D6A84B]/40 shadow-sm space-y-2">
              <h3 className="text-xs font-bold text-[#17233F] uppercase tracking-wider">Suggested Phrasing Polish</h3>
              <ul className="space-y-1.5 text-xs text-[#20243A]">
                <li className="flex items-start gap-1.5">
                  <span className="text-[#C77B54] font-bold">●</span> Cite numeric export tolerances (e.g. 1/16th inch tolerance).
                </li>
              </ul>
            </div>
          </div>

          {/* High-Impact Sample Model Answer */}
          <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-2">
            <h3 className="text-xs font-bold text-[#17233F] uppercase tracking-wider">Benchmark Exemplary Answer</h3>
            <p className="text-xs sm:text-sm text-[#20243A] leading-relaxed italic bg-[#FBF8F1] p-4 rounded-xl border border-[#E6DFD1]">
              &ldquo;{currentQ.sampleAnswer}&rdquo;
            </p>
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <BrandButton
              variant="violet"
              onClick={handleNextQuestion}
              size="md"
            >
              <span>{currentQuestionIndex === questions.length - 1 ? "Complete Interview Session" : "Next Question"}</span>
              <ArrowRight className="w-4 h-4 ml-1.5" />
            </BrandButton>
          </div>
        </div>
      )}
    </AppShell>
  );
}
