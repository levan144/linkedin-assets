"""Week of 2026-11-16: 2 LinkedIn visuals (1080x1350). Wed and Sat are text-only.

Reuses CSS, page() and FOOT from build.py; only content changes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "2026-11-16"
OUT.mkdir(parents=True, exist_ok=True)

X = """<style>
.rule{margin-top:30px;background:rgba(255,90,69,.08);border:1px solid rgba(255,90,69,.55);border-radius:20px;
  padding:24px 30px;font-size:30px;font-weight:800;color:#fff;line-height:1.3}
.rule span{color:#FF5A45}
.dates{display:flex;gap:14px;margin-top:18px}
.dt{flex:1;background:#161B22;border:1px solid #262C36;border-radius:16px;padding:14px 10px;text-align:center}
.dt .m{font-size:22px;color:#AEB6BF;font-weight:700}
.dt .v{font-size:34px;color:#fff;font-weight:800;margin-top:4px;font-family:'DejaVu Sans Mono',monospace}
.dt.bad{border-color:rgba(255,90,69,.6);background:rgba(255,90,69,.08)}
.dt.bad .v{color:#FF5A45}
pre{font-size:25px}
.col li{font-size:26px}
</style>"""

MON = f"""{X}<div class="card">
<div class="kicker">PHP &middot; Dates &middot; Billing</div>
<h1 style="font-size:70px;white-space:nowrap">Jan 31 + 1 month <em>= March 3.</em></h1>
<div class="block" style="margin-top:50px"><span class="label bad">Chained addMonth()</span>
<pre><span class="v">$sub</span>-&gt;next_billing_at =
    <span class="v">$sub</span>-&gt;next_billing_at-&gt;<span class="f">addMonth</span>();</pre>
<div class="dates">
<div class="dt"><div class="m">Start</div><div class="v">Jan 31</div></div>
<div class="dt bad"><div class="m">February</div><div class="v">&mdash;</div></div>
<div class="dt bad"><div class="m">Next</div><div class="v">Mar 3</div></div>
<div class="dt bad"><div class="m">Then</div><div class="v">Apr 3</div></div>
</div></div>
<div class="block" style="margin-top:50px"><span class="label good">From the start date, no overflow</span>
<pre><span class="v">$sub</span>-&gt;next_billing_at = <span class="v">$sub</span>-&gt;started_at
    -&gt;<span class="f">copy</span>()-&gt;<span class="f">addMonthsNoOverflow</span>(<span class="v">$n</span>);</pre>
<div class="dates">
<div class="dt"><div class="m">Start</div><div class="v">Jan 31</div></div>
<div class="dt"><div class="m">n = 1</div><div class="v">Feb 28</div></div>
<div class="dt"><div class="m">n = 2</div><div class="v">Mar 31</div></div>
<div class="dt"><div class="m">n = 3</div><div class="v">Apr 30</div></div>
</div></div>
<div class="rule" style="margin-top:46px">Test the 31st and leap years. <span>The 1st and the 15th always pass.</span></div>
{FOOT.format(tag="Run it yourself")}
</div>"""

THU = f"""{X}<div class="card">
<div class="kicker">Laravel &middot; Queues &middot; Hot take</div>
<h1 style="font-size:72px">Most small apps don&rsquo;t need <em>Redis for queues.</em></h1>
<div class="block" style="margin-top:30px"><span class="label neutral">Default in new Laravel apps</span>
<pre><span class="c"># .env</span>
QUEUE_CONNECTION=<span class="s">database</span>

<span class="c"># jobs table migration ships with the skeleton</span></pre></div>
<div class="cols" style="margin-top:28px">
<div class="col"><span class="label good">Stay on database</span><ul>
<li>Order emails, stock syncs, image jobs</li><li>One less service to run and pay for</li><li>Read stuck jobs with plain SQL</li></ul></div>
<div class="col"><span class="label bad">Move to Redis</span><ul>
<li>Thousands of jobs per minute</li><li>You want Horizon (Redis only)</li><li>Queue queries in the slow log</li></ul></div>
</div>
<div class="rule">Measure first. <span>Switch when the slow query log says so.</span></div>
{FOOT.format(tag="Database, or Redis?")}
</div>"""


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, body in [("1-mon-month-overflow", MON), ("4-thu-database-queue", THU)]:
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
