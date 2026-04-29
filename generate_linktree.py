
import json, os, re

NOTEBOOKS = [
    {"file": "1.ipynb", "title": "Lab 1 – Number Series", "icon": "🔢",
     "desc": "Even/Odd Series, Fibonacci, Reverse Number, Sum of Digits, Prime Series"},
    {"file": "2.ipynb", "title": "Lab 2 – Conditional Statements", "icon": "🔀",
     "desc": "Age check, Grade system, Driving licence, Positive/Negative, Discount, Login, Speed Zone"},
    {"file": "3.ipynb", "title": "Lab 3 – Functions & Lambdas", "icon": "λ",
     "desc": "Addition, Square, Area, Map +10, Sum of List, Power, Even/Odd, Factorial"},
    {"file": "4.ipynb", "title": "Lab 4 – Data Structures", "icon": "📦",
     "desc": "String, List, Tuple, Set, Dictionary operations"},
    {"file": "5.ipynb", "title": "Lab 5 – Regular Expressions", "icon": "🔍",
     "desc": "match, search, findall, sub, Email/Phone/Password validators"},
    {"file": "6.ipynb", "title": "Lab 6 – OOP & Inheritance", "icon": "🏗️",
     "desc": "Single & multi-level inheritance, polymorphism, method overriding"},
    {"file": "7.ipynb", "title": "Lab 7 – File Handling & Exceptions", "icon": "📂",
     "desc": "File read/write/append, ZeroDivisionError, ValueError, custom exceptions"},
    {"file": "8.ipynb", "title": "Lab 8 – Netflix Data Analysis", "icon": "📊",
     "desc": "Pandas, NumPy, Matplotlib – EDA on Netflix titles dataset"},
]

BASE = os.path.dirname(os.path.abspath(__file__))

def get_cells(nb_path):
    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)
    cells = []
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "code":
            src = "".join(cell["source"]).strip()
            if src:
                cells.append({"idx": i, "code": src})
    return cells

def escape_html(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

# ── Build notebook sections ──────────────────────────────────────────────────
sections_html = ""
for nb in NOTEBOOKS:
    path = os.path.join(BASE, nb["file"])
    cells = get_cells(path)

    cards_html = ""
    for c in cells:
        code_esc = escape_html(c["code"])
        cell_id  = f"{nb['file']}-{c['idx']}"
        cards_html += f"""
        <div class="code-card">
          <div class="code-header">
            <span class="cell-label">Cell {c['idx']}</span>
            <button class="copy-btn" onclick="copyCode('{cell_id}')" title="Copy">
              <svg viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            </button>
          </div>
          <pre id="{cell_id}"><code>{code_esc}</code></pre>
        </div>"""

    sections_html += f"""
  <section class="nb-section" id="{nb['file']}">
    <div class="nb-header">
      <span class="nb-icon">{nb['icon']}</span>
      <div>
        <h2>{nb['title']}</h2>
        <p class="nb-desc">{nb['desc']}</p>
      </div>
      <button class="toggle-btn" onclick="toggleSection('{nb['file']}')">
        <svg class="chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
    </div>
    <div class="nb-body collapsed" id="body-{nb['file']}">
      {cards_html}
    </div>
  </section>"""

# ── Linktree cards ────────────────────────────────────────────────────────────
link_cards_html = ""
for nb in NOTEBOOKS:
    link_cards_html += f"""
      <a class="link-card" href="#{nb['file']}">
        <span class="lc-icon">{nb['icon']}</span>
        <div class="lc-info">
          <span class="lc-title">{nb['title']}</span>
          <span class="lc-desc">{nb['desc']}</span>
        </div>
        <svg class="lc-arrow" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>
      </a>"""

# ── Full HTML ─────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>APCS Lab – Code Notebook Hub</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0d0f1a;--surface:#13162b;--surface2:#1a1e38;
  --accent:#7c6ef7;--accent2:#a78bfa;--accent3:#38bdf8;
  --text:#e2e8f0;--muted:#8892b0;--border:#252945;
  --green:#22c55e;--red:#f87171;
}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;min-height:100vh}}

