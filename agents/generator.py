import os
from groq import Groq
from dotenv import load_dotenv
import json

from sympy import content

from sympy import content

from utils.helpers import clean_llm_json

load_dotenv()

class GeneratorAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _build_prompt(self, grade, topic, feedback=None):
        prompt = f"""
You are an expert educational content creator.

Generate content for:
- Grade: {grade}
- Topic: {topic}

Requirements:
- Use simple, age-appropriate language
- Keep explanation concise (3-5 sentences)
- Generate EXACTLY 3 MCQs
- Each MCQ must have 4 options
- Include correct answer

Return ONLY valid JSON in this format:
{{
  "explanation": "...",
  "mcqs": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "..."
    }}
  ]
}}
"""

        if feedback:
            prompt += f"\nImprove the content based on this feedback:\n{feedback}"

        return prompt

    def generate(self, grade: int, topic: str, feedback: list = None) -> dict:
        prompt = self._build_prompt(grade, topic, feedback)

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You generate structured educational JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        try:
            from utils.helpers import clean_llm_json

            parsed = clean_llm_json(content)

            if parsed:
                return parsed
            else:
                return {
                 "explanation": "Error parsing response",
                "mcqs": []
                        }
        except:
            return {
                "explanation": "Error parsing response",
                "mcqs": []
            }