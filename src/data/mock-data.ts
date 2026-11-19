import { 
  UserProfile, 
  RecognizedSkill, 
  JobListing, 
  SkillGapItem, 
  RoadmapMilestone, 
  CareerTransitionPath, 
  AssessmentQuestion, 
  AssessmentResult, 
  InterviewQuestion, 
  MockInterviewSession, 
  JobApplication, 
  PromptEvaluationItem, 
  ResumeData, 
  AssistantMessage 
} from "@/types";

export const defaultUserProfile: UserProfile = {
  id: "user-demo-101",
  fullName: "Ramesh Sharma",
  email: "ramesh.sharma@example.com",
  phone: "+91 98765 43210",
  avatarUrl: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
  role: "user",
  location: "New Delhi, India",
  preferredLanguage: "English",
  ageRange: "28-35",
  educationLevel: "Secondary School (10th Grade)",
  qualifications: [
    "10th Grade Matriculation Certificate (CBSE)",
    "Vocational Apprenticeship in Apparel Stitching (Local Workshop)"
  ],
  currentOccupation: "Master Tailor & Garment Artisan",
  yearsOfExperience: 5,
  workDescription: "I have worked as a custom tailor for five years in Delhi. I take precise client measurements, cut intricate fabric patterns, operate industrial sewing machinery, repair high-end garments, manage fabric inventories, and consult with 30+ daily walk-in customers.",
  desiredSalaryMin: 35000,
  desiredSalaryMax: 55000,
  preferredLocations: ["New Delhi", "Noida", "Gurugram", "Remote"],
  employmentType: "Full-time",
  profileCompleteness: 88,
  skills: [
    {
      id: "sk-1",
      name: "Industrial Sewing Machine Operation",
      category: "Tools & Machinery",
      confidence: 96,
      status: "assessed",
      proficiency: "Advanced",
      evidence: "5 years hands-on daily use of Juki & Brother single-needle lockstitch machines.",
      assessedScore: 92,
      yearsOfPractice: 5
    },
    {
      id: "sk-2",
      name: "Garment Pattern Drafting & Grading",
      category: "Technical",
      confidence: 90,
      status: "assessed",
      proficiency: "Advanced",
      evidence: "Custom drafting for blazers, ethnic wear, and standard apparel sizing.",
      assessedScore: 88,
      yearsOfPractice: 4
    },
    {
      id: "sk-3",
      name: "Apparel Quality Inspection & Finishing",
      category: "Technical",
      confidence: 84,
      status: "ai_inferred",
      proficiency: "Intermediate",
      evidence: "Detects tension defects, seam puckering, and fabric flaws before dispatch.",
      yearsOfPractice: 3
    },
    {
      id: "sk-4",
      name: "Client Consultation & Measurement Taking",
      category: "Transferable",
      confidence: 92,
      status: "self_reported",
      proficiency: "Advanced",
      evidence: "Direct consultation with diverse clientele, managing expectations and bespoke fit.",
      yearsOfPractice: 5
    },
    {
      id: "sk-5",
      name: "Workshop Inventory & Fabric Costing",
      category: "Domain",
      confidence: 78,
      status: "ai_inferred",
      proficiency: "Intermediate",
      evidence: "Calculates yardage needed per garment, minimizes fabric wastage to under 4%.",
      yearsOfPractice: 3
    },
    {
      id: "sk-6",
      name: "Bilingual Communication (Hindi & English)",
      category: "Transferable",
      confidence: 85,
      status: "self_reported",
      proficiency: "Intermediate",
      evidence: "Interacts seamlessly with suppliers, tailors, and urban retail customers.",
      yearsOfPractice: 5
    }
  ]
};

