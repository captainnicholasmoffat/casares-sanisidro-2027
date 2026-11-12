#!/usr/bin/env bash
# Arma el sitio, lo publica en el anticipo, lo prueba y, sólo si todo da bien, lo publica en el link principal.
# Uso: bash revision/publicar.sh   (desde la raíz del repositorio)
# Necesita CLOUDFLARE_API_TOKEN en el entorno. El control de cifras (cuentas/check.py) corre dentro del armado:
# si un número del texto no coincide con el modelo fiscal, el armado se detiene y no se publica nada.
set -euo pipefail
cd "$(dirname "$0")/.."
export CLOUDFLARE_ACCOUNT_ID=b9ff0a47e862fc50eccca51708ec9fc7 WRANGLER_SEND_METRICS=false
WRANGLER=${WRANGLER:-"npx --yes wrangler@4"}

(cd proyecto/web && python3 -I build_site.py ../../trabajo/nueve.json)

(cd proyecto/sitio && $WRANGLER pages deploy ./public --project-name sanisidro2027 --branch anticipo --commit-dirty=true)
sleep 20
python3 -I revision/probar.py https://anticipo.sanisidro2027.pages.dev

(cd proyecto/sitio && $WRANGLER pages deploy ./public --project-name sanisidro2027 --branch main --commit-dirty=true)
sleep 20
python3 -I revision/probar.py https://sanisidro2027.pages.dev
echo "Publicado y probado."
