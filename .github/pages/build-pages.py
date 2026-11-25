#!/usr/bin/env python3
"""Build isolated, pinned Hexo snapshots without modifying historical tags."""
import json
import html
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parents[2]
MANIFEST = json.loads((REPO / '.github/pages/pages-versions.json').read_text())
OUT = REPO / '_pages'
BASE = os.environ.get('PAGES_URL', 'https://weepwood.github.io/HexoPage').rstrip('/')
BASE_PATH = urlsplit(BASE).path.rstrip('/')


def run(*args, cwd=REPO):
    subprocess.run(args, cwd=cwd, check=True)


def rebase_assets(public, prefix):
    # Hexo resolves its own links; legacy literal attributes and CSS URLs do not.
    pattern = re.compile(r'''(?P<lead>\b(?:href|src|poster|data-src|content)\s*=\s*["']|url\(\s*["']?)(?P<url>/(?!/)[^\s"'<>)]*)''', re.I)
    for path in public.rglob('*'):
        if path.suffix.lower() not in {'.html', '.css'}:
            continue
        original = path.read_text(encoding='utf-8')
        def replace(match):
            value = match['url']
            if value == prefix.rstrip('/') or value.startswith(prefix):
                return match[0]
            route = unquote(urlsplit(value).path).lstrip('/')
            target = public / route
            if target.is_file() or (target / 'index.html').is_file():
                return match['lead'] + prefix + value.lstrip('/')
            return match[0]
        patched = pattern.sub(replace, original)
        if patched != original:
            path.write_text(patched, encoding='utf-8')