/* ── HEADER ── */
.hero{{
  text-align:center;padding:60px 20px 30px;
  background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(124,110,247,.18) 0%,transparent 70%);
}}
.hero-badge{{display:inline-block;background:rgba(124,110,247,.15);border:1px solid rgba(124,110,247,.35);
  color:var(--accent2);border-radius:999px;padding:4px 14px;font-size:.75rem;font-weight:600;letter-spacing:.07em;margin-bottom:18px}}
.hero h1{{font-size:clamp(1.8rem,5vw,3rem);font-weight:800;
  background:linear-gradient(135deg,#fff 30%,var(--accent2) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.hero p{{color:var(--muted);margin-top:10px;font-size:.95rem}}
.stats{{display:flex;justify-content:center;gap:28px;margin-top:28px;flex-wrap:wrap}}
.stat{{text-align:center}}
.stat-n{{font-size:1.6rem;font-weight:800;color:var(--accent2)}}
.stat-l{{font-size:.7rem;color:var(--muted);letter-spacing:.05em;text-transform:uppercase}}

/* ── LINK CARDS ── */
.link-grid{{max-width:720px;margin:40px auto;padding:0 20px;display:flex;flex-direction:column;gap:12px}}
.link-card{{
  display:flex;align-items:center;gap:14px;
  background:var(--surface);border:1px solid var(--border);border-radius:14px;
  padding:16px 20px;cursor:pointer;text-decoration:none;color:inherit;
  transition:transform .2s,border-color .2s,box-shadow .2s;
}}
.link-card:hover{{transform:translateY(-2px);border-color:var(--accent);
  box-shadow:0 0 20px rgba(124,110,247,.2)}}
.lc-icon{{font-size:1.6rem;flex-shrink:0;width:40px;text-align:center}}
.lc-info{{flex:1;min-width:0}}
.lc-title{{display:block;font-weight:600;font-size:.95rem}}
.lc-desc{{display:block;font-size:.75rem;color:var(--muted);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.lc-arrow{{width:18px;height:18px;stroke:var(--accent);fill:none;stroke-width:2.5;flex-shrink:0}}

/* ── DIVIDER ── */
.divider{{text-align:center;padding:10px 0 30px;color:var(--muted);font-size:.8rem;letter-spacing:.08em;text-transform:uppercase}}

/* ── NOTEBOOK SECTIONS ── */
.sections{{max-width:860px;margin:0 auto;padding:0 20px 80px;display:flex;flex-direction:column;gap:20px}}
.nb-section{{background:var(--surface);border:1px solid var(--border);border-radius:16px;overflow:hidden}}
.nb-header{{
  display:flex;align-items:center;gap:14px;padding:20px;cursor:pointer;
  transition:background .2s;
}}
.nb-header:hover{{background:var(--surface2)}}
.nb-icon{{font-size:1.8rem;width:44px;text-align:center;flex-shrink:0}}
.nb-header h2{{font-size:1rem;font-weight:700}}
.nb-desc{{font-size:.75rem;color:var(--muted);margin-top:3px}}
.toggle-btn{{margin-left:auto;background:none;border:none;cursor:pointer;color:var(--muted);
  width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  transition:background .2s,color .2s;flex-shrink:0}}
.toggle-btn:hover{{background:rgba(124,110,247,.15);color:var(--accent)}}
.chevron{{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2.5;
  transition:transform .3s}}
.nb-body{{padding:0 20px;max-height:0;overflow:hidden;transition:max-height .4s ease,padding .3s}}
.nb-body:not(.collapsed){{max-height:99999px;padding:0 20px 20px}}
.nb-body.collapsed .chevron{{transform:rotate(0deg)}}
.nb-section:not(.collapsed-section) .chevron{{transform:rotate(180deg)}}

/* ── CODE CARDS ── */
.code-card{{background:var(--bg);border:1px solid var(--border);border-radius:12px;
  margin-top:14px;overflow:hidden}}
.code-header{{display:flex;align-items:center;justify-content:space-between;
  padding:8px 14px;background:var(--surface2);border-bottom:1px solid var(--border)}}
.cell-label{{font-size:.7rem;color:var(--muted);font-weight:600;letter-spacing:.06em;text-transform:uppercase}}
.copy-btn{{background:none;border:1px solid var(--border);border-radius:6px;
  cursor:pointer;color:var(--muted);padding:4px 8px;display:flex;align-items:center;gap:6px;
  font-size:.72rem;font-weight:500;transition:border-color .2s,color .2s,background .2s}}
.copy-btn svg{{width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.copy-btn:hover{{border-color:var(--accent);color:var(--accent);background:rgba(124,110,247,.1)}}
.copy-btn.copied{{border-color:var(--green);color:var(--green)}}
pre{{overflow-x:auto;padding:16px 18px;font-family:'JetBrains Mono',monospace;font-size:.8rem;
  line-height:1.7;color:#cdd6f4}}
pre code{{white-space:pre}}

/* ── FOOTER ── */
footer{{text-align:center;padding:20px;color:var(--muted);font-size:.75rem}}

/* ── COPY TOAST ── */
.toast{{position:fixed;bottom:30px;right:30px;background:var(--green);color:#fff;
  padding:10px 18px;border-radius:10px;font-size:.82rem;font-weight:600;
  opacity:0;transform:translateY(10px);transition:opacity .3s,transform .3s;pointer-events:none;z-index:999}}
.toast.show{{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-badge">APCS LAB · Python Practicals</div>
  <h1>Code Notebook Hub</h1>
  <p>All lab notebooks in one place — browse &amp; copy any code snippet instantly.</p>
  <div class="stats">
    <div class="stat"><div class="stat-n">8</div><div class="stat-l">Notebooks</div></div>
    <div class="stat"><div class="stat-n">Python</div><div class="stat-l">Language</div></div>
    <div class="stat"><div class="stat-n">∞</div><div class="stat-l">Copy &amp; Paste</div></div>
  </div>
</div>

<div class="link-grid">
  {link_cards_html}
</div>

<div class="divider">↓ All Notebooks</div>

<div class="sections">
  {sections_html}
</div>

<footer>Made with 💜 · APCS Lab</footer>
<div class="toast" id="toast">✅ Copied to clipboard!</div>

<script>
function toggleSection(id) {{
  const body = document.getElementById('body-' + id);
  const sec  = body.closest('.nb-section');
  body.classList.toggle('collapsed');
  sec.classList.toggle('collapsed-section');
}}

function copyCode(id) {{
  const pre  = document.getElementById(id);
  const text = pre.innerText;
  navigator.clipboard.writeText(text).then(() => {{
    const btn = pre.previousElementSibling.querySelector('.copy-btn');
    btn.classList.add('copied');
    btn.innerHTML = '<svg viewBox="0 0 24 24"><polyline points="20 6 9 12 4 12"/><path d="M9 12L4 17"/></svg> Copied!';
    showToast();
    setTimeout(() => {{
      btn.classList.remove('copied');
      btn.innerHTML = '<svg viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
    }}, 2000);
  }});
}}

function showToast() {{
  const t = document.getElementById('toast');
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}}

// All sections start collapsed
document.querySelectorAll('.nb-body').forEach(b => b.classList.add('collapsed'));
document.querySelectorAll('.nb-section').forEach(s => s.classList.add('collapsed-section'));

// Smooth scroll to section when link card clicked
document.querySelectorAll('.link-card').forEach(card => {{
  card.addEventListener('click', e => {{
    const href = card.getAttribute('href');
    const id   = href.replace('#','');
    const body = document.getElementById('body-' + id);
    const sec  = body.closest('.nb-section');
    if (body.classList.contains('collapsed')) {{
      body.classList.remove('collapsed');
      sec.classList.remove('collapsed-section');
    }}
  }});
}});
</script>
</body>
</html>"""

out = os.path.join(BASE, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"Generated: {out}")
