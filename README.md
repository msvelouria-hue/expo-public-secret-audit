# Expo Public Secret Audit

A tiny Python CLI that scans Expo `.env` and config files for risky public secret exposure.

Expo bundles `EXPO_PUBLIC_*` values into the client app. That is fine for Firebase client config and OAuth client IDs, but dangerous for provider secrets such as OpenAI, Vuxo, PhotoRoom, Stripe secret keys, tokens, and private API keys.

The scanner also flags committed Google/Firebase API-key-looking values in app config files, such as static values inside `app.json`. Those values should be loaded from local environment variables during builds and restricted/rotated if they were exposed publicly.

## Why I Made This

I ran into the practical question of which Expo environment variables are safe to expose. This tool captures that lesson in a small, testable script.

## Local Development

```bash
git clone <repository-url>
cd expo-public-secret-audit
python3 -m unittest discover -s tests
```

## Usage

```bash
python3 -m expo_public_secret_audit .env .env.example app.json app.config.js
```

The command exits with status `1` if it finds risky public-prefixed names or committed API-key-looking values.

## Allowed Public Names

The scanner allows common Expo-safe public names such as:

- `EXPO_PUBLIC_FIREBASE_API_KEY`
- `EXPO_PUBLIC_FIREBASE_PROJECT_ID`
- `EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID`
- `EXPO_PUBLIC_WEATHER_API_KEY`

Everything else with secret-like words such as `SECRET`, `TOKEN`, `PRIVATE`, `OPENAI`, `VUXO`, `PHOTOROOM`, or `STRIPE_SECRET` is flagged.

## Static Config Checks

The scanner flags Google/Firebase API-key-looking values in committed config files so an `app.json` entry like a hardcoded Firebase API key is caught before GitHub secret scanning has to complain.

## License

MIT.
