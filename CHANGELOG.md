# Changelog

All notable changes to this repository.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Entries use the `[Xh]` time-tracking marker scanned by the autorecon parser across all Champlin Enterprises projects.

## [Unreleased]

### Added (2026-05-08, repo-scaffold) [2h]

- Initial public scaffold — README with hero (56.5% validated / 22,762-game training set / 55.4% live / Brier 0.2468), 5-line quickstart in curl, Python, and Node.
- OpenAPI 3.1 spec covering all 5 v1 endpoints (`/predictions`, `/model`, `/rankings`, `/value-bets`, `/accuracy`), security schemes for both `X-Api-Key` header and `?api_key=` query param, and full response schemas including calibration buckets.
- Python examples: `01_predictions_today.py`, `02_value_bets_alert.py` (Slack/Discord webhook ready), `03_team_matchup.py`, `04_track_accuracy.py`. Single dependency: `requests`.
- Node 18+ examples mirroring the Python set, native `fetch`, no dependencies.
- curl one-liners for every endpoint at `examples/curl/examples.sh`.
- MIT license, `.gitignore`, `.env.example`.
- GitHub repo metadata: 12 topics (mlb, baseball, api, sports-data, sports-betting, predictions, elo, machine-learning, openapi, python, nodejs, dfs), homepage set to `https://diamond.champlinenterprises.com`.
