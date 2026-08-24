import streamlit as st
import json
import re
from database import insert_quiz_result


# ---------------------------------
# SAFE JSON EXTRACTION
# ---------------------------------
def extract_json(text):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


# ---------------------------------
# QUIZ PAGE
# ---------------------------------
def show_quiz_page(model):

    st.title("📝 Quiz Assessment")

    subject = st.session_state.selected_subject
    level = st.session_state.selected_level
    user_id = st.session_state.user["id"]

    st.write(f"Subject: **{subject}**")
    st.write(f"Level: **{level}**")

    st.markdown("---")

    # ---------------------------------
    # GENERATE QUIZ ONLY ONCE
    # ---------------------------------
    if "quiz_questions" not in st.session_state:

        prompt = f"""
        Generate 5 multiple choice questions about {subject}
        at {level} level.

        Return ONLY valid JSON format:

        [
          {{
            "question": "Question text",
            "options": {{
              "A": "Option A",
              "B": "Option B",
              "C": "Option C",
              "D": "Option D"
            }},
            "answer": "A"
          }}
        ]
        """

        response = model.generate_content(prompt)
        cleaned_json = extract_json(response.text)

        if cleaned_json is None:
            st.error("Error generating quiz.")
            return

        try:
            quiz_data = json.loads(cleaned_json)
            st.session_state.quiz_questions = quiz_data
        except:
            st.error("Error parsing quiz.")
            return

    quiz_data = st.session_state.quiz_questions

    user_answers = []

    # ---------------------------------
    # DISPLAY QUESTIONS
    # ---------------------------------
    for i, q in enumerate(quiz_data):

        st.markdown(f"### Q{i+1}. {q['question']}")

        choice = st.radio(
            "Select your answer:",
            options=["Select an option"] + list(q["options"].keys()),
            format_func=lambda x: (
                x if x == "Select an option"
                else f"{x}) {q['options'][x]}"
            ),
            key=f"quiz_q_{i}"
        )

        user_answers.append(choice)

    st.markdown("---")

    # ---------------------------------
    # SUBMIT QUIZ
    # ---------------------------------
    if st.button("Submit Quiz"):

        if "Select an option" in user_answers:
            st.warning("Please answer all questions.")
            return

        score = 0
        incorrect_questions = []

        for i, q in enumerate(quiz_data):
            if user_answers[i] == q["answer"]:
                score += 1
            else:
                incorrect_questions.append(q["question"])

        st.success(f"Your Score: {score} / {len(quiz_data)}")

        # Store result in database
        insert_quiz_result(user_id, subject, level, score, len(quiz_data))

        # ---------------------------------
        # AI EXPLANATION FOR WRONG ANSWERS
        # ---------------------------------
        if incorrect_questions:

            explanation_prompt = f"""
            The student answered some questions incorrectly
            in {subject} at {level} level.

            Incorrect questions:
            {incorrect_questions}

            Explain the correct concepts clearly and simply.
            """

            explanation = model.generate_content(explanation_prompt)

            st.markdown("### 📘 AI Explanation for Mistakes")
            st.write(explanation.text)

        else:
            st.success("🎉 Perfect Score! Excellent Work!")

    st.markdown("---")

    # ---------------------------------
    # NEW QUIZ
    # ---------------------------------
    if st.button("🔄 Generate New Quiz"):
        if "quiz_questions" in st.session_state:
            del st.session_state.quiz_questions
        st.rerun()

    # ---------------------------------
    # BACK BUTTON
    # ---------------------------------
    if st.button("⬅ Back to Dashboard"):
        if "quiz_questions" in st.session_state:
            del st.session_state.quiz_questions
        st.session_state.page = "dashboard"
        st.rerun()
