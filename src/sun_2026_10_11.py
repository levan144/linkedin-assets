"""Sunday 2026-10-11 post: check 4 things before paying for a redesign (business owners)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "2026-10-06"

FOOT = """<div class="foot"><div class="who"><div class="av">L</div><div>
<div class="name">Levan</div><div class="role">Full-stack developer</div></div></div>
<div class="tag">{tag}</div></div>"""

ROWS = [
    ("Speed on a phone", "Run your homepage through PageSpeed Insights (free). Look at the mobile result, not desktop."),
    ("Which pages bring visitors", "Google Search Console (free) shows the pages people find you through. Those must survive any redesign."),
    ("Buy something yourself", "On your phone, as a new customer. Count the taps from product to paid. Note every moment you hesitate."),
    ("Your last backup", "Ask: when was it made, where is it, and has anyone ever restored it?"),
]

rows = "".join(
    f"""<div class="row"><div class="n">{i}</div><div>
<div class="t">{t}</div><div class="d">{d}</div></div></div>"""
    for i, (t, d) in enumerate(ROWS, start=1)
)

STYLE = """<style>
.list{display:flex;flex-direction:column;gap:16px;margin-top:36px}
.row{display:flex;gap:24px;background:#161B22;border:1px solid #262C36;border-radius:20px;padding:22px 28px}
.n{flex:none;width:54px;height:54px;border-radius:14px;background:#FF5A45;color:#0E1117;font-weight:800;
  font-size:27px;display:flex;align-items:center;justify-content:center}
.t{font-size:33px;font-weight:800;color:#fff;line-height:1.2}
.d{font-size:24px;line-height:1.4;color:#AEB6BF;margin-top:8px}
.out{margin-top:28px;font-size:29px;line-height:1.4;color:#C9D1D9}
.out b{color:#5FE0A5}
</style>"""

CARD = f"""{STYLE}<div class="card">
<div class="kicker">For business owners</div>
<h1 style="font-size:74px">Before you pay for a <em>new website,</em> check these 4 things.</h1>
<div class="list">{rows}</div>
<div class="out">Free. About 20 minutes. Often the answer is <b>fix, not rebuild.</b></div>
{FOOT.format(tag="Save before your next redesign")}
</div>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(page(CARD))
    pg.wait_for_timeout(150)
    pg.screenshot(path=str(OUT / "7-sun-before-redesign.png"),
                  clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
    b.close()
print("ok")
