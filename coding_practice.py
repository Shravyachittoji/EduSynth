import streamlit as st
import subprocess
import tempfile
import os
import json
import re
import ast
from database import insert_coding_result


# --------------------------------------------------
# SAFE JSON EXTRACTION
# --------------------------------------------------
def extract_json(text):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


# --------------------------------------------------
# SAFE OBJECT PARSER
# Converts string output to real Python object
# --------------------------------------------------
def safe_parse(value):
    try:
        return ast.literal_eval(value)
    except:
        return value.strip()


# --------------------------------------------------
# GENERATE AI CODING QUESTION (NO PARAM RESTRICTION)
# --------------------------------------------------
def generate_coding_question(model, subject, level):

    # Subject-specific guidance
    if subject == "Python":
        topic_instruction = "Focus on Python programming concepts."
    elif subject == "Data Structures":
        topic_instruction = "Focus on arrays, stacks, queues, recursion, or sorting."
    elif subject == "Java":
        topic_instruction = "Focus on logical problem-solving (use Python syntax)."
    elif subject == "Machine Learning":
        topic_instruction = "Focus on data manipulation, metrics calculation, or ML-related logic."
    elif subject == "Artificial Intelligence":
        topic_instruction = "Focus on search algorithms, heuristics, or logical reasoning."
    else:
        topic_instruction = "Generate a general programming problem."

    # Difficulty rules
    if level == "Beginner":
        difficulty_rules = """
        - Keep problem simple.
        - Single core concept.
        - Small input sizes.
        """

    elif level == "Intermediate":
        difficulty_rules = """
        - Combine multiple concepts.
        - Include edge cases.
        - Moderate logic complexity.
        """

    else:
        difficulty_rules = """
        - Require algorithmic thinking.
        - Handle edge cases.
        - Encourage optimized solution.
        """

    prompt = f"""
    Generate ONE coding problem for {subject}
    at {level} level.

    {topic_instruction}

    Difficulty Requirements:
    {difficulty_rules}

    Return ONLY valid JSON in this format:

    {{
        "question": "Problem statement",
        "function_name": "function_name",
        "tests": [
            {{"input": [1,2,3], "output": {{'6':1}}}},
            {{"input": [4,5], "output": {{'9':1}}}}
        ]
    }}

    Important:
    - Allow input to be int, list, string, etc.
    - Output may be int, float, list, dict, string, or boolean.
    - Test cases must be correct.
    """

    response = model.generate_content(prompt)
    cleaned = extract_json(response.text)

    if cleaned:
        return json.loads(cleaned)

    return None


# --------------------------------------------------
# CODING PRACTICE PAGE
# --------------------------------------------------
def show_coding_practice_page(model):

    st.title("💻 AI Coding Practice")

    subject = st.session_state.selected_subject
    level = st.session_state.selected_level
    user_id = st.session_state.user["id"]

    # Regenerate if subject/level changed
    if (
        "ai_coding_question" not in st.session_state
        or st.session_state.get("coding_subject") != subject
        or st.session_state.get("coding_level") != level
    ):
        st.session_state.ai_coding_question = generate_coding_question(
            model, subject, level
        )
        st.session_state.coding_subject = subject
        st.session_state.coding_level = level

    question_data = st.session_state.ai_coding_question

    if not question_data:
        st.error("Failed to generate coding question. Try again.")
        return

    st.markdown("### 📘 Problem")
    st.write(question_data["question"])

    default_code = f"""# Write your solution below

def {question_data['function_name']}(*args):
    pass
"""

    user_code = st.text_area("Your Code:", value=default_code, height=300)

    # --------------------------------------------------
    # RUN & EVALUATE
    # --------------------------------------------------
    if st.button("▶ Run & Submit"):

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:

                tmp.write(user_code.encode("utf-8"))
                tmp.write(b"\n\n# Auto Test\n")

                for test in question_data["tests"]:
                    tmp.write(
                        f"print({question_data['function_name']}({repr(test['input'])}))\n".encode("utf-8")
                    )

                tmp_path = tmp.name

            result = subprocess.run(
                ["python", tmp_path],
                capture_output=True,
                text=True,
                timeout=5
            )

            os.remove(tmp_path)

            raw_outputs = result.stdout.strip().split("\n")
            raw_expected = [repr(test["output"]) for test in question_data["tests"]]

            parsed_outputs = [safe_parse(o) for o in raw_outputs]
            parsed_expected = [safe_parse(e) for e in raw_expected]

            # Compare real Python objects
            if parsed_outputs == parsed_expected:

                st.success("✅ Correct Solution!")

                insert_coding_result(
                    user_id,
                    subject,
                    level,
                    question_data["question"],
                    1
                )

            else:

                st.error("❌ Incorrect Solution")

                insert_coding_result(
                    user_id,
                    subject,
                    level,
                    question_data["question"],
                    0
                )

                explanation_prompt = f"""
                The student wrote this code:

                {user_code}

                Expected outputs: {parsed_expected}
                Actual outputs: {parsed_outputs}

                Explain:
                1. Why it is incorrect
                2. What concept is misunderstood
                3. How to fix it
                """

                explanation = model.generate_content(explanation_prompt)

                st.markdown("### 🤖 AI Explanation")
                st.write(explanation.text)

        except subprocess.TimeoutExpired:
            st.error("Execution timed out.")
        except Exception as e:
            st.error(str(e))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Try Again"):
            st.rerun()

    with col2:
        if st.button("➡ New AI Question"):
            del st.session_state.ai_coding_question
            st.rerun()

    st.markdown("---")

    if st.button("⬅ Back to Dashboard"):
        if "ai_coding_question" in st.session_state:
            del st.session_state.ai_coding_question
        st.session_state.page = "dashboard"
        st.rerun()
