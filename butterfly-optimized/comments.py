"""Generate the official Giscus comment mount with stable article identity."""
import hashlib,html,re,shutil,unicodedata,json
from urllib.parse import quote
from pathlib import Path
def prepare(work):
    opt=work/'butterfly-optimized'
    theme=work/'themes/butterfly'
    p=theme/'_config.yml';s=p.read_text()
    s,n=re.subn(r'(?m)^    - Valine\s*$', '    - HaloGitHub',s,count=1)
    if n!=1:raise RuntimeError('Unexpected original comment configuration')
    p.write_text(s)
    p=theme/'layout/includes/third-party/comments/index.pug'
    p.write_text('hr\n#post-comment\n  .comment-head\n    .comment-headline\n      i.fas.fa-comments.fa-fw\n      span= " 评论"\n  .comment-wrap\n    #halo-comments\n')
    shutil.copy2(opt/'giscus.js',work/'source/js/halo-giscus.js')

def finish(work,root):
    public=work/'public';count=0
    config=json.loads((work/'butterfly-optimized/giscus.json').read_text())
    config_attr=html.escape(json.dumps(config,separators=(',',':')),quote=True)
    for p in public.rglob('*.html'):
        s=p.read_text(encoding='utf-8')
        if '<div id="halo-comments"></div>' not in s:continue
        rel=p.relative_to(public).as_posix()
        rel=unicodedata.normalize('NFC',rel.removesuffix('index.html').strip('/'))
        # Main and historical snapshots share the same article path, not the version prefix.
        key='halo-comment-'+hashlib.sha256(rel.encode()).hexdigest()[:20]
        canonical='https://weepwood.github.io/HexoPage/'+quote(rel,safe='/')+('/' if rel else '')
        esc=lambda v:html.escape(v,quote=True)
        content=f'''<section id="halo-comments" data-key="{key}" aria-label="文章评论" data-giscus="{config_attr}">
<p class="halo-giscus-status" role="status">滚动到评论区附近后加载站内评论。</p>
<div class="giscus" id="halo-giscus"></div>
<button type="button" class="halo-giscus-retry" hidden>重新加载站内评论</button>
<noscript>请启用 JavaScript 以加载评论。</noscript></section>'''
        s=s.replace('<div id="halo-comments"></div>',content,1)
        s=s.replace('</head>',f'<meta name="giscus:backlink" content="{esc(canonical)}"></head>',1)
        s=s.replace('</body>',f'<script defer src="{root}js/halo-giscus.js"></script></body>',1)
        p.write_text(s,encoding='utf-8');count+=1
    if count==0:raise RuntimeError('No comment sections generated')
    print('GITHUB_COMMENT_SECTIONS',count,flush=True)
