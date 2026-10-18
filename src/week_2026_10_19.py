"""Week of 2026-10-19: 6 LinkedIn visuals (1080x1350) + Wednesday carousel PDF.

Reuses CSS, page() and FOOT from build.py; only content changes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "2026-10-19"
OUT.mkdir(parents=True, exist_ok=True)

X = """<style>
.list{display:flex;flex-direction:column;gap:16px;margin-top:40px}
.row{display:flex;gap:24px;background:#161B22;border:1px solid #262C36;border-radius:20px;padding:22px 28px}
.n{flex:none;width:54px;height:54px;border-radius:14px;background:#FF5A45;color:#0E1117;font-weight:800;
  font-size:27px;display:flex;align-items:center;justify-content:center}
.t{font-size:31px;font-weight:800;color:#fff;line-height:1.25}
.d{font-size:24px;line-height:1.4;color:#AEB6BF;margin-top:8px}
.d b{color:#5FE0A5;font-weight:700}
.rule{margin-top:34px;background:rgba(255,90,69,.08);border:1px solid rgba(255,90,69,.55);border-radius:20px;
  padding:26px 30px;font-size:34px;font-weight:800;color:#fff;line-height:1.3}
.rule span{color:#FF5A45}
.chain{display:flex;flex-direction:column;gap:8px;margin-top:32px}
.node{background:#161B22;border:1px solid #262C36;border-radius:16px;padding:18px 26px;font-size:30px;color:#fff;font-weight:700}
.node small{display:block;font-size:22px;color:#8B949E;font-weight:400;margin-top:4px}
.node.alert{border-color:rgba(255,90,69,.6);background:rgba(255,90,69,.08)}
.arrow{font-size:28px;color:#FF5A45;padding-left:30px;line-height:1}
.reply{margin-top:40px;background:#161B22;border:1px solid #262C36;border-left:6px solid #5FE0A5;border-radius:20px;padding:30px 34px}
.reply .q{font-size:36px;font-weight:800;color:#fff;line-height:1.3;margin-bottom:22px}
.kv{display:flex;gap:20px;align-items:baseline;padding:16px 0;border-top:1px solid #262C36}
.kv .k2{flex:none;width:170px;font-size:24px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#5FE0A5}
.kv .v2{font-size:32px;color:#E6EDF3;line-height:1.3}
.pair{background:#161B22;border:1px solid #262C36;border-radius:20px;padding:16px 26px}
.pair .says{font-size:25px;color:#FF8A78;line-height:1.35}
.pair .says b{font-size:19px;letter-spacing:.08em;text-transform:uppercase;color:#8B949E;font-weight:700;display:block;margin-bottom:4px}
.pair .needs{font-size:26px;color:#fff;font-weight:700;line-height:1.3;margin-top:8px}
.pair .needs b{font-size:19px;letter-spacing:.08em;text-transform:uppercase;color:#5FE0A5;font-weight:700;display:block;margin-bottom:4px}
.cols .col li{font-size:26px}
.big2{font-family:'Inter Display','Inter';font-weight:800;font-size:58px;color:#fff;line-height:1.1}
.col .big2 small{display:block;font-size:24px;color:#8B949E;font-weight:400;margin-top:8px}
</style>"""

# ---------------------------------------------------------------- MON
MON = f"""{X}<div class="card">
<div class="kicker">Freelance &middot; Scope changes</div>
<h1 style="font-size:78px">Never answer a new idea with <em>&ldquo;sure, no problem.&rdquo;</em></h1>
<div class="sub" style="font-size:30px">Reply the same way to every new request. In writing.</div>
<div class="reply"><div class="q">&ldquo;Yes, we can add that. Here&rsquo;s what it changes:&rdquo;</div>
<div class="kv"><div class="k2">Cost</div><div class="v2">+&euro;300</div></div>
<div class="kv"><div class="k2">Launch</div><div class="v2">moves from the 14th to the 18th</div></div>
<div class="kv"><div class="k2">Or swap</div><div class="v2">drop something on the list, and nothing moves</div></div>
</div>
<div class="note" style="margin-top:16px">Example numbers. The format is the point.</div>
<div class="rule">Show the trade-off. <span>Let the client choose.</span></div>
{FOOT.format(tag="Save for the next &ldquo;can we just add&hellip;&rdquo;")}
</div>"""

# ---------------------------------------------------------------- TUE
PAIRS = [
    ("&ldquo;Must have&rdquo; &times; 40 features", "Tag each one: launch, later, or drop"),
    ("&ldquo;Integrate with our accounting system&rdquo;", "&ldquo;When an order is paid, the invoice appears in accounting.&rdquo;"),
    ("&ldquo;A simple customer dashboard&rdquo;", "&ldquo;Customers see past orders and can change their address.&rdquo;"),
    ("(nothing about after launch)", "Who updates it, who pays hosting, who answers when it breaks"),
]
prows = "".join(f"""<div class="pair"><div class="says"><b>The AI brief says</b>{a}</div>
<div class="needs"><b>Ask for</b>{b}</div></div>""" for a, b in PAIRS)
TUE = f"""{X}<div class="card">
<div class="kicker">AI &middot; Project briefs</div>
<h1 style="font-size:62px">A brief with 40 &ldquo;must-haves&rdquo; <em>has no priorities.</em></h1>
<div class="list" style="margin-top:28px;gap:12px">{prows}</div>
<div class="rule" style="font-size:31px">Quote the launch list. <span>Price the rest later.</span></div>
{FOOT.format(tag="Clients and developers: save this")}
</div>"""

# ---------------------------------------------------------------- WED carousel
SLIDES = [
    ("Updates",
     "WordPress, plugins and theme, or your platform&rsquo;s apps. Done regularly, and tested on a copy of the site before they touch the real one.",
     "Do you test updates before they go live?"),
    ("Backups",
     "Made every day, stored away from your server, and restored at least once to prove they work.",
     "When did you last restore one?"),
    ("Security",
     "Old admin accounts removed. 2-step login for everyone with admin access. Unused plugins and apps deleted.",
     "Who has admin access right now?"),
    ("Monitoring",
     "An alert goes to a person when the site goes down or starts showing errors. Before a customer tells you.",
     "How will you know the site is down at 3am?"),
    ("Renewals",
     "Your domain, registered in your name. The padlock certificate now lasts 200 days at most, and about 100 from March 2027. Miss it, and visitors see a security warning.",
     "Is renewal automatic, and who gets the warning email?"),
    ("Small changes",
     "A set number of hours each month for text, images and small fixes. Written down, so nobody argues later.",
     "How many hours are included, and what counts as &ldquo;small&rdquo;?"),
    ("Response time",
     "&ldquo;Checkout is broken&rdquo; and &ldquo;typo on the About page&rdquo; are different jobs. Each needs a promised reply time.",
     "How fast do you reply when checkout breaks?"),
]


def carousel() -> str:
    total = len(SLIDES) + 2
    names = "".join(f'<div class="step"><div class="num">{i}</div><p><b>{t}</b></p></div>'
                    for i, (t, _, _) in enumerate(SLIDES, start=1))
    out = [f"""{X}<div class="card"><div class="mid">
<div class="kicker">For business owners &middot; Explained simply</div>
<h1 style="font-size:96px">What you&rsquo;re paying for in <em>website maintenance</em></h1>
<div class="sub" style="font-size:34px;margin-top:32px">7 things a good plan covers, and one question to ask about each.</div>
<div class="rule" style="margin-top:50px;font-size:34px">If it&rsquo;s not written down, <span>it&rsquo;s not included.</span></div>
<div style="margin-top:50px" class="swipe">Swipe for all 7 &rarr;</div></div>
{FOOT.format(tag=f"1 / {total}")}</div>"""]
    for i, (title, why, ask) in enumerate(SLIDES, start=1):
        out.append(f"""<div class="card"><div class="mid">
<div class="big" style="font-size:220px">0{i}</div>
<div class="slide-h" style="font-size:96px">{title}</div>
<div class="why" style="font-size:38px">{why}</div>
<div class="do"><div class="t">Ask</div><p>&ldquo;{ask}&rdquo;</p></div></div>
{FOOT.format(tag=f"{i + 1} / {total}")}</div>""")
    out.append(f"""<div class="card"><div class="mid">
<div class="kicker">Recap</div>
<h1 style="font-size:80px">A good plan covers <em>all 7.</em></h1>
<div class="flow" style="margin-top:36px;gap:12px">{names}</div>
<div class="sub" style="font-size:30px;margin-top:30px"><b style="color:#fff">Save</b> this for the next time you review your plan.</div>
</div>
{FOOT.format(tag=f"{total} / {total}")}</div>""")
    return "".join(out)


# ---------------------------------------------------------------- THU
THU = f"""{X}<div class="card">
<div class="kicker">Hot take &middot; WordPress</div>
<h1 style="font-size:74px">Headless WordPress is wrong for <em>most small businesses.</em></h1>
<div class="cols" style="margin-top:40px">
<div class="col"><span class="label good">Standard WordPress</span><ul>
<li>One system to host, update and secure</li>
<li>Forms, SEO and page builders work out of the box</li>
<li>Preview built in</li>
<li>Most WordPress developers can take it over</li></ul></div>
<div class="col"><span class="label bad">Headless</span><ul>
<li>Two systems to host, update and secure</li>
<li>Each plugin needs custom work</li>
<li>Preview has to be rebuilt</li>
<li>Fewer developers can take it over</li></ul></div>
</div>
<div class="rule" style="font-size:31px">Go headless when you can <span>name the problem it solves.</span></div>
{FOOT.format(tag="Disagree? Tell me where")}
</div>"""

# ---------------------------------------------------------------- FRI
FRI = f"""{X}<div class="card">
<div class="kicker">This month &middot; Store security</div>
<h1 style="font-size:68px">Hijacked apps sent shoppers to <em>fake checkouts.</em></h1>
<div class="chain">
<div class="node">Shopper clicks &ldquo;Checkout&rdquo;</div><div class="arrow">&darr;</div>
<div class="node alert">A hijacked app script on the store page<small>Reported in several third-party Shopify apps this month</small></div><div class="arrow">&darr;</div>
<div class="node alert">Fake payment page on an outside domain</div></div>
<div class="label neutral" style="margin-top:26px">Check your store today</div>
<div class="list" style="margin-top:4px;gap:12px">
<div class="row"><div class="n">1</div><div class="t" style="font-size:28px">Remove apps you haven&rsquo;t used this month</div></div>
<div class="row"><div class="n">2</div><div class="t" style="font-size:28px">Private window &rarr; cart &rarr; Checkout. Check the address bar.</div></div>
<div class="row"><div class="n">3</div><div class="t" style="font-size:28px">2-step login on your store and app accounts</div></div>
</div>
{FOOT.format(tag="Check your store today")}
</div>"""

# ---------------------------------------------------------------- SAT
SAT = f"""{X}<div class="card">
<div class="kicker">This or that</div>
<h1 style="font-size:108px">Fixed price <em>or</em> hourly?</h1>
<div class="sub" style="font-size:32px">Example: a job estimated at 20 hours.</div>
<div class="cols" style="margin-top:40px">
<div class="col"><span class="label neutral">Fixed</span><div class="big2">~25 h<small>quoted, with a cushion for risk</small></div>
<p style="font-size:27px;line-height:1.4;color:#C9D1D9;margin-top:24px">You know the cost upfront. <b style="color:#fff">Risk sits with the freelancer.</b></p></div>
<div class="col"><span class="label neutral">Hourly</span><div class="big2">20&ndash;35 h<small>depending on surprises</small></div>
<p style="font-size:27px;line-height:1.4;color:#C9D1D9;margin-top:24px">You pay for what happens. <b style="color:#fff">Risk sits with you.</b></p></div>
</div>
<div class="sub" style="margin-top:40px;font-size:36px;color:#fff;font-weight:700">Reply &ldquo;fixed&rdquo; or &ldquo;hourly&rdquo;, and one reason.</div>
<div class="note" style="margin-top:12px">Illustrative numbers.</div>
{FOOT.format(tag="Clients and freelancers both")}
</div>"""

# ---------------------------------------------------------------- SUN
SUN = f"""{X}<div class="card">
<div class="kicker">A bug that teaches &middot; Reports</div>
<h1 style="font-size:76px">This report looks right. <em>It&rsquo;s missing a day.</em></h1>
<div class="block" style="margin-top:36px"><span class="label bad">October&rsquo;s orders?</span>
<pre><span class="k">WHERE</span> created_at
  <span class="k">BETWEEN</span> <span class="s">'2026-10-01'</span> <span class="k">AND</span> <span class="s">'2026-10-31'</span></pre>
<div class="note">'2026-10-31' = <b>midnight at the start</b> of Oct 31. Orders later that day are left out. No error.</div></div>
<div class="block" style="margin-top:28px"><span class="label good">Include the start, exclude the next start</span>
<pre><span class="k">WHERE</span> created_at &gt;= <span class="s">'2026-10-01'</span>
  <span class="k">AND</span> created_at &lt;  <span class="s">'2026-11-01'</span></pre></div>
<div class="rule" style="font-size:30px">&euro;31,000 month, spread evenly: <span>about &euro;1,000 missing.</span></div>
{FOOT.format(tag="Check the edges first")}
</div>"""


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, body in [("1-mon-scope-change-reply", MON), ("2-tue-ai-written-briefs", TUE),
                           ("4-thu-headless-wordpress", THU), ("5-fri-hijacked-shop-apps", FRI),
                           ("6-sat-fixed-or-hourly", SAT), ("7-sun-between-last-day", SUN)]:
            pg.set_content(page(body))
            pg.wait_for_timeout(200)
            over = pg.evaluate("""() => [...document.querySelectorAll('.card')].map(c => {
                const f = c.querySelector('.foot'); const kids = [...c.children].filter(k => k !== f && k.tagName !== 'STYLE');
                const last = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
                return {gap: Math.round(f.getBoundingClientRect().top - last), sh: c.scrollHeight};})""")
            print(name, over)
            pg.screenshot(path=str(OUT / f"{name}.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        pg.set_content(page(carousel()))
        pg.wait_for_timeout(200)
        pg.pdf(path=str(OUT / "3-wed-maintenance-carousel.pdf"), width="1080px", height="1350px",
               print_background=True)
        prev = Path(__file__).resolve().parent / "out"
        prev.mkdir(exist_ok=True)
        for i, c in enumerate(pg.query_selector_all(".card"), start=1):
            c.screenshot(path=str(prev / f"_wed-slide-{i}.png"))
            if i == 1:
                c.screenshot(path=str(OUT / "3-wed-carousel-cover.png"))
        print("sh", pg.evaluate("[...document.querySelectorAll('.card')].map(c=>c.scrollHeight)"))
        b.close()


if __name__ == "__main__":
    main()
