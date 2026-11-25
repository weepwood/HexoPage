#!/usr/bin/env python3
"""Build isolated, pinned Hexo snapshots without modifying historical tags."""
import json
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
        # Do not publish an obsolete custom domain.
        (work / 'source/CNAME').unlink(missing_ok=True)
        # Local theme sources are authoritative; avoid vanished custom CDN JS.
        theme = work / 'themes/butterfly/_config.yml'
        if theme.exists():
            config = theme.read_text(encoding='utf-8')
            config = re.sub(r'(?m)^  main: https://cdn\.jsdelivr\.net/gh/halo-blog/[^\n]+', '  main: /js/main.js', config)
            config = re.sub(r'(?m)^  utils: https://cdn\.jsdelivr\.net/gh/halo-blog/[^\n]+', '  utils: /js/utils.js', config)
            config = config.replace('https://cdn.jsdelivr.net/gh/halo-blog/cdn-blog-resources@latest/css/bilibili-banner.css', '/css/bilibiliBanner.css')
            theme.write_text(config, encoding='utf-8')
        run('npm', 'ci', '--ignore-scripts', '--legacy-peer-deps', '--no-audit', '--no-fund', cwd=work)
        for relative in destinations:
            root = BASE_PATH + ('/' + relative if relative else '') + '/'
            url = BASE + ('/' + relative if relative else '')
            (work / '_config.pages.json').write_text(json.dumps({'url': url, 'root': root, 'deploy': {'type': ''}, 'timezone': 'Asia/Shanghai'}), encoding='utf-8')
            run('npm', 'run', 'clean', cwd=work)
            run('npm', 'run', 'build', '--', '--config', '_config.yml,_config.pages.json', cwd=work)
            public = work / 'public'
            rebase_assets(public, root)
            for name in ('index.html', 'archives/index.html', 'css/index.css', 'js/main.js', 'js/utils.js', 'search.xml'):
                if not (public / name).is_file() or (public / name).stat().st_size == 0:
                    raise RuntimeError(f'Missing build output: {name}')
            posts = [p for p in public.glob('20*/*/*/**/index.html') if p.is_file()]
            if not posts:
                raise RuntimeError('No generated article pages')
            dest = OUT / relative
            shutil.copytree(public, dest, dirs_exist_ok=True)
            (dest / 'version.json').write_text(json.dumps({'version': version, 'commit': sha, 'posts': len(posts)}, indent=2), encoding='utf-8')
            print(f'Built {root}: {len(posts)} dated pages', flush=True)


if __name__ == '__main__':
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for version, sha in MANIFEST['versions'].items():
        destinations = ([''] if version == MANIFEST['latest'] else []) + [f'versions/{version}']
        build(version, sha, destinations)
    if not (OUT / 'index.html').is_file():
        raise RuntimeError('Latest version missing')
    (OUT / '.nojekyll').touch()
    (OUT / 'versions.json').write_text(json.dumps(MANIFEST, indent=2), encoding='utf-8')
    links = ''.join(f'<li><a href="./{v}/">{v}</a></li>' for v in MANIFEST['versions'])
    (OUT / 'versions').mkdir(exist_ok=True)
    (OUT / 'versions/index.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>HALO 历史版本</title><h1>HALO 历史版本</h1><ul>{links}</ul><a href="../">返回首页</a></html>', encoding='utf-8')
