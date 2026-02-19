from __future__ import annotations

from typing import Dict, Tuple

FEATURE_WEIGHTS = {
    "ip_velocity_high": 18,
    "ip_velocity_medium": 8,
    "device_velocity_high": 16,
    "otp_failure_high": 14,
    "short_session": 10,
    "low_navigation_entropy": 7,
    "disposable_email": 12,
    "proxy_ip": 9,
    "geo_mismatch": 6,
}


def score_signup(features: Dict[str, float]) -> Tuple[int, str]:
    raw = 0.0
    for name, weight in FEATURE_WEIGHTS.items():
        raw += features.get(name, 0.0) * weight

    score = min(int(round(raw)), 100)

    if score >= 60:
        tier = "TIER_4_BLOCK"
    elif score >= 38:
        tier = "TIER_3_REVIEW"
    elif score >= 20:
        tier = "TIER_2_CHALLENGE"
    else:
        tier = "TIER_1_MONITOR"

    return score, tier
