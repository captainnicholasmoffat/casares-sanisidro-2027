import sys
from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text()
a = t.index("  function renderBody(box, text){"); b = t.index("  function parseTail(text){")
new = '''  function renderBody(box, text){
    box.textContent = "";
    var main = text.split(/\\n\\s*FUENTES\\s*:/i)[0].split(/\\n\\s*SEGUIR\\s*:/i)[0];
    var para = [], ul = null;
    function flushP(){ if (para.length) { box.appendChild(el("p", null, para.join(" ").replace(/\\*\\*/g, ""))); para = []; } }
    main.trim().split("\\n").forEach(function(l){
      if (!l.trim()) { flushP(); ul = null; return; }
      var m = l.match(/^\\s*(?:[-•*]|\\d+[.)])\\s+(.*)$/);
      if (m) { flushP(); if (!ul) { ul = el("ul"); box.appendChild(ul); } ul.appendChild(el("li", null, m[1].replace(/\\*\\*/g, ""))); }
      else { ul = null; para.push(l.trim()); }
    });
    flushP();
  }
'''
t = t[:a] + new + t[b:]
p.write_text(t); print("ok", p)
