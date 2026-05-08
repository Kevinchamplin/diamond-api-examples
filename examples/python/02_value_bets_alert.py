"""Find today's value bets and post them to a Slack or Discord webhook.

Set DIAMOND_KEY (required) and either SLACK_WEBHOOK or DISCORD_WEBHOOK.
With no webhook configured, results print to stdout.

Run as a daily cron at ~10am CT to catch lineup-adjusted picks before first pitch.
"""
import os
import sys
import requests

API = "https://diamond.champlinenterprises.com/api/v1"
KEY = os.environ.get("DIAMOND_KEY")
SLACK = os.environ.get("SLACK_WEBHOOK")
DISCORD = os.environ.get("DISCORD_WEBHOOK")
MIN_EDGE = float(os.environ.get("MIN_EDGE", "5"))

if not KEY:
    sys.exit("Set DIAMOND_KEY. Free key: https://diamond.champlinenterprises.com/signup.php")


def fetch_value_bets() -> dict:
    r = requests.get(
        f"{API}/value-bets.php",
        params={"min_edge": MIN_EDGE},
        headers={"X-Api-Key": KEY},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def format_message(data: dict) -> str:
    if not data["value_bets"]:
        return f"No value bets today ({data['date']}) above {MIN_EDGE}% edge."

    lines = [f"*Diamond AI value bets — {data['date']}*", ""]
    for b in data["value_bets"]:
        side = b["home_team"] if b["value_side"] == "home" else b["away_team"]
        lines.append(
            f"• `{b['away_team']} @ {b['home_team']}`  "
            f"→ *{side}* — edge {b['edge_pct']:+.1f}% ({b['rating']})"
        )
    lines.append(f"\n_{data.get('disclaimer', '')}_")
    return "\n".join(lines)


def post(text: str) -> None:
    if SLACK:
        requests.post(SLACK, json={"text": text}, timeout=10).raise_for_status()
    if DISCORD:
        requests.post(DISCORD, json={"content": text}, timeout=10).raise_for_status()
    if not (SLACK or DISCORD):
        print(text)


if __name__ == "__main__":
    post(format_message(fetch_value_bets()))
