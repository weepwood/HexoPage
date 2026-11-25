"""Post-build quality pass, with stable original content and local image assets."""
import json,re,html
from pathlib import Path
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser

def finish(work,root):
    public=work/'public'
    manifest=json.loads((work/'butterfly-optimized/assets/images.json').read_text())
    sizes={v['file'].lstrip('/'):(v['width'],v['height']) for v in manifest.values() if v.get('file') and v.get('width') and v.get('height')}
    image_count=0
    for p in public.glob('20*/**/index.html'):
        s=p.read_text(encoding='utf-8')
        if 'id="article-container"' not in s:continue
        def patch(m):
            nonlocal image_count
            tag=m[0]
            src=re.search(r'\bsrc="([^"]+)"',tag)
            if not src:return tag
            rel=unquote(urlsplit(html.unescape(src[1])).path).removeprefix(root)
            size=sizes.get(rel)
            if size and not re.search(r'\b(?:width|height)=',tag) and 'post_bg' not in tag and 'avatar-img' not in tag and 'data-move-multiple' not in tag:
                tag=tag.replace('<img','<img width="%s" height="%s"'%size,1);image_count+=1
            return tag
        s=re.sub(r'<img\b[^>]*>',patch,s)
        if 'data-pagefind-body' not in s:s=s.replace('id="article-container"','id="article-container" data-pagefind-body',1)
        p.write_text(s,encoding='utf-8')
    print('IMAGE_DIMENSIONS',image_count,flush=True)
    # Validate public article routes; keep historical alias redirects and exact source paths.
    rows=json.loads((public/'search-meta.json').read_text())
    for r in rows:
        path=unquote(urlsplit(r['url']).path).removeprefix(root).lstrip('/')
        if not (public/path/'index.html').is_file():raise RuntimeError('Missing article route: '+path)
    for route in ['archives/index.html','page/categories/index.html','page/tags/index.html','sitemap.xml','atom.xml']:
        if not (public/route).is_file():raise RuntimeError('Missing quality route '+route)
