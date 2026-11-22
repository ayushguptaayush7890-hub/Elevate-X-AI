"""
Gemini AI Assistant Service for Elevate X AI Career Mentor.
Integrates Google Gemini API via official google-genai SDK with multi-turn history,
multilingual capabilities (English, Hindi, Hinglish), context injection, and follow-up suggestion extraction.
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
import json
import time
from app.core.config import settings

logger = logging.getLogger(__name__)

# Supported model cascade for high reliability
DEFAULT_MODELS = [
    settings.GEMINI_MODEL or "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3-flash-preview",
]


class GeminiAssistantService:
    """Service handling multi-turn AI consultations using Google Gemini."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not configured in settings or environment.")

    def _get_client(self):
        """Initializes and returns the Google GenAI Client."""
        if not self.api_key:
            raise ValueError(
                "Gemini API key is missing. Please set GEMINI_API_KEY in backend/.env"
            )
        from google import genai
        return genai.Client(api_key=self.api_key)

    def _build_system_instruction(self, candidate_context: str, language: str) -> str:
        """Constructs the comprehensive system instruction for the AI Career Mentor."""
        lang_directive = (
            "The candidate prefers HINDI (हिन्दी). Provide your response primarily in fluent, professional, and natural Hindi (Devanagari script). Maintain technical/vocational terms (e.g. AQL 2.5, ATS Resume, Python, Inspection) in their standard form where appropriate."
            if language.lower() in ["hindi", "hi"]
            else "The candidate prefers ENGLISH. Provide your response in clear, professional, empathetic, and encouraging English."
        )

        return f"""You are the **Elevate X AI Career Mentor**, an empathetic, authoritative, and practical vocational career coach and technical advisor within the Elevate X AI platform.

### Core Mission & Domain Expertise:
1. **Vocational & Informal-to-Formal Career Guidance:** Validate practical hands-on experience, shop-floor skills, and informal work. Translate craftsmanship into formal industry standards, certifications, and NSQF levels.
2. **Interview Preparation:** Provide actionable STAR-method talking points, technical and trade explanations (e.g. garment QA and AQL 2.5 sampling, electrical safety, software engineering principles), and confidence coaching.
3. **Resume & ATS Optimization:** Suggest strong action verbs, quantifiable achievements, and modern ATS phrasing.
4. **Skill Development & Roadmaps:** Advise on high-priority bridge skills, target competencies, and real-world project portfolios.
5. **Multilingual Agility:** Effortlessly communicate in English, Hindi (Devanagari), or conversational Hinglish depending on how the candidate writes and their preferences.

### Language Preference:
{lang_directive}
Note: If the user writes in Hindi or Hinglish, match their language style naturally.

### Authenticated Candidate Context:
{candidate_context}

### Formatting Guidelines:
- Format your response with clean Markdown (bullet points, bold highlights, concise sections).
- Be concrete, realistic, and highly practical. Never give vague or generic platitudes.
- Reference the candidate's actual background, verified skills, and career transition targets whenever directly relevant to their question.

### Interactive Suggestions:
At the very end of your response, output a delimiter `<<<SUGGESTIONS>>>` followed by exactly 3 short, highly clickable follow-up questions or prompts (each on its own line starting with `- `) that the candidate might want to ask next.
Example format:
<<<SUGGESTIONS>>>
- How do I answer "tell me about yourself" for this role?
- What are the top 3 interview questions on AQL 2.5?
- How should I list my practical workshop experience on my resume?
"""

    def generate_mentor_response(
        self,
        user_message: str,
        language: str = "English",
        candidate_context: str = "",
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Executes inference via Google Gemini with conversation history and context.
        Returns a dict containing:
        - content: markdown response string (cleaned of delimiters)
        - suggestions: list of 3 suggested follow-up questions
        - model_used: name of the model that served the response
        - latency_seconds: time taken
        """
        client = self._get_client()
        system_instruction = self._build_system_instruction(candidate_context, language)

        # Build contents structure for multi-turn conversation
        from google.genai import types

        contents: List[types.Content] = []

        if conversation_history:
            # Include recent turns (up to 10 previous messages)
            for msg in conversation_history[-10:]:
                role = "user" if msg.get("sender") == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg.get("content", ""))],
                    )
                )

        # Append current user prompt
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)],
            )
        )

        # Config with system instruction
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
            max_output_tokens=1500,
        )

        last_error = None
        for model_name in DEFAULT_MODELS:
            try:
                t0 = time.time()
                logger.info(f"Querying Gemini API with model: {model_name}")
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config,
                )
                latency = time.time() - t0

                raw_text = response.text or ""
                content, suggestions = self._parse_response_and_suggestions(raw_text, language)

                tokens_used = None
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    tokens_used = getattr(response.usage_metadata, "total_token_count", None)

                return {
                    "content": content,
                    "suggestions": suggestions,
                    "model_used": model_name,
                    "tokens_used": tokens_used,
                    "latency_seconds": round(latency, 2),
                }
            except Exception as e:
                logger.warning(f"Gemini model {model_name} failed: {e}. Trying next model...")
                last_error = e

        raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")

    def _parse_response_and_suggestions(
        self, raw_text: str, language: str
    ) -> Tuple[str, List[str]]:
        """Splits response text by <<<SUGGESTIONS>>> delimiter and extracts clean chips."""
        delimiter = "<<<SUGGESTIONS>>>"
        if delimiter in raw_text:
            parts = raw_text.split(delimiter, 1)
            content = parts[0].strip()
            suggestions_block = parts[1].strip()
            suggestions: List[str] = []
            for line in suggestions_block.splitlines():
                line = line.strip().lstrip("-*•0123456789. ")
                if line and len(line) > 3:
                    suggestions.append(line)
            if suggestions:
                return content, suggestions[:3]

        # Fallback suggestions if delimiter was not generated
        if language.lower() in ["hindi", "hi"]:
            default_suggestions = [
                "इंटरव्यू के लिए आत्म-परिचय (Self-Introduction) कैसे दें?",
                "मेरे अनुभव के आधार पर कौन से 3 सवाल पूछे जा सकते हैं?",
                "अपने रिज्यूमे को और बेहतर कैसे बनाएं?",
            ]
        else:
            default_suggestions = [
                "Generate a tailored self-introduction for my interviews",
                "What are top interview questions for my target occupation?",
                "How can I highlight my practical experience on my resume?",
            ]

        return raw_text.strip(), default_suggestions
