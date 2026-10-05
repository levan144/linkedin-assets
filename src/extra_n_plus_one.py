"""One-off post: preventLazyLoading (N+1). Reuses styles from build.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "extra" / "2026-10-05"
OUT.mkdir(parents=True, exist_ok=True)

CARD = f"""<div class="card">
<div class="kicker">Laravel &middot; Eloquent</div>
<h1>Catch N+1 queries <em>before your users do.</em></h1>
<div class="block" style="margin-top:34px"><span class="label bad">The trap</span>
<pre><span class="v">$orders</span> = Order::<span class="f">all</span>();

<span class="k">foreach</span> (<span class="v">$orders</span> <span class="k">as</span> <span class="v">$order</span>) {{
    <span class="k">echo</span> <span class="v">$order</span>-&gt;customer-&gt;name;
}}</pre>
<div class="note">100 orders = <b>101 queries</b></div></div>
<div class="block" style="margin-top:28px"><span class="label good">One line &middot; AppServiceProvider::boot()</span>
<pre>Model::<span class="f">preventLazyLoading</span>(
    ! <span class="v">$this</span>-&gt;app-&gt;<span class="f">isProduction</span>()
);</pre>
<div class="note">Lazy load in dev &rarr; <b>exception</b>. Production stays safe.</div></div>
<div class="block" style="margin-top:28px"><span class="label neutral">The fix</span>
<pre>Order::<span class="f">with</span>(<span class="s">'customer'</span>)-&gt;<span class="f">get</span>(); <span class="c">// 2 queries</span></pre></div>
{FOOT.format(tag="Save this for your next project")}
</div>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(page(CARD))
    pg.wait_for_timeout(150)
    pg.screenshot(path=str(OUT / "laravel-prevent-lazy-loading.png"),
                  clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
    b.close()
print("ok")
