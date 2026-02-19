from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
from typing import Dict, List

from .feature_engineering import build_features, feature_names
from .rule_generator import suggest_rules
from .scoring import score_signup


def _read_rows(input_csv: Path) -> List[Dict[str, str]]:
    with input_csv.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(rows: List[Dict[str, str]], path: Path) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_pipeline(input_csv: str, output_dir: str) -> Dict[str, float]:
    input_path = Path(input_csv)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    base_rows = _read_rows(input_path)
    names = feature_names()
    scored_rows: List[Dict[str, str]] = []

    for row in base_rows:
        feats = build_features(row)
        score, tier = score_signup(feats)
        enriched = dict(row)
        for n in names:
            enriched[n] = f"{feats[n]:.0f}"
        enriched["risk_score"] = str(score)
        enriched["risk_tier"] = tier
        scored_rows.append(enriched)

    scored_rows.sort(key=lambda r: int(r["risk_score"]), reverse=True)
    _write_csv(scored_rows, out_path / "scored_signups.csv")

    rules = suggest_rules(scored_rows, names)
    (out_path / "generated_rules.md").write_text("\n".join(rules) + "\n", encoding="utf-8")

    scores = [int(r["risk_score"]) for r in scored_rows]
    block_count = sum(1 for r in scored_rows if r["risk_tier"] == "TIER_4_BLOCK")
    review_count = sum(1 for r in scored_rows if r["risk_tier"] == "TIER_3_REVIEW")
    challenge_count = sum(1 for r in scored_rows if r["risk_tier"] == "TIER_2_CHALLENGE")
    monitor_count = sum(1 for r in scored_rows if r["risk_tier"] == "TIER_1_MONITOR")

    summary = {
        "records_processed": len(scored_rows),
        "average_risk_score": round(mean(scores), 2) if scores else 0.0,
        "tier_4_block_count": block_count,
        "tier_3_review_count": review_count,
        "tier_2_challenge_count": challenge_count,
        "tier_1_monitor_count": monitor_count,
        "highest_risk_event_id": scored_rows[0]["event_id"] if scored_rows else None,
    }
    (out_path / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary
