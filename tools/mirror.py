#!/usr/bin/env python3
"""Copy the 10onlinecasinos.com AU article onto the bigscissors.com.au homepage.

Run from the repo root:  python3 tools/mirror.py

- Fetches SOURCE and writes it to index.html and en-au/index.html.
- Downloads every image, font, script and stylesheet the page uses from the
  source site into mirror/ and points the page at those local copies.
- Keeps the source's canonical and page links (the original stays
  the canonical version), sets hreflang en-AU and x-default to the source
  article, removes the Clarity and c-tracker analytics, and adds
  the bigscissors Search Console verification tag.
- Removes files in mirror/ the page no longer uses.

Prints "changed" or "unchanged" as the last line. Uses only the standard library.
Do not edit index.html or en-au/index.html by hand: the next sync overwrites them.
"""
import hashlib
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE = "https://10onlinecasinos.com/au/online-casinos/"
SITE = "https://bigscissors.com.au"
MIRROR_DIR = Path("mirror")
OUTPUTS = [Path("index.html"), Path("en-au/index.html")]
HREFLANG = ["en-AU", "x-default"]   # each points to SOURCE
GSC_TAG = '<meta name="google-site-verification" content="RKb416_rnBgrgI837ietY225mlvH1OF2wHtuC_0ONJo" />'
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")

# Any asset URL on the source host, plain or JSON-escaped (https:\/\/...).
ASSET_RE = re.compile(
    r"https?:(?:\\?/){2}(?:www\.)?10onlinecasinos\.com"
    r"((?:\\?/)wp-(?:content|includes)(?:\\?/)[^\"'\s)<>,]+)"
)
CSS_URL_RE = re.compile(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)|@import\s+(['"])([^'"]+)\3""")


def fetch(url, tries=3):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-AU,en;q=0.9",
    })
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == tries - 1:
                raise RuntimeError(f"fetch failed: {url}: {e}") from e
            time.sleep(2 * (attempt + 1))


def short_hash(data):
    return hashlib.sha1(data).hexdigest()[:8]


class Mirror:
    def __init__(self):
        self.done = {}   # source path -> local URL (with ?v=hash)
        self.files = set()

    def local(self, path):
        """Download the asset at source path (e.g. /wp-content/x.png) and return its local URL."""
        path = urllib.parse.unquote(path.split("?")[0].split("#")[0])
        if path in self.done:
            return self.done[path]
        src_url = "https://10onlinecasinos.com" + urllib.parse.quote(path)
        data = fetch(src_url)
        if path.endswith(".css"):
            data = self.rewrite_css(data.decode("utf-8", "replace"), src_url).encode("utf-8")
        dest = MIRROR_DIR / path.lstrip("/")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.read_bytes() != data:
            dest.write_bytes(data)
        self.files.add(dest.resolve())
        url = "/mirror" + urllib.parse.quote(path) + "?v=" + short_hash(data)
        self.done[path] = url
        return url

    def rewrite_css(self, css, base):
        def repl(m):
            ref = m.group(2) or m.group(4)
            if ref.startswith(("data:", "#")):
                return m.group(0)
            absolute = urllib.parse.urljoin(base, ref)
            parsed = urllib.parse.urlparse(absolute)
            if parsed.netloc.replace("www.", "") != "10onlinecasinos.com":
                return m.group(0)
            new = self.local(parsed.path)
            return f'url("{new}")' if m.group(2) else f'@import "{new}"'
        return CSS_URL_RE.sub(repl, css)

    def rewrite_html(self, html):
        def repl(m):
            path = m.group(1).replace("\\/", "/").replace("&amp;", "&")
            return self.local(path)
        return ASSET_RE.sub(repl, html)


def cf_decode(hexstr):
    key = int(hexstr[:2], 16)
    return "".join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))


