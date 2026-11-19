"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Logo } from "@/components/ui/Logo";
import { useAuth } from "@/context/AuthContext";
import { apiService } from "@/services/api-service";
import { toast } from "sonner";
import { Eye, EyeOff, Lock, Mail, ArrowRight, Sparkles, CheckCircle2, Shield } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("candidate@elevatex.ai");
  const [password, setPassword] = useState("Password123!");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [selectedRole, setSelectedRole] = useState<"user" | "admin">("user");
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      toast.error("Please enter both email and password.");
      return;
    }

    setIsLoading(true);
    try {
      const res = await apiService.login(email, password);
      const token = res?.data?.token?.access_token;
      if (token) {
        localStorage.setItem("elevate_auth_token", token);
      }
      login(email, selectedRole, token);
      toast.success(`Welcome back! Signed in as ${selectedRole === "admin" ? "Admin" : "Candidate"}.`);
      const searchParams = typeof window !== "undefined" ? new URLSearchParams(window.location.search) : null;
      const returnUrl = searchParams?.get("from") || (selectedRole === "admin" ? "/admin" : "/assessment");
      router.push(returnUrl);
    } catch (err: any) {
      toast.error(err.message || "Invalid email or password. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleDemo = async () => {
    setIsLoading(true);
    try {
      const res = await apiService.login("candidate@elevatex.ai", "Password123!");
      const token = res?.data?.token?.access_token;
      if (token) {
        localStorage.setItem("elevate_auth_token", token);
      }
      login("candidate@elevatex.ai", "user", token);
      toast.success("Demo candidate session authenticated with verified token.");
      const searchParams = typeof window !== "undefined" ? new URLSearchParams(window.location.search) : null;
      const returnUrl = searchParams?.get("from") || "/assessment";
      router.push(returnUrl);
    } catch {
      try {
        const reg = await apiService.register({
          email: "candidate@elevatex.ai",
          password: "Password123!",
          fullName: "Demo Candidate",
        });
        const token = reg?.data?.token?.access_token;
        if (token) {
          localStorage.setItem("elevate_auth_token", token);
        }
        login("candidate@elevatex.ai", "user", token);
        toast.success("Demo candidate session created and authenticated.");
        router.push("/assessment");
      } catch (err: any) {
        toast.error("Authentication error: " + err.message);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A] flex flex-col lg:flex-row">
      {/* LEFT SIDE (Desktop): Royal Navy & Gold Branding Column */}
      <div className="lg:w-1/2 bg-[#10192D] text-[#F5F0E6] p-8 sm:p-12 lg:p-16 flex flex-col justify-between relative overflow-hidden border-b lg:border-b-0 lg:border-r border-[#D6A84B]/20">
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#7355D9]/20 blur-3xl rounded-full pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-[#D6A84B]/10 blur-3xl rounded-full pointer-events-none" />

        <div className="relative z-10">
          <Logo size="lg" lightText={true} />
        </div>

        <div className="relative z-10 my-12 space-y-6 max-w-lg">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#17233F] border border-[#D6A84B]/40 text-xs font-bold text-[#F0D99B]">
            <Sparkles className="w-3.5 h-3.5 text-[#D6A84B]" />
            <span>Vocational AI Career Gateway</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight leading-tight">
            Empowering Trade Talent with Recognized Dignity.
          </h2>

          <p className="text-sm sm:text-base text-[#E6DFD1]/80 leading-relaxed font-normal">
            Translate practical craftsmanship, tooling know-how, and years of tactile mastery into verified corporate opportunities.
          </p>

          <div className="pt-2 space-y-3">
            <div className="flex items-center gap-3 text-xs text-[#E6DFD1]">
              <CheckCircle2 className="w-4 h-4 text-[#D6A84B] shrink-0" />
              <span>NSQF-aligned vocational taxonomy recognition</span>
            </div>
            <div className="flex items-center gap-3 text-xs text-[#E6DFD1]">
              <CheckCircle2 className="w-4 h-4 text-[#7355D9] shrink-0" />
              <span>Adaptive diagnostic skill verifications</span>
            </div>
            <div className="flex items-center gap-3 text-xs text-[#E6DFD1]">
              <CheckCircle2 className="w-4 h-4 text-[#27856B] shrink-0" />
              <span>ATS-compliant resume generator for export careers</span>
            </div>
          </div>
        </div>

        <div className="relative z-10 pt-4 border-t border-white/10 flex items-center justify-between text-xs text-[#8E97AB]">
          <span>© 2026 ELEVATE X AI</span>
          <span className="flex items-center gap-1.5 text-[#F0D99B]">
            <Shield className="w-3.5 h-3.5 text-[#D6A84B]" />
            <span>Enterprise Security</span>
          </span>
        </div>
      </div>

      {/* RIGHT SIDE: Warm Ivory Authentication Form */}
      <div className="lg:w-1/2 flex items-center justify-center p-6 sm:p-12 lg:p-16 bg-[#FBF8F1]">
        <div className="w-full max-w-md space-y-6">
          <div className="space-y-1.5 text-left">
            <h1 className="text-2xl sm:text-3xl font-black text-[#17233F] tracking-tight">
              Sign In to Your Account
            </h1>
            <p className="text-xs sm:text-sm text-[#687187]">
              Enter your credentials to access your candidate workspace
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 sm:p-8 border border-[#E6DFD1] shadow-xl space-y-5">
            {/* Role Toggle Selector */}
            <div className="p-1 rounded-2xl bg-[#F5F0E6] border border-[#E6DFD1] flex items-center text-xs">
              <button
                type="button"
                onClick={() => setSelectedRole("user")}
                className={`flex-1 py-2 rounded-xl font-bold transition-all ${
                  selectedRole === "user"
                    ? "bg-[#17233F] text-[#F0D99B] shadow-sm"
                    : "text-[#687187] hover:text-[#17233F]"
                }`}
              >
                Candidate Portal
              </button>
              <button
                type="button"
                onClick={() => setSelectedRole("admin")}
                className={`flex-1 py-2 rounded-xl font-bold transition-all ${
                  selectedRole === "admin"
                    ? "bg-[#17233F] text-[#F0D99B] shadow-sm"
                    : "text-[#687187] hover:text-[#17233F]"
                }`}
              >
                Admin Gateway
              </button>
            </div>

            <form onSubmit={handleLogin} className="space-y-4">
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

              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-bold text-[#17233F]">Password</label>
                  <Link
                    href="/forgot-password"
                    className="text-xs font-semibold text-[#7355D9] hover:underline"
                  >
                    Forgot password?
                  </Link>
                </div>
                <div className="relative">
                  <Lock className="w-4 h-4 text-[#8E97AB] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password"
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
              </div>

              <div className="flex items-center justify-between pt-1">
                <label className="flex items-center gap-2 cursor-pointer text-xs text-[#687187]">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="rounded text-[#D6A84B] focus:ring-[#D6A84B] accent-[#D6A84B]"
                  />
                  <span>Remember my workstation</span>
                </label>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn-violet w-full py-3 rounded-xl text-xs font-bold flex items-center justify-center gap-2 shadow-lg shadow-[#7355D9]/25 hover:scale-[1.02] transition-all cursor-pointer"
              >
                <span>{isLoading ? "Authenticating..." : "Sign In to Workspace"}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>

            <div className="relative flex items-center justify-center pt-2">
              <div className="border-t border-[#E6DFD1] w-full" />
              <span className="bg-white px-3 text-[11px] font-semibold text-[#8E97AB] uppercase absolute">
                Or Instant Demo
              </span>
            </div>

            <button
              type="button"
              onClick={handleGoogleDemo}
              disabled={isLoading}
              className="w-full py-2.5 rounded-xl border border-[#E6DFD1] bg-white hover:bg-[#F5F0E6] text-xs font-bold text-[#17233F] flex items-center justify-center gap-2 transition-all shadow-xs cursor-pointer"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.67v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.16z"
                />
                <path
                  fill="#34A853"
                  d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.34 24 12 24z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 10.03 0 12s.45 3.82 1.25 5.42l4.03-3.15z"
                />
                <path
                  fill="#EA4335"
                  d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.34 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"
                />
              </svg>
              <span>Continue with Demo Profile</span>
            </button>
          </div>

          <div className="text-center text-xs text-[#687187]">
            <span>Don&apos;t have an account yet? </span>
            <Link href="/signup" className="font-bold text-[#17233F] hover:text-[#D6A84B] underline">
              Create an account
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
