// POST /api/ask: recibe sólo la pregunta (y las dos últimas idas y vueltas). El servidor busca él mismo los pasajes
// del programa, de las cuentas y de las investigaciones, así nadie puede mandarle textos largos ni usarlo para otra cosa.
import { json, guard, askClaude, logStart } from "../../lib/claude.js";
import { ready, context } from "../../lib/context.js";

const MAX_Q = 700, MAX_SEARCH = 1600, MAX_HIST = 6, MAX_HIST_CHARS = 3000;

function cleanHistory(raw) {
  if (raw == null) return [];
  if (!Array.isArray(raw) || raw.length > MAX_HIST) return null;
  const out = [];
  for (let i = 0; i < raw.length; i++) {
    const t = raw[i], role = i % 2 === 0 ? "user" : "assistant";
    if (!t || t.role !== role) return null;
    const content = String(t.content || "").trim();
    if (!content || content.length > MAX_HIST_CHARS) return null;
    out.push({ role, content });
  }
  if (out.length && out[out.length - 1].role !== "assistant") return null;
  return out;
}

export async function onRequestPost({ request, env, waitUntil }) {
  const blocked = await guard(request, env, { daily: true });
  if (blocked) return blocked;
  if (!env.ANTHROPIC_API_KEY) return json({ code: "not_configured" }, 503);
  let body;
  try { body = await request.json(); } catch (_) { return json({ code: "invalid_request" }, 400); }
  const q = String((body && body.question) || "").trim();
  if (!q || q.length > MAX_Q) return json({ code: "invalid_request" }, 400);
  const search = String((body && body.search) || q).slice(0, MAX_SEARCH);
  const hist = cleanHistory(body && body.history);
  if (hist === null) return json({ code: "invalid_request" }, 400);
  try { await ready(env, new URL(request.url).origin); } catch (_) { return json({ code: "upstream_error" }, 502); }
  const ctx = context(search);
  const id = await logStart(env, request, q);
  return askClaude(env, hist.concat([{ role: "user", content: ctx.text + "\nPREGUNTA DEL VECINO: " + q }]), ctx.refs, { id, waitUntil });
}
