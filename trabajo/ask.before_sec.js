// POST /api/ask: recibe la pregunta con los pasajes que eligió la página y devuelve la respuesta de Claude, a medida que se escribe.
import { json, guard, cleanMessages, askClaude } from "../../lib/claude.js";

export async function onRequestPost({ request, env }) {
  const blocked = guard(request);
  if (blocked) return blocked;
  if (!env.ANTHROPIC_API_KEY) return json({ code: "not_configured" }, 503);
  let body;
  try { body = await request.json(); } catch (_) { return json({ code: "invalid_request" }, 400); }
  const messages = cleanMessages(body && body.messages);
  if (!messages) return json({ code: "invalid_request" }, 400);
  return askClaude(env, messages);
}
