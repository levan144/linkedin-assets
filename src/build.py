"""Render LinkedIn week-1 visuals (1080x1350) to PNG + carousel PDF."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
@page{size:1080px 1350px;margin:0}
body{background:#0E1117;font-family:'Inter',sans-serif;color:#E8E6E3}
.card{width:1080px;height:1350px;padding:84px 84px 64px;display:flex;flex-direction:column;
  background:radial-gradient(circle at 92% 6%,rgba(255,90,69,.16),transparent 38%),#0E1117;
  position:relative;overflow:hidden;page-break-after:always}
.kicker{font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#FF5A45;margin-bottom:26px}
h1{font-family:'Inter Display','Inter';font-weight:800;font-size:82px;line-height:1.04;letter-spacing:-.02em;color:#fff}
h1 em{font-style:normal;color:#FF5A45}
.sub{font-size:32px;line-height:1.4;color:#9AA3AE;margin-top:24px}
.label{display:inline-flex;align-items:center;gap:12px;font-size:22px;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;padding:9px 18px;border-radius:999px;margin-bottom:16px}
.bad{background:rgba(255,90,69,.14);color:#FF8A78}
.good{background:rgba(63,207,142,.14);color:#5FE0A5}
.neutral{background:rgba(154,163,174,.14);color:#C3CAD2}
pre{font-family:'DejaVu Sans Mono',monospace;font-size:25px;line-height:1.55;background:#161B22;
  border:1px solid #262C36;border-radius:22px;padding:30px 34px;color:#E6EDF3;white-space:pre}
.k{color:#FF7B72}.s{color:#A5D6FF}.f{color:#D2A8FF}.v{color:#FFA657}.c{color:#7D8590}.a{color:#7EE787}
.note{font-size:26px;color:#9AA3AE;margin-top:14px}
.note b{color:#fff}
.block{margin-top:40px}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between;padding-top:28px;
  border-top:1px solid #222833}
.who{display:flex;align-items:center;gap:18px}
.av{width:62px;height:62px;border-radius:50%;background:#FF5A45;color:#0E1117;font-weight:800;font-size:30px;
  display:flex;align-items:center;justify-content:center}
.name{font-size:26px;font-weight:700;color:#fff}.role{font-size:21px;color:#8B949E}
.tag{font-size:21px;color:#8B949E}
.flow{display:flex;flex-direction:column;gap:18px;margin-top:44px}
.step{display:flex;gap:24px;align-items:flex-start;background:#161B22;border:1px solid #262C36;border-radius:20px;padding:24px 28px}
.num{flex:none;width:52px;height:52px;border-radius:14px;background:#222833;color:#fff;font-weight:800;font-size:26px;
  display:flex;align-items:center;justify-content:center}
.step p{font-size:28px;line-height:1.38;color:#C9D1D9}.step b{color:#fff}
.step.alert{border-color:rgba(255,90,69,.6);background:rgba(255,90,69,.08)}
.step.alert .num{background:#FF5A45;color:#0E1117}
.mono{font-family:'DejaVu Sans Mono',monospace;font-size:25px;color:#A5D6FF}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:48px}
.col{background:#161B22;border:1px solid #262C36;border-radius:22px;padding:32px}
.col h3{font-size:34px;font-weight:800;color:#fff;margin:6px 0 20px}
.col li{list-style:none;font-size:27px;line-height:1.35;color:#C9D1D9;padding:12px 0 12px 34px;position:relative}
.col li:before{content:"";position:absolute;left:4px;top:24px;width:12px;height:12px;border-radius:3px;background:currentColor;opacity:.5}
.quote{font-family:'Inter Display','Inter';font-weight:800;font-size:58px;line-height:1.12;color:#fff;margin-top:52px}
.quote em{font-style:normal;color:#FF5A45}
/* carousel */
.big{font-family:'Inter Display','Inter';font-weight:800;font-size:290px;line-height:.9;color:#FF5A45;letter-spacing:-.04em}
.slide-h{font-family:'Inter Display','Inter';font-weight:800;font-size:88px;line-height:1.06;color:#fff;margin-top:24px;letter-spacing:-.015em}
.why{font-size:37px;line-height:1.45;color:#9AA3AE;margin-top:30px}
.do{margin-top:40px;background:#161B22;border:1px solid #262C36;border-left:6px solid #5FE0A5;border-radius:18px;padding:28px 32px}
.do .t{font-size:24px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#5FE0A5;margin-bottom:12px}
.do p{font-size:34px;line-height:1.45;color:#E6EDF3}
.page{font-size:22px;color:#8B949E}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.swipe{font-size:36px;font-weight:700;color:#FF5A45}
"""

