# utils.py
import os
import re
import time
from typing import List

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
import os, streamlit as st



# -------------------- Data Models --------------------
class MCQQuestion(BaseModel):
    question: str = Field(description="The question text")
    options: List[str] = Field(description="List of 4 possible answers")
    correct_answer: str = Field(description="The correct answer from the options")

    @validator('question', pre=True)
    def clean_question(cls, v):
        return str(v) if not isinstance(v, dict) else v.get('description', str(v))

class InterviewQA(BaseModel):
    question: str = Field(description="The interview question")
    answer: str = Field(description="The best suitable answer")

# -------------------- Generator ----------------------
class QuestionGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            api_key = st.secrets["GROQ_API_KEY"],
            model="llama-3.1-8b-instant",
            temperature=0.8,
        )

    def generate_mcq(self, context: str, difficulty: str = "medium") -> MCQQuestion:
        """
        context example: 'Wipro | Technical MCQs | SQL'
        difficulty: easy | medium | hard
        """
        parser = PydanticOutputParser(pydantic_object=MCQQuestion)
        prompt = PromptTemplate(
            template=(
                "Generate a {difficulty} level multiple-choice question for placement preparation.\n"
                "Context: {context}\n"
                "- Ensure it matches the company/round/topic context.\n"
                "- Provide exactly 4 distinct options.\n"
                "- The correct_answer must be one of the options.\n\n"
                "Return ONLY JSON with fields: question, options, correct_answer.\n"
                "No extra text. No markdown fences."
            ),
            input_variables=["context", "difficulty"],
        )
        return self._retry_parse(prompt, parser, context=context, difficulty=difficulty)

    def generate_interview_qa(self, company: str) -> InterviewQA:
        """
        HR-style, company-specific interview Q&A (short, realistic, unique).
        """
        parser = PydanticOutputParser(pydantic_object=InterviewQA)
        prompt = PromptTemplate(
            template=(
                "Act as an HR interviewer for {company} campus placements.\n"
                "Generate ONE short, realistic HR interview question (6–18 words) and a concise professional answer (2–4 sentences).\n"
                "Guidelines:\n"
                "- HR/behavioral/situational/cultural-fit ONLY (no technical).\n"
                "- Vary themes across calls: motivation for {company}, strengths/weaknesses, teamwork, leadership, conflict resolution,\n"
                "  communication, career goals, relocation, work ethics, flexibility, learning mindset, salary expectations.\n"
                "- Make the question feel specific to {company} (mention it when natural) and avoid long case studies.\n"
                "- Keep answer crisp, polite, and tailored to {company}'s values (innovation, client-focus, learning, integrity, teamwork as applicable).\n"
                "- Avoid clichés and avoid repeating common templates.\n\n"
                "Return ONLY JSON with fields: question, answer.\n"
                "No extra text. No markdown fences."
            ),
            input_variables=["company"],
        )
        return self._retry_parse(prompt, parser, company=company)

    # -------------------- Helpers ----------------------
    def _retry_parse(self, prompt: PromptTemplate, parser: PydanticOutputParser, **kwargs):
        max_attempts = 3
        last_err = None
        for _ in range(max_attempts):
            try:
                raw = self.llm.predict(prompt.format(**kwargs))
                cleaned = self._clean_to_json(raw)
                return parser.parse(cleaned)
            except Exception as e:
                last_err = e
                time.sleep(0.8)
        raise RuntimeError(f"Failed to generate after {max_attempts} attempts: {last_err}")

    @staticmethod
    def _clean_to_json(text: str) -> str:
        t = text.strip()
        # remove code fences if present
        t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.IGNORECASE)
        # extract first {...} block
        start = t.find("{")
        end = t.rfind("}")
        if start != -1 and end != -1 and end > start:
            return t[start : end + 1]
        return t
