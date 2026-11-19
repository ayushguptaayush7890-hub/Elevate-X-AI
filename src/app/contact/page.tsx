"use client";

import React, { useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { BrandButton } from "@/components/ui/BrandButton";
import { toast } from "sonner";
import { Mail, Phone, MapPin, Send, MessageSquare, Building2, CheckCircle2, ShieldCheck } from "lucide-react";

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "Candidate Support",
    message: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setTimeout(() => {
      setIsSubmitting(false);
      toast.success("Message sent successfully! Our vocational team will respond within 24 hours.");
      setFormData({ name: "", email: "", subject: "Candidate Support", message: "" });
    }, 800);
  };

  return (
    <div className="min-h-screen bg-[#FBF8F1] text-[#20243A]">
      <Navbar />

      {/* Header Banner */}
      <section className="pt-32 pb-20 bg-gradient-to-b from-[#10192D] via-[#17233F] to-[#10192D] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-3">
          <span className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-widest text-[#F0D99B] px-3.5 py-1 rounded-full bg-[#10192D] border border-[#D6A84B]/40">
            <Mail className="w-3.5 h-3.5 text-[#D6A84B]" />
            Connect With Our Team
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            We&apos;re Here to Support Your Career Journey
          </h1>
          <p className="text-[#F5F0E6]/80 text-sm max-w-xl mx-auto leading-relaxed">
            Have questions regarding skill validation, employer hiring integrations, or vocational institutional partnerships?
          </p>
        </div>
      </section>

      <main className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Contact Details */}
          <div className="space-y-4">
            <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
              <div className="p-2.5 rounded-xl bg-[#F5F0E6] text-[#17233F] border border-[#E6DFD1] w-fit">
                <Mail className="w-5 h-5 text-[#D6A84B]" />
              </div>
              <h3 className="text-sm font-bold text-[#17233F]">Email Inquiries</h3>
              <p className="text-xs text-[#687187]">Candidate Guidance:</p>
              <p className="text-xs font-semibold text-[#17233F]">support@elevatex-ai.org</p>
              <p className="text-xs text-[#687187] pt-1">Employer Partnerships:</p>
              <p className="text-xs font-semibold text-[#7355D9]">partnerships@elevatex-ai.org</p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
              <div className="p-2.5 rounded-xl bg-[#F5F0E6] text-[#7355D9] border border-[#E6DFD1] w-fit">
                <Phone className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-[#17233F]">Career Helpline</h3>
              <p className="text-xs text-[#687187]">Toll-free vocational hotline:</p>
              <p className="text-xs font-semibold text-[#17233F]">1800-ELEVATE-AI (Mon - Sat, 9am - 7pm IST)</p>
            </div>

            <div className="p-6 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-3">
              <div className="p-2.5 rounded-xl bg-[#DCEAE6] text-[#27856B] border border-[#27856B]/30 w-fit">
                <MapPin className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold text-[#17233F]">Innovation Center</h3>
              <p className="text-xs text-[#687187] leading-relaxed">
                Elevate X AI Skilling Foundation <br />
                Technology Tower, Okhla Phase III, <br />
                New Delhi, 110020, India
              </p>
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-2">
            <div className="p-8 rounded-2xl bg-white border border-[#E6DFD1] shadow-sm space-y-6">
              <h3 className="text-lg font-bold text-[#17233F] flex items-center gap-2">
                <MessageSquare className="w-5 h-5 text-[#D6A84B]" /> Send Us a Message
              </h3>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-[#687187]">Full Name</label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      placeholder="e.g. Ramesh Sharma"
                      className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3.5 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-[#687187]">Email Address</label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      placeholder="you@example.com"
                      className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3.5 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-[#687187]">Inquiry Subject</label>
                  <select
                    value={formData.subject}
                    onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3.5 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
                  >
                    <option value="Candidate Support">Candidate Support & Assessment Help</option>
                    <option value="Employer Partnerships">Employer & Export House Recruitment</option>
                    <option value="Vocational Skilling">Vocational Skilling Institute Partner</option>
                    <option value="API / Technical">Technical & API Inquiries</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-[#687187]">Message</label>
                  <textarea
                    rows={5}
                    required
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    placeholder="Describe your inquiry or how we can assist..."
                    className="w-full bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-3.5 py-2.5 text-xs text-[#20243A] focus:outline-none focus:border-[#D6A84B] resize-none"
                  />
                </div>

                <div className="pt-2">
                  <BrandButton
                    type="submit"
                    variant="gold"
                    size="md"
                    fullWidth
                    disabled={isSubmitting}
                  >
                    <Send className="w-4 h-4 mr-1.5" />
                    <span>{isSubmitting ? "Sending..." : "Submit Message"}</span>
                  </BrandButton>
                </div>
              </form>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
