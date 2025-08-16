# app.py
import streamlit as st
import pandas as pd
import os
from utils import QuestionGenerator

class QuizManager:
    def __init__(self):
        self.questions = []     # list of dicts
        self.results = []       # evaluation results

    def generate_questions(self, generator, company, round_type, sub_topic, difficulty, num_questions):
        self.questions = []
        self.results = []

        try:
            context_topic = f"{company} | {round_type} | {sub_topic}"

            if round_type == "Interview Qs":
                seen = set()
                for _ in range(num_questions * 3):  # extra attempts to avoid repeats
                    qa = generator.generate_interview_qa(company)
                    q_text = qa.question.strip().lower()
                    if q_text and q_text not in seen:
                        seen.add(q_text)
                        self.questions.append({
                            "type": "Interview",
                            "question": qa.question.strip(),
                            "answer": qa.answer.strip()
                        })
                    if len(self.questions) >= num_questions:
                        break
            else:
                for _ in range(num_questions):
                    q = generator.generate_mcq(context_topic, difficulty)
                    self.questions.append({
                        "type": "MCQ",
                        "question": q.question.strip(),
                        "options": [opt.strip() for opt in q.options][:4],
                        "correct_answer": q.correct_answer.strip()
                    })

        except Exception as e:
            st.error(f"Error generating questions: {e}")
            return False
        return True

    def attempt_quiz(self, round_type):
        if round_type == "Interview Qs":
            for i, q in enumerate(self.questions):
                st.markdown(f"**Interview Question {i+1}:** {q['question']}")
                st.info(q['answer'])
                st.markdown("---")
        else:
            for i, q in enumerate(self.questions):
                st.markdown(f"**Question {i+1}:** {q['question']}")
                st.radio(
                    f"Select an answer for Question {i+1}",
                    q["options"],
                    key=f"mcq_{i}"
                )
                st.markdown("---")

    def evaluate_quiz(self):
        self.results = []
        for i, q in enumerate(self.questions):
            user_ans = st.session_state.get(f"mcq_{i}", "")
            is_correct = user_ans == q.get("correct_answer", "")
            self.results.append({
                "question_number": i + 1,
                "question_type": q["type"],
                "question": q["question"],
                "options": q.get("options", []),
                "user_answer": user_ans,
                "correct_answer": q.get("correct_answer", ""),
                "is_correct": is_correct
            })

    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)

    def save_to_csv(self):
        if not self.results:
            st.warning("No results to save.")
            return None
        df = self.generate_result_dataframe()
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"quiz_results_{timestamp}.csv"
        os.makedirs("results", exist_ok=True)
        full_path = os.path.join("results", unique_filename)
        df.to_csv(full_path, index=False)
        st.success(f"Results saved to {full_path}")
        return full_path


def main():
    st.set_page_config(page_title="Placement-Oriented Question Generator", page_icon="💼")

    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    st.title(" Placement-Oriented Question Generator")
    st.sidebar.header("Quiz Settings")

    st.sidebar.selectbox("Select API", ["Groq"], index=0)

    # Only Multiple Choice (kept for UI consistency)
    st.sidebar.selectbox("Question Type", ["Multiple Choice"], index=0)

    company = st.sidebar.selectbox(
        "Select Company",
        ["Accenture","Amazon","Capgemini","Cognizant GenC","CTS","Deloitte",
         "Hexaware","Saint Gobain","TCS","Wipro","IBM","Infosys","Tech Mahindra"]
    )

    round_type = st.sidebar.selectbox(
        "Select Round",
        ["Aptitude MCQs", "Technical MCQs", "Interview Qs"]
    )

    if round_type == "Aptitude MCQs":
        sub_topic = st.sidebar.selectbox(
            "Select Aptitude Topic",
            ["Quantitative Aptitude","Data Interpretation","Logical Reasoning",
             "Verbal Reasoning","Non Verbal Reasoning"]
        )
    elif round_type == "Technical MCQs":
        sub_topic = st.sidebar.selectbox(
            "Select Technical Topic",
            ["Python","C Programming","C++ Programming","Java Programming",
             "JavaScript","SQL","DSA","DBMS","Operating System",
             "Computer Network","React","Angular"]
        )
    else:
        sub_topic = "Company Specific HR Interview"

    # Difficulty only for MCQ rounds
    difficulty = "medium"
    if round_type != "Interview Qs":
        difficulty = st.sidebar.selectbox(
            "Difficulty Level",
            ["Easy", "Medium", "Hard"],
            index=1
        ).lower()

    num_questions = st.sidebar.number_input(
        "Number of Questions",
        min_value=1, max_value=10, value=5
    )

    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False
        generator = QuestionGenerator()
        ok = st.session_state.quiz_manager.generate_questions(
            generator, company, round_type, sub_topic, difficulty, num_questions
        )
        st.session_state.quiz_generated = bool(ok)
        if st.session_state.quiz_generated:
            st.rerun()
        else:
            st.error("⚠️ Could not generate questions. Try again.")

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz(round_type)

        if round_type != "Interview Qs":
            if st.button("Submit Quiz"):
                st.session_state.quiz_manager.evaluate_quiz()
                st.session_state.quiz_submitted = True
                st.rerun()

    if st.session_state.quiz_submitted and round_type != "Interview Qs":
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()
        if not results_df.empty:
            correct_count = int(results_df["is_correct"].sum())
            total_questions = len(results_df)
            pct = (correct_count / total_questions) * 100 if total_questions else 0.0
            st.write(f"Score: {correct_count}/{total_questions} ({pct:.1f}%)")

            for _, row in results_df.iterrows():
                if row["is_correct"]:
                    st.success(f"✅ Q{row['question_number']}: {row['question']}")
                else:
                    st.error(f"❌ Q{row['question_number']}: {row['question']}")
                    st.write(f"Your Answer: {row['user_answer']}")
                    st.write(f"Correct Answer: {row['correct_answer']}")
                st.markdown("---")

            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file, "rb") as f:
                        st.download_button(
                            "Download Results",
                            f.read(),
                            file_name=os.path.basename(saved_file),
                            mime="text/csv"
                        )
        else:
            st.warning("No results available.")

if __name__ == "__main__":
    main()
