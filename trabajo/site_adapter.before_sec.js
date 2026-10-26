  /* ---------- Preguntale al programa: versión sitio propio (responde la función /api/ask) ---------- */
  var history = [], busy = false, ctl = null;
  function readSSE(r, opts){
    var reader = r.body.getReader(), dec = new TextDecoder(), buf = "", text = "", truncated = false;
    function handle(ev){
      var data = ev.split("\n").filter(function(l){ return l.indexOf("data:") === 0; }).map(function(l){ return l.slice(5).trim(); }).join("");
      if (!data) return;
      var j; try { j = JSON.parse(data); } catch (e) { return; }
      if (j.type === "content_block_delta" && j.delta && j.delta.type === "text_delta") {
        text += j.delta.text;
        if (opts.onText) opts.onText({text: text, delta: j.delta.text});
      } else if (j.type === "message_delta" && j.delta && j.delta.stop_reason === "max_tokens") {
        truncated = true;
      } else if (j.type === "error") {
        var t = j.error && j.error.type;
        throw {code: (t === "overloaded_error" || t === "rate_limit_error") ? "rate_limited" : "upstream_error", text: text};
      }
    }
    function pump(){
      return reader.read().then(function(x){
        if (x.done) { if (buf.trim()) handle(buf); if (!text.trim()) throw {code: "empty_completion"}; return {text: text, truncated: truncated}; }
        buf += dec.decode(x.value, {stream: true});
        var parts = buf.split(/\r?\n\r?\n/); buf = parts.pop();
        parts.forEach(handle);
        return pump();
      });
    }
    return pump();
  }
  function siteSample(input, opts){
    opts = opts || {};
    var turns = Array.isArray(input) ? input.slice() : [{role: "user", content: String(input)}];
    if (turns.length && turns[0].content === RULES) turns.shift();
    while (turns.length && turns[0].role !== "user") turns.shift();
    return fetch("/api/ask", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({messages: turns}), signal: opts.signal})
      .then(function(r){
        if (!r.ok) return r.json().catch(function(){ return {}; }).then(function(j){ throw {code: j.code || (r.status === 429 ? "rate_limited" : "upstream_error")}; });
        return readSSE(r, opts);
      })
      .catch(function(e){
        if (e && e.name === "AbortError") throw {code: "cancelled"};
        if (e && e.code) throw e;
        throw {code: "upstream_error"};
      });
  }
  siteSample.json = function(prompt, opts){
    var q = String(prompt).split("\n\n").slice(1).join("\n\n") || String(prompt);
    return fetch("/api/translate", {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify({text: q}), signal: opts && opts.signal})
      .then(function(r){ return r.ok ? r.json() : {}; });
  };
  function getSample(){ return Promise.resolve(siteSample); }
