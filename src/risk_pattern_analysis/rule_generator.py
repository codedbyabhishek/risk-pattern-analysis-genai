from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List


RULE_TEXT = {
    "ip_velocity_high": "If last_24h_signups_ip >= 8, raise high-velocity risk flag.",
    "device_velocity_high": "If last_24h_signups_device >= 6, mark as likely coordinated device reuse.",
    "otp_failure_high": "If failed_otps >= 3 during onboarding, escalate for review.",
    "disposable_email": "If disposable email domain detected, add identity-quality penalty.",
    "proxy_ip": "If proxy/VPN signal is true and velocity is elevated, require challenge.",
    "geo_mismatch": "If phone_country and ip_country mismatch and other indicators exist, increase risk tier.",
    "short_session": "If session_duration_sec < 35 with low entropy, classify as automation-like flow.",
    "low_navigation_entropy": "If navigation entropy is low across steps, add bot-likelihood weight.",
}


def suggest_rules(scored_rows: Iterable[Dict[str, str]], feature_names: List[str]) -> List[str]:
    """
    Generate prioritized candidate rules from fraud-labeled rows.
    This simulates a GenAI output layer with deterministic logic.
    """
    counts = defaultdict(float)
    fraud_total = 0.0

    for row in scored_rows:
        if str(row.get("label", "")).strip() == "1":
            fraud_total += 1
            for feat in feature_names:
                counts[feat] += float(row.get(feat, 0))

    if fraud_total == 0:
        ordered = feature_names[:5]
    else:
        ordered = sorted(feature_names, key=lambda n: counts[n] / fraud_total, reverse=True)[:6]

    lines = [
        "# Generated Candidate Rules",
        "",
        "These rules are generated from observed high-risk feature prevalence.",
        "",
    ]
    for idx, feat in enumerate(ordered, start=1):
        lines.append(f"{idx}. {RULE_TEXT.get(feat, feat)}")

    lines.append("")
    lines.append("## Governance Notes")
    lines.append("- Validate precision/recall before production rollout.")
    lines.append("- Enable versioning and rollback for all rule changes.")
    lines.append("- Track false positives by channel and segment.")

    return lines
