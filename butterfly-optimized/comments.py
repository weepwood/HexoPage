"""Build a credential-free GitHub Issues comment entry for the published snapshot."""
import hashlib,html,re,shutil,unicodedata,json
from urllib.parse import urlsplit,unquote,quote,urlencode
from pathlib import Path
REPO='weepwood/HexoPage'
def prepare(work):
    opt=work/'butterfly-optimized'
    theme=work/'themes/butterfly'
    p=theme/'_config.yml';s=p.read_text()
    s,n=re.subn(r'(?m)^    - Valine\s*$', '    - HaloGitHub',s,count=1)
    if n!=1:raise RuntimeError('Unexpected original comment configuration')
    p.write_text(s)
    p=theme/'layout/includes/third-party/comments/index.pug'
    p.write_text('hr\n#post-comment\n  .comment-head\n    .comment-headline\n      i.fas.fa-comments.fa-fw\n      span= " 评论"\n  .comment-wrap\n    #halo-comments\n')
    shutil.copy2(opt/'comments.js',work/'source/js/halo-comments.js')
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
        query=f'repo:{REPO} is:issue in:title "{key}"'
        url='https://github.com/'+REPO+'/issues?q='+quote(query,safe='')
        canonical='https://weepwood.github.io/HexoPage/'+quote(rel,safe='/')+('/' if rel else '')
        title='HALO 文章评论 ['+key+']'
        body='文章：'+canonical+'\n\n<!-- 请在下方填写评论。评论公开显示，请不要填写私人信息。 -->\n\n'
        create='https://github.com/'+REPO+'/issues/new?'+urlencode({'title':title,'body':body})
        esc=lambda v:html.escape(v,quote=True)
        content=f'''<section id="halo-comments" data-key="{key}" data-query="{esc(query)}" data-create="{esc(create)}" aria-label="文章评论" data-giscus="{config_attr}">
<p class="halo-giscus-status" role="status">滚动到评论区附近后加载站内评论。</p>
<div class="giscus" id="halo-giscus"></div>
<button type="button" class="halo-giscus-retry" hidden>重新加载站内评论</button>
<details class="halo-legacy-comments"><summary>GitHub 备用讨论入口（旧版 Issues）</summary>
<div class="halo-comment-intro"><div><strong>文章讨论</strong><p>使用 GitHub 账号参与评论，讨论内容公开展示。</p></div><a class="halo-comment-primary" href="{esc(url)}" target="_blank" rel="noopener noreferrer">前往 GitHub 讨论</a></div>
<p class="halo-comment-status" role="status">滚动到评论区后加载讨论。</p><div class="halo-comment-list"></div>
<div class="halo-comment-actions"><button type="button" class="halo-comment-retry" hidden>重新加载</button><a class="halo-comment-new" href="{esc(create)}" target="_blank" rel="noopener noreferrer" hidden>发起第一条讨论</a><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">查看讨论记录</a></div>
</details><noscript>请展开上方 GitHub 备用讨论入口。</noscript></section>'''
        s=s.replace('<div id="halo-comments"></div>',content,1)
        s=s.replace('</head>',f'<meta name="giscus:backlink" content="{esc(canonical)}"></head>',1)
        s=s.replace('</body>',f'<script defer src="{root}js/halo-comments.js"></script><script defer src="{root}js/halo-giscus.js"></script></body>',1)
        p.write_text(s,encoding='utf-8');count+=1
    if count==0:raise RuntimeError('No comment sections generated')
    print('GITHUB_COMMENT_SECTIONS',count,flush=True)
