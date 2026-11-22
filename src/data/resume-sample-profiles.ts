import { ResumeFullData } from "@/types/resume-generator";

export const fresherProfile: ResumeFullData = {
  personalInfo: {
    fullName: "Rohan Verma",
    professionalTitle: "Associate Software Engineer / CS Graduate",
    email: "rohan.verma@example.com",
    phone: "+91 98111 22334",
    location: "New Delhi, India",
    linkedIn: "https://linkedin.com/in/rohanverma-cs",
    gitHub: "https://github.com/rohanverma",
    portfolio: "https://rohanverma.dev",
    summary: "Aspiring software engineer with a strong foundation in computer science fundamentals, data structures, algorithms, and full-stack development. Eager to contribute to scalable web applications and cloud architectures."
  },
  education: [
    {
      id: "edu-fresher-1",
      institution: "Delhi Technological University (DTU)",
      degree: "Bachelor of Technology (B.Tech)",
      fieldOfStudy: "Computer Science and Engineering",
      startDate: "August 2020",
      endDate: "May 2024",
      grade: "8.65 / 10.0",
      coursework: ["Data Structures & Algorithms", "Operating Systems", "Database Management Systems", "Computer Networks", "Object-Oriented Programming"]
    }
  ],
  skills: {
    programmingLanguages: ["C++", "Java", "Python", "JavaScript", "SQL"],
    frameworks: ["React.js", "Node.js", "Express", "Tailwind CSS"],
    databases: ["PostgreSQL", "MongoDB"],
    developerTools: ["Git", "GitHub", "VS Code", "Postman", "Linux"],
    aiMlSkills: ["Basic Machine Learning", "Scikit-Learn"],
    otherSkills: ["REST APIs", "Agile Methodologies", "Problem Solving"]
  },
  experience: [],
  internships: [
    {
      id: "int-fresher-1",
      organization: "FinTech Labs Pvt Ltd",
      role: "Software Engineering Intern",
      duration: "June 2023 – August 2023 (3 months)",
      workPerformed: [
        "Developed responsive dashboard widgets using React.js and TypeScript for internal financial metrics.",
        "Created RESTful endpoints in Node.js/Express to aggregate user transaction summaries."
      ],
      achievements: [
        "Optimized frontend render times by 25% through memoization and code splitting."
      ]
    }
  ],
  projects: [
    {
      id: "proj-fresher-1",
      title: "CampusConnect – Academic Resource Sharing Portal",
      description: "Full-stack university portal enabling student study material exchange and collaborative note sharing.",
      technologies: ["React", "Node.js", "MongoDB", "Express", "Tailwind CSS"],
      contributions: [
        "Implemented JWT-based authentication and role-based access control for student moderators.",
        "Engineered full-text search across 5,000+ course documents with sub-200ms query latency.",
        "Deployed application on AWS EC2 with automated GitHub Actions CI/CD pipeline."
      ],
      githubUrl: "https://github.com/rohanverma/campus-connect",
      projectUrl: "https://campusconnect-demo.vercel.app"
    },
    {
      id: "proj-fresher-2",
      title: "AlgoVisualizer – Interactive Algorithm Workbench",
      description: "Web application visualizing sorting and graph traversal algorithms step-by-step for educational use.",
      technologies: ["JavaScript", "HTML5 Canvas", "CSS3"],
      contributions: [
        "Built interactive step-by-step visualizations for Dijkstra, A*, QuickSort, and MergeSort.",
        "Attracted 1,200+ active student users across university computer science batches."
      ],
      githubUrl: "https://github.com/rohanverma/algo-visualizer"
    }
  ],
  certifications: [
    {
      id: "cert-fresher-1",
      name: "Meta Front-End Developer Professional Certificate",
      issuingOrganization: "Coursera / Meta",
      issueDate: "December 2023",
      credentialUrl: "https://coursera.org/verify/professional-cert/meta-frontend"
    }
  ],
  additional: {
    achievements: [
      "Top 5% in LeetCode Global Contest with 450+ algorithmic problems solved.",
      "Finalist at Smart India Hackathon 2023 (Hardware & Software Edition)."
    ],
    awards: ["Academic Merit Scholarship, DTU (2021, 2022)"],
    publications: [],
    volunteerExperience: ["Technical Head, DTU Coding Club – Mentored 120+ first-year students."],
    extracurricular: ["Competitive Programming", "Technical Blogging"],
    languages: ["English (Professional)", "Hindi (Native)"],
    interests: ["Open-Source Systems", "System Architecture", "Chess"]
  },
  templateId: "fresher",
  accentColor: "#1E3A8A",
  typography: "sans",
  spacing: "normal"
};

