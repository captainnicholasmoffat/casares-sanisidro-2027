// GET /api/panel/datos?dias=7|30|0: lo que pregunta la gente, para el panel privado.
import { json } from "../../../lib/claude.js";
import { accessEmail } from "../../../lib/access.js";

const DIA = 86400000;
export async function onRequestGet({ request, env }) {
  const email = await accessEmail(request, env);
  if (!email) return json({ code: "forbidden" }, 403);
  if (!env.DB) return json({ code: "not_configured" }, 503);
  const dias = Math.max(0, Math.min(3650, parseInt(new URL(request.url).searchParams.get("dias") || "30", 10) || 0));
  const desde = dias ? Date.now() - dias * DIA : 0;
  const q = (sql, ...b) => env.DB.prepare(sql).bind(...b);
  const [tot, sinDato, fb, todas, fuentes, ret, msgs, msgRet] = await env.DB.batch([
    q("SELECT COUNT(*) AS n, COALESCE(SUM(sin_dato),0) AS sd, COALESCE(SUM(cortada),0) AS ct, COALESCE(SUM(feedback IS NOT NULL),0) AS fb, COUNT(DISTINCT conn) AS personas FROM preguntas WHERE ts >= ?1", desde),
    q("SELECT id, ts, pregunta, respuesta FROM preguntas WHERE ts >= ?1 AND sin_dato = 1 ORDER BY ts DESC LIMIT 150", desde),
    q("SELECT id, ts, pregunta, respuesta, feedback, feedback_ts FROM preguntas WHERE ts >= ?1 AND feedback IS NOT NULL ORDER BY feedback_ts DESC LIMIT 150", desde),
    q("SELECT id, ts, pagina, pregunta, respuesta, fuentes, sin_dato, cortada, feedback FROM preguntas WHERE ts >= ?1 ORDER BY ts DESC LIMIT 300", desde),
    q("SELECT fuentes FROM preguntas WHERE ts >= ?1 AND fuentes IS NOT NULL AND fuentes != '' ORDER BY ts DESC LIMIT 5000", desde),
    q("SELECT COUNT(*) AS total, COALESCE(SUM(ts < ?1),0) AS mas5, COALESCE(SUM(ts < ?2),0) AS mas6, MIN(ts) AS primera FROM preguntas", Date.now() - 150 * DIA, Date.now() - 180 * DIA),
    q("SELECT id, ts, pagina, texto, mail FROM mensajes WHERE ts >= ?1 ORDER BY ts DESC LIMIT 300", desde),
    q("SELECT COALESCE(SUM(ts < ?1),0) AS mas5, COALESCE(SUM(ts < ?2),0) AS mas6 FROM mensajes", Date.now() - 150 * DIA, Date.now() - 180 * DIA),
  ]);
  const cuenta = {};
  for (const r of fuentes.results) for (const f of String(r.fuentes).split(/\s+/)) if (f) cuenta[f] = (cuenta[f] || 0) + 1;
  const top = Object.entries(cuenta).sort((a, b) => b[1] - a[1]).slice(0, 25);
  return json({ email, dias, resumen: tot.results[0], sinDato: sinDato.results, comentarios: fb.results, todas: todas.results, fuentes: top, retencion: ret.results[0], mensajes: msgs.results, retencionMensajes: msgRet.results[0] });
}