export const mockJobListings: JobListing[] = [
  {
    id: "job-1",
    title: "Apparel Quality Assurance Specialist",
    company: "Raymond Lifestyle Exports",
    location: "Noida / Greater Noida, India",
    salaryRange: "₹40,000 - ₹52,000 / month",
    employmentType: "Full-time",
    experienceLevel: "3-6 years",
    requiredSkills: [
      "Apparel Quality Inspection & Finishing",
      "Industrial Sewing Machine Operation",
      "Garment Pattern Drafting & Grading",
      "Quality Control Checklists",
      "AQL 2.5 Sampling Standards"
    ],
    source: "Verified Apparel Council Portal (Demo)",
    postedDate: "2026-11-08",
    matchScore: 91,
    matchingSkills: [
      "Industrial Sewing Machine Operation",
      "Garment Pattern Drafting & Grading",
      "Apparel Quality Inspection & Finishing",
      "Client Consultation"
    ],
    missingSkills: ["AQL 2.5 Sampling Standards", "Digital Quality ERP Logging"],
    matchExplanation: "High practical compatibility based on your 5-year lockstitch and pattern mastery. Bridging AQL 2.5 standards will make you an exceptional fit.",
    description: "Raymond Lifestyle is looking for an experienced Quality Assurance Specialist to oversee garment finishing, seam integrity, and export specifications across our premium shirting lines.",
    responsibilities: [
      "Inspect finished apparel units for stitch balance, seam puckering, and dimensional tolerance.",
      "Liaise between floor tailors and production managers to rectify recurring fabrication errors.",
      "Conduct final packaging reviews in alignment with international export regulations.",
      "Log pass/fail metrics into factory tablets and report variance summaries."
    ],
    qualifications: [
      "Minimum 3+ years hands-on tailoring, garment manufacturing, or quality inspection experience.",
      "Proficient understanding of woven fabrics, grain lines, and sewing machine mechanics.",
      "Vocational training or practical trade experience recognized by Elevate X AI skill badge."
    ],
    benefits: [
      "Provident Fund (PF) & ESI Health Coverage",
      "Subsidized factory cafeteria & transit shuttle",
      "Skill upgrade certifications sponsored by company",
      "Annual performance bonus"
    ],
    employerInfo: {
      name: "Raymond Lifestyle Exports",
      about: "A leading fabric and apparel enterprise delivering world-class suiting and apparel across 55 countries.",
      size: "2,500+ employees",
      industry: "Textiles & Fashion Manufacturing"
    }
  },
  {
    id: "job-2",
    title: "Production Assistant - Garment Sampling",
    company: "FabIndia Overseas Pvt Ltd",
    location: "Okhla Phase III, New Delhi",
    salaryRange: "₹36,000 - ₹48,000 / month",
    employmentType: "Full-time",
    experienceLevel: "2-5 years",
    requiredSkills: [
      "Garment Pattern Drafting & Grading",
      "Industrial Sewing Machine Operation",
      "Fabric Costing & Consumption",
      "Sample Prototyping"
    ],
    source: "Craft & Textile Hub (Demo)",
    postedDate: "2026-11-10",
    matchScore: 88,
    matchingSkills: [
      "Garment Pattern Drafting & Grading",
      "Industrial Sewing Machine Operation",
      "Fabric Costing & Consumption"
    ],
    missingSkills: ["CAD Pattern Digitization (Optitex/Gerber)"],
    matchExplanation: "Exceptional alignment with sample crafting and artisan supervision. Your bespoke fitting background is highly prized for prototype validation.",
    description: "Join FabIndia's creative sample unit to translate artisan sketches into production-ready sample garments. You will work directly with master designers.",
    responsibilities: [
      "Cut and assemble first-stage design prototypes using ethnic handloom textiles.",
      "Evaluate garment drape, ease allowances, and seam allowances.",
      "Recommend fabrication adjustments to optimize assembly line efficiency.",
      "Maintain fabric swatches and trim inventories."
    ],
    qualifications: [
      "Strong background in custom tailoring, sample making, or boutique alterations.",
      "Ability to interpret technical sketches and measurement spec sheets.",
      "High attention to detail with intricate trims and embroideries."
    ],
    benefits: [
      "Health insurance for self and family",
      "Staff merchandise discount (30%)",
      "5-day work week in creative design studio"
    ],
    employerInfo: {
      name: "FabIndia Overseas",
      about: "India's premier artisanal lifestyle brand working with over 55,000 rural craftspersons.",
      size: "4,000+ employees",
      industry: "Retail & Apparel"
    }
  },
  {
    id: "job-3",
    title: "Bespoke Master Tailor & Alteration Lead",
    company: "The Raymond Custom Shop",
    location: "Khan Market, New Delhi",
    salaryRange: "₹45,000 - ₹60,000 / month",
    employmentType: "Full-time",
    experienceLevel: "4+ years",
    requiredSkills: [
      "Client Consultation & Measurement Taking",
      "Garment Pattern Drafting & Grading",
      "Hand Finishing & Lapel Shaping",
      "Bespoke Fitting Problem-Solving"
    ],
    source: "Retail Craft Guild (Demo)",
    postedDate: "2026-11-11",
    matchScore: 95,
    matchingSkills: [
      "Client Consultation & Measurement Taking",
      "Garment Pattern Drafting & Grading",
      "Industrial Sewing Machine Operation",
      "Bilingual Communication"
    ],
    missingSkills: ["Luxury POS Billing"],
    matchExplanation: "Near perfect match! Your direct client consultation experience and custom tailoring expertise align directly with premium showroom requirements.",
    description: "Manage client fittings for custom suits, sherwanis, and luxury formalwear. Lead a team of two bench tailors to deliver immaculate bespoke results.",
    responsibilities: [
      "Conduct in-depth measurement sessions with executive clientele.",
      "Advise on collar styles, lapel proportions, fabric weights, and linings.",
      "Perform intermediate basting fittings and pin alterations.",
      "Ensure turnaround times meet client delivery commitments."
    ],
    qualifications: [
      "Proven track record in bespoke tailoring or high-end alterations.",
      "Poised verbal communication and warm customer service demeanour.",
      "Elevate X AI verified skill report."
    ],
    benefits: [
      "Attractive monthly sales incentive scheme",
      "Medical insurance coverage",
      "Air-conditioned retail showroom environment"
    ],
    employerInfo: {
      name: "The Raymond Custom Shop",
      about: "Exclusive bespoke atelier delivering personalized suiting and luxury menswear.",
      size: "500+ across retail",
      industry: "Luxury Menswear"
    }
  },
  {
    id: "job-4",
    title: "Technical Sewing Instructor / Trainer",
    company: "National Skill Development Partner Institute",
    location: "Gurugram, Haryana",
    salaryRange: "₹38,000 - ₹50,000 / month",
    employmentType: "Full-time",
    experienceLevel: "3+ years",
    requiredSkills: [
      "Industrial Sewing Machine Operation",
      "Curriculum Demonstration",
      "Student Mentorship",
      "Workshop Safety Protocols"
    ],
    source: "Vocational Trainers Portal (Demo)",
    postedDate: "2026-11-05",
    matchScore: 82,
    matchingSkills: [
      "Industrial Sewing Machine Operation",
      "Client Consultation & Measurement Taking",
      "Garment Pattern Drafting & Grading"
    ],
    missingSkills: ["Basic Lesson Planning", "Vocational Assessment Rubrics"],
    matchExplanation: "Your deep hands-on mastery allows you to train next-generation apprentices. Elevate X AI provides the quick pedagogy roadmap to qualify.",
    description: "Train aspiring youth in vocational garment manufacturing, operating lockstitch/overlock machinery, and understanding industrial safety standards.",
    responsibilities: [
      "Conduct hands-on machinery demonstrations for batches of 15 students.",
      "Grade apprentice stitching samples for stitch density and tension.",
      "Maintain machinery lubrication and safety guards.",
      "Foster confidence in students entering the formal garment industry."
    ],
    qualifications: [
      "Minimum 3 years practical experience as a tailor or machine operator.",
      "Patience and clear verbal communication in Hindi and conversational English.",
      "Enthusiasm for uplifting youth from underprivileged backgrounds."
    ],
    benefits: [
      "Fixed government institute holidays & calendar leaves",
      "Subsidized accommodation allowance",
      "Train-the-Trainer certification pathway"
    ],
    employerInfo: {
      name: "Vocational Skills Institute",
      about: "Empowering 100,000+ candidates through skill certifications and dignified livelihood opportunities.",
      size: "800+ staff",
      industry: "Education & Skilling"
    }
  }
];

