"""Week of 2026-11-09: 3 LinkedIn visuals (1080x1350). Saturday is text-only.

Reuses CSS, page() and FOOT from build.py; only content changes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "2026-11-09"
OUT.mkdir(parents=True, exist_ok=True)

X = """<style>
.rule{margin-top:30px;background:rgba(255,90,69,.08);border:1px solid rgba(255,90,69,.55);border-radius:20px;
  padding:24px 30px;font-size:30px;font-weight:800;color:#fff;line-height:1.3}
.rule span{color:#FF5A45}
.list{display:flex;flex-direction:column;gap:10px;margin-top:20px}
.row{display:flex;gap:22px;background:#161B22;border:1px solid #262C36;border-radius:18px;padding:13px 22px;align-items:center}
.row.alert{border-color:rgba(255,90,69,.6);background:rgba(255,90,69,.08)}
.n{flex:none;width:46px;height:46px;border-radius:12px;background:#222833;color:#fff;font-weight:800;
  font-size:24px;display:flex;align-items:center;justify-content:center}
.row.alert .n{background:#FF5A45;color:#0E1117}
.t{font-size:27px;font-weight:800;color:#fff;line-height:1.25}
.d{font-size:23px;line-height:1.4;color:#AEB6BF;margin-top:4px;font-family:'DejaVu Sans Mono',monospace}
pre{font-size:24px}
.col li{font-size:26px}
</style>"""

TUE = f"""{X}<div class="card">
<div class="kicker">PHP &middot; Money</div>
<h1 style="font-size:84px">(int) (19.99 * 100) <em>is 1998.</em></h1>
<div class="block" style="margin-top:36px"><span class="label bad">Charges one cent less</span>
<pre><span class="v">$amount</span> = (<span class="k">int</span>) (<span class="v">$order</span>-&gt;total * <span class="a">100</span>); <span class="c">// 1998</span>

<span class="c">// 19.99 * 100 = 1998.9999999999998</span>
<span class="c">// (int) cuts toward zero</span></pre>
<div class="note">DECIMAL column? Eloquent returns <b>"19.99"</b> &rarr; same result.</div></div>
<div class="block" style="margin-top:30px"><span class="label good">Round, or never use floats</span>
<pre><span class="v">$amount</span> = (<span class="k">int</span>) <span class="f">round</span>(<span class="v">$order</span>-&gt;total * <span class="a">100</span>); <span class="c">// 1999</span>

<span class="c">// better: store integer cents</span>
<span class="c">// tax/discount math: money lib or bcmath</span></pre></div>
<div class="rule">10.99 converts fine. 19.99 doesn&rsquo;t. <span>&ldquo;Nice&rdquo; test prices pass.</span></div>
{FOOT.format(tag="Run it yourself")}
</div>"""

WED = f"""{X}<div class="card">
<div class="kicker">AI &middot; Migrations</div>
<h1 style="font-size:60px">AI writes migrations against your schema, <em>not your data.</em></h1>
<div class="block" style="margin-top:24px">
<pre style="font-size:23px;padding:24px 30px"><span class="f">Schema</span>::<span class="f">table</span>(<span class="s">'users'</span>, <span class="k">function</span> (Blueprint <span class="v">$table</span>) {{
    <span class="v">$table</span>-&gt;<span class="f">string</span>(<span class="s">'phone'</span>)-&gt;<span class="f">nullable</span>();
    <span class="v">$table</span>-&gt;<span class="f">unique</span>(<span class="s">'email'</span>);
}});</pre></div>
<div class="list">
<div class="row"><div class="n">1</div><div class="t">phone column added &mdash; committed (MySQL)</div></div>
<div class="row alert"><div class="n">2</div><div><div class="t">unique(email) fails</div><div class="d">1062 Duplicate entry &middot; old import</div></div></div>
<div class="row"><div class="n">3</div><div class="t">Migration not marked as run</div></div>
<div class="row alert"><div class="n">4</div><div><div class="t">Next deploy fails too</div><div class="d">Duplicate column name 'phone'</div></div></div>
</div>
<div class="block" style="margin-top:20px"><span class="label good">Run on a production copy first</span>
<pre style="font-size:22px"><span class="k">SELECT</span> email, <span class="f">COUNT</span>(*) <span class="k">FROM</span> users
<span class="k">WHERE</span> email <span class="k">IS NOT NULL</span>
<span class="k">GROUP BY</span> email <span class="k">HAVING</span> <span class="f">COUNT</span>(*) &gt; <span class="a">1</span>;</pre></div>
{FOOT.format(tag="Give the AI the data")}
</div>"""

THU = f"""{X}<div class="card">
<div class="kicker">Laravel &middot; Hot take</div>
<h1 style="font-size:76px">SoftDeletes shouldn&rsquo;t be <em>a default.</em></h1>
<div class="block" style="margin-top:34px"><span class="label bad">1 &middot; Deleted user signs up again</span>
<pre><span class="c">// rule: "email already taken"</span>
<span class="c">// no rule: 1062 Duplicate entry</span>
<span class="c">// (email, deleted_at)? NULLs never collide</span></pre></div>
<div class="block" style="margin-top:22px"><span class="label bad">2 &middot; Only Eloquent hides it</span>
<pre>DB::<span class="f">table</span>(<span class="s">'orders'</span>)-&gt;<span class="f">sum</span>(<span class="s">'total'</span>);
<span class="c">// includes deleted orders</span></pre></div>
<div class="cols" style="margin-top:22px">
<div class="col"><span class="label good">Instead</span><ul>
<li>Hard delete by default</li><li>SoftDeletes where users need undo</li><li>Orders: status = cancelled</li></ul></div>
<div class="col"><span class="label neutral">Where I&rsquo;d be wrong</span><ul>
<li>Admin panels that restore records weekly</li></ul></div>
</div>
{FOOT.format(tag="Default, or on request?")}
</div>"""


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, body in [("1-mon-int-cast-money", TUE), ("3-wed-ai-migration-data", WED),
                           ("4-thu-soft-deletes", THU)]:
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
