"""
visualization/charts.py
-----------------------
Professional Matplotlib data visualization module for CampusConnect Analytics.
Generates publication-quality charts for the Streamlit dashboard and generated reports:
  - Chart 1: Event Participation (Horizontal bar chart with values)
  - Chart 2: Feedback Rating Distribution (Color-coded histogram/bar chart)
  - Chart 3: Event Popularity vs Capacity (Grouped bar chart)
  - Chart 4: Average Event Rating (Ranked horizontal chart with grade threshold)
  - Chart 5: Department Participation Distribution (Donut / Pie & Bar chart)
  - Chart 6: Event Category Analysis (Participation by domain)
  - Chart 7: Event Performance Score Matrix (Ranked score breakdown)
"""

from typing import Optional
import io
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

# Use non-interactive backend for web/server safety
import matplotlib
matplotlib.use("Agg")

# University theme palette
COLOR_PRIMARY = "#1E3A8A"       # Royal Blue
COLOR_SECONDARY = "#0D9488"     # Teal
COLOR_ACCENT = "#F59E0B"        # Amber
COLOR_DANGER = "#EF4444"        # Crimson / Red
COLOR_SUCCESS = "#10B981"       # Emerald / Green
COLOR_MUTED = "#64748B"         # Slate Grey
PALETTE = ["#1E3A8A", "#0D9488", "#F59E0B", "#8B5CF6", "#EC4899", "#06B6D4", "#10B981", "#64748B"]


def _apply_theme(ax: plt.Axes, title: str, xlabel: str, ylabel: str) -> None:
    """Apply consistent styling across all Matplotlib axes."""
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15, color="#0F172A")
    ax.set_xlabel(xlabel, fontsize=11, fontweight="medium", labelpad=10, color="#334155")
    ax.set_ylabel(ylabel, fontsize=11, fontweight="medium", labelpad=10, color="#334155")
    ax.grid(True, linestyle="--", alpha=0.5, color="#CBD5E1")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#94A3B8")
    ax.spines["bottom"].set_color("#94A3B8")
    ax.tick_params(colors="#334155", labelsize=10)


# ---------------------------------------------------------------------------
# Chart 1 — Event Participation
# ---------------------------------------------------------------------------

def plot_event_participation(df_table: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    """
    Horizontal bar chart showing the number of confirmed participants per event.
    """
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

    if df_table.empty:
        ax.text(0.5, 0.5, "No event participation data available", ha="center", va="center", fontsize=12)
        return fig

    # Take top N by registration
    subset = df_table.sort_values(by="Registered", ascending=True).tail(top_n)

    y_pos = np.arange(len(subset))
    bars = ax.barh(y_pos, subset["Registered"], color=COLOR_PRIMARY, height=0.65, edgecolor="none")

    # Add numeric labels at bar ends
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            ha="left",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="#1E293B",
        )

    # Format event names (truncate if long)
    names = [name if len(name) <= 28 else name[:25] + "..." for name in subset["Event Name"]]
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)

    max_val = subset["Registered"].max() if not subset.empty else 10
    ax.set_xlim(0, max_val * 1.15)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    _apply_theme(ax, f"Top {len(subset)} Events by Student Participation", "Confirmed Registrations", "Campus Event")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Chart 2 — Feedback Distribution (1 to 5)
# ---------------------------------------------------------------------------

def plot_feedback_distribution(df_dist: pd.DataFrame) -> plt.Figure:
    """
    Color-coded rating bar chart showing student satisfaction from Rating 1 (Poor) to 5 (Excellent).
    """
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)

    if df_dist.empty:
        ax.text(0.5, 0.5, "No feedback data available", ha="center", va="center", fontsize=12)
        return fig

    rating_colors = ["#EF4444", "#F97316", "#FBBF24", "#34D399", "#10B981"]

    x = df_dist["Rating"]
    counts = df_dist["Count"]
    bars = ax.bar(x, counts, color=rating_colors, width=0.55, edgecolor="#0F172A", linewidth=0.5)

    # Add values and percentages above bars
    total = counts.sum()
    for bar, pct in zip(bars, df_dist["Percentage"]):
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.5,
            f"{int(h)} ({pct}%)",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#1E293B",
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f"★ {r}\n({df_dist.loc[df_dist['Rating'] == r, 'Label'].values[0]})" for r in x])
    max_c = counts.max() if total > 0 else 5
    ax.set_ylim(0, max_c * 1.25)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    _apply_theme(ax, "Student Feedback Rating Distribution (1 to 5 Stars)", "Rating Scale", "Number of Reviews")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Chart 3 — Event Popularity vs Maximum Capacity
