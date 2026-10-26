// Funciones compartidas de «Preguntale al programa» (Cloudflare Pages Functions).
// La clave de Claude vive sólo acá, como secreto ANTHROPIC_API_KEY. Nunca llega al navegador.
import { RULES } from "./rules.js";

const API = "https://api.anthropic.com/v1/messages";
const DEFAULT_MODEL = "claude-sonnet-5-5";
const MAX_TURNS = 9;          // las reglas van aparte; esto es historia + pregunta
const MAX_TURN_CHARS = 52000; // un turno (los pasajes + la pregunta)
const MAX_TOTAL_CHARS = 72000;
const PER_IP = 40;            // preguntas por persona…
const WINDOW_MS = 10 * 60 * 1000; // …cada 10 minutos (aproximado: cuenta por servidor)

const seen = new Map();

export function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

async function hashIp(salt, ip) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(salt + ip));
  return [...new Uint8Array(b)].slice(0, 12).map((x) => x.toString(16).padStart(2, "0")).join("");
}
const UPSERT = "INSERT INTO hits (k, n, exp) VALUES (?1, 1, ?2) ON CONFLICT(k) DO UPDATE SET n = n + 1 RETURNING n";

// Protección: sólo desde la propia página, un límite por conexión (60 por hora) y un total por día para cuidar los créditos.
// La conexión se guarda como un código irreversible (hash), nunca la dirección real.
export async function guard(request, env, opts = {}) {
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
  if (env && env.DB) {
    try {
      const h = await hashIp(env.IP_SALT || "sanisidro2027", ip);
      const stmts = [env.DB.prepare(UPSERT).bind("ip:" + h + ":" + Math.floor(now / 3600000), now + 2 * 3600000)];
      if (opts.daily) stmts.push(env.DB.prepare(UPSERT).bind("day:" + new Date(now - 3 * 3600000).toISOString().slice(0, 10), now + 3 * 86400000));
      const res = await env.DB.batch(stmts);
      if (res[0].results[0].n > (+env.PER_IP_HOUR || 60)) return json({ code: "rate_limited" }, 429);
      if (opts.daily && res[1].results[0].n > (+env.DAILY_CAP || 500)) return json({ code: "daily_limit" }, 429);
      if (Math.random() < 0.01) await env.DB.prepare("DELETE FROM hits WHERE exp < ?1").bind(now).run();
    } catch (_) {
      // Si la base de datos falla, sigue funcionando con el límite en memoria.
    }
  }
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
  // El tope de gasto (el que se pone en la consola de Claude) o los créditos del mes: el chat avisa que llegó a su límite
  if (/credit|billing|balance|usage limit|spend limit|enforced_spend_limit/i.test(text)) return json({ code: "no_credits" }, 402);
  if (res.status === 429 || res.status === 529) return json({ code: "rate_limited" }, 429);
  return json({ code: "upstream_error" }, 502);
}

export async function askClaude(env, messages, refs) {
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
      // Sin pensar antes de responder (no hace falta para leer pasajes) y con esfuerzo medio: la respuesta es igual de buena y cuesta mucho menos.
      thinking: { type: env.THINKING || "between_tools" },
      output_config: { effort: env.EFFORT || "medium" },
      system: RULES,
      messages,
      stream: true,
    }),
  });
  if (!res.ok) return upstreamError(res);
  // Primero le dice a la página qué pasaje es cada código (P1, I2…), para que las fuentes salgan bien.
  const { readable, writable } = new TransformStream();
  (async () => {
    const w = writable.getWriter();
    await w.write(new TextEncoder().encode("data: " + JSON.stringify({ type: "refs", refs: refs || {} }) + "\n\n"));
    w.releaseLock();
    await res.body.pipeTo(writable);
  })().catch(() => {});
  return new Response(readable, {
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
      thinking: { type: "between_tools" },
      output_config: { effort: "low" },
      system: "Traducí al castellano rioplatense la pregunta que te pasan. Respondé sólo con la traducción, sin nada más.",
      messages: [{ role: "user", content: text }],
    }),
  });
  if (!res.ok) return upstreamError(res);
  const data = await res.json();
  const es = (data.content || []).filter((b) => b.type === "text").map((b) => b.text).join("").trim();
  return json({ es });
}
