"""Compare two generated search indexes; fail closed on structural regressions."""
import argparse,json,re,xml.etree.ElementTree as ET
from pathlib import Path
def load(root):
    return {e.findtext('url'):e for e in ET.parse(root/'search.xml').getroot().findall('entry')}
def compare(old,new):
    a,b=load(old),load(new);out={'old':len(a),'new':len(b),'missing':sorted(a.keys()-b.keys()),'added':sorted(b.keys()-a.keys()),'differences':{}}
    patterns={'headings':r'<h[1-6]\b','code':r'<figure class="highlight','tables':r'<table\b','images':r'<img\b','tabs':r'class="tabs','note':r'class="note','footnotes':r'class="footnotes','math_script':r'<script type="math/tex'}
    for name,pat in patterns.items():
        diffs=[]
        for u in sorted(a.keys()&b.keys()):
            n,m=(len(re.findall(pat,x[u].findtext('content') or '')) for x in (a,b))
            if n!=m:diffs.append({'url':u,'old':n,'new':m})
        out['differences'][name]=diffs
    out['title_differences']=[u for u in sorted(a.keys()&b.keys()) if a[u].findtext('title')!=b[u].findtext('title')]
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('old',type=Path);p.add_argument('new',type=Path);args=p.parse_args();result=compare(args.old,args.new);print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(1 if result['missing'] or result['added'] or result['title_differences'] or any(result['differences'].values()) else 0)
