// Funciones compartidas de «Preguntale al programa» (Cloudflare Pages Functions).
// La clave de Claude vive sólo acá, como secreto ANTHROPIC_API_KEY. Nunca llega al navegador.
import { RULES } from "./rules.js";

const API = "https://api.anthropic.com/v1/messages";
const DEFAULT_MODEL = "claude-sonnet-5-5";
const MAX_TURNS = 9;          // las reglas van aparte; esto es historia + pregunta
const MAX_TURN_CHARS = 52000; // un turno (los pasajes + la pregunta)
const MAX_TOTAL_CHARS = 72000;
const PER_IP = 12;            // preguntas por persona…
const WINDOW_MS = 10 * 60 * 1000; // …cada 10 minutos (aproximado: cuenta por servidor)

const seen = new Map();

export function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

export function guard(request) {
  const url = new URL(request.url);
  const origin = request.headers.get("Origin");
  if (!origin) return json({ code: "forbidden" }, 403);
  try {
    if (new URL(origin).host !== url.host) return json({ code: "forbidden" }, 403);
  } catch (_) {
    return json({ code: "forbidden" }, 403);
  }
  const ip = request.headers.get("CF-Connecting-IP") || "sin-ip";
  const now = Date.now();
  const list = (seen.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (list.length >= PER_IP) return json({ code: "rate_limited" }, 429);
  list.push(now);
  seen.set(ip, list);
  if (seen.size > 5000) seen.clear();
  return null;
}

export function cleanMessages(raw) {
  if (!Array.isArray(raw) || raw.length === 0 || raw.length > MAX_TURNS) return null;
  let total = 0;
  const out = [];
  for (const t of raw) {
    if (!t || (t.role !== "user" && t.role !== "assistant")) return null;
    const content = String(t.content || "").trim();
    if (!content || content.length > MAX_TURN_CHARS) return null;
    total += content.length;
    out.push({ role: t.role, content });
  }
  if (total > MAX_TOTAL_CHARS) return null;
  if (out[0].role !== "user" || out[out.length - 1].role !== "user") return null;
  return out;
}

async function upstreamError(res) {
  let text = "";
  try { text = await res.text(); } catch (_) {}
  if (res.status === 429 || res.status === 529) return json({ code: "rate_limited" }, 429);
  if (/credit|billing|balance/i.test(text)) return json({ code: "no_credits" }, 402);
  return json({ code: "upstream_error" }, 502);
}

export async function askClaude(env, messages) {
  const res = await fetch(env.ANTHROPIC_BASE || API, {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: env.MODEL || DEFAULT_MODEL,
      max_tokens: 1400,
      system: RULES,
      messages,
      stream: true,
    }),
  });
  if (!res.ok) return upstreamError(res);
  return new Response(res.body, {
    headers: { "content-type": "text/event-stream; charset=utf-8", "cache-control": "no-store" },
  });
}

export async function translate(env, text) {
  const res = await fetch(env.ANTHROPIC_BASE || API, {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: env.MODEL_QUICK || env.MODEL || DEFAULT_MODEL,
      max_tokens: 200,
      system: "Traducí al castellano rioplatense la pregunta que te pasan. Respondé sólo con la traducción, sin nada más.",
      messages: [{ role: "user", content: text }],
    }),
  });
  if (!res.ok) return upstreamError(res);
  const data = await res.json();
  const es = (data.content || []).filter((b) => b.type === "text").map((b) => b.text).join("").trim();
  return json({ es });
}
