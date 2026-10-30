#!/usr/bin/env python3
"""把 site/ 打包成 Cloudflare Pages 的 _worker.js，并生成部署脚本。"""
import base64, json, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = ROOT / 'site'
TYPES = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.png':'image/png','.svg':'image/svg+xml','.ico':'image/x-icon','.woff2':'font/woff2','.txt':'text/plain; charset=utf-8'}
files = {}
for p in sorted(SITE.rglob('*')):
    if not p.is_file():
        continue
    kind = TYPES.get(p.suffix, 'application/octet-stream')
    if p.suffix in {'.woff2', '.png', '.svg', '.ico'}:
        body = 'data:' + kind.split(';')[0] + ';base64,' + base64.b64encode(p.read_bytes()).decode('ascii')
        files['/' + p.relative_to(SITE).as_posix()] = [kind, body, True]
    else:
        files['/' + p.relative_to(SITE).as_posix()] = [kind, p.read_text(encoding='utf-8'), False]
worker = """const FILES = %s;
function resolve(p){
  if (FILES[p]) return p;
  const q = p.endsWith('/') ? p + 'index.html' : p + '/index.html';
  if (FILES[q]) return q;
  if (FILES[p + '.html']) return p + '.html';
  return null;
}
export default { async fetch(req){
  const url = new URL(req.url); const k = resolve(decodeURIComponent(url.pathname));
  if (!k) { const [type, body, binary] = FILES['/404.html']; return new Response(binary ? decode(body) : body, {status:404, headers:{'content-type':type,'cache-control':'public, max-age=60','x-content-type-options':'nosniff'}}); }
  const [type, body, binary] = FILES[k];
  const value = binary ? decode(body) : body;
  const cache = k.startsWith('/fonts/') ? 'public, max-age=31536000, immutable' : (type.startsWith('text/html') ? 'public, max-age=60' : 'public, max-age=3600');
  return new Response(value, {headers:{'content-type':type,'cache-control':cache,'x-content-type-options':'nosniff'}});
} };
function decode(data){ const raw = atob(data.split(',')[1]); const out = new Uint8Array(raw.length); for(let i=0;i<raw.length;i++) out[i] = raw.charCodeAt(i); return out; }""" % json.dumps(files, ensure_ascii=False, separators=(',', ':'))
(ROOT / 'dist').mkdir(exist_ok=True)
(ROOT / 'dist/_worker.js').write_text(worker, encoding='utf-8')
deploy = """async () => {
const ACC='b7907d57051b31ded7651f3c88c8ffcc', P='starlit-tree';
const worker=%s;
const b='----F'+Date.now();
const fields=[['manifest','{}'],['branch','main'],['commit_message','qkdawn homepage'],['commit_dirty','true']];
let body=fields.map(([n,v])=>`--${b}\\r\\nContent-Disposition: form-data; name="${n}"\\r\\n\\r\\n${v}\\r\\n`).join('');
body+=`--${b}\\r\\nContent-Disposition: form-data; name="_worker.js"; filename="_worker.js"\\r\\nContent-Type: application/javascript+module\\r\\n\\r\\n${worker}\\r\\n--${b}--\\r\\n`;
const d = await cloudflare.request({method:'POST',path:`/accounts/${ACC}/pages/projects/${P}/deployments`,body:new TextEncoder().encode(body),contentType:`multipart/form-data; boundary=${b}`,rawBody:true});
return {id:d.result.id,url:d.result.url,env:d.result.environment};
}""" % json.dumps(worker, ensure_ascii=False)
(ROOT / 'dist/deploy.js').write_text(deploy, encoding='utf-8')
print('files:', len(files), 'worker bytes:', len(worker.encode()))
