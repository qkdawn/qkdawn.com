#!/usr/bin/env python3
"""Subset display fonts into site/fonts (woff2).

Requires: pip install fonttools brotli
Place full TTF sources in fonts-src/ (see README). Prebuilt woff2 already ship in site/fonts/.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).parent
SRC = Path(__file__).parent / 'fonts-src'
OUT = ROOT / 'site/fonts'
OUT.mkdir(parents=True, exist_ok=True)

text = ''.join(p.read_text(encoding='utf-8') for p in ROOT.glob('site/*.html') if p.name != 'deer.html')
text += ''.join(p.read_text(encoding='utf-8') for p in (ROOT / 'site/blog').glob('*.html'))
text += (ROOT / 'site/blog/posts.js').read_text(encoding='utf-8')
common = '，。！？：；、“”‘’（）《》【】·—…「」,.!?;:()[]{}<>/\\+-=_@#%&*~`\'"'
unicode_text = ''.join(sorted(set(text + common)))
unicodes = ','.join(f'U+{ord(c):04X}' for c in unicode_text if 0x200 <= ord(c) <= 0xFFFF)

def subset(source, target, extra):
    cmd = ['pyftsubset', str(SRC / source), f'--output-file={OUT / target}', '--flavor=woff2', f'--unicodes={extra}', '--layout-features=*', '--name-IDs=0,1,2,4,6', '--drop-tables+=DSIG', '--no-hinting', '--desubroutinize']
    subprocess.run(cmd, check=True)

latin = 'U+0000-007F,U+00A0-00FF'
subset('Inter[opsz,wght].ttf', 'Inter.woff2', latin)
subset('NotoSansSC[wght].ttf', 'NotoSansSC.woff2', unicodes)
subset('NotoSerifSC[wght].ttf', 'NotoSerifSC.woff2', unicodes)
subset('InstrumentSerif-Regular.ttf', 'InstrumentSerif.woff2', latin)
print('subset characters:', len(unicode_text), 'fonts:', ', '.join(p.name for p in OUT.glob('*.woff2')))
