# Relevamiento de habilidades (skills) para la inteligencia artificial municipal · 26 de octubre de 2026

Hecho por un agente de investigación y controlado por el coordinador (existencia de los repositorios principales verificada con git). Sirve de base para el kit municipal y el proyecto Luján.

## Fuentes revisadas
- Oficiales de Anthropic: anthropics/skills, knowledge-work-plugins, claude-plugins-official, financial-services, claude-for-legal, healthcare, life-sciences, claude-cookbooks, claude-code-security-review, claude-plugins-community (2.283 plugins).
- supabase/agent-skills, supabase-community/supabase-plugin, DietrichGebert/ponytail.
- Listas de la comunidad: ComposioHQ/awesome-claude-skills, hesreallyhim/awesome-claude-code, BehiSecc/awesome-claude-skills y otras.
- No se pudieron abrir: skills.sh, claude-plugins.dev, claudemarketplaces.com, ClawHub, LobeHub, tessl.io, claude.com/plugins.

## Adoptar
- Modelo fiscal: xlsx (Anthropic, ya en la sesión), audit-xls (anthropics/financial-services, Apache 2.0), model-qa-review (en tu cuenta).
- Base de datos y login: supabase + supabase-postgres-best-practices (supabase/agent-skills, MIT).
- Trabajos programados y evaluación del chat: inngest-skills (inngest/inngest-skills, Apache 2.0).
- Seguridad: owasp-security (agamm/claude-code-owasp, MIT, cubre ASVS), security-guidance (claude-plugins-official, Apache 2.0), claude-security (Anthropic, sólo uso interno).
- Accesibilidad WCAG 2.2: accessibility (addyosmani/web-quality-skills, MIT).
- Pruebas en navegador: webapp-testing (anthropics/skills, Apache 2.0).
- Pruebas del chat y de ataques: promptfoo-evals y redteam (promptfoo, MIT) — o las de Inngest, no las dos.
- WhatsApp oficial de Meta: whatsapp-webhooks (hookdeck/webhook-skills, MIT).
- Diagnóstico: tabular-review (claude-for-legal, Apache 2.0: una fila por documento, cada dato con cita), duckdb-skills (MIT: planillas y mapas), pdf (Anthropic), explore-data y validate-data.
- Escritura y verificación (en tu cuenta): house-copy-desk, trace-to-source.
- Para crear las nuestras: skill-creator.
- Ya en Mala Fama, mantener: ponytail, code-review, design-critique, accessibility-review, ux-copy.

## Mirar y adaptar
- claude-skills-gov (whitegloveai, MIT): 68 habilidades para gobiernos locales de Texas (clasificar reclamos, impacto de ordenanzas, resoluciones, narrativa del presupuesto, transparencia). Molde para adaptar a Buenos Aires.
- ib-check-deck (financial-services): detecta una cifra con valores distintos; adaptar al formato 1.234,5.
- privacy-legal y ai-governance-legal (claude-for-legal): adaptar a la ley argentina de datos personales.
- Atención de reclamos: ticket-triage y kb-article; plan: process-doc y risk-assessment; presupuesto: variance-analysis.
- Cloudflare (antibots, despliegue), Twilio o Vercel chat-sdk para WhatsApp, Trail of Bits (CC BY-SA), langfuse, deepeval, giskard.

## Descartadas
- castellano-rae (español de España, licencia no comercial), mineru y Kapso (sin licencia, mandan datos afuera), Plugin Hub (pago y opaco), modelos DCF/LBO (son de empresas, no de municipios).

## Huecos: habilidades propias a escribir
1. Escritura en castellano rioplatense llano con las reglas de Nick.
2. Fuentes públicas argentinas: presupuesto, ejecución, ordenanzas fiscal e impositiva, boletín municipal, censo por radio.
3. Control texto contra modelo, con formato 1.234,5 y fuente por cifra.
4. Ordenanzas en técnica legislativa municipal bonaerense.
5. Plan de despliegue con camino crítico.
6. Datos personales con la ley argentina y gobernanza de la inteligencia artificial municipal.
7. Panel «la inteligencia artificial propone, las reglas deciden, una persona aprueba» sobre Supabase e Inngest (base: Mala Fama).
8. Rúbrica en castellano para evaluar las respuestas del chat municipal.
9. Lista ASVS nivel 2 para Next.js, Supabase y Cloudflare.
10. Alta de WhatsApp Business para un organismo público argentino.
11. Next.js en Cloudflare Pages.
12. App instalable (PWA).
