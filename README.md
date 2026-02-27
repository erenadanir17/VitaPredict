<p align="center">
  <h1 align="center">VitaPredict</h1>
  <p align="center">AI-powered vitamin & mineral blood test analyzer with personalized supplement recommendations</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" />
</p>

---

## What is VitaPredict?

VitaPredict analyzes your blood test results and provides a comprehensive health report including deficiency detection, supplement plans, drug interactions, meal suggestions, and recovery timelines — all in a beautiful dark-themed dashboard.

**No AI API needed. Everything runs locally.**

## Features

### Core Analysis
| Feature | Description |
|---------|-------------|
| **5-Level Detection** | Urgent, Critical, Low, Borderline, Normal severity classification |
| **18 Vitamins & Minerals** | D, B12, Folate, Iron, Magnesium, Zinc, B6, C, A, E, Omega-3, B1, B2, Selenium, K, Copper, Chromium, Iodine |
| **Personal Profile** | Age, gender, and lifestyle-based risk analysis |
| **Drug Interactions** | SSRI, SNRI, Benzodiazepine, Antipsychotic, Mood Stabilizer, Stimulant interactions |

### Visual Dashboard
| Feature | Description |
|---------|-------------|
| **Bar Chart + Radar Chart** | Side-by-side vitamin level visualization |
| **Category Donut Charts** | Vitamin vs Mineral and Status distribution |
| **Health Score Gauge** | 0-100 overall health score with conic gradient ring |
| **Body Map** | Affected organ systems with emoji indicators |

### Smart Recommendations
| Feature | Description |
|---------|-------------|
| **Supplement Plan** | Dose, form, and timing for each deficiency |
| **Daily Schedule** | Morning / Noon / Evening supplement timetable |
| **Weekly Meal Plan** | 7-day food recommendations per vitamin |
| **Food Portions** | Exact portions to meet daily requirements |
| **Brand Suggestions** | Popular supplement brands available in Turkey |
| **Vitamin Synergy** | Which vitamins to take together |
| **Conflict Matrix** | Which vitamins should NOT be taken together |

### Insights & Tracking
| Feature | Description |
|---------|-------------|
| **Recovery Timeline** | When to expect improvements (1 / 3 / 6 months) |
| **Before/After Simulation** | Visual timeline of expected changes |
| **Turkey Comparison** | Compare your levels with national averages |
| **Seasonal Tips** | Season-specific vitamin recommendations |
| **History Tracking** | Compare with previous analysis |
| **Monthly Cost Estimate** | Supplement budget calculator |

### Interactive Features
| Feature | Description |
|---------|-------------|
| **Symptom Checker** | Select symptoms to predict deficiencies |
| **Vitamin Quiz** | 10-question interactive knowledge quiz |
| **Vitamin Encyclopedia** | Browse detailed info for any vitamin |
| **Daily Fun Fact** | New vitamin fact every day |
| **Water Calculator** | Daily water intake based on body weight |
| **Achievement Badges** | 8 unlockable badges (Iron Warrior, Sun Child, Brain Power...) |
| **Demo Mode** | One-click sample data to showcase all features |

### Export & Share
| Feature | Description |
|---------|-------------|
| **PDF Report** | Download complete analysis as PDF |
| **Share Summary** | Copy-paste friendly result summary |

### Design
| Feature | Description |
|---------|-------------|
| **Dark Theme** | Custom CSS with Space Grotesk + JetBrains Mono |
| **Animations** | Fade-in cards, scale-up counters, shimmer effects |
| **Mobile Responsive** | Works on phones and tablets |

## Quick Start

```bash
git clone https://github.com/erenadanir17/VitaPredict.git
cd VitaPredict
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8510` in your browser.

## Project Structure

```
VitaPredict/
├── app.py                  # Main Streamlit application
├── data/
│   ├── vitamins.py         # 18 vitamin/mineral database
│   ├── drugs.py            # 6 drug class interactions
│   └── extras.py           # Symptoms, meals, quiz, brands, costs
├── utils/
│   ├── analyzer.py         # 5-level analysis engine
│   ├── styles.py           # Full custom CSS design
│   └── pdf_report.py       # PDF report generator
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── requirements.txt
├── .gitignore
└── README.md
```

## Screenshots

Click **Demo Mode** in the sidebar to instantly see all features with sample blood test data.

## Tech Stack

- **Python 3.9+** — Core language
- **Streamlit** — Web framework
- **Plotly** — Interactive charts (bar, radar, donut)
- **fpdf2** — PDF generation
- **Custom CSS** — 600+ lines of hand-crafted dark theme

## Supported Vitamins & Minerals

| # | Vitamin/Mineral | Unit | Normal Range |
|---|----------------|------|-------------|
| 1 | Vitamin D | ng/mL | 30 - 100 |
| 2 | Vitamin B12 | pg/mL | 200 - 900 |
| 3 | Folate (B9) | ng/mL | 3 - 17 |
| 4 | Iron (Ferritin) | ng/mL | 12 - 150 |
| 5 | Magnesium | mg/dL | 1.7 - 2.2 |
| 6 | Zinc | ug/dL | 70 - 130 |
| 7 | Vitamin B6 | ug/L | 5 - 50 |
| 8 | Vitamin C | mg/dL | 0.4 - 2.0 |
| 9 | Vitamin A | ug/dL | 30 - 65 |
| 10 | Iodine (TSH) | mIU/L | 0.4 - 4.0 |
| 11 | Vitamin E | mg/L | 5.5 - 17.0 |
| 12 | Omega-3 | Index % | 8 - 12 |
| 13 | Vitamin B1 | nmol/L | 70 - 180 |
| 14 | Vitamin B2 | ug/L | 5 - 50 |
| 15 | Selenium | ug/L | 70 - 150 |
| 16 | Vitamin K | ug/L | 0.2 - 3.2 |
| 17 | Copper | ug/dL | 70 - 175 |
| 18 | Chromium | ug/L | 0.1 - 0.5 |

## Disclaimer

This application is for **informational purposes only** and does not replace medical advice.
Always consult your doctor before starting any supplements or making medication changes.

## License

MIT
