"""Pull live model accuracy + recent form. Suitable as a daily cron / monitoring check."""
import os
import sys
import requests

API = "https://diamond.champlinenterprises.com/api/v1"
KEY = os.environ.get("DIAMOND_KEY")
if not KEY:
    sys.exit("Set DIAMOND_KEY. Free key: https://diamond.champlinenterprises.com/signup.php")

r = requests.get(f"{API}/accuracy.php", headers={"X-Api-Key": KEY}, timeout=10)
r.raise_for_status()
d = r.json()

o, b = d["overall"], d["benchmarks"]
print(f"\nDiamond AI — season {d['season']} accuracy")
print(f"  Predictions: {o['total_predictions']}")
print(f"  Correct:     {o['correct']}")
print(f"  Accuracy:    {o['accuracy_pct']:.1f}%   (vs Vegas {b['vegas_consensus']}%, coin flip {b['coin_flip']}%)")
print(f"  Brier:       {o['brier_score']:.4f}   (lower is better; <0.25 is calibrated)")

print("\nCalibration buckets:")
for c in d["calibration"]:
    print(f"  {c['bucket']:>6}%  →  actual {c['actual_win_pct']:5.1f}%  (n={c['predictions']})")

print("\nRecent 7 days:")
for r_ in d["recent_form"][:7]:
    print(f"  {r_['date']}: {r_['correct']:>2}/{r_['games']:>2}  {r_['accuracy_pct']:5.1f}%")
