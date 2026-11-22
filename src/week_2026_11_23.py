"""Week of 2026-11-23: 2 LinkedIn visuals (1080x1350). Wed and Sat are text-only.

Reuses CSS, page() and FOOT from build.py; only content changes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "2026-11-23"
OUT.mkdir(parents=True, exist_ok=True)

X = """<style>
.rule{margin-top:30px;background:rgba(255,90,69,.08);border:1px solid rgba(255,90,69,.55);border-radius:20px;
  padding:24px 30px;font-size:30px;font-weight:800;color:#fff;line-height:1.3}
.rule span{color:#FF5A45}
.out{margin-top:14px;font-family:'DejaVu Sans Mono',monospace;font-size:27px;border-radius:16px;padding:16px 24px}
.out.bad{background:rgba(255,90,69,.10);border:1px solid rgba(255,90,69,.55);color:#FF8A78}
.out.good{background:rgba(63,207,142,.10);border:1px solid rgba(63,207,142,.5);color:#5FE0A5}
.out b{color:#fff;font-weight:700;font-family:'Inter',sans-serif;font-size:22px;letter-spacing:.06em;text-transform:uppercase;margin-right:14px}
table{width:100%;border-collapse:separate;border-spacing:0 10px;margin-top:6px}
td{background:#161B22;border-top:1px solid #262C36;border-bottom:1px solid #262C36;padding:15px 22px;font-size:27px;color:#C9D1D9}
td:first-child{border-left:1px solid #262C36;border-radius:16px 0 0 16px;font-family:'DejaVu Sans Mono',monospace;color:#A5D6FF;font-size:25px}
td:last-child{border-right:1px solid #262C36;border-radius:0 16px 16px 0;text-align:right;white-space:nowrap;font-family:'DejaVu Sans Mono',monospace}
td .o{color:#8B949E}td .n{color:#5FE0A5;font-weight:700}
.col li{font-size:25px;padding:8px 0 8px 34px}.col li:before{top:20px}
</style>"""

MON = f"""{X}<div class="card">
<div class="kicker">PHP &middot; Laravel &middot; APIs</div>
<h1 style="font-size:70px">array_filter() turns your JSON array <em>into an object.</em></h1>
<div class="block" style="margin-top:44px"><span class="label bad">Keys kept</span>
<pre><span class="v">$ids</span> = [<span class="v">12</span>, <span class="v">0</span>, <span class="v">31</span>, <span class="k">null</span>, <span class="v">47</span>];
<span class="k">echo</span> <span class="f">json_encode</span>(<span class="f">array_filter</span>(<span class="v">$ids</span>));</pre>
<div class="out bad"><b>Output</b>{{"0":12,"2":31,"4":47}}</div></div>
<div class="block" style="margin-top:40px"><span class="label good">Re-index first</span>
<pre><span class="k">echo</span> <span class="f">json_encode</span>(<span class="f">array_values</span>(<span class="f">array_filter</span>(<span class="v">$ids</span>)));

<span class="c">// Laravel collections</span>
<span class="v">$products</span>-&gt;<span class="f">filter</span>()-&gt;<span class="f">values</span>();</pre>
<div class="out good"><b>Output</b>[12,31,47]</div></div>
<div class="rule" style="margin-top:44px">Breaks only when an item <span>before the last one</span> is removed. Clean test data passes.</div>
{FOOT.format(tag="Run it yourself")}
</div>"""

THU = f"""{X}<div class="card">
<div class="kicker">PHP 8.6 &middot; Released Nov 19</div>
<h1 style="font-size:70px">Check your sessions <em>before you upgrade.</em></h1>
<div class="block" style="margin-top:28px"><span class="label neutral">Session defaults that change</span>
<table>
<tr><td>session.use_strict_mode</td><td><span class="o">0</span> &rarr; <span class="n">1</span></td></tr>
<tr><td>session.cookie_httponly</td><td><span class="o">0</span> &rarr; <span class="n">1</span></td></tr>
<tr><td>session.cookie_samesite</td><td><span class="o">""</span> &rarr; <span class="n">Lax</span></td></tr>
</table></div>
<div class="cols" style="margin-top:22px">
<div class="col"><span class="label bad">Test these</span><ul>
<li>JS that reads the session cookie</li><li>Gateways that POST back to you</li><li>Plugins calling session_start()</li></ul></div>
<div class="col"><span class="label good">Mostly fine</span><ul>
<li>Laravel sessions</li><li>WordPress core</li><li>php.ini that already sets these</li></ul></div>
</div>
<div class="block" style="margin-top:28px"><pre><span class="c"># what your server actually runs</span>
php -i | grep session</pre></div>
{FOOT.format(tag="Week one, or wait for .1?")}
</div>"""


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, body in [("1-mon-array-filter-json", MON), ("4-thu-php86-sessions", THU)]:
            pg.set_content(page(body))
            pg.wait_for_timeout(200)
            info = pg.evaluate("""() => { const c = document.querySelector('.card'); const f = c.querySelector('.foot');
                const kids = [...c.children].filter(k => k !== f && k.tagName !== 'STYLE');
                const last = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
                const wide = [...c.querySelectorAll('pre')].map(e => e.scrollWidth - e.clientWidth);
                return {gap: Math.round(f.getBoundingClientRect().top - last), sh: c.scrollHeight, preOverflow: wide}; }""")
            print(name, info)
            pg.screenshot(path=str(OUT / f"{name}.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        b.close()


if __name__ == "__main__":
    main()
