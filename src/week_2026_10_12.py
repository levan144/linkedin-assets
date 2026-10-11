"""Week of 2026-10-12: 7 LinkedIn visuals (1080x1350) + Wednesday carousel PDF.

Reuses CSS, page() and FOOT from build.py; only content changes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import page, FOOT  # noqa: E402
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "2026-10-12"
OUT.mkdir(parents=True, exist_ok=True)

X = """<style>
.list{display:flex;flex-direction:column;gap:16px;margin-top:40px}
.row{display:flex;gap:24px;background:#161B22;border:1px solid #262C36;border-radius:20px;padding:22px 28px}
.n{flex:none;width:54px;height:54px;border-radius:14px;background:#FF5A45;color:#0E1117;font-weight:800;
  font-size:27px;display:flex;align-items:center;justify-content:center}
.t{font-size:31px;font-weight:800;color:#fff;line-height:1.25}
.d{font-size:24px;line-height:1.4;color:#AEB6BF;margin-top:8px}
.d b{color:#5FE0A5;font-weight:700}
.free{display:inline-block;font-size:19px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:#5FE0A5;background:rgba(63,207,142,.12);border-radius:999px;padding:5px 14px;margin-top:10px}
.rule{margin-top:34px;background:rgba(255,90,69,.08);border:1px solid rgba(255,90,69,.55);border-radius:20px;
  padding:26px 30px;font-size:34px;font-weight:800;color:#fff;line-height:1.3}
.rule span{color:#FF5A45}
.cols .col p{font-size:27px;line-height:1.42;color:#C9D1D9}
.cols .col .ix{font-family:'DejaVu Sans Mono',monospace;font-size:27px;color:#fff;margin:14px 0 16px}
.chain{display:flex;flex-direction:column;gap:12px;margin-top:46px}
.node{background:#161B22;border:1px solid #262C36;border-radius:16px;padding:18px 26px;font-size:30px;color:#fff;font-weight:700}
.node small{display:block;font-size:22px;color:#8B949E;font-weight:400;margin-top:4px}
.arrow{font-size:28px;color:#FF5A45;padding-left:30px;line-height:1}
.opt{display:flex;gap:22px;align-items:center;background:#161B22;border:1px solid #262C36;border-radius:20px;padding:24px 28px}
.opt p{font-size:33px;line-height:1.3;color:#E6EDF3}
.seen{margin-top:40px;background:#161B22;border:1px solid #262C36;border-radius:20px;padding:26px 30px}
.seen .t{font-size:30px}
.bar{height:22px;border-radius:8px;background:#5FE0A5;margin-top:16px}
</style>"""

# ---------------------------------------------------------------- MON
MON = f"""{X}<div class="card">
<div class="kicker">Laravel &middot; Eloquent</div>
<h1>chunk() can skip <em>half your rows.</em></h1>
<div class="block" style="margin-top:40px"><span class="label bad">chunk() + update the filtered column</span>
<pre>User::<span class="f">where</span>(<span class="s">'active'</span>, <span class="k">false</span>)
    -&gt;<span class="f">chunk</span>(<span class="v">100</span>, <span class="k">fn</span> (<span class="v">$users</span>) =&gt;
        <span class="v">$users</span>-&gt;each-&gt;<span class="f">update</span>([<span class="s">'active'</span> =&gt; <span class="k">true</span>])
    );</pre>
<div class="note">Pages with OFFSET. 1,000 inactive users, batches of 100 &rarr; <b>only 500 updated.</b> No error.</div></div>
<div class="block" style="margin-top:30px"><span class="label good">chunkById() &middot; pages by id</span>
<pre>User::<span class="f">where</span>(<span class="s">'active'</span>, <span class="k">false</span>)
    -&gt;<span class="f">chunkById</span>(<span class="v">100</span>, <span class="k">fn</span> (<span class="v">$users</span>) =&gt;
        <span class="v">$users</span>-&gt;each-&gt;<span class="f">update</span>([<span class="s">'active'</span> =&gt; <span class="k">true</span>])
    );</pre>
<div class="note">Uses <b>where id &gt; last id</b>, so updated rows can&rsquo;t shift the pages.</div></div>
<div class="note" style="margin-top:26px">No per-row logic? Skip chunking: one <b style="font-family:'DejaVu Sans Mono',monospace;font-size:24px">update()</b> query does it.</div>
{FOOT.format(tag="Save before your next backfill")}
</div>"""

# ---------------------------------------------------------------- TUE
TUE = f"""{X}<div class="card">
<div class="kicker">SQL &middot; Indexes</div>
<h1>Same columns. <em>Wrong order.</em></h1>
<div class="block" style="margin-top:36px">
<pre><span class="k">SELECT</span> id, total <span class="k">FROM</span> orders
<span class="k">WHERE</span> status = <span class="s">'paid'</span>
  <span class="k">AND</span> created_at &gt;= <span class="s">'2026-10-01'</span>;</pre></div>
<div class="cols" style="margin-top:30px">
<div class="col"><span class="label bad">Index A</span><div class="ix">(created_at, status)</div>
<p>Jumps to Oct 1, then walks <b style="color:#fff">every order since</b>, paid or not.</p></div>
<div class="col"><span class="label good">Index B</span><div class="ix">(status, created_at)</div>
<p>Jumps to &lsquo;paid&rsquo;, then to Oct 1 inside it. Reads <b style="color:#fff">only what you asked for.</b></p></div>
</div>
<div class="rule">Equality columns first. <span>Range column last.</span></div>
<div class="note" style="margin-top:22px">Then run <b>EXPLAIN</b>: check the key it picks and the rows it expects to read.</div>
{FOOT.format(tag="Check your slowest query")}
</div>"""

# ---------------------------------------------------------------- WED carousel
SLIDES = [
    ("Your card number skips the store.",
     "On a well-built checkout, the card form belongs to the payment provider (Stripe, PayPal, Adyen and others). Your card details go straight to them. The store gets a token, like a coat-check ticket.",
     "For developers", "Card data that never touches your server means far fewer PCI rules for you."),
    ("The provider calls your bank through Visa or Mastercard.",
     "The card network is the road. Your bank, the one that gave you the card, is the one who decides.",
     "For developers", "Store &rarr; provider (and its acquiring bank) &rarr; network &rarr; issuing bank."),
    ("Your bank decides in seconds.",
     "Is the card valid? Do the details match? Is there enough money or credit? Does this look like fraud?",
     "For store owners", "When the answer is no, you often get only a generic reason. Many declines are not your website&rsquo;s fault."),
    ("Sometimes your bank asks: &ldquo;Is this really you?&rdquo;",
     "The app prompt or SMS code is called 3-D Secure. It comes from your bank, not the store. In Europe and the UK it is often required.",
     "For developers", "Your checkout must handle this extra step, or those payments fail."),
    ("&ldquo;Approved&rdquo; can mean a hold, not money moved.",
     "Your bank reserves the amount and your available balance drops. Many stores collect it right away. Others, like hotels, hold now and collect later.",
     "For developers", "Authorize now, capture when you ship. Online card holds usually last about 7 days. Capture inside that window."),
    ("The money arrives days later.",
     "After capture, funds move from your bank to the store&rsquo;s payment provider, then to the store&rsquo;s bank account. Usually within a few days, longer for new accounts.",
     "For store owners", "Today&rsquo;s sales are not in your bank account today. Plan cash flow for that."),
    ("Where checkouts go wrong.",
     "A double-click on &ldquo;Pay&rdquo; must not charge twice. A customer may close the tab before the &ldquo;Thank you&rdquo; page.",
     "For developers", "Send the same idempotency key for the same order and disable the button after one click. Confirm orders from the provider&rsquo;s webhook, not the thank-you page."),
]


def carousel() -> str:
    total = len(SLIDES) + 2
    out = [f"""{X}<div class="card"><div class="mid">
<div class="kicker">Explained simply &middot; Payments</div>
<h1 style="font-size:96px">What happens when you <em>click &ldquo;Pay&rdquo;</em></h1>
<div class="sub" style="font-size:32px;margin-top:30px">A few seconds. Several companies. No money moves yet.</div>
<div class="chain">
<div class="node">You click Pay<small>on the store&rsquo;s checkout</small></div><div class="arrow">&darr;</div>
<div class="node">Payment provider<small>Stripe, PayPal, Adyen&hellip;</small></div><div class="arrow">&darr;</div>
<div class="node">Card network<small>Visa, Mastercard&hellip;</small></div><div class="arrow">&darr;</div>
<div class="node">Your bank says yes or no</div></div>
<div style="margin-top:44px" class="swipe">Swipe for all 7 steps &rarr;</div></div>
{FOOT.format(tag=f"1 / {total}")}</div>"""]
    for i, (title, why, who, do) in enumerate(SLIDES, start=1):
        out.append(f"""<div class="card"><div class="mid">
<div class="big" style="font-size:220px">0{i}</div>
<div class="slide-h" style="font-size:76px">{title}</div>
<div class="why" style="font-size:35px">{why}</div>
<div class="do"><div class="t">{who}</div><p>{do}</p></div></div>
{FOOT.format(tag=f"{i + 1} / {total}")}</div>""")
    steps = ["Card details go to the provider. Store gets a token.",
             "Provider &rarr; card network &rarr; your bank.",
             "Your bank says yes or no.",
             "Maybe: &ldquo;Is this really you?&rdquo;",
             "Approved = a hold until it&rsquo;s captured.",
             "Money reaches the store days later."]
    rows = "".join(f'<div class="step"><div class="num">{n}</div><p>{s}</p></div>'
                   for n, s in enumerate(steps, start=1))
    out.append(f"""<div class="card"><div class="mid">
<div class="kicker">Recap</div>
<h1 style="font-size:84px">One click, <em>six steps.</em></h1>
<div class="flow" style="margin-top:40px;gap:14px">{rows}</div>
<div class="sub" style="font-size:30px;margin-top:34px"><b style="color:#fff">Save</b> this for your next checkout project.</div>
</div>
{FOOT.format(tag=f"{total} / {total}")}</div>""")
    return "".join(out)


# ---------------------------------------------------------------- THU
QS = [
    ("Whose name will the domain, hosting and code be in?",
     "Yours. Code in a repository you own. The developer gets access, not ownership."),
    ("How do you back up, and when did you last test a restore?",
     "Automatic backups stored away from the server, and a real date they restored one."),
    ("What happens if I change the plan halfway?",
     "A written scope, and every change priced before work starts."),
    ("What does support after launch include?",
     "A clear list: updates, security fixes, monitoring, reply time when it breaks."),
    ("Can I talk to a past client with a similar project?",
     "A name, a live site, something you can verify."),
]
qrows = "".join(f"""<div class="row"><div class="n">{i}</div><div>
<div class="t">{q}</div><div class="d"><b>Listen for:</b> {a}</div></div></div>"""
                for i, (q, a) in enumerate(QS, start=1))
THU = f"""{X}<div class="card">
<div class="kicker">For business owners</div>
<style>.tight .row{{padding:18px 24px}}.tight .t{{font-size:28px}}.tight .d{{font-size:23px;margin-top:6px}}</style>
<h1 style="font-size:64px">Ask a developer these 5 questions <em>before paying a deposit.</em></h1>
<div class="list tight" style="margin-top:28px;gap:12px">{qrows}</div>
{FOOT.format(tag="No tech knowledge needed")}
</div>"""

# ---------------------------------------------------------------- FRI
TOOLS = [
    ("Healthchecks.io", "Alerts you when a cron job stops pinging.", "Free: 20 jobs"),
    ("Sentry", "Production exceptions with stack trace and context.", "Free: 1 user, 5k errors"),
    ("Uptime Kuma", "Self-hosted uptime checks, 90+ notification services.", "Open source &middot; MIT"),
    ("Mailpit", "Catches every email from local or staging.", "Open source &middot; MIT"),
    ("Crontab.guru", "Reads a cron expression back in plain English.", "Free in the browser"),
]
trows = "".join(f"""<div class="row"><div class="n">{i}</div><div>
<div class="t">{n} <span class="free" style="margin:0 0 0 10px;vertical-align:middle">{f}</span></div><div class="d">{d}</div></div></div>"""
                for i, (n, d, f) in enumerate(TOOLS, start=1))
FRI = f"""{X}<div class="card">
<div class="kicker">Free tools &middot; Developers</div>
<h1 style="font-size:76px">5 free tools for the failures <em>nobody reports.</em></h1>
<div class="list" style="margin-top:34px">{trows}</div>
<div class="rule" style="font-size:30px">Start with 1 and 2. <span>They catch what nobody reports.</span></div>
{FOOT.format(tag="Links in the first comment")}
</div>"""

# ---------------------------------------------------------------- SAT
OPTS = ["A pop-up before you&rsquo;ve read a word",
        "&ldquo;Create an account&rdquo; to buy one item",
        "The page jumps while you try to tap",
        "Chat bubble + cookie banner + newsletter box"]
orows = "".join(f'<div class="opt"><div class="n">{i}</div><p>{o}</p></div>'
                for i, o in enumerate(OPTS, start=1))
SAT = f"""{X}<div class="card">
<div class="kicker">Quick question</div>
<h1 style="font-size:92px">What makes you <em>close a website</em> in 5 seconds?</h1>
<div class="list" style="margin-top:46px;gap:18px">{orows}</div>
<div class="sub" style="margin-top:34px;font-size:34px">Reply with a number, or your own.</div>
{FOOT.format(tag="Everyone has one")}
</div>"""

# ---------------------------------------------------------------- SUN
HIDDEN = [
    ("Find every place it appears", "Product page, cart, emails, mobile menu."),
    ("Check small phones and other languages", "Longer text can break a layout."),
    ("Test the checkout", "That button sits next to the money."),
    ("Go live at a quiet hour", "Then check again."),
]
hrows = "".join(f"""<div class="row"><div class="n">{i}</div><div>
<div class="t">{t}</div><div class="d">{d}</div></div></div>"""
                for i, (t, d) in enumerate(HIDDEN, start=1))
SUN = f"""{X}<div class="card">
<div class="kicker">Tech explained simply</div>
<h1 style="font-size:68px">Why a &ldquo;small change&rdquo; takes longer than <em>the edit itself.</em></h1>
<div class="seen"><span class="label good">What you see</span><div class="t">Change the button text</div></div>
<div class="label neutral" style="margin-top:30px">What also has to happen</div>
<div class="list" style="margin-top:6px;gap:14px">{hrows}</div>
{FOOT.format(tag="The edit is quick. Safety is the job.")}
</div>"""


def main() -> None:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for name, body in [("1-mon-chunk-by-id", MON), ("2-tue-index-column-order", TUE),
                           ("4-thu-questions-before-hiring", THU), ("5-fri-free-monitoring-tools", FRI),
                           ("6-sat-close-the-tab", SAT), ("7-sun-small-change", SUN)]:
            pg.set_content(page(body))
            pg.wait_for_timeout(200)
            over = pg.evaluate("""() => [...document.querySelectorAll('.card')].map(c => {
                const f = c.querySelector('.foot'); const kids = [...c.children].filter(k => k !== f);
                const last = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
                return {gap: f.getBoundingClientRect().top - last, sh: c.scrollHeight};})""")
            print(name, over)
            pg.screenshot(path=str(OUT / f"{name}.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        pg.set_content(page(carousel()))
        pg.wait_for_timeout(200)
        pg.pdf(path=str(OUT / "3-wed-payments-carousel.pdf"), width="1080px", height="1350px",
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