export const mockSkillGaps: SkillGapItem[] = [
  {
    id: "gap-1",
    skillName: "AQL 2.5 Quality Sampling Protocols",
    category: "Technical Standards",
    currentLevel: "None",
    requiredLevel: "Intermediate",
    importance: "High",
    gapScore: 75,
    learningRecommendation: "Master Acceptable Quality Limit (AQL 2.5) sampling tables used by global apparel brands to check lot acceptance.",
    recommendedResource: {
      title: "Practical AQL 2.5 for Garment Inspectors",
      type: "Interactive Guide",
      duration: "3 hours",
      isFree: true
    }
  },
  {
    id: "gap-2",
    skillName: "Digital Quality ERP Logging (Tablet Interface)",
    category: "Digital Tools",
    currentLevel: "Beginner",
    requiredLevel: "Intermediate",
    importance: "High",
    gapScore: 60,
    learningRecommendation: "Learn how to record seam defects, upload photos of sewing flaws, and submit batch pass/fail reports on Android tablets.",
    recommendedResource: {
      title: "Factory Tablet Defect Logging Simulation",
      type: "Hands-on Project",
      duration: "2 hours",
      isFree: true
    }
  },
  {
    id: "gap-3",
    skillName: "Computer-Aided Pattern Drafting Basics (CAD)",
    category: "Software & Digital Design",
    currentLevel: "None",
    requiredLevel: "Beginner",
    importance: "Medium",
    gapScore: 50,
    learningRecommendation: "Bridge from manual cardboard pattern drafting to digital pattern adjustments using open-source tools like Seamly2D.",
    recommendedResource: {
      title: "From Paper to Screen: Digital Pattern Basics",
      type: "Video",
      duration: "4 hours",
      isFree: true
    }
  },
  {
    id: "gap-4",
    skillName: "Industrial Workshop Safety & 5S Principles",
    category: "Operations",
    currentLevel: "Intermediate",
    requiredLevel: "Advanced",
    importance: "Medium",
    gapScore: 35,
    learningRecommendation: "Adopt formal 5S workshop organization (Sort, Set in order, Shine, Standardize, Sustain) for supervisory roles.",
    recommendedResource: {
      title: "5S in Apparel Manufacturing Floor Management",
      type: "Vocational Workshop",
      duration: "1.5 hours",
      isFree: true
    }
  }
];

export const mockRoadmapMilestones: RoadmapMilestone[] = [
  {
    id: "stage-1",
    stageNumber: 1,
    title: "Foundational Quality Inspection & Defect Taxonomy",
    timeEstimate: "Week 1 - 2",
    status: "completed",
    description: "Formalize your intuitive garment inspection skills into standardized terminology (broken stitches, skip stitch, wavy seam, shading).",
    skillsToAcquire: [
      "Stitch Defect Identification",
      "Fabric Grain Alignment Inspection",
      "Measurement Spec Sheet Reading"
    ],
    practicalTasks: [
      "Inspect 20 garments using a standard 10-point checklist.",
      "Log discrepancies on the Elevate X practice defect sheet.",
      "Take the 15-minute diagnostic assessment."
    ],
    resources: [
      {
        name: "Standard Garment Defect Visual Guide (PDF)",
        type: "Illustrated Cheatsheet",
        duration: "45 mins",
        free: true
      },
      {
        name: "Practical Measurement Tolerance Workshop",
        type: "Interactive Video",
        duration: "1 hr 15 mins",
        free: true
      }
    ]
  },
  {
    id: "stage-2",
    stageNumber: 2,
    title: "AQL 2.5 International Export Sampling Mastery",
    timeEstimate: "Week 3 - 4",
    status: "in_progress",
    description: "Learn how export houses use mathematical random sampling tables to accept or reject carton shipments.",
    skillsToAcquire: [
      "AQL Table Reading (Normal Level II)",
      "Batch Defect Counting",
      "Minor vs Major Defect Classification"
    ],
    practicalTasks: [
      "Run sample calculations for a 1,200-piece shirting order.",
      "Complete the interactive simulation test on Elevate X AI.",
      "Earn the Elevate X 'AQL Certified Inspector' platform badge."
    ],
    resources: [
      {
        name: "Interactive AQL 2.5 Simulator Tool",
        type: "Web Application Exercise",
        duration: "2 hours",
        free: true
      },
      {
        name: "Apparel Export Standards Masterclass",
        type: "Self-paced Video Course",
        duration: "3 hours",
        free: true
      }
    ]
  },
  {
    id: "stage-3",
    stageNumber: 3,
    title: "Digital Factory Tools & Floor Communication",
    timeEstimate: "Week 5 - 6",
    status: "upcoming",
    description: "Transition from paper registers to digital tablet QA entry and learn professional team handover communication.",
    skillsToAcquire: [
      "Tablet QA Data Entry",
      "Shift Handover Briefings",
      "Conflict Resolution with Line Operators"
    ],
    practicalTasks: [
      "Complete 5 simulated tablet shift reports.",
      "Practice mock supervisor voice briefings in Hindi and English.",
      "Shadow an online factory floor tour."
    ],
    resources: [
      {
        name: "Digital Quality App Practice Sandbox",
        type: "Interactive Lab",
        duration: "1.5 hours",
        free: true
      },
      {
        name: "Effective Floor Leadership for Former Artisans",
        type: "Audio Guide",
        duration: "1 hour",
        free: true
      }
    ]
  },
  {
    id: "stage-4",
    stageNumber: 4,
    title: "Mock Interview & Verified Application Deployment",
    timeEstimate: "Week 7 - 8",
    status: "upcoming",
    description: "Polish your verified resume, practice technical and situational interview questions with the AI Interview Lab, and submit applications.",
    skillsToAcquire: [
      "Technical Interview Self-Introduction",
      "Salary Negotiation for Formal Sector",
      "Work Sample Portfolio Presentation"
    ],
    practicalTasks: [
      "Complete 3 AI mock interview sessions with 85%+ score.",
      "Download ATS-optimized resume emphasizing verified skills.",
      "Apply to 4 curated partner export companies with direct referral."
    ],
    resources: [
      {
        name: "Elevate X AI Interview Simulator (QA Specialist)",
        type: "Interactive AI Lab",
        duration: "30 mins / session",
        free: true
      },
      {
        name: "First 90 Days Success Guide in Formal Apparel Manufacturing",
        type: "Handbook",
        duration: "1 hour",
        free: true
      }
    ]
  }
];

