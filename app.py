import json
import streamlit as st
import pandas as pd

from src.rosi import RosiInputs, calculate
from dataclasses import asdict


st.set_page_config(page_title="Cyber Risk Calculator (ROSI)", page_icon="🛡️", layout="centered")

st.title("🛡️ Cyber Risk Calculator (ROSI Model)")
st.caption("Quantitative risk analysis for security investment decisions (SLE, ALE, Risk Reduction, ROSI).")

with st.sidebar:
    st.header("Inputs")
    asset_value = st.number_input("Asset Value (€)", min_value=0.0, value=500000.0, step=1000.0)
    exposure_factor = st.slider("Exposure Factor (0–1)", min_value=0.0, max_value=1.0, value=0.40, step=0.01)
    aro = st.number_input("Annual Rate of Occurrence (ARO)", min_value=0.0, value=0.30, step=0.05)
    risk_reduction_pct = st.slider("Risk Reduction (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
    control_cost = st.number_input("Control Cost (€)", min_value=1.0, value=20000.0, step=500.0)

run = st.button("✅ Calculate", use_container_width=True)

def format_eur(v: float) -> str:
    return f"€{v:,.2f}"

if run:
    inputs = RosiInputs(
        asset_value=asset_value,
        exposure_factor=exposure_factor,
        aro=aro,
        risk_reduction_pct=risk_reduction_pct,
        control_cost=control_cost,
    )
    results = calculate(inputs)

    decision = "APPROVE" if results.rosi_pct > 0 else "REJECT"

    st.subheader("📊 Results")

    c1, c2, c3 = st.columns(3)
    c1.metric("SLE", format_eur(results.sle))
    c2.metric("ALE (Before)", format_eur(results.ale_before))
    c3.metric("Risk Level", results.risk_level)

    c4, c5, c6 = st.columns(3)
    c4.metric("ALE (After)", format_eur(results.ale_after))
    c5.metric("Risk Reduction", format_eur(results.risk_reduction))
    c6.metric("ROSI", f"{results.rosi_pct:.2f}%")

    st.markdown("### ✅ Decision")
    if decision == "APPROVE":
        st.success("✅ APPROVE INVESTMENT (ROSI > 0)")
    else:
        st.error("❌ REJECT INVESTMENT (ROSI ≤ 0)")

    st.markdown("### 📈 ALE Comparison")
    chart_df = pd.DataFrame(
        {
            "Metric": ["ALE Before", "ALE After"],
            "Value (€)": [results.ale_before, results.ale_after],
        }
    )
    st.bar_chart(chart_df.set_index("Metric"))

    st.markdown("### 📦 JSON Report")
    payload = {
        "inputs": asdict(inputs),
        "results": asdict(results),
        "decision": decision,
    }
    json_str = json.dumps(payload, indent=2)
    st.code(json_str, language="json")

    st.download_button(
        label="⬇️ Download JSON report",
        data=json_str,
        file_name="rosi_report.json",
        mime="application/json",
        use_container_width=True,
    )
else:
    st.info("Set inputs in the sidebar, then click **Calculate**.")