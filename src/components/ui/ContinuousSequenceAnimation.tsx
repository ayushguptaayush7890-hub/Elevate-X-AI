"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";

interface ContinuousSequenceAnimationProps {
  totalFrames?: number;
  framePathPrefix?: string;
  fps?: number;
  className?: string;
  aspectRatio?: string; // e.g., "16/9"
  fit?: "cover" | "contain";
  overlayGradient?: boolean;
  priorityInitialFrames?: number;
}

export function ContinuousSequenceAnimation({
  totalFrames = 190,
  framePathPrefix = "/animation-frames/ezgif-frame-",
  fps = 24,
  className = "",
  aspectRatio = "16/9",
  fit = "cover",
  overlayGradient = false,
  priorityInitialFrames = 20,
}: ContinuousSequenceAnimationProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const [isReady, setIsReady] = useState(false);
  const [loadProgress, setLoadProgress] = useState(0);

  const imagesRef = useRef<HTMLImageElement[]>([]);
  const currentFrameIndexRef = useRef(0);
  const animFrameIdRef = useRef<number | null>(null);
  const lastDrawTimeRef = useRef(0);
  const isVisibleRef = useRef(true);

  // Pad frame number: 1 -> "001"
  const getFrameUrl = useCallback(
    (index: number) => {
      const padded = String(index).padStart(3, "0");
      return `${framePathPrefix}${padded}.jpg`;
    },
    [framePathPrefix]
  );

  // Render a specific frame on canvas with proper aspect ratio math
  const drawFrame = useCallback(
    (frameIdx: number) => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext("2d", { alpha: false });
      if (!ctx) return;

      const img = imagesRef.current[frameIdx];
      if (!img || !img.complete || img.naturalWidth === 0) {
        // Fallback to nearest loaded previous frame
        for (let i = frameIdx - 1; i >= 0; i--) {
          const fallback = imagesRef.current[i];
          if (fallback && fallback.complete && fallback.naturalWidth > 0) {
            ctx.drawImage(fallback, 0, 0, canvas.width, canvas.height);
            break;
          }
        }
        return;
      }

      const cw = canvas.width;
      const ch = canvas.height;
      const iw = img.naturalWidth;
      const ih = img.naturalHeight;

      if (fit === "cover") {
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
      } else {
        // contain
        const imgRatio = iw / ih;
        const canvasRatio = cw / ch;

        let dw: number;
        let dh: number;
        let dx: number;
        let dy: number;

        if (canvasRatio > imgRatio) {
          dh = ch;
          dw = ch * imgRatio;
          dx = (cw - dw) / 2;
          dy = 0;
        } else {
          dw = cw;
          dh = cw / imgRatio;
          dx = 0;
          dy = (ch - dh) / 2;
        }

        ctx.fillStyle = "#10192D";
        ctx.fillRect(0, 0, cw, ch);
        ctx.drawImage(img, dx, dy, dw, dh);
      }
    },
    [fit]
  );

  // Canvas size sync
  const updateCanvasDimensions = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const rect = container.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    const w = Math.round(rect.width * dpr);
    const h = Math.round(rect.height * dpr);

    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w || 1280;
      canvas.height = h || 720;
    }

    drawFrame(currentFrameIndexRef.current);
  }, [drawFrame]);

  // Progressive preloader: Phase 1 loads initial frames, Phase 2 loads remaining in idle chunks
  useEffect(() => {
    let isCancelled = false;
    const images: HTMLImageElement[] = new Array(totalFrames);
    let loadedCount = 0;

    // Phase 1: High priority initial frames
    const initialBatchSize = Math.min(priorityInitialFrames, totalFrames);

    for (let i = 1; i <= initialBatchSize; i++) {
      const img = new Image();
      img.src = getFrameUrl(i);
      img.onload = () => {
        if (isCancelled) return;
        loadedCount++;
        setLoadProgress(Math.round((loadedCount / totalFrames) * 100));

        if (loadedCount >= Math.min(6, initialBatchSize)) {
          setIsReady(true);
        }
      };
      img.onerror = () => {
        if (isCancelled) return;
        loadedCount++;
      };
      images[i - 1] = img;
    }

    // Phase 2: Background idle loader for remaining frames
    let currentIdx = initialBatchSize + 1;

    const loadNextChunk = () => {
      if (isCancelled || currentIdx > totalFrames) return;
      const chunkSize = 10;
      const limit = Math.min(currentIdx + chunkSize, totalFrames + 1);

      for (let i = currentIdx; i < limit; i++) {
        const img = new Image();
        img.src = getFrameUrl(i);
        img.onload = () => {
          if (isCancelled) return;
          loadedCount++;
          setLoadProgress(Math.round((loadedCount / totalFrames) * 100));
        };
        img.onerror = () => {
          if (isCancelled) return;
          loadedCount++;
        };
        images[i - 1] = img;
      }

      currentIdx = limit;

      if (currentIdx <= totalFrames) {
        if ("requestIdleCallback" in window) {
          (window as any).requestIdleCallback(loadNextChunk, { timeout: 1000 });
        } else {
          setTimeout(loadNextChunk, 80);
        }
      }
    };

    if ("requestIdleCallback" in window) {
      (window as any).requestIdleCallback(loadNextChunk, { timeout: 500 });
    } else {
      setTimeout(loadNextChunk, 150);
    }

    imagesRef.current = images;

    return () => {
      isCancelled = true;
    };
  }, [totalFrames, getFrameUrl, priorityInitialFrames]);

  // Resize listener
  useEffect(() => {
    updateCanvasDimensions();
    const handleResize = () => updateCanvasDimensions();
    window.addEventListener("resize", handleResize, { passive: true });
    return () => window.removeEventListener("resize", handleResize);
  }, [updateCanvasDimensions]);

  // Visibility detection (IntersectionObserver)
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        isVisibleRef.current = entry.isIntersecting;
      },
      { threshold: 0.05 }
    );

    observer.observe(container);
    return () => observer.disconnect();
  }, []);

  // Continuous animation loop using requestAnimationFrame
  useEffect(() => {
    if (!isReady) return;

    // Check prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const effectiveFps = prefersReducedMotion ? 6 : fps;
    const frameInterval = 1000 / effectiveFps;

    const loop = (timestamp: number) => {
      if (!lastDrawTimeRef.current) lastDrawTimeRef.current = timestamp;
      const elapsed = timestamp - lastDrawTimeRef.current;

      if (elapsed >= frameInterval && isVisibleRef.current) {
        lastDrawTimeRef.current = timestamp - (elapsed % frameInterval);

        // Advance to next frame in continuous loop
        const nextFrame = (currentFrameIndexRef.current + 1) % totalFrames;
        currentFrameIndexRef.current = nextFrame;

        drawFrame(nextFrame);
      }

      animFrameIdRef.current = requestAnimationFrame(loop);
    };

    animFrameIdRef.current = requestAnimationFrame(loop);

    return () => {
      if (animFrameIdRef.current) {
        cancelAnimationFrame(animFrameIdRef.current);
      }
    };
  }, [isReady, totalFrames, fps, drawFrame]);

  return (
    <div
      ref={containerRef}
      className={`relative w-full overflow-hidden rounded-2xl bg-[#10192D] select-none ${className}`}
      style={{ aspectRatio }}
    >
      {/* Canvas */}
      <canvas
        ref={canvasRef}
        className={`w-full h-full object-cover transition-opacity duration-700 ${
          isReady ? "opacity-100" : "opacity-0"
        }`}
      />

      {/* Loading Skeleton */}
      {!isReady && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-[#10192D] text-[#D6A84B] space-y-2">
          <div className="w-8 h-8 rounded-full border-2 border-[#D6A84B]/30 border-t-[#D6A84B] animate-spin" />
          <span className="text-[11px] font-mono tracking-wider text-[#F0D99B]">
            Preparing Sequence ({loadProgress}%)
          </span>
        </div>
      )}

      {/* Optional Overlay Gradient for seamless blending */}
      {overlayGradient && (
        <div className="absolute inset-0 bg-gradient-to-t from-[#10192D]/80 via-transparent to-[#10192D]/30 pointer-events-none" />
      )}
    </div>
  );
}

