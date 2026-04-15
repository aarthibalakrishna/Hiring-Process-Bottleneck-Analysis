import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hiring Bottleneck Analyser",
    page_icon="📊",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .main { background-color: #f8fafc; }
  .block-container { padding-top: 2rem; padding-bottom: 2rem; }
  .metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
  }
  .metric-label {
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
  }
  .metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #1e3a5f;
    line-height: 1.1;
  }
  .metric-sub {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 4px;
  }
  .bottleneck-card {
    background: #fff5f5;
    border: 1.5px solid #feb2b2;
    border-left: 5px solid #e53e3e;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 10px;
  }
  .watch-card {
    background: #fffbeb;
    border: 1.5px solid #fbd38d;
    border-left: 5px solid #d97706;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 10px;
  }
  .ok-card {
    background: #f0fff4;
    border: 1.5px solid #9ae6b4;
    border-left: 5px solid #38a169;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 10px;
  }
  .rec-card {
    background: #ebf8ff;
    border: 1px solid #bee3f8;
    border-left: 4px solid #2b6cb0;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 8px;
  }
  .section-title {
    font-size: 18px;
    font-weight: 700;
    color: #1e3a5f;
    margin-bottom: 0.8rem;
    padding-bottom: 6px;
    border-bottom: 2px solid #e2e8f0;
  }
  .app-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2b6cb0 100%);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.8rem;
    color: white;
  }
  .upload-box {
    background: white;
    border: 2px dashed #cbd5e0;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
  }
  h1, h2, h3 { color: #1e3a5f; }
  .stAlert { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <h1 style="color:white; margin:0; font-size:26px;">📊 Hiring Process Bottleneck Analyser</h1>
  <p style="color:#bee3f8; margin:6px 0 0; font-size:14px;">
    Upload your hiring pipeline data to identify bottlenecks, track cycle time, and get actionable recommendations.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Benchmarks ────────────────────────────────────────────────────────────────
BENCHMARKS = {
    "Days_App_to_Screen":  5,
    "Days_Screen_to_Int1": 4,
    "Days_Int1_to_Int2":   3,
    "Days_Int2_to_Offer":  4,
    "Days_Offer_to_Join":  14,
}
STAGE_LABELS = {
    "Days_App_to_Screen":  "Application → Screening",
    "Days_Screen_to_Int1": "Screening → Interview 1",
    "Days_Int1_to_Int2":   "Interview 1 → Interview 2",
    "Days_Int2_to_Offer":  "Interview 2 → Offer",
    "Days_Offer_to_Join":  "Offer → Joining",
}

# ── Sidebar — Upload + Benchmarks ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📁 Data Source")
    uploaded = st.file_uploader(
        "Upload Excel file (.xlsx)",
        type=["xlsx"],
        help="Must have a sheet named 'Candidate_Pipeline' with the standard columns."
    )
    st.markdown("---")
    st.markdown("### ⚙️ Benchmark Settings (days)")
    st.caption("Adjust expected days per stage")
    BENCHMARKS["Days_App_to_Screen"]  = st.slider("Application → Screening",  1, 20, 5)
    BENCHMARKS["Days_Screen_to_Int1"] = st.slider("Screening → Interview 1",  1, 14, 4)
    BENCHMARKS["Days_Int1_to_Int2"]   = st.slider("Interview 1 → Interview 2",1, 10, 3)
    BENCHMARKS["Days_Int2_to_Offer"]  = st.slider("Interview 2 → Offer",      1, 14, 4)
    BENCHMARKS["Days_Offer_to_Join"]  = st.slider("Offer → Joining",          5, 40, 14)
    st.markdown("---")
    st.markdown("### 📌 About")
    st.caption(
        "Built by Aarthi as part of the Hiring Process "
        "Bottleneck Analysis project. Tools: Python · Pandas · Plotly · Streamlit."
    )

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    return pd.read_excel(file, sheet_name="Candidate_Pipeline")

if uploaded:
    try:
        df = load_data(uploaded)
    except Exception as e:
        st.error(f"Could not read file: {e}. Make sure it has a 'Candidate_Pipeline' sheet.")
        st.stop()
else:
    st.info("👆 Upload your hiring dataset in the sidebar to begin. Using the sample dataset for now.")
    try:
        df = pd.read_excel("hiring_bottleneck_dataset.xlsx", sheet_name="Candidate_Pipeline")
    except FileNotFoundError:
        st.warning("Place `hiring_bottleneck_dataset.xlsx` in the same folder as this app to see the demo.")
        st.stop()

# ── Compute summary ───────────────────────────────────────────────────────────
results = []
for col, bench in BENCHMARKS.items():
    if col not in df.columns:
        continue
    numeric  = pd.to_numeric(df[col], errors="coerce")
    avg      = round(numeric.mean(), 1)
    variance = round(avg - bench, 1)
    status   = "Bottleneck" if variance > 5 else ("Watch" if variance > 0 else "On Track")
    results.append({
        "Stage":     STAGE_LABELS[col],
        "Avg Days":  avg,
        "Benchmark": bench,
        "Variance":  variance,
        "Status":    status,
    })
summary = pd.DataFrame(results)

total        = len(df)
avg_total    = round(pd.to_numeric(df.get("Total_Days", pd.Series(dtype=float)), errors="coerce").mean(), 1)
hired_count  = int((df["Final_Status"] == "Hired").sum()) if "Final_Status" in df.columns else 0
offered      = int(df["Offer_Date"].notna().sum()) if "Offer_Date" in df.columns else 0
offer_accept = round(hired_count / offered * 100, 1) if offered > 0 else 0
screened     = int(df["Screening_Date"].notna().sum()) if "Screening_Date" in df.columns else total
interviewed1 = int(df["Interview_1_Date"].notna().sum()) if "Interview_1_Date" in df.columns else 0
interviewed2 = int(df["Interview_2_Date"].notna().sum()) if "Interview_2_Date" in df.columns else 0

bottleneck_stages = summary[summary["Status"] == "Bottleneck"]
primary = bottleneck_stages.loc[bottleneck_stages["Variance"].idxmax()] if not bottleneck_stages.empty else None

# ── Section 1: Key Metrics ────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Metrics</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

def metric_card(col, label, value, sub=""):
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

metric_card(c1, "Total Candidates", total, "in pipeline")
metric_card(c2, "Avg Total Hire Time", f"{avg_total}d", "application to joining")
metric_card(c3, "Hired", hired_count, f"{round(hired_count/total*100,1)}% of applicants")
metric_card(c4, "Offer Acceptance", f"{offer_accept}%", f"{hired_count} of {offered} offers")

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 2: Bottleneck + Funnel side by side ───────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">Bottleneck Analysis</div>', unsafe_allow_html=True)

    if primary is not None:
        st.markdown(f"""
        <div class="bottleneck-card">
          <div style="font-size:13px;font-weight:700;color:#c53030;margin-bottom:4px;">PRIMARY BOTTLENECK DETECTED</div>
          <div style="font-size:17px;font-weight:700;color:#1a202c;">{primary['Stage']}</div>
          <div style="font-size:13px;color:#4a5568;margin-top:4px;">
            Averaging <strong>{primary['Avg Days']} days</strong> vs benchmark of <strong>{primary['Benchmark']} days</strong>
            — that's <strong>+{primary['Variance']} days</strong> over target on every single hire.
          </div>
        </div>""", unsafe_allow_html=True)

    for _, row in summary.iterrows():
        card_class = "bottleneck-card" if row["Status"] == "Bottleneck" else \
                     "watch-card"      if row["Status"] == "Watch"       else "ok-card"
        icon  = "🔴" if row["Status"] == "Bottleneck" else \
                "🟡" if row["Status"] == "Watch"       else "🟢"
        var_str = f"+{row['Variance']}d" if row['Variance'] >= 0 else f"{row['Variance']}d"
        st.markdown(f"""
        <div class="{card_class}">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
              <span style="font-size:13px;font-weight:600;color:#1a202c;">{icon} {row['Stage']}</span><br>
              <span style="font-size:12px;color:#4a5568;">
                Avg: <b>{row['Avg Days']}d</b> &nbsp;|&nbsp; Benchmark: <b>{row['Benchmark']}d</b>
              </span>
            </div>
            <div style="text-align:right;">
              <span style="font-size:16px;font-weight:700;color:{'#c53030' if row['Status']=='Bottleneck' else '#d97706' if row['Status']=='Watch' else '#276749'}">
                {var_str}
              </span><br>
              <span style="font-size:11px;color:#718096;">{row['Status']}</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-title">Candidate Funnel</div>', unsafe_allow_html=True)

    funnel_data = pd.DataFrame([
        {"Stage": "Applied",        "Candidates": total},
        {"Stage": "Screened",       "Candidates": screened},
        {"Stage": "Interview 1",    "Candidates": interviewed1},
        {"Stage": "Interview 2",    "Candidates": interviewed2},
        {"Stage": "Offer Extended", "Candidates": offered},
        {"Stage": "Joined",         "Candidates": hired_count},
    ])

    colors = ["#2b6cb0", "#3182ce", "#4299e1", "#63b3ed", "#90cdf4", "#bee3f8"]

    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data["Stage"],
        x=funnel_data["Candidates"],
        textinfo="value+percent initial",
        textfont=dict(size=13),
        marker=dict(color=colors),
        connector=dict(line=dict(color="#e2e8f0", width=1)),
    ))
    fig_funnel.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=370,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=12, color="#1e3a5f"),
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    biggest_drop_idx = funnel_data["Candidates"].diff().abs().idxmax()
    if biggest_drop_idx and biggest_drop_idx > 0:
        drop_stage = funnel_data.iloc[biggest_drop_idx]["Stage"]
        drop_prev  = funnel_data.iloc[biggest_drop_idx - 1]["Candidates"]
        drop_curr  = funnel_data.iloc[biggest_drop_idx]["Candidates"]
        drop_n     = drop_prev - drop_curr
        st.caption(f"Biggest drop-off: **{drop_stage}** — {drop_n} candidates lost ({round(drop_n/total*100,1)}% of total)")

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 3: Recommendations ───────────────────────────────────────────────
st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)

recs = [
    ("1", "Introduce structured screening criteria",
     f"Implement an ATS-based checklist to reduce screening time from "
     f"{summary.iloc[0]['Avg Days']} days to the {BENCHMARKS['Days_App_to_Screen']}-day benchmark. "
     f"Expected saving: ~{round(summary.iloc[0]['Avg Days'] - BENCHMARKS['Days_App_to_Screen'], 1)} days per hire."),
    ("2", "Increase screener capacity",
     "Add a part-time recruiter or delegate initial screening to hiring managers "
     "to handle volume without overloading a single person."),
    ("3", "Weekly bottleneck tracking",
     "Monitor avg days per stage weekly using this dashboard. Set alerts when any "
     "stage exceeds benchmark by more than 2 days to catch new bottlenecks early."),
]

rc1, rc2, rc3 = st.columns(3)
for col, (num, title, body) in zip([rc1, rc2, rc3], recs):
    col.markdown(f"""
    <div class="rec-card">
      <div style="font-size:11px;font-weight:700;color:#2b6cb0;margin-bottom:4px;">RECOMMENDATION {num}</div>
      <div style="font-size:14px;font-weight:600;color:#1a202c;margin-bottom:6px;">{title}</div>
      <div style="font-size:12px;color:#4a5568;line-height:1.5;">{body}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Section 4: Raw Data ───────────────────────────────────────────────────────
with st.expander("View raw pipeline data"):
    st.dataframe(df, use_container_width=True, height=300)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download as CSV", csv, "pipeline_data.csv", "text/csv")