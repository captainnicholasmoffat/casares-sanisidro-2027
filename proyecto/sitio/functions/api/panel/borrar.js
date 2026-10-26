// POST /api/panel/borrar: borra las preguntas y los mensajes de más de 6 meses. Sólo con el pedido explícito desde el panel.
import { json } from "../../../lib/claude.js";
import { accessEmail } from "../../../lib/access.js";

export async function onRequestPost({ request, env }) {
  if (!(await accessEmail(request, env))) return json({ code: "forbidden" }, 403);
  const origin = request.headers.get("Origin");
  try { if (!origin || new URL(origin).host !== new URL(request.url).host) return json({ code: "forbidden" }, 403); } catch (_) { return json({ code: "forbidden" }, 403); }
  let body; try { body = await request.json(); } catch (_) { return json({ code: "invalid_request" }, 400); }
  if (!body || body.confirmar !== "BORRAR") return json({ code: "invalid_request" }, 400);
  const corte = Date.now() - 180 * 86400000;
  const [r, m] = await env.DB.batch([
    env.DB.prepare("DELETE FROM preguntas WHERE ts < ?1").bind(corte),
    env.DB.prepare("DELETE FROM mensajes WHERE ts < ?1").bind(corte),
  ]);
  return json({ ok: true, borradas: (r.meta && r.meta.changes) || 0, mensajes: (m.meta && m.meta.changes) || 0 });
}
