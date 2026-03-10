# app.py — Virat Kohli 100 Centuries Hypothesis Dashboard

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title  = "Kohli 100 Centuries",
    page_icon   = "🏏",
    layout      = "wide"
)

# ── Load Data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/kohli_odi_innings.csv',
                     parse_dates=['date'])
    df['year']         = df['date'].dt.year
    df['century_int']  = df['century'].astype(int)
    df['rolling_rate'] = (df['century_int']
                          .rolling(window=20, min_periods=10)
                          .mean() * 100)
    return df

df = load_data()

# ── Sidebar Navigation ────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/en/thumb/4/41/"
    "Flag_of_India.svg/1200px-Flag_of_India.svg.png",
    width=100
)
st.sidebar.title("🏏 Kohli 100 Centuries")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview",
     "📊 EDA — Career Analysis",
     "🔬 Hypothesis Test",
     "🎛️ Interactive Scenarios"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Project Info**
- Format : ODI only
- Data   : Cricsheet.org
- Method : Binomial Test
- α      : 0.05
""")

# ═══════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════
if page == "🏠 Overview":

    st.title("🏏 Will Virat Kohli Reach 100 International Centuries?")
    st.markdown("""
    A statistical hypothesis test using Virat Kohli's complete ODI career data
    to determine whether he can score **15 more ODI centuries** to reach
    the historic milestone of **100 international centuries**.
    """)

    st.markdown("---")

    # ── Key Metrics ───────────────────────────────────────
    st.subheader("📌 Current Status")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("ODI Centuries",      "54",    "Active format")
    col2.metric("Test Centuries",     "30",    "Retired ❌")
    col3.metric("T20I Centuries",     "1",     "Retired ❌")
    col4.metric("Total International","85",    "15 short of 100")
    col5.metric("Age",                "37",    "Born Nov 1988")

    st.markdown("---")

    col6, col7, col8, col9 = st.columns(4)

    total_runs  = df['runs'].sum()
    dismissals  = df['dismissed'].sum()
    avg         = total_runs / dismissals
    c_rate      = len(df) / df['century'].sum()

    col6.metric("ODI Innings",       f"{len(df)}")
    col7.metric("Total ODI Runs",    f"{total_runs:,}")
    col8.metric("Batting Average",   f"{avg:.2f}")
    col9.metric("Century Rate",      f"1 per {c_rate:.1f} innings")

    st.markdown("---")

    # ── Career runs per innings bar chart ─────────────────
    st.subheader("📈 Career at a Glance — Every Innings")

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(df.index,
           df['runs'],
           color=df['century'].map({True: '#ff6b00', False: '#1a73e8'}),
           alpha=0.7, width=1.0)
    ax.axhline(y=100, color='red', linestyle='--',
               linewidth=1.2, label='100 run mark')
    ax.set_xlabel("Innings Number")
    ax.set_ylabel("Runs Scored")
    ax.set_title("Kohli ODI Innings — Orange = Century, Blue = Non-Century")
    ax.legend()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")

    # ── The challenge ──────────────────────────────────────
    st.subheader("🎯 The Challenge")

    col_a, col_b = st.columns(2)

    with col_a:
        st.info("""
        **What needs to happen:**
        - Score 15 more ODI centuries
        - Only plays ODIs now (retired from Tests & T20Is)
        - Estimated 32–39 ODI innings remaining
        - Needs to maintain current form through 2027 WC
        """)

    with col_b:
        st.warning("""
        **What makes it hard:**
        - At career rate (18.2%): expects only ~7 more centuries
        - At recent form (23.8%): expects only ~9 more centuries
        - Even best case is 6 centuries short of target
        - Would need ~62 innings for a 50/50 chance
        """)

# ═══════════════════════════════════════════════════════════
# PAGE 2 — EDA
# ═══════════════════════════════════════════════════════════
elif page == "📊 EDA — Career Analysis":

    st.title("📊 Career Analysis — Exploring the Data")
    st.markdown("---")

    # ── Centuries per year ────────────────────────────────
    st.subheader("📅 Centuries Per Year")

    centuries_per_year = df.groupby('year')['century'].sum()

    fig, ax = plt.subplots(figsize=(14, 4))
    colors  = ['#ff6b00' if y >= 2022 else '#1a73e8'
               for y in centuries_per_year.index]
    ax.bar(centuries_per_year.index,
           centuries_per_year.values,
           color=colors, alpha=0.85)
    ax.set_xlabel("Year")
    ax.set_ylabel("Centuries")
    ax.set_title("ODI Centuries Per Year  🟠 = Recent Form (2022+)")
    ax.set_xticks(centuries_per_year.index)
    ax.set_xticklabels(centuries_per_year.index, rotation=45)
    ax.grid(alpha=0.2, axis='y')
    st.pyplot(fig)
    plt.close()

    st.markdown("---")

    # ── Opponent analysis ─────────────────────────────────
    st.subheader("🌍 Performance by Opponent")

    opponent_stats = df.groupby('opponent').agg(
        innings   = ('runs', 'count'),
        runs      = ('runs', 'sum'),
        centuries = ('century', 'sum'),
    ).reset_index()
    opponent_stats = opponent_stats[opponent_stats['innings'] >= 10]
    opponent_stats['century_rate'] = (
        opponent_stats['centuries'] /
        opponent_stats['innings'] * 100
    ).round(1)
    opponent_stats = opponent_stats.sort_values('centuries', ascending=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].barh(opponent_stats['opponent'],
                 opponent_stats['centuries'],
                 color='#ff6b00', alpha=0.85)
    axes[0].set_title("Centuries vs Each Opponent")
    axes[0].set_xlabel("Centuries")

    axes[1].barh(opponent_stats['opponent'],
                 opponent_stats['century_rate'],
                 color='#1a73e8', alpha=0.85)
    axes[1].set_title("Century Rate % vs Each Opponent")
    axes[1].set_xlabel("Century Rate (%)")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")

    # ── Rolling form ──────────────────────────────────────
    st.subheader("📉 Century Rate Over Career (Rolling 20 Innings)")

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(df['date'], df['rolling_rate'],
            color='#ff6b00', linewidth=2.5,
            label='Rolling 20-innings rate')
    ax.axhline(y=df['century_int'].mean() * 100,
               color='blue', linestyle='--',
               linewidth=1.5,
               label=f'Career avg ({df["century_int"].mean()*100:.1f}%)')
    ax.axvspan(pd.Timestamp('2020-01-01'),
               pd.Timestamp('2022-06-01'),
               alpha=0.15, color='red',
               label='Drought (2020-2022)')
    ax.axvspan(pd.Timestamp('2023-01-01'),
               pd.Timestamp('2026-12-31'),
               alpha=0.15, color='green',
               label='Comeback (2023+)')
    ax.set_ylabel("Century Rate %")
    ax.set_title("Rolling Century Rate — Career Form Trend")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 45)
    ax.grid(alpha=0.2)
    st.pyplot(fig)
    plt.close()

    # ── Cumulative centuries ───────────────────────────────
    st.markdown("---")
    st.subheader("📈 Cumulative Centuries Over Career")

    df['cumulative'] = df['century_int'].cumsum()

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(df['date'], df['cumulative'],
            color='#ff6b00', linewidth=2.5)
    ax.axhline(y=54, color='green', linestyle='--',
               label='Current (54)')
    ax.fill_between(df['date'], df['cumulative'],
                    alpha=0.1, color='#ff6b00')
    ax.set_ylabel("Cumulative Centuries")
    ax.set_title("How Kohli's Century Tally Grew Over Time")
    ax.legend()
    ax.grid(alpha=0.2)
    st.pyplot(fig)
    plt.close()

# ═══════════════════════════════════════════════════════════
# PAGE 3 — HYPOTHESIS TEST
# ═══════════════════════════════════════════════════════════
elif page == "🔬 Hypothesis Test":

    st.title("🔬 Hypothesis Test — The Statistical Verdict")
    st.markdown("---")

    # ── Hypothesis statement ──────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.error("""
        **H₀ (Null Hypothesis)**

        Kohli will NOT score 15 more
        ODI centuries in his remaining career.

        Projected centuries < 15
        """)
    with col2:
        st.success("""
        **H₁ (Alternative Hypothesis)**

        Kohli WILL score 15 more
        ODI centuries in his remaining career.

        Projected centuries ≥ 15
        """)

    st.markdown("> **Test used:** Binomial Test  |  **α = 0.05**  |  **Method:** `1 - binom.cdf(14, n, p)`")
    st.markdown("---")

    # ── Results table ─────────────────────────────────────
    st.subheader("📊 Results Across All Scenarios")

    results = []
    for p_label, p in [('Conservative (18.2%)', 0.1824),
                        ('Optimistic (23.8%)',   0.2381)]:
        for n_label, n in [('Worst (n=25)',  25),
                            ('Middle (n=32)', 32),
                            ('Best (n=39)',   39)]:
            expected = round(n * p, 1)
            std      = np.sqrt(n * p * (1-p))
            ci_low   = round(max(0, expected - 1.96*std), 1)
            ci_high  = round(expected + 1.96*std, 1)
            pval     = round(1 - stats.binom.cdf(14, n, p), 4)
            decision = "❌ Unlikely" if pval < 0.01 else \
                       "⚠️ Borderline" if pval < 0.05 else \
                       "✅ Likely"
            results.append({
                'Rate Scenario'    : p_label,
                'Innings Scenario' : n_label,
                'Expected'         : expected,
                '95% CI'           : f"[{ci_low}, {ci_high}]",
                'P(≥15 centuries)' : f"{pval*100:.2f}%",
                'Decision'         : decision
            })

    st.dataframe(pd.DataFrame(results), use_container_width=True)
    st.markdown("---")

    # ── Innings needed chart ───────────────────────────────
    st.subheader("📉 How Many Innings Would He Need?")

    fig, ax = plt.subplots(figsize=(12, 5))
    innings_range = np.arange(1, 150)

    for label, p, color in [
        ('Conservative 18.2%', 0.1824, '#1a73e8'),
        ('Optimistic 23.8%',   0.2381, '#ff6b00'),
    ]:
        probs = [(1 - stats.binom.cdf(14, n, p)) * 100
                 for n in innings_range]
        ax.plot(innings_range, probs,
                color=color, linewidth=2.5, label=label)

    ax.axhline(y=5,  color='red',   linestyle='--',
               linewidth=1.5, label='5% threshold')
    ax.axhline(y=50, color='green', linestyle='--',
               linewidth=1.5, label='50% threshold')
    ax.axvspan(32, 39, alpha=0.2, color='purple',
               label='Estimated innings remaining')
    ax.set_xlabel("Remaining Innings")
    ax.set_ylabel("Probability of 15+ Centuries (%)")
    ax.set_title("Probability of Reaching Target vs Innings Remaining")
    ax.legend(fontsize=9)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close()

    st.markdown("---")

    # ── Final verdict ──────────────────────────────────────
    st.subheader("⚖️ Final Statistical Verdict")
    st.error("""
    **FAIL TO REJECT H₀**

    At α = 0.05, there is insufficient statistical evidence to support H₁.
    Across ALL scenarios tested, the probability of Kohli scoring
    15 more ODI centuries remains well below the 5% significance threshold.

    **Best case probability: only 2.94%**
    **Expected shortfall: ~6 centuries below target**
    """)

    st.info("""
    **Important Note:**
    This is a statistical conclusion based on historical rates and
    estimated schedules. Cricket is unpredictable — Kohli has defied
    statistics many times before. If he plays beyond 2027 or
    maintains exceptional form, the picture could change.
    """)

# ═══════════════════════════════════════════════════════════
# PAGE 4 — INTERACTIVE SCENARIOS
# ═══════════════════════════════════════════════════════════
elif page == "🎛️ Interactive Scenarios":

    st.title("🎛️ Interactive Scenario Explorer")
    st.markdown("Adjust the sliders to explore different scenarios and see how the probability changes live.")
    st.markdown("---")

    # ── Sliders ───────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎚️ Adjust Parameters")
        p_slider = st.slider(
            "Century Rate (%) — Kohli's form",
            min_value  = 10.0,
            max_value  = 35.0,
            value      = 18.2,
            step       = 0.1,
            help       = "Career avg = 18.2% | Recent form = 23.8%"
        )
        n_slider = st.slider(
            "Remaining Innings",
            min_value = 10,
            max_value = 80,
            value     = 39,
            step      = 1,
            help      = "Estimated 32-39 realistic | 62 needed for 50/50"
        )
        target_slider = st.slider(
            "Centuries Still Needed",
            min_value = 1,
            max_value = 20,
            value     = 15,
            step      = 1,
            help      = "Currently needs 15 more ODI centuries"
        )

    # ── Live calculation ───────────────────────────────────
    p        = p_slider / 100
    n        = n_slider
    target   = target_slider
    expected = n * p
    std      = np.sqrt(n * p * (1-p))
    ci_low   = max(0, expected - 1.96*std)
    ci_high  = expected + 1.96*std
    pval     = (1 - stats.binom.cdf(target-1, n, p)) * 100

    with col2:
        st.subheader("📊 Live Results")
        st.metric("Expected Centuries",  f"{expected:.1f}",
                  f"{expected - target:.1f} vs target")
        st.metric("95% Confidence Interval",
                  f"[{ci_low:.1f}, {ci_high:.1f}]")
        st.metric("Probability of Reaching Target",
                  f"{pval:.2f}%",
                  f"Need > 5% to be 'likely'")

        if pval >= 5:
            st.success("✅ REJECT H₀ — Statistically LIKELY at this scenario")
        elif pval >= 1:
            st.warning("⚠️ BORDERLINE — Possible but uncertain")
        else:
            st.error("❌ FAIL TO REJECT H₀ — Statistically UNLIKELY")

    st.markdown("---")

    # ── Live probability chart ─────────────────────────────
    st.subheader("📈 Probability Curve — Current Settings")

    innings_range = np.arange(1, 120)
    probs = [(1 - stats.binom.cdf(target-1, ni, p)) * 100
             for ni in innings_range]

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(innings_range, probs,
            color='#ff6b00', linewidth=2.5)
    ax.axhline(y=5,  color='red',   linestyle='--',
               linewidth=1.5, label='5% threshold')
    ax.axhline(y=50, color='green', linestyle='--',
               linewidth=1.5, label='50% threshold')
    ax.axvline(x=n_slider, color='purple', linestyle='-',
               linewidth=2, label=f'Your setting (n={n_slider})')
    ax.scatter([n_slider], [pval],
               color='purple', s=100, zorder=5)
    ax.annotate(f'  {pval:.1f}%',
                xy=(n_slider, pval),
                fontsize=11, color='purple',
                fontweight='bold')
    ax.set_xlabel("Remaining Innings")
    ax.set_ylabel("Probability (%)")
    ax.set_title(f"Probability of {target}+ Centuries at {p_slider:.1f}% Rate")
    ax.legend()
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close()

    # ── What if table ──────────────────────────────────────
    st.markdown("---")
    st.subheader("🔍 What Would It Take?")

    what_if = []
    for rate in [15, 18.2, 23.8, 28, 35]:
        p_wi = rate / 100
        for ni in range(10, 150):
            prob_wi = (1 - stats.binom.cdf(target-1, ni, p_wi)) * 100
            if prob_wi >= 5:
                what_if.append({
                    'Century Rate' : f"{rate}%",
                    'Innings for 5% chance'  : ni,
                    'Innings for 50% chance' : next(
                        (x for x in range(ni, 200)
                         if (1-stats.binom.cdf(target-1, x, p_wi))*100 >= 50),
                        ">200"
                    )
                })
                break

    st.dataframe(pd.DataFrame(what_if), use_container_width=True)