export const mockCareerTransitions: CareerTransitionPath[] = [
  {
    id: "path-1",
    targetRole: "Apparel Quality Assurance Specialist",
    industry: "Garment Manufacturing & Exports",
    suitabilityScore: 92,
    transitionDifficulty: "Low",
    averageSalaryIncrease: "+35% to +60%",
    transferableSkills: [
      "Stitch defect identification",
      "Lockstitch machine operation",
      "Measurement spec precision",
      "Fabric grain & tension awareness"
    ],
    skillsToAcquire: [
      "AQL 2.5 Sampling protocols",
      "Digital quality tablet entry",
      "Line inspection report documentation"
    ],
    bridgeSteps: [
      "Take Elevate X AI AQL 2.5 diagnostic assessment (15 mins).",
      "Generate verified skill credentials.",
      "Apply to partner garment export houses in NCR and Tirupur."
    ],
    demandLevel: "Very High"
  },
  {
    id: "path-2",
    targetRole: "Production Sampling Supervisor",
    industry: "Fashion Boutiques & Design Studios",
    suitabilityScore: 86,
    transitionDifficulty: "Moderate",
    averageSalaryIncrease: "+40% to +75%",
    transferableSkills: [
      "Pattern drafting & grading",
      "Bespoke garment fitting",
      "Fabric yield calculation & wastage reduction",
      "Customer communication"
    ],
    skillsToAcquire: [
      "Design spec-sheet software (Techpack interpretation)",
      "Basic inventory software",
      "Production timeline scheduling"
    ],
    bridgeSteps: [
      "Build visual portfolio of 5 completed garments.",
      "Practice techpack translation exercises on Elevate X AI.",
      "Connect with export boutique recruitment leads."
    ],
    demandLevel: "High"
  },
  {
    id: "path-3",
    targetRole: "Vocational Garment Sewing Trainer",
    industry: "Skill Development & Training Institutes",
    suitabilityScore: 81,
    transitionDifficulty: "Moderate",
    averageSalaryIncrease: "+25% to +45% (with fixed hours)",
    transferableSkills: [
      "Patient demonstration of lockstitch machines",
      "Garment construction troubleshooting",
      "Bilingual explanation (Hindi & English)"
    ],
    skillsToAcquire: [
      "Lesson plan structuring",
      "Vocational assessment grading",
      "Workshop safety compliance protocols"
    ],
    bridgeSteps: [
      "Complete the 2-week Elevate X Train-the-Trainer module.",
      "Obtain platform pedagogical readiness badge.",
      "Interview with NSDC partner skilling centers."
    ],
    demandLevel: "Growing"
  },
  {
    id: "path-4",
    targetRole: "Formal Alteration Specialist for Luxury Retail",
    industry: "Premium Fashion & Departmental Stores",
    suitabilityScore: 94,
    transitionDifficulty: "Low",
    averageSalaryIncrease: "+30% to +50% (plus store incentives)",
    transferableSkills: [
      "Bespoke measuring & pinning",
      "Hand finishing & blind hemming",
      "Direct customer rapport building",
      "High attention to luxury fabric drape"
    ],
    skillsToAcquire: [
      "Point-of-Sale (POS) ticket creation",
      "Standard store service protocols"
    ],
    bridgeSteps: [
      "Record mock client fitting demonstration on Elevate X AI.",
      "Export customer-focused retail resume.",
      "Apply to premium brand stores."
    ],
    demandLevel: "High"
  }
];

