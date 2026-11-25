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

def seo(work,root):
    from urllib.parse import urljoin,quote
    public=work/'public'
    base=json.loads((work/'_config.pages.json').read_text())['url'].rstrip('/')+'/'
    origin=urlsplit(base).scheme+'://'+urlsplit(base).netloc
    article_paths={public/unquote(urlsplit(r['url']).path).removeprefix(root).lstrip('/')/'index.html' for r in json.loads((public/'search-meta.json').read_text())}
    count=0
    for f in public.rglob('*.html'):
        s=f.read_text(encoding='utf-8')
        if '</head>' not in s or '<body' not in s:continue
        # Existing canonical and metadata remain authoritative for the original route.
        class Meta(HTMLParser):
            def __init__(self):super().__init__();self.values={};self.canonical=[]
            def handle_starttag(self,t,attrs):
                a=dict(attrs)
                if t=='meta' and a.get('content'):self.values[a.get('property') or a.get('name')]=a['content']
                if t=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        m=Meta();m.feed(s)
        if len(m.canonical)!=1:raise RuntimeError('Invalid canonical '+str(f))
        canonical=m.canonical[0]
        if not canonical.startswith(base):raise RuntimeError('Canonical outside version: '+canonical)
        def label_link(match):
            tag=match[0]
            if 'aria-label=' in tag:return tag
            if re.search(r'class="[^"]*\bheader-anchor\b',tag):
                href=re.search(r'href="#([^"]+)"',tag)
                if href:return tag[:-1]+' aria-label="'+html.escape('定位到 '+unquote(html.unescape(href[1])).replace('-',' '),quote=True)+'">'
            if re.search(r'class="[^"]*\bextend\b',tag):
                label='下一页' if 'rel="next"' in tag else '上一页'
                return tag[:-1]+' aria-label="'+label+'">'
            return tag
        s=re.sub(r'<a\b[^>]*>',label_link,s)
        def label_image(match):
            tag=match[0]
            if re.search(r'\balt=',tag):return tag
            # Decorative banner artwork is not article content. Unknown legacy image descriptions remain explicitly marked.
            alt='' if 'data-move-multiple' in tag else '历史图片（原文未提供替代文字）'
            return tag.replace('<img','<img alt="'+alt+'"',1)
        s=re.sub(r'<img\b[^>]*>',label_image,s)
        s=re.sub(r'(<meta property="og:image" content=")(/[^"]+)(")',lambda a:a[1]+origin+a[2]+a[3],s)
        target='content-inner'
        if 'id="content-inner"' in s:
            s=re.sub(r'(<body(?:\s[^>]*)?>)',r'\1<a class="halo-skip-link" href="#content-inner">跳转到主要内容</a>',s,count=1)
            s=s.replace('id="content-inner"','id="content-inner" tabindex="-1"',1)
        if f in article_paths:
            v=m.values
            data={'@context':'https://schema.org','@type':'BlogPosting','headline':v.get('og:title',''),'mainEntityOfPage':{'@type':'WebPage','@id':canonical},'url':canonical,'inLanguage':'zh-CN'}
            if v.get('description'):data['description']=v['description']
            if v.get('article:published_time'):data['datePublished']=v['article:published_time']
            if v.get('article:author'):data['author']={'@type':'Person','name':v['article:author']}
            if v.get('og:image'):data['image']=urljoin(origin,v['og:image'])
            payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
            s=s.replace('</head>','<script type="application/ld+json">'+payload+'</script></head>',1);count+=1
        f.write_text(s,encoding='utf-8')
    print('SEO_BLOGPOSTING',count,flush=True)
    if count!=len(json.loads((public/'search-meta.json').read_text())):raise RuntimeError('Structured data coverage mismatch')
