# qkdawn.com

Personal site for **钱坤 / Kun Qian** — https://www.qkdawn.com

Static Chinese site: through-line「写代码，做 AI，玩 XR。」, project grid, blog stub, and the Starlit Tree experience at `/starlit`.

## Layout

```
site/                 ← public files (edit these)
  index.html          homepage
  styles.css
  blog/
    index.html
    posts.js          ← add blog posts here
  starlit/            Starlit Tree (do not casually rewrite)
  deer.html           legacy path for Starlit
  fonts/              self-hosted woff2 subsets
  404.html
build.py              packs site/ into a Cloudflare Pages worker (optional manual deploy)
fonts.py              regenerate font subsets (optional)
```

## Edit content

**Blog post**

1. Add `site/blog/<slug>.html`
2. Prepend to `POSTS` in `site/blog/posts.js`:
   `{ title: '标题', date: 'YYYY-MM-DD', url: '/blog/<slug>.html' }`

**Project**

Edit the project cells in `site/index.html`. Keep descriptions truthful; do not invent facts.

**Privacy**

Do not put school or city on the public site.

## Local preview

```bash
cd site && python3 -m http.server 8765
# open http://localhost:8765
```

## Deploy

### A. Git → Cloudflare Pages (preferred when connected)

Push to `main`. Intended Pages settings for project **`starlit-tree`**:

- Build command: *(empty / none)*
- Build output directory: `site`
- Root directory: `/` (repo root)
- Production branch: `main`
- Custom domain: `www.qkdawn.com`

**Status (2026-10-31):** API connect returned Cloudflare error `8000011` (Pages Git installation issue). Reconnect GitHub in the Cloudflare dashboard:

1. https://dash.cloudflare.com → Workers & Pages → **starlit-tree** → Settings → Builds & deployments
2. Connect to Git → GitHub → authorize `qkdawn/qkdawn.com`
3. Set output directory to `site`, save

Until that is fixed, production stays on the existing direct-upload worker deploy (path B). Do not delete the custom domain while switching.

### B. Manual worker upload (box / MCP)

Used historically when direct Git was not connected:

```bash
python3 build.py
# then run dist/deploy.js via Cloudflare MCP `execute`
# (account b7907d57051b31ded7651f3c88c8ffcc, project starlit-tree)
```

### Regenerate fonts (optional)

Only needed when new CJK characters appear in HTML/JS:

```bash
pip install fonttools brotli
# place Inter / Noto Sans SC / Noto Serif SC / Instrument Serif sources in fonts-src/
python3 fonts.py
```

Prebuilt `site/fonts/*.woff2` are already committed; most edits do not need this.

## License

Site content © Kun Qian. Third-party font licenses apply to font files (OFL).