export const mockAssessmentQuestions: AssessmentQuestion[] = [
  {
    id: "q-1",
    questionNumber: 1,
    type: "scenario",
    skillEvaluated: "Industrial Sewing Machine Operation",
    scenarioContext: "You are stitching a high-density cotton twill trouser on a high-speed single-needle lockstitch machine. The machine suddenly begins skipping stitches when passing over a double-folded flat-felled seam.",
    questionText: "What is the most probable technical cause and the immediate corrective action?",
    options: [
      {
        id: "opt-a",
        text: "The bobbin case is completely out of thread; reload a new bobbin."
      },
      {
        id: "opt-b",
        text: "The needle is slightly deflected or blunt; replace with a reinforced-shank needle and verify needle-to-rotary-hook timing clearance."
      },
      {
        id: "opt-c",
        text: "Increase machine operating speed to 4,500 RPM to puncture through the thicker seam."
      },
      {
        id: "opt-d",
        text: "Loosen the presser foot pressure completely to let the fabric slide freely."
      }
    ],
    correctOptionId: "opt-b",
    explanation: "Skipping stitches over thick intersections is classically caused by needle deflection where the hook point misses the needle thread loop. Using a fresh, heavier-gauge or reinforced needle and inspecting hook timing solves this without damaging the fabric."
  },
  {
    id: "q-2",
    questionNumber: 2,
    type: "multiple_choice",
    skillEvaluated: "Apparel Quality Inspection & Finishing",
    questionText: "In international export standards, what does an 'AQL 2.5' sampling standard signify for a batch inspection?",
    options: [
      {
        id: "opt-a",
        text: "Exactly 2.5% of every carton must be discarded automatically before packing."
      },
      {
        id: "opt-b",
        text: "A statistical threshold where the process average is considered acceptable if major defects do not exceed the lot size's specific AQL 2.5 acceptance number."
      },
      {
        id: "opt-c",
        text: "The factory is penalized 2.5% of the invoice value for any minor loose threads detected."
      },
      {
        id: "opt-d",
        text: "The inspector tests 2.5 shirts per hour regardless of shipment quantity."
      }
    ],
    correctOptionId: "opt-b",
    explanation: "AQL (Acceptable Quality Limit) 2.5 designates the maximum percent defective (or maximum number of defects per hundred units) that, for the purpose of sampling inspection, can be considered satisfactory as a process average."
  },
  {
    id: "q-3",
    questionNumber: 3,
    type: "practical",
    skillEvaluated: "Garment Pattern Drafting & Grading",
    scenarioContext: "A client reports that when raising their arms, the entire body of their button-up tailored shirt pulls up uncomfortably out of their waistband.",
    questionText: "Which pattern modification should be executed to correct this armhole mobility flaw?",
    options: [
      {
        id: "opt-a",
        text: "Enlarge the chest circumference by 6 inches without altering the armscye."
      },
      {
        id: "opt-b",
        text: "Raise the lower armhole curve (reduce armscye depth) and lengthen the sleeve cap ease allowance to increase mobility."
      },
      {
        id: "opt-c",
        text: "Shorten the shirt hem length so there is less fabric to pull."
      },
      {
        id: "opt-d",
        text: "Increase shoulder slope padding by 1.5 inches."
      }
    ],
    correctOptionId: "opt-b",
    explanation: "A common misconception is that a lower, deeper armhole gives more room. In reality, a lower armhole pulls the side seam immediately when the arm is lifted. A higher, closer-fitting armscye allows the arm to rotate independently."
  },
  {
    id: "q-4",
    questionNumber: 4,
    type: "scenario",
    skillEvaluated: "Client Consultation & Communication",
    scenarioContext: "An upset customer arrives at your studio complaining that their custom suit jacket sleeve is 0.75 inches longer than agreed for tomorrow's wedding event.",
    questionText: "How should a professional career artisan handle this interaction?",
    options: [
      {
        id: "opt-a",
        text: "Argue that 0.75 inches is within standard tailoring variation and refuse the alteration."
      },
      {
        id: "opt-b",
        text: "Acknowledge the customer's distress calmly, inspect the sleeve with them in front of the mirror, measure the exact cuff distance from the shirt cuff, and commit to an expedited 2-hour correction."
      },
      {
        id: "opt-c",
        text: "Offer an immediate 50% cash refund and ask them to find another tailor nearby."
      },
      {
        id: "opt-d",
        text: "Blame the cutting assistant for misinterpreting the order notebook."
      }
    ],
    correctOptionId: "opt-b",
    explanation: "Effective customer relationship management in craftsmanship combines active listening, mirror verification, de-escalation, and confident technical remedy without shifting blame."
  }
];

export const mockAssessmentResults: AssessmentResult[] = [
  {
    id: "res-1",
    skillName: "Industrial Sewing Machine Operation",
    dateCompleted: "2026-11-09",
    score: 92,
    totalQuestions: 15,
    correctAnswers: 14,
    timeSpentMinutes: 12,
    strengths: [
      "Mastery of rotary hook timing and needle clearance troubleshooting",
      "Exceptional thread tension balance across woven and knit fabrics",
      "Preventive machine maintenance knowledge (lubrication, feed dog height)"
    ],
    areasToImprove: [
      "Automated programmable CNC pocket stitcher error codes"
    ],
    nextSteps: [
      "Add verified score badge to your public profile",
      "Proceed to AQL 2.5 Quality Inspection assessment"
    ],
    status: "passed",
    indicativeLevel: "Advanced"
  },
  {
    id: "res-2",
    skillName: "Garment Pattern Drafting & Grading",
    dateCompleted: "2026-11-04",
    score: 88,
    totalQuestions: 12,
    correctAnswers: 11,
    timeSpentMinutes: 14,
    strengths: [
      "Accurate armscye depth and sleeve cap geometry calculation",
      "Grainline balance on checked and striped fabrics",
      "Body shape adjustments (stooping posture, prominent shoulder blade)"
    ],
    areasToImprove: [
      "Grading nested sizes using digital coordinates"
    ],
    nextSteps: [
      "Practice Seamly2D digital pattern drafting tutorial",
      "Review sample techpack exercise"
    ],
    status: "passed",
    indicativeLevel: "Advanced"
  }
];

export const mockInterviewQuestions: InterviewQuestion[] = [
  {
    id: "iq-1",
    role: "Apparel Quality Assurance Specialist",
    category: "Experience",
    question: "Walk me through how you detect subtle sewing defects, such as seam slippage or puckering, when reviewing a finished batch of formal shirts.",
    sampleAnswer: "In my 5 years on the shop floor, I test seam slippage by applying moderate fingertip lateral pull along high-stress points like the armhole seam and back yoke. For seam puckering, I lay the garment flat under angled inspection lighting to differentiate between structural feed puckering (mismatched feed dog tension) and shrinkage puckering caused by excessive thread tension. I inspect stitch balance on both face and underside to ensure the lock knot rests precisely within the fabric core.",
    evaluationCriteria: [
      "Demonstrates tactile, practical testing method",
      "Uses correct technical vocabulary (feed dog tension, stitch knot placement)",
      "Explains cause and diagnosis rather than just observing"
    ]
  },
  {
    id: "iq-2",
    role: "Apparel Quality Assurance Specialist",
    category: "Situational",
    question: "If an assembly line operator with 10 years of seniority gets defensive when you reject their batch for measurement variation, how do you resolve the situation?",
    sampleAnswer: "I never approach quality rejections as a personal critique. I bring the original approved spec sheet and sample garment to the operator's workbench. I ask them to measure the critical dimension together with me so we both agree on the 0.5-inch deviation. Then, I check if their machine folder or presser foot is drifting. By diagnosing the machine root cause alongside them, I respect their seniority while upholding our zero-defect export standard.",
    evaluationCriteria: [
      "Emotional intelligence and de-escalation",
      "Reliance on objective benchmarks (spec sheets)",
      "Collaborative root-cause mindset"
    ]
  },
  {
    id: "iq-3",
    role: "Apparel Quality Assurance Specialist",
    category: "Technical",
    question: "What steps would you take if a lot of 500 garments shows 8 major defects during an AQL 2.5 General Inspection Level II check?",
    sampleAnswer: "For a lot size of 500 under General Inspection Level II, Sample Size Code Letter is H, corresponding to a sample size of 50 garments. Under AQL 2.5, the Accept/Reject criteria are Accept = 3, Reject = 4. Since 8 major defects were found, the lot clearly fails the sampling plan. I would immediately stop carton packing, issue an internal Non-Conformance Report (NCR), notify the production manager, and mandate 100% sorting and rework for that specific flaw before any re-inspection.",
    evaluationCriteria: [
      "Correct AQL table recall or procedural logic",
      "Decisive action: halting dispatch, issuing NCR",
      "Mandating 100% screening before re-audit"
    ]
  }
];

