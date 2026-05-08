// Find today's value bets and post to Slack or Discord webhook.
// Set DIAMOND_KEY plus SLACK_WEBHOOK and/or DISCORD_WEBHOOK. Without webhooks, prints to stdout.
const API = "https://diamond.champlinenterprises.com/api/v1";
const { DIAMOND_KEY, SLACK_WEBHOOK, DISCORD_WEBHOOK, MIN_EDGE = "5" } = process.env;

if (!DIAMOND_KEY) {
  console.error("Set DIAMOND_KEY. Free key: https://diamond.champlinenterprises.com/signup.php");
  process.exit(1);
}

const url = new URL(`${API}/value-bets.php`);
url.searchParams.set("min_edge", MIN_EDGE);

const res = await fetch(url, { headers: { "X-Api-Key": DIAMOND_KEY } });
const data = await res.json();

const lines = [`*Diamond AI value bets — ${data.date}*`, ""];
if (!data.value_bets.length) {
  lines.push(`No value bets today above ${MIN_EDGE}% edge.`);
} else {
  for (const b of data.value_bets) {
    const side = b.value_side === "home" ? b.home_team : b.away_team;
    const sign = b.edge_pct >= 0 ? "+" : "";
    lines.push(
      `• \`${b.away_team} @ ${b.home_team}\`  → *${side}* — edge ${sign}${b.edge_pct.toFixed(1)}% (${b.rating})`,
    );
  }
}
if (data.disclaimer) lines.push(`\n_${data.disclaimer}_`);
const text = lines.join("\n");

const posts = [];
if (SLACK_WEBHOOK) posts.push(fetch(SLACK_WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }) }));
if (DISCORD_WEBHOOK) posts.push(fetch(DISCORD_WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ content: text }) }));

if (posts.length) {
  await Promise.all(posts);
  console.log("Posted.");
} else {
  console.log(text);
}
