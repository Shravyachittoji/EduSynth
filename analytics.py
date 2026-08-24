"""
EduSynth Analytics - Paper Benchmark Graphs
Based on: EduSynth: Generative Content Creation for Personalized Learning
Chittoji Shravya, Gajula Deekshith, Shaik Charishma, Kukutla Venu
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Paper-reported data: Table 1 - Comparative Performance of Prediction Models
MODEL_COMPARISON_DATA = [
    {"Model": "Logistic Regression", "Accuracy": 82.4, "Precision": 81, "Recall": 79, "F1-Score": 80},
    {"Model": "Decision Tree", "Accuracy": 86.7, "Precision": 85, "Recall": 84, "F1-Score": 84},
    {"Model": "Support Vector Machine", "Accuracy": 89.2, "Precision": 88, "Recall": 87, "F1-Score": 87},
    {"Model": "EduSynth (Random Forest)", "Accuracy": 94.6, "Precision": 93, "Recall": 92, "F1-Score": 93},
]

# Paper-reported data: Section 4.5 - Feature Importance
FEATURE_IMPORTANCE_DATA = [
    {"Feature": "Attendance %", "Importance": 28},
    {"Feature": "Assignment Completion", "Importance": 24},
    {"Feature": "Quiz Performance", "Importance": 21},
    {"Feature": "Participation Metrics", "Importance": 17},
    {"Feature": "Historical GPA", "Importance": 10},
]


def show_analytics_page():
    st.title("📊 EduSynth Research Analytics")
    st.caption("Benchmark graphs from the paper: *EduSynth: Generative Content Creation for Personalized Learning*")

    df = pd.DataFrame(MODEL_COMPARISON_DATA)
    feature_df = pd.DataFrame(FEATURE_IMPORTANCE_DATA)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Model Comparison",
        "📐 Accuracy, Precision, Recall, F1",
        "📊 Feature Importance",
        "📉 Model Success Ranking",
    ])

    # ========== TAB 1: Model Comparison (Grouped Bar) ==========
    with tab1:
        st.markdown("### Comparative Performance of Prediction Models (Table 1)")
        st.markdown("EduSynth (Random Forest) vs Logistic Regression, Decision Tree, and SVM on 1,200 students dataset.")

        fig_comp = go.Figure()
        # Brighter, high-contrast colors for metrics
        fig_comp.add_trace(go.Bar(name="Accuracy (%)", x=df["Model"], y=df["Accuracy"], marker_color="#60a5fa"))  # bright blue
        fig_comp.add_trace(go.Bar(name="Precision (%)", x=df["Model"], y=df["Precision"], marker_color="#f97316"))  # bright orange
        fig_comp.add_trace(go.Bar(name="Recall (%)", x=df["Model"], y=df["Recall"], marker_color="#22c55e"))  # bright green
        fig_comp.add_trace(go.Bar(name="F1-Score (%)", x=df["Model"], y=df["F1-Score"], marker_color="#eab308"))  # bright yellow

        fig_comp.update_layout(
            barmode="group",
            title="Model Comparison: EduSynth Outperforms Baseline Classifiers",
            xaxis_title="Model",
            yaxis_title="Score (%)",
            yaxis=dict(range=[0, 100]),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-25,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        st.markdown("---")
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ========== TAB 2: Accuracy, Precision, Recall, F1 (Individual Metrics) ==========
    with tab2:
        st.markdown("### Classification Metrics by Model")
        st.markdown("Accuracy: 94.6% | Precision: 93.8% | Recall: 92.9% | F1-Score: 93.3% (EduSynth)")

        metrics_melt = df.melt(
            id_vars=["Model"],
            value_vars=["Accuracy", "Precision", "Recall", "F1-Score"],
            var_name="Metric",
            value_name="Value (%)",
        )

        fig_metrics = px.bar(
            metrics_melt,
            x="Model",
            y="Value (%)",
            color="Metric",
            barmode="group",
            color_discrete_sequence=["#60a5fa", "#f97316", "#22c55e", "#eab308"],
        )
        fig_metrics.update_layout(
            title="Accuracy, Precision, Recall, F1-Score Across Models",
             yaxis_title="Metric Value (%)",
             yaxis=dict(range=[0, 100]),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-25,
        )
        st.plotly_chart(fig_metrics, use_container_width=True)

        st.markdown("---")
        st.markdown("**EduSynth Results (Section 4.3):** High accuracy indicates strong predictive capability. Balanced precision and recall demonstrate effective identification of At-Risk students without excessive false positives.")

    # ========== TAB 3: Feature Importance ==========
    with tab3:
        st.markdown("### Feature Importance Analysis (Section 4.5)")
        st.markdown("Academic factors most influential in predicting student knowledge levels.")

        fig_feat = px.bar(
            feature_df,
            x="Feature",
            y="Importance",
            color="Feature",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_feat.update_layout(
            title="Feature Importance Ranking (Random Forest)",
            xaxis_title="Academic Indicator",
            yaxis_title="Contribution (%)",
            yaxis=dict(range=[0, 100]),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
        )
        st.plotly_chart(fig_feat, use_container_width=True)

        st.markdown("---")
        # Bar-only alternative to pie chart: 100% stacked bar (out of 100)
        feature_df_norm = feature_df.copy()
        total = feature_df_norm["Importance"].sum()
        feature_df_norm["Share"] = (feature_df_norm["Importance"] / total) * 100 if total else 0
        feature_df_norm = feature_df_norm.sort_values("Share", ascending=False)

        fig_share = go.Figure()
        for _, row in feature_df_norm.iterrows():
            fig_share.add_trace(
                go.Bar(
                    name=row["Feature"],
                    y=["100%"],
                    x=[row["Share"]],
                    orientation="h",
                    text=[f'{row["Share"]:.1f}%'],
                    textposition="inside",
                )
            )

        fig_share.update_layout(
            barmode="stack",
            title="Feature Contribution Distribution (100% Stacked Bar)",
            xaxis_title="Share (%)",
            yaxis_title="",
            xaxis=dict(range=[0, 100]),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_share, use_container_width=True)

    # ========== TAB 4: Model Success Ranking ==========
    with tab4:
        st.markdown("### Successful Model Ranking")
        df["Overall"] = (df["Accuracy"] + df["Precision"] + df["Recall"] + df["F1-Score"]) / 4
        rank_df = df.sort_values("Overall", ascending=False)

        fig_rank = px.bar(
            rank_df,
            x="Model",
            y="Overall",
            color="Overall",
            color_continuous_scale="Viridis",
        )
        fig_rank.update_layout(
            title="Model Success Ranking (Average of All Metrics)",
            yaxis_title="Average Score (%)",
            yaxis=dict(range=[0, 100]),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig_rank, use_container_width=True)

        st.markdown("---")
        st.markdown("**EduSynth (Random Forest)** achieves the highest overall score, attributed to the aggregation of multiple decision trees which reduces variance and improves generalization across diverse academic patterns.")

    st.markdown("---")
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
