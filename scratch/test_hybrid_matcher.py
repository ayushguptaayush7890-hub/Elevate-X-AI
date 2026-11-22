import os
import re
import json
import torch
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from transformers import AutoTokenizer, AutoModel

# 1. Technical Alias Dictionary
TECHNICAL_ALIASES = {
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite", "sql (mysql)", "t-sql", "pl/sql"],
    "react": ["react", "react.js", "reactjs", "react native"],
    "react.js": ["react", "react.js", "reactjs"],
    "node": ["node", "node.js", "nodejs"],
    "node.js": ["node", "node.js", "nodejs"],
    "llm": ["llm", "llms", "large language model", "large language models", "generative ai"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "nlp": ["nlp", "natural language processing", "text mining"],
    "computer vision": ["computer vision", "cv", "opencv", "yolo", "yolov8", "object detection", "image recognition", "image segmentation", "resnet", "cnn"],
    "machine learning": ["machine learning", "ml", "scikit-learn", "sklearn", "supervised learning", "unsupervised learning"],
    "deep learning": ["deep learning", "dl", "neural network", "neural networks", "cnn", "rnn", "lstm", "transformer", "transformers", "pytorch", "tensorflow"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow", "tf", "keras"],
    "docker": ["docker", "containerization", "containers"],
    "git": ["git"],
    "github": ["github"],
    "postman": ["postman", "api testing"],
    "data structures and algorithms": ["data structures and algorithms", "dsa", "data structures & algorithms", "data structures", "algorithms"],
    "rest api": ["rest api", "rest apis", "restful", "restful api", "restful apis", "api development"],
    "c++": ["c++", "cpp"],
    "python": ["python", "python3"],
    "numpy": ["numpy"],
    "pandas": ["pandas"]
}

_EMBED_MODEL = None
_EMBED_TOKENIZER = None

def get_embed_model():
    global _EMBED_MODEL, _EMBED_TOKENIZER
    if _EMBED_MODEL is None:
        model_name = "typeform/distilbert-base-uncased-mnli"
        _EMBED_TOKENIZER = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
        _EMBED_MODEL = AutoModel.from_pretrained(model_name, local_files_only=True)
        _EMBED_MODEL.eval()
    return _EMBED_MODEL, _EMBED_TOKENIZER

def compute_embeddings(texts: List[str]) -> np.ndarray:
    model, tokenizer = get_embed_model()
    inputs = tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        # Mean pooling with attention mask
        mask = inputs["attention_mask"].unsqueeze(-1).expand(outputs.last_hidden_state.size()).float()
        sum_embeddings = torch.sum(outputs.last_hidden_state * mask, 1)
        sum_mask = torch.clamp(mask.sum(1), min=1e-9)
        mean_pooled = sum_embeddings / sum_mask
        # L2 normalize
        normalized = torch.nn.functional.normalize(mean_pooled, p=2, dim=1)
    return normalized.cpu().numpy()

def match_requirement(req: str, candidate_pool: List[Dict[str, Any]]) -> Dict[str, Any]:
    req_clean = req.strip()
    req_lower = req_clean.lower()
    
    # 1. Exact & Alias Match on Pool
    best_match = None
    best_score = 0.0
    match_layer = None
    
    # Check if compound requirement (e.g. "NumPy, Pandas and Scikit-learn" or "Python, PyTorch, and Transformers")
    # Extract sub-terms if compound
    compound_delimiters = r"[,|/•]|\band\b"
    raw_sub_terms = [t.strip() for t in re.split(compound_delimiters, req_clean, flags=re.I) if len(t.strip()) > 1]
    # Filter out stopwords from sub-terms
    stopwords = {"experience", "with", "knowledge", "of", "proficient", "in", "strong", "understanding", "hands-on", "familiarity", "prior", "plus", "skills"}
    sub_terms = []
    for st in raw_sub_terms:
        clean_st = " ".join(w for w in st.split() if w.lower() not in stopwords).strip()
        if clean_st and len(clean_st) > 1:
            sub_terms.append(clean_st)
    
    if not sub_terms:
        sub_terms = [req_clean]
        
    matched_sub_terms = []
    matched_evidences = []
    
    for sub in sub_terms:
        sub_lower = sub.lower()
        sub_aliases = TECHNICAL_ALIASES.get(sub_lower, [sub_lower])
        sub_found = False
        
        # Check candidate pool
        for cand in candidate_pool:
            cand_text = cand["text"]
            cand_lower = cand_text.lower()
            section = cand["section"]
            
            # Direct word boundary match for any alias
            for alias in sub_aliases:
                # Escaped boundary
                pat = rf"(?:^|[^\w\+#\.-]){re.escape(alias)}(?:$|[^\w\+#\.-])"
                if re.search(pat, cand_lower):
                    matched_sub_terms.append(sub)
                    matched_evidences.append((cand_text, section, 1.0, f"Layer 1/2/3: Exact/Alias '{alias}'"))
                    sub_found = True
                    break
            if sub_found:
                break
                
    if matched_sub_terms:
        # We found exact/alias matches for sub-terms!
        ratio = len(matched_sub_terms) / len(sub_terms)
        top_ev = matched_evidences[0]
        ev_text, ev_sec, _, layer_info = top_ev
        
        # Determine 5-state status
        if ev_sec == "coursework":
            status = "partially_supported"
            status_label = "Partially Supported (Academic Coursework)"
            score = 0.65
        elif ratio >= 0.99 or len(sub_terms) == 1:
            status = "explicitly_matched"
            status_label = "Explicit Match"
            score = 0.95
        else:
            status = "partially_supported"
            status_label = f"Partially Supported ({len(matched_sub_terms)}/{len(sub_terms)} skills verified)"
            score = 0.50 + 0.40 * ratio
            
        all_ev_strings = [f"[{sec.upper()}] {txt}" for txt, sec, _, _ in matched_evidences]
        return {
            "requirement": req_clean,
            "status": status,
            "status_label": status_label,
            "similarityScore": float(score),
            "resumeEvidence": " | ".join(all_ev_strings[:3]),
            "matchLayer": layer_info,
            "matchedSubTerms": matched_sub_terms
        }
        
    # Layer 4: Semantic Embedding Matching
    req_vec = compute_embeddings([req_clean])
    cand_texts = [c["text"] for c in candidate_pool]
    cand_vecs = compute_embeddings(cand_texts)
    
    sims = np.dot(cand_vecs, req_vec.T).squeeze()
    best_idx = int(np.argmax(sims))
    semantic_sim = float(sims[best_idx])
    best_cand = candidate_pool[best_idx]
    
    if semantic_sim >= 0.72:
        status = "explicitly_matched"
        status_label = "Explicit Match (Semantic)"
    elif semantic_sim >= 0.48:
        status = "partially_supported"
        status_label = "Partially Supported (Semantic)"
    else:
        status = "not_found_in_resume"
        status_label = "Not Found in Text"
        
    return {
        "requirement": req_clean,
        "status": status,
        "status_label": status_label,
        "similarityScore": float(round(semantic_sim, 3)),
        "resumeEvidence": f"[{best_cand['section'].upper()}] {best_cand['text']}" if status != "not_found_in_resume" else None,
        "matchLayer": "Layer 4: Pretrained DistilBERT Embeddings (768-dim)" if status != "not_found_in_resume" else None,
        "matchedSubTerms": []
    }

print("Loaded hybrid matcher test definition.")