export const aimlStudentProfile: ResumeFullData = {
  personalInfo: {
    fullName: "Priya Sundaram",
    professionalTitle: "AI / ML Researcher & Graduate Student",
    email: "priya.sundaram@ai-research.edu",
    phone: "+91 97234 56789",
    location: "Bengaluru, India",
    linkedIn: "https://linkedin.com/in/priyasundaram-ai",
    gitHub: "https://github.com/priyasundaram",
    portfolio: "https://priyasundaram.ai",
    summary: "Machine learning researcher specializing in Natural Language Processing, Multimodal Transformer architectures, and Low-Rank Adaptation (LoRA). Experienced in building fine-tuning pipelines and evaluating large language models."
  },
  education: [
    {
      id: "edu-aiml-1",
      institution: "Indian Institute of Science (IISc), Bengaluru",
      degree: "Master of Science (M.S. by Research)",
      fieldOfStudy: "Artificial Intelligence & Computational Data Science",
      startDate: "August 2022",
      endDate: "July 2024",
      grade: "3.92 / 4.0",
      coursework: ["Deep Learning for NLP", "Statistical Machine Learning", "Probabilistic Graphical Models", "Reinforcement Learning", "High-Performance Computing"]
    },
    {
      id: "edu-aiml-2",
      institution: "Vellore Institute of Technology (VIT)",
      degree: "B.Tech in Computer Science",
      fieldOfStudy: "Computer Science & Engineering",
      startDate: "July 2018",
      endDate: "May 2022",
      grade: "9.18 / 10.0",
      coursework: ["Linear Algebra", "Probability Theory", "Artificial Intelligence"]
    }
  ],
  skills: {
    programmingLanguages: ["Python", "C++", "SQL", "Julia"],
    frameworks: ["PyTorch", "Hugging Face Transformers", "vLLM", "DeepSpeed", "LangChain", "JAX"],
    databases: ["ChromaDB", "Milvus", "Qdrant", "PostgreSQL"],
    developerTools: ["Git", "Docker", "WandB", "MLflow", "CUDA", "Ray Train"],
    aiMlSkills: ["Transformer LLMs", "LoRA / QLoRA Fine-tuning", "Retrieval-Augmented Generation (RAG)", "Token Classification (NER)", "Multimodal Embeddings"],
    otherSkills: ["Model Quantization (GGUF, AWQ)", "Latency Profiling", "Distributed Training"]
  },
  experience: [],
  internships: [
    {
      id: "int-aiml-1",
      organization: "AI4Bharat / IIT Madras",
      role: "Machine Learning Research Intern",
      duration: "May 2023 – November 2023 (6 months)",
      workPerformed: [
        "Curated and benchmarked Indic-language tokenizers across 12 Scheduled Indian languages.",
        "Implemented Parameter-Efficient Fine-Tuning (PEFT) on LLaMA-2-7B and Mistral-7B for Hindi question-answering."
      ],
      achievements: [
        "Achieved a 4.2 BLEU score improvement on regional technical translation benchmarks."
      ]
    }
  ],
  projects: [
    {
      id: "proj-aiml-1",
      title: "MedRAG – Multilingual Clinical Information Retrieval",
      description: "Domain-specific medical RAG system synthesizing clinical trial outcomes with verifiable source citations.",
      technologies: ["PyTorch", "Hugging Face", "Qdrant", "FastAPI", "Docker"],
      contributions: [
        "Constructed hybrid dense-sparse retriever indexing 250,000+ PubMed abstracts with reciprocal rank fusion.",
        "Fine-tuned BioMistral-7B using LoRA on clinical case reports, reducing hallucinated citations by 38%."
      ],
      githubUrl: "https://github.com/priyasundaram/medrag-clinical",
      projectUrl: "https://medrag.ai-demo.org"
    },
    {
      id: "proj-aiml-2",
      title: "FastNER-Indic – Subword Entity Extractor",
      description: "High-throughput token classification pipeline for low-resource multilingual skill and entity extraction.",
      technologies: ["XLM-RoBERTa", "PyTorch", "ONNX Runtime"],
      contributions: [
        "Quantized model to INT8 via ONNX Runtime, delivering 3.4x faster inference latency on CPU targets.",
        "Published open-source checkpoint on Hugging Face Hub with 4,500+ community downloads."
      ],
      githubUrl: "https://github.com/priyasundaram/fastner-indic"
    }
  ],
  certifications: [
    {
      id: "cert-aiml-1",
      name: "Deep Learning Specialization",
      issuingOrganization: "DeepLearning.AI / Andrew Ng",
      issueDate: "January 2023"
    }
  ],
  additional: {
    achievements: [
      "Kaggle Competitions Master (Top 0.8% worldwide).",
      "Prime Minister's Research Fellowship (PMRF) Nominee, 2023."
    ],
    awards: ["Best Research Poster Award at Indian Conference on AI (ICAI 2023)"],
    publications: [
      "Sundaram, P. et al. 'Subword Boundary Optimization for Indic Token Classification' – Proceedings of EMNLP Findings (2023)."
    ],
    volunteerExperience: ["Reviewer for NeurIPS 2024 Workshops."],
    extracurricular: ["Open Source AI Contributor", "Hugging Face Community"],
    languages: ["English (Bilingual)", "Tamil (Native)", "Hindi (Fluent)"],
    interests: ["Mechanistic Interpretability", "AI Safety", "Astrophysics"]
  },
  templateId: "data_science",
  accentColor: "#0F766E",
  typography: "sans",
  spacing: "normal"
};

