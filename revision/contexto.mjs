// Muestra qué pasajes del programa encuentra la búsqueda del chat para cada pregunta, sin llamar a la IA (gratis).
// Uso (desde proyecto/sitio, después de armar): node ../../revision/contexto.mjs "$PWD/lib/context.js" "$PWD/public" "pregunta 1" "pregunta 2"
import { readFileSync } from "node:fs";
const [ctxPath, pubDir, ...qs] = process.argv.slice(2);
const { ready, context } = await import(ctxPath);
const env = { ASSETS: { fetch: async (req) => { const p = new URL(req.url).pathname; try { return new Response(readFileSync(pubDir + p)); } catch { return new Response("", { status: 404 }); } } } };
await ready(env, "http://local");
for (const q of qs) {
  const c = context(q);
  const heads = c.text.split("\n").filter((l) => /^\[P\d+\]/.test(l)).slice(0, 8);
  console.log("\n### " + q); heads.forEach((h) => console.log("  " + h.slice(0, 110)));
}
