import streamlit as st
import pandas as pd
from database import fetch_user_performance

# PDF Libraries
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

import tempfile


def generate_pdf(subject, df, attempts, avg, best, last):

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)

    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("EduSynth Performance Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Subject Info
    elements.append(Paragraph(f"Subject: {subject}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    # Summary Table
    summary_data = [
        ["Total Attempts", attempts],
        ["Average Score", round(avg, 2)],
        ["Best Score", best],
        ["Last Score", last],
    ]

    summary_table = Table(summary_data, colWidths=[2.5 * inch, 2.5 * inch])

    summary_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 0.4 * inch))

    # Attempt History Table
    table_data = [["Attempt", "Score"]]

    for _, row in df.iterrows():
        table_data.append([row["Attempt"], row["Score"]])

    performance_table = Table(table_data, colWidths=[2.5 * inch, 2.5 * inch])

    performance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))

    elements.append(performance_table)

    doc.build(elements)

    return temp_file.name


def show_performance_page():

    st.title("📊 Performance Analytics")

    subject = st.session_state.selected_subject
    user_id = st.session_state.user["id"]

    st.write(f"Subject: **{subject}**")

    records = fetch_user_performance(user_id, subject)

    if not records:
        st.info("No quiz attempts yet.")
        if st.button("⬅ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        return

    scores = [r[0] for r in records]
    totals = [r[1] for r in records]

    attempts = len(scores)
    avg = sum(scores) / attempts
    best = max(scores)
    last = scores[-1]

    df = pd.DataFrame({
        "Attempt": list(range(1, attempts + 1)),
        "Score": scores
    })

    # Summary
    st.markdown("### 📌 Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Attempts", attempts)
    col2.metric("Average Score", round(avg, 2))
    col3.metric("Best Score", best)
    col4.metric("Last Score", last)

    st.markdown("---")

    # Trend
    st.markdown("### 📈 Score Trend")
    st.line_chart(df.set_index("Attempt"))

    st.markdown("---")

    # Attempt History
    st.markdown("### 🗂 Attempt History")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # PDF Download
    st.markdown("### 📄 Download Report")

    if st.button("Generate Performance PDF"):

        pdf_path = generate_pdf(subject, df, attempts, avg, best, last)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇ Download PDF",
                data=f,
                file_name=f"{subject}_performance_report.pdf",
                mime="application/pdf"
            )

    st.markdown("---")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

