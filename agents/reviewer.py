import os
from groq import Groq
from dotenv import load_dotenv
import json

from utils.helpers import clean_llm_json

load_dotenv()

class ReviewerAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def _rule_check(self, content):
        feedback = []

        if "explanation" not in content:
            feedback.append("Missing explanation")

        if "mcqs" not in content:
            feedback.append("Missing MCQs")

        if "mcqs" in content:
            if len(content["mcqs"]) != 3:
                feedback.append("Must contain exactly 3 MCQs")

            for i, mcq in enumerate(content["mcqs"]):
                if "question" not in mcq:
                    feedback.append(f"MCQ {i+1} missing question")

                if "options" not in mcq or len(mcq["options"]) != 4:
                    feedback.append(f"MCQ {i+1} must have 4 options")

                if "answer" not in mcq:
                    feedback.append(f"MCQ {i+1} missing answer")

        return feedback

    def _llm_review(self, content, grade):
        prompt = f"""
You are an expert educational reviewer.

Evaluate the following content for Grade {grade}.

Check:
- Age appropriateness
- Concept correctness
- Clarity and simplicity

Return ONLY JSON:
{{
  "status": "pass" or "fail",
  "feedback": ["point 1", "point 2"]
}}

Content:
{json.dumps(content)}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You evaluate educational content strictly."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        raw = response.choices[0].message.content

        try:
            from utils.helpers import clean_llm_json

            parsed = clean_llm_json(raw)

            if parsed:
                return parsed
            else:
                return {
                    "status": "fail",
                    "feedback": ["LLM output parsing failed"]
                }
        except:
            return {
                "status": "fail",
                "feedback": ["LLM output parsing failed"]
            }   
        

    def review(self, content, grade):
        rule_feedback = self._rule_check(content)
        llm_result = self._llm_review(content, grade)
        # Prefer rule-based checks: if any rule feedback exists, mark fail.
        # Otherwise trust the LLM's status.
        llm_status = llm_result.get("status", "fail")

        if rule_feedback:
            status = "fail"
            final_feedback = rule_feedback + llm_result.get("feedback", [])
        else:
            status = llm_status
            # Only include feedback when status is fail. If LLM reports pass,
            # return an empty feedback list per spec.
            if status == "pass":
                final_feedback = []
            else:
                final_feedback = llm_result.get("feedback", [])

        return {
            "status": status,
            "feedback": final_feedback
        }