def build_modern(repo, destinations, version, sha):
    spec = importlib.util.spec_from_file_location('prepare_modern', repo / 'modern/prepare.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix='halo-modern-') as d:
        work = Path(d)
        undated = module.prepare(repo, work)
        run('npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund', cwd=work)
        module.vendor(work)
        for relative in destinations:
            root = BASE_PATH + ('/' + relative if relative else '') + '/'
            url = BASE + ('/' + relative if relative else '')
            (work / '_config.pages.json').write_text(json.dumps({'url': url, 'root': root, 'history_url': BASE_PATH + '/versions/'}), encoding='utf-8')
            run('npm', 'run', 'clean', cwd=work)
            run('npm', 'run', 'build', '--', '--config', '_config.yml,_config.pages.json', cwd=work)
            public = work / 'public'
            rebase_assets(public, root)
            index = json.loads((public / 'search-index.json').read_text())
            expected = len(list((work / 'source/_posts').rglob('*.md')))
            if len(index) != expected:
                raise RuntimeError(f'Article count mismatch: {len(index)} != {expected}')
            for name, budget in {'index.html': 25000, 'css/site.css': 16000, 'js/site.js': 8000, 'search-index.json': 100000}.items():
                if not (public / name).is_file() or not 0 < (public / name).stat().st_size <= budget:
                    raise RuntimeError(f'Missing or over-budget asset: {name}')
            for name in ('archives/index.html', 'page/categories/index.html', 'page/tags/index.html', 'atom.xml', 'sitemap.xml', '404.html'):
                if not (public / name).is_file():
                    raise RuntimeError(f'Missing route: {name}')
            for row in index:
                rel = unquote(urlsplit(row['url']).path).removeprefix(root)
                if not (public / rel / 'index.html').is_file():
                    raise RuntimeError(f'Missing article: {rel}')
            # Preserve the previously published URLs of undated legacy posts.
            for source, date in undated:
                row = next((r for r in index if unquote(urlsplit(r['url']).path).endswith('/' + source + '/')), None)
                if not row:
                    continue
                alias = public / '2026/11/25' / source / 'index.html'
                if not alias.exists():
                    alias.parent.mkdir(parents=True, exist_ok=True)
                    target = html.escape(row['url'], quote=True)
                    alias.write_text(f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{target}"><a href="{target}">文章已迁移</a>', encoding='utf-8')
            dest = OUT / relative
            shutil.copytree(public, dest, dirs_exist_ok=True)
            (dest / 'version.json').write_text(json.dumps({'version': version, 'commit': sha, 'posts': len(index), 'renderer': 'Hexo 8'}, indent=2), encoding='utf-8')
            print(f'Built modern {root}: {len(index)} articles', flush=True)


def build(version, sha, destinations):
    if not re.fullmatch(r'v\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?', version) or not re.fullmatch(r'[a-f0-9]{40}', sha):
        raise ValueError('Invalid pinned version')
    resolved = subprocess.check_output(['git', 'rev-parse', f'{version}^{{commit}}'], cwd=REPO, text=True).strip()
    if resolved != sha:
        raise RuntimeError(f'Tag {version} changed: {resolved}')
    with tempfile.TemporaryDirectory(prefix='hexopage-') as d:
        work = Path(d)
        archive = subprocess.check_output(['git', 'archive', sha], cwd=REPO)
        subprocess.run(['tar', '-xf', '-'], input=archive, cwd=work, check=True)
        optimized = (work / 'butterfly-optimized/prepare.py').is_file()
        if (work / 'modern/prepare.py').is_file() and not optimized:
            build_modern(work, destinations, version, sha)
            return
        # Do not publish an obsolete custom domain.
        (work / 'source/CNAME').unlink(missing_ok=True)
        # Local theme sources are authoritative; avoid vanished custom CDN JS.
        theme = work / 'themes/butterfly/_config.yml'
        if theme.exists():
            config = theme.read_text(encoding='utf-8')
            config = re.sub(r'(?m)^  main: https://cdn\.jsdelivr\.net/gh/halo-blog/[^\n]+', '  main: /js/main.js', config)
            config = re.sub(r'(?m)^  utils: https://cdn\.jsdelivr\.net/gh/halo-blog/[^\n]+', '  utils: /js/utils.js', config)
            config = config.replace('https://cdn.jsdelivr.net/gh/halo-blog/cdn-blog-resources@latest/css/bilibili-banner.css', '/css/bilibiliBanner.css')
            # The original winter/autumn OSS bucket now returns 403. Use the
            # original theme's spring variant (its assets remain available).
            config = re.sub(r'(?m)^  style: winter[^\n]*', '  style: spring', config)
            config = re.sub(r'(?m)^  bilibili_banner: https://cdn\.jsdelivr\.net/gh/halo-blog/[^\n]+', '  bilibili_banner: /js/bilibili-banner.js', config)
            # Historic analytics endpoints are not required to view the archive.
            config = re.sub(r'(?m)^(baidu_analytics|google_analytics):[^\n]*', r'\1:', config)
            config = re.sub(r'(?m)^(  (?:site_uv|site_pv|page_pv)): true', r'\1: false', config)
            header = work / 'themes/butterfly/layout/includes/header/bilibili-banner.pug'
            layout = header.read_text(encoding='utf-8')
            layout = re.sub(r'(?m)^  - var banner_style = .*$', "  - var banner_style = 'spring'", layout)
            header.write_text(layout, encoding='utf-8')
            banner = work / 'source/js/bilibili-banner.js'
            script = banner.read_text(encoding='utf-8')
            banner.write_text("if (document.getElementById('springBanner') && document.getElementById('canvas')) {\n" + script + '\n}\n', encoding='utf-8')
            theme.write_text(config, encoding='utf-8')
        if optimized:
            spec = importlib.util.spec_from_file_location('butterfly_optimized', work / 'butterfly-optimized/prepare.py')
            opt = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(opt)
            opt.prepare(work)
        run('npm', 'ci', '--ignore-scripts', '--legacy-peer-deps', '--no-audit', '--no-fund', cwd=work)
        for relative in destinations:
            root = BASE_PATH + ('/' + relative if relative else '') + '/'
            url = BASE + ('/' + relative if relative else '')
            (work / '_config.pages.json').write_text(json.dumps({'url': url, 'root': root, 'deploy': {'type': ''}, 'timezone': 'Asia/Shanghai'}), encoding='utf-8')
            run('npm', 'run', 'clean', cwd=work)
            run('npm', 'run', 'build', '--', '--config', '_config.yml,_config.pages.json', cwd=work)
            public = work / 'public'
            if optimized:
                opt.finish(work, root)
            rebase_assets(public, root)
            for name in ('index.html', 'archives/index.html', 'css/index.css', 'js/main.js', 'js/utils.js', 'search.xml'):
                if not (public / name).is_file() or (public / name).stat().st_size == 0:
                    raise RuntimeError(f'Missing build output: {name}')
            posts = [p for p in public.glob('20*/*/*/**/index.html') if p.is_file()]
            if not posts:
                raise RuntimeError('No generated article pages')
            dest = OUT / relative
            shutil.copytree(public, dest, dirs_exist_ok=True)
            (dest / 'version.json').write_text(json.dumps({'version': version, 'commit': sha, 'posts': len(json.loads((public / 'search-meta.json').read_text())) if optimized else len(posts)}, indent=2), encoding='utf-8')
            print(f'Built {root}: {len(posts)} dated pages', flush=True)


if __name__ == '__main__':
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    cache = REPO / '.pages-cache'
    cache.mkdir(exist_ok=True)
    fingerprint = hashlib.sha256(Path(__file__).read_bytes() + BASE.encode()).hexdigest()[:16]
    expected_cache = set()
    for version, sha in MANIFEST['versions'].items():
        resolved = subprocess.check_output(['git','rev-parse',f'{version}^{{commit}}'], cwd=REPO, text=True).strip()
        if resolved != sha:
            raise RuntimeError(f'Tag {version} changed: {resolved}')
        destinations = ([''] if version == MANIFEST['latest'] else []) + [f'versions/{version}']
        missing = []
        for relative in destinations:
            key = hashlib.sha256((fingerprint + sha + relative).encode()).hexdigest()
            expected_cache.add(key)
            saved = cache / key
            if (saved/'version.json').is_file() and (saved/'index.html').is_file():
                meta = json.loads((saved/'version.json').read_text())
                if meta.get('commit') == sha and meta.get('version') == version:
                    shutil.copytree(saved, OUT / relative, dirs_exist_ok=True)
                    print(f'Reused immutable snapshot {version} {relative}', flush=True)
                    continue
            missing.append(relative)
        if missing:
            build(version, sha, missing)
            for relative in missing:
                key = hashlib.sha256((fingerprint + sha + relative).encode()).hexdigest()
                shutil.copytree(OUT/relative, cache/key, dirs_exist_ok=True) if relative else shutil.copytree(OUT, cache/key, dirs_exist_ok=True, ignore=shutil.ignore_patterns('versions'))
    for item in cache.iterdir():
        if item.is_dir() and re.fullmatch(r'[a-f0-9]{64}',item.name) and item.name not in expected_cache:
            shutil.rmtree(item)
    # Avoid duplicate indexing of historical preview copies without changing their source tags.
    for path in (OUT/'versions').rglob('*.html'):
        content = path.read_text(encoding='utf-8')
        if 'name="robots"' not in content and '</head>' in content:
            path.write_text(content.replace('</head>', '<meta name="robots" content="noindex,follow"></head>', 1), encoding='utf-8')
    if not (OUT / 'index.html').is_file():
        raise RuntimeError('Latest version missing')
    (OUT / '.nojekyll').touch()
    (OUT / 'versions.json').write_text(json.dumps(MANIFEST, indent=2), encoding='utf-8')
    links = ''.join(f'<li><a href="./{v}/">{v}</a></li>' for v in MANIFEST['versions'])
    (OUT / 'versions').mkdir(exist_ok=True)
    (OUT / 'versions/index.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>HALO 历史版本</title><h1>HALO 历史版本</h1><ul>{links}</ul><a href="../">返回首页</a></html>', encoding='utf-8')
