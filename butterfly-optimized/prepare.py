from pathlib import Path
import re, shutil, subprocess, json, html, importlib.util, xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit
from html.parser import HTMLParser

class Text(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'): self.skip+=1
        elif tag in ('p','br','div','li','tr','pre','h1','h2','h3','h4','td'): self.parts.append(' ')
    def handle_endtag(self,tag):
        if tag in ('script','style') and self.skip:self.skip-=1
        elif tag in ('p','div','li','tr','pre','td'):self.parts.append(' ')
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)

def load_policy(opt):
    p=opt/"assets_policy.py"
    if not p.exists():return None
    spec=importlib.util.spec_from_file_location("asset_policy",p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def prepare(work):
    opt=work/'butterfly-optimized'
    undated=[]
    for post in (work/'source/_posts').rglob('*.md'):
        text=post.read_text(encoding='utf-8'); m=re.match(r'\A---\n(.*?)\n---',text,re.S)
        if m and not re.search(r'^date\s*:',m[1],re.M):
            created=re.search(r'^create:\s*(\d{4}-\d{2}-\d{2})',m[1],re.M); date=created[1] if created else '2022-05-12'
            post.write_text(text[:m.end(1)]+'\ndate: '+date+' 00:00:00'+text[m.end(1):],encoding='utf-8');undated.append(post.relative_to(work/'source/_posts').with_suffix('').as_posix())
    (opt/'undated.json').write_text(json.dumps(undated),encoding='utf-8')
    theme=work/'themes/butterfly'; cfg=theme/'_config.yml'
    s=cfg.read_text(); replacements={'fontawesome':'/vendor/fontawesome/css/all.min.css','jquery':'/vendor/jquery/jquery.min.js','fancybox_css':'/vendor/fancybox/jquery.fancybox.min.css','fancybox':'/vendor/fancybox/jquery.fancybox.min.js'}
    for key,val in replacements.items():s=re.sub(r'(?m)^  '+key+r': https?://[^\n]+','  '+key+': '+val,s)
    s=s.replace('https://cdn.jsdelivr.net/npm/jquery@latest/dist/jquery.min.js','/vendor/jquery/jquery.min.js').replace('https://cdn.jsdelivr.net/gh/l-lin/font-awesome-animation/dist/font-awesome-animation.min.css','/vendor/animation/font-awesome-animation.min.css')
    s=re.sub(r'(?m)^    - <script defer src="https://cdn.jsdelivr.net/npm/hexo-theme-volantis@latest/source/js/issues.min.js"></script>\n','',s)
    s=s.replace('enter_transitions: true','enter_transitions: false').replace('instantpage: true','instantpage: false').replace('lazyload: false\n  count:','lazyload: true\n  count:')
    s=s.replace('https://github.com/lanqilu','https://github.com/weepwood')
    # Keep original theme and cover layout; only refine style and expensive loading.
    s=s.replace('    - <link rel="stylesheet" href="/css/main.css">','    - <link rel="stylesheet" href="/css/main.css">\n    - <link rel="stylesheet" href="/css/halo-refine.css">')
    # main.css already imports this stylesheet; avoid a duplicate network request.
    s=re.sub(r'(?m)^    - <link rel="stylesheet" href="/css/bilibiliBanner.css"[^\n]*\n','',s)
    cfg.write_text(s)
    css=work/'source/css/butterfly.css'; c=css.read_text();c=re.sub(r'@font-face\s*\{\s*font-family:\s*(?:HarmonyOS_Sans_SC_Regular|MyFont);[^}]+\}','',c);c=c.replace('font-family: "HarmonyOS_Sans_SC_Regular";','font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;').replace('font-family: MyFont !important','font-family: ui-monospace, SFMono-Regular, Consolas, monospace !important');c=re.sub(r'cursor: url\(https?://[^)]+\), default','cursor: auto',c);css.write_text(c)
    style_dir=opt/'styles'
    order=json.loads((style_dir/'order.json').read_text())
    if len(order)!=len(set(order)) or set(order)!={f.name for f in style_dir.glob('*.css')} or order[0]!='tokens.css' or order[-1]!='motion.css':
        raise RuntimeError('Invalid design stylesheet order')
    (work/'source/css/halo-refine.css').write_text('\n'.join((style_dir/name).read_text() for name in order),encoding='utf-8')
    shutil.copy2(opt/'search.js',theme/'source/js/search/local-search.js')
    # Preserve the original animated spring banner, but avoid a perpetual animation when offscreen.
    banner=work/'source/js/bilibili-banner.js';b=banner.read_text();b=b.replace('ctx.drawImage(this.img, this.x, this.y, this.width, this.height)\n    }','if (this.img.complete && this.img.naturalWidth) ctx.drawImage(this.img, this.x, this.y, this.width, this.height)\n    }');b=b.replace('    ctx.clearRect(0, 0, _w, _h)','    if (document.hidden || mb.getBoundingClientRect().bottom < 0) { window.requestAnimationFrame(move); return }\n    ctx.clearRect(0, 0, _w, _h)').replace('start()\nmove()','if (!matchMedia("(prefers-reduced-motion: reduce)").matches) { start(); move() }');banner.write_text(b)
    policy=load_policy(opt)
    if policy:policy.prepare(work)
    toc=opt/'toc.js'
    if toc.exists():
        main=theme/'source/js/main.js'
        js=main.read_text()
        start=js.index('  const tocFn = function () {')
        end=js.index('  /**\n * Rightside',start)
        js=js[:start]+'  const tocFn = function () { window.haloInitToc() }\n\n'+js[end:]
        main.write_text(toc.read_text()+';\n'+(opt/'reading.js').read_text()+';\n'+(opt/'navigation.js').read_text()+';\n'+js)

    subprocess.run(['npm','ci','--ignore-scripts','--no-audit','--no-fund'],cwd=opt,check=True)
    spec=importlib.util.spec_from_file_location('compat',opt/'compat.py');compat=importlib.util.module_from_spec(spec);spec.loader.exec_module(compat);compat.prepare(work)
    spec=importlib.util.spec_from_file_location('comments',opt/'comments.py');comments=importlib.util.module_from_spec(spec);spec.loader.exec_module(comments);comments.prepare(work)
    n=opt/'node_modules';dst=work/'source/vendor'
    for source,target in [('@fortawesome/fontawesome-free/css/all.min.css','fontawesome/css/all.min.css'),('jquery/dist/jquery.min.js','jquery/jquery.min.js'),('@fancyapps/fancybox/dist/jquery.fancybox.min.css','fancybox/jquery.fancybox.min.css'),('@fancyapps/fancybox/dist/jquery.fancybox.min.js','fancybox/jquery.fancybox.min.js')]:
        dest=dst/target;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(n/source,dest)
    shutil.copytree(n/'@fortawesome/fontawesome-free/webfonts',dst/'fontawesome/webfonts',dirs_exist_ok=True)
    animation=next((n/'font-awesome-animation').rglob('font-awesome-animation.min.css'));(dst/'animation').mkdir(exist_ok=True);shutil.copy2(animation,dst/'animation/font-awesome-animation.min.css')
    shutil.copy2(n/'@fancyapps/fancybox/dist/jquery.fancybox.js',dst/'fancybox/jquery.fancybox.js')
    shutil.copy2(n/'@fancyapps/fancybox/dist/jquery.fancybox.css',dst/'fancybox/jquery.fancybox.css')
    (dst/'fancybox/SOURCE.txt').write_text('Fancybox 3.5.7 GPL-3.0, unmodified source: https://github.com/fancyapps/fancybox/tree/v3.5.7\n',encoding='utf-8')
    for package,folder in [('@fortawesome/fontawesome-free','fontawesome'),('jquery','jquery'),('@fancyapps/fancybox','fancybox'),('font-awesome-animation','animation')]:
        for f in (n/package).glob('LICENSE*'):
            if f.is_file():shutil.copy2(f,dst/folder/f.name)

def finish(work,root):
    public=work/'public'; entries=ET.parse(public/'search.xml').getroot().findall('entry');meta=[];full=[]
    for e in entries:
        title=e.findtext('title') or '';url=e.findtext('url') or '';content=e.findtext('content') or ''; parser=Text();parser.feed(content);plain=re.sub(r'\s+',' ',' '.join(parser.parts)).strip();meta.append({'title':title,'url':url});full.append({'title':title,'url':url,'text':plain})
    for name,data in [('search-meta.json',meta),('search-full.json',full)]: (public/name).write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    if len(full)!=len(list((work/'source/_posts').rglob('*.md'))):raise RuntimeError('search count mismatch')
    for source in json.loads((work/'butterfly-optimized/undated.json').read_text()):
        row=next((r for r in meta if unquote(urlsplit(r['url']).path).endswith('/'+source+'/')),None)
        if row:
            alias=public/'2026/11/25'/source/'index.html';alias.parent.mkdir(parents=True,exist_ok=True)
            target=html.escape(row['url'] if row['url'].startswith('/') else root+row['url'],quote=True)
            alias.write_text(f'<!doctype html><meta charset=\"utf-8\"><meta http-equiv=\"refresh\" content=\"0;url={target}\"><link rel=\"canonical\" href=\"{target}\"><a href=\"{target}\">文章已迁移</a>',encoding='utf-8')
    # Browser-native lazy loading; first cover and avatar stay eager. Keep image URLs unchanged.
    for page in public.rglob('*.html'):
        s=page.read_text(encoding='utf-8'); first=[False]
        def img(m):
            v=m[0]
            if 'avatar-img' in v or ('post_bg' in v and not first[0]):
                if 'post_bg' in v:first[0]=True
                return v
            return v if re.search(r'\bloading=',v) else v.replace('<img','<img loading="lazy" decoding="async"',1)
        s=re.sub(r'<img\b[^>]*>',img,s,flags=re.I);page.write_text(s,encoding='utf-8')
    policy=load_policy(work/'butterfly-optimized')
    if policy:policy.finish(work,root)
    subprocess.run(['node','butterfly-optimized/minify.cjs'],cwd=work,check=True)
    q=work/'butterfly-optimized/quality.py'
    spec=importlib.util.spec_from_file_location('quality',q);quality=importlib.util.module_from_spec(spec);spec.loader.exec_module(quality);quality.finish(work,root);quality.seo(work,root)
    spec=importlib.util.spec_from_file_location('comments',work/'butterfly-optimized/comments.py');comments=importlib.util.module_from_spec(spec);spec.loader.exec_module(comments);comments.finish(work,root)
    subprocess.run([str(work/'butterfly-optimized/node_modules/.bin/pagefind'),'--site',str(public),'--root-selector','#article-container','--glob','20*/**/index.html','--force-language','zh','--exclude-selectors','.headerlink,.highlight-tools,.copy-button'],cwd=work,check=True)
    if not (public/'pagefind/pagefind.js').is_file():raise RuntimeError('Pagefind bundle missing')
    for name,limit in {'index.html':60000,'css/index.css':220000,'js/main.js':32000,'search-meta.json':50000}.items():
        if not 0<(public/name).stat().st_size<=limit:raise RuntimeError('asset exceeds budget: '+name)
    print('BUTTERFLY METRICS',json.dumps({name:(public/name).stat().st_size for name in ['index.html','css/index.css','css/main.css','js/main.js','js/utils.js','search-meta.json','search-full.json']}),flush=True)
