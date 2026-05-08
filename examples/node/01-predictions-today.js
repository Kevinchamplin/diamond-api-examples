// Print today's MLB predictions, sorted by confidence.
// Requires Node 18+ (native fetch).
const API = "https://diamond.champlinenterprises.com/api/v1";
const KEY = process.env.DIAMOND_KEY;

if (!KEY) {
  console.error("Set DIAMOND_KEY. Free key: https://diamond.champlinenterprises.com/signup.php");
  process.exit(1);
}

const res = await fetch(`${API}/predictions.php`, { headers: { "X-Api-Key": KEY } });
if (!res.ok) {
  console.error(`HTTP ${res.status}: ${await res.text()}`);
  process.exit(1);
}
const data = await res.json();

console.log(`\nDiamond AI — ${data.date} (${data.count} games, model v${data.model_version})\n`);
for (const p of [...data.predictions].sort((a, b) => b.confidence - a.confidence)) {
  const edge = p.value_edge ? `  edge ${p.value_edge >= 0 ? "+" : ""}${p.value_edge.toFixed(1)}%` : "";
  console.log(
    `  ${p.away_team.padStart(3)} @ ${p.home_team.padEnd(3)}  ` +
    `→ ${p.predicted_winner.padEnd(3)}  ${p.confidence}% (${p.confidence_level})${edge}`,
  );
}

const remaining = res.headers.get("x-ratelimit-remaining");
if (remaining !== null) console.log(`\n${remaining} API calls remaining today.`);
