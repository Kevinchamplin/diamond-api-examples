# Python Examples

Each script is standalone — copy, set `DIAMOND_KEY`, run.

## Setup

```bash
pip install -r requirements.txt
export DIAMOND_KEY="your_key_from_signup.php"
```

## Scripts

| Script | What it does |
|--------|--------------|
| `01_predictions_today.py` | Print today's MLB games with predicted winner and confidence |
| `02_value_bets_alert.py` | Find games with 5%+ edge vs Vegas, format as a Slack/Discord webhook payload |
| `03_team_matchup.py` | One-off matchup prediction (e.g. NYY vs BOS) with feature breakdown |
| `04_track_accuracy.py` | Pull live accuracy + recent form, useful as a daily monitoring cron |
