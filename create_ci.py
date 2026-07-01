import pathlib

p = pathlib.Path('.github/workflows/ci.yml')
p.parent.mkdir(parents=True, exist_ok=True)

content = """name: CI

on:
  push:
    branches: [ main, cleanup/analyzer-warnings ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Analyze & Test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.44.4'
          channel: stable
          cache: true

      - name: Create .env for CI
        run: |
          echo "SUPABASE_URL=${{ secrets.SUPABASE_URL }}" >> .env
          echo "SUPABASE_ANON_KEY=${{ secrets.SUPABASE_ANON_KEY }}" >> .env
          echo "SENTRY_DSN=${{ secrets.SENTRY_DSN }}" >> .env

      - name: Install dependencies
        run: flutter pub get

      - name: Analyze
        run: flutter analyze --no-pub

      - name: Test
        run: flutter test --no-pub
"""

p.write_text(content, encoding='utf-8')
print(f"Created {p}")