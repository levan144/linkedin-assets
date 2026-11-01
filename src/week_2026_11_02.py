"""Week of 2026-11-02: 3 LinkedIn visuals (1080x1350). Saturday is text-only.

Reuses CSS, page() and FOOT from build.py; only content changes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "2026-11-02"
OUT.mkdir(parents=True, exist_ok=True)

X = """<style>
.rule{margin-top:34px;background:rgba(255,90,69,.08);border:1px solid rgba(255,90,69,.55);border-radius:20px;
  padding:26px 30px;font-size:32px;font-weight:800;color:#fff;line-height:1.3}
.rule span{color:#FF5A45}
.list{display:flex;flex-direction:column;gap:14px;margin-top:30px}
.row{display:flex;gap:22px;background:#161B22;border:1px solid #262C36;border-radius:18px;padding:20px 26px;align-items:center}
.n{flex:none;width:50px;height:50px;border-radius:14px;background:#FF5A45;color:#0E1117;font-weight:800;
  font-size:26px;display:flex;align-items:center;justify-content:center}
.t{font-size:29px;font-weight:800;color:#fff;line-height:1.25}
.d{font-size:24px;line-height:1.4;color:#AEB6BF;margin-top:6px}
pre{font-size:24px}
.col li{font-size:26px}
</style>"""

MON = f"""{X}<div class="card">
<div class="kicker">Laravel &middot; Deploys</div>
<h1 style="font-size:70px">Add config:cache and env() <em>starts returning null.</em></h1>
<div class="block" style="margin-top:36px"><span class="label bad">Works locally, fails after config:cache</span>
<pre><span class="c">// app/Services/PaymentClient.php</span>
<span class="v">$key</span> = <span class="f">env</span>(<span class="s">'PAYMENT_API_KEY'</span>); <span class="c">// null</span></pre>
<div class="note">Cached config &rarr; <b>.env isn&rsquo;t loaded</b> &rarr; failed checkouts.</div></div>
<div class="block" style="margin-top:30px"><span class="label good">env() in config, config() everywhere else</span>
<pre><span class="c">// config/services.php</span>
<span class="s">'payments'</span> =&gt; [<span class="s">'key'</span> =&gt; <span class="f">env</span>(<span class="s">'PAYMENT_API_KEY'</span>)],

<span class="c">// app code</span>
<span class="v">$key</span> = <span class="f">config</span>(<span class="s">'services.payments.key'</span>);</pre></div>
<div class="block" style="margin-top:30px"><span class="label neutral">CI guard</span>
<pre>! grep -rnE <span class="s">"\\benv\\("</span> app/ routes/</pre></div>
{FOOT.format(tag="php artisan optimize runs it too")}
</div>"""

WED = f"""{X}<div class="card">
<div class="kicker">Freelancing &middot; Estimates</div>
<h1 style="font-size:72px">An API quote before one real call <em>is a guess.</em></h1>
<div class="list">
<div class="row"><div class="n">1</div><div class="t">Sandbox, or only production?</div></div>
<div class="row"><div class="n">2</div><div><div class="t">Rate limit</div><div class="d">5,000 products &middot; 1 request each &middot; 60/min = 83 min per sync</div></div></div>
<div class="row"><div class="n">3</div><div class="t">Dates with a timezone?</div></div>
<div class="row"><div class="n">4</div><div class="t">Pagination, or one huge response?</div></div>
<div class="row"><div class="n">5</div><div class="t">Do webhooks retry?</div></div>
</div>
<div class="rule" style="font-size:30px">Paid first step &rarr; real calls &rarr; <span>then the fixed quote.</span>
<div style="font-size:21px;color:#8B949E;font-weight:400;margin-top:8px">Illustrative: 20 h quoted, 30 h real = 50% over</div></div>
{FOOT.format(tag="Quote what you've seen")}
</div>"""

THU = f"""{X}<div class="card">
<div class="kicker">Laravel &middot; Hot take</div>
<h1 style="font-size:74px">Most repositories are <em>Eloquent with extra steps.</em></h1>
<div class="block" style="margin-top:34px"><span class="label bad">Three pieces to call User::find()</span>
<pre><span class="k">class</span> <span class="f">EloquentUserRepository</span>
    <span class="k">implements</span> UserRepositoryInterface {{
    <span class="k">public function</span> <span class="f">find</span>(<span class="k">int</span> <span class="v">$id</span>): ?User {{
        <span class="k">return</span> User::<span class="f">find</span>(<span class="v">$id</span>);
    }}
}}
<span class="c">// + interface + binding in a provider</span></pre></div>
<div class="cols" style="margin-top:30px">
<div class="col"><span class="label good">Instead</span><ul>
<li>Query scopes for reused filters</li><li>One class per big query</li><li>Test the real query with RefreshDatabase</li></ul></div>
<div class="col"><span class="label neutral">Where they fit</span><ul>
<li>API + database behind one interface</li><li>Large team, hard module boundaries</li><li>Framework-free domain core</li></ul></div>
</div>
{FOOT.format(tag="Start, or stop?")}
</div>"""


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, body in [("1-mon-env-config-cache", MON), ("3-wed-api-call-before-quote", WED),
                           ("4-thu-repository-pattern", THU)]:
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
