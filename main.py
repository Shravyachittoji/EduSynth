# ==========================================
# EduSynth - Modern UI Version
# ==========================================

import streamlit as st
import google.generativeai as genai

from database import (
    create_users_table,
    create_quiz_table,
    create_doubts_table,
    create_coding_table
)

from auth import show_auth_page
from learning_flow import show_learning_page
from quiz_engine import show_quiz_page
from progress import show_performance_page
from subject_comparison import show_subject_comparison
from analytics import show_analytics_page
from doubts import show_doubts_page
from coding_practice import show_coding_practice_page


# -----------------------------------------
# INITIALIZE DATABASE TABLES
# -----------------------------------------
create_users_table()
create_quiz_table()
create_doubts_table()
create_coding_table()


# -----------------------------------------
# CONFIGURE GEMINI
# -----------------------------------------
genai.configure(api_key="AIzaSyATvKo4ZzOpWI-uPnVQTxVDToQTfNXW1eU")

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash"
)


# -----------------------------------------
# STREAMLIT CONFIG
# -----------------------------------------
st.set_page_config(page_title="EduSynth AI", layout="wide")


# -----------------------------------------
# CUSTOM MODERN UI STYLING
# -----------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}

section[data-testid="stSidebar"] {
    background: #1e293b;
    padding: 20px;
}

.custom-card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: 0.3s ease-in-out;
    border: 1px solid rgba(255,255,255,0.1);
}

.custom-card:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.1);
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    padding: 12px;
    font-weight: 600;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
}

h1, h2, h3 {
    font-weight: 700;
}

.profile-badge {
    background: rgba(255,255,255,0.1);
    padding:8px 15px;
    border-radius:20px;
    display:inline-block;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# SESSION INIT
# -----------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "auth"


# =====================================================
# ROUTING
# =====================================================

# -------- AUTH --------
if st.session_state.page == "auth":
    show_auth_page()


# -------- SUBJECT SELECTION --------
elif st.session_state.page == "subject_selection":

    st.title("🎓 EduSynth - Adaptive AI Learning System")
    st.markdown("### Select the Subject You Want to Learn")

    st.success(f"Welcome {st.session_state.user['name']} 👋")

    subjects = [
        "Python",
        "Java",
        "Data Structures",
        "Machine Learning",
        "Artificial Intelligence"
    ]

    selected_subject = st.selectbox("Choose a Subject", subjects)

    if st.button("Continue"):
        st.session_state.selected_subject = selected_subject
        st.session_state.page = "level_selection"
        st.rerun()


# -------- LEVEL SELECTION --------
elif st.session_state.page == "level_selection":

    st.title("📊 Select Your Learning Level")

    st.write(f"Selected Subject: **{st.session_state.selected_subject}**")

    levels = ["Beginner", "Intermediate", "Advanced"]

    selected_level = st.radio("Choose Your Level", levels)

    if st.button("Continue"):
        st.session_state.selected_level = selected_level
        st.session_state.page = "dashboard"
        st.rerun()


# -------- DASHBOARD --------
elif st.session_state.page == "dashboard":

    subject = st.session_state.selected_subject
    level = st.session_state.selected_level
    name = st.session_state.user["name"]

    # ---------------- HEADER WITH USERNAME ----------------
    col_left, col_right = st.columns([6, 1])

    with col_left:
        st.markdown("<h1 style='margin-bottom:0;'>🎯 Learning Dashboard</h1>", unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
            <div class="profile-badge">
            👤 {name}
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats Section
    colA, colB, colC = st.columns(3)
    colA.metric("📘 Subject", subject)
    colB.metric("🔥 Level", level)
    colC.metric("🎯 Mode", "Active")

    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("⚙ Quick Navigation")

        subjects = [
            "Python",
            "Java",
            "Data Structures",
            "Machine Learning",
            "Artificial Intelligence"
        ]

        new_subject = st.selectbox("Change Subject", subjects)
        new_level = st.selectbox("Change Level", ["Beginner", "Intermediate", "Advanced"])

        if st.button("Apply Changes"):
            st.session_state.selected_subject = new_subject
            st.session_state.selected_level = new_level
            st.rerun()

        st.markdown("---")

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.session_state.page = "auth"
            st.rerun()

    # Dashboard Cards
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        st.markdown('<div class="custom-card">📚 Continue Learning</div>', unsafe_allow_html=True)
        if st.button("Open", key="learn"):
            st.session_state.page = "learning"
            st.rerun()

    with col2:
        st.markdown('<div class="custom-card">📝 Take Quiz</div>', unsafe_allow_html=True)
        if st.button("Open", key="quiz"):
            st.session_state.page = "quiz"
            st.rerun()

    with col3:
        st.markdown('<div class="custom-card">📊 View Performance</div>', unsafe_allow_html=True)
        if st.button("Open", key="performance"):
            st.session_state.page = "performance"
            st.rerun()

    with col4:
        st.markdown('<div class="custom-card">📈 Compare Subjects</div>', unsafe_allow_html=True)
        if st.button("Open", key="compare"):
            st.session_state.page = "subject_comparison"
            st.rerun()

    with col5:
        st.markdown('<div class="custom-card">💬 Ask Doubt</div>', unsafe_allow_html=True)
        if st.button("Open", key="doubt"):
            st.session_state.page = "doubts"
            st.rerun()

    with col6:
        st.markdown('<div class="custom-card">💻 Coding Practice</div>', unsafe_allow_html=True)
        if st.button("Open", key="coding"):
            st.session_state.page = "coding"
            st.rerun()

    col7, col8, col9 = st.columns(3)
    with col7:
        st.markdown('<div class="custom-card">📊 Research Analytics</div>', unsafe_allow_html=True)
        if st.button("Open", key="analytics"):
            st.session_state.page = "analytics"
            st.rerun()


# -------- OTHER ROUTES --------
elif st.session_state.page == "learning":
    show_learning_page(model)

elif st.session_state.page == "quiz":
    show_quiz_page(model)

elif st.session_state.page == "performance":
    show_performance_page()

elif st.session_state.page == "subject_comparison":
    show_subject_comparison()

elif st.session_state.page == "analytics":
    show_analytics_page()

elif st.session_state.page == "doubts":
    show_doubts_page(model)

elif st.session_state.page == "coding":
    show_coding_practice_page(model)
