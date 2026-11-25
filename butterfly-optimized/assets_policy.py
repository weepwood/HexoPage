"""Runtime-free image migration: all image requests resolve within the published version."""
import html,json,re,shutil
from pathlib import Path
from urllib.parse import urlsplit
from html.parser import HTMLParser

MISSING='/images/archive/missing.svg'
FONT_URL='https://fonts.googleapis.com/css2?family=Inter:wght@400..700&family=Noto+Sans+SC:wght@400..700&display=swap'

def prepare(work):
    opt=work/'butterfly-optimized'
    config=work/'_config.yml';c=config.read_text();c=re.sub(r'(?m)^skip_render:.*$', 'skip_render:\n  - CodePen/**\n  - images/archive/**\n  - vendor/**', c);config.write_text(c)
    shutil.copy2(opt/'assets/missing.svg',work/'source/images/archive/missing.svg')
    shutil.copy2(opt/'parallax.js',work/'source/js/bilibili-banner.js')
    manifest=json.loads((opt/'assets/images.json').read_text())
    for i in (1,2):
        row=manifest['https://cdn.jsdelivr.net/gh/halo-blog/cdn-blog-img-a@main/BilibiliBannerSpring/flow'+str(i)+'.png']
        shutil.copy2(work/'source'/row['file'].lstrip('/'),work/'source/images/archive'/('petal-'+str(i)+'.webp'))
    # Font service publishes variable WOFF2 shards with unicode-range; CSS loaded non-blocking.
    p=work/'themes/butterfly/_config.yml';s=p.read_text()
    marker='    - <link rel="stylesheet" href="/css/halo-refine.css">'
    s=s.replace(marker,marker+'\n    - <link rel="preconnect" href="https://fonts.googleapis.com">\n    - <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    - <link rel="stylesheet" href="'+FONT_URL.replace('&','&amp;')+'" media="print" onload="this.media=\'all\'">')
    p.write_text(s)
    p=work/'source/css/butterfly.css';s=p.read_text().replace('font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;', 'font-family: "Noto Sans SC", -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;');p.write_text(s)

def finish(work,root):
    opt=work/'butterfly-optimized';public=work/'public'; manifest=json.loads((opt/'assets/images.json').read_text())
    mapping={u:root+(v.get('file') or MISSING).lstrip('/') for u,v in manifest.items()}
    for u,v in manifest.items():
        if v.get('file') and not (public/v['file'].lstrip('/')).is_file():raise RuntimeError('Missing migrated file: '+v['file'])
    # Replace actual image references and CSS backgrounds, not ordinary outgoing site links.
    ext=re.compile(r'^(?:https?:)?//',re.I)
    attrs=re.compile(r'(?P<lead>\b(?P<name>src|data-src|data-lazy-src|data-original|poster|href|xlink:href|content)\s*=\s*)(?P<q>["\x27])(?P<val>.*?)(?P=q)',re.I|re.S)
    tags=re.compile(r'<(?:img|image|source|meta|a|video)\b[^>]*>',re.I)
    cssurl=re.compile(r"""url\(\s*(?:(?P<q>["'])(?P<quoted>(?:https?:)?//.*?)(?P=q)|(?P<bare>(?:https?:)?//[^\s)]+))\s*\)""",re.I)
    stats={'mapped':0,'fallback':0,'unknown':set()}
    def local(u, allow_unknown=True):
        url=html.unescape(u)
        if not ext.match(url):return u
        if url in mapping:
            stats['mapped']+=1
            if not manifest[url].get('file'):stats['fallback']+=1
            return mapping[url]
        if not allow_unknown:return u
        stats['unknown'].add(url);stats['fallback']+=1
        return root+MISSING.lstrip('/')
    def replace_tag(m):
        tag=m[0];kind=re.match(r'<(\w+)',tag)[1].lower()
        is_image=kind in ('img','image') or (kind=='source' and ('image/' in tag or 'srcset' in tag))
        is_meta=kind=='meta' and re.search(r'(og:image|twitter:image)',tag,re.I)
        def replace(a):
            n=a['name'].lower();v=a['val'];un=html.unescape(v)
            if is_image or (n=='poster') or (is_meta and n=='content') or (kind=='a' and n=='href' and un in mapping):
                new=local(v);return a['lead']+a['q']+new+a['q']
            return a[0]
        tag=attrs.sub(replace,tag)
        if is_image:
            tag=re.sub(r'(\bsrcset\s*=\s*)(["\x27])(.*?)\2',lambda a:a[1]+a[2]+', '.join(' '.join([local(parts[0])]+parts[1:]) for item in a[3].split(',') if (parts:=item.strip().split()))+a[2],tag,flags=re.I)
        return tag
    def css_replace(m):
        u=m['quoted'] or m['bare']
        if html.unescape(u) in mapping or re.search(r'\.(png|jpe?g|gif|webp|svg|avif|ico)(?:\?|$)',u,re.I):return 'url('+local(u)+')'
        return m[0]
    for p in public.rglob('*'):
        if p.suffix not in ('.html','.css'):continue
        s=p.read_text(encoding='utf-8')
        if p.suffix=='.html':s=tags.sub(replace_tag,s)
        s=cssurl.sub(css_replace,s)
        p.write_text(s,encoding='utf-8')
    class Audit(HTMLParser):
        def __init__(self):super().__init__();self.external=set();self.missing=set();self.count=0
        def handle_starttag(self,tag,attrs):
            for k,v in attrs:
                if not v:continue
                if (tag in ('img','image') and k in ('src','data-src','data-lazy-src','data-original','href','xlink:href')) or k=='poster':
                    if ext.match(v):self.external.add(v)
                    if v.startswith(root):
                        self.count+=1
                        from urllib.parse import unquote
                        if not (public/unquote(urlsplit(v).path.removeprefix(root))).is_file():self.missing.add(v)
                if k=='style':
                    for match in cssurl.finditer(v):self.external.add(match['quoted'] or match['bare'])
    audit=Audit()
    for p in public.rglob('*.html'):audit.feed(p.read_text(encoding='utf-8'))
    if audit.external or audit.missing:raise RuntimeError('External or missing image: '+str((audit.external,audit.missing)))
    print('IMAGE_AUDIT',audit.count,'local references verified',flush=True)
    print('IMAGE_POLICY',json.dumps({**stats,'unknown':sorted(stats['unknown'])},ensure_ascii=False),flush=True)