FOOT = """<div class="foot"><div class="who"><div class="av">L</div><div>
<div class="name">Levan</div><div class="role">Laravel &amp; WooCommerce developer</div></div></div>
<div class="tag">{tag}</div></div>"""


def page(body: str) -> str:
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


MON = f"""<div class="card">
<div class="kicker">Laravel &middot; HTTP client</div>
<h1>Stop calling APIs <em>one by one.</em></h1>
<div class="block" style="margin-top:34px"><span class="label bad">Sequential</span>
<pre><span class="k">foreach</span> (<span class="v">$ids</span> <span class="k">as</span> <span class="v">$id</span>) {{
    <span class="v">$responses</span>[] = Http::<span class="f">get</span>(
        <span class="s">"<span class="v">$api</span>/products/<span class="v">$id</span>"</span>
    );
}}</pre>
<div class="note">10 calls &times; 500 ms = <b>~5 s of waiting</b></div></div>
<div class="block" style="margin-top:30px"><span class="label good">Parallel &middot; Http::pool()</span>
<pre><span class="v">$responses</span> = Http::<span class="f">pool</span>(
    <span class="k">fn</span> (Pool <span class="v">$pool</span>) =&gt; <span class="f">collect</span>(<span class="v">$ids</span>)
        -&gt;<span class="f">map</span>(<span class="k">fn</span> (<span class="v">$id</span>) =&gt; <span class="v">$pool</span>-&gt;<span class="f">get</span>(
            <span class="s">"<span class="v">$api</span>/products/<span class="v">$id</span>"</span>
        ))-&gt;<span class="f">all</span>(),
    concurrency: <span class="v">5</span>
);</pre>
<div class="note">10 calls, 5 at a time = <b>~1 s total</b></div></div>
{FOOT.format(tag="Save for your next sync job")}
</div>"""

TUE = f"""<div class="card">
<div class="kicker">API sync &middot; debugging</div>
<h1>The bug that skips <em>5 hours</em> of updates.</h1>
<div class="sub">No error. No log entry. Just wrong stock.</div>
<div class="flow">
<div class="step"><div class="num">1</div><p><b>Your server (UTC)</b> saves last sync time:<br><span class="mono">14:00</span></p></div>
<div class="step"><div class="num">2</div><p>Next run asks the other system:<br><span class="mono">changed_since=14:00</span> &nbsp;(no timezone)</p></div>
<div class="step"><div class="num">3</div><p><b>Other system (UTC&minus;5)</b> reads it as local time<br>= <b>19:00 UTC</b></p></div>
<div class="step alert"><div class="num">!</div><p><b>Everything changed 14:00&ndash;19:00 UTC never syncs.</b></p></div>
</div>
<div class="block" style="margin-top:34px"><span class="label good">Fix</span>
<pre><span class="v">$since</span>-&gt;<span class="f">copy</span>()
    -&gt;<span class="f">setTimezone</span>(<span class="f">config</span>(<span class="s">'services.erp.tz'</span>))
    -&gt;<span class="f">format</span>(<span class="s">'Y-m-d H:i:s'</span>);</pre></div>
{FOOT.format(tag="Check time before code")}
</div>"""

THU = f"""<div class="card">
<div class="kicker">Laravel 13 &middot; Queues</div>
<h1>Job config moves <em>into attributes.</em></h1>
<div class="block" style="margin-top:34px"><span class="label neutral">Laravel 12</span>
<pre><span class="k">class</span> <span class="f">SyncProducts</span> <span class="k">implements</span> ShouldQueue {{
    <span class="k">public int</span> <span class="v">$tries</span> = <span class="v">5</span>;
    <span class="k">public int</span> <span class="v">$timeout</span> = <span class="v">120</span>;
}}</pre></div>
<div class="block" style="margin-top:28px"><span class="label good">Laravel 13</span>
<pre><span class="a">#[Tries(5)]</span>
<span class="a">#[Timeout(120)]</span>
<span class="a">#[FailOnTimeout]</span>
<span class="k">class</span> <span class="f">SyncProducts</span> <span class="k">implements</span> ShouldQueue {{}}</pre></div>
<div class="block" style="margin-top:28px"><span class="label good">New &middot; Queue::route()</span>
<pre><span class="c">// AppServiceProvider::boot()</span>
Queue::<span class="f">route</span>(SyncProducts::<span class="k">class</span>,
    connection: <span class="s">'redis'</span>, queue: <span class="s">'sync'</span>);</pre></div>
{FOOT.format(tag="Property style still works")}
</div>"""

