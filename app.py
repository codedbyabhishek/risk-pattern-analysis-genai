from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"
DATA_PATH = OUTPUT_DIR / "scored_signups.csv"
SUMMARY_PATH = OUTPUT_DIR / "summary.json"
RULES_PATH = OUTPUT_DIR / "generated_rules.md"


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        return pd.DataFrame()
    df = pd.read_csv(DATA_PATH)
    if "risk_score" in df.columns:
        df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0).astype(int)
    return df


def load_summary() -> dict:
    if not SUMMARY_PATH.exists():
        return {}
    return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))


def load_rules() -> str:
    if not RULES_PATH.exists():
        return "No generated rules found. Run ./scripts/run_pipeline.sh first."
    return RULES_PATH.read_text(encoding="utf-8")


def main() -> None:
    st.set_page_config(page_title="Risk Pattern Analysis Dashboard", layout="wide")
    st.title("Risk Pattern Analysis Using GenAI")
    st.caption("Interactive fraud-risk dashboard | Independent Project (Nov 2025 - Feb 2026)")

    df = load_data()
    summary = load_summary()

    if df.empty:
        st.warning("No scored data found. Run ./scripts/run_pipeline.sh first.")
        st.stop()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Records Processed", summary.get("records_processed", len(df)))
    c2.metric("Average Risk Score", summary.get("average_risk_score", round(df["risk_score"].mean(), 2)))
    c3.metric("Tier 4 (Block)", summary.get("tier_4_block_count", int((df["risk_tier"] == "TIER_4_BLOCK").sum())))
    c4.metric("Tier 1 (Monitor)", summary.get("tier_1_monitor_count", int((df["risk_tier"] == "TIER_1_MONITOR").sum())))

    st.subheader("Risk Tier Distribution")
    tier_counts = df["risk_tier"].value_counts().rename_axis("risk_tier").reset_index(name="count")
    st.bar_chart(tier_counts.set_index("risk_tier"))

    st.subheader("Filter Suspicious Accounts")
    min_score = st.slider("Minimum Risk Score", min_value=0, max_value=100, value=20, step=1)
    selected_tiers = st.multiselect(
        "Risk Tiers",
        options=sorted(df["risk_tier"].dropna().unique().tolist()),
        default=sorted(df["risk_tier"].dropna().unique().tolist()),
    )

    filtered = df[(df["risk_score"] >= min_score) & (df["risk_tier"].isin(selected_tiers))]
    st.write(f"Showing {len(filtered)} of {len(df)} records")
    st.dataframe(
        filtered[
            [
                "event_id",
                "timestamp",
                "email",
                "risk_score",
                "risk_tier",
                "last_24h_signups_ip",
                "last_24h_signups_device",
                "failed_otps",
                "is_disposable_email",
                "is_proxy_ip",
                "ip_country",
                "phone_country",
            ]
        ],
        use_container_width=True,
    )

    st.subheader("Top High-Risk Events")
    top_cols = [
        "event_id",
        "email",
        "risk_score",
        "risk_tier",
        "ip_velocity_high",
        "device_velocity_high",
        "otp_failure_high",
        "disposable_email",
        "proxy_ip",
        "geo_mismatch",
    ]
    st.dataframe(df.sort_values("risk_score", ascending=False).head(10)[top_cols], use_container_width=True)

    st.subheader("Generated Candidate Rules")
    st.markdown(load_rules())


if __name__ == "__main__":
    main()
