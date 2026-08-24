import streamlit as st


def show_learning_page(model):

    st.title("📘 Learning Module")

    subject = st.session_state.selected_subject
    level = st.session_state.selected_level

    st.write(f"Subject: **{subject}**")
    st.write(f"Level: **{level}**")

    # ---------------------------------
    # TOPIC MAP
    # ---------------------------------
    topic_map = {
        "Python": [
            "Introduction to Python",
            "Variables and Data Types",
            "Control Structures",
            "Functions",
            "Object-Oriented Programming"
        ],
        "Data Structures": [
            "Introduction to Data Structures",
            "Arrays",
            "Linked Lists",
            "Stacks",
            "Queues"
        ],
        "Machine Learning": [
            "What is Machine Learning?",
            "Supervised Learning",
            "Unsupervised Learning",
            "Model Training",
            "Evaluation Metrics"
        ],
        "Artificial Intelligence": [
            "Introduction to AI",
            "Search Algorithms",
            "Knowledge Representation",
            "Neural Networks",
            "Ethics in AI"
        ],
        "Java": [
            "Introduction to Java",
            "Variables and Data Types",
            "Control Flow",
            "OOP in Java",
            "Collections Framework"
        ]
    }

    topics = topic_map.get(subject, ["Introduction"])

    if "current_topic_index" not in st.session_state:
        st.session_state.current_topic_index = 0

    current_topic = topics[st.session_state.current_topic_index]

    st.markdown("---")
    st.subheader(f"📖 Topic {st.session_state.current_topic_index + 1}: {current_topic}")

    # ---------------------------------
    # GENERATE CONTENT
    # ---------------------------------
    prompt = f"""
    Act as an intelligent tutor.

    Teach the topic '{current_topic}' in {subject}
    at a {level} level.

    Provide:
    1. Clear Explanation
    2. Real-world Example
    """

    response = model.generate_content(prompt)
    st.write(response.text)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Previous Topic") and st.session_state.current_topic_index > 0:
            st.session_state.current_topic_index -= 1
            st.rerun()

    with col2:
        if st.session_state.current_topic_index < len(topics) - 1:
            if st.button("Next Topic ➡"):
                st.session_state.current_topic_index += 1
                st.rerun()

    st.markdown("---")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
