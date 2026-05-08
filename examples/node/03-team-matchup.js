// One-off matchup prediction with feature breakdown.
// Usage: node 03-team-matchup.js NYY BOS [season]
const API = "https://diamond.champlinenterprises.com/api/v1";
const KEY = process.env.DIAMOND_KEY;

if (!KEY) {
  console.error("Set DIAMOND_KEY. Free key: https://diamond.champlinenterprises.com/signup.php");
  process.exit(1);
}
if (process.argv.length < 4) {
  console.error("Usage: node 03-team-matchup.js <HOME> <AWAY> [season]");
  process.exit(1);
}

const [home, away, season] = process.argv.slice(2);
const url = new URL(`${API}/model.php`);
url.searchParams.set("home", home.toUpperCase());
url.searchParams.set("away", away.toUpperCase());
if (season) url.searchParams.set("season", season);

const res = await fetch(url, { headers: { "X-Api-Key": KEY } });
const d = await res.json();
const { matchup: m, prediction: p, features: f } = d;

console.log(`\n${m.away.name} @ ${m.home.name}`);
console.log(`  ${m.home.abbreviation} Elo ${m.home.elo.toFixed(1)} (mom ${m.home.momentum >= 0 ? "+" : ""}${m.home.momentum.toFixed(1)})`);
console.log(`  ${m.away.abbreviation} Elo ${m.away.elo.toFixed(1)} (mom ${m.away.momentum >= 0 ? "+" : ""}${m.away.momentum.toFixed(1)})`);
console.log(`\nPrediction: ${p.predicted_winner}  (${p.confidence.toFixed(1)}% confidence)`);
console.log(`  P(${m.home.abbreviation} win) = ${p.home_win_probability.toFixed(4)}`);
console.log(`  P(${m.away.abbreviation} win) = ${p.away_win_probability.toFixed(4)}`);
console.log("\nFeatures:");
console.log(`  Elo diff:     ${f.elo_diff >= 0 ? "+" : ""}${f.elo_diff.toFixed(1)}`);
console.log(`  Pitcher diff: ${f.pitcher_diff >= 0 ? "+" : ""}${f.pitcher_diff.toFixed(2)}`);
console.log(`  Park adj:     ${f.park_adj >= 0 ? "+" : ""}${f.park_adj.toFixed(3)}`);
