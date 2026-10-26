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

export async function hashIp(salt, ip) {
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
      const day = new Date(now - 3 * 3600000).toISOString().slice(0, 10);
      const stmts = [env.DB.prepare(UPSERT).bind("ip:" + h + ":" + Math.floor(now / 3600000), now + 2 * 3600000)];
      if (opts.daily) stmts.push(env.DB.prepare(UPSERT).bind("pday:" + h + ":" + day, now + 2 * 86400000));
      const res = await env.DB.batch(stmts);
      if (res[0].results[0].n > (+env.PER_IP_HOUR || 60)) return json({ code: "rate_limited" }, 429);
      if (opts.daily && res[1].results[0].n > (+env.PER_IP_DAY || 100)) return json({ code: "person_daily_limit" }, 429);
      // El tope del día para todos sólo cuenta las preguntas que pasaron los topes por persona:
      // así alguien que insiste no puede gastar el cupo de los demás.
      if (opts.daily) {
        const g = await env.DB.prepare(UPSERT).bind("day:" + day, now + 3 * 86400000).all();
        if (g.results[0].n > (+env.DAILY_CAP || 500)) return json({ code: "daily_limit" }, 429);
      }
      if (opts.key) {
        const k = await env.DB.prepare(UPSERT).bind(opts.key + ":" + h + ":" + day, now + 2 * 86400000).all();
        if (k.results[0].n > opts.max) return json({ code: opts.code || "person_daily_limit" }, 429);
      }
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

// Aprendizaje: guarda la pregunta y la respuesta, sin datos de la persona (sólo un código irreversible de la conexión).
export async function logStart(env, request, q) {
  if (!env.DB) return null;
  try {
    const id = crypto.randomUUID();
    const conn = await hashIp(env.IP_SALT || "sanisidro2027", request.headers.get("CF-Connecting-IP") || "sin-ip");
    let pagina = "";
    try { pagina = new URL(request.headers.get("Referer") || "").pathname.slice(0, 40); } catch (_) {}
    await env.DB.prepare("INSERT INTO preguntas (id, ts, conn, pagina, pregunta) VALUES (?1, ?2, ?3, ?4, ?5)").bind(id, Date.now(), conn, pagina, q.slice(0, 700)).run();
    return id;
  } catch (_) { return null; }
}
async function logEnd(env, id, text, truncated, refs) {
  if (!env.DB || !id) return;
  const main = text.split(/\n\s*FUENTES\s*:/i)[0].trim();
  const f = (text.match(/FUENTES\s*:\s*([^\n]*)/i) || [])[1] || "";
  const fuentes = (f.match(/[PI]\d+/gi) || []).map((c) => (refs || {})[c.toUpperCase()] || c).join(" ");
  const sinDato = /no habla de|no trae (esa|ese|esta|este|eso|ningun)|no tiene (ninguna|datos|información)|no hay ninguna propuesta|no lo trata|no dice nada sobre|no menciona/i.test(main) ? 1 : 0;
  try {
    await env.DB.prepare("UPDATE preguntas SET respuesta = ?1, fuentes = ?2, sin_dato = ?3, cortada = ?4 WHERE id = ?5").bind(main.slice(0, 4000), fuentes.slice(0, 400), sinDato, truncated ? 1 : 0, id).run();
  } catch (_) {}
}

export async function askClaude(env, messages, refs, log) {
  const res = await fetch(env.ANTHROPIC_BASE || API, {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: env.MODEL || DEFAULT_MODEL,
      max_tokens: 3000,
      // Piensa antes de responder cuando hace falta (Nick, 12 de octubre: respeta mejor las reglas; cuesta un 12% más).
      // El tope de 3.000 tokens deja lugar para pensar y responder sin que se corte.
      thinking: { type: "adaptive" },
      output_config: { effort: "high" },
      system: RULES,
      messages,
      stream: true,
    }),
  });
  if (!res.ok) return upstreamError(res);
  // Primero le dice a la página qué pasaje es cada código (P1, I2…) y el número de la pregunta; después pasa la respuesta tal cual.
  const { readable, writable } = new TransformStream();
  const job = (async () => {
    const w = writable.getWriter(), enc = new TextEncoder(), dec = new TextDecoder();
    await w.write(enc.encode("data: " + JSON.stringify({ type: "refs", refs: refs || {}, qid: (log && log.id) || null }) + "\n\n"));
    const reader = res.body.getReader();
    let buf = "", text = "", truncated = false;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      await w.write(value);
      buf += dec.decode(value, { stream: true });
      const parts = buf.split(/\r?\n\r?\n/); buf = parts.pop();
      for (const ev of parts) {
        const data = ev.split("\n").filter((l) => l.startsWith("data:")).map((l) => l.slice(5).trim()).join("");
        if (!data) continue;
        try {
          const j = JSON.parse(data);
          if (j.type === "content_block_delta" && j.delta && j.delta.type === "text_delta") text += j.delta.text;
          if (j.type === "message_delta" && j.delta && j.delta.stop_reason === "max_tokens") truncated = true;
        } catch (_) {}
      }
    }
    await w.close();
    if (log && log.id) await logEnd(env, log.id, text, truncated, refs);
  })().catch(() => {});
  if (log && log.waitUntil) log.waitUntil(job);
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
