import re,sys,html
from pathlib import Path
root=Path(__file__).resolve().parent.parent
urls=re.findall(r"<loc>https://www\.kortexlab\.me([^<]*)</loc>",(root/"sitemap.xml").read_text())
bad=[];stats={"desc":0,"alt":0,"h1":0,"lang":0}
for u in urls:
    f=root/u.lstrip("/")/"index.html" if u!="/" else root/"index.html"
    h=f.read_text(encoding="utf-8")
    d=re.search(r'<meta name="description" content="([^"]*)"',h)
    n=len(html.unescape(d.group(1))) if d else 0
    if not 130<=n<=155: bad.append((u,"description",n)); stats["desc"]+=1
    for img in re.findall(r"<img\b[^>]*>",h):
        if " alt=" not in img: bad.append((u,"img without alt",img[:80])); stats["alt"]+=1
    body=re.sub(r"<script.*?</script>","",h,flags=re.S)
    c=len(re.findall(r"<h1[\s>]",body))
    if c!=1: bad.append((u,"h1 count",c)); stats["h1"]+=1
    lg=re.search(r'<html lang="([^"]+)"',h).group(1)
    exp="fr" if u.startswith("/fr/") else "en"
    if lg!=exp: bad.append((u,"lang",lg)); stats["lang"]+=1
print(len(urls),"urls",stats)
if "-v" in sys.argv:
    for b in bad: print(b)
sys.exit(1 if bad else 0)
