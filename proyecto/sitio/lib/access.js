// Verifica que quien pide los datos del panel entró con Cloudflare Access (código por mail) y que su mail está autorizado.
// Cloudflare Access ya bloquea en la puerta; esto es una segunda cerradura dentro del servidor.
let CERTS = null, CERTS_AT = 0;
function b64u(s) { s = s.replace(/-/g, "+").replace(/_/g, "/"); while (s.length % 4) s += "="; return s; }
function bytes(s) { const bin = atob(b64u(s)); const a = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) a[i] = bin.charCodeAt(i); return a; }
function cookie(request, name) { const m = (request.headers.get("Cookie") || "").match(new RegExp("(?:^|;\\s*)" + name + "=([^;]+)")); return m ? m[1] : null; }

export async function accessEmail(request, env) {
  if (!env.ACCESS_TEAM || !env.ACCESS_AUD || !env.PANEL_EMAILS) return null;
  const jwt = request.headers.get("Cf-Access-Jwt-Assertion") || cookie(request, "CF_Authorization");
  if (!jwt) return null;
  const parts = jwt.split(".");
  if (parts.length !== 3) return null;
  try {
    const header = JSON.parse(new TextDecoder().decode(bytes(parts[0])));
    const payload = JSON.parse(new TextDecoder().decode(bytes(parts[1])));
    if (!CERTS || Date.now() - CERTS_AT > 3600000) {
      const r = await fetch("https://" + env.ACCESS_TEAM + ".cloudflareaccess.com/cdn-cgi/access/certs");
      CERTS = await r.json(); CERTS_AT = Date.now();
    }
    const jwk = (CERTS.keys || []).find((k) => k.kid === header.kid);
    if (!jwk) return null;
    const key = await crypto.subtle.importKey("jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]);
    const ok = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, bytes(parts[2]), new TextEncoder().encode(parts[0] + "." + parts[1]));
    if (!ok) return null;
    const aud = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
    if (!aud.includes(env.ACCESS_AUD)) return null;
    if (!payload.exp || payload.exp * 1000 < Date.now()) return null;
    const email = String(payload.email || "").toLowerCase();
    const allowed = String(env.PANEL_EMAILS).toLowerCase().split(",").map((x) => x.trim()).filter(Boolean);
    return allowed.includes(email) ? email : null;
  } catch (_) {
    return null;
  }
}
