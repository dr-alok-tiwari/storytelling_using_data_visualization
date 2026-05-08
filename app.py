"""
Storytelling using Data Visualization - Interactive Streamlit Teaching App
PGDM-BDA Term 1 | Goa Institute of Management
Instructor: Dr. Alok Tiwari

Run locally:
    streamlit run app.py

Compatibility fixes included: Python 3.9+ type hints, PyArrow-safe HTML tables, no Plotly text_auto dependency, and Timestamp-safe Plotly event markers.
V7 upgrade: instructor/student mode, projector mode, 75-minute delivery planner, what-to-say prompts, visual makeover studio, rubrics, exam bank, upload-and-auto-story, role play, teaching-note exports, and model solutions for cases and activities.
"""

from __future__ import annotations

import io
import html
import textwrap
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# -----------------------------------------------------------------------------
# Page configuration and global style
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Storytelling using Data Visualization",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


PRIMARY = "#174A7C"
SECONDARY = "#11A579"
ACCENT = "#F28E2B"
SOFT_BG = "#F7FAFC"
INK = "#1F2937"
MUTED = "#64748B"
DANGER = "#C2410C"
PURPLE = "#7C3AED"


MODULE_COLORS = {
    "Module 1": "#E0F2FE",
    "Module 2": "#ECFDF5",
    "Module 3": "#FFF7ED",
    "Module 4": "#F3E8FF",
}


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: {INK};
        }}
        .block-container {{
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }}
        h1, h2, h3 {{ letter-spacing: -0.02em; }}
        .hero {{
            background: linear-gradient(135deg, #0F3A5E 0%, #176B87 48%, #13A89E 100%);
            color: white;
            padding: 2.1rem 2.4rem;
            border-radius: 28px;
            box-shadow: 0 18px 40px rgba(15, 58, 94, 0.22);
            margin-bottom: 1.2rem;
        }}
        .hero h1 {{
            color: white;
            font-size: 2.35rem;
            margin-bottom: .45rem;
        }}
        .hero p {{
            color: rgba(255,255,255,.92);
            font-size: 1.05rem;
            line-height: 1.55;
            max-width: 1100px;
        }}
        .pill {{
            display: inline-block;
            padding: .32rem .7rem;
            background: rgba(255,255,255,.16);
            color: white;
            border: 1px solid rgba(255,255,255,.24);
            border-radius: 999px;
            margin-right: .35rem;
            margin-bottom: .35rem;
            font-size: .88rem;
        }}
        .card {{
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 22px;
            padding: 1.05rem 1.1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            height: 100%;
        }}
        .card h3 {{ margin-top: 0; color: {PRIMARY}; }}
        .small-card {{
            background: white;
            border: 1px solid #E6EEF6;
            border-radius: 18px;
            padding: .85rem 1rem;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.045);
        }}
        .module-card {{
            border-radius: 20px;
            padding: 1rem;
            border: 1px solid rgba(15,23,42,.08);
            min-height: 188px;
        }}
        .callout {{
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin: .7rem 0;
            border-left: 6px solid {PRIMARY};
            background: #F8FBFE;
            line-height: 1.55;
        }}
        .insight {{ border-left-color: {SECONDARY}; background: #F0FDF4; }}
        .warning {{ border-left-color: {ACCENT}; background: #FFF7ED; }}
        .danger {{ border-left-color: {DANGER}; background: #FFF1F2; }}
        .purple {{ border-left-color: {PURPLE}; background: #F5F3FF; }}
        .tag {{
            display: inline-block;
            background: #EEF2FF;
            color: #3730A3;
            border-radius: 999px;
            padding: .18rem .58rem;
            font-size: .78rem;
            margin: .1rem .15rem .1rem 0;
        }}
        .roadmap-item {{
            background: white;
            border-radius: 18px;
            padding: .85rem;
            border: 1px solid #E5E7EB;
            margin-bottom: .6rem;
            box-shadow: 0 5px 16px rgba(15,23,42,.045);
        }}
        .step-row {{
            display: flex;
            gap: .65rem;
            flex-wrap: wrap;
            align-items: stretch;
            margin: .7rem 0 1rem;
        }}
        .step {{
            flex: 1 1 150px;
            background: white;
            border: 1px solid #DBEAFE;
            border-radius: 18px;
            padding: .85rem;
            text-align: center;
            box-shadow: 0 4px 16px rgba(15, 23, 42, .04);
        }}
        .step .num {{
            width: 30px;
            height: 30px;
            line-height: 30px;
            border-radius: 50%;
            background: {PRIMARY};
            color: white;
            display: inline-block;
            margin-bottom: .3rem;
            font-weight: 700;
        }}
        .metric-box {{
            border-radius: 20px;
            background: linear-gradient(180deg, #FFFFFF, #F8FAFC);
            border: 1px solid #E2E8F0;
            padding: .9rem 1rem;
            box-shadow: 0 6px 18px rgba(2, 6, 23, .05);
            text-align: left;
        }}
        .metric-box .label {{ color: {MUTED}; font-size: .86rem; }}
        .metric-box .value {{ color: {PRIMARY}; font-size: 1.55rem; font-weight: 800; }}
        .metric-box .note {{ color: {SECONDARY}; font-size: .82rem; }}
        .quiz-card {{
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 1rem;
            margin-bottom: .8rem;
        }}
        .quiz-option {{
            display: block;
            padding: .52rem .7rem;
            margin: .38rem 0;
            border-radius: 12px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            line-height: 1.35;
        }}
        .teacher-kit {{
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 1px solid #E2E8F0;
            border-radius: 22px;
            padding: 1.05rem 1.15rem;
            margin: .85rem 0;
            box-shadow: 0 8px 22px rgba(15,23,42,.045);
        }}
        .teacher-kit h4 {{
            margin: .1rem 0 .55rem;
            color: #174A7C;
        }}
        .script-line {{
            background: #FFF7ED;
            border-left: 6px solid #F28E2B;
            border-radius: 16px;
            padding: .9rem 1rem;
            margin: .55rem 0;
            line-height: 1.55;
        }}
        .hint-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: .7rem;
            margin: .7rem 0;
        }}
        .hint-card {{
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            padding: .85rem;
            box-shadow: 0 4px 16px rgba(15,23,42,.04);
        }}
        .stTabs [data-baseweb="tab-list"] {{ gap: .25rem; }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 999px;
            padding: .45rem .75rem;
        }}
        div[data-testid="stExpander"] {{
            border-radius: 18px;
            border: 1px solid #E5E7EB;
            overflow: hidden;
        }}
        .download-card {{
            border-radius: 18px;
            background: #F8FAFC;
            border: 1px dashed #94A3B8;
            padding: 1rem;
        }}

        .safe-table-wrap {{
            width: 100%;
            overflow-x: visible;
            margin: .35rem 0 1rem;
        }}
        .safe-table {{
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            font-size: .88rem;
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            overflow: hidden;
        }}
        .safe-table th {{
            background: #F1F5F9;
            color: #0F3A5E;
            font-weight: 750;
            border: 1px solid #E2E8F0;
            padding: .55rem .5rem;
            text-align: left;
            vertical-align: top;
        }}
        .safe-table td {{
            border: 1px solid #E5E7EB;
            padding: .5rem;
            vertical-align: top;
            white-space: normal;
            overflow-wrap: anywhere;
            line-height: 1.35;
        }}
        .safe-table tr:nth-child(even) td {{ background: #FAFAFA; }}

        .mode-banner {{
            border-radius: 18px;
            padding: .75rem .95rem;
            margin: .5rem 0 1rem;
            background: linear-gradient(90deg, #EEF2FF, #ECFDF5);
            border: 1px solid #C7D2FE;
            color: #1F2937;
            font-weight: 650;
        }}
        .say-card {{
            background: #FFFBEB;
            border: 1px solid #FBBF24;
            border-left: 7px solid #F59E0B;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin: .7rem 0;
            line-height: 1.6;
            box-shadow: 0 8px 22px rgba(245,158,11,.08);
        }}
        .rubric-cell {{
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: .75rem;
            margin: .3rem 0;
            line-height: 1.45;
        }}
        .role-card {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 16px;
            padding: .85rem 1rem;
            margin: .45rem 0;
            line-height: 1.5;
        }}
        .projector-mode .block-container {{ max-width: 1650px; }}
        .projector-mode p, .projector-mode li, .projector-mode .stMarkdown, .projector-mode .callout,
        .projector-mode .quiz-card, .projector-mode .hint-card {{ font-size: 1.12rem !important; }}
        .projector-mode h1 {{ font-size: 2.75rem !important; }}
        .projector-mode h2 {{ font-size: 2.05rem !important; }}
        .projector-mode h3 {{ font-size: 1.55rem !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


def safe_dataframe(df: pd.DataFrame, max_rows: Optional[int] = None) -> None:
    """Render a pandas table without calling st.dataframe.

    This avoids Streamlit's optional PyArrow rendering path, which can fail in
    some Anaconda environments when PyArrow and protobuf/abseil libraries are
    version-mismatched.
    """
    view = df.copy()
    if max_rows is not None:
        view = view.head(max_rows)
    # Keep displayed numeric values readable without changing source data.
    for col in view.select_dtypes(include=["float", "float64", "float32"]).columns:
        view[col] = view[col].map(lambda x: f"{x:,.2f}" if pd.notna(x) else "")
    for col in view.select_dtypes(include=["int", "int64", "int32"]).columns:
        view[col] = view[col].map(lambda x: f"{x:,}" if pd.notna(x) else "")
    html = view.to_html(index=False, escape=True, classes="safe-table", border=0)
    st.markdown(f'<div class="safe-table-wrap">{html}</div>', unsafe_allow_html=True)



# -----------------------------------------------------------------------------
# Data models and core content
# -----------------------------------------------------------------------------
@dataclass
class SessionInfo:
    no: int
    module: str
    title: str
    clos: str
    objective: str
    concept: str
    manager_value: str
    mini_lab: str
    common_mistakes: List[str]
    takeaway: str
    diagram_steps: List[str]


SESSIONS: List[SessionInfo] = [
    SessionInfo(
        1,
        "Module 1",
        "Introduction: Why Data Visualization and Storytelling Matter",
        "CLO1",
        "Explain why visuals need narrative to support managerial decisions.",
        "A visualization is not merely a picture of data; it is a decision aid. Good visual storytelling links context, evidence, interpretation, and action so that a manager can understand what changed, why it matters, and what should be done next.",
        "Managers rarely need every data point. They need the pattern, the risk, the trade-off, and the recommended action. The storyteller’s job is to reduce confusion without reducing truth.",
        "Compare a table and a bar chart, then write a one-sentence decision message from the same data.",
        ["Showing a chart without a business question", "Using a decorative visual that does not clarify action", "Reporting numbers without explaining implications"],
        "A good visual story turns data into a decision conversation.",
        ["Business Context", "Data Evidence", "Visual Pattern", "Managerial Insight", "Action"],
    ),
    SessionInfo(
        2,
        "Module 1",
        "Mapping Data to Visual Forms",
        "CLO1, CLO2",
        "Select appropriate chart types based on data type and business question.",
        "Chart selection begins with the question. Comparison, trend, distribution, relationship, composition, and deviation each require different visual encodings. The best chart is the one that makes the intended comparison easiest to see.",
        "Incorrect chart selection can lead managers toward slow or wrong interpretation. Matching data structure to visual form improves credibility and reduces cognitive effort.",
        "Choose a chart type for five business questions and justify each choice in one sentence.",
        ["Using pie charts for too many categories", "Using line charts for unordered categories", "Using stacked bars when exact comparison is needed"],
        "Start with the question, then choose the chart; do not start with the software menu.",
        ["Question", "Data Type", "Encoding", "Chart", "Decision"],
    ),
    SessionInfo(
        3,
        "Module 1",
        "Coordinate Systems, Axes, and Scales",
        "CLO1, CLO2",
        "Evaluate how axes and scales influence interpretation.",
        "Axes and scales frame the visual argument. Truncated axes, inconsistent intervals, and inappropriate transformations can exaggerate or hide differences. Ethical visualization requires scale choices that support truthful interpretation.",
        "Strategic decisions depend on magnitude. A misleading axis can make a small difference look urgent or a serious change look harmless.",
        "Redesign a chart with a truncated axis and write how the interpretation changes.",
        ["Truncating a bar chart axis", "Using unequal time intervals", "Hiding the baseline when magnitude matters"],
        "Scale is part of the message; use it responsibly.",
        ["Raw Values", "Scale Choice", "Visual Impression", "Interpretation", "Trust"],
    ),
    SessionInfo(
        4,
        "Module 1",
        "Color, Emphasis, and Visual Attention",
        "CLO2",
        "Use color and emphasis to guide attention without clutter.",
        "Color should serve meaning. It can group, highlight, warn, and direct the eye. Overuse of color weakens attention because everything appears equally important.",
        "Executives scan dashboards quickly. Clear emphasis helps them locate exceptions, risks, and priorities within seconds.",
        "Improve a multi-color chart by using neutral colors and one intentional highlight.",
        ["Using rainbow color without meaning", "Highlighting too many elements", "Ignoring contrast and readability"],
        "Use color sparingly: most items can be quiet; the message should be visible.",
        ["Audience Goal", "Neutral Base", "Highlight", "Label", "Takeaway"],
    ),
    SessionInfo(
        5,
        "Module 2",
        "Visualizing Amounts with a Message",
        "CLO2, CLO3",
        "Create comparison visuals that communicate a clear business message.",
        "Amounts are often compared through bars, dots, heatmaps, and ranked views. The story improves when the chart title states the insight rather than merely naming the variables.",
        "Managers compare regions, products, teams, and costs. A good comparison visual should make the strongest and weakest performers immediately visible.",
        "Build a ranked bar chart and convert its title into an action-oriented headline.",
        ["Unsorted bars", "Too many labels", "A title that only says 'Sales by Region'"],
        "A comparison chart should answer: who is ahead, who is behind, and what needs attention?",
        ["Metric", "Comparator", "Rank", "Exception", "Message"],
    ),
    SessionInfo(
        6,
        "Module 2",
        "Visualizing Distributions and Variation",
        "CLO2, CLO3",
        "Explain spread, variation, and risk using distribution visuals.",
        "Distribution charts show how values vary, not just what the average is. Histograms, box plots, and density views reveal skew, outliers, and consistency.",
        "Averages can hide operational risk. Two branches may have the same average service time but very different variability and customer experience.",
        "Interpret a histogram and identify whether the managerial issue is average performance, spread, or outliers.",
        ["Reporting only the mean", "Ignoring outliers", "Using too many histogram bins"],
        "Variation is often the real management story.",
        ["Values", "Spread", "Outliers", "Risk", "Decision"],
    ),
    SessionInfo(
        7,
        "Module 2",
        "Visualizing Proportions and Composition",
        "CLO2, CLO3",
        "Show contribution and share without causing visual confusion.",
        "Composition visuals explain how a whole is divided into parts. Stacked bars, 100% stacked bars, treemaps, and carefully limited pies can show contribution, but precise comparison becomes difficult when there are too many segments.",
        "Managers often need to know what contributes most to revenue, cost, delay, or risk. Composition charts should reveal the largest drivers clearly.",
        "Compare a pie chart and a sorted bar chart for category contribution; decide which communicates better.",
        ["Pie charts with many slices", "Unlabeled composition charts", "Using composition when ranking is the actual question"],
        "Use composition charts when the part-to-whole relationship is the message.",
        ["Whole", "Parts", "Share", "Driver", "Priority"],
    ),
    SessionInfo(
        8,
        "Module 2",
        "Critiquing and Reframing Weak Visual Stories",
        "CLO1–CLO3",
        "Diagnose weak visuals and redesign them into clearer stories.",
        "Chart critique is a disciplined process: identify the question, inspect the encoding, test the title, examine clutter, check for misleading framing, and rewrite the takeaway.",
        "Managers are often shown dashboards created by others. The ability to critique visual evidence is as important as the ability to create it.",
        "Use a critique checklist to improve a weak dashboard screenshot or synthetic chart.",
        ["Criticizing aesthetics only", "Ignoring the decision context", "Fixing colors but not fixing the story"],
        "A weak visual can often be saved by clarifying the question and sharpening the message.",
        ["Diagnose", "Remove Clutter", "Correct Encoding", "Rewrite Title", "Recommend"],
    ),
    SessionInfo(
        9,
        "Module 3",
        "Visualizing Relationships and Building Insight",
        "CLO2, CLO3",
        "Use relationship visuals to move from pattern observation to insight.",
        "Scatter plots and bubble charts help reveal association, segmentation, and exceptions. A relationship visual becomes meaningful when the storyteller explains what the pattern suggests and what should be investigated.",
        "Relationship visuals support questions such as: does discount improve sales, does satisfaction relate to retention, or does waiting time affect complaints?",
        "Create a scatter plot and write one cautious managerial interpretation without overstating causality.",
        ["Treating correlation as causation", "Ignoring clusters", "Hiding outliers that may be important"],
        "A relationship chart suggests where to ask better business questions.",
        ["Variables", "Pattern", "Segment", "Exception", "Hypothesis"],
    ),
    SessionInfo(
        10,
        "Module 3",
        "Visualizing Time Series and Change Over Time",
        "CLO3, CLO4",
        "Tell a meaningful story of trend, seasonality, change, and turning points.",
        "Time-series storytelling focuses on movement. Good line charts show direction, rate of change, comparison, seasonality, and important events.",
        "Managers need to know whether performance is improving, declining, stable, seasonal, or disrupted by an intervention.",
        "Annotate a time-series chart to explain a turning point and its possible business implication.",
        ["Using bars for long time series", "Ignoring seasonality", "Not marking interventions or events"],
        "A time-series chart should explain what changed and why that change matters.",
        ["Baseline", "Trend", "Change Point", "Explanation", "Action"],
    ),
    SessionInfo(
        11,
        "Module 3",
        "Dashboard Storytelling for Business Audiences",
        "CLO2, CLO3, CLO4",
        "Design dashboard layouts for executive interpretation and action.",
        "A dashboard is a structured argument, not a collection of charts. It should show context, key metrics, comparison, exception, diagnosis, and recommended action.",
        "Executive dashboards must support quick prioritization. Layout, hierarchy, and concise labels matter because attention is limited.",
        "Create an executive dashboard wireframe with one decision question and three supporting visuals.",
        ["Adding too many charts", "Mixing unrelated KPIs", "No clear top-level decision question"],
        "A dashboard should guide the eye from priority to explanation to action.",
        ["Decision Question", "KPI", "Comparison", "Diagnosis", "Action"],
    ),
    SessionInfo(
        12,
        "Module 3",
        "Annotation, Titles, Captions, and Narrative Flow",
        "CLO3, CLO4",
        "Use titles, captions, and annotations to guide interpretation.",
        "Narrative text turns a chart from a display into an explanation. Strong titles state the insight; annotations explain important moments; captions clarify interpretation and limitations.",
        "A busy manager may read the title first and inspect the chart second. Titles and annotations must therefore carry the message responsibly.",
        "Rewrite three chart titles from descriptive to action-oriented and add one annotation.",
        ["Using vague titles", "Annotating everything", "Writing captions that repeat the obvious"],
        "Text is part of the visualization; use it to guide, not decorate.",
        ["Observation", "Insight Title", "Annotation", "Implication", "Decision"],
    ),
    SessionInfo(
        13,
        "Module 4",
        "Common Pitfalls in Data Storytelling",
        "CLO1, CLO2",
        "Identify and correct common errors in visual storytelling.",
        "Common pitfalls include misleading scales, decorative overload, chart junk, poor sequencing, weak titles, hidden uncertainty, and visuals that do not connect to action.",
        "Poor visual storytelling can misdirect decisions, waste time, or reduce trust in analytics.",
        "Use the pitfall checklist to diagnose and correct three weak visuals.",
        ["Mistaking beauty for clarity", "Removing context", "Overclaiming from limited evidence"],
        "Ethical and useful visualization requires clarity, context, and humility.",
        ["Pitfall", "Risk", "Correction", "Message", "Trust"],
    ),
    SessionInfo(
        14,
        "Module 4",
        "Strategy Communication through Visual Stories",
        "CLO3, CLO4",
        "Translate analysis into strategic implication and recommendation.",
        "Strategic visual storytelling connects evidence to competitive choices. The narrative should clarify the business situation, the option space, the trade-off, and the recommended path.",
        "Senior leaders need visual stories that distinguish noise from strategic signals and convert analysis into choices.",
        "Create a recommendation storyboard for a market, product, or operational strategy decision.",
        ["Stopping at insight without recommendation", "Ignoring trade-offs", "Presenting too many disconnected charts"],
        "A strategic visual story should end with a clear recommendation and rationale.",
        ["Context", "Strategic Question", "Evidence", "Trade-off", "Recommendation"],
    ),
    SessionInfo(
        15,
        "Module 4",
        "Integrated Storytelling with Data Workshop",
        "CLO1–CLO4",
        "Build an end-to-end visual story from business problem to action.",
        "The integrated workshop combines question framing, chart selection, visual design, annotation, dashboard logic, insight writing, and recommendation. The focus is not on making many charts, but on creating a coherent decision narrative.",
        "This is the closest classroom simulation of managerial analytics communication.",
        "Choose a dataset, build three visuals, write a storyboard, and present the recommendation.",
        ["Creating visuals before framing the problem", "Using too many charts", "Weak link between evidence and action"],
        "A complete data story connects context, evidence, insight, implication, and action.",
        ["Problem", "Data", "Visuals", "Narrative", "Recommendation"],
    ),
    SessionInfo(
        16,
        "Module 4",
        "Guest Session: Healthcare Data Visualization",
        "CLO2–CLO4",
        "Apply visualization and storytelling principles to healthcare dashboards.",
        "Healthcare visualization requires careful attention to patient flow, operational efficiency, risk, ethics, and interpretability. Dashboards should serve clinicians, administrators, and patients without creating false certainty.",
        "Healthcare managers need dashboards that clarify capacity, waiting time, bed occupancy, patient outcomes, and resource allocation.",
        "Interpret a healthcare dashboard and write an insight note for hospital operations.",
        ["Showing sensitive data without context", "Ignoring denominator effects", "Using operational metrics without patient meaning"],
        "Healthcare visual stories must combine clarity, caution, and action orientation.",
        ["Patient Flow", "Metric", "Risk", "Capacity", "Action"],
    ),
]


# -----------------------------------------------------------------------------
# Synthetic datasets
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def retail_data(seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    regions = ["North", "South", "East", "West", "Central"]
    categories = ["Electronics", "Grocery", "Apparel", "Home", "Beauty"]
    months = pd.date_range("2025-01-01", periods=12, freq="MS")
    rows = []
    for month_idx, month in enumerate(months):
        season = 1 + 0.18 * np.sin((month_idx + 1) / 12 * 2 * np.pi)
        for region in regions:
            for cat in categories:
                base = rng.integers(70, 190)
                regional_factor = 1 + regions.index(region) * 0.05
                sales = int(base * season * regional_factor + rng.normal(0, 12))
                profit = int(sales * rng.uniform(0.12, 0.28))
                discount = float(np.clip(rng.normal(10, 4), 0, 25))
                satisfaction = float(np.clip(72 + profit / 30 - discount * 0.6 + rng.normal(0, 6), 45, 98))
                rows.append([month, region, cat, sales, profit, discount, satisfaction])
    return pd.DataFrame(rows, columns=["Month", "Region", "Category", "Sales", "Profit", "Discount", "Satisfaction"])


@st.cache_data(show_spinner=False)
def marketing_data(seed: int = 8) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    channels = ["Search", "Social", "Email", "Events", "Referral", "Display"]
    rows = []
    for channel in channels:
        spend = rng.integers(50, 240) * 1000
        impressions = int(spend * rng.uniform(15, 42))
        ctr = rng.uniform(0.012, 0.07)
        clicks = int(impressions * ctr)
        conversion_rate = rng.uniform(0.015, 0.09)
        conversions = int(clicks * conversion_rate)
        revenue = int(conversions * rng.integers(1800, 7200))
        rows.append([channel, spend, impressions, clicks, conversions, revenue, ctr * 100, conversion_rate * 100])
    return pd.DataFrame(rows, columns=["Channel", "Spend", "Impressions", "Clicks", "Conversions", "Revenue", "CTR", "Conversion Rate"])


@st.cache_data(show_spinner=False)
def operations_data(seed: int = 9) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    plants = ["Plant A", "Plant B", "Plant C", "Plant D", "Plant E"]
    start_date = pd.Timestamp("2025-01-06")
    rows = []
    for plant in plants:
        for week in range(1, 27):
            date = start_date + pd.Timedelta(days=(week - 1) * 7)
            delay = max(0, rng.normal(7 + plants.index(plant) * 1.1, 3))
            defect_rate = max(0.2, rng.normal(2.5 + delay * 0.08, 0.8))
            output = max(60, rng.normal(180 - delay * 3, 18))
            overtime = max(0, rng.normal(delay * 1.8, 5))
            rows.append([date, plant, week, delay, defect_rate, output, overtime])
    return pd.DataFrame(rows, columns=["Date", "Plant", "Week", "Delay Days", "Defect Rate", "Output", "Overtime Hours"])


@st.cache_data(show_spinner=False)
def finance_data(seed: int = 10) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    depts = ["Sales", "Marketing", "Operations", "HR", "IT", "Finance"]
    rows = []
    for dept in depts:
        budget = rng.integers(40, 150) * 100000
        actual = int(budget * rng.uniform(0.82, 1.25))
        savings = budget - actual
        risk = "High" if actual > budget * 1.12 else "Moderate" if actual > budget else "Low"
        rows.append([dept, budget, actual, savings, risk])
    return pd.DataFrame(rows, columns=["Department", "Budget", "Actual", "Variance", "Risk"])


@st.cache_data(show_spinner=False)
def healthcare_data(seed: int = 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    departments = ["Emergency", "OPD", "ICU", "Radiology", "Surgery", "Pharmacy"]
    dates = pd.date_range("2025-01-01", periods=90, freq="D")
    rows = []
    for date in dates:
        dow = date.dayofweek
        weekend_factor = 0.85 if dow >= 5 else 1.0
        for dept in departments:
            patients = int(max(10, rng.normal(85 + departments.index(dept) * 7, 18) * weekend_factor))
            wait = float(np.clip(rng.normal(25 + departments.index(dept) * 4, 9), 5, 90))
            occupancy = float(np.clip(rng.normal(70 + departments.index(dept) * 3, 11), 35, 99))
            readmit = float(np.clip(rng.normal(6 + departments.index(dept) * .4, 1.8), 1, 15))
            rows.append([date, dept, patients, wait, occupancy, readmit])
    return pd.DataFrame(rows, columns=["Date", "Department", "Patients", "Avg Wait Time", "Bed Occupancy", "Readmission Rate"])


@st.cache_data(show_spinner=False)
def learning_data(seed: int = 12) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sections = ["A", "B", "C"]
    rows = []
    for i in range(1, 121):
        section = rng.choice(sections)
        attendance = float(np.clip(rng.normal(82, 12), 45, 100))
        practice = int(np.clip(rng.normal(7, 2.3), 1, 12))
        quiz = float(np.clip(45 + attendance * .25 + practice * 3 + rng.normal(0, 8), 25, 100))
        project = float(np.clip(50 + quiz * .35 + rng.normal(0, 10), 30, 100))
        rows.append([f"S{i:03d}", section, attendance, practice, quiz, project])
    return pd.DataFrame(rows, columns=["Student", "Section", "Attendance", "Practice Hours", "Quiz Score", "Project Score"])


@st.cache_data(show_spinner=False)
def regional_data(seed: int = 13) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    regions = ["North", "South", "East", "West", "Central", "North-East"]
    rows = []
    for region in regions:
        market_size = rng.integers(120, 420)
        share = float(np.clip(rng.normal(18, 7), 4, 42))
        growth = float(np.clip(rng.normal(9, 5), -4, 24))
        competition = rng.integers(3, 13)
        attractiveness = share * .4 + growth * 1.5 + market_size * .035 - competition * 1.8
        rows.append([region, market_size, share, growth, competition, attractiveness])
    return pd.DataFrame(rows, columns=["Region", "Market Size", "Market Share", "Growth Rate", "Competitors", "Attractiveness"])


@st.cache_data(show_spinner=False)
def time_series_revenue(seed: int = 14) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    months = pd.date_range("2023-01-01", periods=36, freq="MS")
    rows = []
    base = 120
    for i, month in enumerate(months):
        intervention = 18 if i >= 22 else 0
        seasonality = 14 * np.sin(2 * np.pi * i / 12)
        trend = i * 2.1
        revenue = base + trend + seasonality + intervention + rng.normal(0, 7)
        cost = 80 + i * 1.4 + 5 * np.sin(2 * np.pi * (i + 2) / 12) + rng.normal(0, 5)
        rows.append([month, revenue, cost, intervention > 0])
    return pd.DataFrame(rows, columns=["Month", "Revenue", "Cost", "Post Campaign"])


def get_dataset(name: str) -> pd.DataFrame:
    mapping = {
        "Retail Sales": retail_data(),
        "Marketing Campaign": marketing_data(),
        "Operations Delays": operations_data(),
        "Financial Expenses": finance_data(),
        "Healthcare Patient Flow": healthcare_data(),
        "Student Learning Analytics": learning_data(),
        "Regional Strategy": regional_data(),
        "Time-Series Revenue": time_series_revenue(),
    }
    return mapping[name].copy()


DATASET_OPTIONS = [
    "Retail Sales",
    "Marketing Campaign",
    "Operations Delays",
    "Financial Expenses",
    "Healthcare Patient Flow",
    "Student Learning Analytics",
    "Regional Strategy",
    "Time-Series Revenue",
]


# -----------------------------------------------------------------------------
# UI helpers
# -----------------------------------------------------------------------------
def hero(title: str, subtitle: str, pills: Optional[List[str]] = None) -> None:
    pill_html = "".join([f'<span class="pill">{p}</span>' for p in (pills or [])])
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
            <div>{pill_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def callout(title: str, body: str, kind: str = "callout") -> None:
    st.markdown(
        f"""
        <div class="callout {kind}">
            <b>{title}</b><br>{body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_box(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str, tags: Optional[List[str]] = None) -> None:
    tag_html = "".join([f'<span class="tag">{t}</span>' for t in (tags or [])])
    st.markdown(
        f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{body}</p>
            <div>{tag_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def process_diagram(steps: List[str]) -> None:
    html = '<div class="step-row">'
    for i, step in enumerate(steps, start=1):
        html += f'<div class="step"><span class="num">{i}</span><br><b>{step}</b></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def nice_title(text: str) -> str:
    return text.replace("_", " ").title()


# -----------------------------------------------------------------------------
# One-stop teaching enrichments: concept stories, activity bank, and gallery data
# -----------------------------------------------------------------------------
SESSION_STORY_CONTEXT: Dict[int, Dict[str, str]] = {
    1: {
        "scene": "A leadership team opens a quarterly review and sees ten tables of numbers. Everyone reads a different column, and the discussion moves in five directions.",
        "data_moment": "The same numbers are converted into a single ranked visual with a clear headline: two regions are driving growth, while one region needs diagnosis.",
        "teaching_story": "The class should notice that the chart did not create new data; it created shared attention. The story begins when the presenter connects the visual pattern to a managerial question: where should time, budget, and follow-up be allocated?",
        "student_hook": "Ask students to imagine they have only ninety seconds in front of a CEO. Which one sentence would they say before showing the chart?",
    },
    2: {
        "scene": "A student creates a pie chart, a line chart, and a scatter plot from the same sales dataset, then asks which one is best.",
        "data_moment": "The correct answer depends on the question: ranking needs bars, time needs lines, association needs scatter plots, and part-to-whole needs composition views.",
        "teaching_story": "This concept is like choosing the right lens. A microscope, telescope, and camera are all useful, but each serves a different purpose. Chart selection works the same way.",
        "student_hook": "Give students five business questions and ask them to defend the chart choice before opening any software.",
    },
    3: {
        "scene": "Two branches differ by only four satisfaction points, but a truncated axis makes the weaker branch look like a crisis.",
        "data_moment": "When the axis is restored to the proper context, the story changes from emergency to modest performance gap.",
        "teaching_story": "Axes are not background decoration; they are part of the argument. A scale can quietly exaggerate, minimize, or clarify the business situation.",
        "student_hook": "Ask students whether the chart is technically accurate but communicatively unfair. This opens the ethics discussion naturally.",
    },
    4: {
        "scene": "A dashboard uses bright colors for every product, region, and alert. Nothing looks secondary, so nothing feels important.",
        "data_moment": "After using neutral colors for context and one accent for the priority category, the audience immediately knows where to look.",
        "teaching_story": "Color is attention currency. Spend it carefully. In business communication, the goal is not to make the chart colorful; the goal is to make the message visible.",
        "student_hook": "Show students a multi-color chart and ask: what should I look at first? If answers differ, the design has failed.",
    },
    5: {
        "scene": "A manager asks which region deserves support. The first chart lists all regions alphabetically, forcing the audience to calculate rank mentally.",
        "data_moment": "Sorting the values and rewriting the title turns the chart into a clear comparison: leaders, laggards, and the managerial priority become visible.",
        "teaching_story": "Amount charts should reduce the effort of comparison. A good ranked chart lets the audience see the answer before they start reading every label.",
        "student_hook": "Ask students to replace the title 'Sales by Region' with a headline that tells the managerial meaning.",
    },
    6: {
        "scene": "Two service desks report the same average waiting time. One is consistent; the other swings between very fast and very slow service.",
        "data_moment": "A distribution chart reveals the hidden difference: variation and outliers, not the mean, explain the customer experience risk.",
        "teaching_story": "The average is a summary, not the whole story. Managers need to know whether performance is predictable, risky, skewed, or affected by exceptional cases.",
        "student_hook": "Ask students which team they would trust more if both teams have the same average but different spread.",
    },
    7: {
        "scene": "A revenue report says total sales increased, but leadership wants to know what contributed to the increase.",
        "data_moment": "A composition view shows whether growth came from one category, many balanced categories, or a risky overdependence on a single segment.",
        "teaching_story": "Composition is about explaining the whole through its parts. It is useful when the business question is contribution, dependency, or portfolio balance.",
        "student_hook": "Ask students when a pie chart is acceptable and when a sorted bar chart would be more honest and readable.",
    },
    8: {
        "scene": "A dashboard looks impressive, but the audience cannot identify the problem, priority, or recommendation.",
        "data_moment": "A critique checklist exposes the real weakness: unclear question, weak title, cluttered encoding, and no action path.",
        "teaching_story": "Critique is not about insulting a chart; it is about improving the quality of decision support. A strong analyst can diagnose weak visuals respectfully and precisely.",
        "student_hook": "Ask students to critique the chart in three layers: truthfulness, clarity, and usefulness for action.",
    },
    9: {
        "scene": "A marketing team notices that higher discounts sometimes produce higher sales, but not always.",
        "data_moment": "A scatter plot shows clusters and exceptions, suggesting that category context matters more than a simple discount rule.",
        "teaching_story": "Relationship charts are hypothesis builders. They reveal association, segmentation, and exceptions, but they do not automatically prove causation.",
        "student_hook": "Ask students to write one cautious insight and one follow-up question instead of making a causal claim.",
    },
    10: {
        "scene": "Revenue rises after a campaign launch, but the team also observes seasonal demand and cost changes.",
        "data_moment": "A time-series chart with an event marker helps the audience separate trend, seasonality, and possible intervention effects.",
        "teaching_story": "Time-series storytelling is the story of movement. The audience wants to know what changed, when it changed, whether the change is sustained, and what may explain it.",
        "student_hook": "Ask students to annotate one turning point and write a sentence beginning with: 'After this point...'.",
    },
    11: {
        "scene": "An executive receives a dashboard with twenty charts and no hierarchy. The dashboard contains information but does not create direction.",
        "data_moment": "Rearranging the dashboard around a decision question, KPI row, diagnostic visuals, and action note creates a management-ready view.",
        "teaching_story": "A dashboard is a structured argument. It should first orient the audience, then diagnose the situation, then support an action conversation.",
        "student_hook": "Ask students to identify the first thing an executive should see within five seconds.",
    },
    12: {
        "scene": "A line chart is titled 'Monthly Revenue'. It is accurate, but it does not tell the audience what matters.",
        "data_moment": "The title is rewritten as an insight, and an annotation marks the campaign launch. The chart now explains the business moment.",
        "teaching_story": "Text is not separate from visualization. Titles, captions, and annotations act as signposts that guide interpretation without overclaiming.",
        "student_hook": "Ask students to write three titles: descriptive, analytical, and action-oriented. Then compare which one helps decision-making most.",
    },
    13: {
        "scene": "A report uses dramatic colors, 3D shapes, missing baselines, and a confident recommendation from limited evidence.",
        "data_moment": "Removing chart junk and adding context changes the story from persuasive-looking to trustworthy and decision-ready.",
        "teaching_story": "The danger in data storytelling is not only being unclear; it is being clear in the wrong direction. Responsible design protects both insight and trust.",
        "student_hook": "Ask students to find one issue that affects truth, one that affects clarity, and one that affects actionability.",
    },
    14: {
        "scene": "A strategy team must choose between a large saturated market and a smaller high-growth market.",
        "data_moment": "A strategic visual compares market size, growth, competition, and current share, making trade-offs visible rather than hidden in paragraphs.",
        "teaching_story": "Strategic visualization is about choice. The best story does not simply show performance; it explains options, trade-offs, risk, and recommended direction.",
        "student_hook": "Ask students to write the recommendation and then name the trade-off they are accepting.",
    },
    15: {
        "scene": "Students have a dataset, several charts, and many observations. The challenge is to create one coherent presentation.",
        "data_moment": "The strongest output follows a sequence: business question, selected evidence, visual pattern, managerial implication, recommendation, and limitation.",
        "teaching_story": "An integrated data story is not a chart collection. It is a decision narrative in which every visual has a job and every sentence moves the audience closer to action.",
        "student_hook": "Ask each group to delete one chart. If the story becomes clearer, the removed chart was not necessary.",
    },
    16: {
        "scene": "A hospital dashboard shows occupancy, waiting time, patient volume, and readmission rate, but each audience reads it differently.",
        "data_moment": "The dashboard becomes useful when the story is adapted for administrators, clinicians, and operational teams with careful attention to ethics and context.",
        "teaching_story": "Healthcare visualization is high-responsibility storytelling. Metrics represent patient experience, resource pressure, and safety signals, so false certainty must be avoided.",
        "student_hook": "Ask students what extra context they need before recommending action on a healthcare metric.",
    },
}


def _story_teaching_kit(sess: SessionInfo, scene: str, data_moment: str, teaching_story: str, student_hook: str) -> Dict[str, str]:
    chart_hint = {
        1: "Use a ranked bar chart: Region on the y-axis, revenue or growth on the x-axis, sorted from high to low.",
        2: "Show four thumbnails: bar for comparison, line for time, scatter for relationship, and stacked bar for composition.",
        3: "Show the same bar chart twice: one with a truncated axis and one with a full baseline.",
        4: "Show a neutral chart with one accent color to highlight the key category.",
        5: "Use a sorted bar or dot plot with an insight headline instead of a variable-name title.",
        6: "Use a histogram or box plot to show spread, skew, and outliers behind the average.",
        7: "Use a 100% stacked bar for share comparison and a sorted bar when exact contribution matters.",
        8: "Show a weak chart beside a reframed chart and ask students what became clearer.",
        9: "Use a scatter plot with clusters, outliers, and a cautious interpretation note.",
        10: "Use a line chart with one event marker and one annotation explaining the turning point.",
        11: "Use a dashboard wireframe: KPI row first, diagnostic visuals second, action note last.",
        12: "Show the same visual with three titles: descriptive, analytical, and action-oriented.",
        13: "Show a misleading chart and ask students to identify truth, clarity, and action problems.",
        14: "Use a matrix or bubble chart to compare options, trade-offs, market attractiveness, and risk.",
        15: "Use three visuals only: context, diagnosis, and recommendation; remove everything else.",
        16: "Use a healthcare dashboard with volume, waiting time, occupancy, and safety indicators together.",
    }.get(sess.no, "Use the simplest visual that makes the intended comparison easy to see.")
    example = {
        1: "Example: Instead of saying 'these are regional sales numbers', say 'West and South are creating most of the growth; Central needs diagnosis before the next budget cycle'.",
        2: "Example: For 'Which region is highest?', choose a ranked bar. For 'How did revenue change?', choose a line chart.",
        3: "Example: A satisfaction movement from 82 to 86 should not be shown as a dramatic collapse or surge unless the scale supports that reading.",
        4: "Example: Keep all regions grey and highlight only the region that requires action.",
        5: "Example: Replace 'Revenue by Region' with 'West leads revenue, but Central is the immediate recovery priority'.",
        6: "Example: Two branches may both average 15 minutes, but one has stable service and the other has extreme delays.",
        7: "Example: If one category contributes 68% of revenue, the story may be growth strength as well as dependency risk.",
        8: "Example: A beautiful dashboard is weak if the manager cannot identify the decision within five seconds.",
        9: "Example: A discount-sales relationship may reveal clusters by product type, not a universal discount rule.",
        10: "Example: Revenue rising after a campaign is not enough; students must check seasonality and sustained change.",
        11: "Example: Executive dashboards should begin with 'Are we on track?' before showing detailed diagnosis.",
        12: "Example: 'Monthly Revenue' describes; 'Revenue recovered after April campaign' interprets; 'Continue campaign in South and diagnose Central' recommends.",
        13: "Example: A 3D pie chart may look impressive but makes share comparison harder and can distort interpretation.",
        14: "Example: A smaller market with high growth may be more attractive than a large market with intense competition.",
        15: "Example: The final story should read like: problem, evidence, insight, risk, recommendation, next step.",
        16: "Example: Average waiting time needs patient volume, department mix, and capacity context before action is recommended.",
    }.get(sess.no, f"Example: Use the session concept to convert an observation into a recommendation: {sess.takeaway}")
    expected_answer = {
        1: "Students should say that visuals focus attention and support decisions, but the story gives meaning.",
        2: "Students should defend the chart choice by referring to the business question and data type.",
        3: "Students should notice that axes can change perceived urgency and ethical interpretation.",
        4: "Students should identify where the viewer should look first and why.",
        5: "Students should move from ranking categories to naming the managerial priority.",
        6: "Students should explain why averages hide variation, risk, and outliers.",
        7: "Students should distinguish between absolute totals and proportional contribution.",
        8: "Students should critique the visual respectfully using clarity, truthfulness, and actionability.",
        9: "Students should describe association carefully and avoid unsupported causal claims.",
        10: "Students should discuss trend, turning point, seasonality, and possible explanations.",
        11: "Students should identify hierarchy: headline KPI, diagnosis, and action cue.",
        12: "Students should see that titles and annotations guide interpretation.",
        13: "Students should detect exaggeration, clutter, missing context, and overclaiming.",
        14: "Students should connect visual evidence to strategic options and trade-offs.",
        15: "Students should build a coherent story, not a chart collection.",
        16: "Students should interpret healthcare metrics with caution, context, and stakeholder sensitivity.",
    }.get(sess.no, "Students should connect the visible pattern to managerial meaning.")
    return {
        "opening": f"Let us treat this session as a management meeting, not a software class. The question is: how does '{sess.title}' help a manager make a better decision?",
        "board_note": f"Write this on the board: Context → Evidence → Pattern → Insight → Implication → Action. Then connect it to the session takeaway: {sess.takeaway}",
        "chart_hint": chart_hint,
        "example": example,
        "ask": student_hook,
        "expected": expected_answer,
        "misconception": f"Do not let students stop at 'the chart looks good'. Push them to explain the business meaning. Also watch for this common mistake: {sess.common_mistakes[0] if sess.common_mistakes else 'ignoring decision context'}.",
        "activity": f"Two-minute activity: ask students to write one observation, one insight, and one recommended action for the visual shown in this session. Then ask them to remove any sentence that is not supported by evidence.",
        "wrap": f"Close with this line: '{sess.takeaway}'",
    }


def render_quiz_card(i: int, q: Dict[str, str], show_tags: bool = False) -> None:
    tags = ""
    if show_tags:
        tags = f"<span class='tag'>Session {html.escape(str(q.get('session', '')))}</span><span class='tag'>{html.escape(str(q.get('clo', '')))}</span><br>"
    option_html = "".join(
        f"<span class='quiz-option'>{html.escape(part.strip())}</span>"
        for part in str(q.get("options", "")).split("|")
        if part.strip()
    )
    st.markdown(
        f"<div class='quiz-card'><b>Q{i}. {html.escape(str(q.get('q', '')))}</b><br>{tags}<div style='margin-top:.65rem'>{option_html}</div></div>",
        unsafe_allow_html=True,
    )


def render_concept_story(sess: SessionInfo) -> None:
    story = SESSION_STORY_CONTEXT.get(sess.no, {})
    scene = story.get("scene", f"A manager is trying to understand the topic: {sess.title}.")
    data_moment = story.get("data_moment", sess.concept)
    teaching_story = story.get("teaching_story", sess.manager_value)
    student_hook = story.get("student_hook", "Ask students to convert the observation into one action recommendation.")
    kit = _story_teaching_kit(sess, scene, data_moment, teaching_story, student_hook)

    st.markdown("### 📖 Tell me the story")
    callout("Scene", scene, "purple")
    callout("Data moment", data_moment, "insight")
    st.markdown(
        f"""
**Classroom story:** {teaching_story}

**Managerial lesson:** {sess.takeaway}
        """.strip()
    )
    process_diagram(["Situation", "Evidence", "Pattern", "Meaning", "Action"])

    st.markdown("#### 🧑‍🏫 Ready-to-teach guide")
    st.markdown(f"<div class='script-line'><b>Opening line:</b> {html.escape(kit['opening'])}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='script-line'><b>Board note:</b> {html.escape(kit['board_note'])}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='script-line'><b>Chart to show:</b> {html.escape(kit['chart_hint'])}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='script-line'><b>Example to narrate:</b> {html.escape(kit['example'])}</div>", unsafe_allow_html=True)

    st.markdown("#### 💡 Hints you can use while teaching")
    hint_html = "<div class='hint-grid'>"
    for title, value in [
        ("Ask this", kit["ask"]),
        ("Expected student answer", kit["expected"]),
        ("Misconception to correct", kit["misconception"]),
        ("Quick activity", kit["activity"]),
        ("Closing line", kit["wrap"]),
        ("Transition to next step", "Now let us test whether the same idea survives when students touch the data themselves."),
    ]:
        hint_html += f"<div class='hint-card'><b>{html.escape(title)}</b><br>{html.escape(value)}</div>"
    hint_html += "</div>"
    st.markdown(hint_html, unsafe_allow_html=True)

    st.markdown("#### 🧩 Use this on the spot")
    st.markdown(
        f"""
1. **Point to the chart and ask:** What is the first thing your eye notices?
2. **Ask for evidence:** Which number or pattern supports that claim?
3. **Ask for business meaning:** Why should a manager care?
4. **Ask for risk:** What could be misread or overclaimed?
5. **Ask for action:** What should be done next, and by whom?

**One-sentence template for students:** Because **[pattern]** is visible in **[evidence]**, the manager should **[action]** while checking **[risk/limitation]**.
        """.strip()
    )
    guide_text = textwrap.dedent(f"""
    Session {sess.no}: {sess.title}

    Opening line:
    {kit['opening']}

    Scene:
    {scene}

    Data moment:
    {data_moment}

    Classroom story:
    {teaching_story}

    Chart to show:
    {kit['chart_hint']}

    Example:
    {kit['example']}

    Ask this:
    {kit['ask']}

    Expected student answer:
    {kit['expected']}

    Misconception to correct:
    {kit['misconception']}

    Quick activity:
    {kit['activity']}

    Closing line:
    {kit['wrap']}
    """).strip()
    st.download_button("Download this teaching story guide", guide_text, file_name=f"session_{sess.no}_teaching_guide.txt", mime="text/plain", key=f"story_guide_{sess.no}")
    callout("Discussion prompt", "What could be misunderstood if this concept is ignored? Ask students to answer in one sentence and then improve the sentence into an action-oriented insight.", "warning")


def build_activity_bank() -> List[Dict[str, str]]:
    activity_types = [
        ("Chart diagnosis sprint", "Show a weak visual, identify the main design problem, and propose one correction.", "One corrected chart decision and one improved headline.", "What changed in the audience's interpretation?"),
        ("Insight headline challenge", "Rewrite a descriptive title into an analytical and action-oriented title.", "Three-title ladder: descriptive, analytical, action-oriented.", "Which title is most useful for a manager and why?"),
        ("Managerial implication note", "Convert one observed pattern into implication, risk, and recommendation.", "A three-line note: pattern, implication, action.", "Is the recommendation justified by the evidence?"),
        ("Peer critique round", "Exchange visual stories with another group and critique clarity, truthfulness, and usefulness.", "Peer feedback using three criteria.", "What did the peer group notice that the original group missed?"),
        ("Ninety-second CEO briefing", "Prepare a short oral explanation of the visual for a senior leader who has only ninety seconds.", "Opening sentence, one evidence sentence, and one recommendation sentence.", "Was the recommendation clear enough for immediate action?"),
        ("Evidence-versus-opinion check", "Mark every sentence in the story as evidence, inference, recommendation, or unsupported opinion.", "A cleaned-up story with unsupported claims removed.", "Which claim needed more data before it could be used?"),
        ("Before-after redesign", "Take the weak version of the visual and improve title, chart choice, color, annotation, and takeaway.", "Before-after comparison with a short explanation.", "Which single redesign choice improved clarity the most?"),
        ("Stakeholder translation", "Rewrite the same visual story for an executive, analyst, frontline manager, and customer audience.", "Four audience-specific versions of the same insight.", "How did the wording and level of detail change across audiences?"),
    ]
    bank: List[Dict[str, str]] = []
    for sess in SESSIONS:
        for idx, (name, instruction, output, debrief) in enumerate(activity_types, start=1):
            bank.append({
                "Session": str(sess.no),
                "Module": sess.module,
                "CLOs": sess.clos,
                "Activity": f"S{sess.no}.{idx} {name}",
                "Instruction": f"For '{sess.title}', {instruction.lower()} Use the session takeaway: {sess.takeaway}",
                "Student Output": output,
                "Debrief Question": debrief,
                "Estimated Time": ["8–10 min", "10–12 min", "12–15 min", "15–20 min", "6–8 min", "8–10 min", "15–20 min", "10–12 min"][idx-1],
            })
    return bank


ACTIVITY_BANK: List[Dict[str, str]] = build_activity_bank()


CHART_GALLERY = [
    {"name": "Ranked Bar", "family": "Comparison", "use": "Rank categories and reveal leaders or laggards.", "avoid": "Avoid when the x-axis is true time.", "story": "Who is ahead, who is behind, and where should attention go?"},
    {"name": "Dot Plot", "family": "Comparison", "use": "Compare many categories with less ink than bars.", "avoid": "Avoid when audiences require filled magnitude bars for quick executive scanning.", "story": "Which categories stand out without visual clutter?"},
    {"name": "Heatmap", "family": "Pattern scan", "use": "Find high-low patterns across two categorical dimensions.", "avoid": "Avoid when exact values matter more than pattern recognition.", "story": "Where are the strongest pockets or risk zones?"},
    {"name": "Histogram", "family": "Distribution", "use": "Show spread, skew, and frequency of numeric values.", "avoid": "Avoid for small samples where each point needs inspection.", "story": "Is the process stable, skewed, or affected by extremes?"},
    {"name": "Box Plot", "family": "Distribution", "use": "Compare median, spread, and outliers across groups.", "avoid": "Avoid when students have not been oriented to quartiles.", "story": "Which group is more variable or risky?"},
    {"name": "Scatter Plot", "family": "Relationship", "use": "Show association, clusters, and outliers between two numerical variables.", "avoid": "Avoid using it to claim causation without stronger evidence.", "story": "What pattern deserves investigation?"},
    {"name": "Bubble Chart", "family": "Relationship", "use": "Add a third quantitative variable through size.", "avoid": "Avoid when too many bubbles overlap.", "story": "Which opportunity is large, growing, and strategically attractive?"},
    {"name": "Line Chart", "family": "Time", "use": "Show trend, seasonality, and turning points over time.", "avoid": "Avoid for unordered categories.", "story": "What changed, when, and why might it matter?"},
    {"name": "Area Chart", "family": "Time composition", "use": "Show cumulative or stacked movement over time.", "avoid": "Avoid when exact category comparison is critical.", "story": "How does total volume evolve and what contributes to it?"},
    {"name": "Stacked Bar", "family": "Composition", "use": "Show part-to-whole contribution across groups.", "avoid": "Avoid when exact segment ranking is needed across many bars.", "story": "What makes up the total and how does mix differ?"},
    {"name": "100% Stacked Bar", "family": "Composition", "use": "Compare proportional mix across groups after normalizing totals.", "avoid": "Avoid when absolute totals matter.", "story": "How does the mix differ, regardless of size?"},
    {"name": "Treemap", "family": "Composition", "use": "Show hierarchical contribution and large drivers.", "avoid": "Avoid when exact comparison among similar small rectangles matters.", "story": "Which segments dominate the whole?"},
    {"name": "Waterfall", "family": "Change explanation", "use": "Explain how positive and negative components build to a final value.", "avoid": "Avoid for simple rank comparison.", "story": "What caused the movement from start to finish?"},
    {"name": "Funnel", "family": "Process conversion", "use": "Show drop-off through stages of a process.", "avoid": "Avoid for unrelated categories.", "story": "Where does the process lose the most value?"},
    {"name": "Slope Chart", "family": "Change comparison", "use": "Show change between two points for several categories.", "avoid": "Avoid with too many crossing lines.", "story": "Who improved, declined, or reversed position?"},
    {"name": "Executive KPI Dashboard", "family": "Dashboard", "use": "Combine headline metrics, diagnosis, and action cues.", "avoid": "Avoid as a dumping ground for unrelated charts.", "story": "What should leadership notice first and act on next?"},
    {"name": "Violin Plot", "family": "Distribution", "use": "Show distribution shape and density across groups.", "avoid": "Avoid when the audience is unfamiliar with density shapes.", "story": "Which group has the widest experience spread?"},
    {"name": "Strip Plot", "family": "Distribution", "use": "Show individual observations and clusters.", "avoid": "Avoid when there are too many overlapping points.", "story": "Where do individual cases cluster or stand apart?"},
    {"name": "Pareto Chart", "family": "Priority", "use": "Reveal the few categories that explain most of the outcome.", "avoid": "Avoid when categories are not additive.", "story": "Which few drivers deserve first attention?"},
    {"name": "Radar Chart", "family": "Profile", "use": "Compare multi-dimensional profiles for a few entities.", "avoid": "Avoid with many entities or when exact comparison matters.", "story": "Which option has the strongest balanced profile?"},
    {"name": "Gantt Timeline", "family": "Project", "use": "Show task sequence, duration, and overlaps.", "avoid": "Avoid when performance magnitude is the main question.", "story": "Which tasks create timeline pressure?"},
    {"name": "Calendar Heatmap", "family": "Time pattern", "use": "Show daily or weekly intensity patterns.", "avoid": "Avoid when exact daily values must be read quickly.", "story": "Which periods repeatedly show pressure or opportunity?"},
    {"name": "Sankey Diagram", "family": "Flow", "use": "Show movement, conversion, or allocation from source to destination.", "avoid": "Avoid for simple rank comparisons.", "story": "Where does flow concentrate or leak?"},
    {"name": "Sunburst Chart", "family": "Hierarchy", "use": "Show hierarchical part-to-whole structure.", "avoid": "Avoid with deep hierarchies and tiny slices.", "story": "Which branch contributes most to the whole?"},
    {"name": "Geo Bubble Map", "family": "Geography", "use": "Show location-based magnitude and regional variation.", "avoid": "Avoid when geography is irrelevant to the decision.", "story": "Where are regional hotspots?"},
    {"name": "Small Multiples", "family": "Comparison", "use": "Compare repeated patterns across categories using the same scale.", "avoid": "Avoid when the audience needs a single headline only.", "story": "Which category follows a different pattern?"},
    {"name": "Bullet Chart", "family": "Performance", "use": "Compare actual performance against target compactly.", "avoid": "Avoid when trends over time are needed.", "story": "Are we above or below target, and by how much?"},
    {"name": "Control Chart", "family": "Process", "use": "Show whether a process is stable or has unusual variation.", "avoid": "Avoid when control limits are not meaningful for the process.", "story": "Is the process variation normal or alarming?"},
    {"name": "Dumbbell Chart", "family": "Change comparison", "use": "Show before-after change across categories.", "avoid": "Avoid with too many categories or tiny changes.", "story": "Who improved, who declined, and how large is the gap?"},
    {"name": "Gauge Indicator", "family": "Performance", "use": "Show one KPI against a target or threshold.", "avoid": "Avoid using many gauges when a table or bar chart is clearer.", "story": "Is the headline KPI in a safe, watch, or action zone?"},
]


# -----------------------------------------------------------------------------
# Charts and demos
# -----------------------------------------------------------------------------


def plotly_x_value(value):
    """Return a Plotly-safe x-axis value.

    Plotly's add_vline can fail with recent pandas versions when the
    x value is a pandas Timestamp because the internal annotation logic
    attempts integer arithmetic on Timestamp objects. Converting dates
    to ISO strings keeps the same axis location and avoids that error.
    """
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    return value


def add_vertical_marker(fig, x_value, label: str, line_dash: str = "dash"):
    """Add a vertical event marker without using fig.add_vline.

    This avoids pandas Timestamp arithmetic errors in Plotly's add_vline
    annotation helper on newer pandas/Python stacks.
    """
    safe_x = plotly_x_value(x_value)
    fig.add_shape(
        type="line",
        x0=safe_x,
        x1=safe_x,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(dash=line_dash, width=2),
    )
    fig.add_annotation(
        x=safe_x,
        y=1.04,
        xref="x",
        yref="paper",
        text=label,
        showarrow=False,
        align="center",
    )
    return fig

def add_chart_teaching_notes(chart_name: str, use: str, avoid: str, mistake: str, takeaway: str) -> None:
    c1, c2 = st.columns(2)
    with c1:
        callout("When to use", use, "insight")
        callout("When not to use", avoid, "warning")
    with c2:
        callout("Common mistake", mistake, "danger")
        callout("Managerial takeaway", takeaway, "purple")


def ranked_bar(df: pd.DataFrame, x: str, y: str, title: str, color: Optional[str] = None) -> go.Figure:
    d = df.sort_values(y, ascending=True)
    fig = px.bar(d, x=y, y=x, orientation="h", color=color, text=y, title=title)
    fig.update_layout(height=430, margin=dict(l=20, r=20, t=70, b=20), title_x=0.02)
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside", cliponaxis=False)
    return fig


def render_table_vs_chart() -> None:
    df = retail_data().groupby("Region", as_index=False)["Sales"].sum()
    st.write("Observe the same data as a table and as a visual comparison.")
    c1, c2 = st.columns([.9, 1.4])
    with c1:
        safe_dataframe(df)
    with c2:
        fig = ranked_bar(df, "Region", "Sales", "West and Central lead total sales; East needs attention")
        st.plotly_chart(fig, use_container_width=True)
    callout("Teaching point", "The table is precise, but the chart helps the audience detect relative performance quickly. The story becomes useful when we add a decision message: protect momentum in leading regions and diagnose the weaker region.", "insight")


def render_chart_mapping_demo() -> None:
    question = st.selectbox(
        "Choose the business question",
        [
            "Which region has the highest sales?",
            "How has revenue changed over time?",
            "How widely do waiting times vary?",
            "Is discount associated with sales?",
            "Which category contributes most to revenue?",
        ],
    )
    recommendations = {
        "Which region has the highest sales?": ("Ranked bar or dot plot", "Comparison across categories"),
        "How has revenue changed over time?": ("Line chart", "Trend and change over time"),
        "How widely do waiting times vary?": ("Histogram or box plot", "Distribution and variation"),
        "Is discount associated with sales?": ("Scatter plot", "Relationship between two numerical variables"),
        "Which category contributes most to revenue?": ("Sorted bar or treemap", "Contribution and composition"),
    }
    chart, reason = recommendations[question]
    callout("Recommended chart", f"Use a <b>{chart}</b> because the question is about <b>{reason}</b>.", "insight")
    df = retail_data()
    if "highest sales" in question:
        st.plotly_chart(ranked_bar(df.groupby("Region", as_index=False)["Sales"].sum(), "Region", "Sales", "Ranked regional sales reveal the leading region"), use_container_width=True)
    elif "over time" in question:
        d = time_series_revenue()
        fig = px.line(d, x="Month", y=["Revenue", "Cost"], markers=True, title="Revenue is improving faster than cost after the campaign period")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif "waiting" in question:
        d = healthcare_data()
        fig = px.box(d, x="Department", y="Avg Wait Time", points="outliers", title="Waiting-time variation is highest in departments with patient-flow pressure")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif "discount" in question:
        fig = px.scatter(df, x="Discount", y="Sales", color="Category", size="Profit", title="Discount and sales show mixed association across categories")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    else:
        d = df.groupby("Category", as_index=False)["Sales"].sum()
        st.plotly_chart(ranked_bar(d, "Category", "Sales", "Electronics and Grocery drive the largest revenue contribution"), use_container_width=True)


def render_axes_demo() -> None:
    df = pd.DataFrame({"Branch": ["Branch A", "Branch B", "Branch C", "Branch D"], "Customer Score": [84, 86, 87, 88]})
    toggle = st.radio("Axis framing", ["Misleading truncated axis", "Responsible full context"], horizontal=True)
    fig = px.bar(df, x="Branch", y="Customer Score", text="Customer Score", title="Small score differences can look dramatic when the axis is truncated")
    fig.update_traces(textposition="outside")
    if toggle == "Misleading truncated axis":
        fig.update_yaxes(range=[80, 90])
    else:
        fig.update_yaxes(range=[0, 100])
    fig.update_layout(height=430, title_x=.02)
    st.plotly_chart(fig, use_container_width=True)
    callout("What changed?", "The values did not change; the visual impression changed. This is why axis choices must be justified by the message and the measurement context.", "warning")


def render_color_demo() -> None:
    df = retail_data().groupby("Category", as_index=False)["Profit"].sum()
    highlight = st.selectbox("Choose the category to emphasize", df["Category"].tolist(), index=0)
    df["Focus"] = np.where(df["Category"] == highlight, "Focus", "Context")
    fig = px.bar(df.sort_values("Profit"), x="Profit", y="Category", orientation="h", color="Focus", text="Profit", title=f"{highlight} is highlighted while other categories remain context")
    fig.update_layout(height=430, title_x=.02, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    callout("Design logic", "Most colors should stay quiet. Use emphasis only where the audience should look first.", "insight")


def render_amounts_demo() -> None:
    df = retail_data().groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    chart = st.radio("Choose visual form", ["Ranked bar", "Dot plot", "Heatmap"], horizontal=True)
    if chart == "Ranked bar":
        st.plotly_chart(ranked_bar(df, "Region", "Sales", "Regional sales ranking shows where growth momentum is strongest"), use_container_width=True)
    elif chart == "Dot plot":
        d = df.sort_values("Sales")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d["Sales"], y=d["Region"], mode="markers", marker=dict(size=16), name="Sales"))
        fig.update_layout(title="Dot plot reduces ink and keeps comparison precise", height=430, title_x=.02, xaxis_title="Sales", yaxis_title="Region")
        st.plotly_chart(fig, use_container_width=True)
    else:
        h = retail_data().pivot_table(index="Region", columns="Category", values="Sales", aggfunc="sum")
        fig = px.imshow(h, aspect="auto", title="Heatmap identifies strong region-category pockets")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    add_chart_teaching_notes("Amount chart", "Use for ranking, comparison, and identifying high/low performers.", "Avoid when the real question is a trend or distribution.", "Leaving categories unsorted makes comparison slower.", "The strongest visual message should be visible within a few seconds.")


def render_distribution_demo() -> None:
    df = healthcare_data()
    dept = st.multiselect("Select departments", sorted(df["Department"].unique()), default=["Emergency", "OPD", "Radiology"])
    d = df[df["Department"].isin(dept)]
    chart = st.radio("Distribution view", ["Histogram", "Box plot"], horizontal=True)
    if chart == "Histogram":
        fig = px.histogram(d, x="Avg Wait Time", color="Department", nbins=24, barmode="overlay", title="Distribution view reveals waiting-time spread and service risk")
    else:
        fig = px.box(d, x="Department", y="Avg Wait Time", points="outliers", title="Box plot highlights variation and outlier pressure")
    fig.update_layout(height=460, title_x=.02)
    st.plotly_chart(fig, use_container_width=True)
    callout("Managerial meaning", "Do not stop at the average. Ask whether the distribution shows consistency, unpredictable service experience, or extreme cases requiring process attention.", "insight")


def render_composition_demo() -> None:
    df = retail_data().groupby("Category", as_index=False)["Sales"].sum()
    chart = st.radio("Composition view", ["Pie chart", "Sorted contribution bar", "Treemap"], horizontal=True)
    if chart == "Pie chart":
        fig = px.pie(df, names="Category", values="Sales", title="Pie chart works only when slices are few and the message is part-to-whole")
    elif chart == "Sorted contribution bar":
        st.plotly_chart(ranked_bar(df, "Category", "Sales", "Sorted bars often explain contribution more clearly than pie slices"), use_container_width=True)
        return
    else:
        fig = px.treemap(df, path=["Category"], values="Sales", title="Treemap emphasizes relative contribution by area")
    fig.update_layout(height=460, title_x=.02)
    st.plotly_chart(fig, use_container_width=True)
    callout("Decision lens", "Composition is useful when contribution is the question. Use a ranking chart when exact comparison is more important than part-to-whole perception.", "purple")


def render_critique_demo() -> None:
    issue = st.radio("Choose critique focus", ["Weak title", "Too much color", "Wrong chart type", "No action"], horizontal=True)
    df = marketing_data()
    weak_title = "Chart of Marketing Data"
    better_title = "Search and Referral deliver stronger revenue efficiency than Display"
    if issue == "Wrong chart type":
        fig1 = px.pie(df, names="Channel", values="Revenue", title=weak_title)
        fig2 = ranked_bar(df, "Channel", "Revenue", better_title)
    elif issue == "Too much color":
        fig1 = px.bar(df, x="Channel", y="Revenue", color="Channel", title=weak_title)
        d = df.sort_values("Revenue", ascending=False)
        d["Focus"] = np.where(d["Channel"] == d.iloc[0]["Channel"], "Highest", "Context")
        fig2 = px.bar(d, x="Channel", y="Revenue", color="Focus", title=better_title)
        fig2.update_layout(showlegend=False)
    else:
        fig1 = px.bar(df, x="Channel", y="Revenue", title=weak_title)
        fig2 = ranked_bar(df, "Channel", "Revenue", better_title)
    fig1.update_layout(height=390, title_x=.02)
    fig2.update_layout(height=390, title_x=.02)
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Weak visual story")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.caption("Reframed visual story")
        st.plotly_chart(fig2, use_container_width=True)
    callout("Critique method", "First diagnose the decision question. Then check encoding, title, clutter, scale, and action orientation.", "insight")


def render_relationship_demo() -> None:
    df = retail_data()
    x = st.selectbox("X variable", ["Discount", "Satisfaction", "Profit"], index=0)
    y = st.selectbox("Y variable", ["Sales", "Profit", "Satisfaction"], index=0)
    fig = px.scatter(df, x=x, y=y, color="Category", size="Profit", hover_data=["Region"], title=f"Relationship view: {x} versus {y}")
    if df[x].nunique() > 1 and df[y].nunique() > 1:
        coef = np.polyfit(df[x], df[y], 1)
        xs = np.linspace(df[x].min(), df[x].max(), 50)
        ys = coef[0] * xs + coef[1]
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="Simple trend", line=dict(dash="dash")))
    fig.update_layout(height=470, title_x=.02)
    st.plotly_chart(fig, use_container_width=True)
    callout("Interpret carefully", "A scatter plot can suggest association, clusters, and exceptions. It does not prove causality on its own.", "warning")


def render_time_series_demo() -> None:
    df = time_series_revenue()
    metric = st.multiselect("Metrics", ["Revenue", "Cost"], default=["Revenue", "Cost"])
    fig = px.line(df, x="Month", y=metric, markers=True, title="Revenue accelerates after the campaign marker while cost rises more gradually")
    campaign_month = df.loc[df["Post Campaign"], "Month"].min()
    add_vertical_marker(fig, campaign_month, "Campaign period begins")
    fig.update_layout(height=470, title_x=.02)
    st.plotly_chart(fig, use_container_width=True)
    callout("Narrative cue", "Time-series charts become more meaningful when key events, interventions, and turning points are annotated.", "insight")


def kpi_cards_for_domain(domain: str) -> None:
    if domain == "Retail Sales":
        df = retail_data()
        values = [
            ("Total Sales", f"{df['Sales'].sum():,.0f}", "Across all regions"),
            ("Total Profit", f"{df['Profit'].sum():,.0f}", "Profit pool"),
            ("Avg Satisfaction", f"{df['Satisfaction'].mean():.1f}", "Customer signal"),
            ("Avg Discount", f"{df['Discount'].mean():.1f}%", "Price pressure"),
        ]
    elif domain == "Healthcare Patient Flow":
        df = healthcare_data()
        values = [
            ("Patients", f"{df['Patients'].sum():,.0f}", "90-day volume"),
            ("Avg Wait", f"{df['Avg Wait Time'].mean():.1f} min", "Service speed"),
            ("Occupancy", f"{df['Bed Occupancy'].mean():.1f}%", "Capacity use"),
            ("Readmission", f"{df['Readmission Rate'].mean():.1f}%", "Quality signal"),
        ]
    elif domain == "Marketing Campaign":
        df = marketing_data()
        values = [
            ("Spend", f"₹{df['Spend'].sum()/1e5:.1f}L", "Campaign cost"),
            ("Revenue", f"₹{df['Revenue'].sum()/1e5:.1f}L", "Generated revenue"),
            ("Conversions", f"{df['Conversions'].sum():,.0f}", "Outcome volume"),
            ("Avg CVR", f"{df['Conversion Rate'].mean():.2f}%", "Conversion quality"),
        ]
    else:
        df = finance_data()
        values = [
            ("Budget", f"₹{df['Budget'].sum()/1e5:.1f}L", "Planned"),
            ("Actual", f"₹{df['Actual'].sum()/1e5:.1f}L", "Spent"),
            ("Variance", f"₹{df['Variance'].sum()/1e5:.1f}L", "Budget gap"),
            ("High Risk", f"{(df['Risk']=='High').sum()}", "Departments"),
        ]
    cols = st.columns(4)
    for col, (label, value, note) in zip(cols, values):
        with col:
            metric_box(label, value, note)


def render_dashboard_demo(domain: str = "Retail Sales") -> None:
    kpi_cards_for_domain(domain)
    st.write("")
    if domain == "Healthcare Patient Flow":
        df = healthcare_data()
        c1, c2 = st.columns([1.15, .85])
        with c1:
            d = df.groupby("Date", as_index=False)["Patients"].sum()
            fig = px.line(d, x="Date", y="Patients", title="Daily patient volume shows recurring capacity pressure")
            fig.update_layout(height=360, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            d2 = df.groupby("Department", as_index=False)["Avg Wait Time"].mean()
            st.plotly_chart(ranked_bar(d2, "Department", "Avg Wait Time", "Departments ranked by average waiting time"), use_container_width=True)
    elif domain == "Marketing Campaign":
        df = marketing_data()
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(ranked_bar(df, "Channel", "Revenue", "Revenue contribution by marketing channel"), use_container_width=True)
        with c2:
            fig = px.scatter(df, x="Spend", y="Revenue", size="Conversions", color="Channel", title="Spend-to-revenue relationship highlights channel efficiency")
            fig.update_layout(height=430, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
    elif domain == "Financial Expenses":
        df = finance_data()
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df, x="Department", y=["Budget", "Actual"], barmode="group", title="Budget versus actual spend by department")
            fig.update_layout(height=430, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.plotly_chart(ranked_bar(df, "Department", "Variance", "Variance identifies budget pressure points", color="Risk"), use_container_width=True)
    else:
        df = retail_data()
        c1, c2 = st.columns(2)
        with c1:
            d = df.groupby("Month", as_index=False)["Sales"].sum()
            fig = px.line(d, x="Month", y="Sales", markers=True, title="Sales trend reveals seasonal movement")
            fig.update_layout(height=430, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            d2 = df.groupby("Region", as_index=False)["Profit"].sum()
            st.plotly_chart(ranked_bar(d2, "Region", "Profit", "Profit ranking identifies where to protect margin"), use_container_width=True)


def render_annotation_demo() -> None:
    df = time_series_revenue()
    title_type = st.radio("Title style", ["Descriptive", "Analytical", "Action-oriented"], horizontal=True)
    titles = {
        "Descriptive": "Monthly Revenue and Cost",
        "Analytical": "Revenue growth improves after the campaign period",
        "Action-oriented": "Scale the campaign cautiously: revenue rises faster than cost after launch",
    }
    fig = px.line(df, x="Month", y=["Revenue", "Cost"], markers=True, title=titles[title_type])
    campaign_month = df.loc[df["Post Campaign"], "Month"].min()
    add_vertical_marker(fig, campaign_month, "Campaign begins")
    fig.add_annotation(x=plotly_x_value(df.loc[df["Revenue"].idxmax(), "Month"]), y=df["Revenue"].max(), text="Highest revenue point", showarrow=True, arrowhead=2)
    fig.update_layout(height=470, title_x=.02)
    st.plotly_chart(fig, use_container_width=True)
    callout("Title clinic", "Descriptive titles name the chart. Analytical titles state the insight. Action-oriented titles connect the insight to a recommendation.", "insight")


def render_pitfalls_demo() -> None:
    render_misleading_clinic(inline=True)


def render_strategy_demo() -> None:
    df = regional_data()
    fig = px.scatter(df, x="Market Size", y="Growth Rate", size="Market Share", color="Attractiveness", hover_name="Region", title="Strategy map: market size, growth, share, and attractiveness")
    fig.update_layout(height=470, title_x=.02)
    st.plotly_chart(fig, use_container_width=True)
    callout("Strategic interpretation", "A strategy visual should not simply rank markets. It should clarify trade-offs: growth versus current strength, opportunity versus competition, and focus versus diversification.", "purple")


def render_workshop_demo() -> None:
    st.info("Use the Final Integrated Workshop page for a complete build. Here is the minimum workflow.")
    process_diagram(["Frame the problem", "Choose the data", "Select 2–3 visuals", "Write the insight", "Recommend action"])


def render_healthcare_demo() -> None:
    render_dashboard_demo("Healthcare Patient Flow")
    callout("Healthcare caution", "Healthcare dashboards must avoid false certainty. Always consider denominator effects, patient safety, operational feasibility, and ethical interpretation.", "warning")


def render_session_demo(session_no: int) -> None:
    if session_no == 1:
        render_table_vs_chart()
    elif session_no == 2:
        render_chart_mapping_demo()
    elif session_no == 3:
        render_axes_demo()
    elif session_no == 4:
        render_color_demo()
    elif session_no == 5:
        render_amounts_demo()
    elif session_no == 6:
        render_distribution_demo()
    elif session_no == 7:
        render_composition_demo()
    elif session_no == 8:
        render_critique_demo()
    elif session_no == 9:
        render_relationship_demo()
    elif session_no == 10:
        render_time_series_demo()
    elif session_no == 11:
        render_dashboard_demo(st.selectbox("Dashboard domain", ["Retail Sales", "Marketing Campaign", "Financial Expenses", "Healthcare Patient Flow"], key="s11_domain"))
    elif session_no == 12:
        render_annotation_demo()
    elif session_no == 13:
        render_pitfalls_demo()
    elif session_no == 14:
        render_strategy_demo()
    elif session_no == 15:
        render_workshop_demo()
    elif session_no == 16:
        render_healthcare_demo()


# -----------------------------------------------------------------------------
# Quiz bank: 56 questions
# -----------------------------------------------------------------------------
QUIZ_BANK: List[Dict[str, str]] = [
    {"session": "1", "clo": "CLO1", "q": "What is the primary purpose of data storytelling in managerial communication?", "options": "A. To decorate reports | B. To connect evidence with interpretation and action | C. To replace analysis | D. To hide uncertainty", "answer": "B", "explanation": "Data storytelling helps managers move from evidence to meaning, implication, and action."},
    {"session": "1", "clo": "CLO1", "q": "A chart without a decision context is most likely to fail because:", "options": "A. It has too few colors | B. The audience may not know what action or interpretation is expected | C. It uses data | D. It has labels", "answer": "B", "explanation": "Decision context clarifies why the visual matters."},
    {"session": "1", "clo": "CLO1", "q": "True or False: A beautiful chart is always an effective business visual.", "options": "True | False", "answer": "False", "explanation": "Beauty does not guarantee clarity, accuracy, or actionability."},
    {"session": "2", "clo": "CLO2", "q": "Which chart is usually best for comparing sales across five regions?", "options": "A. Ranked bar chart | B. Word cloud | C. 3D pie | D. Gauge only", "answer": "A", "explanation": "A ranked bar chart supports clear categorical comparison."},
    {"session": "2", "clo": "CLO2", "q": "A line chart is most appropriate when the business question focuses on:", "options": "A. Change over time | B. Part-to-whole composition only | C. Exact ranking of departments | D. Text frequency", "answer": "A", "explanation": "Line charts show trend, direction, and change over time."},
    {"session": "2", "clo": "CLO2", "q": "Which visual is most suitable for showing the relationship between discount and sales?", "options": "A. Scatter plot | B. Pie chart | C. Stacked bar only | D. Table of footnotes", "answer": "A", "explanation": "A scatter plot shows association between two numerical variables."},
    {"session": "3", "clo": "CLO1", "q": "Why can a truncated bar-chart axis be misleading?", "options": "A. It may exaggerate differences | B. It makes bars too colorful | C. It removes labels automatically | D. It prevents sorting", "answer": "A", "explanation": "Truncation can make small differences appear large."},
    {"session": "3", "clo": "CLO2", "q": "When is a zero baseline especially important?", "options": "A. Bar charts comparing magnitude | B. Word clouds | C. Text-only reports | D. Scatter plots with negative values only", "answer": "A", "explanation": "Bars encode magnitude by length; without zero baseline the length comparison can mislead."},
    {"session": "3", "clo": "CLO2", "q": "True or False: Changing an axis cannot change the audience’s interpretation if data values are unchanged.", "options": "True | False", "answer": "False", "explanation": "The data may remain unchanged, but visual framing can alter perceived magnitude."},
    {"session": "4", "clo": "CLO2", "q": "The best use of color in a business chart is to:", "options": "A. Make every category bright | B. Guide attention and encode meaning | C. Fill empty space | D. Replace labels", "answer": "B", "explanation": "Color should direct attention and communicate meaning."},
    {"session": "4", "clo": "CLO2", "q": "Which color strategy is usually clearer?", "options": "A. Rainbow palette for every bar | B. Neutral base with one highlighted category | C. Random colors | D. Similar colors for all opposing groups", "answer": "B", "explanation": "A neutral base with focused highlight guides attention."},
    {"session": "4", "clo": "CLO2", "q": "True or False: Color should always be used as decoration first.", "options": "True | False", "answer": "False", "explanation": "Color should serve communication, not decoration."},
    {"session": "5", "clo": "CLO3", "q": "A title such as 'Sales by Region' is weaker than 'West leads sales while East requires attention' because:", "options": "A. It is shorter | B. It does not state the insight | C. It uses region names | D. It has no punctuation", "answer": "B", "explanation": "The stronger title tells the audience what the chart means."},
    {"session": "5", "clo": "CLO2", "q": "For amount comparison, unsorted bars are problematic because:", "options": "A. They make ranking slower | B. They reduce file size | C. They make data private | D. They remove the axis", "answer": "A", "explanation": "Sorting helps the audience see rank and exceptions quickly."},
    {"session": "5", "clo": "CLO2", "q": "Which visual can compare many category values with low visual clutter?", "options": "A. Dot plot | B. 3D exploded pie | C. Clip art | D. Paragraph only", "answer": "A", "explanation": "Dot plots are efficient for comparison with less ink."},
    {"session": "6", "clo": "CLO2", "q": "Why should managers examine distributions instead of only averages?", "options": "A. Distributions reveal spread, outliers, and risk | B. Averages are illegal | C. Distributions remove uncertainty | D. Averages cannot be calculated", "answer": "A", "explanation": "Variation and outliers often explain operational risk."},
    {"session": "6", "clo": "CLO3", "q": "A box plot is useful because it shows:", "options": "A. Median, spread, and outliers | B. Only one total value | C. A story title automatically | D. Geographic borders", "answer": "A", "explanation": "Box plots summarize distribution and outliers compactly."},
    {"session": "6", "clo": "CLO2", "q": "True or False: Two teams with the same average can have very different service consistency.", "options": "True | False", "answer": "True", "explanation": "Their distributions may differ substantially."},
    {"session": "7", "clo": "CLO2", "q": "Composition charts are best when the main question is:", "options": "A. How a whole is divided into parts | B. Whether variables are correlated | C. How values change every hour | D. How to write a paragraph", "answer": "A", "explanation": "Composition is about part-to-whole contribution."},
    {"session": "7", "clo": "CLO2", "q": "Why are pie charts with many slices difficult to interpret?", "options": "A. Human angle comparison becomes difficult | B. They are always illegal | C. They cannot use data | D. They require coding", "answer": "A", "explanation": "Humans compare lengths more easily than many similar angles."},
    {"session": "7", "clo": "CLO3", "q": "If exact ranking is more important than part-to-whole perception, choose:", "options": "A. Sorted bar chart | B. Many-slice pie | C. Icon collage | D. Random colors", "answer": "A", "explanation": "Sorted bars make ranking clearer."},
    {"session": "8", "clo": "CLO1", "q": "The first step in critiquing a visual should be to identify:", "options": "A. The decision question | B. The software used | C. The presenter’s age | D. The file name", "answer": "A", "explanation": "A visual should be assessed against its decision purpose."},
    {"session": "8", "clo": "CLO3", "q": "A weak dashboard can often be improved by:", "options": "A. Adding more unrelated charts | B. Clarifying the question and removing clutter | C. Hiding labels | D. Using more 3D effects", "answer": "B", "explanation": "Clarity begins with question and structure."},
    {"session": "8", "clo": "CLO2", "q": "True or False: Dashboard critique should focus only on aesthetics.", "options": "True | False", "answer": "False", "explanation": "Critique should include context, encoding, hierarchy, accuracy, and actionability."},
    {"session": "9", "clo": "CLO2", "q": "A scatter plot is primarily used to show:", "options": "A. Relationship between two numerical variables | B. A list of definitions | C. Only part-to-whole share | D. A single KPI", "answer": "A", "explanation": "Scatter plots reveal association, clusters, and outliers."},
    {"session": "9", "clo": "CLO3", "q": "Why should correlation not be presented as causation?", "options": "A. Association alone does not prove one variable caused the other | B. Scatter plots cannot have labels | C. All correlations are false | D. Charts remove uncertainty", "answer": "A", "explanation": "Causal claims require stronger design and evidence."},
    {"session": "9", "clo": "CLO3", "q": "In a relationship chart, outliers may be important because they can signal:", "options": "A. Special cases, errors, or opportunities | B. That the chart must be deleted | C. That data has no meaning | D. That labels are unnecessary", "answer": "A", "explanation": "Outliers can reveal exceptional risks or opportunities."},
    {"session": "10", "clo": "CLO3", "q": "Which chart is usually best for monthly revenue across three years?", "options": "A. Line chart | B. Pie chart | C. 3D cylinder | D. Static icon", "answer": "A", "explanation": "Line charts communicate time-based change."},
    {"session": "10", "clo": "CLO4", "q": "Annotating a campaign launch date on a time-series chart helps the audience:", "options": "A. Connect events with observed changes | B. Remove all uncertainty | C. Avoid reading the chart | D. Hide the trend", "answer": "A", "explanation": "Annotations add explanatory context."},
    {"session": "10", "clo": "CLO3", "q": "True or False: Seasonality should be ignored when telling a time-series story.", "options": "True | False", "answer": "False", "explanation": "Seasonality may explain recurring highs and lows."},
    {"session": "11", "clo": "CLO4", "q": "An executive dashboard should begin with:", "options": "A. A clear decision question or priority | B. The maximum number of charts | C. Decorative animations | D. Raw data tables only", "answer": "A", "explanation": "Dashboards should guide decisions, not just display data."},
    {"session": "11", "clo": "CLO2", "q": "KPI cards are most useful when they:", "options": "A. Summarize priority metrics with context | B. Replace every chart | C. Use no labels | D. Show only random values", "answer": "A", "explanation": "KPI cards provide fast orientation."},
    {"session": "11", "clo": "CLO3", "q": "Too many dashboard charts can reduce quality because:", "options": "A. They create attention overload | B. They always improve insight | C. They make data more true | D. They remove the need for titles", "answer": "A", "explanation": "Too much visual material dilutes attention and priority."},
    {"session": "12", "clo": "CLO3", "q": "An analytical chart title should:", "options": "A. State the key insight | B. Only name the variables | C. Avoid meaning | D. Be as vague as possible", "answer": "A", "explanation": "Analytical titles guide interpretation."},
    {"session": "12", "clo": "CLO4", "q": "Annotations are useful when they:", "options": "A. Explain important points or events | B. Label every pixel | C. Replace all data | D. Hide uncertainty", "answer": "A", "explanation": "Annotations should guide attention to meaningful evidence."},
    {"session": "12", "clo": "CLO4", "q": "True or False: Captions should repeat only what the axis labels already say.", "options": "True | False", "answer": "False", "explanation": "Captions should add interpretation, context, or caution."},
    {"session": "13", "clo": "CLO1", "q": "Chart junk refers to:", "options": "A. Decorative elements that do not support understanding | B. Accurate labels | C. Useful annotations | D. Proper scales", "answer": "A", "explanation": "Chart junk distracts from the message."},
    {"session": "13", "clo": "CLO2", "q": "A misleading visual can damage:", "options": "A. Trust and decision quality | B. Only font selection | C. The number of rows | D. The file extension", "answer": "A", "explanation": "Misleading visuals can distort interpretation and reduce trust."},
    {"session": "13", "clo": "CLO1", "q": "True or False: Uncertainty and limitations should always be hidden from managers.", "options": "True | False", "answer": "False", "explanation": "Responsible storytelling acknowledges uncertainty where relevant."},
    {"session": "14", "clo": "CLO4", "q": "A strategic visual story should end with:", "options": "A. A recommendation and rationale | B. A random screenshot | C. No conclusion | D. Only raw data", "answer": "A", "explanation": "Strategy communication must connect evidence to choices."},
    {"session": "14", "clo": "CLO3", "q": "What makes a strategy chart stronger?", "options": "A. Showing trade-offs and decision implications | B. Using more clip art | C. Avoiding context | D. Hiding labels", "answer": "A", "explanation": "Strategy often requires comparing trade-offs among options."},
    {"session": "14", "clo": "CLO4", "q": "True or False: A strategic story can stop at describing a pattern without recommendation.", "options": "True | False", "answer": "False", "explanation": "Strategic communication should point toward action."},
    {"session": "15", "clo": "CLO1–CLO4", "q": "In an integrated visual story, which sequence is strongest?", "options": "A. Context → Evidence → Insight → Implication → Action | B. Color → Decoration → Screenshot → End | C. Raw data → Raw data → Raw data | D. Animation → More animation → No message", "answer": "A", "explanation": "This sequence supports decision-oriented storytelling."},
    {"session": "15", "clo": "CLO3", "q": "Why should problem framing happen before chart creation?", "options": "A. It clarifies what the visuals must answer | B. It reduces data quality | C. It prevents interpretation | D. It removes the audience", "answer": "A", "explanation": "Problem framing guides chart choice and narrative design."},
    {"session": "15", "clo": "CLO4", "q": "A final visual story summary should include:", "options": "A. Business question, evidence, insight, recommendation | B. Only chart screenshots | C. Only software names | D. No conclusion", "answer": "A", "explanation": "These components connect analysis to management action."},
    {"session": "16", "clo": "CLO2–CLO4", "q": "In healthcare dashboards, denominator effects matter because:", "options": "A. Rates can be misread without the population base | B. They make charts colorful | C. They remove patient meaning | D. They are irrelevant", "answer": "A", "explanation": "Rates need denominators to be interpreted responsibly."},
    {"session": "16", "clo": "CLO4", "q": "A hospital operations dashboard should help managers understand:", "options": "A. Patient flow, capacity, waiting time, and risk | B. Only logo size | C. Only decorative icons | D. Only unrelated revenue", "answer": "A", "explanation": "Healthcare dashboards should connect operational metrics to care quality and action."},
    {"session": "16", "clo": "CLO4", "q": "True or False: Healthcare visual stories should avoid false certainty.", "options": "True | False", "answer": "True", "explanation": "Healthcare decisions require careful and ethical interpretation."},
    {"session": "2", "clo": "CLO2", "q": "Which business question best matches a heatmap?", "options": "A. Which region-category combinations are unusually high or low? | B. What is one exact value only? | C. What is the legal policy? | D. What font should be used?", "answer": "A", "explanation": "Heatmaps help scan patterns across two categorical dimensions."},
    {"session": "5", "clo": "CLO3", "q": "A stronger visual message usually answers:", "options": "A. What changed, why it matters, and what to do | B. How to add more decoration | C. How to avoid interpretation | D. How to hide labels", "answer": "A", "explanation": "Decision-oriented visuals connect observation to action."},
    {"session": "6", "clo": "CLO2", "q": "Outliers should be automatically removed from every chart.", "options": "True | False", "answer": "False", "explanation": "Outliers should be investigated; they may be errors, risks, or meaningful exceptions."},
    {"session": "7", "clo": "CLO2", "q": "A 100% stacked bar is useful for:", "options": "A. Comparing share composition across groups | B. Showing exact raw totals only | C. Showing correlation | D. Showing text sentiment", "answer": "A", "explanation": "100% stacked bars normalize groups to compare proportions."},
    {"session": "11", "clo": "CLO4", "q": "Dashboard hierarchy means:", "options": "A. Arranging information from priority to supporting detail | B. Making all visuals equal | C. Removing titles | D. Sorting files alphabetically", "answer": "A", "explanation": "Hierarchy guides attention through the dashboard."},
    {"session": "12", "clo": "CLO3", "q": "The phrase 'Customer complaints rose after waiting time exceeded 35 minutes' is best described as:", "options": "A. Analytical title | B. Decorative label | C. Raw variable name | D. Axis tick", "answer": "A", "explanation": "It states a meaningful interpretation of the data."},
    {"session": "13", "clo": "CLO1", "q": "What is the risk of decorative overload?", "options": "A. It distracts from the evidence and message | B. It improves statistical validity | C. It makes all decisions obvious | D. It removes bias", "answer": "A", "explanation": "Decorative overload competes with the signal."},
    {"session": "14", "clo": "CLO4", "q": "A recommendation storyboard should include trade-offs because:", "options": "A. Strategic choices usually involve competing priorities | B. Trade-offs make data wrong | C. Managers dislike clarity | D. Visuals cannot show alternatives", "answer": "A", "explanation": "Good strategy communication clarifies what is gained and what may be sacrificed."},
    {"session": "16", "clo": "CLO4", "q": "In patient-flow visualization, average waiting time should be interpreted with:", "options": "A. Volume, department context, and variation | B. Logo size only | C. Random color | D. No labels", "answer": "A", "explanation": "Waiting time is more meaningful when combined with capacity and volume context."},
]


def build_extra_quizzes() -> List[Dict[str, str]]:
    """Create additional scenario-based questions to make the app revision-ready."""
    extras: List[Dict[str, str]] = []
    for sess in SESSIONS:
        mistake = sess.common_mistakes[0] if sess.common_mistakes else "ignoring the decision context"
        extras.extend([
            {
                "session": str(sess.no),
                "clo": sess.clos,
                "q": f"Scenario: A student presents a visual for '{sess.title}' but the audience asks, 'So what?' What is the strongest improvement?",
                "options": "A. Add more colors | B. Add a decision-oriented insight and implication | C. Remove the title | D. Hide the axis labels",
                "answer": "B",
                "explanation": f"The session takeaway is: {sess.takeaway} The visual must connect evidence to managerial meaning.",
            },
            {
                "session": str(sess.no),
                "clo": sess.clos,
                "q": f"For Session {sess.no}, which student output would show the best learning?",
                "options": "A. A decorative chart only | B. A chart with context, pattern, insight, and recommended action | C. A raw table with no interpretation | D. A screenshot without labels",
                "answer": "B",
                "explanation": "The course emphasizes visual storytelling, not isolated chart production.",
            },
            {
                "session": str(sess.no),
                "clo": sess.clos,
                "q": f"Which problem should be avoided while applying '{sess.title}'?",
                "options": f"A. {mistake} | B. Clear title | C. Appropriate context | D. Audience-specific explanation",
                "answer": "A",
                "explanation": f"This is listed as a common mistake for the session and can weaken interpretation.",
            },
            {
                "session": str(sess.no),
                "clo": sess.clos,
                "q": f"A manager has only 30 seconds to read the visual from Session {sess.no}. What should be most visible?",
                "options": "A. The software name | B. The file path | C. The main pattern and action implication | D. Every raw row",
                "answer": "C",
                "explanation": "Managerial communication requires fast orientation toward meaning and action.",
            },
            {
                "session": str(sess.no),
                "clo": sess.clos,
                "q": f"True or False: In '{sess.title}', the visual is stronger when it is connected to the audience's decision need.",
                "options": "True | False",
                "answer": "True",
                "explanation": "Audience and decision context are central to data storytelling.",
            },
        ])
    return extras


QUIZ_BANK.extend(build_extra_quizzes())



def build_deep_quizzes() -> List[Dict[str, str]]:
    """Add more practice questions covering interpretation, ethics, chart choice, and teaching-ready scenarios."""
    templates = [
        (
            "A student says the chart is complete because the numbers are correct. What should you ask next?",
            "A. What decision does the chart support? | B. Which font looks stylish? | C. Can we remove all labels? | D. Can we add a 3D effect?",
            "A",
            "Correct numbers are necessary, but data storytelling also requires decision relevance.",
        ),
        (
            "Which sentence best turns an observation into a managerial insight?",
            "A. The bar is blue | B. Sales are shown by region | C. West leads revenue, but Central needs diagnosis before budget allocation | D. There are five categories",
            "C",
            "A managerial insight connects a visible pattern to a decision or action implication.",
        ),
        (
            "What is the safest way to handle uncertainty in a visual story?",
            "A. Hide it | B. Mention limitations briefly and explain what can still be concluded | C. Use brighter colors | D. Remove the title",
            "B",
            "Responsible storytelling communicates both useful evidence and reasonable caution.",
        ),
        (
            "What should come immediately after showing a visible pattern?",
            "A. Add decoration | B. Explain why the pattern matters for the business problem | C. Change the software | D. Stop the presentation",
            "B",
            "The movement from pattern to meaning is the heart of data storytelling.",
        ),
        (
            "Which classroom answer shows strongest learning?",
            "A. I used a chart because it looks good | B. I chose this chart because it answers the comparison question clearly | C. I used all available colors | D. I copied the default output",
            "B",
            "Chart choice should be justified by the question, data type, and audience need.",
        ),
    ]
    deep: List[Dict[str, str]] = []
    for sess in SESSIONS:
        for idx, (q, options, answer, explanation) in enumerate(templates, start=1):
            deep.append({
                "session": str(sess.no),
                "clo": sess.clos,
                "q": f"Session {sess.no} application check {idx}: {q}",
                "options": options,
                "answer": answer,
                "explanation": f"{explanation} In this session, remember: {sess.takeaway}",
            })
    return deep


QUIZ_BANK.extend(build_deep_quizzes())






# -----------------------------------------------------------------------------
# V6 classroom delivery systems: modes, teaching flows, rubrics, exam bank
# -----------------------------------------------------------------------------

def apply_projector_mode(enabled: bool) -> None:
    """Increase readability for physical classrooms without changing app logic."""
    if enabled:
        st.markdown("<script>document.body.classList.add('projector-mode');</script>", unsafe_allow_html=True)
        st.markdown(
            """
            <style>
            .block-container { max-width: 1650px; }
            p, li, div[data-testid="stMarkdownContainer"], .callout, .quiz-card, .hint-card, .safe-table td, .safe-table th {
                font-size: 1.08rem !important;
                line-height: 1.55 !important;
            }
            button, input, textarea, select { font-size: 1.05rem !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def get_teaching_mode() -> str:
    return st.session_state.get("teaching_mode", "Instructor Mode")


def mode_banner() -> None:
    mode = get_teaching_mode()
    msg = (
        "Instructor Mode: full teaching guides, hints, board notes, expected answers, misconceptions, and facilitation prompts are visible."
        if mode == "Instructor Mode"
        else "Student Mode: explanations, practice tasks, quizzes, and reflection prompts are emphasized with reduced instructor-only detail."
    )
    st.markdown(f"<div class='mode-banner'>🎛️ {html.escape(msg)}</div>", unsafe_allow_html=True)


def session_flow_rows(sess: SessionInfo) -> List[Dict[str, str]]:
    return [
        {"Time": "0–5 min", "Segment": "Opening hook", "Instructor action": f"Start with a business situation linked to {sess.title}.", "Student output": "One quick answer or reaction."},
        {"Time": "5–15 min", "Segment": "Concept framing", "Instructor action": sess.objective, "Student output": "Identify the decision problem."},
        {"Time": "15–30 min", "Segment": "Visual demonstration", "Instructor action": f"Show the session demo and ask what pattern appears first. Focus on: {sess.takeaway}", "Student output": "Observation plus evidence."},
        {"Time": "30–50 min", "Segment": "Guided activity", "Instructor action": sess.mini_lab, "Student output": "Short chart/critique/storyboard draft."},
        {"Time": "50–62 min", "Segment": "Peer discussion", "Instructor action": "Ask pairs to improve each other's insight using evidence, implication, and action.", "Student output": "Improved action-oriented insight."},
        {"Time": "62–70 min", "Segment": "Quiz and misconception check", "Instructor action": "Use 3–5 reveal-answer questions and correct overclaims immediately.", "Student output": "Reasoned answer, not only option selection."},
        {"Time": "70–75 min", "Segment": "Closing reflection", "Instructor action": f"Close with: {sess.takeaway}", "Student output": "One manager-ready recommendation."},
    ]


def render_75_min_flow(sess: SessionInfo) -> None:
    st.markdown("#### ⏱️ 75-minute classroom flow")
    safe_dataframe(pd.DataFrame(session_flow_rows(sess)))
    flow_text = "\n".join([f"{r['Time']} | {r['Segment']} | {r['Instructor action']} | Student output: {r['Student output']}" for r in session_flow_rows(sess)])
    st.download_button("Download this 75-minute teaching flow", flow_text, file_name=f"session_{sess.no}_75_min_flow.txt", mime="text/plain", key=f"flow_download_{sess.no}")


def what_to_say_bank(sess: SessionInfo) -> Dict[str, str]:
    story = SESSION_STORY_CONTEXT.get(sess.no, {})
    scene = story.get("scene", f"A manager is working with {sess.title}.")
    data_moment = story.get("data_moment", sess.concept)
    return {
        "Opening the concept": f"Let us begin with a real management problem. {scene} The question is not only what chart to make; the question is what decision the visual should support.",
        "Explaining the chart": f"Look first at the visible pattern, not the decoration. The data moment here is: {data_moment} Now ask: which part of the chart supports that statement?",
        "Asking students": "Before I explain, write one observation and one decision implication. An observation describes what is visible; an implication explains why a manager should care.",
        "Correcting misconception": f"A common mistake here is: {sess.common_mistakes[0] if sess.common_mistakes else 'stopping at description'}. Let us correct it by reconnecting the visual to the business question.",
        "Moving to activity": f"Now apply the idea. Your task is: {sess.mini_lab} Do not only create a chart; write the headline that would help a manager act.",
        "Closing the concept": f"The key message to carry forward is: {sess.takeaway} In the next visual you create, check whether the audience can see this without you overexplaining.",
    }


def render_what_should_i_say(sess: SessionInfo) -> None:
    st.markdown("#### 🗣️ What should I say now?")
    moment = st.selectbox("Choose the teaching moment", list(what_to_say_bank(sess).keys()), key=f"say_moment_{sess.no}")
    if st.button("Show ready-to-speak line", key=f"say_button_{sess.no}"):
        st.session_state[f"say_reveal_{sess.no}"] = True
    if st.session_state.get(f"say_reveal_{sess.no}", False):
        st.markdown(f"<div class='say-card'>{html.escape(what_to_say_bank(sess)[moment])}</div>", unsafe_allow_html=True)
        st.markdown("**Follow-up prompts:**")
        st.markdown("- What evidence supports this statement?")
        st.markdown("- What could be misunderstood?")
        st.markdown("- What would change if the audience were a CEO rather than an analyst?")
        st.markdown("- What action can be recommended without overclaiming?")


def teaching_notes_text(sess: SessionInfo) -> str:
    story = SESSION_STORY_CONTEXT.get(sess.no, {})
    lines = [
        f"Session {sess.no}: {sess.title}",
        f"Module: {sess.module}",
        f"CLOs: {sess.clos}",
        "",
        "Learning objective:", sess.objective,
        "",
        "Concept explanation:", sess.concept,
        "",
        "Managerial value:", sess.manager_value,
        "",
        "Opening story:", story.get("scene", "Use a management meeting context."),
        "",
        "Data moment:", story.get("data_moment", sess.takeaway),
        "",
        "What to say:", what_to_say_bank(sess)["Opening the concept"],
        "",
        "Mini-lab:", sess.mini_lab,
        "",
        "Common mistakes:", "\n".join([f"- {m}" for m in sess.common_mistakes]),
        "",
        "75-minute flow:",
        "\n".join([f"- {r['Time']}: {r['Segment']} — {r['Instructor action']}" for r in session_flow_rows(sess)]),
        "",
        "Closing takeaway:", sess.takeaway,
    ]
    return "\n".join(lines)


RUBRICS: Dict[str, List[Dict[str, str]]] = {
    "Chart Design Rubric": [
        {"Criterion": "Question alignment", "Excellent": "Chart directly answers a clear managerial question.", "Good": "Chart mostly fits the question with minor ambiguity.", "Needs improvement": "Chart is made before the question is clear.", "Weight": "20%"},
        {"Criterion": "Chart selection", "Excellent": "Visual form matches data type and comparison need.", "Good": "Chart is acceptable but not the most efficient.", "Needs improvement": "Wrong visual form creates confusion.", "Weight": "20%"},
        {"Criterion": "Clarity and readability", "Excellent": "Labels, scale, sorting, and layout are easy to read.", "Good": "Readable with small formatting issues.", "Needs improvement": "Clutter, scale, or labels reduce interpretation.", "Weight": "20%"},
        {"Criterion": "Truthfulness", "Excellent": "Axis, scale, aggregation, and context are responsible.", "Good": "Mostly truthful with minor context missing.", "Needs improvement": "Design may exaggerate, hide, or overclaim.", "Weight": "20%"},
        {"Criterion": "Managerial takeaway", "Excellent": "Clear insight and decision implication are stated.", "Good": "Insight is present but action is weak.", "Needs improvement": "Only describes the chart without implication.", "Weight": "20%"},
    ],
    "Dashboard Critique Rubric": [
        {"Criterion": "Decision focus", "Excellent": "Dashboard is organized around one clear decision question.", "Good": "Decision focus is visible but broad.", "Needs improvement": "Dashboard is a collection of unrelated visuals.", "Weight": "25%"},
        {"Criterion": "Hierarchy", "Excellent": "Most important KPIs appear first with clear visual priority.", "Good": "Hierarchy is usable but could be sharper.", "Needs improvement": "Audience cannot tell what to inspect first.", "Weight": "20%"},
        {"Criterion": "Diagnostic depth", "Excellent": "Dashboard moves from KPI to explanation to action.", "Good": "Some diagnostic support is present.", "Needs improvement": "Dashboard reports numbers but does not explain drivers.", "Weight": "25%"},
        {"Criterion": "Design discipline", "Excellent": "Color, labels, spacing, and grouping reduce cognitive load.", "Good": "Mostly clean with minor clutter.", "Needs improvement": "Design choices compete for attention.", "Weight": "15%"},
        {"Criterion": "Actionability", "Excellent": "Recommended next step is clear and evidence-based.", "Good": "Action is suggested but could be stronger.", "Needs improvement": "No decision or recommendation emerges.", "Weight": "15%"},
    ],
    "Final Data Story Rubric": [
        {"Criterion": "Context and audience", "Excellent": "Audience, decision context, and stakes are clearly framed.", "Good": "Context is present but not fully audience-specific.", "Needs improvement": "Story begins with data without business context.", "Weight": "15%"},
        {"Criterion": "Evidence selection", "Excellent": "Only relevant visuals are used and sequenced logically.", "Good": "Mostly relevant visuals with some redundancy.", "Needs improvement": "Too many charts or weak evidence selection.", "Weight": "20%"},
        {"Criterion": "Narrative flow", "Excellent": "Context → evidence → insight → implication → action is coherent.", "Good": "Flow is understandable with minor jumps.", "Needs improvement": "Story feels like disconnected observations.", "Weight": "25%"},
        {"Criterion": "Visual integrity", "Excellent": "Design is clear, honest, and avoids misleading framing.", "Good": "Generally sound with minor issues.", "Needs improvement": "Visuals may mislead or lack context.", "Weight": "20%"},
        {"Criterion": "Recommendation", "Excellent": "Action is specific, justified, and acknowledges limitations.", "Good": "Action is reasonable but general.", "Needs improvement": "Recommendation is absent or unsupported.", "Weight": "20%"},
    ],
}


def build_exam_bank() -> List[Dict[str, str]]:
    base = []
    templates = [
        ("Short answer", "Explain why a chart title should communicate insight rather than merely name the variables.", "A strong title reduces interpretation effort and guides the audience toward the intended managerial meaning without hiding the evidence."),
        ("Chart diagnosis", "A bar chart compares branch performance but starts the y-axis at 80 instead of zero. What is the risk?", "The visual may exaggerate differences. If magnitude matters, a full baseline or explicit justification is needed."),
        ("Case question", "A hospital dashboard shows average waiting time declining, but the distribution has widened. What should the manager investigate?", "The manager should examine variability, outliers, department-level bottlenecks, and whether some patients still experience extreme waits."),
        ("Viva", "When would you prefer a dot plot over a bar chart?", "A dot plot is useful when comparing many categories with lower visual weight, especially when ranking is more important than filled magnitude."),
        ("Application", "Convert this observation into an insight: Region C sales fell for three months.", "Region C shows a sustained decline that may indicate local demand, channel, or service issues; management should diagnose the driver before increasing spend."),
    ]
    for sess in SESSIONS:
        for idx, (kind, question, answer) in enumerate(templates, start=1):
            base.append({
                "Session": str(sess.no),
                "Type": kind,
                "Question": f"Session {sess.no}: {question}",
                "Model Answer": f"{answer} Related takeaway: {sess.takeaway}",
                "CLOs": sess.clos,
            })
    return base


EXAM_BANK: List[Dict[str, str]] = build_exam_bank()


def render_rubric(rubric_name: str) -> None:
    st.markdown(f"### {rubric_name}")
    rows = RUBRICS[rubric_name]
    safe_dataframe(pd.DataFrame(rows))
    csv = to_csv_bytes(pd.DataFrame(rows))
    st.download_button("Download rubric as CSV", csv, file_name=f"{rubric_name.lower().replace(' ', '_')}.csv", mime="text/csv", key=f"rubric_{rubric_name}")


def render_bad_good_chart(issue: str) -> None:
    c1, c2 = st.columns(2)
    if issue == "Truncated axis":
        df = pd.DataFrame({"Branch": ["A", "B", "C", "D"], "Satisfaction": [86, 88, 84, 87]})
        with c1:
            fig = px.bar(df, x="Branch", y="Satisfaction", title="Weak: tiny differences look dramatic")
            fig.update_yaxes(range=[80, 90])
            fig.update_layout(height=390, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
            callout("Diagnosis", "The truncated axis exaggerates small differences and may create unnecessary alarm.", "danger")
        with c2:
            fig2 = px.bar(df, x="Branch", y="Satisfaction", title="Improved: all branches perform within a narrow satisfaction band")
            fig2.update_yaxes(range=[0, 100])
            fig2.update_layout(height=390, title_x=.02)
            st.plotly_chart(fig2, use_container_width=True)
            callout("Improved story", "The real message is consistency with a modest gap, not crisis.", "insight")
    elif issue == "Pie overload":
        df = retail_data().groupby("Category", as_index=False)["Sales"].sum()
        extra = pd.DataFrame({"Category": ["Accessories", "Toys", "Books", "Sports"], "Sales": [450, 380, 300, 260]})
        df = pd.concat([df, extra], ignore_index=True)
        with c1:
            fig = px.pie(df, names="Category", values="Sales", title="Weak: too many slices for clear ranking")
            fig.update_layout(height=390, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
            callout("Diagnosis", "Many similar slices make comparison slow and imprecise.", "danger")
        with c2:
            st.plotly_chart(ranked_bar(df, "Category", "Sales", "Improved: sorted categories reveal the biggest contributors"), use_container_width=True)
            callout("Improved story", "The sorted bar chart shows contribution and priority more clearly.", "insight")
    elif issue == "Color overload":
        df = retail_data().groupby("Category", as_index=False)["Profit"].sum()
        with c1:
            fig = px.bar(df, x="Category", y="Profit", color="Category", title="Weak: every category competes for attention")
            fig.update_layout(height=390, title_x=.02, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            callout("Diagnosis", "Color is used as decoration rather than emphasis, so the key message is unclear.", "danger")
        with c2:
            focus = df.loc[df["Profit"].idxmax(), "Category"]
            df["Focus"] = np.where(df["Category"] == focus, "Priority", "Context")
            fig2 = px.bar(df, x="Category", y="Profit", color="Focus", title=f"Improved: {focus} is the profit leader")
            fig2.update_layout(height=390, title_x=.02, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
            callout("Improved story", "Use most color for context and one highlight for the takeaway.", "insight")
    else:
        df = pd.DataFrame({"Month": pd.date_range("2025-01-01", periods=6, freq="MS"), "Revenue": [100, 103, 108, 125, 128, 132]})
        with c1:
            shuffled = df.sample(frac=1, random_state=2)
            fig = px.line(shuffled, x="Month", y="Revenue", markers=True, title="Weak: time points are not narrated or contextualized")
            fig.update_layout(height=390, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
            callout("Diagnosis", "The chart shows movement but does not explain the turning point or implication.", "danger")
        with c2:
            fig2 = px.line(df, x="Month", y="Revenue", markers=True, title="Improved: revenue steps up after April and remains above baseline")
            add_vertical_marker(fig2, pd.Timestamp("2025-04-01"), "Intervention")
            fig2.update_layout(height=390, title_x=.02)
            st.plotly_chart(fig2, use_container_width=True)
            callout("Improved story", "Add an event marker and an action-oriented headline to guide interpretation.", "insight")


def auto_story_from_dataframe(df: pd.DataFrame, audience: str, question: str) -> Dict[str, str]:
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    cat = df.select_dtypes(exclude=np.number).columns.tolist()
    if numeric:
        main_metric = numeric[0]
        if cat:
            group = cat[0]
            grouped = df.groupby(group, as_index=False)[main_metric].sum().sort_values(main_metric, ascending=False)
            top = grouped.iloc[0][group]
            pattern = f"{top} has the highest {main_metric} among {group} categories."
            visual = f"Ranked bar chart of {main_metric} by {group}"
        else:
            pattern = f"{main_metric} ranges from {df[main_metric].min():.2f} to {df[main_metric].max():.2f}, with an average of {df[main_metric].mean():.2f}."
            visual = f"Histogram or box plot of {main_metric}"
    else:
        pattern = "The uploaded data has no numeric columns, so the first step is to define measurable outcomes."
        visual = "Frequency table or bar chart after selecting a countable category"
    return {
        "Audience": audience,
        "Question": question,
        "Suggested visual": visual,
        "Possible pattern": pattern,
        "Managerial implication": "Use the visible pattern to prioritize diagnosis, resource allocation, or follow-up discussion.",
        "Caution": "Check sample size, missing values, definitions, and whether the pattern is stable before making a final recommendation.",
    }


def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        if name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read file: {exc}")
        return None
    st.warning("Please upload a CSV or Excel file.")
    return None


def page_instructor_planner() -> None:
    hero("Instructor Delivery Planner", "Teach without remembering sequence: choose a session and get the full 75-minute flow, teaching guide, board notes, prompts, activities, and downloadable teaching notes.", ["Instructor Mode", "75-min Flow", "Teaching Notes"])
    mode_banner()
    selected = st.selectbox("Choose session", [f"Session {s.no}: {s.title}" for s in SESSIONS], key="planner_session")
    no = int(selected.split(":")[0].replace("Session", "").strip())
    sess = next(s for s in SESSIONS if s.no == no)
    c1, c2 = st.columns([1, 1])
    with c1:
        callout("Session objective", sess.objective, "insight")
        callout("Closing takeaway", sess.takeaway, "purple")
    with c2:
        callout("Mini-lab", sess.mini_lab, "warning")
        callout("Common misconception", sess.common_mistakes[0] if sess.common_mistakes else "Students may stop at description instead of implication.", "danger")
    render_75_min_flow(sess)
    render_what_should_i_say(sess)
    st.markdown("#### Download complete teaching notes")
    st.download_button("Download session teaching notes", teaching_notes_text(sess), file_name=f"session_{sess.no}_complete_teaching_notes.txt", mime="text/plain", key=f"planner_notes_{sess.no}")


def page_visual_makeover() -> None:
    hero("Before–After Visual Makeover Studio", "Show students how weak visuals become honest, clear, and decision-ready stories.", ["Bad Chart", "Diagnosis", "Improved Chart", "Takeaway"])
    issue = st.selectbox("Choose makeover scenario", ["Truncated axis", "Pie overload", "Color overload", "Missing annotation"])
    render_bad_good_chart(issue)
    st.markdown("### Makeover checklist")
    checklist = pd.DataFrame([
        {"Step": "1. Clarify question", "Prompt": "What decision should this visual support?"},
        {"Step": "2. Check truthfulness", "Prompt": "Could the scale, aggregation, or omission mislead?"},
        {"Step": "3. Reduce clutter", "Prompt": "What can be removed without losing meaning?"},
        {"Step": "4. Add emphasis", "Prompt": "What should the audience see first?"},
        {"Step": "5. Rewrite title", "Prompt": "Does the title state the insight?"},
        {"Step": "6. Add action", "Prompt": "What should a manager do next?"},
    ])
    safe_dataframe(checklist)
    issue_solutions = {
        "Truncated axis": "Model solution: restore the baseline or clearly justify the scale, rewrite the title to show the true magnitude, and avoid presenting a modest difference as a crisis.",
        "Pie overload": "Model solution: replace the crowded pie with a sorted bar chart, group small categories only when appropriate, and write a title that identifies the largest contributor.",
        "Color overload": "Model solution: use neutral colors for context and one intentional highlight for the priority item. Color should guide attention, not decorate the chart.",
        "Missing annotation": "Model solution: add an event marker, label the turning point, and connect the visible change to a cautious managerial implication."
    }
    callout("Model makeover solution", issue_solutions.get(issue, "Improve the chart by clarifying the question, correcting the visual encoding, and adding an action-oriented title."), "insight")


def page_rubrics_exam_bank() -> None:
    hero("Rubrics and Exam Question Bank", "Ready-to-use assessment tools for chart design, dashboard critique, final data stories, viva, and end-term preparation.", ["Rubrics", f"{len(EXAM_BANK)} Questions", "Model Answers"])
    tab1, tab2, tab3 = st.tabs(["Rubrics", "Exam/Viva Bank", "Assessment Generator"])
    with tab1:
        rubric_name = st.selectbox("Choose rubric", list(RUBRICS.keys()))
        render_rubric(rubric_name)
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            sess_filter = st.selectbox("Session", ["All"] + [str(i) for i in range(1, 17)], key="exam_session")
        with c2:
            type_filter = st.selectbox("Question type", ["All"] + sorted(set(q["Type"] for q in EXAM_BANK)), key="exam_type")
        qs = EXAM_BANK
        if sess_filter != "All":
            qs = [q for q in qs if q["Session"] == sess_filter]
        if type_filter != "All":
            qs = [q for q in qs if q["Type"] == type_filter]
        st.write(f"Showing {len(qs)} matching questions.")
        for i, q in enumerate(qs[:20], start=1):
            with st.expander(f"Q{i}. {q['Type']} — Session {q['Session']}"):
                st.write(q["Question"])
                st.markdown("**Model answer**")
                st.write(q["Model Answer"])
                st.caption(q["CLOs"])
        st.download_button("Download filtered question bank", to_csv_bytes(pd.DataFrame(qs)), file_name="exam_viva_question_bank.csv", mime="text/csv")
    with tab3:
        st.markdown("Generate a quick assessment mix for class, quiz, viva, or end-term revision.")
        n_short = st.slider("Number of questions", 3, 20, 8)
        sample = pd.DataFrame(EXAM_BANK).sample(n=min(n_short, len(EXAM_BANK)), random_state=n_short)
        safe_dataframe(sample[["Session", "Type", "Question", "CLOs"]])
        st.download_button("Download generated assessment", to_csv_bytes(sample), file_name="generated_assessment.csv", mime="text/csv")


def page_upload_auto_story() -> None:
    hero("Upload and Auto-Story Lab", "Upload a CSV or Excel file, preview the data, identify possible visuals, and generate a first-pass managerial story.", ["CSV", "Excel", "Auto Story", "No API"])
    c1, c2 = st.columns([.9, 1.1])
    with c1:
        uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
        audience = st.selectbox("Audience", ["Executive Committee", "Functional Manager", "Healthcare Administrator", "Marketing Head", "Operations Head", "Student Presentation Panel"])
        question = st.text_area("Decision question", value="What should management notice first, and where should action be prioritized?")
    df = read_uploaded_file(uploaded)
    if df is None:
        st.info("Upload a file to activate auto-story mode. Until then, use any built-in dataset from the Resources or Final Workshop pages.")
        return
    with c2:
        metric_box("Rows", f"{len(df):,}", "uploaded")
        metric_box("Columns", f"{len(df.columns):,}", "detected")
    st.subheader("Preview")
    safe_dataframe(df, max_rows=20)
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    cat = df.select_dtypes(exclude=np.number).columns.tolist()
    st.subheader("Automatic column reading")
    safe_dataframe(pd.DataFrame({"Numeric columns": pd.Series(numeric), "Categorical/date/text columns": pd.Series(cat)}))
    if numeric:
        st.subheader("Suggested first visual")
        if cat:
            group = st.selectbox("Group by", cat)
            metric = st.selectbox("Metric", numeric)
            d = df.groupby(group, as_index=False)[metric].sum().sort_values(metric, ascending=True).tail(15)
            st.plotly_chart(px.bar(d, x=metric, y=group, orientation="h", title=f"Ranked {metric} by {group}"), use_container_width=True)
        else:
            metric = st.selectbox("Metric", numeric)
            st.plotly_chart(px.histogram(df, x=metric, title=f"Distribution of {metric}"), use_container_width=True)
    story = auto_story_from_dataframe(df, audience, question)
    st.subheader("Generated first-pass story")
    for k, v in story.items():
        callout(k, v, "insight" if k in ["Suggested visual", "Possible pattern"] else "purple")
    with st.expander("Model solution structure for this uploaded dataset", expanded=True):
        callout("Solution sentence", f"Because {story['Possible pattern']} the {audience.lower()} should use {story['Suggested visual'].lower()} to decide the first diagnostic or resource-allocation priority.", "insight")
        callout("What students should submit", "One visual, one insight headline, two evidence points, one recommendation, and one limitation. The recommendation should be cautious unless the dataset supports causal interpretation.", "warning")
    md = "\n".join([f"**{k}:** {v}" for k, v in story.items()])
    st.download_button("Download auto-story draft", md, file_name="uploaded_data_story_draft.md", mime="text/markdown")


def page_role_play_mode() -> None:
    hero("Business Role-Play Mode", "Use the same visual from different managerial perspectives to make data storytelling more realistic and discussion-oriented.", ["CEO", "Finance", "Operations", "Marketing", "Healthcare"])
    case_name = st.selectbox("Choose case", list(CASE_LIBRARY.keys()), key="role_case")
    case = CASE_LIBRARY[case_name]
    df = render_case_visual(case["domain"])
    render_case_solution(case_name, case, df, expanded=False)
    roles = {
        "CEO": "What is the strategic priority and what trade-off are we accepting?",
        "Finance Controller": "What is the financial risk, budget impact, or cost-control implication?",
        "Operations Head": "Where is the process constraint and what should be fixed first?",
        "Marketing Head": "Which customer, channel, or segment action is justified by the pattern?",
        "Data Analyst": "What evidence supports the claim, and what limitation should be disclosed?",
        "Healthcare Administrator": "What patient-flow, capacity, safety, or service-quality implication emerges?",
    }
    st.markdown("### Role cards")
    cols = st.columns(2)
    for i, (role, prompt) in enumerate(roles.items()):
        with cols[i % 2]:
            st.markdown(f"<div class='role-card'><b>{html.escape(role)}</b><br>{html.escape(prompt)}<br><br><i>Sentence starter:</i> From my role, the most important implication is...</div>", unsafe_allow_html=True)
    st.markdown("### Group output")
    role = st.selectbox("Selected role", list(roles.keys()))
    response = st.text_area("Role-based interpretation", placeholder="Write one interpretation, one concern, and one recommendation.")
    if response:
        callout(f"{role} interpretation", response, "insight")
    st.download_button("Download role-play case dataset", to_csv_bytes(df), file_name=f"{case_name.lower().replace(' ', '_')}_roleplay.csv", mime="text/csv")


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------
def page_home() -> None:
    hero(
        "Storytelling using Data Visualization",
        "A complete interactive teaching studio for PGDM-BDA Term 1. This app teaches visual reasoning, chart selection, dashboard critique, narrative design, and managerial recommendation using built-in datasets and no-cost tools.",
        ["PGDM-BDA", "2 Credits", "16 Sessions", "Offline / Blended", "No API Calls"],
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_box("Course Sessions", "16", "75 minutes each")
    with c2:
        metric_box("Modules", "4", "Foundation to strategy")
    with c3:
        metric_box("Quiz Bank", f"{len(QUIZ_BANK)}", "With explanations")
    with c4:
        metric_box("Datasets", "8", "Generated inside app")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        metric_box("Rubrics", f"{len(RUBRICS)}", "Assessment ready")
    with c6:
        metric_box("Exam Bank", f"{len(EXAM_BANK)}", "Model answers")
    with c7:
        metric_box("Visual Gallery", f"{len(CHART_GALLERY)}", "Live examples")
    with c8:
        metric_box("Activities", f"{len(ACTIVITY_BANK)}", "Classroom-ready")

    st.subheader("Course Learning Outcome Cards")
    cols = st.columns(4)
    clo_cards = [
        ("CLO1", "Explain the role of visualization in analytics-driven management solutions.", ["Understand", "Decision context"]),
        ("CLO2", "Select and design charts, dashboards, and layouts for stakeholder needs.", ["Analyze", "Chart selection"]),
        ("CLO3", "Construct coherent and decision-oriented narratives from data.", ["Create", "Story logic"]),
        ("CLO4", "Communicate insights and strategic recommendations through visual stories.", ["Evaluate", "Recommendation"]),
    ]
    for col, (title, body, tags) in zip(cols, clo_cards):
        with col:
            card(title, body, tags)

    st.subheader("Visual Course Roadmap")
    module_groups: Dict[str, List[SessionInfo]] = {}
    for s in SESSIONS:
        module_groups.setdefault(s.module, []).append(s)
    cols = st.columns(4)
    for col, (module, sess) in zip(cols, module_groups.items()):
        bg = MODULE_COLORS[module]
        with col:
            items = "".join([f"<li><b>S{s.no}</b>: {s.title}</li>" for s in sess])
            st.markdown(
                f"""
                <div class="module-card" style="background:{bg};">
                    <h3>{module}</h3>
                    <ul>{items}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("How to use this app in class")
    process_diagram(["Start with session page", "Explain concept", "Run demo", "Do lab", "Reveal quiz", "Reflect"])
    callout("Instructor note", "Every session page is structured as Concept → Diagram → Demo → Lab → Quiz → Reflection. The app is designed to replace PPT-based delivery for this course.", "insight")


def page_roadmap() -> None:
    hero("Course Roadmap", "Use this page to plan the 16-session flow, map sessions to CLOs, and align classroom activities with outcomes.", ["Roadmap", "CLO Mapping", "75-min Flow"])
    roadmap_rows = []
    for s in SESSIONS:
        roadmap_rows.append({"Session": s.no, "Module": s.module, "Topic": s.title, "CLOs": s.clos, "Suggested 75-min Flow": "15m concept + 25m demo + 25m lab + 10m quiz/reflection"})
    safe_dataframe(pd.DataFrame(roadmap_rows))

    st.subheader("CLO Coverage View")
    clo_count = pd.Series([c.strip() for s in SESSIONS for c in s.clos.replace("–", ",").split(",")]).value_counts().reset_index()
    clo_count.columns = ["CLO", "Session Mentions"]
    fig = px.bar(clo_count, x="CLO", y="Session Mentions", text="Session Mentions", title="CLO coverage across the course")
    fig.update_layout(height=390, title_x=.02)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Reusable 75-minute Teaching Flow")
    c1, c2, c3, c4, c5 = st.columns(5)
    flows = [("Concept", "15 min", "Introduce principle"), ("Demonstration", "20–25 min", "Show interactive visual"), ("Hands-on Lab", "25 min", "Students apply"), ("Quiz", "7 min", "Check understanding"), ("Reflection", "3–8 min", "Convert to action")]
    for col, (a, b, c) in zip([c1, c2, c3, c4, c5], flows):
        with col:
            metric_box(a, b, c)

    st.subheader("Session-specific delivery plan")
    selected = st.selectbox("Choose a session for detailed 75-minute flow", [f"Session {s.no}: {s.title}" for s in SESSIONS], key="roadmap_flow_session")
    no = int(selected.split(":")[0].replace("Session", "").strip())
    render_75_min_flow(next(s for s in SESSIONS if s.no == no))


def page_session_studio() -> None:
    hero("Session Learning Studio", "Teach any session with ready-to-speak stories, hints, examples, diagrams, demos, mini-labs, quizzes, and reflection prompts.", ["Concept", "Demo", "Lab", "Quiz", "Reflection"])
    selected = st.selectbox("Choose session", [f"Session {s.no}: {s.title}" for s in SESSIONS])
    no = int(selected.split(":")[0].replace("Session", "").strip())
    sess = next(s for s in SESSIONS if s.no == no)

    mode_banner()
    st.markdown(f"### Session {sess.no}: {sess.title}")
    st.markdown(f"<span class='tag'>{sess.module}</span><span class='tag'>{sess.clos}</span>", unsafe_allow_html=True)

    if "completed" not in st.session_state:
        st.session_state.completed = set()
    completed = st.checkbox("Mark this session as completed", value=no in st.session_state.completed)
    if completed:
        st.session_state.completed.add(no)
    else:
        st.session_state.completed.discard(no)
    st.progress(len(st.session_state.completed) / len(SESSIONS))
    st.caption(f"Course progress: {len(st.session_state.completed)} of {len(SESSIONS)} sessions marked complete")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Concept", "What to Say", "75-min Flow", "Diagram", "Interactive Demo", "Mini-Lab", "Quiz", "Reflection"])
    with tab1:
        callout("Learning objective", sess.objective, "insight")
        st.write(sess.concept)
        callout("Why this matters for managers", sess.manager_value, "purple")
        story_key = f"show_story_{sess.no}"
        if story_key not in st.session_state:
            st.session_state[story_key] = False
        if st.button("📖 Tell me the story", key=f"tell_story_{sess.no}"):
            st.session_state[story_key] = not st.session_state[story_key]
        if st.session_state[story_key]:
            render_concept_story(sess)
        st.markdown("**Common mistakes to avoid**")
        for m in sess.common_mistakes:
            st.markdown(f"- {m}")
        callout("Session takeaway", sess.takeaway, "insight")
    with tab2:
        render_what_should_i_say(sess)
        st.download_button("Download complete teaching notes", teaching_notes_text(sess), file_name=f"session_{sess.no}_teaching_notes.txt", mime="text/plain", key=f"session_notes_{sess.no}")
    with tab3:
        render_75_min_flow(sess)
    with tab4:
        st.write("Use this flow to explain the session logic visually.")
        process_diagram(sess.diagram_steps)
        st.caption("Classroom prompt: ask students where misinterpretation can enter this flow.")
    with tab5:
        render_session_demo(sess.no)
    with tab6:
        callout("Mini-lab task", sess.mini_lab, "warning")
        domain = st.selectbox("Download a practice dataset", DATASET_OPTIONS, key=f"lab_dataset_{sess.no}")
        df = get_dataset(domain)
        safe_dataframe(df, max_rows=20)
        st.download_button("Download this dataset as CSV", to_csv_bytes(df), file_name=f"{domain.lower().replace(' ', '_')}.csv", mime="text/csv", key=f"download_lab_{sess.no}")
        st.markdown("#### More activity options for this session")
        sess_activities = [a for a in ACTIVITY_BANK if a["Session"] == str(sess.no)]
        for a in sess_activities[:8]:
            with st.expander(a["Activity"]):
                st.write(a["Instruction"])
                st.write(f"**Expected output:** {a['Student Output']}")
                st.write(f"**Debrief:** {a['Debrief Question']}")
        student_note = st.text_area("Student workspace: write a one-sentence visual insight", key=f"lab_note_{sess.no}", placeholder="Example: The West region leads profit, but Central shows stronger satisfaction and may offer a scalable service model.")
        if student_note:
            callout("Draft insight", student_note, "insight")
    with tab7:
        relevant = [q for q in QUIZ_BANK if str(sess.no) == q["session"]]
        if not relevant:
            relevant = QUIZ_BANK[:3]
        quiz_limit = st.slider("How many questions for this session?", 3, min(12, len(relevant)), min(7, len(relevant)), key=f"session_quiz_limit_{sess.no}")
        for idx, q in enumerate(relevant[:quiz_limit], start=1):
            render_quiz_card(idx, q, show_tags=False)
            with st.expander("Reveal answer and explanation"):
                st.write(f"**Answer:** {q['answer']}")
                st.write(q["explanation"])
    with tab8:
        prompt = f"After Session {sess.no}, what would a manager conclude and what action would you recommend?"
        reflection = st.text_area(prompt, key=f"reflect_{sess.no}")
        if reflection:
            st.success("Reflection captured. Use it as a class discussion note or short submission.")
        summary = f"Session {sess.no}: {sess.title}\nCLOs: {sess.clos}\nTakeaway: {sess.takeaway}\nReflection: {reflection or '[write reflection]'}"
        st.download_button("Download session reflection", summary, file_name=f"session_{sess.no}_reflection.txt", key=f"reflection_download_{sess.no}")


def recommend_chart(data_type: str, question: str, audience: str) -> Tuple[str, str, str]:
    rules = {
        "Compare or rank": ("Ranked bar chart or dot plot", "Makes category comparison and rank easy to see."),
        "Show trend": ("Line chart", "Best for direction, change, seasonality, and turning points."),
        "Show distribution": ("Histogram or box plot", "Reveals spread, skew, and outliers beyond the average."),
        "Show relationship": ("Scatter plot or bubble chart", "Shows association, clusters, and exceptions."),
        "Show composition": ("Stacked bar, 100% stacked bar, treemap, or limited pie", "Shows contribution to a whole."),
        "Show deviation": ("Diverging bar or variance chart", "Highlights positive and negative gaps against a benchmark."),
    }
    chart, reason = rules[question]
    caution = "For executives, add an analytical title and a visible recommendation." if audience == "Executive" else "For analysts, include enough detail for diagnosis without clutter."
    if data_type == "Geospatial" and question in ["Compare or rank", "Show deviation"]:
        chart = "Map plus ranked bar chart"
        reason = "The map gives location context, while the ranked bar prevents geographic area from distorting comparison."
    return chart, reason, caution


def page_chart_engine() -> None:
    hero("Chart Selection Engine", "Select the data type, business question, and audience. The app recommends chart forms and explains the reasoning.", ["CLO2", "Chart Logic", "Managerial Fit"])
    c1, c2, c3 = st.columns(3)
    with c1:
        data_type = st.selectbox("Data type", ["Categorical", "Numerical", "Time-series", "Geospatial", "Relational", "Hierarchical"])
    with c2:
        question = st.selectbox("Business question", ["Compare or rank", "Show trend", "Show distribution", "Show relationship", "Show composition", "Show deviation"])
    with c3:
        audience = st.selectbox("Audience", ["Executive", "Analyst", "Customer", "Operations Manager", "Healthcare Manager"])
    chart, reason, caution = recommend_chart(data_type, question, audience)
    callout("Recommended visual form", f"<b>{chart}</b><br>{reason}", "insight")
    callout("Audience adaptation", caution, "purple")

    st.subheader("Live example")
    if question == "Compare or rank":
        df = retail_data().groupby("Region", as_index=False)["Sales"].sum()
        st.plotly_chart(ranked_bar(df, "Region", "Sales", "Regional ranking clarifies where sales momentum is strongest"), use_container_width=True)
    elif question == "Show trend":
        render_time_series_demo()
    elif question == "Show distribution":
        render_distribution_demo()
    elif question == "Show relationship":
        render_relationship_demo()
    elif question == "Show composition":
        render_composition_demo()
    else:
        df = finance_data()
        fig = px.bar(df, x="Department", y="Variance", color="Risk", title="Variance chart reveals departments above and below budget")
        fig.add_hline(y=0, line_dash="dash")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)


def render_misleading_clinic(inline: bool = False) -> None:
    issue = st.selectbox(
        "Select misleading-chart problem",
        ["Truncated axis", "Wrong chart type", "3D-style distortion", "Poor color use", "Too many categories", "Pie chart overload", "Misleading time scale", "Decorative overload"],
        key="clinic_issue_inline" if inline else "clinic_issue",
    )
    c1, c2 = st.columns(2)
    if issue == "Truncated axis":
        df = pd.DataFrame({"Branch": ["A", "B", "C", "D"], "Score": [82, 84, 85, 86]})
        fig1 = px.bar(df, x="Branch", y="Score", title="Weak: Axis exaggerates the difference")
        fig1.update_yaxes(range=[80, 87])
        fig2 = px.bar(df, x="Branch", y="Score", title="Improved: Full scale shows modest differences")
        fig2.update_yaxes(range=[0, 100])
        why = "The weak chart makes small differences look dramatic."
        fix = "Use a responsible scale and explain the real magnitude."
    elif issue == "Wrong chart type":
        df = marketing_data()
        fig1 = px.pie(df, names="Channel", values="Revenue", title="Weak: Pie makes ranking difficult")
        fig2 = ranked_bar(df, "Channel", "Revenue", "Improved: Ranked bars reveal channel contribution")
        why = "The pie chart makes it harder to compare several categories precisely."
        fix = "Use sorted bars when ranking and comparison are the story."
    elif issue == "3D-style distortion":
        df = finance_data()
        fig1 = px.bar(df, x="Department", y="Actual", title="Weak: Decorative effects would distort attention")
        fig1.update_traces(marker_line_width=4, opacity=.65)
        fig2 = ranked_bar(df, "Department", "Actual", "Improved: Clean comparison of actual expenditure")
        why = "3D-style embellishment can distort perception and distract from values."
        fix = "Keep the geometry simple and readable."
    elif issue == "Poor color use":
        df = retail_data().groupby("Category", as_index=False)["Profit"].sum()
        fig1 = px.bar(df, x="Category", y="Profit", color="Category", title="Weak: Every category competes for attention")
        df["Focus"] = np.where(df["Category"] == df.loc[df["Profit"].idxmax(), "Category"], "Focus", "Context")
        fig2 = px.bar(df, x="Category", y="Profit", color="Focus", title="Improved: One meaningful highlight")
        why = "Too many colors make every item look equally important."
        fix = "Use color to encode meaning or direct attention."
    elif issue == "Too many categories":
        df = pd.DataFrame({"Item": [f"Item {i}" for i in range(1, 22)], "Value": np.random.default_rng(3).integers(20, 110, 21)})
        fig1 = px.bar(df, x="Item", y="Value", title="Weak: Too many categories crowd the chart")
        top = df.nlargest(8, "Value").sort_values("Value")
        fig2 = px.bar(top, x="Value", y="Item", orientation="h", title="Improved: Focus on top drivers")
        why = "The audience cannot easily identify priorities in a crowded view."
        fix = "Group, filter, or focus on top contributors."
    elif issue == "Pie chart overload":
        df = pd.DataFrame({"Segment": [f"Segment {i}" for i in range(1, 12)], "Share": np.random.default_rng(5).integers(3, 20, 11)})
        fig1 = px.pie(df, names="Segment", values="Share", title="Weak: Too many slices")
        fig2 = ranked_bar(df, "Segment", "Share", "Improved: Sorted bars make contribution clearer")
        why = "Many slices are difficult to compare accurately."
        fix = "Use sorted bars or group smaller categories."
    elif issue == "Misleading time scale":
        df = pd.DataFrame({"Date": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-06-01", "2025-07-01", "2025-12-01"]), "Value": [100, 112, 118, 130, 135]})
        fig1 = px.line(df.assign(Point=[1, 2, 3, 4, 5]), x="Point", y="Value", markers=True, title="Weak: Equal spacing hides unequal time gaps")
        fig2 = px.line(df, x="Date", y="Value", markers=True, title="Improved: True date scale reveals timing")
        why = "Equal spacing makes irregular intervals appear regular."
        fix = "Use actual dates or clearly explain interval differences."
    else:
        df = operations_data().groupby("Plant", as_index=False)["Delay Days"].mean()
        fig1 = px.bar(df, x="Plant", y="Delay Days", title="Weak: Decorative framing distracts from delay priority")
        fig1.update_layout(images=[])
        fig2 = ranked_bar(df, "Plant", "Delay Days", "Improved: Delay ranking identifies plants needing process attention")
        why = "Decoration consumes attention that should go to the evidence."
        fix = "Remove non-data ink and strengthen the message."
    with c1:
        st.caption("Weak version")
        fig1.update_layout(height=400, title_x=.02)
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.caption("Improved version")
        fig2.update_layout(height=400, title_x=.02)
        st.plotly_chart(fig2, use_container_width=True)
    callout("Why it misleads", why, "danger")
    callout("How to correct it", fix, "insight")


def page_misleading_clinic() -> None:
    hero("Misleading Chart Clinic", "Diagnose weak visual stories and redesign them into truthful, decision-oriented visuals.", ["Critique", "Redesign", "Ethics"])
    render_misleading_clinic()


def page_dashboard_studio() -> None:
    hero("Dashboard Design Studio", "Build a dashboard wireframe for a specific audience, decision question, and business domain.", ["KPI", "Layout", "Executive View"])
    c1, c2, c3 = st.columns(3)
    with c1:
        domain = st.selectbox("Business domain", ["Retail Sales", "Marketing Campaign", "Financial Expenses", "Healthcare Patient Flow"])
    with c2:
        audience = st.selectbox("Audience", ["Executive Committee", "Operations Head", "Marketing Manager", "Hospital Administrator", "Finance Controller"])
    with c3:
        layout = st.selectbox("Layout logic", ["Executive summary first", "Diagnosis first", "Exception first"])
    question = st.text_input("Main decision question", value="Where should management focus attention this month?")
    callout("Dashboard brief", f"Audience: <b>{audience}</b><br>Question: <b>{question}</b><br>Layout: <b>{layout}</b>", "purple")
    process_diagram(["Decision Question", "KPI Summary", "Trend/Comparison", "Exception", "Recommended Action"])
    render_dashboard_demo(domain)
    critique = {
        "Executive summary first": "Good for senior leaders who need priority metrics before detail. Keep the first row limited to the most decision-relevant KPIs.",
        "Diagnosis first": "Useful when the audience already knows the problem and wants causes. Ensure the dashboard still states the headline insight.",
        "Exception first": "Effective for operational review. Highlight risk areas, but avoid hiding normal context."
    }
    callout("Auto-critique", critique[layout], "insight")


def page_story_builder() -> None:
    hero("Storytelling Framework Builder", "Convert observations into a complete data story using context, evidence, insight, implication, and action.", ["CLO3", "CLO4", "Narrative"])
    c1, c2 = st.columns(2)
    with c1:
        context = st.text_area("1. Context", value="A business unit is reviewing performance across regions and categories.")
        question = st.text_area("2. Business question", value="Which area requires management attention and what action should be taken?")
        evidence = st.text_area("3. Data evidence", value="Sales, profit, customer satisfaction, and discount patterns were compared.")
        pattern = st.text_area("4. Visual pattern", value="One region leads sales, while another shows weaker performance and lower satisfaction.")
    with c2:
        insight = st.text_area("5. Insight", value="The underperforming region may need service diagnosis rather than only additional promotion.")
        implication = st.text_area("6. Implication", value="If the issue is not addressed, revenue growth may remain uneven and customer experience may decline.")
        recommendation = st.text_area("7. Recommendation", value="Run a focused review of service quality and category mix in the weak region.")
        action = st.text_area("8. Action", value="Assign a two-week diagnostic sprint and report the top three improvement levers.")
    narrative = f"""
**Context:** {context}

**Business Question:** {question}

**Evidence:** {evidence}

**Pattern:** {pattern}

**Insight:** {insight}

**Implication:** {implication}

**Recommendation:** {recommendation}

**Action:** {action}
""".strip()
    st.subheader("Generated Visual Story")
    st.markdown(narrative)
    st.download_button("Download visual story summary", narrative, file_name="visual_story_summary.md", mime="text/markdown")


def page_title_lab() -> None:
    hero("Annotation and Title Lab", "Practice moving from descriptive titles to analytical and action-oriented headlines.", ["Titles", "Captions", "Annotations"])
    render_annotation_demo()
    st.subheader("Rewrite your own title")
    current = st.text_input("Descriptive title", value="Monthly Revenue and Cost")
    insight = st.text_input("What is the insight?", value="Revenue improved after the campaign launch")
    action = st.text_input("What action should management consider?", value="Continue campaign investment but monitor cost growth")
    st.markdown("#### Suggested title ladder")
    st.markdown(f"- **Descriptive:** {current}")
    st.markdown(f"- **Analytical:** {insight}")
    st.markdown(f"- **Action-oriented:** {action}")
    callout("Writing principle", "A strong title should not overclaim. It should make the intended interpretation clear and support the evidence shown.", "warning")


CASE_LIBRARY = {
    "Sales performance story": {
        "domain": "Retail Sales",
        "context": "A national retail firm wants to identify which regions and categories should receive managerial attention.",
        "question": "Which region-category combinations drive performance and where is intervention needed?",
        "recommended": "Use ranked bars for regional performance, heatmaps for region-category pockets, and a short recommendation on focus areas.",
    },
    "Marketing campaign story": {
        "domain": "Marketing Campaign",
        "context": "A campaign team is reviewing spend efficiency across channels.",
        "question": "Which channels generate the strongest return and where should budget be reallocated?",
        "recommended": "Use spend-versus-revenue scatter, ranked revenue bars, and conversion-rate comparison.",
    },
    "Operations delay story": {
        "domain": "Operations Delays",
        "context": "An operations head wants to reduce delays and defects across plants.",
        "question": "Which plants show delay pressure and how does it relate to output and defects?",
        "recommended": "Use plant delay rankings, weekly trends, and delay-defect relationship plots.",
    },
    "Finance cost-control story": {
        "domain": "Financial Expenses",
        "context": "A finance controller is reviewing department-level budget discipline.",
        "question": "Which departments exceed budget and require corrective action?",
        "recommended": "Use budget-versus-actual grouped bars and variance chart with risk labels.",
    },
    "Healthcare hospital dashboard story": {
        "domain": "Healthcare Patient Flow",
        "context": "A hospital administrator wants to monitor patient volume, waiting time, occupancy, and readmission signals.",
        "question": "Where is patient-flow pressure highest and what action should be prioritized?",
        "recommended": "Use KPI cards, patient trend, waiting-time ranking, and department comparison.",
    },
    "Strategy market-entry story": {
        "domain": "Regional Strategy",
        "context": "A strategy team is evaluating market-entry priorities across regions.",
        "question": "Which region balances market size, growth, competition, and current share most attractively?",
        "recommended": "Use a strategy bubble chart and a ranked attractiveness score.",
    },
}


def render_case_visual(domain: str) -> pd.DataFrame:
    df = get_dataset(domain)
    if domain == "Retail Sales":
        d = df.groupby("Region", as_index=False)["Sales"].sum()
        st.plotly_chart(ranked_bar(d, "Region", "Sales", "Regional sales ranking guides attention"), use_container_width=True)
    elif domain == "Marketing Campaign":
        fig = px.scatter(df, x="Spend", y="Revenue", size="Conversions", color="Channel", title="Campaign efficiency: spend versus revenue")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif domain == "Operations Delays":
        d = df.groupby("Plant", as_index=False)["Delay Days"].mean()
        st.plotly_chart(ranked_bar(d, "Plant", "Delay Days", "Plants ranked by average delay"), use_container_width=True)
    elif domain == "Financial Expenses":
        fig = px.bar(df, x="Department", y=["Budget", "Actual"], barmode="group", title="Budget versus actual expenditure")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif domain == "Healthcare Patient Flow":
        d = df.groupby("Department", as_index=False)["Avg Wait Time"].mean()
        st.plotly_chart(ranked_bar(d, "Department", "Avg Wait Time", "Departments ranked by waiting-time pressure"), use_container_width=True)
    elif domain == "Regional Strategy":
        fig = px.scatter(df, x="Market Size", y="Growth Rate", size="Market Share", color="Attractiveness", hover_name="Region", title="Market-entry strategy map")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    return df



def _num(x, decimals: int = 1) -> str:
    """Compact number formatter for classroom solution text."""
    try:
        if abs(float(x)) >= 1_000_000:
            return f"{float(x)/1_000_000:.{decimals}f}M"
        if abs(float(x)) >= 1_000:
            return f"{float(x)/1_000:.{decimals}f}K"
        return f"{float(x):.{decimals}f}"
    except Exception:
        return str(x)


def _domain_case_name(domain: str) -> Optional[str]:
    for name, meta in CASE_LIBRARY.items():
        if meta["domain"] == domain:
            return name
    return None


def case_model_solution(case_name: str, case: Dict[str, str], df: pd.DataFrame) -> Dict[str, str]:
    """Generate a data-grounded solution for each built-in case.

    The goal is not to create a perfect consulting answer; it is to give the
    instructor a ready classroom solution that students can compare against.
    """
    domain = case["domain"]
    if domain == "Retail Sales":
        reg = df.groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Satisfaction=("Satisfaction", "mean")).sort_values("Sales", ascending=False)
        cat = df.groupby("Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).sort_values("Sales", ascending=False)
        top_r, low_r = reg.iloc[0], reg.iloc[-1]
        top_c = cat.iloc[0]
        return {
            "Model interpretation": f"{top_r['Region']} is the strongest revenue region with total sales of {_num(top_r['Sales'],1)}, while {low_r['Region']} is the weakest region at {_num(low_r['Sales'],1)}. The leading category is {top_c['Category']}, so the story should focus on where growth is already strong and where diagnosis is needed.",
            "Evidence from the visual": f"Regional ranking places {top_r['Region']} first and {low_r['Region']} last; category aggregation shows {top_c['Category']} contributes the highest sales at {_num(top_c['Sales'],1)}.",
            "Recommended action": f"Protect and learn from the {top_r['Region']} playbook, then run a focused diagnostic for {low_r['Region']} covering stock availability, local demand, pricing, and store execution. Do not spread intervention equally across all regions.",
            "Possible limitation": "This built-in case does not include competitor activity, footfall, promotion timing, or local store capacity, so the recommendation should be framed as a first diagnostic priority rather than a final causal claim.",
            "Student answer template": f"Because {top_r['Region']} leads the sales ranking while {low_r['Region']} trails, management should prioritize a region-level diagnostic and replicate successful practices from the leading market after checking category mix and local context.",
        }
    if domain == "Marketing Campaign":
        d = df.copy()
        d["ROI"] = d["Revenue"] / d["Spend"]
        top_roi = d.sort_values("ROI", ascending=False).iloc[0]
        top_rev = d.sort_values("Revenue", ascending=False).iloc[0]
        low_roi = d.sort_values("ROI", ascending=True).iloc[0]
        return {
            "Model interpretation": f"{top_roi['Channel']} gives the strongest return on spend with ROI of {_num(top_roi['ROI'],2)}, while {top_rev['Channel']} generates the largest absolute revenue at {_num(top_rev['Revenue'],1)}. The managerial story should distinguish efficiency from scale.",
            "Evidence from the visual": f"The spend-versus-revenue scatter separates channels by both size and conversion performance. {low_roi['Channel']} has the weakest ROI at {_num(low_roi['ROI'],2)}, which makes it a candidate for review before further budget expansion.",
            "Recommended action": f"Shift incremental budget toward {top_roi['Channel']} if capacity allows, protect {top_rev['Channel']} if it remains strategically important, and audit {low_roi['Channel']} for targeting, creative quality, and conversion leakage.",
            "Possible limitation": "ROI should be checked with attribution window, customer lifetime value, channel saturation, and campaign objective. A high-ROI small channel may not scale indefinitely.",
            "Student answer template": f"Because {top_roi['Channel']} is most efficient but {top_rev['Channel']} is largest in revenue, management should separate scale decisions from efficiency decisions and reallocate only incremental budget after checking channel capacity.",
        }
    if domain == "Operations Delays":
        p = df.groupby("Plant", as_index=False).agg(avg_delay=("Delay Days", "mean"), avg_defect=("Defect Rate", "mean"), avg_output=("Output", "mean")).sort_values("avg_delay", ascending=False)
        high, low = p.iloc[0], p.iloc[-1]
        return {
            "Model interpretation": f"{high['Plant']} has the highest average delay at {_num(high['avg_delay'],1)} days and an average defect rate of {_num(high['avg_defect'],2)}. {low['Plant']} is the least delayed plant at {_num(low['avg_delay'],1)} days.",
            "Evidence from the visual": f"The plant delay ranking makes the operational hotspot visible; delay and defect indicators should be read together because late processes may also create quality pressure.",
            "Recommended action": f"Start with {high['Plant']} for root-cause analysis: capacity, supplier reliability, maintenance downtime, staffing, and rework loops. Use {low['Plant']} as an internal benchmark to identify transferable process practices.",
            "Possible limitation": "Average delay alone may hide weekly spikes, product-mix differences, and plant capacity differences. Confirm with trend charts before enforcing corrective targets.",
            "Student answer template": f"Because {high['Plant']} carries the highest delay pressure, operations should diagnose that plant first and compare its process conditions with the lowest-delay plant before generalizing the solution.",
        }
    if domain == "Financial Expenses":
        d = df.copy()
        d["Overspend"] = d["Actual"] - d["Budget"]
        over = d.sort_values("Overspend", ascending=False).iloc[0]
        best = d.sort_values("Overspend", ascending=True).iloc[0]
        over_count = int((d["Overspend"] > 0).sum())
        return {
            "Model interpretation": f"{over['Department']} shows the largest overspend at {_num(over['Overspend'],1)}, while {best['Department']} is the strongest budget saver with variance of {_num(best['Overspend'],1)}. {over_count} department(s) exceed budget in this scenario.",
            "Evidence from the visual": "The grouped budget-versus-actual chart shows which actual bars cross their budget bars; variance identifies the scale of the budget discipline issue.",
            "Recommended action": f"Ask {over['Department']} for a variance explanation and split the cause into controllable, strategic, and one-time items. Do not impose uniform cuts before understanding whether the overspend produced measurable value.",
            "Possible limitation": "Budget excess may be justified by growth, compliance, emergency procurement, or delayed accounting. The visual flags review priority, not automatic failure.",
            "Student answer template": f"Because {over['Department']} has the largest actual-over-budget gap, finance should request a variance note and decide whether the excess is corrective, strategic, or avoidable.",
        }
    if domain == "Healthcare Patient Flow":
        h = df.groupby("Department", as_index=False).agg(wait=("Avg Wait Time", "mean"), patients=("Patients", "sum"), occupancy=("Bed Occupancy", "mean"), readmit=("Readmission Rate", "mean")).sort_values("wait", ascending=False)
        high_wait = h.iloc[0]
        high_volume = h.sort_values("patients", ascending=False).iloc[0]
        return {
            "Model interpretation": f"{high_wait['Department']} has the highest average waiting-time pressure at {_num(high_wait['wait'],1)} minutes. {high_volume['Department']} handles the largest patient volume at {_num(high_volume['patients'],1)} patients, so pressure should be interpreted through both wait and volume.",
            "Evidence from the visual": "The wait-time ranking highlights where patients experience the longest delays; pairing it with volume and occupancy avoids overreacting to a small department with few cases.",
            "Recommended action": f"Prioritize a patient-flow review for {high_wait['Department']}, checking staffing windows, triage, appointment batching, and downstream capacity. Track whether interventions reduce wait without increasing readmission or safety risk.",
            "Possible limitation": "Healthcare dashboards need denominators, acuity, case mix, and safety indicators. Do not rank departments without considering patient severity and service complexity.",
            "Student answer template": f"Because {high_wait['Department']} shows the highest wait-time pressure, the hospital should diagnose patient-flow constraints there while checking volume, acuity, and safety outcomes before changing staffing.",
        }
    if domain == "Regional Strategy":
        r = df.sort_values("Attractiveness", ascending=False)
        top, second, low = r.iloc[0], r.iloc[1], r.iloc[-1]
        return {
            "Model interpretation": f"{top['Region']} has the highest attractiveness score at {_num(top['Attractiveness'],1)}, followed by {second['Region']} at {_num(second['Attractiveness'],1)}. {low['Region']} appears least attractive in this synthetic scenario.",
            "Evidence from the visual": f"The strategy map combines market size, growth, share, competition, and attractiveness, showing that market-entry priority should not be based on size alone.",
            "Recommended action": f"Shortlist {top['Region']} for deeper market-entry evaluation, then compare it with {second['Region']} using qualitative factors such as regulatory fit, channel access, partner availability, and implementation cost.",
            "Possible limitation": "The attractiveness score is an illustrative composite. Before final strategy, validate the scoring weights, market assumptions, competitive intensity, and organizational capabilities.",
            "Student answer template": f"Because {top['Region']} balances attractiveness indicators better than other regions, strategy should prioritize it for due diligence while validating assumptions beyond the chart.",
        }
    story = auto_story_from_dataframe(df, "managerial audience", case["question"])
    return {
        "Model interpretation": story["Possible pattern"],
        "Evidence from the visual": story["Suggested visual"],
        "Recommended action": story["Managerial implication"],
        "Possible limitation": story["Caution"],
        "Student answer template": "State the visible pattern, identify the evidence, explain managerial meaning, and recommend a cautious next step.",
    }


def render_case_solution(case_name: str, case: Dict[str, str], df: pd.DataFrame, expanded: bool = True) -> None:
    sol = case_model_solution(case_name, case, df)
    st.markdown("### ✅ Complete solution for this case")
    callout("Model answer", sol["Model interpretation"], "insight")
    with st.expander("Step-by-step solution, evidence, recommendation, and teaching notes", expanded=expanded):
        c1, c2 = st.columns(2)
        with c1:
            callout("Evidence to cite", sol["Evidence from the visual"], "purple")
            callout("Recommended action", sol["Recommended action"], "warning")
        with c2:
            callout("Limitation to mention", sol["Possible limitation"], "danger")
            callout("Expected student answer", sol["Student answer template"], "insight")
        st.markdown("**How to use this in class**")
        st.markdown("- First ask students for the visible pattern before showing the model answer.")
        st.markdown("- Then ask them to separate observation, insight, recommendation, and limitation.")
        st.markdown("- Finally compare their answer with the model solution and improve one sentence.")
    solution_text = "\n\n".join([f"{k}:\n{v}" for k, v in sol.items()])
    st.download_button("Download case solution", solution_text, file_name=f"{case_name.lower().replace(' ', '_')}_solution.txt", mime="text/plain", key=f"case_solution_{case_name}")


def activity_model_solution(activity: Dict[str, str]) -> str:
    session_no = int(activity["Session"])
    sess = next((s for s in SESSIONS if s.no == session_no), None)
    takeaway = sess.takeaway if sess else "connect visual evidence to action"
    return (
        f"A strong response should contain four parts: (1) a visible pattern from the chart, "
        f"(2) the evidence that supports it, (3) the managerial meaning, and (4) a cautious action. "
        f"For this activity, a model answer should end with the idea: {takeaway} "
        f"Avoid unsupported claims, decorative comments, and recommendations that do not follow from the visual evidence."
    )



def session_support_pack(sess: SessionInfo) -> Dict[str, str]:
    pack = {
        1: {
            "Worked example": "A regional sales review is easier to teach with a sorted bar chart that shows West and South leading performance while Central lags. The teaching message is that the chart aligns attention before discussion begins.",
            "Right way": "Open with the business question, show one clean ranked visual, state the key pattern, and end with a specific managerial next step.",
            "Wrong way": "Show a dense table first, read values aloud, and assume students will discover the message by themselves.",
            "Misinterpretation": "Students may think the visual itself creates insight automatically.",
            "Clarification": "Clarify that the visual supports insight, but the presenter still has to explain why the pattern matters for action.",
            "Solved mini-lab": "Model solution: 'West leads sales while Central lags. The immediate managerial move is to diagnose Central before reallocating more budget, while also protecting the practices that keep West ahead.'",
        },
        2: {
            "Worked example": "Use the same dataset to ask three questions: which region is highest, how did revenue change, and is discount associated with sales? Then show bar, line, and scatter choices side by side.",
            "Right way": "Select visuals from the business question, not from software habit. Comparison → bars, trend → lines, relationship → scatter, composition → stacked views.",
            "Wrong way": "Choose the visual that looks attractive before clarifying the analytical task.",
            "Misinterpretation": "Students may believe one chart type is universally best.",
            "Clarification": "Clarify that no chart is best in general; it is best only in relation to the question and audience.",
            "Solved mini-lab": "Model solution: 'For ranking products I would use a sorted bar chart, because the decision task is comparison and not trend or relationship.'",
        },
        3: {
            "Worked example": "Show the same bar chart with a truncated axis and then with a zero baseline. Ask which version makes the difference look like a crisis.",
            "Right way": "Explain how scale affects perceived magnitude and use a fair axis when the chart relies on bar length for comparison.",
            "Wrong way": "Use a compressed or truncated axis without warning, especially when the audience may read the visual quickly.",
            "Misinterpretation": "Students may say 'the numbers are correct, so the chart is fine.'",
            "Clarification": "Clarify that a technically correct chart can still communicate unfairly if the framing exaggerates or minimizes the pattern.",
            "Solved mini-lab": "Model solution: 'The original visual exaggerates the performance gap because the bar baseline is truncated. Restoring the axis shows that the gap is real but modest.'",
        },
        10: {
            "Worked example": "Show monthly revenue with a campaign marker. Ask students to identify the pre-campaign trend, the post-campaign shift, and whether the change looks temporary or sustained.",
            "Right way": "Separate trend, seasonality, turning points, and events. Narrate what changed, when it changed, and what evidence is strong versus tentative.",
            "Wrong way": "Claim the campaign caused the increase without considering seasonality or prior momentum.",
            "Misinterpretation": "Students may jump from sequence to causation.",
            "Clarification": "Clarify that time ordering supports a hypothesis, but it does not prove causality by itself.",
            "Solved mini-lab": "Model solution: 'Revenue increased after the campaign marker, but we should verify whether similar seasonal uplift appears in earlier periods before attributing the change fully to the campaign.'",
        },
        11: {
            "Worked example": "Begin with one dashboard question: 'Are we on track?' Then show KPI cards, one diagnostic chart, one supporting chart, and a written action note.",
            "Right way": "Give the dashboard hierarchy: orient, diagnose, and then decide. The executive should know within seconds where attention is needed.",
            "Wrong way": "Treat the dashboard as a gallery of unrelated charts.",
            "Misinterpretation": "Students may think more visuals always mean more insight.",
            "Clarification": "Clarify that weak hierarchy increases cognitive load and can reduce the chance of good action.",
            "Solved mini-lab": "Model solution: 'Place KPI cards first, then one ranked issue chart, then one explanatory chart. The dashboard should end with a short action note that names the priority decision.'",
        },
        12: {
            "Worked example": "Take the title 'Monthly Revenue' and rewrite it into 'Revenue recovered after April campaign, led by South region.' Then add one annotation at the turning point.",
            "Right way": "Use titles to tell the audience what the visual means, and annotations to mark the evidence that supports the claim.",
            "Wrong way": "Leave the audience with variable names and expect them to infer the story alone.",
            "Misinterpretation": "Students may over-explain the chart through paragraphs or under-explain it with generic labels.",
            "Clarification": "Clarify that the best titles and annotations are concise, evidence-linked, and decision-oriented.",
            "Solved mini-lab": "Model solution: 'Analytical title: Revenue improved after April. Action title: Continue the campaign in South, but review Central response before expanding budget.'",
        },
        15: {
            "Worked example": "Students often collect too many charts. Demonstrate how to keep only the context chart, the diagnosis chart, and the recommendation chart.",
            "Right way": "Build a story arc: business question → evidence → insight → implication → recommendation → limitation.",
            "Wrong way": "Present every chart created during analysis and hope the audience connects them.",
            "Misinterpretation": "Students may think completeness means showing everything.",
            "Clarification": "Clarify that storytelling is selective; it prioritizes the visuals that move the audience toward action.",
            "Solved mini-lab": "Model solution: 'The final story should show only the visuals that answer the business question directly. Every retained chart must have a speaking role in the decision narrative.'",
        },
        16: {
            "Worked example": "Use a hospital dashboard that combines wait time, patient volume, occupancy, and readmission. Ask students which department deserves review first and what extra context is needed.",
            "Right way": "Narrate healthcare visuals with caution, context, and ethics. Pair performance with volume and safety, not just ranking.",
            "Wrong way": "Rank departments on one metric alone and recommend staffing changes immediately.",
            "Misinterpretation": "Students may confuse a high wait time with poor clinical quality in every case.",
            "Clarification": "Clarify that healthcare visuals require case-mix, acuity, safety, and service-complexity context before action.",
            "Solved mini-lab": "Model solution: 'Emergency has the highest wait pressure, but the recommendation should be a patient-flow review that also considers acuity, occupancy, and safety before any staffing decision.'",
        },
    }
    generic = {
        "Worked example": f"Use a short business scene to explain '{sess.title}', then show one visual, ask what pattern is visible, and convert that pattern into a managerial action.",
        "Right way": f"Teach {sess.title} by connecting the business question, the visual evidence, and the action implication in sequence.",
        "Wrong way": "Explain the chart mechanically without telling students why a manager should care.",
        "Misinterpretation": "Students may confuse observation with recommendation or treat the first visible pattern as complete proof.",
        "Clarification": f"Clarify that the session takeaway is: {sess.takeaway}",
        "Solved mini-lab": f"Model solution: start with the visible pattern, cite the evidence, explain the managerial meaning, and end with a cautious recommendation that reflects this session takeaway: {sess.takeaway}",
    }
    out = dict(generic)
    out.update(pack.get(sess.no, {}))
    out["Story narrative"] = f"Start with context, introduce the visual evidence, state the visible pattern, translate it into business meaning, and end with an action. For this session, end with: {sess.takeaway}"
    out["Instructor hint"] = "If students get stuck, ask them three prompts in order: What do you see? Why does it matter? What should management do next?"
    return out


def render_session_support_pack(sess: SessionInfo) -> None:
    pack = session_support_pack(sess)
    c1, c2 = st.columns(2)
    with c1:
        callout("Worked example", pack["Worked example"], "purple")
        callout("Right way to teach it", pack["Right way"], "insight")
        callout("Likely misinterpretation", pack["Misinterpretation"], "danger")
        callout("Instructor hint", pack["Instructor hint"], "warning")
    with c2:
        callout("Story narrative", pack["Story narrative"], "insight")
        callout("Wrong way", pack["Wrong way"], "danger")
        callout("Clarification", pack["Clarification"], "purple")
        callout("Solved mini-lab", pack["Solved mini-lab"], "warning")
    safe_dataframe(pd.DataFrame([
        {"Teaching element": "Worked example", "Use it for": "Opening explanation", "What to say": pack["Worked example"]},
        {"Teaching element": "Right way", "Use it for": "Best-practice framing", "What to say": pack["Right way"]},
        {"Teaching element": "Misinterpretation", "Use it for": "Preventing error", "What to say": pack["Misinterpretation"]},
        {"Teaching element": "Clarification", "Use it for": "Corrective explanation", "What to say": pack["Clarification"]},
    ]), max_rows=4)


def mini_lab_solution_text(sess: SessionInfo) -> str:
    pack = session_support_pack(sess)
    return pack["Solved mini-lab"] + " Also ensure the answer distinguishes observation, insight, recommendation, and limitation."


def case_teaching_cautions(case_name: str, case: Dict[str, str], sol: Dict[str, str]) -> Dict[str, str]:
    domain = case.get("domain", "")
    wrong = "Use the most dramatic visible difference to justify a strong recommendation immediately."
    clarification = "A business visual should first prioritize diagnosis, then support action with evidence and caution."
    misread = "The highest or lowest point automatically tells the full story."
    if domain == "Marketing Campaign":
        wrong = "Move all budget to the highest-revenue channel without checking efficiency, scale limits, or attribution logic."
        misread = "Highest revenue means best channel in every sense."
        clarification = "Clarify the difference between scale and efficiency. A channel can lead revenue but still be less efficient than a smaller channel."
    elif domain == "Operations Delays":
        wrong = "Blame the slowest plant immediately without checking product mix, downtime, or capacity context."
        misread = "Average delay alone proves the root cause."
        clarification = "Clarify that delay rankings identify where to investigate first, not why the issue exists."
    elif domain == "Healthcare Patient Flow":
        wrong = "Treat the highest wait department as poor quality and cut staff elsewhere to fix it quickly."
        misread = "Higher waiting time always means poorer care."
        clarification = "Clarify that wait pressure must be interpreted with acuity, patient volume, and safety indicators before action."
    elif domain == "Regional Strategy":
        wrong = "Choose the largest market without looking at competition, share, or implementation difficulty."
        misread = "Largest market equals best opportunity."
        clarification = "Clarify that strategy visuals reveal trade-offs, not one-dimensional answers."
    return {
        "Wrong way": wrong,
        "Misinterpretation": misread,
        "Clarification": clarification,
        "Teaching note": f"Ask students to compare their first instinct with the full solution. The model answer should separate visible evidence, recommended action, and limitation: {sol['Possible limitation']}",
    }


def render_domain_model_solution(domain: str, df: pd.DataFrame, expanded: bool = False) -> None:
    case_name = _domain_case_name(domain)
    if case_name:
        render_case_solution(case_name, CASE_LIBRARY[case_name], df, expanded=expanded)
    else:
        story = auto_story_from_dataframe(df, "managerial audience", "What is the most important visual pattern?")
        callout("Model solution", story["Possible pattern"], "insight")
        callout("Recommended action", story["Managerial implication"], "warning")
        callout("Limitation", story["Caution"], "danger")


def page_case_library() -> None:
    hero("Business Case Library", "Use built-in cases to practice visual storytelling across business and healthcare domains, with full solutions, right-versus-wrong interpretation, and clarification notes.", ["Cases", "Datasets", "Solutions"])
    case_name = st.selectbox("Choose case", list(CASE_LIBRARY.keys()))
    case = CASE_LIBRARY[case_name]
    c1, c2 = st.columns([1, 1])
    with c1:
        callout("Business context", case["context"], "purple")
    with c2:
        callout("Decision question", case["question"], "insight")
    df = render_case_visual(case["domain"])
    callout("Recommended visual story", case["recommended"], "warning")
    render_case_solution(case_name, case, df, expanded=True)
    with st.expander("Guided questions for classroom discussion", expanded=True):
        st.markdown("- What pattern is most visible?")
        st.markdown("- What might a manager misinterpret?")
        st.markdown("- What extra context is needed before action?")
        st.markdown("- What recommendation is justified by the visual evidence?")
    st.markdown("### Role-play prompts for this case")
    role_prompts = {
        "CEO": "What strategic decision does this evidence support?",
        "Finance Controller": "What cost, risk, or budget implication should be checked?",
        "Operations Head": "What process should be improved first?",
        "Marketing Head": "Which segment, channel, or customer action follows from this pattern?",
        "Data Analyst": "What evidence supports the claim and what limitation should be stated?",
    }
    for role, prompt in role_prompts.items():
        st.markdown(f"<div class='role-card'><b>{html.escape(role)}</b><br>{html.escape(prompt)}</div>", unsafe_allow_html=True)
    st.download_button("Download case dataset", to_csv_bytes(df), file_name=f"{case_name.lower().replace(' ', '_')}.csv", mime="text/csv")


def page_quiz_zone() -> None:
    hero("Quiz Zone", "Use the quiz bank for concept checks, scenario discussion, and revision across all 16 sessions.", [f"{len(QUIZ_BANK)} Questions", "Reveal Answers", "CLO Tagged"])
    c1, c2, c3 = st.columns(3)
    with c1:
        session_filter = st.selectbox("Session filter", ["All"] + [str(i) for i in range(1, 17)])
    with c2:
        clo_filter = st.selectbox("CLO filter", ["All"] + sorted(set(q["clo"] for q in QUIZ_BANK)))
    with c3:
        limit = st.slider("Number of questions", 5, len(QUIZ_BANK), 12)
    qs = QUIZ_BANK
    if session_filter != "All":
        qs = [q for q in qs if q["session"] == session_filter]
    if clo_filter != "All":
        qs = [q for q in qs if q["clo"] == clo_filter]
    st.write(f"Showing {min(limit, len(qs))} of {len(qs)} matching questions.")
    for i, q in enumerate(qs[:limit], start=1):
        render_quiz_card(i, q, show_tags=True)
        with st.expander("Reveal answer"):
            st.write(f"**Correct answer:** {q['answer']}")
            st.write(q["explanation"])


def page_final_workshop() -> None:
    hero("Final Integrated Workshop", "Build a complete visual story from dataset selection to recommendation and export the summary.", ["CLO1–CLO4", "End-to-End", "Export"])
    process_diagram(["Problem", "Dataset", "Chart", "Insight", "Recommendation"])
    c1, c2 = st.columns(2)
    with c1:
        domain = st.selectbox("Select dataset", DATASET_OPTIONS)
        problem = st.text_area("Business problem", value="Management needs to identify the most important performance issue and decide where to act first.")
        chart_choice = st.selectbox("Primary visual", ["Ranked comparison", "Trend", "Distribution", "Relationship", "Composition", "Dashboard"])
    with c2:
        audience = st.selectbox("Audience", ["Executive committee", "Functional manager", "Healthcare administrator", "Analyst team", "Student presentation panel"])
        insight = st.text_area("Key insight", value="The visual evidence suggests one clear priority area that requires focused managerial attention.")
        recommendation = st.text_area("Recommendation", value="Prioritize a short diagnostic review and implement targeted corrective action based on the top driver.")
    df = get_dataset(domain)
    st.subheader("Dataset Preview")
    safe_dataframe(df, max_rows=15)
    st.subheader("Generated Visual")
    if chart_choice == "Dashboard":
        if domain in ["Retail Sales", "Marketing Campaign", "Financial Expenses", "Healthcare Patient Flow"]:
            render_dashboard_demo(domain)
        else:
            render_case_visual(domain)
    elif chart_choice == "Trend":
        if "Month" in df.columns:
            numeric = df.select_dtypes(include=np.number).columns.tolist()
            y = st.selectbox("Trend metric", numeric)
            fig = px.line(df.groupby("Month", as_index=False)[y].sum(), x="Month", y=y, markers=True, title=f"Trend story for {y}")
            fig.update_layout(height=430, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
        elif "Date" in df.columns:
            numeric = df.select_dtypes(include=np.number).columns.tolist()
            y = st.selectbox("Trend metric", numeric)
            fig = px.line(df.groupby("Date", as_index=False)[y].sum(), x="Date", y=y, title=f"Trend story for {y}")
            fig.update_layout(height=430, title_x=.02)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("This dataset does not have a time field; showing case visual instead.")
            render_case_visual(domain)
    elif chart_choice == "Distribution":
        numeric = df.select_dtypes(include=np.number).columns.tolist()
        y = st.selectbox("Distribution metric", numeric)
        fig = px.histogram(df, x=y, nbins=24, title=f"Distribution of {y}")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_choice == "Relationship":
        numeric = df.select_dtypes(include=np.number).columns.tolist()
        x = st.selectbox("X", numeric, index=0)
        y = st.selectbox("Y", numeric, index=min(1, len(numeric)-1))
        fig = px.scatter(df, x=x, y=y, title=f"Relationship between {x} and {y}")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_choice == "Composition":
        cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
        numeric = df.select_dtypes(include=np.number).columns.tolist()
        if cat_cols and numeric:
            cat = st.selectbox("Category", cat_cols)
            val = st.selectbox("Value", numeric)
            d = df.groupby(cat, as_index=False)[val].sum()
            st.plotly_chart(ranked_bar(d, cat, val, f"Contribution of {cat} to {val}"), use_container_width=True)
        else:
            render_case_visual(domain)
    else:
        render_case_visual(domain)
    summary = f"""
# Final Visual Story Summary

**Dataset:** {domain}

**Audience:** {audience}

**Business Problem:** {problem}

**Primary Visual:** {chart_choice}

**Key Insight:** {insight}

**Recommendation:** {recommendation}

**Suggested Presentation Flow:**
1. Start with business context.
2. Show the primary visual and explain the visible pattern.
3. State the managerial implication.
4. Present the recommendation.
5. Mention one limitation or additional data need.
""".strip()
    st.subheader("Capstone checklist")
    capstone_checks = {
        "Business question is clear": st.checkbox("Business question is clear", key="cap_q"),
        "Audience is specified": st.checkbox("Audience is specified", key="cap_a"),
        "Chart choice matches the question": st.checkbox("Chart choice matches the question", key="cap_c"),
        "Insight is evidence-based": st.checkbox("Insight is evidence-based", key="cap_i"),
        "Recommendation is specific": st.checkbox("Recommendation is specific", key="cap_r"),
        "Limitation is acknowledged": st.checkbox("Limitation is acknowledged", key="cap_l"),
    }
    completed = sum(capstone_checks.values())
    st.progress(completed / len(capstone_checks))
    callout("Rubric reminder", "A strong final story is not a collection of charts. It is a decision narrative: context, evidence, insight, implication, recommendation, and limitation.", "purple")
    with st.expander("Show model solution for this selected dataset", expanded=True):
        render_domain_model_solution(domain, df, expanded=False)

    st.subheader("Exportable Story Summary")
    st.markdown(summary)
    st.download_button("Download final workshop summary", summary, file_name="final_visual_story_summary.md", mime="text/markdown")


def render_gallery_chart(chart_name: str) -> None:
    """Render a safe, self-contained example for each chart in the gallery."""
    if chart_name == "Ranked Bar":
        d = retail_data().groupby("Region", as_index=False)["Sales"].sum()
        st.plotly_chart(ranked_bar(d, "Region", "Sales", "Regional ranking shows where sales momentum is strongest"), use_container_width=True)
    elif chart_name == "Dot Plot":
        d = retail_data().groupby("Category", as_index=False)["Profit"].sum().sort_values("Profit")
        fig = go.Figure(go.Scatter(x=d["Profit"], y=d["Category"], mode="markers+text", text=d["Profit"], textposition="middle right", marker=dict(size=16)))
        fig.update_layout(title="Dot plot: category profit comparison with low visual clutter", height=430, title_x=.02, xaxis_title="Profit", yaxis_title="Category")
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Heatmap":
        h = retail_data().pivot_table(index="Region", columns="Category", values="Sales", aggfunc="sum")
        fig = px.imshow(h, aspect="auto", title="Heatmap: region-category pockets of sales strength")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Histogram":
        d = healthcare_data()
        fig = px.histogram(d, x="Avg Wait Time", nbins=26, title="Histogram: waiting-time spread shows service consistency risk")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Box Plot":
        d = healthcare_data()
        fig = px.box(d, x="Department", y="Avg Wait Time", points="outliers", title="Box plot: department-level waiting-time variation")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Scatter Plot":
        d = retail_data()
        fig = px.scatter(d, x="Discount", y="Sales", color="Category", size="Profit", title="Scatter plot: discount-sales association differs by category")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Bubble Chart":
        d = regional_data()
        fig = px.scatter(d, x="Market Size", y="Growth Rate", size="Market Share", color="Attractiveness", hover_name="Region", title="Bubble chart: strategic attractiveness across regions")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Line Chart":
        d = time_series_revenue()
        fig = px.line(d, x="Month", y=["Revenue", "Cost"], markers=True, title="Line chart: revenue improves faster than cost after the campaign period")
        add_vertical_marker(fig, pd.Timestamp("2024-11-01"), "Campaign begins")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Area Chart":
        d = retail_data().groupby(["Month", "Category"], as_index=False)["Sales"].sum()
        fig = px.area(d, x="Month", y="Sales", color="Category", title="Area chart: category contribution to monthly sales volume")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Stacked Bar":
        d = retail_data().groupby(["Region", "Category"], as_index=False)["Sales"].sum()
        fig = px.bar(d, x="Region", y="Sales", color="Category", title="Stacked bar: category mix within each region")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "100% Stacked Bar":
        d = retail_data().groupby(["Region", "Category"], as_index=False)["Sales"].sum()
        totals = d.groupby("Region")["Sales"].transform("sum")
        d["Share"] = d["Sales"] / totals * 100
        fig = px.bar(d, x="Region", y="Share", color="Category", title="100% stacked bar: proportional category mix by region")
        fig.update_layout(height=430, title_x=.02, yaxis_title="Share (%)")
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Treemap":
        d = retail_data().groupby(["Region", "Category"], as_index=False)["Sales"].sum()
        fig = px.treemap(d, path=["Region", "Category"], values="Sales", title="Treemap: sales contribution by region and category")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Waterfall":
        d = finance_data()
        start = int(d["Budget"].sum())
        changes = d["Variance"].astype(int).tolist()
        labels = ["Total Budget"] + d["Department"].tolist() + ["Net Position"]
        values = [start] + changes + [sum(changes)]
        measures = ["absolute"] + ["relative"] * len(changes) + ["total"]
        fig = go.Figure(go.Waterfall(name="Budget bridge", orientation="v", measure=measures, x=labels, y=values))
        fig.update_layout(title="Waterfall: department variances explain the budget bridge", height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Funnel":
        d = marketing_data()
        stages = pd.DataFrame({"Stage": ["Impressions", "Clicks", "Conversions"], "Value": [int(d["Impressions"].sum()), int(d["Clicks"].sum()), int(d["Conversions"].sum())]})
        fig = go.Figure(go.Funnel(y=stages["Stage"], x=stages["Value"], textinfo="value+percent previous"))
        fig.update_layout(title="Funnel: conversion drop-off across marketing stages", height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Slope Chart":
        d = retail_data()
        first_last = d[d["Month"].isin([d["Month"].min(), d["Month"].max()])].groupby(["Month", "Category"], as_index=False)["Sales"].sum()
        fig = px.line(first_last, x="Month", y="Sales", color="Category", markers=True, title="Slope chart: category change from first to last month")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Violin Plot":
        d = healthcare_data()
        fig = px.violin(d, x="Department", y="Avg Wait Time", box=True, points="outliers", title="Violin plot: shape of waiting-time variation by department")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Strip Plot":
        d = customer_data()
        fig = px.strip(d, x="Segment", y="Satisfaction", color="Segment", title="Strip plot: individual customer satisfaction cases by segment")
        fig.update_layout(height=430, title_x=.02, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Pareto Chart":
        d = retail_data().groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
        d["CumShare"] = d["Sales"].cumsum() / d["Sales"].sum() * 100
        fig = go.Figure()
        fig.add_bar(x=d["Category"], y=d["Sales"], name="Sales")
        fig.add_trace(go.Scatter(x=d["Category"], y=d["CumShare"], name="Cumulative share", yaxis="y2", mode="lines+markers"))
        fig.update_layout(title="Pareto chart: few categories explain most sales", height=430, title_x=.02, yaxis_title="Sales", yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105]))
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Radar Chart":
        d = regional_data().copy()
        metrics = ["Market Size", "Growth Rate", "Market Share", "Competition"]
        row = d.iloc[0]
        values = []
        for m in metrics:
            col = d[m]
            values.append(float((row[m] - col.min()) / (col.max() - col.min()) * 100))
        fig = go.Figure(data=go.Scatterpolar(r=values + [values[0]], theta=metrics + [metrics[0]], fill="toself", name=row["Region"]))
        fig.update_layout(title=f"Radar chart: multi-metric profile for {row['Region']}", height=430, title_x=.02, polar=dict(radialaxis=dict(visible=True, range=[0,100])))
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Gantt Timeline":
        d = pd.DataFrame({"Task": ["Frame question", "Prepare data", "Build visuals", "Write story", "Present"], "Start": pd.to_datetime(["2026-07-01", "2026-07-03", "2026-07-07", "2026-07-10", "2026-07-14"]), "Finish": pd.to_datetime(["2026-07-03", "2026-07-08", "2026-07-11", "2026-07-14", "2026-07-15"]), "Owner": ["Team", "Analyst", "Analyst", "Presenter", "Team"]})
        fig = px.timeline(d, x_start="Start", x_end="Finish", y="Task", color="Owner", title="Gantt timeline: visual-story project flow")
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Calendar Heatmap":
        d = time_series_revenue().copy()
        d["Week"] = d["Month"].dt.isocalendar().week.astype(int)
        d["MonthName"] = d["Month"].dt.strftime("%b")
        p = d.pivot_table(index="MonthName", columns="Week", values="Revenue", aggfunc="sum")
        fig = px.imshow(p, aspect="auto", title="Calendar heatmap: monthly intensity pattern across weeks")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Sankey Diagram":
        fig = go.Figure(data=[go.Sankey(node=dict(label=["Visitors", "Clicks", "No Click", "Trials", "No Trial", "Conversions"]), link=dict(source=[0,0,1,1,3], target=[1,2,3,4,5], value=[4200,5800,900,3300,260]))])
        fig.update_layout(title="Sankey diagram: marketing flow from visitors to conversions", height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Sunburst Chart":
        d = retail_data().groupby(["Region", "Category"], as_index=False)["Sales"].sum()
        fig = px.sunburst(d, path=["Region", "Category"], values="Sales", title="Sunburst chart: sales hierarchy by region and category")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Geo Bubble Map":
        d = pd.DataFrame({"City": ["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai", "Goa"], "lat": [28.61, 19.07, 12.97, 22.57, 13.08, 15.49], "lon": [77.20, 72.88, 77.59, 88.36, 80.27, 73.82], "Value": [90, 115, 100, 72, 84, 45]})
        fig = px.scatter_geo(d, lat="lat", lon="lon", size="Value", hover_name="City", text="City", title="Geo bubble map: regional demand hotspots")
        fig.update_geos(scope="asia", projection_type="natural earth")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Small Multiples":
        d = retail_data().groupby(["Month", "Category"], as_index=False)["Sales"].sum()
        fig = px.line(d, x="Month", y="Sales", facet_col="Category", facet_col_wrap=2, markers=True, title="Small multiples: category trends on comparable panels")
        fig.update_layout(height=520, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Bullet Chart":
        fig = go.Figure(go.Indicator(mode="number+gauge+delta", value=78, delta={"reference": 85}, title={"text": "Service Level vs Target"}, gauge={"shape": "bullet", "axis": {"range": [0, 100]}, "threshold": {"value": 85}}))
        fig.update_layout(height=260, title="Bullet chart: compact actual-versus-target story", title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Control Chart":
        d = operations_data().groupby("Date", as_index=False)["Delay Days"].mean().sort_values("Date")
        mean = d["Delay Days"].mean(); std = d["Delay Days"].std()
        fig = px.line(d, x="Date", y="Delay Days", markers=True, title="Control chart: average delay stability over time")
        for val, label in [(mean, "Mean"), (mean + 2*std, "Upper watch"), (max(mean - 2*std, 0), "Lower watch")]:
            fig.add_hline(y=val, annotation_text=label, line_dash="dash")
        fig.update_layout(height=430, title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Dumbbell Chart":
        d = retail_data()
        p = d[d["Month"].isin([d["Month"].min(), d["Month"].max()])].groupby(["Category", "Month"], as_index=False)["Sales"].sum()
        wide = p.pivot(index="Category", columns="Month", values="Sales").reset_index()
        first, last = wide.columns[1], wide.columns[2]
        fig = go.Figure()
        for _, row in wide.iterrows():
            fig.add_trace(go.Scatter(x=[row[first], row[last]], y=[row["Category"], row["Category"]], mode="lines+markers", showlegend=False))
        fig.update_layout(title="Dumbbell chart: before-after sales change by category", height=430, title_x=.02, xaxis_title="Sales")
        st.plotly_chart(fig, use_container_width=True)
    elif chart_name == "Gauge Indicator":
        fig = go.Figure(go.Indicator(mode="gauge+number+delta", value=82, delta={"reference": 90}, title={"text": "Customer Satisfaction"}, gauge={"axis": {"range": [0, 100]}, "threshold": {"value": 90}}))
        fig.update_layout(height=360, title="Gauge indicator: one headline KPI against target", title_x=.02)
        st.plotly_chart(fig, use_container_width=True)
    else:
        render_dashboard_demo("Retail Sales")


def page_visual_gallery() -> None:
    hero("Visualization Master Gallery", "A one-stop chart encyclopedia with live examples, storytelling use-cases, cautions, and classroom prompts.", [f"{len(CHART_GALLERY)} Visuals", "When to Use", "Story Prompts"])
    c1, c2 = st.columns([.9, 1.4])
    with c1:
        families = ["All"] + sorted(set(item["family"] for item in CHART_GALLERY))
        family = st.selectbox("Filter by visual family", families)
        visible = [item for item in CHART_GALLERY if family == "All" or item["family"] == family]
        names = [item["name"] for item in visible]
        chart_name = st.selectbox("Choose visual", names)
        meta = next(item for item in CHART_GALLERY if item["name"] == chart_name)
        callout("When to use", meta["use"], "insight")
        callout("When to avoid", meta["avoid"], "warning")
        callout("Story question", meta["story"], "purple")
    with c2:
        render_gallery_chart(chart_name)
    st.subheader("From chart to story")
    process_diagram(["Business Question", "Chart Choice", "Visible Pattern", "Interpretation", "Recommendation"])
    st.markdown("#### Quick teaching guide")
    st.write(f"Use the {chart_name} to ask students: What do you see first? What might be misleading? What decision could this support? What extra context is needed before action?")


def page_activity_bank() -> None:
    hero("Activity Bank", "Ready-to-use classroom activities for every session, each with instructions, expected output, debrief question, and model solution so the app can function as a full teaching companion.", [f"{len(ACTIVITY_BANK)} Activities", "Session-wise", "Solved"])
    c1, c2, c3 = st.columns(3)
    with c1:
        session_filter = st.selectbox("Session", ["All"] + [str(i) for i in range(1, 17)], key="activity_session_filter")
    with c2:
        module_filter = st.selectbox("Module", ["All"] + sorted(set(a["Module"] for a in ACTIVITY_BANK)), key="activity_module_filter")
    with c3:
        time_filter = st.selectbox("Time", ["All"] + sorted(set(a["Estimated Time"] for a in ACTIVITY_BANK)), key="activity_time_filter")
    activities = ACTIVITY_BANK
    if session_filter != "All":
        activities = [a for a in activities if a["Session"] == session_filter]
    if module_filter != "All":
        activities = [a for a in activities if a["Module"] == module_filter]
    if time_filter != "All":
        activities = [a for a in activities if a["Estimated Time"] == time_filter]
    st.write(f"Showing {len(activities)} matching activities.")
    for idx, a in enumerate(activities[:24], start=1):
        with st.expander(f"{idx}. {a['Activity']}  —  {a['Estimated Time']}"):
            st.markdown(f"<span class='tag'>Session {a['Session']}</span><span class='tag'>{a['Module']}</span><span class='tag'>{a['CLOs']}</span>", unsafe_allow_html=True)
            st.write(a["Instruction"])
            st.write(f"**Student output:** {a['Student Output']}")
            st.write(f"**Debrief question:** {a['Debrief Question']}")
            callout("Model solution / expected response", activity_model_solution(a), "insight")
    export = pd.DataFrame(activities)
    st.download_button("Download filtered activity bank as CSV", to_csv_bytes(export), file_name="storytelling_activity_bank.csv", mime="text/csv")



def page_resources() -> None:
    hero("Resources and Tool Guide", "A practical guide to no-cost or accessible visualization tools for independent practice.", ["No-cost tools", "Practice", "Self-study"])
    tools = [
        ("Tableau Public", "Useful for dashboards and interactive visual exploration. Best for publishing public projects and learning dashboard design."),
        ("Flourish", "Useful for interactive and animated data stories. Best for quick public-facing visual narratives."),
        ("Datawrapper", "Useful for clean charts, maps, and tables. Strong for journalistic and public communication."),
        ("RAWGraphs", "Useful for converting tabular data into less common visual forms. Good for experimentation."),
        ("Google Sheets / Excel", "Useful for quick charting, data cleaning, pivot tables, and classroom exercises."),
        ("Power BI", "Useful for business dashboards, KPI tracking, and management reporting."),
    ]
    cols = st.columns(2)
    for i, (name, desc) in enumerate(tools):
        with cols[i % 2]:
            card(name, desc, ["Optional practice", "No API needed"])
    st.subheader("Practice datasets inside this app")
    choice = st.selectbox("Choose dataset to preview/download", DATASET_OPTIONS)
    df = get_dataset(choice)
    safe_dataframe(df, max_rows=25)
    st.download_button("Download selected dataset", to_csv_bytes(df), file_name=f"{choice.lower().replace(' ', '_')}.csv", mime="text/csv")
    callout("Usage note", "The course can be fully taught inside this app. External tools are optional practice environments for students who want to recreate or extend the visuals.", "insight")


# -----------------------------------------------------------------------------
# Main app
# -----------------------------------------------------------------------------
def main() -> None:
    with st.sidebar:
        st.markdown("## 📊 Data Storytelling Studio")
        st.caption("PGDM-BDA | Goa Institute of Management")
        st.session_state["teaching_mode"] = st.radio("Mode", ["Instructor Mode", "Student Mode"], index=0, horizontal=False)
        projector = st.checkbox("Projector-friendly mode", value=False)
        page = st.radio(
            "Navigate",
            [
                "Home",
                "Course Roadmap",
                "Instructor Delivery Planner",
                "Session Learning Studio",
                "Chart Selection Engine",
                "Visualization Master Gallery",
                "Before–After Visual Makeover Studio",
                "Misleading Chart Clinic",
                "Dashboard Design Studio",
                "Storytelling Framework Builder",
                "Annotation and Title Lab",
                "Business Case Library",
                "Business Role-Play Mode",
                "Activity Bank",
                "Quiz Zone",
                "Rubrics and Exam Question Bank",
                "Upload and Auto-Story Lab",
                "Final Integrated Workshop",
                "Resources",
            ],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.caption("Built with Streamlit, Plotly, Pandas, and NumPy. No API calls. No paid dependencies.")
    apply_projector_mode(projector)

    if page == "Home":
        page_home()
    elif page == "Course Roadmap":
        page_roadmap()
    elif page == "Instructor Delivery Planner":
        page_instructor_planner()
    elif page == "Session Learning Studio":
        page_session_studio()
    elif page == "Chart Selection Engine":
        page_chart_engine()
    elif page == "Visualization Master Gallery":
        page_visual_gallery()
    elif page == "Before–After Visual Makeover Studio":
        page_visual_makeover()
    elif page == "Misleading Chart Clinic":
        page_misleading_clinic()
    elif page == "Dashboard Design Studio":
        page_dashboard_studio()
    elif page == "Storytelling Framework Builder":
        page_story_builder()
    elif page == "Annotation and Title Lab":
        page_title_lab()
    elif page == "Business Case Library":
        page_case_library()
    elif page == "Business Role-Play Mode":
        page_role_play_mode()
    elif page == "Activity Bank":
        page_activity_bank()
    elif page == "Quiz Zone":
        page_quiz_zone()
    elif page == "Rubrics and Exam Question Bank":
        page_rubrics_exam_bank()
    elif page == "Upload and Auto-Story Lab":
        page_upload_auto_story()
    elif page == "Final Integrated Workshop":
        page_final_workshop()
    elif page == "Resources":
        page_resources()


if __name__ == "__main__":
    main()