def clean(html):
    # Cloudflare email obfuscation differs on every request; store plain emails
    # (bigscissors' own Cloudflare re-obfuscates them when serving).
    html = re.sub(r'<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="([0-9a-f]+)">\[email&#160;protected\]</a>',
                  lambda m: f'<a href="mailto:{cf_decode(m.group(1))}">{cf_decode(m.group(1))}</a>', html)
    html = re.sub(r'<span class="__cf_email__" data-cfemail="([0-9a-f]+)">\[email&#160;protected\]</span>',
                  lambda m: cf_decode(m.group(1)), html)
    html = re.sub(r'/cdn-cgi/l/email-protection#([0-9a-f]+)', lambda m: "mailto:" + cf_decode(m.group(1)), html)
    html = re.sub(r'<script[^>]*email-decode\.min\.js[^>]*></script>', "", html)

    # Analytics that belong to the source site.
    html = re.sub(r'<script[^>]*>(?:(?!</script>).)*?clarity\.ms(?:(?!</script>).)*?</script>', "", html, flags=re.S)
    html = re.sub(r'<link[^>]*clarity\.ms[^>]*>\s*', "", html)
    html = re.sub(r'<script[^>]*id="c-tracker-js(?:-before)?"[^>]*>.*?</script>\s*', "", html, flags=re.S)

    # Replace the source's hreflang set with ours: en-AU and x-default -> the AU article.
    html = re.sub(r'<!-- Hreflang Manager - Custom Tags -->.*?<!-- /Hreflang Manager -->\s*', "", html, flags=re.S)
    html = re.sub(r'<link rel="alternate"[^>]*hreflang=[^>]*>\s*', "", html)
    html = html.replace("<link rel=\"canonical\"",
                        "".join(f'<link rel="alternate" hreflang="{lang}" href="{SOURCE}" />\n\t'
                                for lang in HREFLANG) + "<link rel=\"canonical\"", 1)

    # Build timestamp that changes on every cache rebuild.
    html = re.sub(r'\s*<!-- This website is like a Rocket.*?-->', "", html, flags=re.S)
    return html


def main():
    html = fetch(SOURCE).decode("utf-8")
    if "<title>" not in html or len(html) < 20000:
        sys.exit("source page looks wrong (blocked or empty); nothing written")

    html = clean(html)

    # Leave structured data pointing at the original article.
    protected = []
    def protect(m):
        protected.append(m.group(0))
        return f"\0LDJSON{len(protected) - 1}\0"
    html = re.sub(r'<script[^>]*application/ld\+json[^>]*>.*?</script>', protect, html, flags=re.S)

    mirror = Mirror()
    paths = {m.group(1).replace("\\/", "/").replace("&amp;", "&") for m in ASSET_RE.finditer(html)}
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(mirror.local, sorted(paths)))
    html = mirror.rewrite_html(html)

    for i, block in enumerate(protected):
        html = html.replace(f"\0LDJSON{i}\0", block)

    # Social preview images must be absolute URLs.
    html = re.sub(r'(<meta (?:property|name)="(?:og:image|twitter:image)" content=")(/mirror/)', rf'\1{SITE}\2', html)

    html = html.replace('<meta charset="UTF-8">',
                        f'<meta charset="UTF-8">\n    <!-- Copied from {SOURCE} by tools/mirror.py. Do not edit by hand. -->\n    {GSC_TAG}', 1)

    changed = False
    for out in OUTPUTS:
        out.parent.mkdir(parents=True, exist_ok=True)
        data = html.encode("utf-8")
        if not out.exists() or out.read_bytes() != data:
            out.write_bytes(data)
            changed = True

    removed = 0
    if MIRROR_DIR.exists():
        for f in sorted(MIRROR_DIR.rglob("*"), reverse=True):
            if f.is_file() and f.resolve() not in mirror.files:
                f.unlink()
                removed += 1
                changed = True
            elif f.is_dir() and not any(f.iterdir()):
                f.rmdir()

    print(f"{len(mirror.done)} assets mirrored, {removed} stale removed")
    print("changed" if changed else "unchanged")


if __name__ == "__main__":
    main()
