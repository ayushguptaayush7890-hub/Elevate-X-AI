"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Logo } from "@/components/ui/Logo";
import { toast } from "sonner";
import { Mail, ArrowLeft, CheckCircle2, Shield, Sparkles } from "lucide-react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [isSent, setIsSent] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      toast.error("Please enter your registered email address.");
      return;
    }

    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      setIsSent(true);
      toast.success("Password recovery link dispatched.");
    }, 600);
  };

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A] flex flex-col lg:flex-row">
      {/* LEFT SIDE: Royal Navy & Gold Branding */}
      <div className="lg:w-1/2 bg-[#10192D] text-[#F5F0E6] p-8 sm:p-12 lg:p-16 flex flex-col justify-between relative overflow-hidden border-b lg:border-b-0 lg:border-r border-[#D6A84B]/20">
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#7355D9]/20 blur-3xl rounded-full pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-[#D6A84B]/10 blur-3xl rounded-full pointer-events-none" />

        <div className="relative z-10">
          <Logo size="lg" lightText={true} />
        </div>

        <div className="relative z-10 my-12 space-y-6 max-w-lg">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#17233F] border border-[#D6A84B]/40 text-xs font-bold text-[#F0D99B]">
            <Sparkles className="w-3.5 h-3.5 text-[#D6A84B]" />
            <span>Secure Account Recovery</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight leading-tight">
            Regain Immediate Access to Your Career Credentials.
          </h2>

          <p className="text-sm sm:text-base text-[#E6DFD1]/80 leading-relaxed">
            Your verified competencies, diagnostic scores, and saved job applications remain protected and ready for retrieval.
          </p>
        </div>

        <div className="relative z-10 pt-4 border-t border-white/10 flex items-center justify-between text-xs text-[#8E97AB]">
          <span>© 2026 ELEVATE X AI</span>
          <span className="text-[#F0D99B]">Zero-Knowledge Protection</span>
        </div>
      </div>

      {/* RIGHT SIDE: Warm Ivory Form */}
      <div className="lg:w-1/2 flex items-center justify-center p-6 sm:p-12 lg:p-16 bg-[#FBF8F1]">
        <div className="w-full max-w-md space-y-6">
          <div className="space-y-1.5 text-left">
            <h1 className="text-2xl sm:text-3xl font-black text-[#17233F] tracking-tight">
              Reset Your Password
            </h1>
            <p className="text-xs sm:text-sm text-[#687187]">
              Enter your account email to receive verification instructions
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 sm:p-8 border border-[#E6DFD1] shadow-xl space-y-5">
            {isSent ? (
              <div className="text-center space-y-4 py-4">
                <div className="w-14 h-14 rounded-full bg-[#27856B]/15 border border-[#27856B]/30 text-[#27856B] flex items-center justify-center mx-auto shadow-inner">
                  <CheckCircle2 className="w-7 h-7" />
                </div>
                <h3 className="text-base font-bold text-[#17233F]">Recovery Link Sent</h3>
                <p className="text-xs sm:text-sm text-[#687187] leading-relaxed">
                  If an account exists for <span className="font-bold text-[#17233F]">{email}</span>, you will receive password reset instructions shortly.
                </p>
                <Link
                  href="/login"
                  className="btn-gold inline-flex items-center justify-center w-full py-3 rounded-xl text-xs font-bold"
                >
                  Return to Sign In
                </Link>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-[#17233F]">Email Address</label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="you@example.com"
                      className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl pl-10 pr-4 py-2.5 text-xs text-[#20243A] placeholder:text-[#8E97AB] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="btn-violet w-full py-3 rounded-xl text-xs font-bold flex items-center justify-center gap-2 shadow-lg shadow-[#7355D9]/25 hover:scale-[1.02] transition-all cursor-pointer"
                >
                  <span>{isLoading ? "Dispatching..." : "Send Password Reset Link"}</span>
                </button>
              </form>
            )}

            <div className="pt-2 text-center">
              <Link
                href="/login"
                className="inline-flex items-center gap-1.5 text-xs font-bold text-[#17233F] hover:text-[#D6A84B] transition-colors"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Back to Sign In</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
