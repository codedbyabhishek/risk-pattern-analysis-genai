# Risk Pattern Analysis Using GenAI

**Duration:** Nov 2025 - Feb 2026  
**Type:** Independent Project  
**Focus Area:** Fraud Prevention, Risk Analytics, GenAI-Assisted Decisioning

![Risk Pattern Analysis Framework](assets/risk-pattern-framework.svg)

## Overview
This repository contains a working fraud-risk analysis prototype for account creation abuse. It ingests signup events, computes behavioral risk features, applies a scoring model, and generates prioritized candidate rules in a GenAI-style output format.

## Why This Project Matters
Fraudulent account creation impacts onboarding quality, trust, and downstream financial risk. This project demonstrates how to convert observed attacker behavior into implementation-ready control logic with explainable outcomes.

## What Is Implemented
- Feature engineering for signup abuse indicators
- Risk scoring model with tier-based actions
- Deterministic GenAI-style rule suggestion module
- End-to-end pipeline producing scored outputs and summary metrics
- Streamlit dashboard for recruiter-friendly interactive exploration

## Project Structure
- `src/risk_pattern_analysis/feature_engineering.py`: builds risk features from signup events
- `src/risk_pattern_analysis/scoring.py`: weighted risk score and policy tier mapping
- `src/risk_pattern_analysis/rule_generator.py`: candidate-rule generation from risky patterns
- `src/risk_pattern_analysis/pipeline.py`: orchestrates full analysis pipeline
- `src/risk_pattern_analysis/cli.py`: command-line entrypoint
- `app.py`: Streamlit dashboard UI
- `data/sample_signups.csv`: sample dataset for demonstration
- `outputs/`: generated artifacts after execution
- `docs/portfolio-version.md`: recruiter/interview narrative

## Risk Logic Snapshot
Behavioral signals include:
- IP and device velocity
- OTP failure intensity
- Disposable email indicator
- Proxy/VPN network indicator
- Country mismatch between phone and IP
- Session duration and navigation entropy anomalies

Decision tiers:
- `TIER_1_MONITOR`
- `TIER_2_CHALLENGE`
- `TIER_3_REVIEW`
- `TIER_4_BLOCK`

## Run Locally
```bash
cd "/Users/abhishekkumar/Documents/Risk pattern analyis"
./scripts/run_pipeline.sh
```

Alternative command:
```bash
PYTHONPATH=src python3 -m risk_pattern_analysis.cli \
  --input data/sample_signups.csv \
  --output outputs
```

## Launch Dashboard
Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

Run Streamlit app:
```bash
streamlit run app.py
```

## Generated Outputs
After running, the pipeline creates:
- `outputs/scored_signups.csv`: each signup enriched with features, score, and tier
- `outputs/generated_rules.md`: ranked candidate fraud rules
- `outputs/summary.json`: high-level processing and tier metrics

## Example Use Cases
- Demonstrating fraud-risk analytics approach in interviews
- Prototyping rule strategies before production rule-engine rollout
- Showing GenAI-assisted rule authoring workflow with human governance

## Professional Resume Entry
**Risk Pattern Analysis Using GenAI, Independent Project | Nov 2025 - Feb 2026**
- Built a fraud-risk analysis pipeline to detect and classify suspicious account creation behavior.
- Designed GenAI-assisted candidate rules from behavioral abuse patterns for preventive controls.
- Produced implementation-ready scoring tiers and governance outputs for engineering deployment.