export const mockInterviewSessions: MockInterviewSession[] = [
  {
    id: "int-session-1",
    targetJob: "Apparel Quality Assurance Specialist",
    date: "2026-11-10",
    overallScore: 88,
    relevanceScore: 92,
    communicationScore: 84,
    strengths: [
      "Outstanding practical depth when explaining sewing defects",
      "Calm, respectful demeanor in de-escalation scenarios",
      "Clear explanation of seam mechanics"
    ],
    growthAreas: [
      "Speak with more confidence when citing numerical AQL limits",
      "Slightly reduce pauses before technical definitions"
    ],
    feedbackNotes: "Candidate displays strong shop-floor credibility. Communicates real-world experience vividly. Recommended for senior QA and supervisory rounds."
  }
];

export const mockApplications: JobApplication[] = [
  {
    id: "app-1",
    jobId: "job-1",
    jobTitle: "Apparel Quality Assurance Specialist",
    company: "Raymond Lifestyle Exports",
    location: "Noida / Greater Noida",
    salary: "₹40,000 - ₹52,000 / month",
    status: "interview",
    appliedDate: "2026-11-09",
    lastUpdated: "2026-11-11",
    matchScore: 91,
    notes: "Technical interview scheduled for Nov 16 at 2:30 PM with Plant Head."
  },
  {
    id: "app-2",
    jobId: "job-3",
    jobTitle: "Bespoke Master Tailor & Alteration Lead",
    company: "The Raymond Custom Shop",
    location: "Khan Market, New Delhi",
    salary: "₹45,000 - ₹60,000 / month",
    status: "applied",
    appliedDate: "2026-11-10",
    lastUpdated: "2026-11-10",
    matchScore: 95,
    notes: "Application submitted with Elevate X verified skills portfolio."
  },
  {
    id: "app-3",
    jobId: "job-2",
    jobTitle: "Production Assistant - Garment Sampling",
    company: "FabIndia Overseas Pvt Ltd",
    location: "Okhla Phase III, New Delhi",
    salary: "₹36,000 - ₹48,000 / month",
    status: "saved",
    appliedDate: "—",
    lastUpdated: "2026-11-11",
    matchScore: 88,
    notes: "Reviewing CAD requirements before submitting."
  },
  {
    id: "app-4",
    jobId: "job-4",
    jobTitle: "Technical Sewing Instructor / Trainer",
    company: "Vocational Skills Institute",
    location: "Gurugram, Haryana",
    salary: "₹38,000 - ₹50,000 / month",
    status: "shortlisted",
    appliedDate: "2026-11-05",
    lastUpdated: "2026-11-12",
    matchScore: 82,
    notes: "HR requested sample demonstration video of lockstitch threading."
  }
];

export const defaultResumeData: ResumeData = {
  fullName: "Ramesh Sharma",
  email: "ramesh.sharma@example.com",
  phone: "+91 98765 43210",
  location: "New Delhi, India",
  headline: "Senior Garment Artisan & Quality Assurance Specialist",
  summary: "Results-driven craftsperson and apparel specialist with 5+ years of hands-on expertise in industrial sewing machinery, bespoke pattern drafting, and precision quality control. Proven track record in garment construction, defect minimization, and client relationship management. Certified by Elevate X AI with advanced scores in stitch mechanics and measurement accuracy.",
  experience: [
    {
      id: "exp-1",
      role: "Lead Master Tailor & Workshop Supervisor",
      organization: "Sharma Tailoring Studio (Custom Atelier)",
      period: "2021 - Present (4 Years)",
      highlights: [
        "Crafted over 1,200 bespoke suits, ethnic garments, and formal shirts with a 98% first-fitting satisfaction rate.",
        "Supervised and trained 3 junior apprentices in single-needle lockstitch maintenance, seam balancing, and pressing.",
        "Managed client consultations and individual measurements for 30+ weekly walk-in clients.",
        "Reduced fabric cutting wastage by 6.5% through optimized pattern marker layout."
      ]
    },
    {
      id: "exp-2",
      role: "Apparel Stitching & Alteration Technician",
      organization: "Laxmi Garments & Alterations Hub",
      period: "2019 - 2021 (2 Years)",
      highlights: [
        "Executed high-speed garment alterations, zipper replacements, and sleeve adjustments under tight turnaround schedules.",
        "Conducted final quality inspection on 50+ altered units daily, checking seam integrity and press finish."
      ]
    }
  ],
  education: [
    {
      id: "edu-1",
      degree: "Secondary School Examination (Class X)",
      institution: "Delhi Government Senior Secondary School",
      year: "2018"
    },
    {
      id: "edu-2",
      degree: "Vocational Certificate in Industrial Sewing & Garment Fabrication",
      institution: "Elevate X AI Verified Skill Program",
      year: "2026"
    }
  ],
  skills: {
    technical: [
      "Industrial Sewing Machine Operation (Juki/Brother)",
      "Garment Pattern Drafting & Grading",
      "Apparel Quality Inspection & AQL Standards",
      "Fabric Grain & Drape Analysis",
      "Seam Defect Troubleshooting"
    ],
    transferable: [
      "Client Relationship Consultation",
      "Team Supervision & Apprentice Training",
      "Bilingual Communication (Hindi, English)",
      "Attention to Detail & Punctuality"
    ],
    tools: [
      "Single-needle Lockstitch",
      "Overlock (4-thread / 5-thread)",
      "Steam Press & Iron Stations",
      "Tailor's L-Square & French Curves"
    ]
  },
  certifications: [
    "Elevate X AI Verified: Industrial Sewing Machine Specialist (Score: 92/100)",
    "Elevate X AI Verified: Garment Pattern Drafting Mastery (Score: 88/100)",
    "Apparel Guild Practical Quality Inspection Credential"
  ],
  projects: [
    {
      id: "proj-1",
      name: "Zero-Waste Bridal Fabric Optimization",
      description: "Restructured traditional lehenga pattern pieces to decrease scrap fabric by 14%, saving the studio ₹45,000 in material costs annually."
    }
  ],
  template: "modern"
};

