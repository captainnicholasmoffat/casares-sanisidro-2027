// POST /api/translate: traduce al castellano una pregunta escrita en otro idioma, para buscarla en el programa.
import { json, guard, translate } from "../../lib/claude.js";

export async function onRequestPost({ request, env }) {
  const blocked = await guard(request, env, {});
  if (blocked) return blocked;
  if (!env.ANTHROPIC_API_KEY) return json({ code: "not_configured" }, 503);
  let body;
  try { body = await request.json(); } catch (_) { return json({ code: "invalid_request" }, 400); }
  const text = String((body && body.text) || "").trim();
  if (!text || text.length > 700) return json({ code: "invalid_request" }, 400);
  return translate(env, text);
}
