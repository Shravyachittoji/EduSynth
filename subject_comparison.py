import streamlit as st
import pandas as pd
from database import fetch_subject_comparison

# PDF Libraries
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

import tempfile


def generate_comparison_pdf(df):

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)

    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("EduSynth Subject Comparison Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Table Data
    table_data = [["Subject", "Average Score (%)"]]

    for _, row in df.iterrows():
        table_data.append([row["Subject"], round(row["Percentage"], 2)])

    table = Table(table_data, colWidths=[3 * inch, 3 * inch])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))

    elements.append(table)

    doc.build(elements)

    return temp_file.name


def show_subject_comparison():

    st.title("📈 Subject Comparison")

    user_id = st.session_state.user["id"]

    records = fetch_subject_comparison(user_id)

    if not records:
        st.info("No quiz attempts available.")
        if st.button("⬅ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        return

    df = pd.DataFrame(records, columns=["Subject", "Score", "Total"])

    df["Percentage"] = (df["Score"] / df["Total"]) * 100

    subject_avg = df.groupby("Subject")["Percentage"].mean().reset_index()

    st.markdown("### 📊 Average Score per Subject (%)")
    st.bar_chart(subject_avg.set_index("Subject"))

    st.markdown("### 📋 Detailed Table")
    st.dataframe(subject_avg, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # PDF Download Section
    # -----------------------------
    st.markdown("### 📄 Download Comparison Report")

    if st.button("Generate Comparison PDF"):

        pdf_path = generate_comparison_pdf(subject_avg)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇ Download PDF",
                data=f,
                file_name="subject_comparison_report.pdf",
                mime="application/pdf"
            )

    st.markdown("---")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