# ---------------------------------------------------------------------------

def plot_popularity_vs_capacity(df_table: pd.DataFrame, top_n: int = 8) -> plt.Figure:
    """
    Grouped bar chart comparing Registered attendees vs Maximum capacity.
    """
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=100)

    if df_table.empty:
        ax.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=12)
        return fig

    subset = df_table.head(top_n)
    indices = np.arange(len(subset))
    bar_width = 0.38

    bars1 = ax.bar(
        indices - bar_width / 2,
        subset["Registered"],
        width=bar_width,
        label="Registered",
        color=COLOR_PRIMARY,
        alpha=0.9,
    )
    bars2 = ax.bar(
        indices + bar_width / 2,
        subset["Capacity"],
        width=bar_width,
        label="Total Capacity",
        color="#CBD5E1",
        edgecolor=COLOR_MUTED,
        linewidth=0.8,
    )

    names = [name if len(name) <= 20 else name[:17] + "..." for name in subset["Event Name"]]
    ax.set_xticks(indices)
    ax.set_xticklabels(names, rotation=25, ha="right")
    ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0")

    _apply_theme(ax, "Event Registration vs Total Seat Capacity", "Event", "Number of Seats")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Chart 4 — Average Event Rating
# ---------------------------------------------------------------------------

def plot_average_ratings(df_summary: pd.DataFrame, min_reviews: int = 1) -> plt.Figure:
    """
    Horizontal bar chart showing average satisfaction score per event.
    """
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=100)

    if df_summary.empty or "Avg_Rating" not in df_summary.columns:
        ax.text(0.5, 0.5, "No rating data available", ha="center", va="center", fontsize=12)
        return fig

    # Filter events that have reviews
    filtered = df_summary[df_summary["Review_Count"] >= min_reviews].sort_values(
        by="Avg_Rating", ascending=True
    )

    if filtered.empty:
        ax.text(0.5, 0.5, "No events meet review criteria", ha="center", va="center", fontsize=12)
        return fig

    y_pos = np.arange(len(filtered))
    colors = [
        COLOR_SUCCESS if r >= 4.5 else (COLOR_SECONDARY if r >= 3.5 else COLOR_ACCENT)
        for r in filtered["Avg_Rating"]
    ]

    bars = ax.barh(y_pos, filtered["Avg_Rating"], color=colors, height=0.6)

    for bar in bars:
        w = bar.get_width()
        ax.text(
            w + 0.05,
            bar.get_y() + bar.get_height() / 2,
            f"{w:.2f} ★",
            ha="left",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="#1E293B",
        )

    names = [name if len(name) <= 26 else name[:23] + "..." for name in filtered["event_name"]]
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xlim(0, 5.4)
    ax.axvline(4.0, color="#10B981", linestyle=":", alpha=0.7, label="Benchmark (4.0 ★)")
    ax.legend(loc="lower right")

    _apply_theme(ax, "Average Student Rating by Event", "Rating (1 to 5 Stars)", "Campus Event")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Chart 5 — Department-Wise Participation
# ---------------------------------------------------------------------------

