from __future__ import annotations

from typing import Dict, List


def _to_int(value: str) -> int:
    return int(value) if value not in (None, "") else 0


def _to_float(value: str) -> float:
    return float(value) if value not in (None, "") else 0.0


def _to_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def build_features(row: Dict[str, str]) -> Dict[str, float]:
    """Build normalized fraud-risk features from a signup event row."""
    ip_velocity = _to_int(row.get("last_24h_signups_ip", "0"))
    device_velocity = _to_int(row.get("last_24h_signups_device", "0"))
    failed_otps = _to_int(row.get("failed_otps", "0"))
    session_duration = _to_float(row.get("session_duration_sec", "0"))
    nav_entropy = _to_float(row.get("navigation_entropy", "0"))

    ip_country = (row.get("ip_country") or "").strip().upper()
    phone_country = (row.get("phone_country") or "").strip().upper()

    features: Dict[str, float] = {
        "ip_velocity_high": 1.0 if ip_velocity >= 8 else 0.0,
        "ip_velocity_medium": 1.0 if 5 <= ip_velocity < 8 else 0.0,
        "device_velocity_high": 1.0 if device_velocity >= 6 else 0.0,
        "otp_failure_high": 1.0 if failed_otps >= 3 else 0.0,
        "short_session": 1.0 if session_duration < 35 else 0.0,
        "low_navigation_entropy": 1.0 if nav_entropy < 1.2 else 0.0,
        "disposable_email": 1.0 if _to_bool(row.get("is_disposable_email", "false")) else 0.0,
        "proxy_ip": 1.0 if _to_bool(row.get("is_proxy_ip", "false")) else 0.0,
        "geo_mismatch": 1.0 if ip_country and phone_country and ip_country != phone_country else 0.0,
    }
    return features


def feature_names() -> List[str]:
    return [
        "ip_velocity_high",
        "ip_velocity_medium",
        "device_velocity_high",
        "otp_failure_high",
        "short_session",
        "low_navigation_entropy",
        "disposable_email",
        "proxy_ip",
        "geo_mismatch",
    ]