export const softwareDevProfile: ResumeFullData = {
  personalInfo: {
    fullName: "Arjun Mehta",
    professionalTitle: "Full-Stack Software Engineer",
    email: "arjun.mehta@devmail.io",
    phone: "+91 99887 66554",
    location: "Pune, Maharashtra, India",
    linkedIn: "https://linkedin.com/in/arjunmehta-dev",
    gitHub: "https://github.com/arjunmehtadev",
    portfolio: "https://arjunmehta.tech",
    summary: "Full-stack software engineer with 3+ years of experience engineering high-availability web applications, distributed microservices, and reactive user interfaces. Proficient in Next.js, Node.js, Go, PostgreSQL, and AWS cloud infrastructure."
  },
  education: [
    {
      id: "edu-dev-1",
      institution: "Pune Institute of Computer Technology (PICT)",
      degree: "B.E. in Information Technology",
      fieldOfStudy: "Information Technology",
      startDate: "August 2017",
      endDate: "June 2021",
      grade: "8.9 / 10.0",
      coursework: ["Distributed Computing", "Software Engineering", "Cloud Computing"]
    }
  ],
  skills: {
    programmingLanguages: ["TypeScript", "JavaScript", "Go", "Python", "SQL"],
    frameworks: ["React", "Next.js", "Node.js", "Express", "FastAPI", "Tailwind CSS"],
    databases: ["PostgreSQL", "Redis", "Elasticsearch", "MongoDB"],
    developerTools: ["Docker", "Kubernetes", "AWS (EC2, S3, RDS, Lambda)", "Git", "GitHub Actions", "Terraform"],
    aiMlSkills: ["OpenAI API", "Vector Embeddings"],
    otherSkills: ["Microservices Architecture", "REST & GraphQL APIs", "Event-Driven Systems", "Kafka"]
  },
  experience: [
    {
      id: "exp-dev-1",
      company: "Apex Cloud Technologies",
      role: "Software Development Engineer II",
      employmentType: "Full-time",
      location: "Pune, India (Hybrid)",
      startDate: "July 2022",
      endDate: "Present",
      current: true,
      responsibilities: [
        "Architected and deployed multi-tenant subscription microservices serving 450,000+ monthly active enterprise users.",
        "Refactored legacy monolith into event-driven Go services backed by Apache Kafka, slashing peak API latency by 55%.",
        "Engineered automated Terraform infrastructure provisioning and GitHub Actions CI/CD pipelines achieving zero-downtime rolling deployments."
      ]
    },
    {
      id: "exp-dev-2",
      company: "Zest Infotech Solutions",
      role: "Associate Software Engineer",
      employmentType: "Full-time",
      location: "Mumbai, India",
      startDate: "July 2021",
      endDate: "June 2022",
      current: false,
      responsibilities: [
        "Developed core UI components using Next.js, TypeScript, and Tailwind CSS for enterprise CRM dashboard.",
        "Integrated Stripe payment gateway and webhook reconciliation processing over ₹8 Crore in annual billing volume.",
        "Authored comprehensive end-to-end test suites using Playwright and Jest, elevating test coverage from 42% to 88%."
      ]
    }
  ],
  internships: [],
  projects: [
    {
      id: "proj-dev-1",
      title: "FlowEngine – Distributed Task Orchestration Pipeline",
      description: "Distributed workflow scheduler with fault-tolerant worker nodes and real-time WebSocket progress telemetry.",
      technologies: ["Go", "React", "Redis", "PostgreSQL", "Docker"],
      contributions: [
        "Implemented distributed lock consensus using Redis Redlock algorithm to prevent duplicate worker task executions.",
        "Built responsive real-time DAG monitoring interface visualizing active workflow execution graphs."
      ],
      githubUrl: "https://github.com/arjunmehtadev/flow-engine",
      projectUrl: "https://flowengine.dev"
    }
  ],
  certifications: [
    {
      id: "cert-dev-1",
      name: "AWS Certified Solutions Architect – Associate",
      issuingOrganization: "Amazon Web Services",
      issueDate: "September 2022",
      credentialUrl: "https://aws.amazon.com/verification"
    },
    {
      id: "cert-dev-2",
      name: "Certified Kubernetes Application Developer (CKAD)",
      issuingOrganization: "Cloud Native Computing Foundation",
      issueDate: "March 2023"
    }
  ],
  additional: {
    achievements: [
      "Recipient of 'Spotlight Engineer of the Quarter' award at Apex Cloud Technologies (Q3 2023).",
      "Open-source maintainer of Go-Cache-Helper library with 350+ GitHub stars."
    ],
    awards: ["1st Place, Maharashtra State Hackathon (2020)"],
    publications: [],
    volunteerExperience: ["Technical Speaker at Pune Gophers Meetup (Topic: Distributed Concurrency in Go)."],
    extracurricular: ["Tech Blogging (15k+ reads on Dev.to)"],
    languages: ["English (Fluent)", "Hindi (Fluent)", "Marathi (Native)"],
    interests: ["Distributed Systems", "Cloud Security", "Mechanical Keyboards"]
  },
  templateId: "technical",
  accentColor: "#4F46E5",
  typography: "mono",
  spacing: "normal"
};

