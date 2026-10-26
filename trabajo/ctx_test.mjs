import { readFileSync } from "fs";
const m = await import("/home/claude/proyecto/sitio/lib/context.js");
const env = { ASSETS: { fetch: async (req) => { const p = new URL(req.url).pathname; try { return new Response(readFileSync("/home/claude/proyecto/sitio/public" + p)); } catch (e) { return new Response("", { status: 404 }); } } } };
await m.ready(env, "https://x.test");
for (const q of ["Vivo en Béccar cuánta obra deciden los vecinos", "deuda nueva", "cuando se licita la recoleccion"]) {
  const c = m.context(q + " " + q);
  console.log(q, "|", c.text.length, "chars |", Object.entries(c.refs).slice(0, 5).map(([k, v]) => k + "=" + v).join(", "));
}
