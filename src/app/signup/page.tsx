"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Logo } from "@/components/ui/Logo";
import { useAuth } from "@/context/AuthContext";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import { User, Mail, Phone, Lock, Eye, EyeOff, Globe, ArrowRight, Sparkles, CheckCircle2 } from "lucide-react";

export default function SignupPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [preferredLanguage, setPreferredLanguage] = useState<"English" | "Hindi">("English");
  const [termsAccepted, setTermsAccepted] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  const { login, updateUser } = useAuth();
  const router = useRouter();

  const getPasswordStrength = (pwd: string) => {
    let score = 0;
    if (pwd.length >= 8) score++;
    if (/[A-Z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^A-Za-z0-9]/.test(pwd)) score++;
    return score;
  };

  const strength = getPasswordStrength(password);
  const strengthLabels = ["Very Weak", "Weak", "Fair", "Good", "Strong"];
  const strengthColors = ["bg-rose-500", "bg-amber-500", "bg-yellow-500", "bg-[#3478F6]", "bg-[#27856B]"];

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fullName || !email || !password) {
      toast.error("Please fill in all required fields.");
      return;
    }

    if (password !== confirmPassword) {
      toast.error("Passwords do not match.");
      return;
    }

    if (!termsAccepted) {
      toast.error("Please accept the terms to proceed.");
      return;
    }

    setIsLoading(true);
    try {
      const res = await apiService.register({
        email,
        password,
        fullName,
        phone,
      });
      const token = res?.data?.token?.access_token;
      if (token) {
        localStorage.setItem("elevate_auth_token", token);
      }
      login(email, "user", token);
      updateUser({
        fullName,
        phone,
        preferredLanguage,
      });
      toast.success("Account created successfully! Starting onboarding.");
      router.push("/assessment");
    } catch (err: any) {
      toast.error(err.message || "Registration failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A] flex flex-col lg:flex-row">
      {/* LEFT SIDE: Royal Navy & Champagne Gold Branding */}
      <div className="lg:w-1/2 bg-[#10192D] text-[#F5F0E6] p-8 sm:p-12 lg:p-16 flex flex-col justify-between relative overflow-hidden border-b lg:border-b-0 lg:border-r border-[#D6A84B]/20">
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#7355D9]/20 blur-3xl rounded-full pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-[#D6A84B]/10 blur-3xl rounded-full pointer-events-none" />

        <div className="relative z-10">
          <Logo size="lg" lightText={true} />
        </div>

        <div className="relative z-10 my-12 space-y-6 max-w-lg">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#17233F] border border-[#D6A84B]/40 text-xs font-bold text-[#F0D99B]">
            <Sparkles className="w-3.5 h-3.5 text-[#D6A84B]" />
            <span>Join 10,000+ Trade Professionals</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight leading-tight">
            Turn What You Know Into Recognized Credentials.
          </h2>

          <p className="text-sm sm:text-base text-[#E6DFD1]/80 leading-relaxed">
            Create your candidate profile in under 2 minutes. Map your vocational abilities to formal career roadmaps with AI assistance.
          </p>

          <div className="pt-2 space-y-3">
            <div className="flex items-center gap-3 text-xs text-[#E6DFD1]">
              <CheckCircle2 className="w-4 h-4 text-[#D6A84B]" />
              <span>Voice & text experience transcription in Hindi and English</span>
            </div>
            <div className="flex items-center gap-3 text-xs text-[#E6DFD1]">
              <CheckCircle2 className="w-4 h-4 text-[#7355D9]" />
              <span>Personalized skill gap diagnosis and free micro-learning</span>
            </div>
            <div className="flex items-center gap-3 text-xs text-[#E6DFD1]">
              <CheckCircle2 className="w-4 h-4 text-[#27856B]" />
              <span>Corporate ATS export resume ready for formal job applications</span>
            </div>
          </div>
        </div>

        <div className="relative z-10 pt-4 border-t border-white/10 flex items-center justify-between text-xs text-[#8E97AB]">
          <span>© 2026 ELEVATE X AI</span>
          <span className="text-[#F0D99B]">Data Protection Guarantee</span>
        </div>
      </div>

      {/* RIGHT SIDE: Warm Ivory Registration Form */}
      <div className="lg:w-1/2 flex items-center justify-center p-6 sm:p-12 lg:p-16 bg-[#FBF8F1]">
        <div className="w-full max-w-md space-y-6">
          <div className="space-y-1.5 text-left">
            <h1 className="text-2xl sm:text-3xl font-black text-[#17233F] tracking-tight">
              Create Candidate Account
            </h1>
            <p className="text-xs sm:text-sm text-[#687187]">
              Start your career recognition pathway today
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 sm:p-8 border border-[#E6DFD1] shadow-xl space-y-4">
            <form onSubmit={handleSignup} className="space-y-3.5">
              <div className="space-y-1">
                <label className="text-xs font-bold text-[#17233F]">Full Name</label>
                <div className="relative">
                  <User className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g. Ramesh Sharma"
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl pl-10 pr-4 py-2.5 text-xs text-[#20243A] placeholder:text-[#8E97AB] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-[#17233F]">Email Address</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="ramesh@example.com"
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl pl-10 pr-4 py-2.5 text-xs text-[#20243A] placeholder:text-[#8E97AB] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-[#17233F]">Mobile Number</label>
                  <div className="relative">
                    <Phone className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="tel"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+91 98765 43210"
                      className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl pl-10 pr-3 py-2.5 text-xs text-[#20243A] placeholder:text-[#8E97AB] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-[#17233F]">Preferred Language</label>
                  <div className="relative">
                    <Globe className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <select
                      value={preferredLanguage}
                      onChange={(e) => setPreferredLanguage(e.target.value as "English" | "Hindi")}
                      className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl pl-10 pr-3 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all appearance-none cursor-pointer"
                    >
                      <option value="English">English</option>
                      <option value="Hindi">हिन्दी (Hindi)</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-[#17233F]">Create Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Minimum 8 characters"
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl pl-10 pr-10 py-2.5 text-xs text-[#20243A] placeholder:text-[#8E97AB] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#8E97AB] hover:text-[#17233F]"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {password && (
                  <div className="pt-1 space-y-1">
                    <div className="flex gap-1 h-1">
                      {[0, 1, 2, 3].map((step) => (
                        <div
                          key={step}
                          className={`flex-1 rounded-full ${
                            strength > step ? strengthColors[strength] : "bg-slate-200"
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-[10px] text-[#687187]">
                      Security: <strong className="text-[#17233F]">{strengthLabels[strength]}</strong>
                    </span>
                  </div>
                )}
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-[#17233F]">Confirm Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter password"
                    className="w-full bg-[#F5F0E6] border border-[#E6DFD1] rounded-xl pl-10 pr-4 py-2.5 text-xs text-[#20243A] placeholder:text-[#8E97AB] focus:outline-none focus:border-[#D6A84B] focus:bg-white transition-all"
                  />
                </div>
              </div>

              <div className="pt-1">
                <label className="flex items-start gap-2 cursor-pointer text-xs text-[#687187]">
                  <input
                    type="checkbox"
                    checked={termsAccepted}
                    onChange={(e) => setTermsAccepted(e.target.checked)}
                    className="rounded text-[#D6A84B] focus:ring-[#D6A84B] accent-[#D6A84B] mt-0.5"
                  />
                  <span>
                    I consent to vocational skill verification and agree to the platform guidelines.
                  </span>
                </label>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn-violet w-full py-3 rounded-xl text-xs font-bold flex items-center justify-center gap-2 shadow-lg shadow-[#7355D9]/25 hover:scale-[1.02] transition-all cursor-pointer"
              >
                <span>{isLoading ? "Creating Profile..." : "Create Account & Start Journey"}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          </div>

          <div className="text-center text-xs text-[#687187]">
            <span>Already have an account? </span>
            <Link href="/login" className="font-bold text-[#17233F] hover:text-[#D6A84B] underline">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