export const experiencedLeadProfile: ResumeFullData = {
  personalInfo: {
    fullName: "Vikramaditya Singhania",
    professionalTitle: "Director of Engineering / Senior Technology Leader",
    email: "v.singhania@techleadership.com",
    phone: "+91 98200 12345",
    location: "Bengaluru, Karnataka, India",
    linkedIn: "https://linkedin.com/in/vikramaditya-singhania",
    portfolio: "https://singhania.io",
    summary: "Senior Engineering Leader with 8+ years of experience scaling global SaaS platforms, directing distributed engineering organizations of 40+ engineers, and establishing modern DevOps practices. Proven track record of aligning engineering roadmaps with business revenue growth."
  },
  education: [
    {
      id: "edu-lead-1",
      institution: "Indian Institute of Management (IIM) Bangalore",
      degree: "Executive General Management Programme",
      fieldOfStudy: "Technology Leadership & Strategy",
      startDate: "2019",
      endDate: "2020",
      grade: "Executive Honours",
      coursework: []
    },
    {
      id: "edu-lead-2",
      institution: "National Institute of Technology (NIT) Trichy",
      degree: "B.Tech in Computer Science",
      fieldOfStudy: "Computer Science & Engineering",
      startDate: "2012",
      endDate: "2016",
      grade: "8.75 / 10.0",
      coursework: []
    }
  ],
  skills: {
    programmingLanguages: ["Python", "Go", "Java", "TypeScript", "SQL"],
    frameworks: ["React", "FastAPI", "Spring Boot", "gRPC", "Next.js"],
    databases: ["PostgreSQL", "Cassandra", "Redis", "Snowflake"],
    developerTools: ["AWS", "Kubernetes", "Datadog", "Terraform", "Kafka", "GitLab CI"],
    aiMlSkills: ["Enterprise Generative AI Integration", "MLOps Governance"],
    otherSkills: ["Engineering Leadership", "Strategic Architecture", "P&L Management", "SOC2 & GDPR Compliance", "Technical Recruitment"]
  },
  experience: [
    {
      id: "exp-lead-1",
      company: "HyperScale Global Cloud Inc.",
      role: "Director of Platform Engineering",
      employmentType: "Full-time",
      location: "Bengaluru, India",
      startDate: "January 2022",
      endDate: "Present",
      current: true,
      responsibilities: [
        "Lead a distributed engineering department of 42 software engineers, architects, and DevOps leads across 4 product verticals.",
        "Spearheaded architectural transformation to multi-region cloud infrastructure, delivering 99.995% SLA and cutting annual cloud infrastructure spend by $420,000.",
        "Established unified engineering operational standards, lowering quarterly production defect escape rates by 68% and doubling deployment velocity."
      ]
    },
    {
      id: "exp-lead-2",
      company: "OmniPay Financial Services",
      role: "Lead Systems Architect & Engineering Manager",
      employmentType: "Full-time",
      location: "Gurugram, India",
      startDate: "March 2018",
      endDate: "December 2021",
      current: false,
      responsibilities: [
        "Directed the engineering of high-throughput payment transaction gateway processing ₹1,200+ Crore monthly transaction volume.",
        "Achieved full PCI-DSS Level 1 and SOC2 Type II certifications in partnership with international cybersecurity audit teams.",
        "Scaled engineering team from 6 to 24 developers while maintaining 94% retention through structured engineering mentorship frameworks."
      ]
    },
    {
      id: "exp-lead-3",
      company: "Cognitive Solutions Labs",
      role: "Senior Software Engineer",
      employmentType: "Full-time",
      location: "Bengaluru, India",
      startDate: "June 2016",
      endDate: "February 2018",
      current: false,
      responsibilities: [
        "Engineered real-time data streaming pipelines using Apache Kafka and Apache Spark for enterprise supply chain analytics.",
        "Mentored junior engineers and instituted rigorous code review standards across the backend engineering team."
      ]
    }
  ],
  internships: [],
  projects: [],
  certifications: [
    {
      id: "cert-lead-1",
      name: "AWS Certified Solutions Architect – Professional",
      issuingOrganization: "Amazon Web Services",
      issueDate: "2021",
      credentialUrl: "https://aws.amazon.com/verify"
    },
    {
      id: "cert-lead-2",
      name: "Certified Information Systems Security Professional (CISSP)",
      issuingOrganization: "ISC2",
      issueDate: "2022"
    }
  ],
  additional: {
    achievements: [
      "Keynote Speaker at AWS Community Day India 2023 (Scaling Multi-Region SaaS).",
      "Mentored 35+ aspiring engineering managers through Plato Leadership Network."
    ],
    awards: ["CTO Excellence Award for Strategic Cloud Transformation (2023)"],
    publications: [
      "Singhania, V. 'Architecting Resilient Enterprise Payment Gateways' – Tech Leaders Journal (2021)."
    ],
    volunteerExperience: ["Board Member, Tech Foundation for Rural Education."],
    extracurricular: ["Angel Investing in B2B SaaS Startups", "Marathon Running"],
    languages: ["English (Fluent)", "Hindi (Native)"],
    interests: ["Cloud Native Architecture", "Product Strategy", "High Altitude Trekking"]
  },
  templateId: "corporate_executive",
  accentColor: "#17233F",
  typography: "serif",
  spacing: "normal"
};