export const mockPromptEvaluations: PromptEvaluationItem[] = [
  {
    id: "prompt-1",
    name: "Informal Experience Skill Extraction Engine",
    category: "Skill Extraction",
    technique: "Structured JSON",
    version: "v3.2",
    status: "Production",
    systemPrompt: `You are Elevate X AI's Senior Occupational Taxonomist.
Given informal, conversational worker narratives (often spoken with colloquialisms, local vocabulary, and non-academic phrasings), your task is to extract:
1. Technical skills (tied to machinery, materials, tools, protocols).
2. Transferable skills (communication, problem-solving, team coordination).
3. Verifiable evidence extracted strictly from the user's direct testimony.
4. Confidence score (0-100) reflecting factual certainty.
Strictly return a valid JSON object matching the SkillExtractionSchema. Do not hallucinate credentials the worker never mentioned.`,
    userPromptTemplate: `Worker Narrative: {raw_narrative}
Context: {worker_location}, {years_reported} years experience.
Extract skills into valid JSON.`,
    testInput: `"Maine pichle 5 saal se Chandni Chowk me tailoring ki dukaan chalayi hai. Roz Juki lockstitch machine pe sherwani aur blazers silta hoon, grahako ka naap leta hoon aur kapda bachane ke liye pattern banata hoon."`,
    baselineOutput: `{"skills": ["tailoring", "machine use", "talking to clients", "saving cloth"]}`,
    improvedOutput: `{
  "occupation": "Master Tailor & Garment Artisan",
  "technical_skills": [
    {
      "name": "Industrial Lockstitch Machine Operation (Juki)",
      "category": "Tools & Machinery",
      "confidence": 98,
      "evidence": "Stated 5 years daily operation of Juki lockstitch machine on sherwanis and blazers."
    },
    {
      "name": "Pattern Drafting & Marker Optimization",
      "category": "Technical",
      "confidence": 92,
      "evidence": "Creates custom patterns and minimizes fabric consumption."
    }
  ],
  "transferable_skills": [
    {
      "name": "Direct Client Measurement & Consultation",
      "category": "Transferable",
      "confidence": 90,
      "evidence": "Measures customer dimensions directly for bespoke fittings."
    }
  ],
  "unverified_claims": []
}`,
    metrics: {
      extractionAccuracy: 96,
      evidenceValidation: 95,
      jobRelevance: 94,
      factuality: 98,
      jsonValidity: 100,
      latencyMs: 380
    },
    baselineMetrics: {
      extractionAccuracy: 68,
      evidenceValidation: 52,
      jobRelevance: 60,
      factuality: 74,
      jsonValidity: 82,
      latencyMs: 510
    }
  },
  {
    id: "prompt-2",
    name: "Explainable Career Transition Matcher",
    category: "Job Matching",
    technique: "RAG-Grounded",
    version: "v2.8",
    status: "Production",
    systemPrompt: `You are Elevate X AI's Occupational Mobility Advisor. Ground all job match rationales strictly in verified occupational standards (O*NET and NSDC National Skills Qualification Framework).
Never guarantee employment or invent job requirements.
Differentiate between:
- Directly transferable skills (immediate plug-and-play).
- Adjacent skills (bridgeable in under 30 days).
- Hard barriers (licensing, regulatory mandates).`,
    userPromptTemplate: `Candidate Verified Profile: {verified_skills_json}
Target Job: {job_spec_json}
Analyze compatibility with transparent gap identification.`,
    testInput: `Candidate: Tailor with 5 yrs lockstitch & quality inspection experience. Target: Apparel Quality Assurance Specialist (Raymond Lifestyle).`,
    baselineOutput: `Match: 85%. You know how to stitch and inspect clothes so you can do this job easily.`,
    improvedOutput: `{
  "match_score": 91,
  "transferable_matches": [
    "Industrial single-needle stitch mechanics",
    "Measurement spec tolerance checking",
    "Fabric defect troubleshooting"
  ],
  "skill_gaps": [
    {
      "skill": "AQL 2.5 Statistical Sampling Tables",
      "severity": "Medium",
      "bridge_time": "1-2 weeks through Elevate X interactive module"
    },
    {
      "skill": "Tablet ERP QA Logging",
      "severity": "Low",
      "bridge_time": "3 days practice sandbox"
    }
  ],
  "disclaimer": "Indicative compatibility index based on skill overlap; does not guarantee hiring selection."
}`,
    metrics: {
      extractionAccuracy: 94,
      evidenceValidation: 97,
      jobRelevance: 96,
      factuality: 99,
      jsonValidity: 100,
      latencyMs: 420
    },
    baselineMetrics: {
      extractionAccuracy: 64,
      evidenceValidation: 58,
      jobRelevance: 72,
      factuality: 70,
      jsonValidity: 85,
      latencyMs: 640
    }
  },
  {
    id: "prompt-3",
    name: "Resume Factuality Guardrail Prompter",
    category: "Resume Enhancement",
    technique: "Guardrail",
    version: "v4.0",
    status: "Production",
    systemPrompt: `CRITICAL SAFETY GUARDRAIL:
You are an uncompromising Factuality Auditor for AI Resumes.
1. NEVER fabricate degrees, diplomas, or trade credentials not present in the user input.
2. Translate informal duties into professional, high-impact action verbs without exaggerating numbers or scopes.
3. If metric proof is missing, suggest a placeholder prompt to the user instead of inventing arbitrary percentages.`,
    userPromptTemplate: `Input Raw Job Description: {job_text}
Draft professional resume bullets with strict factuality adherence.`,
    testInput: `"Main dukaan pe akele hi kapda kaatta tha aur grahak se baat karta tha."`,
    baselineOutput: `"Led a high-performing international sales division generating $2,000,000 in revenue with 99% customer growth." (HALLUCINATION)`,
    improvedOutput: `[
  "Managed complete end-to-end custom apparel cutting and tailoring operations independently in a fast-paced retail workshop.",
  "Served as primary client liaison, translating bespoke customer design preferences and sizing requirements into finished garments."
]`,
    metrics: {
      extractionAccuracy: 98,
      evidenceValidation: 99,
      jobRelevance: 95,
      factuality: 100,
      jsonValidity: 100,
      latencyMs: 290
    },
    baselineMetrics: {
      extractionAccuracy: 55,
      evidenceValidation: 40,
      jobRelevance: 50,
      factuality: 42,
      jsonValidity: 90,
      latencyMs: 450
    }
  },
  {
    id: "prompt-4",
    name: "Bilingual Context-Aware AI Career Assistant",
    category: "Roadmap Generation",
    technique: "Context-Aware",
    version: "v2.1",
    status: "Production",
    systemPrompt: `You are Elevate X AI's Multilingual Career Mentor.
You speak Hindi, Hinglish, and English with warmth, dignity, and encouragement.
Informal workers often feel imposter syndrome when entering formal corporations. Validate their lived experience, explain technical jargon in simple, relatable metaphors, and provide actionable next steps.`,
    userPromptTemplate: `User query: {query}
Language: {lang}`,
    testInput: `"Mujhe formal company me interview dene me darr lagta hai. English achhi nahi hai meri."`,
    baselineOutput: `You should study English grammar rules and practice vocabulary every day.`,
    improvedOutput: `नमस्ते रमेश जी! आपका यह संकोच बिल्कुल स्वाभाविक है, लेकिन याद रखिए: कंपनियाँ आपके **हुनर और काम की कारीगरी (Hands-on Craftsmanship)** की कद्र करती हैं। 

फैशन और एक्सपोर्ट इंडस्ट्री में सबसे ज़रूरी बात यह होती है कि आप मशीन के काम, टांकों की बारीकी और फैब्रिक को कितनी अच्छी तरह समझते हैं।

यहाँ 3 आसान सुझाव हैं:
1. **टेक्निकल शब्द सीखें:** सिलाई और क्वालिटी से जुड़े 15-20 शब्द (जैसे Seam tolerance, Bobbin tension, AQL sampling) याद कर लें।
2. **इंटरव्यू में आत्मविश्वास:** आप कह सकते हैं: *"Sir, my English is conversational, but my 5-year technical tailoring experience is 100% solid."*
3. **Elevate X Interview Lab:** हमारे AI इंटरव्यू रूम में हिंदी-इंग्लिश मिक्स में 2 बार अभ्यास करें।

आपकी 5 साल की मेहनत आपका सबसे बड़ा प्रमाण पत्र है!`,
    metrics: {
      extractionAccuracy: 95,
      evidenceValidation: 96,
      jobRelevance: 97,
      factuality: 98,
      jsonValidity: 95,
      latencyMs: 340
    },
    baselineMetrics: {
      extractionAccuracy: 60,
      evidenceValidation: 62,
      jobRelevance: 65,
      factuality: 80,
      jsonValidity: 75,
      latencyMs: 480
    }
  }
];

