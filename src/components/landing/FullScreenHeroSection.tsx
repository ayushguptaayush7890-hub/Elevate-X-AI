"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";
import Link from "next/link";
import {
  Sparkles,
  ArrowRight,
  CheckCircle2,
  Briefcase,
  Award,
  TrendingUp,
} from "lucide-react";

interface FullScreenHeroSectionProps {
  totalFrames?: number;
  framePathPrefix?: string;
  fps?: number;
}

export function FullScreenHeroSection({
  totalFrames = 190,
  framePathPrefix = "/animation-frames/ezgif-frame-",
  fps = 24,
}: FullScreenHeroSectionProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const particleCanvasRef = useRef<HTMLCanvasElement | null>(null);

  const imagesRef = useRef<HTMLImageElement[]>([]);
  const currentFrameRef = useRef<number>(0);
  const animFrameIdRef = useRef<number | null>(null);
  const particleAnimIdRef = useRef<number | null>(null);
  const lastDrawTimeRef = useRef<number>(0);

  const [isReady, setIsReady] = useState(false);
  const [mouseOffset, setMouseOffset] = useState({ x: 0, y: 0 });

  // 1. Frame URL helper (ezgif-frame-001.jpg .. 190.jpg)
  const getFrameUrl = useCallback(
    (index: number) => {
      const padded = String(index).padStart(3, "0");
      return `${framePathPrefix}${padded}.jpg`;
    },
    [framePathPrefix]
  );

  // 2. High performance frame drawing with object-fit: cover math
  const drawFrame = useCallback((frameIdx: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d", { alpha: false });
    if (!ctx) return;

    let img = imagesRef.current[frameIdx];

    // Fallback: if current frame not ready, find nearest loaded previous frame
    if (!img || !img.complete || img.naturalWidth === 0) {
      for (let i = frameIdx - 1; i >= 0; i--) {
        const fallback = imagesRef.current[i];
        if (fallback && fallback.complete && fallback.naturalWidth > 0) {
          img = fallback;
          break;
        }
      }
    }

    if (!img || !img.complete || img.naturalWidth === 0) return;

    const cw = canvas.width;
    const ch = canvas.height;
    const iw = img.naturalWidth;
    const ih = img.naturalHeight;

    // Strict "object-fit: cover" calculation
    const imgRatio = iw / ih;
    const canvasRatio = cw / ch;

    let dw: number;
    let dh: number;
    let dx: number;
    let dy: number;

    if (canvasRatio > imgRatio) {
      dw = cw;
      dh = cw / imgRatio;
      dx = 0;
      dy = (ch - dh) / 2;
    } else {
      dh = ch;
      dw = ch * imgRatio;
      dx = (cw - dw) / 2;
      dy = 0;
    }

    ctx.drawImage(img, dx, dy, dw, dh);
  }, []);

  // 3. Resize canvas to match display size * devicePixelRatio
  const handleResize = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const rect = container.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    const w = Math.round(rect.width * dpr);
    const h = Math.round(rect.height * dpr);

    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w || 1920;
      canvas.height = h || 1080;
    }

    // Also resize particle canvas
    const pCanvas = particleCanvasRef.current;
    if (pCanvas) {
      pCanvas.width = w || 1920;
      pCanvas.height = h || 1080;
    }

    drawFrame(Math.round(currentFrameRef.current));
  }, [drawFrame]);

  // 4. Efficient 2-phase preloading: Phase 1 loads first 20 frames immediately, Phase 2 loads rest in idle chunks
  useEffect(() => {
    let isMounted = true;
    const images: HTMLImageElement[] = new Array(totalFrames);

    // Phase 1: High priority initial 20 frames
    const initialBatch = Math.min(20, totalFrames);
    let loadedCount = 0;

    for (let i = 1; i <= initialBatch; i++) {
      const img = new Image();
      img.src = getFrameUrl(i);
      img.onload = () => {
        if (!isMounted) return;
        loadedCount++;
        if (i === 1) {
          drawFrame(0);
        }
        if (loadedCount >= Math.min(6, initialBatch)) {
          setIsReady(true);
        }
      };
      images[i - 1] = img;
    }

    // Phase 2: Background idle chunk loader for remaining frames
    let nextIndex = initialBatch + 1;
    const loadNextChunk = () => {
      if (!isMounted || nextIndex > totalFrames) return;
      const chunkSize = 12;
      const limit = Math.min(nextIndex + chunkSize, totalFrames + 1);

      for (let i = nextIndex; i < limit; i++) {
        const img = new Image();
        img.src = getFrameUrl(i);
        images[i - 1] = img;
      }
      nextIndex = limit;

      if (nextIndex <= totalFrames) {
        if ("requestIdleCallback" in window) {
          (window as any).requestIdleCallback(loadNextChunk, { timeout: 800 });
        } else {
          setTimeout(loadNextChunk, 60);
        }
      }
    };

    if ("requestIdleCallback" in window) {
      (window as any).requestIdleCallback(loadNextChunk, { timeout: 400 });
    } else {
      setTimeout(loadNextChunk, 100);
    }

    imagesRef.current = images;

    return () => {
      isMounted = false;
    };
  }, [totalFrames, getFrameUrl, drawFrame]);

  // 5. Handle window resize
  useEffect(() => {
    handleResize();
    window.addEventListener("resize", handleResize, { passive: true });
    return () => window.removeEventListener("resize", handleResize);
  }, [handleResize]);

  // 6. Animation RAF Playback:
  // Plays from frame 0 up to frame 189 (190 total frames).
  // When reaching the last frame, it stops cleanly on frame 190 as requested ("last mai iss page par ruk jaaye").
  const startPlayback = useCallback(() => {
    if (animFrameIdRef.current) cancelAnimationFrame(animFrameIdRef.current);

    const frameInterval = 1000 / fps;
    lastDrawTimeRef.current = 0;

    const loop = (timestamp: number) => {
      if (!lastDrawTimeRef.current) lastDrawTimeRef.current = timestamp;
      const elapsed = timestamp - lastDrawTimeRef.current;

      if (elapsed >= frameInterval) {
        lastDrawTimeRef.current = timestamp - (elapsed % frameInterval);

        if (currentFrameRef.current < totalFrames - 1) {
          currentFrameRef.current += 1;
          drawFrame(currentFrameRef.current);
        } else {
          // Reached the final frame (190) -> stop and hold permanently on this hero scene!
          drawFrame(totalFrames - 1);
          return;
        }
      }

      animFrameIdRef.current = requestAnimationFrame(loop);
    };

    animFrameIdRef.current = requestAnimationFrame(loop);
  }, [fps, totalFrames, drawFrame]);

  useEffect(() => {
    if (!isReady) return;
    startPlayback();

    return () => {
      if (animFrameIdRef.current) cancelAnimationFrame(animFrameIdRef.current);
    };
  }, [isReady, startPlayback]);

  // 7. Layer 3: Lightweight Drifting Particles (Champagne Gold & Electric Cyan)
  useEffect(() => {
    const pCanvas = particleCanvasRef.current;
    if (!pCanvas) return;
    const ctx = pCanvas.getContext("2d");
    if (!ctx) return;

    interface Particle {
      x: number;
      y: number;
      size: number;
      speedY: number;
      speedX: number;
      color: string;
      alpha: number;
      alphaSpeed: number;
    }

    const count = 35;
    const colors = ["#D6A84B", "#36D6E8", "#7355D9", "#F0D99B"];
    const particles: Particle[] = [];

    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * pCanvas.width,
        y: Math.random() * pCanvas.height,
        size: Math.random() * 2.2 + 0.8,
        speedY: -(Math.random() * 0.4 + 0.15),
        speedX: (Math.random() - 0.5) * 0.25,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: Math.random() * 0.6 + 0.2,
        alphaSpeed: (Math.random() * 0.015 + 0.005) * (Math.random() > 0.5 ? 1 : -1),
      });
    }

    const renderParticles = () => {
      ctx.clearRect(0, 0, pCanvas.width, pCanvas.height);

      particles.forEach((p) => {
        p.y += p.speedY;
        p.x += p.speedX;
        p.alpha += p.alphaSpeed;

        if (p.alpha > 0.85 || p.alpha < 0.15) {
          p.alphaSpeed = -p.alphaSpeed;
        }

        if (p.y < 0) {
          p.y = pCanvas.height + 10;
          p.x = Math.random() * pCanvas.width;
        }
        if (p.x < 0) p.x = pCanvas.width;
        if (p.x > pCanvas.width) p.x = 0;

        ctx.save();
        ctx.globalAlpha = Math.max(0.1, Math.min(p.alpha, 0.8));
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      });

      particleAnimIdRef.current = requestAnimationFrame(renderParticles);
    };

    renderParticles();

    return () => {
      if (particleAnimIdRef.current) cancelAnimationFrame(particleAnimIdRef.current);
    };
  }, []);

  // 8. Gentle Mouse Parallax
  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    setMouseOffset({ x, y });
  };

  return (
    <section
      ref={containerRef}
      onMouseMove={handleMouseMove}
      className="relative w-full min-h-[100svh] h-[100svh] overflow-hidden flex items-center bg-[#100B2E] select-none"
    >
      {/* =========================================================================
          LAYER 1: FULL-SCREEN JPG SEQUENCE CANVAS (EDGE TO EDGE, 100vw x 100svh)
         ========================================================================= */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full object-cover pointer-events-none z-0 transition-opacity duration-1000"
        style={{ opacity: isReady ? 1 : 0.4 }}
      />

      {/* =========================================================================
          LAYER 2: SUBTLE GRADIENT & LIGHTING OVERLAYS (NO LARGE WHITE OVERLAY)
         ========================================================================= */}
      {/* Left Vignette: Enhances text legibility on the left 50% without washing out the center */}
      <div
        className="absolute inset-0 pointer-events-none z-1"
        style={{
          background:
            "linear-gradient(to right, rgba(16, 25, 45, 0.92) 0%, rgba(16, 25, 45, 0.75) 35%, rgba(16, 25, 45, 0.35) 60%, transparent 100%)",
        }}
      />

      {/* Top Navbar Dark Vignette */}
      <div
        className="absolute top-0 left-0 right-0 h-32 pointer-events-none z-1"
        style={{
          background: "linear-gradient(to bottom, rgba(16, 25, 45, 0.7) 0%, transparent 100%)",
        }}
      />

      {/* Bottom Section Blend: Smooth transition into the ivory/cream background of Section 2 */}
      <div
        className="absolute bottom-0 left-0 right-0 h-28 pointer-events-none z-1"
        style={{
          background:
            "linear-gradient(to top, #FBF8F1 0%, rgba(251, 248, 241, 0.7) 30%, transparent 100%)",
        }}
      />

      {/* Ambient Electric-Blue & Soft Violet Radial Glows */}
      <div className="absolute top-1/4 left-1/4 w-[450px] h-[450px] bg-[#36D6E8]/10 blur-[130px] rounded-full pointer-events-none z-1" />
      <div className="absolute top-1/3 right-1/4 w-[500px] h-[500px] bg-[#7355D9]/20 blur-[140px] rounded-full pointer-events-none z-1" />

      {/* =========================================================================
          LAYER 3: LIGHTWEIGHT DRIFTING GOLD & CYAN PARTICLES
         ========================================================================= */}
      <canvas
        ref={particleCanvasRef}
        className="absolute inset-0 w-full h-full pointer-events-none z-2"
      />

      {/* =========================================================================
          LAYER 4: CONTENT OVERLAY (HEADING, BUTTONS, TRUST BADGES & 3 HOLOGRAPHIC CARDS)
         ========================================================================= */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10 pt-20 pb-12 lg:py-0">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center min-h-[calc(100svh-5rem)]">
          {/* LEFT 50% (lg:col-span-6): Core Value Proposition & CTAs */}
          <div className="lg:col-span-6 space-y-6 text-center lg:text-left">
            {/* Small Premium Eyebrow Badge */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#10192D]/85 border border-[#D6A84B]/40 text-xs font-bold text-[#F0D99B] shadow-xl backdrop-blur-md">
              <span className="w-2 h-2 rounded-full bg-[#D6A84B] animate-pulse" />
              <span className="tracking-widest uppercase text-[11px]">
                AI-Powered Career Ecosystem
              </span>
            </div>

            {/* Large Heading with Electric-Blue to Violet Gradient */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-[1.08] text-white">
              Your Experience. <br />
              <span className="bg-gradient-to-r from-[#36D6E8] via-[#3478F6] to-[#7355D9] bg-clip-text text-transparent">
                Your Skills.
              </span>{" "}
              <br />
              Your Future.
            </h1>

            {/* Professional Subtitle (Max Width 520px) */}
            <p className="text-[#E6DFD1]/90 text-base sm:text-lg leading-relaxed max-w-[520px] mx-auto lg:mx-0 font-normal">
              Turn your real-world trade experience into meaningful career opportunities with
              intelligent AI skill recognition, practical diagnostics, and personalized guidance.
            </p>

            {/* Primary & Secondary CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <Link
                href="/onboarding"
                className="btn-gold w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-2xl text-sm font-bold tracking-wide shadow-xl shadow-[#D6A84B]/25 hover:scale-105 transition-all"
              >
                <Sparkles className="w-4 h-4 text-[#10192D]" />
                <span>Start Your Journey</span>
              </Link>

              <Link
                href="/#features"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-4 rounded-2xl text-sm font-bold bg-[#17233F]/85 hover:bg-[#17233F] text-[#F5F0E6] border border-[#D6A84B]/35 backdrop-blur-xl transition-all hover:border-[#D6A84B] hover:scale-105 shadow-md"
              >
                <span>Explore Features</span>
                <ArrowRight className="w-4 h-4 text-[#D6A84B]" />
              </Link>
            </div>

            {/* Three Small Trust Indicators Underneath */}
            <div className="pt-4 flex flex-wrap items-center justify-center lg:justify-start gap-3 text-xs text-[#E6DFD1]/85 font-semibold">
              <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#10192D]/75 backdrop-blur-md border border-white/10 shadow-sm">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#D6A84B]" /> AI Skill Recognition
              </span>
              <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#10192D]/75 backdrop-blur-md border border-white/10 shadow-sm">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#36D6E8]" /> Adaptive Diagnostics
              </span>
              <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#10192D]/75 backdrop-blur-md border border-white/10 shadow-sm">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#27856B]" /> Vetted Job Matching
              </span>
            </div>
          </div>

          {/* RIGHT 50% (lg:col-span-6): Three Floating Holographic Glass Cards with Parallax */}
          <div
            className="lg:col-span-6 relative h-[420px] sm:h-[480px] lg:h-[540px] flex items-center justify-center"
            style={{
              transform: `translate3d(${mouseOffset.x * 16}px, ${mouseOffset.y * 16}px, 0)`,
              transition: "transform 0.2s cubic-bezier(0.16, 1, 0.3, 1)",
            }}
          >
            {/* CARD 1: Smart Job Matching (Top Right) */}
            <div
              className="absolute top-4 sm:top-10 right-2 sm:right-6 max-w-[280px] sm:max-w-[320px] p-4 rounded-2xl bg-[#10192D]/85 backdrop-blur-xl border border-[#36D6E8]/40 shadow-2xl animate-float-slow"
              style={{
                transform: `translate3d(${mouseOffset.x * -10}px, ${mouseOffset.y * -10}px, 0)`,
              }}
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#36D6E8]/15 border border-[#36D6E8]/35 flex items-center justify-center shrink-0">
                  <Briefcase className="w-5 h-5 text-[#36D6E8]" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white tracking-wide">
                      Smart Job Matching
                    </span>
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-[#27856B]/25 text-[#36D6E8] border border-[#27856B]/40">
                      95% Match
                    </span>
                  </div>
                  <p className="text-[11px] text-[#E6DFD1]/75 line-clamp-1 mt-0.5">
                    Apparel QA Specialist • Raymond Exports
                  </p>
                </div>
              </div>
            </div>

            {/* CARD 2: Skill Recognition (Mid/Far Right) */}
            <div
              className="absolute top-1/2 -translate-y-1/2 -right-1 sm:right-0 max-w-[290px] sm:max-w-[330px] p-4 rounded-2xl bg-[#10192D]/85 backdrop-blur-xl border border-[#D6A84B]/40 shadow-2xl animate-float-medium"
              style={{
                transform: `translate3d(${mouseOffset.x * -18}px, ${mouseOffset.y * -18}px, 0)`,
              }}
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#D6A84B]/15 border border-[#D6A84B]/35 flex items-center justify-center shrink-0">
                  <Award className="w-5 h-5 text-[#D6A84B]" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white tracking-wide">
                      Skill Recognition
                    </span>
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-[#D6A84B]/20 text-[#F0D99B] border border-[#D6A84B]/35">
                      Verified
                    </span>
                  </div>
                  <p className="text-[11px] text-[#E6DFD1]/75 line-clamp-1 mt-0.5">
                    Lockstitch Machine Mastery • NSQF Level 5
                  </p>
                </div>
              </div>
            </div>

            {/* CARD 3: Career Roadmap (Bottom Center/Right) */}
            <div
              className="absolute bottom-6 sm:bottom-12 right-6 sm:right-16 max-w-[280px] sm:max-w-[320px] p-4 rounded-2xl bg-[#10192D]/85 backdrop-blur-xl border border-[#27856B]/40 shadow-2xl animate-float-fast"
              style={{
                transform: `translate3d(${mouseOffset.x * -12}px, ${mouseOffset.y * -12}px, 0)`,
              }}
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#27856B]/15 border border-[#27856B]/35 flex items-center justify-center shrink-0">
                  <TrendingUp className="w-5 h-5 text-[#27856B]" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white tracking-wide">
                      Career Roadmap
                    </span>
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-[#7355D9]/25 text-[#7355D9] border border-[#7355D9]/40">
                      Step 3
                    </span>
                  </div>
                  <p className="text-[11px] text-[#E6DFD1]/75 line-clamp-1 mt-0.5">
                    AQL 2.5 Sampling Bridge • 2 Wks to Goal
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

