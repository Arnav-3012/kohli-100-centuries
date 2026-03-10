# 🏏 Virat Kohli — Will He Reach 100 International Centuries?

A complete end-to-end data science project applying **Binomial Hypothesis Testing** to determine whether Virat Kohli can score 15 more ODI centuries and reach the historic milestone of 100 international centuries.

---

## The Question

Kohli currently has **85 international centuries**:
- 54 in ODIs (active)
- 30 in Tests (retired)
- 1 in T20Is (retired)

The only path to 100 is through ODIs. Can he score **15 more** before he retires?

---

## Project Structure

```
kohli_100_centuries/
├── app.py                        # Streamlit dashboard
├── requirements.txt              # Python dependencies
├── data/
│   └── kohli_odi_innings.csv     # Processed dataset (296 innings)
└── notebooks/
    └── kohli_analysis.ipynb      # Full analysis notebook
```

---

## Data Source

**Cricsheet.org** — ball-by-ball CSV data for every international match.

- Downloaded 6,000+ ODI match files
- Filtered all innings where `striker == "V Kohli"`
- Aggregated runs, balls, dismissals per innings
- Final dataset: **296 ODI innings from 2008 to 2026**

---

## Methodology

### Statistical Test — Binomial Hypothesis Test

Each innings is modelled as an independent binary trial:
- **Success** = scoring a century (runs ≥ 100)
- **Failure** = not scoring a century
- **p** = probability of success per innings

```
H₀ : Kohli will NOT score 15 more ODI centuries
H₁ : Kohli WILL score 15 more ODI centuries
α  = 0.05
```

P-value calculated as:
```python
p_value = 1 - scipy.stats.binom.cdf(14, n, p)
```

### Two Probability Estimates

| Scenario | Rate | Source |
|---|---|---|
| Conservative | 18.2% | Full career average |
| Optimistic | 23.8% | 2023–2026 recent form |

### Three Innings Estimates

| Scenario | Innings | Assumption |
|---|---|---|
| Worst case | 25 | Significant rest/injury |
| Conservative | 32 | Some matches missed |
| Optimistic | 39 | Plays all series through 2027 WC |

Upcoming schedule includes:
- vs Afghanistan (Jun 2026) — 3 ODIs
- vs England (Jul 2026) — 3 ODIs
- vs West Indies (Late 2026) — 3 ODIs
- vs New Zealand (Oct 2026) — 5 ODIs
- vs Sri Lanka (Dec 2026) — 3 ODIs
- vs Australia & South Africa (Early 2027) — 6 ODIs
- Asia Cup 2027 — ~5 ODIs
- ODI World Cup 2027 — ~9 ODIs (if India reach final)

---

## Key Findings

### EDA Highlights

- Century rate has been consistent for 18 years — **1 every 5.5 innings**
- Best opponents: Sri Lanka (10 centuries), West Indies (9), Australia (8)
- Worst opponent: England (avg 36.8, only 7.9% century rate)
- 2020–2022 drought: rate crashed to **4.3%** (1 century in 23 innings)
- Post-comeback (2023+): rate at **23.8%** — above career average at age 37

### Hypothesis Test Results

| Rate | Innings | Expected | P(≥15 centuries) | Decision |
|---|---|---|---|---|
| 18.2% | 25 | 4.6 | 0.00% | ❌ Fail to Reject H₀ |
| 18.2% | 32 | 5.8 | 0.02% | ❌ Fail to Reject H₀ |
| 18.2% | 39 | 7.1 | ~0.5% | ❌ Fail to Reject H₀ |
| 23.8% | 25 | 5.9 | ~0.1% | ❌ Fail to Reject H₀ |
| 23.8% | 32 | 7.6 | ~1.2% | ❌ Fail to Reject H₀ |
| 23.8% | 39 | 9.3 | 2.94% | ⚠️ Borderline |

### Innings Needed

| Rate | Innings for 5% chance | Innings for 50/50 |
|---|---|---|
| 18.2% (career) | 54 | 81 |
| 23.8% (recent) | 42 | 62 |

### Verdict

> **Fail to Reject H₀**
>
> At α = 0.05, across all scenarios, the probability of Kohli scoring
> 15 more ODI centuries remains below the 5% significance threshold.
> The best case probability is **2.94%** — just below the threshold.
> He would need approximately **62 innings** for a 50/50 chance,
> but realistically has only **~39 innings** remaining.

---

## Dashboard Features

The Streamlit dashboard has 4 pages:

- **Overview** — career summary metrics and innings timeline
- **EDA** — centuries by year, opponent breakdown, rolling form trend
- **Hypothesis Test** — full results table, probability curves, verdict
- **Interactive Scenarios** — live sliders to explore custom assumptions

---

## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/Arnav-3012/kohli-100-centuries.git
cd kohli-100-centuries

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas | Data processing |
| NumPy | Numerical computing |
| SciPy | Binomial hypothesis test |
| Matplotlib | Visualizations |
| Streamlit | Interactive dashboard |
| Cricsheet | Raw ball-by-ball data |
| Git/GitHub | Version control |

---

## Live Demo

🔗 **Streamlit App**: [your-app-url.streamlit.app]

---

## Limitations

- Missing ~3 innings from early 2008 matches (corrupted files) — century count unaffected
- Home/away classification incomplete due to venue naming inconsistencies in raw data
- Remaining innings estimate is based on publicly known schedule — subject to change
- Model assumes constant p per innings — does not account for specific opponent strength or venue

---

## Author

**Arnav** — [@Arnav-3012](https://github.com/Arnav-3012)
