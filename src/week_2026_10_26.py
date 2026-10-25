"""Week of 2026-10-26: 3 LinkedIn visuals (1080x1350). Saturday is text-only.

Reuses CSS, page() and FOOT from build.py; only content changes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "2026-10-26"
OUT.mkdir(parents=True, exist_ok=True)

X = """<style>
.rule{margin-top:34px;background:rgba(255,90,69,.08);border:1px solid rgba(255,90,69,.55);border-radius:20px;
  padding:26px 30px;font-size:32px;font-weight:800;color:#fff;line-height:1.3}
.rule span{color:#FF5A45}
.list{display:flex;flex-direction:column;gap:16px;margin-top:34px}
.row{display:flex;gap:24px;background:#161B22;border:1px solid #262C36;border-radius:20px;padding:24px 28px}
.n{flex:none;width:54px;height:54px;border-radius:14px;background:#FF5A45;color:#0E1117;font-weight:800;
  font-size:27px;display:flex;align-items:center;justify-content:center}
.t{font-size:31px;font-weight:800;color:#fff;line-height:1.25}
.d{font-size:25px;line-height:1.4;color:#AEB6BF;margin-top:8px}
.d code{font-family:'DejaVu Sans Mono',monospace;font-size:23px;color:#A5D6FF}
.vers{display:flex;gap:14px;margin-top:30px;flex-wrap:wrap}
.ver{background:rgba(63,207,142,.12);border:1px solid rgba(63,207,142,.45);color:#5FE0A5;border-radius:14px;
  padding:12px 20px;font-family:'DejaVu Sans Mono',monospace;font-size:28px;font-weight:700}
.ver.old{background:rgba(255,90,69,.1);border-color:rgba(255,90,69,.45);color:#FF8A78}
pre{font-size:24px}
</style>"""

MON = f"""{X}<div class="card">
<div class="kicker">Laravel &middot; Queues</div>
<h1 style="font-size:72px">Your queued job can run <em>before the order exists.</em></h1>
<div class="block" style="margin-top:36px"><span class="label bad">Dispatched inside the transaction</span>
<pre>DB::<span class="f">transaction</span>(<span class="k">function</span> () <span class="k">use</span> (<span class="v">$data</span>) {{
    <span class="v">$order</span> = Order::<span class="f">create</span>(<span class="v">$data</span>);
    SendReceipt::<span class="f">dispatch</span>(<span class="v">$order</span>);
    <span class="v">$this</span>-&gt;<span class="f">reserveStock</span>(<span class="v">$order</span>);
}});</pre>
<div class="note">Redis/SQS worker runs it <b>before the commit</b> &rarr; ModelNotFoundException.<br>
Rollback? <b>The job is queued anyway.</b></div></div>
<div class="block" style="margin-top:30px"><span class="label good">Wait for the commit</span>
<pre>SendReceipt::<span class="f">dispatch</span>(<span class="v">$order</span>)-&gt;<span class="f">afterCommit</span>();

<span class="c">// or per connection, config/queue.php</span>
<span class="s">'after_commit'</span> =&gt; <span class="k">true</span>,</pre></div>
<div class="rule">Rolled back? <span>The job is discarded.</span></div>
{FOOT.format(tag="Check your dispatch calls")}
</div>"""

WED = f"""{X}<div class="card">
<div class="kicker">AI &middot; Testing</div>
<h1 style="font-size:76px">Let AI write tests. <em>Never the expected values.</em></h1>
<div class="block" style="margin-top:36px"><span class="label neutral">Spec: 20% VAT &middot; the code</span>
<pre><span class="k">return</span> <span class="v">$cents</span> + <span class="f">intdiv</span>(<span class="v">$cents</span> * <span class="v">18</span>, <span class="v">100</span>);</pre></div>
<div class="block" style="margin-top:28px"><span class="label bad">AI test written from the code</span>
<pre><span class="f">assertSame</span>(<span class="v">11800</span>, <span class="f">totalWithVat</span>(<span class="v">10000</span>)); <span class="c">// green</span></pre>
<div class="note">Green test. <b>The bug is now protected.</b></div></div>
<div class="block" style="margin-top:28px"><span class="label good">Expected value from the spec</span>
<pre><span class="f">assertSame</span>(<span class="v">12000</span>, <span class="f">totalWithVat</span>(<span class="v">10000</span>)); <span class="c">// red</span></pre></div>
<div class="rule" style="font-size:30px">10,000 invoices &times; &euro;2 short = <span>&euro;20,000 uncharged.</span>
<div style="font-size:21px;color:#8B949E;font-weight:400;margin-top:8px">Illustrative math</div></div>
{FOOT.format(tag="People pick the numbers")}
</div>"""

THU = f"""{X}<div class="card">
<div class="kicker">PHP security release &middot; Oct 21</div>
<h1 style="font-size:70px">Patched PHP? <em>3 places the old version survives.</em></h1>
<div class="vers"><div class="ver">8.5.12</div><div class="ver">8.4.27</div><div class="ver">8.3.36</div><div class="ver">8.2.35</div><div class="ver old">&le; 8.1: no php.net fix</div></div>
<div class="note" style="margin-top:14px">CVE-2026-109618 &amp; CVE-2026-109619 &middot; CVSS v4 9.2 &middot; source: php.net</div>
<div class="list">
<div class="row"><div class="n">1</div><div><div class="t">Auto-updates</div><div class="d">PHP from a PPA like ondrej/php isn&rsquo;t patched by Ubuntu&rsquo;s unattended upgrades by default.</div></div></div>
<div class="row"><div class="n">2</div><div><div class="t">FPM, not just the CLI</div><div class="d"><code>php -v</code> is the CLI. Check <code>php-fpm8.4 -v</code> and restart the FPM service.</div></div></div>
<div class="row"><div class="n">3</div><div><div class="t">Long-running processes</div><div class="d">Queue workers, Horizon, Octane, Reverb keep the old PHP until restarted.</div></div></div>
</div>
{FOOT.format(tag="Every server, every PHP version")}
</div>"""


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, body in [("1-mon-job-inside-transaction", MON), ("3-wed-ai-tests-expected-values", WED),
                           ("4-thu-php-patch-check", THU)]:
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
