// POST /api/contacto: el formulario «Escribinos». Guarda el mensaje para el panel privado; no manda mails.
import { json, guard, hashIp } from "../../lib/claude.js";

const MAX_TEXTO = 1500, MAX_MAIL = 120, POR_PERSONA = 5, POR_DIA = 300;
const UPSERT = "INSERT INTO hits (k, n, exp) VALUES (?1, 1, ?2) ON CONFLICT(k) DO UPDATE SET n = n + 1 RETURNING n";

export async function onRequestPost({ request, env }) {
  const blocked = await guard(request, env, { key: "msg", max: POR_PERSONA, code: "msg_limit" });
  if (blocked) return blocked;
  if (!env.DB) return json({ code: "not_configured" }, 503);
  let body;
  try { body = await request.json(); } catch (_) { return json({ code: "invalid_request" }, 400); }
  // Campo trampa: las personas no lo ven; los robots lo llenan.
  if (body && body.web) return json({ ok: true });
  const texto = String((body && body.texto) || "").trim();
  const mail = String((body && body.mail) || "").trim();
  const pagina = String((body && body.pagina) || "").slice(0, 40);
  if (texto.length < 3 || texto.length > MAX_TEXTO) return json({ code: "invalid_request" }, 400);
  if (mail && (mail.length > MAX_MAIL || !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(mail))) return json({ code: "bad_mail" }, 400);
  const now = Date.now();
  try {
    const g = await env.DB.prepare(UPSERT).bind("msgday:" + new Date(now - 3 * 3600000).toISOString().slice(0, 10), now + 3 * 86400000).all();
    if (g.results[0].n > POR_DIA) return json({ code: "msg_daily" }, 429);
    const conn = await hashIp(env.IP_SALT || "sanisidro2027", request.headers.get("CF-Connecting-IP") || "sin-ip");
    await env.DB.prepare("INSERT INTO mensajes (id, ts, conn, pagina, texto, mail) VALUES (?1, ?2, ?3, ?4, ?5, ?6)")
      .bind(crypto.randomUUID(), now, conn, pagina, texto, mail || null).run();
  } catch (_) { return json({ code: "upstream_error" }, 502); }
  return json({ ok: true });
}
