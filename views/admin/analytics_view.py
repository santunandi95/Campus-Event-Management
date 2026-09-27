"""
views/admin/analytics_view.py
----------------------------
Administrator Deep Analytics & Data Visualization Hub.
Integrates Pandas statistical modeling, NumPy array aggregations,
and Matplotlib publication-grade visualization charts.
"""

import streamlit as st
import pandas as pd

from analytics.event_analytics import EventAnalytics
from analytics.participation_analytics import ParticipationAnalytics
from analytics.feedback_analytics import FeedbackAnalytics
from visualization.charts import (
    plot_event_participation,
    plot_feedback_distribution,
    plot_popularity_vs_capacity,
    plot_average_ratings,
    plot_department_participation,
    plot_category_analysis,
    plot_performance_scores,
    figure_to_bytes,
)
from components.ui_helpers import render_header, render_kpi


def render_admin_analytics() -> None:
    """Render the full analytical intelligence and charts suite."""
    evt_analytics = EventAnalytics()
    part_analytics = ParticipationAnalytics()
    fbk_analytics = FeedbackAnalytics()

    render_header(
        title="Predictive & Empirical Analytics Hub",
        subtitle="Data-driven insights using Pandas aggregations, NumPy mathematical statistics, and Matplotlib",
        badge_text="Data Intelligence",
    )

    tab_overview, tab_charts, tab_numpy, tab_scores = st.tabs([
        "📊 High-Level Metrics",
        "📈 Matplotlib Visualizations",
        "🧮 NumPy Statistical Analysis",
        "🏆 Event Performance Scoring",
    ])

    # -------------------------------------------------------------
    # TAB 1: High-Level Metrics
    # -------------------------------------------------------------
    with tab_overview:
        st.markdown("#### 🏛️ Campus-Wide Analytical Breakdown")

        part_table = part_analytics.get_event_participation_table()
        st.markdown("##### 📌 Event Participation & Capacity Efficiency")
        if not part_table.empty:
            st.dataframe(part_table, use_container_width=True, hide_index=True)
            csv_data = part_table.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Participation Ledger (CSV)",
                data=csv_data,
                file_name="event_participation_data.csv",
                mime="text/csv",
            )
        else:
            st.info("No participation data available.")

        st.markdown("---")
        col_dept, col_cat = st.columns(2)
        with col_dept:
            st.markdown("##### 🏢 Department-Wise Engagement")
            df_dept = part_analytics.get_department_participation()
            if not df_dept.empty:
                st.dataframe(df_dept, use_container_width=True, hide_index=True)

        with col_cat:
            st.markdown("##### 🏷️ Event Category Distribution")
            df_cat = evt_analytics.get_events_by_category()
            if not df_cat.empty:
                st.dataframe(df_cat, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------
    # TAB 2: Matplotlib Visualizations
    # -------------------------------------------------------------
    with tab_charts:
        st.markdown("#### 🎨 Publication-Quality Matplotlib Visualizations")
        st.caption("Each visualization is dynamically rendered using Matplotlib and can be saved as high-res PNG.")

        chart_select = st.selectbox(
            "Select Analytical Visualization Chart",
            [
                "Chart 1 — Event Participation (Participants per Event)",
                "Chart 2 — Feedback Distribution (1 to 5 Stars)",
                "Chart 3 — Event Popularity vs Capacity Comparison",
                "Chart 4 — Average Event Rating Comparison",
                "Chart 5 — Department Participation Distribution",
                "Chart 6 — Category Analysis & Engagement",
                "Chart 7 — Event Performance Score Matrix",
            ],
        )

        st.markdown("---")

        if "Chart 1" in chart_select:
            top_n = st.slider("Number of Top Events to Display", 5, 15, 10)
            df_table = part_analytics.get_event_participation_table()
            fig = plot_event_participation(df_table, top_n=top_n)
            st.pyplot(fig)
            st.download_button("💾 Download Chart as PNG", figure_to_bytes(fig), "chart_event_participation.png", "image/png")

        elif "Chart 2" in chart_select:
            df_dist = fbk_analytics.get_rating_distribution()
            fig = plot_feedback_distribution(df_dist)
            st.pyplot(fig)
            st.download_button("💾 Download Chart as PNG", figure_to_bytes(fig), "chart_feedback_distribution.png", "image/png")

        elif "Chart 3" in chart_select:
            top_n = st.slider("Number of Events to Compare", 4, 12, 8)
            df_table = part_analytics.get_event_participation_table()
            fig = plot_popularity_vs_capacity(df_table, top_n=top_n)
            st.pyplot(fig)
            st.download_button("💾 Download Chart as PNG", figure_to_bytes(fig), "chart_popularity_vs_capacity.png", "image/png")

        elif "Chart 4" in chart_select:
            df_summary = fbk_analytics.get_event_feedback_summary()
            fig = plot_average_ratings(df_summary)
            st.pyplot(fig)
            st.download_button("💾 Download Chart as PNG", figure_to_bytes(fig), "chart_average_ratings.png", "image/png")

        elif "Chart 5" in chart_select:
            df_dept = part_analytics.get_department_participation()
            fig = plot_department_participation(df_dept)
            st.pyplot(fig)
            st.download_button("💾 Download Chart as PNG", figure_to_bytes(fig), "chart_department_participation.png", "image/png")

        elif "Chart 6" in chart_select:
            df_cat = part_analytics.get_category_participation()
            fig = plot_category_analysis(df_cat)
            st.pyplot(fig)
            st.download_button("💾 Download Chart as PNG", figure_to_bytes(fig), "chart_category_analysis.png", "image/png")

        elif "Chart 7" in chart_select:
            top_n = st.slider("Number of Top Events to Score", 5, 15, 10)
            df_perf = fbk_analytics.get_event_performance_scores()
            fig = plot_performance_scores(df_perf, top_n=top_n)
            st.pyplot(fig)
            st.download_button("💾 Download Chart as PNG", figure_to_bytes(fig), "chart_performance_scores.png", "image/png")

    # -------------------------------------------------------------
    # TAB 3: NumPy Statistical Analysis
    # -------------------------------------------------------------
    with tab_numpy:
        st.markdown("#### 🧮 Numerical & Statistical Foundations (NumPy Engine)")
        st.caption(
            "Empirical verification of feedback distributions using NumPy array operations. "
            "Includes central tendency, dispersion, and quantile distributions."
        )

        num_stats = fbk_analytics.get_numpy_statistics()

        if num_stats:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                render_kpi("Sample Size (N)", str(num_stats["sample_size"]), "Total Student Reviews")
                render_kpi("Minimum Rating", f"{num_stats['min_rating']} ★", "Floor Observation")
            with c2:
                render_kpi("Arithmetic Mean (μ)", f"{num_stats['mean']:.3f}", "numpy.mean()")
                render_kpi("Maximum Rating", f"{num_stats['max_rating']} ★", "Ceiling Observation")
            with c3:
                render_kpi("Median Rating", f"{num_stats['median']:.2f}", "numpy.median() - 50th %ile")
                render_kpi("Interquartile Range", f"{num_stats['interquartile_range']:.2f}", "IQR = Q3 - Q1")
            with c4:
                render_kpi("Standard Deviation (σ)", f"{num_stats['standard_deviation']:.3f}", "numpy.std()")
                render_kpi("Variance (σ²)", f"{num_stats['variance']:.3f}", "numpy.var()")

            st.markdown("##### 📐 Quantile Breakdown")
            q_df = pd.DataFrame([
                {"Quantile": "25th Percentile (Q1)", "Value": num_stats["percentile_25"], "Method": "numpy.percentile(a, 25)"},
                {"Quantile": "50th Percentile (Median)", "Value": num_stats["median"], "Method": "numpy.median(a)"},
                {"Quantile": "75th Percentile (Q3)", "Value": num_stats["percentile_75"], "Method": "numpy.percentile(a, 75)"},
                {"Quantile": "Interquartile Range (IQR)", "Value": num_stats["interquartile_range"], "Method": "Q3 - Q1"},
            ])
            st.table(q_df)
        else:
            st.info("Insufficient feedback data for statistical computation.")

    # -------------------------------------------------------------
    # TAB 4: Event Performance Scoring
    # -------------------------------------------------------------
    with tab_scores:
        st.markdown("#### 🏆 Multi-Criteria Event Performance Score (0 - 100)")
        st.markdown(
            """
            The **Event Performance Score** synthesizes three normalized operational dimensions:
            1. **Capacity Utilization Score (40%)**: \( \min(1.0, \frac{\text{Registrations}}{\text{Capacity}}) \times 40 \)
            2. **Feedback Rating Score (40%)**: \( \frac{\text{Average Rating}}{5.0} \times 40 \)
            3. **Feedback Engagement Score (20%)**: \( \min(1.0, \frac{\text{Reviews}}{\text{Registrations}}) \times 20 \)
            """
        )

        perf_scores = fbk_analytics.get_event_performance_scores()
        if not perf_scores.empty:
            st.dataframe(perf_scores, use_container_width=True, hide_index=True)
            csv_scores = perf_scores.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Performance Matrix (CSV)",
                data=csv_scores,
                file_name="event_performance_matrix.csv",
                mime="text/csv",
            )
        else:
            st.info("No performance scores computed yet.")
