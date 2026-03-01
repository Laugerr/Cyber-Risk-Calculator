# 🛡️ Cyber Risk Calculator (ROSI Model)

![Tests](https://github.com/Laugerr/Cyber-Risk-Calculator/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Status](https://img.shields.io/badge/Project-Active-success)

A lightweight **quantitative cyber risk assessment tool** that calculates:

- 📊 **SLE** (Single Loss Expectancy)  
- 📉 **ALE** (Annualized Loss Expectancy)  
- 💰 **Risk Reduction**  
- 📈 **ROSI** (Return on Security Investment)  

Designed to support **data-driven security investment decisions** for risk managers, CISOs, and cybersecurity professionals.

---

## 🚀 Features

- ✅ Quantitative risk calculations (SLE, ALE before/after)
- 🚦 Automatic risk classification (**LOW / MEDIUM / HIGH**)
- 🖥️ Professional CLI interface
- 📦 JSON report output for automation
- 🧪 Unit tested with pytest
- 🔁 GitHub Actions CI integration

---

## 📘 Risk Model & Formulas

### 🔹 Single Loss Expectancy (SLE)

> “SLE = Asset Value × Exposure Factor”


### 🔹 Annualized Loss Expectancy (ALE)

> “ALE = SLE × Annual Rate of Occurrence (ARO)”


### 🔹 Risk Reduction

> “Risk Reduction = ALE(before) − ALE(after)”


### 🔹 Return on Security Investment (ROSI)

> “ROSI% = ((Risk Reduction − Control Cost) / Control Cost) × 100”

---

## 🧰 Installation

```bash
git clone https://github.com/Laugerr/Cyber-Risk-Calculator.git
cd Cyber-Risk-Calculator
python3 -m pip install -r requirements.txt
```

### ▶️ Usage

## 🖥️ Standard CLI Report

```bash
python3 -m src.cli \
  --asset-value 500000 \
  --exposure-factor 0.4 \
  --aro 0.3 \
  --risk-reduction 60 \
  --control-cost 20000
```

## 📦 JSON Output Mode

```bash
python3 -m src.cli \
  --asset-value 500000 \
  --exposure-factor 0.4 \
  --aro 0.3 \
  --risk-reduction 60 \
  --control-cost 20000 \
  --json
```

## 📄 Example JSON Output

```json
{
  "inputs": {
    "asset_value": 500000.0,
    "exposure_factor": 0.4,
    "aro": 0.3,
    "risk_reduction_pct": 60.0,
    "control_cost": 20000.0
  },
  "results": {
    "sle": 200000.0,
    "ale_before": 60000.0,
    "ale_after": 24000.0,
    "risk_reduction": 36000.0,
    "rosi_pct": 80.0,
    "risk_level": "MEDIUM"
  },
  "decision": "APPROVE"
}
```
---

### 🚦 Risk Level Thresholds

Risk classification is based on **ALE (before control implementation)**:

| ALE (Before) | Risk Level |
| --- | --- |
| < €30,000 | LOW |
| €30,000--€99,999 | MEDIUM |
| ≥ €100,000 | HIGH |

Thresholds are intentionally simple and can be adapted to organizational risk appetite.

---

## 🧪 Run Tests
```bash
pytest -q
```

---

## 📌 Roadmap

-   Add `--out report.json` export option

-   Add configurable risk thresholds

-   Add HTML executive report

-   Add multi-control comparison engine

-   Add Monte Carlo simulation module

---

## 👨‍💻 Author

Salah Eddine El Manssouri
MSc Cybersecurity Management
Vilnius, Lithuania

Focused on Risk Management, Security Economics, and Application Security Engineering.

---

## 📜 License

MIT ⚖️