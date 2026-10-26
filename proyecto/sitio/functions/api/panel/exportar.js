// GET /api/panel/exportar: descarga en un solo archivo CSV (se abre con Excel) todas las preguntas y los mensajes de «Escribinos»,
// para cruzar todo en el reporte de mejoras. Los mensajes van sin el mail: el mail se ve sólo en el panel.
import { json } from "../../../lib/claude.js";
import { accessEmail } from "../../../lib/access.js";

// Una celda que empieza con = + - @ podría ejecutarse como fórmula en Excel: se la neutraliza con un apóstrofo.
function cel(v) {
  let s = v == null ? "" : String(v);
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;
  return /[",\n;\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}
const fecha = (ts) => new Date(ts - 3 * 3600000).toISOString().replace("T", " ").slice(0, 16);
export async function onRequestGet({ request, env }) {
  if (!(await accessEmail(request, env))) return json({ code: "forbidden" }, 403);
  if (!env.DB) return json({ code: "not_configured" }, 503);
  const [p, m] = await env.DB.batch([
    env.DB.prepare("SELECT ts, pagina, pregunta, respuesta, fuentes, sin_dato, cortada, feedback FROM preguntas"),
    env.DB.prepare("SELECT ts, pagina, texto FROM mensajes"),
  ]);
  const filas = p.results.map((x) => [x.ts, "pregunta", x.pagina, x.pregunta, x.respuesta, x.fuentes, x.sin_dato, x.cortada, x.feedback])
    .concat(m.results.map((x) => [x.ts, "mensaje", x.pagina, x.texto, "", "", "", "", ""]))
    .sort((a, b) => a[0] - b[0]);
  const head = ["fecha", "tipo", "pagina", "texto", "respuesta", "fuentes", "sin_dato", "cortada", "le_falto"];
  const rows = filas.map((f) => [fecha(f[0])].concat(f.slice(1)).map(cel).join(","));
  const csv = "﻿" + head.join(",") + "\n" + rows.join("\n") + "\n";
  return new Response(csv, { headers: { "content-type": "text/csv; charset=utf-8", "content-disposition": 'attachment; filename="san-isidro-2027-preguntas-y-mensajes-' + new Date().toISOString().slice(0, 10) + '.csv"', "cache-control": "no-store" } });
}
