"""Print today's MLB predictions sorted by confidence."""
import os
import sys
import requests

API = "https://diamond.champlinenterprises.com/api/v1"
KEY = os.environ.get("DIAMOND_KEY")
if not KEY:
    sys.exit("Set DIAMOND_KEY env var. Get a free key at https://diamond.champlinenterprises.com/signup.php")


def main() -> None:
    r = requests.get(f"{API}/predictions.php", headers={"X-Api-Key": KEY}, timeout=10)
    r.raise_for_status()
    data = r.json()

    print(f"\nDiamond AI — {data['date']} ({data['count']} games, model v{data['model_version']})\n")
    for p in sorted(data["predictions"], key=lambda x: -x["confidence"]):
        edge = f"  edge {p['value_edge']:+.1f}%" if p.get("value_edge") else ""
        print(
            f"  {p['away_team']:>3} @ {p['home_team']:<3}  "
            f"→ {p['predicted_winner']:<3}  "
            f"{p['confidence']}% ({p['confidence_level']}){edge}"
        )

    remaining = r.headers.get("X-RateLimit-Remaining")
    if remaining is not None:
        print(f"\n{remaining} API calls remaining today.")


if __name__ == "__main__":
    main()
