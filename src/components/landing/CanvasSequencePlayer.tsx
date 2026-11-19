"use client";

import React, { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { Play, Pause, RotateCcw } from "lucide-react";

interface CanvasSequencePlayerProps {
  totalFrames?: number;
  fps?: number;
  className?: string;
}

export function CanvasSequencePlayer({
  totalFrames = 180,
  fps = 24,
  className = "",
}: CanvasSequencePlayerProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(true);
  const [currentFrameIndex, setCurrentFrameIndex] = useState<number>(1);
  const [isLoaded, setIsLoaded] = useState<boolean>(false);
  const [loadedCount, setLoadedCount] = useState<number>(0);
  const imagesRef = useRef<HTMLImageElement[]>([]);
  const animationFrameId = useRef<number | null>(null);
  const lastTimeRef = useRef<number>(0);

  // Preload frames
  useEffect(() => {
    let isMounted = true;
    const images: HTMLImageElement[] = [];
    const step = 1; // can sample every frame
    const framesToLoad: number[] = [];

    for (let i = 1; i <= Math.min(totalFrames, 180); i += step) {
      framesToLoad.push(i);
    }

    let loaded = 0;
    framesToLoad.forEach((frameNum, idx) => {
      const img = new window.Image();
      const paddedNum = String(frameNum).padStart(3, "0");
      img.src = `/images/sequence/ezgif-frame-${paddedNum}.jpg`;

      img.onload = () => {
        if (!isMounted) return;
        loaded += 1;
        setLoadedCount(loaded);
        if (loaded >= Math.min(20, framesToLoad.length)) {
          setIsLoaded(true);
        }
      };

      img.onerror = () => {
        // Fallback to static hero if frames fail
        if (!isMounted) return;
        loaded += 1;
      };

      images[idx] = img;
    });

    imagesRef.current = images;

    return () => {
      isMounted = false;
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
      }
    };
  }, [totalFrames]);

  // Render loop
  useEffect(() => {
    if (!isPlaying || !isLoaded) return;

    const interval = 1000 / fps;

    const render = (currentTime: number) => {
      if (!lastTimeRef.current) lastTimeRef.current = currentTime;
      const delta = currentTime - lastTimeRef.current;

      if (delta >= interval) {
        lastTimeRef.current = currentTime - (delta % interval);

        setCurrentFrameIndex((prev) => {
          const next = prev >= imagesRef.current.length - 1 ? 0 : prev + 1;
          const canvas = canvasRef.current;
          if (canvas) {
            const ctx = canvas.getContext("2d");
            const img = imagesRef.current[next];
            if (ctx && img && img.complete && img.naturalWidth > 0) {
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            }
          }
          return next;
        });
      }

      animationFrameId.current = requestAnimationFrame(render);
    };

    animationFrameId.current = requestAnimationFrame(render);

    return () => {
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
      }
    };
  }, [isPlaying, isLoaded, fps]);

  // Initial draw once first frame ready
  useEffect(() => {
    if (isLoaded && canvasRef.current && imagesRef.current[0]) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      const img = imagesRef.current[0];
      if (ctx && img && img.complete) {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      }
    }
  }, [isLoaded]);

  const togglePlay = () => setIsPlaying((prev) => !prev);
  const handleReset = () => {
    setCurrentFrameIndex(0);
    if (canvasRef.current && imagesRef.current[0]) {
      const ctx = canvasRef.current.getContext("2d");
      if (ctx) ctx.drawImage(imagesRef.current[0], 0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  };

  return (
    <div className={`relative rounded-3xl overflow-hidden glass-panel border border-indigo-500/30 shadow-2xl shadow-blue-950/80 group ${className}`}>
      {/* Fallback image while loading */}
      {!isLoaded && (
        <div className="absolute inset-0 z-0">
          <Image
            src="/images/hero-career-ai.jpg"
            alt="Elevate X AI Career Intelligence"
            fill
            className="object-cover object-center"
            priority
          />
          <div className="absolute inset-0 bg-[#080B18]/50 flex items-center justify-center">
            <div className="flex items-center gap-2.5 px-4 py-2 rounded-full bg-slate-900/90 border border-slate-700 text-xs text-slate-300">
              <span className="w-2 h-2 rounded-full bg-blue-500 animate-ping" />
              Loading Cinematic AI Feed ({loadedCount}/{Math.min(totalFrames, 180)})...
            </div>
          </div>
        </div>
      )}

      {/* HTML5 Canvas */}
      <canvas
        ref={canvasRef}
        width={1280}
        height={720}
        className={`w-full h-auto aspect-video object-cover transition-opacity duration-700 ${
          isLoaded ? "opacity-100" : "opacity-0"
        }`}
      />

      {/* Futuristic Blue-Violet Vignette Overlay */}
      <div className="absolute inset-0 pointer-events-none bg-gradient-to-t from-[#080B18] via-transparent to-[#080B18]/40" />
      <div className="absolute inset-0 pointer-events-none bg-radial-gradient from-transparent via-[#080B18]/20 to-[#080B18]/70" />

      {/* Subtle Bottom Controls */}
      <div className="absolute bottom-3 right-4 z-20 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <button
          onClick={togglePlay}
          aria-label={isPlaying ? "Pause animation" : "Play animation"}
          className="p-2 rounded-lg bg-slate-900/80 backdrop-blur-md border border-slate-700/60 text-slate-200 hover:text-white hover:bg-slate-800 transition-colors"
        >
          {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
        </button>
        <button
          onClick={handleReset}
          aria-label="Restart animation"
          className="p-2 rounded-lg bg-slate-900/80 backdrop-blur-md border border-slate-700/60 text-slate-200 hover:text-white hover:bg-slate-800 transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
        <div className="px-2.5 py-1 rounded-md bg-slate-900/80 border border-slate-700/60 text-[10px] font-mono text-cyan-400">
          FRAME {currentFrameIndex + 1}/{imagesRef.current.length || totalFrames}
        </div>
      </div>
    </div>
  );
}
