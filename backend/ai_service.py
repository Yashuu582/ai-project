import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""You are an ATS (Applicant Tracking System) AI assistant.

Analyze the following resume against the job description and respond ONLY with a valid JSON object in this exact format:
{{
  "score": <integer 0-100>,
  "strengths": ["strength1", "strength2", "strength3"],
  "gaps": ["gap1", "gap2"],
  "suggestions": ["suggestion1", "suggestion2"],
  "summary": "<2 sentence summary>"
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Respond with JSON only, no extra text."""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=60)

        response.raise_for_status()
        raw = response.json().get("response", "")

        # Extract JSON from response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            return _fallback()

        return json.loads(raw[start:end])

    except Exception as e:
        print(f"Ollama error: {e}")
        return _fallback()

def _fallback():
    return {
        "score": 0,
        "strengths": [],
        "gaps": ["Could not analyze - ensure Ollama is running with llama3"],
        "suggestions": ["Run: ollama pull llama3 && ollama serve"],
        "summary": "AI analysis unavailable. Please ensure Ollama is running."
    }