export const mockAdminStats = {
  totalRegisteredUsers: 14280,
  activeMonthlyUsers: 9840,
  assessmentsCompleted: 31250,
  verifiedSkillsLogged: 58900,
  curatedJobListings: 1240,
  successfulTransitions: 3480,
  promptEvaluationsCount: 182,
  avgPromptAccuracy: 96.2,
  dailyPlatformActivity: [
    { day: "Mon", users: 1820, assessments: 620, queries: 4100 },
    { day: "Tue", users: 2100, assessments: 710, queries: 4600 },
    { day: "Wed", users: 2450, assessments: 890, queries: 5300 },
    { day: "Thu", users: 2300, assessments: 840, queries: 5100 },
    { day: "Fri", users: 2780, assessments: 1040, queries: 6200 },
    { day: "Sat", users: 3100, assessments: 1250, queries: 7100 },
    { day: "Sun", users: 2950, assessments: 1180, queries: 6800 }
  ]
};

export const initialAssistantMessages: AssistantMessage[] = [
  {
    id: "msg-1",
    sender: "assistant",
    content: "Hello Ramesh! I am your **Elevate X AI Career Mentor**. I can help you translate your informal experience into recognized skills, prepare for job interviews, analyze skill gaps, and explore new high-paying career pathways. How can I assist your career growth today?",
    timestamp: "10:30 AM",
    suggestions: [
      "How do I prepare for an Apparel QA interview?",
      "Explain AQL 2.5 in simple words",
      "Improve my resume summary for export houses",
      "मुझे हिंदी में करियर सलाह चाहिए"
    ],
    language: "English"
  }
];
