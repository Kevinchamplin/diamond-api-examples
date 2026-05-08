# Diamond AI — MLB Prediction API

Official examples and OpenAPI spec for the [Diamond AI](https://diamond.champlinenterprises.com) prediction API. Covers daily game predictions, team Elo rankings, value-bet detection, and accuracy tracking.

**The model:** logistic regression trained on 22,762 MLB games. **Validated accuracy: 56.5%** on held-out data, **55.4% live** across 381 in-season picks. Brier score 0.2468. Beats Vegas consensus (~56%) and coin-flip baseline by a measurable margin.

**Free tier:** 100 calls/day, no credit card. Get a key in 60 seconds at [diamond.champlinenterprises.com/signup.php](https://diamond.champlinenterprises.com/signup.php).

---

## Quickstart (curl)

```bash
export DIAMOND_KEY="your_api_key"
curl "https://diamond.champlinenterprises.com/api/v1/predictions.php?api_key=$DIAMOND_KEY"
```

That's it. Every endpoint is `GET`, returns JSON, and accepts the key as either `?api_key=` or an `X-Api-Key:` header.

## Quickstart (Python)

```python
import os, requests

key = os.environ["DIAMOND_KEY"]
r = requests.get(
    "https://diamond.champlinenterprises.com/api/v1/predictions.php",
    headers={"X-Api-Key": key},
)
for p in r.json()["predictions"]:
    print(f"{p['away_team']} @ {p['home_team']}: {p['predicted_winner']} ({p['confidence']}%)")
```

## Quickstart (Node)

```js
const key = process.env.DIAMOND_KEY;
const res = await fetch(
  "https://diamond.champlinenterprises.com/api/v1/predictions.php",
  { headers: { "X-Api-Key": key } },
);
const { predictions } = await res.json();
predictions.forEach(p =>
  console.log(`${p.away_team} @ ${p.home_team}: ${p.predicted_winner} (${p.confidence}%)`)
);
```

---

## What's in this repo

| Path | What it is |
|------|------------|
| [`openapi.yaml`](./openapi.yaml) | Full OpenAPI 3.1 spec — feed it to Postman, Insomnia, or generate clients in any language |
| [`examples/python/`](./examples/python) | Python: predictions, value-bet alerts, matchup tool, accuracy tracker |
| [`examples/node/`](./examples/node) | Node.js: predictions, value-bet alerts, matchup tool |
| [`examples/curl/`](./examples/curl) | One-liner curl recipes for every endpoint |

---

## Endpoints at a glance

| Endpoint | Returns |
|----------|---------|
| `GET /predictions.php` | All MLB games today (or `?date=`) with predicted winner, confidence, and value edge vs Vegas |
| `GET /model.php` | Single matchup prediction from team abbreviations (`?home=NYY&away=BOS`) |
| `GET /rankings.php` | All 30 teams ranked by Elo, with tier (`elite`/`contender`/...) and 5-game form |
| `GET /value-bets.php` | Today's games where the model disagrees with Vegas, sorted by edge % |
| `GET /accuracy.php` | Live model performance: accuracy, Brier score, calibration buckets, recent form |

Full reference: [diamond.champlinenterprises.com/api/v1/docs.php](https://diamond.champlinenterprises.com/api/v1/docs.php)

---

## Rate limits & tiers

| Tier | Daily calls | Price | Notes |
|------|-------------|-------|-------|
| Free | 100 | $0 | Daily predictions delayed 1hr; perfect for hobby projects |
| Pro | 1,000 | $99/mo | Real-time, value-bet alerts, Pitcher Power Index |
| Enterprise | Unlimited | Custom | Webhooks, raw probabilities + confidence intervals, full 22k-game backtest dataset, 99.9% SLA |

Pricing: [diamond.champlinenterprises.com/pricing.php](https://diamond.champlinenterprises.com/pricing.php).

Every response includes `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` (Unix timestamp; resets midnight CT).

---

## What people build with this

- **Daily picks bots** for Discord / Slack — see [`examples/python/02_value_bets_alert.py`](./examples/python/02_value_bets_alert.py)
- **Backtesting strategies** against the live confidence stream
- **Augmenting DFS lineup tools** with model-vs-Vegas edge
- **Spreadsheet imports** via Google Sheets `IMPORTDATA()` on the JSON endpoints
- **Streaming overlays** for live games using `/model.php` for win-probability snapshots

---

## Disclaimer

Predictions are for entertainment and informational purposes. Bet responsibly; past model accuracy does not guarantee future results.

## License

MIT — see [LICENSE](./LICENSE). Use the examples as starter code in commercial projects.
