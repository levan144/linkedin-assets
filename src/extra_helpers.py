"""One-off post: 5 Laravel helpers. Reuses styles from build.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "extra" / "2026-10-05"
OUT.mkdir(parents=True, exist_ok=True)

ROWS = [
    ("retry()", "Retry flaky calls with a pause between attempts.",
     '<span class="f">retry</span>(<span class="v">3</span>, <span class="k">fn</span> () =&gt; Http::<span class="f">get</span>(<span class="v">$url</span>), <span class="v">200</span>);'),
    ("rescue()", "Run code, return a fallback instead of crashing.",
     '<span class="f">rescue</span>(<span class="k">fn</span> () =&gt; <span class="v">$api</span>-&gt;<span class="f">rates</span>(), []);'),
    ("once()", "Memoize a value for the rest of the request.",
     '<span class="f">once</span>(<span class="k">fn</span> () =&gt; <span class="v">$this</span>-&gt;<span class="f">loadSettings</span>());'),
    ("data_get()", "Read deep keys without a pile of isset() checks.",
     '<span class="f">data_get</span>(<span class="v">$order</span>, <span class="s">\'shipping.address.city\'</span>);'),
    ("Benchmark::dd()", "Time any closure in milliseconds, then dump.",
     'Benchmark::<span class="f">dd</span>(<span class="k">fn</span> () =&gt; Order::<span class="f">count</span>());'),
]

rows = "".join(
    f"""<div class="hrow"><div class="hn">{i}</div><div class="hb">
<div class="ht">{name}</div><div class="hd">{desc}</div><div class="hc">{code}</div></div></div>"""
    for i, (name, desc, code) in enumerate(ROWS, start=1)
)

EXTRA_CSS = """<style>
.hlist{display:flex;flex-direction:column;gap:16px;margin-top:40px}
.hrow{display:flex;gap:22px;background:#161B22;border:1px solid #262C36;border-radius:20px;padding:22px 26px}
.hn{flex:none;width:48px;height:48px;border-radius:13px;background:#FF5A45;color:#0E1117;font-weight:800;
  font-size:24px;display:flex;align-items:center;justify-content:center}
.hb{min-width:0}
.ht{font-family:'DejaVu Sans Mono',monospace;font-size:28px;font-weight:700;color:#fff}
.hd{font-size:23px;color:#9AA3AE;margin-top:4px}
.hc{font-family:'DejaVu Sans Mono',monospace;font-size:21px;color:#E6EDF3;margin-top:10px;white-space:nowrap}
.k{color:#FF7B72}.s{color:#A5D6FF}.f{color:#D2A8FF}.v{color:#FFA657}
</style>"""

CARD = f"""{EXTRA_CSS}<div class="card">
<div class="kicker">Laravel &middot; Helpers</div>
<h1>5 Laravel helpers that <em>delete code.</em></h1>
<div class="hlist">{rows}</div>
{FOOT.format(tag="Which one is new to you?")}
</div>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(page(CARD))
    pg.wait_for_timeout(150)
    pg.screenshot(path=str(OUT / "laravel-5-helpers.png"),
                  clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
    b.close()
print("ok")