FRI = f"""<div class="card">
<div class="kicker">Opinion</div>
<h1>WooCommerce or <em>custom Laravel?</em></h1>
<div class="cols">
<div class="col"><span class="label good">Pick WooCommerce</span><h3>When the store is standard</h3><ul>
<li>Normal catalog and checkout</li><li>Client edits content daily</li><li>Tight budget and timeline</li><li>Plugins cover 90% of needs</li></ul></div>
<div class="col"><span class="label bad">Pick Laravel</span><h3>When logic is the product</h3><ul>
<li>Heavy integrations (ERP, APIs)</li><li>Workflows no plugin models</li><li>Multi-tenant or SaaS</li><li>Performance at scale</li></ul></div>
</div>
<div class="quote">The skill isn&rsquo;t the framework. <em>It&rsquo;s knowing which job needs which.</em></div>
{FOOT.format(tag="Where do you draw the line?")}
</div>"""

FIXES = [
    ("Add a persistent object cache", "WooCommerce repeats the same database queries on every page load. Without an object cache, MySQL answers them again and again.", "Install Redis on the server, then the Redis Object Cache plugin. Check the hit rate in its dashboard."),
    ("Serve full-page cache to guests", "Most visitors are not logged in and see identical pages. Building them from PHP each time wastes the server.", "Cache guest pages at server level (Nginx FastCGI, LiteSpeed) and exclude cart, checkout and my-account."),
    ("Turn on HPOS", "Old order storage puts every order field in wp_postmeta, one of the busiest tables on the site.", "WooCommerce → Settings → Advanced → Features: enable High-Performance Order Storage. Test on staging first."),
    ("Replace WP-Cron with real cron", "WP-Cron runs on page visits, so heavy scheduled tasks slow down real customers.", "Set DISABLE_WP_CRON to true in wp-config.php and run wp-cron.php from a system cron every minute."),
    ("Audit plugins with Query Monitor", "One bad plugin can add hundreds of queries per page. You won’t know which without measuring.", "Install Query Monitor, open your slowest pages, sort by component, remove or replace the worst offender."),
    ("Fix your images", "Product photos are usually the heaviest part of a page, especially on mobile.", "Serve WebP or AVIF, upload at display size, and set width and height to stop layout shift."),
    ("Load cart fragments only where needed", "Some themes still request cart fragments on every page, an uncached AJAX call per visit.", "If your mini-cart doesn’t need live updates, dequeue wc-cart-fragments outside shop pages."),
]


def carousel() -> str:
    total = len(FIXES) + 2
    slides = [f"""<div class="card"><div class="mid">
<div class="kicker">WooCommerce &middot; Performance</div>
<h1 style="font-size:104px">7 fixes for a <em>slow WooCommerce store.</em></h1>
<div class="sub" style="font-size:38px;margin-top:40px">No bigger server needed.<br>In the order I&rsquo;d apply them.</div>
<div style="margin-top:70px" class="swipe">Swipe for all 7 &rarr;</div></div>
{FOOT.format(tag=f"1 / {total}")}</div>"""]
    for i, (title, why, do) in enumerate(FIXES, start=1):
        slides.append(f"""<div class="card"><div class="mid">
<div class="big">0{i}</div>
<div class="slide-h">{title}</div>
<div class="why">{why}</div>
<div class="do"><div class="t">Do this</div><p>{do}</p></div></div>
{FOOT.format(tag=f"{i + 1} / {total}")}</div>""")
    slides.append(f"""<div class="card"><div class="mid">
<div class="kicker">Recap</div>
<h1 style="font-size:100px">Start with <em>#1 and #2.</em></h1>
<div class="sub" style="font-size:36px">Object cache plus page cache fix most slow stores before you touch anything else.</div>
<div class="flow" style="margin-top:56px">
<div class="step"><div class="num">&#9733;</div><p><b>Save</b> this for your next store audit</p></div>
<div class="step"><div class="num">+</div><p><b>Follow</b> for weekly Laravel and WooCommerce lessons</p></div>
</div></div>
{FOOT.format(tag=f"{total} / {total}")}</div>""")
    return "".join(slides)


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, body in [("1-mon-http-pool", MON), ("2-tue-timezone-bug", TUE),
                           ("4-thu-laravel13-job-attributes", THU), ("5-fri-woo-vs-laravel", FRI)]:
            pg.set_content(page(body))
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(OUT / f"{name}.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        html = page(carousel())
        pg.set_content(html)
        pg.wait_for_timeout(150)
        pg.pdf(path=str(OUT / "3-wed-woo-speed-carousel.pdf"), width="1080px", height="1350px",
               print_background=True)
        # PNG previews of carousel slides for checking
        cards = pg.query_selector_all(".card")
        for i, c in enumerate(cards, start=1):
            c.screenshot(path=str(OUT / f"_wed-slide-{i}.png"))
        b.close()


if __name__ == "__main__":
    main()