def plot_department_participation(df_dept: pd.DataFrame) -> plt.Figure:
    """
    Donut chart & horizontal bar representation of department student engagement.
    """
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)

    if df_dept.empty:
        ax.text(0.5, 0.5, "No department participation data", ha="center", va="center", fontsize=12)
        return fig

    sorted_df = df_dept.sort_values(by="Registrations", ascending=True)
    y_pos = np.arange(len(sorted_df))

    bars = ax.barh(y_pos, sorted_df["Registrations"], color=COLOR_SECONDARY, height=0.6)

    for bar, pct in zip(bars, sorted_df["Percentage"]):
        w = bar.get_width()
        ax.text(
            w + 0.4,
            bar.get_y() + bar.get_height() / 2,
            f"{int(w)} ({pct}%)",
            ha="left",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="#1E293B",
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_df["Department"])
    max_val = sorted_df["Registrations"].max() if not sorted_df.empty else 10
    ax.set_xlim(0, max_val * 1.25)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    _apply_theme(ax, "Event Participation Breakdown by Academic Department", "Confirmed Registrations", "Department")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Chart 6 — Category Analysis
# ---------------------------------------------------------------------------

def plot_category_analysis(df_cat: pd.DataFrame) -> plt.Figure:
    """
    Bar chart showing total registrations by event category.
    """
    fig, ax = plt.subplots(figsize=(10, 5), dpi=100)

    if df_cat.empty:
        ax.text(0.5, 0.5, "No category data available", ha="center", va="center", fontsize=12)
        return fig

    sorted_cat = df_cat.sort_values(by="Total Registrations", ascending=False)
    x = np.arange(len(sorted_cat))

    bars = ax.bar(x, sorted_cat["Total Registrations"], color=PALETTE[:len(sorted_cat)], width=0.55)

    for bar, avg_p in zip(bars, sorted_cat["Average per Event"]):
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.8,
            f"{int(h)}\n(avg {avg_p})",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#1E293B",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(sorted_cat["Category"], rotation=20, ha="right")
    max_h = sorted_cat["Total Registrations"].max() if not sorted_cat.empty else 10
    ax.set_ylim(0, max_h * 1.25)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    _apply_theme(ax, "Student Engagement Across Event Categories", "Category", "Total Registrations")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Chart 7 — Event Performance Score Breakdown
# ---------------------------------------------------------------------------

def plot_performance_scores(df_perf: pd.DataFrame, top_n: int = 10) -> plt.Figure:
    """
    Ranked bar chart of Event Performance Scores (0-100) color-coded by tier.
    """
    fig, ax = plt.subplots(figsize=(11, 6), dpi=100)

    if df_perf.empty:
        ax.text(0.5, 0.5, "No performance score data", ha="center", va="center", fontsize=12)
        return fig

    subset = df_perf.head(top_n).sort_values(by="Performance Score", ascending=True)
    y_pos = np.arange(len(subset))

    tier_colors = {
        "Top Performer": COLOR_SUCCESS,
        "Average Performer": COLOR_ACCENT,
        "Needs Improvement": COLOR_DANGER,
    }
    colors = [tier_colors.get(t, COLOR_PRIMARY) for t in subset["Tier"]]

    bars = ax.barh(y_pos, subset["Performance Score"], color=colors, height=0.6)

    for bar, tier in zip(bars, subset["Tier"]):
        w = bar.get_width()
        ax.text(
            w + 0.8,
            bar.get_y() + bar.get_height() / 2,
            f"{w:.1f} ({tier})",
            ha="left",
            va="center",
            fontsize=9,
            fontweight="bold",
            color="#1E293B",
        )

    names = [n if len(n) <= 24 else n[:21] + "..." for n in subset["Event Name"]]
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xlim(0, 115)
    ax.axvline(70, color=COLOR_SUCCESS, linestyle="--", alpha=0.6, label="Top Threshold (70)")
    ax.axvline(40, color=COLOR_DANGER, linestyle="--", alpha=0.6, label="Improvement (40)")
    ax.legend(loc="lower right")

    _apply_theme(ax, "Event Performance Score Matrix (Scale: 0 - 100)", "Composite Performance Score", "Campus Event")
    fig.tight_layout()
    return fig


def figure_to_bytes(fig: plt.Figure, format: str = "png") -> bytes:
    """Export a Matplotlib Figure into binary bytes for downloading in Streamlit."""
    buf = io.BytesIO()
    fig.savefig(buf, format=format, dpi=150, bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()
