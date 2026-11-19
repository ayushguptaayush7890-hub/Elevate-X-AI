"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { BrandButton } from "@/components/ui/BrandButton";
import { initialAssistantMessages } from "@/data/mock-data";
import { AssistantMessage } from "@/types";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import {
  Send,
  Bot,
  User,
  Copy,
  Plus,
  Globe,
  Sparkles,
  ShieldCheck
} from "lucide-react";

export default function AssistantPage() {
  const [messages, setMessages] = useState<AssistantMessage[]>(initialAssistantMessages);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState<"English" | "Hindi">("English");

  const sampleConversations = [
    { id: "c-1", title: "Apparel QA Interview Prep", date: "Today" },
    { id: "c-2", title: "AQL 2.5 Sampling Questions", date: "Yesterday" },
    { id: "c-3", title: "Tailoring Resume Summary", date: "Nov 9" },
  ];

  const handleSendMessage = (textToSend?: string) => {
    const text = textToSend || inputText;
    if (!text.trim()) return;

    const userMsg: AssistantMessage = {
      id: `msg-${Date.now()}`,
      sender: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      language: selectedLanguage,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText("");
    setIsTyping(true);

    // AI response simulation
    setTimeout(() => {
      let replyContent = "";

      if (selectedLanguage === "Hindi" || text.includes("हिंदी") || text.includes("Hindi")) {
        replyContent = `नमस्ते रमेश जी! आपके काम के अनुभव को ध्यान में रखते हुए, यहाँ सलाह है:

1. **कारीगरी की मान्यता:** जब आप किसी फॉर्मल कंपनी में जाएं, तो अपने 5 साल के प्रैक्टिकल काम (सिंगल नीडल लॉकस्टिच और पैटर्न ड्राफ्टिंग) पर पूरा भरोसा रखें।
2. **AQL 2.5 सैंपलिंग:** एक्सपोर्ट फैक्ट्री में सिर्फ एक बात का ध्यान रखना होता है कि 100 पीस में से 3 से ज्यादा बड़े नुक्स न हों।
3. **अगला कदम:** आप हमारे **AI Interview Lab** में 10 मिनट अभ्यास करें ताकि आपको सवालों के जवाब देने में पूरी सहजता महसूस हो।

क्या आप इंटरव्यू के किसी खास सवाल का अभ्यास करना चाहते हैं?`;
      } else {
        replyContent = `Great question, Ramesh! Based on your 5-year tailoring and garment construction background:

- **Key Differentiator:** Formal apparel export houses prize artisans who can detect tension defects, seam puckering, and fabric grain alignment before cutting.
- **Immediate Bridge:** Review the AQL 2.5 sampling tables in your Career Roadmap Stage 2. That covers 80% of what factory quality managers look for in initial rounds.
- **Next Step:** You can export your verified ATS resume and apply directly to the Raymond Lifestyle listing in the Jobs module.

Would you like me to generate a tailored talking point for your self-introduction?`;
      }

      const botMsg: AssistantMessage = {
        id: `msg-${Date.now() + 1}`,
        sender: "assistant",
        content: replyContent,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        suggestions: [
          "Generate my self-introduction for QA manager",
          "What are top 5 export defects?",
          "How do I explain informal workshop years?",
        ],
        language: selectedLanguage,
      };

      setMessages((prev) => [...prev, botMsg]);
      setIsTyping(false);
    }, 900);
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success("Response copied to clipboard.");
  };

  return (
    <AppShell>
      {/* Workspace Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-140px)] min-h-[620px]">
        {/* Left Sidebar: Conversations (3 cols) */}
        <div className="hidden lg:flex lg:col-span-3 flex-col bg-white rounded-2xl border border-[#E6DFD1] shadow-sm p-4 space-y-4">
          <button
            onClick={() => {
              setMessages(initialAssistantMessages);
              toast.info("Started new conversation.");
            }}
            className="flex items-center justify-center gap-2 w-full py-2.5 px-3 rounded-xl bg-[#17233F] hover:bg-[#10192D] text-[#F0D99B] border border-[#D6A84B]/40 text-xs font-bold transition-all"
          >
            <Plus className="w-4 h-4 text-[#D6A84B]" /> New Career Consultation
          </button>

          <div className="flex-1 overflow-y-auto space-y-1.5">
            <span className="text-[10px] font-bold text-[#687187] uppercase tracking-wider block px-2 mb-2">
              Recent Consultations
            </span>
            {sampleConversations.map((conv) => (
              <div
                key={conv.id}
                className="p-3 rounded-xl bg-[#FBF8F1] hover:bg-[#F5F0E6] border border-[#E6DFD1] text-xs text-[#20243A] cursor-pointer transition-colors"
              >
                <p className="font-bold text-[#17233F] truncate">{conv.title}</p>
                <p className="text-[10px] text-[#687187] mt-0.5">{conv.date}</p>
              </div>
            ))}
          </div>

          {/* Language Toggle */}
          <div className="pt-3 border-t border-[#E6DFD1]">
            <div className="flex items-center justify-between text-xs text-[#687187] mb-2">
              <span className="flex items-center gap-1 font-semibold">
                <Globe className="w-3.5 h-3.5 text-[#7355D9]" /> Language:
              </span>
              <span className="font-bold text-[#17233F]">{selectedLanguage}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                type="button"
                onClick={() => setSelectedLanguage("English")}
                className={`py-2 rounded-xl border text-center transition-all ${
                  selectedLanguage === "English"
                    ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                    : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                }`}
              >
                English
              </button>
              <button
                type="button"
                onClick={() => setSelectedLanguage("Hindi")}
                className={`py-2 rounded-xl border text-center transition-all ${
                  selectedLanguage === "Hindi"
                    ? "bg-[#17233F] text-[#F0D99B] border-[#D6A84B] font-bold shadow-sm"
                    : "bg-[#FBF8F1] border-[#E6DFD1] text-[#687187] hover:text-[#17233F]"
                }`}
              >
                हिन्दी
              </button>
            </div>
          </div>
        </div>

        {/* Main Panel: Chat Window (9 cols) */}
        <div className="lg:col-span-9 flex flex-col bg-white rounded-2xl border border-[#E6DFD1] shadow-sm overflow-hidden">
          {/* Top Bar */}
          <div className="p-4 border-b border-[#E6DFD1] flex items-center justify-between bg-[#FBF8F1]">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#17233F] text-[#F0D99B] border border-[#D6A84B]/40 flex items-center justify-center shadow-sm">
                <Bot className="w-5 h-5 text-[#D6A84B]" />
              </div>
              <div>
                <h2 className="text-sm font-bold text-[#17233F]">Elevate X AI Career Mentor</h2>
                <p className="text-xs text-[#27856B] font-semibold flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-[#27856B] animate-pulse" /> Multilingual Mode Active ({selectedLanguage})
                </p>
              </div>
            </div>

            <div className="hidden sm:flex items-center gap-2 text-xs text-[#687187] bg-white px-3 py-1.5 rounded-xl border border-[#E6DFD1]">
              <ShieldCheck className="w-3.5 h-3.5 text-[#27856B]" />
              <span>Vocational Career Coach</span>
            </div>
          </div>

          {/* Messages Stream */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-[#FBF8F1]/40">
            {messages.map((msg) => {
              const isUser = msg.sender === "user";
              return (
                <div
                  key={msg.id}
                  className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
                >
                  {!isUser && (
                    <div className="w-8 h-8 rounded-xl bg-[#17233F] text-[#D6A84B] flex items-center justify-center shrink-0 mt-0.5 border border-[#D6A84B]/30">
                      <Bot className="w-4 h-4 text-[#D6A84B]" />
                    </div>
                  )}

                  <div className={`max-w-xl space-y-2 ${isUser ? "items-end" : "items-start"}`}>
                    <div
                      className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                        isUser
                          ? "bg-[#17233F] text-white rounded-tr-none shadow-md border border-[#D6A84B]/30"
                          : "bg-white border border-[#E6DFD1] text-[#20243A] rounded-tl-none shadow-sm"
                      }`}
                    >
                      <div className={isUser ? "prose prose-invert prose-xs sm:prose-sm max-w-none text-white" : "prose prose-slate prose-xs sm:prose-sm max-w-none text-[#20243A]"}>
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 px-1 text-[11px] text-[#687187]">
                      <span>{msg.timestamp}</span>
                      {!isUser && (
                        <button
                          onClick={() => handleCopy(msg.content)}
                          className="hover:text-[#17233F] transition-colors"
                          title="Copy response"
                        >
                          <Copy className="w-3 h-3" />
                        </button>
                      )}
                    </div>

                    {/* Suggested Chips */}
                    {!isUser && msg.suggestions && (
                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {msg.suggestions.map((sug, i) => (
                          <button
                            key={i}
                            onClick={() => handleSendMessage(sug)}
                            className="text-xs px-3 py-1 rounded-full bg-white border border-[#D6A84B]/60 text-[#17233F] hover:bg-[#F0D99B]/30 transition-colors font-medium shadow-2xs"
                          >
                            {sug}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>

                  {isUser && (
                    <div className="w-8 h-8 rounded-xl bg-[#F5F0E6] text-[#17233F] flex items-center justify-center shrink-0 mt-0.5 border border-[#E6DFD1]">
                      <User className="w-4 h-4" />
                    </div>
                  )}
                </div>
              );
            })}

            {isTyping && (
              <div className="flex items-center gap-2 text-xs font-semibold text-[#7355D9]">
                <span className="w-2 h-2 rounded-full bg-[#7355D9] animate-ping" />
                <span>AI Mentor is drafting practical guidance...</span>
              </div>
            )}
          </div>

          {/* Input Box */}
          <div className="p-4 border-t border-[#E6DFD1] bg-white">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="flex items-center gap-2"
            >
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={
                  selectedLanguage === "Hindi"
                    ? "अपने काम या करियर से जुड़ा कोई भी सवाल पूछें..."
                    : "Ask any career, skill assessment, or interview question..."
                }
                className="flex-1 bg-[#FBF8F1] border border-[#E6DFD1] rounded-xl px-4 py-2.5 text-xs sm:text-sm text-[#20243A] focus:outline-none focus:border-[#D6A84B]"
              />

              <BrandButton type="submit" variant="gold" size="sm">
                <Send className="w-3.5 h-3.5 mr-1" />
                <span>Send</span>
              </BrandButton>
            </form>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
