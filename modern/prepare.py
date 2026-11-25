#!/usr/bin/env python3
"""Prepare a separate Hexo 8 work tree, without rewriting source articles."""
import re, shutil, sys
from pathlib import Path


def prepare(repo, stage):
    stage.mkdir(parents=True, exist_ok=True)
    modern = repo / 'modern'
    for name in ('package.json', 'package-lock.json', '_config.yml'):
        shutil.copy2(modern / name, stage / name)
    shutil.copytree(repo / 'source', stage / 'source', dirs_exist_ok=True)
    (stage / 'source/CNAME').unlink(missing_ok=True)
    theme = stage / 'themes/halo-minimal'
    shutil.copytree(modern / 'theme', theme, dirs_exist_ok=True)
    # Original Apache-2.0 Butterfly tag extensions are reused instead of reimplementing them.
    shutil.copytree(repo / 'themes/butterfly/scripts/tag', theme / 'scripts/tag', dirs_exist_ok=True)
    shutil.copy2(repo / 'themes/butterfly/LICENSE', theme / 'LICENSE-Butterfly')
    # Restore create dates, not the CI runner's filesystem creation time.
    undated = []
    for post in (stage / 'source/_posts').rglob('*.md'):
        text = post.read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---', text, re.S)
        if match and not re.search(r'^date\s*:', match[1], re.M):
            create = re.search(r'^create:\s*(\d{4}-\d{2}-\d{2})', match[1], re.M)
            date = create[1] if create else '2022-05-12'
            post.write_text(text[:match.end(1)] + '\ndate: ' + date + ' 00:00:00' + text[match.end(1):], encoding='utf-8')
            undated.append((post.relative_to(stage / 'source/_posts').with_suffix('').as_posix(), date))
    return undated


def vendor(stage):
    src = stage / 'node_modules/katex/dist'
    dst = stage / 'themes/halo-minimal/source/vendor/katex'
    dst.mkdir(parents=True, exist_ok=True)
    for name in ('katex.min.css', 'katex.min.js'):
        shutil.copy2(src / name, dst / name)
    shutil.copy2(src / 'contrib/auto-render.min.js', dst / 'auto-render.min.js')
    shutil.copytree(src / 'fonts', dst / 'fonts', dirs_exist_ok=True)
    shutil.copy2(stage / 'node_modules/katex/LICENSE', dst / 'LICENSE')


if __name__ == '__main__':
    prepare(Path(sys.argv[1]), Path(sys.argv[2]))
