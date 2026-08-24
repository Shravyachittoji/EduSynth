import streamlit as st
from database import insert_doubt


def show_doubts_page(model):

    st.title("💬 Doubts & Q&A")

    subject = st.session_state.selected_subject
    level = st.session_state.selected_level
    user_id = st.session_state.user["id"]

    st.write(f"Subject: **{subject}**")
    st.write(f"Level: **{level}**")

    st.markdown("---")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display previous messages
    for message in st.session_state.chat_history:
        role = "You" if message["role"] == "user" else "AI Tutor"
        st.markdown(f"**{role}:** {message['content']}")

    st.markdown("---")

    user_question = st.text_input("Ask your doubt here:")

    if st.button("Ask") and user_question:

        # Store user question
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        # Build conversational context
        conversation_context = ""
        for msg in st.session_state.chat_history:
            role = "Student" if msg["role"] == "user" else "Tutor"
            conversation_context += f"{role}: {msg['content']}\n"

        prompt = f"""
        You are an intelligent tutor.

        The student is learning {subject} at {level} level.

        Continue the conversation naturally and help clearly.

        Conversation so far:
        {conversation_context}

        Give a helpful explanation.
        """

        response = model.generate_content(prompt)
        ai_answer = response.text

        # Save AI response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_answer
        })

        # Store in database
        insert_doubt(user_id, subject, user_question, ai_answer)

        st.rerun()

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧹 Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("⬅ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
