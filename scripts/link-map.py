import re,sys
from pathlib import Path
from collections import defaultdict
root=Path(__file__).resolve().parent.parent
sm=(root/"sitemap.xml").read_text()
urls=re.findall(r"<loc>https://www\.kortexlab\.me([^<]*)</loc>",sm)
def f(u): return root/u.lstrip("/")/"index.html" if u!="/" else root/"index.html"
S=set(urls); out=defaultdict(set); inn=defaultdict(set)
for u in urls:
    h=f(u).read_text(encoding="utf-8")
    m=re.search(r"<main.*?</main>",h,flags=re.S)
    if not m: continue
    for href in re.findall(r'href="(/[^"#?]*)',m.group(0)):
        if not href.endswith("/"): href+="/" if "." not in href.split("/")[-1] else ""
        if href in S and href!=u:
            out[u].add(href); inn[href].add(u)
def lang(u): return "fr" if u.startswith("/fr/") else "ar" if u.startswith("/ar/") else "en"
core=[u for u in urls if re.match(r"^(/fr|/ar)?/(blog|glossary|compare|teardowns|solutions)/.+",u)]
rows=[]
for u in sorted(core):
    rows.append((u,len(inn[u]),len(out[u])))
low=[r for r in rows if r[1]<3 or r[2]<3]
with open(root/"docs/audit/link-map.md","w") as w:
    w.write("# Internal link map\n\nBuilt from the main content of every page in the sitemap. Counts are distinct internal pages linking in and out, navigation and footer excluded.\n\n")
    w.write(f"Pages in sitemap: {len(urls)}. Content pages checked (blog, glossary, compare, teardowns, solutions): {len(rows)}. Pages below three inbound or three outbound links: {len(low)}.\n\n")
    w.write("| Page | Inbound | Outbound |\n|---|---|---|\n")
    for u,i,o in rows: w.write(f"| {u} | {i} | {o} |\n")
    orph=[u for u in urls if not inn[u] and u not in ("/","/fr/","/ar/")]
    w.write("\n## Orphans (no inbound link from any main content)\n\n"+("\n".join(f"- {u}" for u in orph) if orph else "None.")+"\n")
print(len(urls),len(rows),len(low))
for r in low[:60]: print(r)
