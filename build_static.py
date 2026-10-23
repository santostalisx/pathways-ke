"""Builds a single-file static copy of the site (no Python server needed) -> pathways-ke.html"""
import json, re, sys
from app import app
out = sys.argv[1] if len(sys.argv) > 1 else "pathways-ke.html"
data = app.test_client().get("/api/data").get_json()
dj = json.dumps(data, ensure_ascii=False).replace("'", "\u2019")
js = open("static/app.js").read()
css = open("static/style.css").read()
js = js.replace("let D = null;                       // data from Flask", "const DATA = " + dj + ";\nlet D = null;")
js = re.sub(r'const res = await fetch\("/api/assess".*?\n', 'const res = { json: async () => assess(answers) };\n', js)
js = re.sub(r'fetch\("/api/data"\).*?route\(\); \}\);', 'D = DATA; route();', js, flags=re.S)
assess = '''
function assess(a) {
  const enjoy = new Set(a.enjoy), strong = new Set(a.strong), ints = new Set(a.interests), sk = new Set(a.skills), cons = new Set(a.careers);
  const ranked = DATA.careers.map(c => {
    let s = c.subjects.filter(x => enjoy.has(x)).length + 2 * c.subjects.filter(x => strong.has(x)).length;
    s += 3 * c.interests.filter(x => ints.has(x)).length + c.skills.filter(x => sk.has(x)).length;
    s += cons.has(c.name) ? 4 : 0; s += c.env.includes(a.env) ? 2 : 0;
    const ov = (x, y) => x.some(i => y.includes(i));
    let vs = 0; (a.values || []).forEach(v => { const m = DATA.values[v]; if (m && (ov(c.interests, m.interests) || ov(c.skills, m.skills))) vs++; }); s += Math.min(2, vs);
    const st = DATA.styles[a.style]; if (st && (ov(c.env, st.env) || ov(c.skills, st.skills))) s += 1;
    const pm = []; (a.problems || []).forEach(p => pm.push(...(DATA.problems[p] || []))); if (ov(c.interests, pm)) s += 3;
    const sd = a.study || "";
    if (c.ymin != null) { if (sd.startsWith("Up to 2") && c.ymin <= 2) s += 2; else if (sd.startsWith("3 to 4") && c.ymin <= 4 && c.ymax >= 3) s += 2; else if (sd.startsWith("5 years") && c.ymax >= 5) s += 2; }
    const best = 3 * c.subjects.length + 3 * c.interests.length + c.skills.length + 14;
    return { ...c, score: Math.min(100, Math.round(s / best * 160)) };
  }).sort((x, y) => y.score - x.score);
  const t = {}; ranked.forEach(c => t[c.track] = (t[c.track] || 0) + c.score);
  const track = Object.keys(t).reduce((m, k) => t[k] > t[m] ? k : m);
  const w = {};
  ranked.filter(c => c.track === track).slice(0, 3).forEach(c => c.subjects.filter(e => !DATA.maths.includes(e)).forEach(e => w[e] = (w[e] || 0) + c.score + (strong.has(e) ? 5 : 0) + (enjoy.has(e) ? 2 : 0)));
  const el = Object.keys(w).sort((x, y) => w[y] - w[x]).slice(0, 3);
  DATA.tracks[track].electives.forEach(e => { if (el.length < 3 && !el.includes(e) && !DATA.maths.includes(e)) el.push(e); });
  return { track, track_info: DATA.tracks[track], careers: ranked.slice(0, 5), subjects: [DATA.core[0], DATA.core[1], track === "STEM" ? "Core Mathematics" : "Essential Mathematics", DATA.core[2], ...el] };
}
'''
js = js.replace("function route() {", assess + "\nfunction route() {")
for x, y in [("don't", "don\u2019t"), ("today's", "today\u2019s"), ("career's", "career\u2019s")]:
    js = js.replace(x, y)
html = open("static/index.html").read()
html = html.replace('<link rel="stylesheet" href="/static/style.css">', "<style>" + css + "</style>").replace('<script src="/static/app.js"></script>', "<script>" + js + "</script>")
open(out, "w").write(html)
