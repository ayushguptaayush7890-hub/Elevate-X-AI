"use client";

import React, { useEffect, useRef, useState, useCallback } from "react";

interface SequenceCanvasCoverProps {
  totalFrames?: number;
  framePathPrefix?: string;
  overlayOpacity?: number; // 0 to 1
}

export function SequenceCanvasCover({
  totalFrames = 190,
  framePathPrefix = "/animation-frames/ezgif-frame-",
  overlayOpacity = 0.35,
}: SequenceCanvasCoverProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  // Images cache
  const imagesRef = useRef<HTMLImageElement[]>([]);
  const currentFrameRef = useRef<number>(0);
  const lastFrameTimeRef = useRef<number>(0);

  // Helper to get image path by 1-based index
  const getFramePath = useCallback(
    (index: number) => {
      const padded = String(index).padStart(3, "0");
      return `${framePathPrefix}${padded}.jpg`;
    },
    [framePathPrefix]
  );

  // 1. Draw a given frame to the canvas with "object-fit: cover"
  const renderFrame = useCallback((frameIdx: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d", { alpha: false });
    if (!ctx) return;

    const img = imagesRef.current[frameIdx];
    if (!img || !img.complete || img.naturalWidth === 0) return;

    const cw = canvas.width;
    const ch = canvas.height;
    const iw = img.naturalWidth;
    const ih = img.naturalHeight;

    // Cover math
    const imgRatio = iw / ih;
    const canvasRatio = cw / ch;

    let drawWidth: number;
    let drawHeight: number;
    let drawX: number;
    let drawY: number;

    if (canvasRatio > imgRatio) {
      drawWidth = cw;
      drawHeight = cw / imgRatio;
      drawX = 0;
      drawY = (ch - drawHeight) / 2;
    } else {
      drawHeight = ch;
      drawWidth = ch * imgRatio;
      drawX = (cw - drawWidth) / 2;
      drawY = 0;
    }

    ctx.drawImage(img, drawX, drawY, drawWidth, drawHeight);
  }, []);

  // 2. Resize canvas to match display size * devicePixelRatio
  const handleResize = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const width = window.innerWidth;
    const height = window.innerHeight;

    if (canvas.width !== width * dpr || canvas.height !== height * dpr) {
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
    }

    renderFrame(Math.round(currentFrameRef.current));
  }, [renderFrame]);

  // 3. Preload all 190 frames progressively
  useEffect(() => {
    let mounted = true;
    const images: HTMLImageElement[] = new Array(totalFrames);

    // Load first frame immediately for instant first paint
    const firstImg = new Image();
    firstImg.src = getFramePath(1);
    firstImg.onload = () => {
      if (!mounted) return;
      images[0] = firstImg;
      renderFrame(0);

      // Load remaining frames in background
      for (let i = 2; i <= totalFrames; i++) {
        const img = new Image();
        img.src = getFramePath(i);
        const idx = i - 1;

        img.onload = () => {
          if (!mounted) return;
          images[idx] = img;
        };
      }
    };

    imagesRef.current = images;

    return () => {
      mounted = false;
    };
  }, [totalFrames, getFramePath, renderFrame]);

  // 4. Handle window resize
  useEffect(() => {
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [handleResize]);

  // 5. Cinematic playback: plays once at 30fps and freezes permanently on the last frame!
  useEffect(() => {
    let animId: number;
    const fpsInterval = 1000 / 30; // 30 FPS smooth cinematic motion
    let isPlaying = true;

    const loop = (timestamp: number) => {
      if (isPlaying) {
        const elapsed = timestamp - lastFrameTimeRef.current;
        if (elapsed > fpsInterval) {
          lastFrameTimeRef.current = timestamp - (elapsed % fpsInterval);

          if (currentFrameRef.current < totalFrames - 1) {
            const next = currentFrameRef.current + 1;
            currentFrameRef.current = next;
            renderFrame(Math.round(next));

            // When reaching the last frame (frame 190), stop permanently!
            if (next >= totalFrames - 1) {
              isPlaying = false;
            }
          }
        }
      }

      if (isPlaying) {
        animId = requestAnimationFrame(loop);
      }
    };

    animId = requestAnimationFrame(loop);

    return () => {
      if (animId) cancelAnimationFrame(animId);
    };
  }, [totalFrames, renderFrame]);

  return (
    <div
      ref={containerRef}
      className="fixed inset-0 w-full h-full pointer-events-none -z-10 overflow-hidden bg-[#FAFAFF]"
    >
      {/* 1. Canvas displaying the video frames */}
      <canvas
        ref={canvasRef}
        className="w-full h-full object-cover block transition-opacity duration-700"
      />

      {/* 2. Soft Luminous Lavender/White Ambient Overlays matching Dashboard */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(ellipse at center, rgba(250, 250, 255, ${overlayOpacity * 0.4}) 0%, rgba(250, 250, 255, ${overlayOpacity * 1.1}) 65%, #FAFAFF 100%)`,
        }}
      />

      {/* Ambient glowing color accents matching the brand */}
      <div className="absolute top-1/4 -left-20 w-96 h-96 bg-purple-400/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-cyan-400/20 rounded-full blur-[120px] pointer-events-none" />
    </div>
  );
}
