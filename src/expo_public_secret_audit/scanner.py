from __future__ import annotations

from dataclasses import dataclass
import re


PUBLIC_ASSIGNMENT = re.compile(r"^\s*(EXPO_PUBLIC_[A-Z0-9_]+)\s*=")

ALLOWED_PUBLIC_NAMES = {
    "EXPO_PUBLIC_FIREBASE_API_KEY",
    "EXPO_PUBLIC_FIREBASE_PROJECT_ID",
    "EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET",
    "EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID",
    "EXPO_PUBLIC_FIREBASE_APP_ID",
    "EXPO_PUBLIC_FIREBASE_MEASUREMENT_ID",
    "EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID",
    "EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID",
    "EXPO_PUBLIC_GOOGLE_ANDROID_CLIENT_ID",
    "EXPO_PUBLIC_WEATHER_API_KEY",
    "EXPO_PUBLIC_IOS_BUNDLE_ID",
}

RISKY_MARKERS = (
    "SECRET",
    "TOKEN",
    "PRIVATE",
    "OPENAI",
    "VUXO",
    "PHOTOROOM",
    "REMOVE_BG",
    "STRIPE_SECRET",
)


@dataclass(frozen=True)
class Finding:
    source: str
    line: int
    name: str
    reason: str


def is_risky_public_name(name: str) -> bool:
    if name in ALLOWED_PUBLIC_NAMES:
        return False
    return any(marker in name for marker in RISKY_MARKERS)


def scan_text(text: str, *, source: str = "<text>") -> list[Finding]:
    findings: list[Finding] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("#"):
            continue

        match = PUBLIC_ASSIGNMENT.match(line)
        if not match:
            continue

        name = match.group(1)
        if is_risky_public_name(name):
            findings.append(
                Finding(
                    source=source,
                    line=line_number,
                    name=name,
                    reason="EXPO_PUBLIC values are bundled into the client app",
                )
            )

    return findings
