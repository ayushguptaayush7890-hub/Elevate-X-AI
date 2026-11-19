"use client";

import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { Briefcase, Sparkles, TrendingUp, Award, Compass } from "lucide-react";

export function ThreeAiCoreHero() {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 550;
    const height = container.clientHeight || 550;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.z = 7;

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: "high-performance",
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // 2. Lighting Setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
    scene.add(ambientLight);

    const blueLight = new THREE.PointLight(0x3478f6, 3, 20);
    blueLight.position.set(4, 4, 5);
    scene.add(blueLight);

    const violetLight = new THREE.PointLight(0x7355d9, 3.5, 20);
    violetLight.position.set(-4, -3, 4);
    scene.add(violetLight);

    const goldLight = new THREE.PointLight(0xd6a84b, 2.5, 15);
    goldLight.position.set(0, 4, 3);
    scene.add(goldLight);

    // 3. Central AI Core Group
    const coreGroup = new THREE.Group();
    scene.add(coreGroup);

    // Central Glowing AI Sphere (Facet Icosahedron)
    const coreGeo = new THREE.IcosahedronGeometry(1.25, 3);
    const coreMat = new THREE.MeshStandardMaterial({
      color: 0x21105a,
      emissive: 0x7355d9,
      emissiveIntensity: 0.85,
      roughness: 0.2,
      metalness: 0.85,
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    coreGroup.add(coreMesh);

    // Outer Wireframe Lattice (Champagne Gold & Cyan)
    const wireGeo = new THREE.IcosahedronGeometry(1.5, 2);
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0xd6a84b,
      wireframe: true,
      transparent: true,
      opacity: 0.35,
    });
    const wireMesh = new THREE.Mesh(wireGeo, wireMat);
    coreGroup.add(wireMesh);

    // Inner glowing processor sphere
    const innerGeo = new THREE.SphereGeometry(0.85, 32, 32);
    const innerMat = new THREE.MeshBasicMaterial({
      color: 0x36d6e8,
      wireframe: true,
      transparent: true,
      opacity: 0.25,
    });
    const innerMesh = new THREE.Mesh(innerGeo, innerMat);
    coreGroup.add(innerMesh);

    // 4. Rotating Holographic Rings
    const ringGroup = new THREE.Group();
    scene.add(ringGroup);

    // Ring 1 (Gold)
    const ringGeo1 = new THREE.TorusGeometry(2.1, 0.015, 16, 120);
    const ringMat1 = new THREE.MeshStandardMaterial({
      color: 0xd6a84b,
      emissive: 0xd6a84b,
      emissiveIntensity: 0.6,
      roughness: 0.3,
    });
    const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
    ring1.rotation.x = Math.PI / 3;
    ringGroup.add(ring1);

    // Ring 2 (Electric Violet)
    const ringGeo2 = new THREE.TorusGeometry(2.4, 0.015, 16, 120);
    const ringMat2 = new THREE.MeshStandardMaterial({
      color: 0x7355d9,
      emissive: 0x7355d9,
      emissiveIntensity: 0.6,
      roughness: 0.3,
    });
    const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
    ring2.rotation.y = Math.PI / 4;
    ringGroup.add(ring2);

    // Ring 3 (Electric Blue)
    const ringGeo3 = new THREE.TorusGeometry(2.7, 0.012, 16, 120);
    const ringMat3 = new THREE.MeshStandardMaterial({
      color: 0x3478f6,
      emissive: 0x36d6e8,
      emissiveIntensity: 0.5,
      roughness: 0.4,
    });
    const ring3 = new THREE.Mesh(ringGeo3, ringMat3);
    ring3.rotation.x = -Math.PI / 4;
    ring3.rotation.z = Math.PI / 6;
    ringGroup.add(ring3);

    // 5. Neural Network Constellation Nodes
    const nodeCount = 30;
    const nodePositions: THREE.Vector3[] = [];
    const nodeGeo = new THREE.SphereGeometry(0.045, 12, 12);
    const nodeMat = new THREE.MeshBasicMaterial({ color: 0xf0d99b });
    const nodesGroup = new THREE.Group();

    for (let i = 0; i < nodeCount; i++) {
      const radius = 1.8 + Math.random() * 1.4;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const pos = new THREE.Vector3(
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.sin(phi) * Math.sin(theta),
        radius * Math.cos(phi)
      );
      nodePositions.push(pos);
      const nodeMesh = new THREE.Mesh(nodeGeo, nodeMat);
      nodeMesh.position.copy(pos);
      nodesGroup.add(nodeMesh);
    }
    scene.add(nodesGroup);

    // Dynamic Neural Network Connecting Lines
    const lineMat = new THREE.LineBasicMaterial({
      color: 0x7355d9,
      transparent: true,
      opacity: 0.28,
    });
    const lineIndices: number[] = [];
    for (let i = 0; i < nodeCount; i++) {
      for (let j = i + 1; j < nodeCount; j++) {
        if (nodePositions[i].distanceTo(nodePositions[j]) < 1.3) {
          lineIndices.push(
            nodePositions[i].x, nodePositions[i].y, nodePositions[i].z,
            nodePositions[j].x, nodePositions[j].y, nodePositions[j].z
          );
        }
      }
    }
    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute("position", new THREE.Float32BufferAttribute(lineIndices, 3));
    const linesMesh = new THREE.LineSegments(lineGeo, lineMat);
    nodesGroup.add(linesMesh);

    // 6. Floating Ambient Particle Dust
    const particleCount = 240;
    const particlePositions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i += 3) {
      particlePositions[i] = (Math.random() - 0.5) * 8;
      particlePositions[i + 1] = (Math.random() - 0.5) * 8;
      particlePositions[i + 2] = (Math.random() - 0.5) * 6;
    }
    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute("position", new THREE.BufferAttribute(particlePositions, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0x36d6e8,
      size: 0.035,
      transparent: true,
      opacity: 0.65,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // 7. Mouse Movement Handler for Parallax
    let targetX = 0;
    let targetY = 0;
    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
      targetX = x * 0.7;
      targetY = -y * 0.7;
      setMousePos({ x, y });
    };

    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth || 550;
      const h = container.clientHeight || 550;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("resize", handleResize);

    // 8. Animation Render Loop
    let animationFrameId: number;
    let clock = 0;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      clock += 0.016;

      // Core rotation & subtle breathing scale
      coreGroup.rotation.y = clock * 0.25;
      coreGroup.rotation.x = clock * 0.12;
      const scale = 1 + Math.sin(clock * 1.8) * 0.04;
      coreMesh.scale.set(scale, scale, scale);

      // Wireframe counter-rotation
      wireMesh.rotation.y = -clock * 0.35;
      wireMesh.rotation.z = clock * 0.18;

      // Holographic Rings at varied speeds
      ring1.rotation.z = clock * 0.22;
      ring1.rotation.y = Math.sin(clock * 0.3) * 0.2;
      ring2.rotation.z = -clock * 0.28;
      ring2.rotation.x = Math.cos(clock * 0.35) * 0.25;
      ring3.rotation.y = clock * 0.18;

      // Constellation nodes rotation
      nodesGroup.rotation.y = clock * 0.08;
      nodesGroup.rotation.x = Math.sin(clock * 0.05) * 0.1;

      // Particles drift
      particles.rotation.y = clock * 0.04;
      particles.rotation.x = clock * 0.02;

      // Smooth camera parallax interpolation
      camera.position.x += (targetX - camera.position.x) * 0.06;
      camera.position.y += (targetY - camera.position.y) * 0.06;
      camera.lookAt(0, 0, 0);

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("resize", handleResize);
      if (container && renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
      coreGeo.dispose();
      coreMat.dispose();
      wireGeo.dispose();
      wireMat.dispose();
      ringGeo1.dispose();
      ringMat1.dispose();
      ringGeo2.dispose();
      ringMat2.dispose();
      ringGeo3.dispose();
      ringMat3.dispose();
      nodeGeo.dispose();
      nodeMat.dispose();
      particleGeo.dispose();
      particleMat.dispose();
    };
  }, []);

  return (
    <div className="relative w-full h-[460px] sm:h-[540px] lg:h-[600px] flex items-center justify-center select-none">
      {/* 1. Deep Royal-Navy & Violet Ambient Container Glow */}
      <div className="absolute inset-4 rounded-3xl bg-radial from-[#3821A6]/25 via-[#21105A]/15 to-transparent pointer-events-none blur-2xl" />

      {/* 2. Interactive 3D WebGL Canvas */}
      <div
        ref={mountRef}
        className="w-full h-full relative z-10 flex items-center justify-center"
      />

      {/* 3. EXACTLY THREE Floating Glass Cards (Properly Spaced & Readable) */}
      <div className="absolute inset-0 pointer-events-none z-20 flex items-center justify-center">
        {/* CARD 1: Smart Job Matching (Top-Left) */}
        <div
          className="absolute top-4 left-2 sm:left-6 animate-float-slow pointer-events-auto transition-transform duration-300"
          style={{
            transform: `translate(${mousePos.x * -14}px, ${mousePos.y * -14}px)`,
          }}
        >
          <div className="bg-[#10192D]/85 backdrop-blur-2xl border border-[#D6A84B]/40 rounded-2xl p-4 shadow-2xl shadow-[#10192D]/80 max-w-[210px] space-y-1.5 hover:border-[#D6A84B] hover:scale-105 transition-all">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-xl bg-[#D6A84B]/15 border border-[#D6A84B]/35 flex items-center justify-center text-[#D6A84B]">
                <Briefcase className="w-3.5 h-3.5" />
              </div>
              <span className="text-[10px] font-black uppercase tracking-wider text-[#F0D99B]">
                Module 01
              </span>
            </div>
            <h4 className="text-xs font-black text-white leading-tight">
              Smart Job Matching
            </h4>
            <p className="text-[10px] text-[#E6DFD1]/80 leading-relaxed">
              Personalized career discovery matching verified tactile abilities.
            </p>
          </div>
        </div>

        {/* CARD 2: Skill Recognition (Top-Right) */}
        <div
          className="absolute top-10 right-2 sm:right-6 animate-float-medium pointer-events-auto transition-transform duration-300"
          style={{
            transform: `translate(${mousePos.x * 16}px, ${mousePos.y * 16}px)`,
          }}
        >
          <div className="bg-[#10192D]/85 backdrop-blur-2xl border border-[#7355D9]/50 rounded-2xl p-4 shadow-2xl shadow-[#10192D]/80 max-w-[220px] space-y-1.5 hover:border-[#7355D9] hover:scale-105 transition-all">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-xl bg-[#7355D9]/20 border border-[#7355D9]/40 flex items-center justify-center text-[#7355D9]">
                <Sparkles className="w-3.5 h-3.5 text-[#36D6E8]" />
              </div>
              <span className="text-[10px] font-black uppercase tracking-wider text-[#36D6E8]">
                Module 02
              </span>
            </div>
            <h4 className="text-xs font-black text-white leading-tight">
              Skill Recognition
            </h4>
            <p className="text-[10px] text-[#E6DFD1]/80 leading-relaxed">
              Maps everyday informal experience into formal industry taxonomies.
            </p>
          </div>
        </div>

        {/* CARD 3: Career Roadmap (Bottom-Center / Left) */}
        <div
          className="absolute bottom-6 left-4 sm:left-12 animate-float-fast pointer-events-auto transition-transform duration-300"
          style={{
            transform: `translate(${mousePos.x * -12}px, ${mousePos.y * -12}px)`,
          }}
        >
          <div className="bg-[#10192D]/85 backdrop-blur-2xl border border-[#27856B]/50 rounded-2xl p-4 shadow-2xl shadow-[#10192D]/80 max-w-[210px] space-y-1.5 hover:border-[#27856B] hover:scale-105 transition-all">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-xl bg-[#27856B]/20 border border-[#27856B]/40 flex items-center justify-center text-[#27856B]">
                <TrendingUp className="w-3.5 h-3.5 text-[#27856B]" />
              </div>
              <span className="text-[10px] font-black uppercase tracking-wider text-[#DCEAE6]">
                Module 03
              </span>
            </div>
            <h4 className="text-xs font-black text-white leading-tight">
              Career Roadmap
            </h4>
            <p className="text-[10px] text-[#E6DFD1]/80 leading-relaxed">
              Step-by-step verified pathways to higher-wage formal employment.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
