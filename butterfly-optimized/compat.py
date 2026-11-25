"""Compatibility repairs in the isolated Butterfly build, never in old tags."""
from pathlib import Path
import shutil,re

def prepare(work):
    theme=work/'themes/butterfly'; opt=work/'butterfly-optimized'
    p=theme/'_config.yml';s=p.read_text()
    s=re.sub(r'(?m)^  mathjax: https?://[^\n]+','  mathjax: /vendor/mathjax/tex-mml-chtml.js',s)
    p.write_text(s)
    p=theme/'layout/includes/third-party/math/mathjax.pug';s=p.read_text()
    s=s.replace("mjx-container:not([display=\\'true\\']","mjx-container:not([display=\\'true\\'])")
    s=s.replace("script.src = '!{theme.CDN.mathjax}'","script.src = '!{url_for(theme.CDN.mathjax)}'")
    p.write_text(s)
    # Legacy demo inputs have no associated label. Preserve the visible text and label from the source.
    p=theme/'scripts/tag/checkbox.js';s=p.read_text()
    s=s.replace("'use strict';","'use strict';\nconst { escapeHTML } = require('hexo-util')")
    s=s.replace('<input type="checkbox"','<input aria-label="${escapeHTML(text)}" type="checkbox"').replace('<input type="radio"','<input aria-label="${escapeHTML(text)}" type="radio"')
    p.write_text(s)
    # Preserve formula source, use safe overflow instead of legacy line-height compression.
    p=work/'source/css/butterfly.css';s=p.read_text()
    s=re.sub(r'mjx-container\[jax="CHTML"\]\s*\{\s*line-height:\s*0\.5\s*!important;?\s*\}', '',s)
    p.write_text(s)
    src=opt/'node_modules/mathjax/es5';dest=work/'source/vendor/mathjax'
    dest.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src/'tex-mml-chtml.js',dest/'tex-mml-chtml.js')
    for rel in ('input/tex/extensions','output/chtml/fonts/woff-v2','a11y','sre'):
        shutil.copytree(src/rel,dest/rel,dirs_exist_ok=True)
    for f in (opt/'node_modules/mathjax').glob('LICENSE*'):shutil.copy2(f,dest/f.name)
