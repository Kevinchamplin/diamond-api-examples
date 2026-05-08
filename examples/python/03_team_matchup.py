"""One-off matchup prediction with feature breakdown.

Usage:
    python 03_team_matchup.py NYY BOS
    python 03_team_matchup.py LAD ATL 2026
"""
import os
import sys
import requests

API = "https://diamond.champlinenterprises.com/api/v1"
KEY = os.environ.get("DIAMOND_KEY")
if not KEY:
    sys.exit("Set DIAMOND_KEY. Free key: https://diamond.champlinenterprises.com/signup.php")

if len(sys.argv) < 3:
    sys.exit("Usage: python 03_team_matchup.py <HOME> <AWAY> [season]")

home, away = sys.argv[1].upper(), sys.argv[2].upper()
params: dict = {"home": home, "away": away}
if len(sys.argv) >= 4:
    params["season"] = sys.argv[3]

r = requests.get(f"{API}/model.php", params=params, headers={"X-Api-Key": KEY}, timeout=10)
r.raise_for_status()
d = r.json()

m, p, f = d["matchup"], d["prediction"], d["features"]
print(f"\n{m['away']['name']} @ {m['home']['name']}")
print(f"  {m['home']['abbreviation']} Elo {m['home']['elo']:.1f} (mom {m['home']['momentum']:+.1f})")
print(f"  {m['away']['abbreviation']} Elo {m['away']['elo']:.1f} (mom {m['away']['momentum']:+.1f})")
print(f"\nPrediction: {p['predicted_winner']}  ({p['confidence']:.1f}% confidence)")
print(f"  P({m['home']['abbreviation']} win) = {p['home_win_probability']:.4f}")
print(f"  P({m['away']['abbreviation']} win) = {p['away_win_probability']:.4f}")
print("\nFeatures:")
print(f"  Elo diff:     {f['elo_diff']:+.1f}")
print(f"  Pitcher diff: {f['pitcher_diff']:+.2f}")
print(f"  Park adj:     {f['park_adj']:+.3f}")
