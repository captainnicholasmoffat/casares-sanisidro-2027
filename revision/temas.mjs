// Prueba gratis de la búsqueda del chat: para cada pregunta de revision/temas.json mira si entre los
// 14 pasajes que recibe la IA aparece la sección esperada. No llama a la IA.
// Uso (desde la raíz, después de armar): node revision/temas.mjs
import { readFileSync } from "node:fs";
const root = new URL("..", import.meta.url).pathname;
const { ready, context } = await import(root + "proyecto/sitio/lib/context.js");
const pub = root + "proyecto/sitio/public";
const env = { ASSETS: { fetch: async (req) => { try { return new Response(readFileSync(pub + new URL(req.url).pathname)); } catch { return new Response("", { status: 404 }); } } } };
await ready(env, "http://local");
const casos = JSON.parse(readFileSync(root + "revision/temas.json", "utf8"));
let mal = 0;
for (const [q, esperado] of casos) {
  const heads = context(q).text.split("\n").filter((l) => /^\[P\d+\]/.test(l)).slice(0, 14);
  const ok = heads.some((h) => esperado.some((e) => h.includes(" " + e) || h.includes(e)));
  if (!ok) { mal++; console.log("FALLA " + q + "\n      esperaba " + esperado.join(" o ") + "\n      encontró " + heads.map((h) => h.split(" · ").slice(1, 3).join(" · ").slice(0, 60)).join(" | ")); }
}
console.log(`${casos.length - mal} de ${casos.length} encuentran la sección correcta`);
process.exit(mal ? 1 : 0);
