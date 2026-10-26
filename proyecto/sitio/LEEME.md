# San Isidro 2027 · sitio con «Preguntale al programa»

Sitio estático (página, programa, investigaciones, imágenes) más dos funciones (`/api/ask` y `/api/translate`) que llaman a Claude con la clave de la campaña. La clave nunca llega al navegador.

## Qué hay
- `public/`: la página (`index.html`), `data/programa.json`, `data/investigaciones.json` e imágenes.
- `functions/api/ask.js` y `functions/api/translate.js`: las funciones.
- `lib/claude.js`: llamada a Claude y controles (sólo desde el propio sitio, 12 preguntas cada 10 minutos por persona, tamaños máximos). `lib/rules.js`: las reglas del chat.
- `wrangler.toml`: nombre del proyecto (`sanisidro2027`).

## Subirlo a Cloudflare Pages (una sola vez)
1. Clave de Cloudflare con permiso **Account › Cloudflare Pages › Edit**. Exportar `CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID`.
2. Desde esta carpeta:
   - `npx wrangler pages project create sanisidro2027 --production-branch main`
   - `npx wrangler pages deploy ./public --project-name sanisidro2027 --branch main`
3. Clave de Claude: en el panel de Cloudflare › Workers & Pages › sanisidro2027 › Settings › Variables and Secrets › agregar **Secret** `ANTHROPIC_API_KEY` (Production). O por consola: `npx wrangler pages secret put ANTHROPIC_API_KEY --project-name sanisidro2027`.
4. Volver a correr el `deploy` del paso 2 para que tome la clave.
5. Dirección: `https://sanisidro2027.pages.dev`.

## Opcional
- `MODEL` (variable): modelo de Claude. Por defecto `claude-sonnet-5-5`.
- `MODEL_QUICK` (variable): modelo para traducir preguntas en otros idiomas.

## La clave de Claude
- Crearla en la organización nueva de la Consola de Claude a la que se vincularon los créditos mensuales del plan Max (así no toca créditos comprados).
- Poner un tope de gasto en esa organización.
- Si los créditos se terminan, el chat muestra «El chat llegó a su límite de este mes» y la página sigue funcionando.
