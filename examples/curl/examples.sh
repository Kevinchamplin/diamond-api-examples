#!/usr/bin/env bash
# Diamond AI — curl recipes for every endpoint.
# Usage: DIAMOND_KEY=xxx ./examples.sh

: "${DIAMOND_KEY:?Set DIAMOND_KEY. Free key: https://diamond.champlinenterprises.com/signup.php}"
API="https://diamond.champlinenterprises.com/api/v1"

echo "=== Today's predictions ==="
curl -s "$API/predictions.php" -H "X-Api-Key: $DIAMOND_KEY" | jq '.predictions | length, .predictions[0]'

echo
echo "=== Single matchup: NYY (home) vs BOS (away) ==="
curl -s "$API/model.php?home=NYY&away=BOS" -H "X-Api-Key: $DIAMOND_KEY" | jq

echo
echo "=== Top 5 teams by Elo ==="
curl -s "$API/rankings.php" -H "X-Api-Key: $DIAMOND_KEY" | jq '.rankings[:5]'

echo
echo "=== Today's value bets (5%+ edge) ==="
curl -s "$API/value-bets.php?min_edge=5" -H "X-Api-Key: $DIAMOND_KEY" | jq

echo
echo "=== Live accuracy snapshot ==="
curl -s "$API/accuracy.php" -H "X-Api-Key: $DIAMOND_KEY" | jq '.overall, .benchmarks'
