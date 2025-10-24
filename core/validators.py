from datetime import date
from typing import Optional

# Lightweight pre-validation so we can enable/disable the button before creating the model

def all_required_present(
    *,
    date_value: Optional[date],
    stream: str,
    founder_name: str,
    venture_name: str,
    venture_manager_name: str,
    link: str,
    password: str,
) -> tuple[bool, list[str]]:
    missing: list[str] = []

    if date_value is None:
        missing.append("Date")
    if not stream or stream.strip() == "" or stream == "— Select —":
        missing.append("CDL Stream")
    if not founder_name.strip():
        missing.append("Founder name")
    if not venture_name.strip():
        missing.append("Venture name")
    if not venture_manager_name.strip():
        missing.append("Venture manager name")
    if not password.strip():
        missing.append("password")
    if not _looks_like_url(link):
        missing.append("Link (must be a valid URL)")

    return (len(missing) == 0, missing)


def _looks_like_url(s: str) -> bool:
    if not s:
        return False
    # Minimal check before Pydantic's strict HttpUrl: scheme + a dot in host
    s = s.strip()
    return s.startswith("http://") or s.startswith("https://")