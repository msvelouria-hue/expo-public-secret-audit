from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from expo_public_secret_audit.scanner import is_risky_public_name, scan_text


class ScannerTests(unittest.TestCase):
    def test_allows_known_public_client_config(self) -> None:
        self.assertFalse(is_risky_public_name("EXPO_PUBLIC_FIREBASE_API_KEY"))
        self.assertFalse(is_risky_public_name("EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID"))

    def test_flags_provider_secrets(self) -> None:
        self.assertTrue(is_risky_public_name("EXPO_PUBLIC_OPENAI_API_KEY"))
        self.assertTrue(is_risky_public_name("EXPO_PUBLIC_VUXO_API_KEY"))
        self.assertTrue(is_risky_public_name("EXPO_PUBLIC_REMOVE_BG_API_KEY"))

    def test_scan_text_ignores_comments(self) -> None:
        findings = scan_text(
            "\n".join(
                [
                    "# EXPO_PUBLIC_OPENAI_API_KEY=commented",
                    "EXPO_PUBLIC_FIREBASE_API_KEY=public",
                    "EXPO_PUBLIC_OPENAI_API_KEY=secret",
                ]
            ),
            source=".env",
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line, 3)
        self.assertEqual(findings[0].name, "EXPO_PUBLIC_OPENAI_API_KEY")

    def test_scan_text_flags_google_api_key_values_in_app_config(self) -> None:
        fake_key = "AI" + "za" + ("A" * 35)
        findings = scan_text(
            "\n".join(
                [
                    '{',
                    f'  "FIREBASE_API_KEY": "{fake_key}",',
                    '}',
                ]
            ),
            source="app.json",
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line, 2)
        self.assertEqual(findings[0].name, "GOOGLE_API_KEY_VALUE")


if __name__ == "__main__":
    unittest.main()
