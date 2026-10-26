// POST /api/feedback: guarda lo que la persona esperaba encontrar en una respuesta («¿Le faltó algo?»). Sin datos de la persona.
import { json, guard } from "../../lib/claude.js";

export async function onRequestPost({ request, env }) {
  const blocked = await guard(request, env, {});
  if (blocked) return blocked;
  if (!env.DB) return json({ code: "not_configured" }, 503);
  let body;
  try { body = await request.json(); } catch (_) { return json({ code: "invalid_request" }, 400); }
  const id = String((body && body.qid) || "");
  const texto = String((body && body.texto) || "").trim();
  if (!/^[0-9a-f-]{36}$/.test(id) || !texto || texto.length > 800) return json({ code: "invalid_request" }, 400);
  try {
    await env.DB.prepare("UPDATE preguntas SET feedback = ?1, feedback_ts = ?2 WHERE id = ?3 AND feedback IS NULL").bind(texto, Date.now(), id).run();
  } catch (_) { return json({ code: "upstream_error" }, 502); }
  return json({ ok: true });
}
