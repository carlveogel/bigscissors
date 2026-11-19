#!/usr/bin/env python3
"""Generate every page of the Aussie Casinos site (root + /en-au/ copies).

Run from the repo root:  python3 tools/build.py
Edit the copy and casino data here, never the generated index.html files.
"""
from urllib.parse import quote
from pathlib import Path
import hashlib

# Changes whenever the CSS/JS change, so browsers and Cloudflare fetch the new files
ASSET_V = hashlib.sha1(Path("css/style.css").read_bytes() + Path("js/script.js").read_bytes()).hexdigest()[:8]

DOMAIN = "https://bigscissors.com.au/"
BRAND = "Aussie Casinos"
EMAIL = "contact@bigscissors.com.au"
UPDATED_LONG = "19 November 2026"
UPDATED_SHORT = "November 2026"
GSC = '    <meta name="google-site-verification" content="RKb416_rnBgrgI837ietY225mlvH1OF2wHtuC_0ONJo">\n'
AUTHOR = "Benjamin Taylor"
AUTHOR_IMG = "Benjamin Taylor.png"

# rank, name, logo, score, offer, wagering (None = not stated), best for, affiliate url
CASINOS = [
    (1, "Lucky 7", "Lucky7 logo.svg", 4.9, "AU$3,000 + 200 free spins", "35x", "All-round pick", "#"),
    (2, "Lucky Vibe", "LuckyVibe Logo.svg", 4.8, "AU$5,000 + 300 free spins", "40x", "Biggest match package", "#"),
    (3, "Goldenbet", "Goldenbet Logo.svg", 4.8, "AU$100 cash on each of your first 3 deposits", "None", "Wager-free cash", "#"),
    (4, "Fortuneplay", "Fortune-Play-Logo.svg", 4.7, "Up to AU$5,000 + 300 free spins", "40x", "Live dealer tables", "#"),
    (5, "Wild Tokyo", "Wild tokyo logo.svg", 4.7, "260% up to AU$4,900 + 620 free spins", "40x", "Free spin volume", "#"),
    (6, "Rolling Slots", "Rollingslots logo.svg", 4.6, "310% up to AU$6,400 + 570 free spins", None, "Pokies fans", "#"),
    (7, "Need for Spin", "Need for spin logo.svg", 4.6, "260% up to AU$4,100 + 530 free spins", None, "High-volatility pokies", "#"),
    (8, "Bets.io", "Betsio logo.svg", 4.5, "225% up to AU$11,500 + 225 free spins", None, "Crypto players", "#"),
    (9, "Aussie Play", "Aussie-Play-Online-Pokies-in-Australia-Logo.jpg", 4.5, "Up to AU$7,500 welcome package", None, "Aussie-themed lobby", "#"),
    (10, "Pubs Casino", "Pubs-Casino-Logo.png", 4.4, "Up to 10% daily cashback", None, "Daily cashback", "#"),
    (11, "Slots Gallery", "Slots-Gallery Logo.webp", 4.4, "Up to AU$9,750 + 225 free spins", None, "Curated pokies", "#"),
    (12, "Winshark", "Winshark-Logo.svg", 4.3, "100% up to AU$400", "45x", "Casual players", "#"),
    (13, "Boho Casino", "Boho-Casino-Logo.svg", 4.3, "100% up to AU$500 + 200 free spins", "40x", "Clean, simple lobby", "#"),
    (14, "BetWhale", "Betwhale-Logo.svg", 4.2, "100% up to AU$1,000", "40x", "Steady all-rounder", "#"),
    (15, "Zizobet", "zizobet logo.svg", 4.1, "100% up to AU$300", "50x", "Low minimum deposits", "#"),
]
CASINO = {c[1]: c for c in CASINOS}


def img(name):
    return quote(name)


def stars(r):
    return (f'<span class="score"><span class="stars" style="--r:{r}" aria-hidden="true"></span>'
            f'<span class="score__num">{r}<small>/5</small></span></span>')


def cta(name, label="Visit site", cls="btn btn--coral btn--sm"):
    url = CASINO[name][7]
    return (f'<a href="{url}" class="{cls}" rel="nofollow sponsored noopener" '
            f'data-casino="{name}">{label} <span class="arrow" aria-hidden="true">&rarr;</span></a>')


# ---------------------------------------------------------------- shell

class Ctx:
    def __init__(self, locale, slug):
        self.locale = locale            # "" or "en-au/"
        self.slug = slug                # "" or "about/"
        depth_asset = (locale + slug).count("/")
        self.a = "../" * depth_asset                       # to repo root (assets)
        self.h = "../" * slug.count("/") or "./"            # to locale home
        self.is_home = slug == ""

    def home(self, anchor=""):
        if self.is_home and anchor:
            return f"#{anchor}"
        return self.h + (f"#{anchor}" if anchor else "")

    def page(self, slug):
        return self.h + slug


NAV = [("rankings", "Rankings"), ("reviews", "Reviews"), ("bonuses", "Bonuses"),
       ("payments", "Payments"), ("about/", "How we test"), ("faq", "FAQ")]


def head(c, title, desc):
    url = DOMAIN + c.slug
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{url}">
    <link rel="alternate" hreflang="en-AU" href="{DOMAIN}en-au/{c.slug}">
    <link rel="alternate" hreflang="x-default" href="{url}">
    <meta property="og:site_name" content="{BRAND}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:locale" content="en_AU">
    <meta name="theme-color" content="#0a1230">
    <link rel="icon" type="image/png" href="{c.a}images/{img("Best Online Casinos Fav Icon.png")}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=Sora:wght@600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{c.a}css/style.css?v={ASSET_V}">
{GSC if c.is_home else ""}</head>
<body>
    <a class="skip-link" href="#main">Skip to content</a>
'''


def brand(c):
    return (f'<a href="{c.home()}" class="brand">'
            f'<img src="{c.a}images/{img("Aussie Casinos Online Logo.png")}" alt="" width="36" height="36">'
            f'<span class="brand__name">Aussie<span>Casinos</span></span></a>')


def header(c, current=""):
    items = []
    for target, label in NAV:
        href = c.page(target) if target.endswith("/") else c.home(target)
        cur = ' aria-current="page"' if target == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f'''
    <header class="site-header">
        <div class="wrap site-header__inner">
            {brand(c)}
            <nav class="site-nav" id="site-nav" aria-label="Main">
                <ul>
                    {"".join(items)}
                </ul>
            </nav>
            <a href="{c.home("rankings")}" class="btn btn--coral btn--sm site-header__cta">Compare all 15</a>
            <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span></button>
        </div>
    </header>
'''


def footer(c):
    return f'''
    <footer class="site-footer">
        <div class="wrap">
            <div class="footer-help">
                <p><strong>Gambling stopped being fun?</strong> Call the National Gambling Helpline on <a href="tel:1800858858">1800 858 858</a>, free and open 24/7.</p>
                <a class="btn btn--ghost btn--sm" href="{c.page("responsible-gambling/")}">Safer gambling tools</a>
            </div>
            <div class="footer-grid">
                <div>
                    {brand(c)}
                    <p>Side-by-side comparisons and plain-English reviews of online casinos that accept Australian players. Read the legal notes before you sign up anywhere.</p>
                    <span class="age-badge" aria-label="Adults only, 18 plus">18+</span>
                </div>
                <div>
                    <h2>Compare</h2>
                    <ul>
                        <li><a href="{c.home("rankings")}">All 15 casinos</a></li>
                        <li><a href="{c.home("reviews")}">Top 5 reviews</a></li>
                        <li><a href="{c.home("bonuses")}">Bonus guide</a></li>
                        <li><a href="{c.home("payments")}">Payment methods</a></li>
                    </ul>
                </div>
                <div>
                    <h2>About</h2>
                    <ul>
                        <li><a href="{c.page("about/")}">How we test</a></li>
                        <li><a href="{c.page("author-benjamin-taylor/")}">Our reviewer</a></li>
                        <li><a href="{c.page("contact/")}">Contact</a></li>
                    </ul>
                </div>
                <div>
                    <h2>Fine print</h2>
                    <ul>
                        <li><a href="{c.page("responsible-gambling/")}">Responsible gambling</a></li>
                        <li><a href="{c.home("legal")}">Australian law</a></li>
                        <li><a href="{c.page("privacy-policy/")}">Privacy policy</a></li>
                        <li><a href="{c.page("terms-of-service/")}">Terms of use</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-base">
                <p>Affiliate disclosure: some links on this site are affiliate links, and we may be paid a commission if you sign up through them. It costs you nothing extra and does not decide where a casino ranks.</p>
                <p>Gambling carries a real risk of losing money. Only bet what you can afford to lose. 18+ only.</p>
                <p>&copy; 2026 {BRAND}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="{c.a}js/script.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


def toc(items, help_box=True):
    lis = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    hb = ('<div class="toc__help"><strong>1800 858 858</strong>National Gambling Helpline, '
          'free and confidential, 24/7.</div>') if help_box else ""
    return f'''<aside class="toc" aria-label="On this page">
                <p class="toc__title">On this page</p>
                <ol>{lis}</ol>
                {hb}
            </aside>'''


def byline(c, label="Reviewed by", date_label="Updated"):
    return f'''<div class="byline">
                <img src="{c.a}images/{img(AUTHOR_IMG)}" alt="{AUTHOR}" width="64" height="64">
                <div>
                    <p class="byline__name">{label} <a href="{c.page("author-benjamin-taylor/")}">{AUTHOR}</a></p>
                    <p>{date_label} {UPDATED_LONG}. Benjamin leads our review desk and signs off every ranking change.</p>
                </div>
            </div>'''


def page_hero(c, crumb, title, lead, extra=""):
    return f'''
    <section class="page-hero">
        <div class="wrap">
            <nav class="crumbs" aria-label="Breadcrumb"><a href="{c.home()}">Home</a> / {crumb}</nav>
            <h1>{title}</h1>
            <p class="page-hero__lead">{lead}</p>
            {extra}
        </div>
    </section>
'''


# ---------------------------------------------------------------- home

def compare_table():
    rows = []
    for rank, name, logo, score, offer, wager, best, _ in CASINOS:
        if wager is None:
            w = '<span class="wager">Wagering: see T&amp;Cs</span>'
        elif wager == "None":
            w = '<span class="wager wager--good">No wagering</span>'
        else:
            good = " wager--good" if wager == "35x" else ""
            w = f'<span class="wager{good}">{wager} wagering</span>'
        top = ' class="is-top"' if rank <= 3 else ""
        rows.append(f'''
                        <tr{top}>
                            <td data-col="rank"><span class="rank">{rank}</span></td>
                            <td data-col="casino"><div class="casino-cell"><span class="logo-box"><img src="{{a}}images/{img(logo)}" alt="{name} logo" loading="lazy"></span><div><strong>{name}</strong><span class="tag">{best}</span></div></div></td>
                            <td data-col="score">{stars(score)}</td>
                            <td data-col="offer"><span class="offer">{offer}</span>{w}</td>
                            <td data-col="cta">{cta(name)}</td>
                        </tr>''')
    return "".join(rows)


REVIEWS = [
    dict(
        name="Lucky 7", title="Lucky 7", sub="Our overall number one",
        banner="Lucky7 Casino.png",
        body=[
            "Lucky 7 is the casino we would point a friend to first. Sign-up and verification were quick, the lobby is easy to find your way around, and the game count is large without feeling like a junk drawer.",
            "Speed is what settled it. Our test cashout by Bitcoin landed in 1 hour 47 minutes, and live chat answered in under half a minute each time we tried it. The welcome offer is generous, but the 35x wagering is what makes it usable: it's the lowest playthrough among the big match bonuses on our list.",
        ],
        facts=[("Welcome offer", "AU$3,000 + 200 free spins"), ("Wagering", "35x"),
               ("Games", "4,000+ (Pragmatic Play, Hacksaw, Evolution)"),
               ("Fastest test payout", "1 hr 47 min (Bitcoin)"),
               ("Banking", "BTC, ETH, LTC, bank transfer, debit card")],
        pros=["Quickest crypto cashout in our testing", "Lowest wagering among the large match bonuses",
              "Casino and sportsbook under one login", "Responsive 24/7 live chat"],
        cons=["Bonus still needs 35x playthrough before you can cash out",
              "Browser only, with no dedicated app"],
    ),
    dict(
        name="Lucky Vibe", title="Lucky Vibe", sub="Biggest welcome package in our top five",
        banner="Lucky Vibe – Low-Limit 1-Hour PayID Crypto Cashout Casino.webp",
        body=[
            "Lucky Vibe's AU$5,000 plus 300 free spins is the headline grabber, so we checked whether the conditions hold up. Wagering is 40x, game weightings are published clearly, and stakes are capped at AU$5 a spin while a bonus is active.",
            "On our test we deposited AU$200, cleared the playthrough on Pragmatic Play pokies and withdrew AU$780. Outside the welcome deal there are weekly reloads and leaderboard tournaments, and the live casino runs on Evolution.",
        ],
        facts=[("Welcome offer", "AU$5,000 + 300 free spins"), ("Wagering", "40x, AU$5 max bet"),
               ("Games", "3,500+ (Pragmatic Play, NetEnt, Play'n GO)"),
               ("Licence", "Curaçao"), ("Extras", "Weekly reloads, tournaments")],
        pros=["Largest total welcome value in our top five", "Bonus rules are written in plain terms",
              "Evolution live tables", "Provably fair hashes on in-house games"],
        cons=["40x wagering is higher than our number one", "AU$5 stake cap while the bonus is running"],
    ),
    dict(
        name="Goldenbet", title="Goldenbet", sub="Best if you hate wagering requirements",
        banner="GoldenBet PayID supported online Casino.jpg",
        body=[
            "Goldenbet skips the usual match bonus. Instead, each of your first three deposits earns an AU$100 cash gift that carries no playthrough at all, so it can be withdrawn like any other balance.",
            "We made three AU$100 deposits, received the gift each time and had a bank withdrawal in our account within 24 hours. It's a smaller headline number than the big packages, but it's money you can actually use. A sportsbook, crash games and a VIP cashback scheme round it out.",
        ],
        facts=[("Welcome offer", "AU$100 cash × first 3 deposits"), ("Wagering", "None"),
               ("Fiat payout (tested)", "Under 24 hours"), ("Extras", "Sportsbook, crash games, VIP cashback")],
        pros=["Bonus cash is withdrawable straight away", "Fast fiat withdrawals",
              "Sportsbook alongside the casino", "Cashback for regular players"],
        cons=["Needs three separate deposits to collect the full AU$300",
              "Smaller total value than the large match deals"],
    ),
    dict(
        name="Fortuneplay", title="Fortuneplay", sub="Best for live dealer games",
        banner="Fortune Play Crypto Bonuses for Australian Players.webp",
        body=[
            "Fortuneplay is the pick for people who mainly play at live tables. The live section runs on Evolution, and in our sessions on Lightning Roulette, Infinite Blackjack and Crazy Time the streams were sharp, with no stutter.",
            "Higher-limit tables are there for bigger bettors, and the VIP scheme pays up to 15% cashback. Our crypto withdrawal arrived inside an hour; bank transfers take one to two business days. The minimum withdrawal is AU$20.",
        ],
        facts=[("Welcome offer", "Up to AU$5,000 + 300 free spins"), ("Wagering", "40x"),
               ("Games", "3,000+ pokies plus Evolution live"),
               ("Crypto payout (tested)", "Under 1 hour"), ("Min. withdrawal", "AU$20")],
        pros=["Strong Evolution live lobby, including high-limit tables", "VIP cashback up to 15%",
              "Both crypto and fiat banking", "Low AU$20 minimum withdrawal"],
        cons=["Bank transfers take 1–2 business days", "40x wagering on the welcome offer"],
    ),
    dict(
        name="Wild Tokyo", title="Wild Tokyo", sub="Most free spins on the list",
        banner="Wild Tokyo Online Casinos for Aussie Players.webp",
        body=[
            "620 free spins is the biggest spin count we found. They are split over your first four deposits, with 150 on the first, and winnings from the spins carry 40x wagering, which is about average.",
            "We played our spins on Cash Connection Golden Book and finished with AU$340 after clearing the playthrough. The wider library is large, with a lot of bonus-buy pokies and networked jackpots, and the mobile site runs without an app.",
        ],
        facts=[("Welcome offer", "260% up to AU$4,900 + 620 free spins"), ("Wagering", "40x on spin winnings"),
               ("Games", "4,500+ (Hacksaw, Pragmatic Play, Push Gaming)"),
               ("Spin schedule", "Over first 4 deposits")],
        pros=["Largest free spin bundle we've seen", "Deep bonus-buy and jackpot selection",
              "Smooth mobile browser play"],
        cons=["Spins are spread over four deposits", "40x wagering on spin winnings"],
    ),
]


def review_html(r, rank):
    name = r["name"]
    score = CASINO[name][3]
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in r["facts"])
    pros = "".join(f"<li>{p}</li>" for p in r["pros"])
    cons = "".join(f"<li>{p}</li>" for p in r["cons"])
    body = "".join(f"<p>{p}</p>" for p in r["body"])
    slug = name.lower().replace(" ", "-").replace(".", "")
    return f'''
                <article class="review" id="review-{slug}">
                    <header class="review__head">
                        <span class="rank">{rank}</span>
                        <div>
                            <h3>{r["title"]}</h3>
                            <p>{r["sub"]}</p>
                        </div>
                        {stars(score)}
                    </header>
                    <div class="review__body">
                        <div class="review__text">
                            <div class="review__banner"><img src="{{a}}images/{img(r["banner"])}" alt="{name} casino lobby" loading="lazy"></div>
                            {body}
                            <div class="proscons">
                                <div class="pros"><h4>What we liked</h4><ul>{pros}</ul></div>
                                <div class="cons"><h4>Watch out for</h4><ul>{cons}</ul></div>
                            </div>
                        </div>
                        <dl class="facts">
                            {facts}
                            {cta(name, "Visit " + name, "btn btn--coral btn--block")}
                            <p class="fine">18+. New customers. T&amp;Cs apply.</p>
                        </dl>
                    </div>
                </article>'''


FAQS = [
    ("Is it legal to play at online casinos from Australia?",
     "The Interactive Gambling Act 2001 makes it illegal for any operator, local or overseas, to offer online casino games such as pokies, roulette and blackjack to people in Australia. Playing is not an offence for you as an individual, but none of these sites hold an Australian licence, ACMA blocks many of them, and you have no Australian regulator to turn to if a withdrawal is refused."),
    ("Which casino on this list is the best overall?",
     "Lucky 7. It paid out fastest in our testing, has one of the biggest game libraries, and its welcome bonus has the lowest wagering among the large match offers."),
    ("Which casino paid out the fastest?",
     "Fortuneplay and Lucky 7 both returned our crypto withdrawals in under two hours. For bank withdrawals, Goldenbet was quickest at under 24 hours."),
    ("Which bonus is the best value?",
     "Goldenbet's AU$100 cash on each of your first three deposits, because it has no wagering attached. If you want the biggest headline number instead, Lucky Vibe's AU$5,000 plus 300 spins is the largest in our top five."),
    ("What does 40x wagering actually mean?",
     "You have to bet 40 times the bonus amount before bonus money and its winnings can be withdrawn. A AU$100 bonus at 40x means AU$4,000 in total bets. Our bonus section works through a full example."),
    ("Do I pay tax on gambling winnings?",
     "For recreational players, generally no. The ATO does not usually treat gambling winnings as income unless gambling is run as a business. If you're unsure about your situation, check with a tax adviser."),
    ("Can I use BetStop to block these casinos?",
     "No. BetStop only covers Australian-licensed online and phone wagering services. To block offshore casinos, use the account limits on each site, ask your bank to block gambling transactions, and install blocking software."),
    ("How do I check whether a gambling site is licensed in Australia?",
     "Search ACMA's register of licensed interactive wagering providers. If a site offering online pokies or table games is accepting Australians, it is not licensed here."),
]


def build_home(c):
    a = c.a
    lead = CASINO["Lucky 7"]
    faqs = "".join(f"<details><summary>{q}</summary><p>{ans}</p></details>" for q, ans in FAQS)
    reviews = "".join(review_html(r, i + 1) for i, r in enumerate(REVIEWS))
    bonus_rows = "".join(
        f"<tr><td>{n}</td><td>{CASINO[n][4]}</td><td>{'None' if CASINO[n][5] == 'None' else CASINO[n][5]}</td><td>{note}</td></tr>"
        for n, note in [("Lucky 7", "Lowest playthrough of the big match bonuses"),
                        ("Lucky Vibe", "AU$5 max bet while wagering"),
                        ("Goldenbet", "Cash, withdrawable straight away"),
                        ("Fortuneplay", "Pairs well with live dealer play"),
                        ("Wild Tokyo", "Spins spread over 4 deposits")])

    html = head(c,
                "Best Online Casinos in Australia (2026): 15 Sites Compared | Aussie Casinos",
                "Compare 15 online casinos that accept Australian players: welcome offers, wagering, payout speed and our scores side by side, plus straight answers on bonuses, banking and Australian law.")
    html += header(c)
    html += f'''
    <main id="main">
    <section class="hero">
        <div class="wrap">
            <div class="hero__grid">
                <div>
                    <span class="eyebrow">Updated {UPDATED_SHORT}</span>
                    <h1>Best Online Casinos in Australia, Compared Side by Side</h1>
                    <p class="hero__lead">Fifteen casinos that accept Australian players, scored on how fast they pay, how fair their bonuses really are and how well they run on a phone. Every number below comes from our own deposits and withdrawals.</p>
                    <div class="hero__actions">
                        <a href="#rankings" class="btn btn--coral">See the comparison table <span class="arrow" aria-hidden="true">&rarr;</span></a>
                        <a href="#legal" class="btn btn--ghost">Read the legal notes</a>
                    </div>
                    <div class="byline-mini">
                        <img src="{a}images/{img(AUTHOR_IMG)}" alt="" width="44" height="44">
                        <span>Reviewed by <a href="{c.page("author-benjamin-taylor/")}">{AUTHOR}</a><br>Last checked {UPDATED_LONG}</span>
                    </div>
                </div>
                <aside class="pick-card" aria-label="Editor's pick">
                    <span class="pick-card__label">Editor's pick</span>
                    <div class="pick-card__top">
                        <span class="logo-box"><img src="{a}images/{img(lead[2])}" alt="Lucky 7 logo"></span>
                        <div>
                            <h2>Lucky 7</h2>
                            {stars(lead[3])}
                        </div>
                    </div>
                    <p class="pick-card__offer">{lead[4]}</p>
                    <ul>
                        <li>Crypto cashout in under 2 hours on our test</li>
                        <li>35x wagering, the lowest of the big bonuses</li>
                        <li>4,000+ games plus a sportsbook</li>
                    </ul>
                    {cta("Lucky 7", "Visit Lucky 7", "btn btn--coral btn--block")}
                    <p class="fine">18+. New customers only. Full T&amp;Cs on the operator's site.</p>
                </aside>
            </div>
            <div class="stat-strip">
                <div class="stat"><span class="stat__num">50+</span><span class="stat__label">casinos assessed</span></div>
                <div class="stat"><span class="stat__num">120+ hrs</span><span class="stat__label">of hands-on play</span></div>
                <div class="stat"><span class="stat__num">15</span><span class="stat__label">made the shortlist</span></div>
                <div class="stat"><span class="stat__num">Quarterly</span><span class="stat__label">re-checks</span></div>
            </div>
        </div>
    </section>

    <div class="wrap layout">
            {toc([("rankings", "Comparison table"), ("method", "How we score"), ("reviews", "Top 5 reviews"),
                  ("games", "Games worth trying"), ("bonuses", "Bonuses explained"), ("payments", "Payments"),
                  ("legal", "Australian law"), ("safer", "Staying in control"), ("verdict", "Verdict"), ("faq", "FAQ")])}
            <div class="content">

            <section class="section" id="rankings">
                <div class="section__head">
                    <span class="eyebrow">The shortlist</span>
                    <h2>All 15 casinos at a glance</h2>
                    <p>Ranked by overall score. Wagering is shown where the operator publishes a single figure; otherwise check the offer's terms before you deposit.</p>
                </div>
                <div class="compare-wrap">
                    <table class="compare">
                        <caption class="sr-only">Comparison of 15 online casinos by score, welcome offer, wagering and strength</caption>
                        <thead>
                            <tr><th scope="col">#</th><th scope="col">Casino</th><th scope="col">Score</th><th scope="col">Welcome offer</th><th scope="col"><span class="sr-only">Link</span></th></tr>
                        </thead>
                        <tbody>{compare_table().replace("{a}", a)}
                        </tbody>
                    </table>
                </div>
                <p class="compare-note">Offers change often and are set by each operator. 18+ only. Always read the full terms on the casino's own site.</p>
            </section>

            <section class="section" id="method">
                <div class="section__head">
                    <span class="eyebrow">Method</span>
                    <h2>How a casino earns its score</h2>
                    <p>We open a real account, fund it with Australian dollars, play, and cash out. Six things decide the final number.</p>
                </div>
                <ol class="criteria">
                    <li><h3>Getting paid</h3><p>We time real withdrawals by every method offered. Crypto under two hours and fiat under a day score top marks; anything past 48 hours loses points.</p></li>
                    <li><h3>Bonus maths</h3><p>We work out what an offer is worth after wagering, stake caps, game weighting and cashout limits, rather than taking the headline figure.</p></li>
                    <li><h3>Licence and security</h3><p>We confirm the offshore licence with the issuing body, check encryption and look for a history of complaints or unpaid winnings.</p></li>
                    <li><h3>Game quality</h3><p>We look at who supplies the games, whether RTPs are published, and whether in-house titles can be verified as provably fair.</p></li>
                    <li><h3>Phone performance</h3><p>Every site is played on iPhone and Android browsers, through the full deposit, play and withdrawal flow.</p></li>
                    <li><h3>Player protection</h3><p>Deposit limits, time-outs and self-exclusion need to be easy to find and actually work. Sites without them don't make the list.</p></li>
                </ol>
            </section>

            <section class="section" id="reviews">
                <div class="section__head">
                    <span class="eyebrow">Hands-on reviews</span>
                    <h2>Our top five, tested in detail</h2>
                    <p>What it was like to deposit, play and withdraw at each casino, and the catches worth knowing before you sign up.</p>
                </div>
                {reviews.replace("{a}", a)}
            </section>

            <section class="section" id="games">
                <div class="section__head">
                    <span class="eyebrow">Game lobby</span>
                    <h2>Games worth trying</h2>
                    <p>Titles you'll find at most casinos on our list, grouped by the type of player they suit.</p>
                </div>
                <div class="grid-3">
                    <div class="card game-card"><span class="card__kicker">Pokies</span><h3>Everyday favourites</h3><p>Popular, well-tested pokies from big studios.</p><ul><li><strong>Big Bass Bonanza</strong>Pragmatic Play, fishing free-spin feature</li><li><strong>Sweet Bonanza</strong>Pragmatic Play, tumbling reels and multipliers</li><li><strong>Gates of Olympus</strong>Pragmatic Play, 6×5 scatter-pays grid</li></ul></div>
                    <div class="card game-card"><span class="card__kicker">Jackpots</span><h3>Networked progressives</h3><p>A slice of every stake feeds a shared prize pool.</p><ul><li><strong>Mega Moolah</strong>Games Global, four-tier jackpot wheel</li><li><strong>Divine Fortune</strong>NetEnt, three progressive tiers</li><li><strong>Jackpot Giant</strong>Playtech, straightforward with a big top prize</li></ul></div>
                    <div class="card game-card"><span class="card__kicker">Live dealer</span><h3>Real tables, streamed</h3><p>Human dealers in a studio, played in real time.</p><ul><li><strong>Lightning Roulette</strong>Evolution, random multipliers on straight-ups</li><li><strong>Crazy Time</strong>Evolution, money-wheel game show</li><li><strong>Infinite Blackjack</strong>Evolution, unlimited seats per table</li></ul></div>
                    <div class="card game-card"><span class="card__kicker">Crash</span><h3>Cash out before it falls</h3><p>Short rounds where the multiplier climbs until it crashes.</p><ul><li><strong>Aviator</strong>Spribe, the best-known crash title</li><li><strong>JetX</strong>SmartSoft, multiplayer crash</li><li><strong>Space XY</strong>BGaming, curve-based multiplier</li></ul></div>
                    <div class="card game-card"><span class="card__kicker">Table games</span><h3>Digital classics</h3><p>Lower house edges if you play them well.</p><ul><li><strong>European Roulette</strong>Single zero, better odds than American</li><li><strong>Blackjack</strong>Look for tables paying 3:2 on naturals</li><li><strong>Casino Hold'em</strong>Poker played against the dealer</li></ul></div>
                    <div class="card game-card"><span class="card__kicker">Bonus buys</span><h3>Straight to the feature</h3><p>Pay up front to trigger the bonus round. High risk.</p><ul><li><strong>Wanted Dead or a Wild</strong>Hacksaw Gaming, western-themed</li><li><strong>Mental</strong>Nolimit City, very high volatility</li><li><strong>San Quentin xWays</strong>Nolimit City, big swings</li></ul></div>
                </div>
            </section>

            <section class="section" id="bonuses">
                <div class="section__head">
                    <span class="eyebrow">Bonus guide</span>
                    <h2>Casino bonuses, explained properly</h2>
                    <p>The headline figure is the least useful part of an offer. Here's what the common types mean and how to tell what one is worth.</p>
                </div>
                <dl class="defs">
                    <div><dt>Deposit match</dt><dd>The casino adds a percentage of your deposit as bonus funds. 100% up to AU$1,000 turns a AU$500 deposit into AU$1,000 to play with.</dd></div>
                    <div><dt>Free spins</dt><dd>Spins on chosen pokies. Winnings usually arrive as bonus money with their own wagering requirement.</dd></div>
                    <div><dt>Cash gift / no-wager bonus</dt><dd>Bonus credit you can withdraw without a playthrough. Rare, and usually smaller, but worth more than it looks.</dd></div>
                    <div><dt>Cashback</dt><dd>A share of your net losses returned over a set period, either as cash or as bonus money.</dd></div>
                    <div><dt>Reloads</dt><dd>Smaller match offers for existing players, often on weekends or tied to a specific day.</dd></div>
                    <div><dt>VIP schemes</dt><dd>Points earned on every bet, traded for cashback, quicker withdrawals or a personal account manager.</dd></div>
                </dl>

                <div class="calc">
                    <h3>Worked example: what wagering really costs</h3>
                    <p>Say you deposit AU$200 and receive a AU$200 match bonus. This is the total you would need to bet before the bonus can be withdrawn:</p>
                    <div class="calc__rows">
                        <div class="calc__row is-good"><span>No wagering (Goldenbet-style)</span><b>AU$0</b></div>
                        <div class="calc__row"><span>35x bonus (Lucky 7)</span><b>AU$7,000</b></div>
                        <div class="calc__row"><span>40x bonus (Lucky Vibe, Wild Tokyo)</span><b>AU$8,000</b></div>
                    </div>
                    <p>If the requirement applies to deposit <em>plus</em> bonus, those totals double. Always check which one the terms use.</p>
                </div>

                <h3>Five things to check before you opt in</h3>
                <ul class="checklist">
                    <li><strong>Playthrough.</strong> Around 35x is reasonable. Above 50x, the bonus is rarely worth taking.</li>
                    <li><strong>Game weighting.</strong> Pokies usually count 100% towards wagering; live and table games often count 5–20%, or nothing at all.</li>
                    <li><strong>Stake cap.</strong> Most offers limit bets to around AU$5–10 while a bonus is active. Going over can void your winnings.</li>
                    <li><strong>Cashout limit.</strong> Some bonuses cap what you can withdraw from bonus winnings.</li>
                    <li><strong>Time limit.</strong> Expect 7 to 30 days to finish wagering before the bonus disappears.</li>
                </ul>

                <h3>Top five offers side by side</h3>
                <div class="table-scroll">
                    <table class="data">
                        <thead><tr><th scope="col">Casino</th><th scope="col">Offer</th><th scope="col">Wagering</th><th scope="col">Our note</th></tr></thead>
                        <tbody>{bonus_rows}</tbody>
                    </table>
                </div>
            </section>

            <section class="section" id="payments">
                <div class="section__head">
                    <span class="eyebrow">Banking</span>
                    <h2>Deposits and withdrawals</h2>
                    <p>How long each method took in our testing, and what to watch for.</p>
                </div>
                <div class="table-scroll">
                    <table class="data">
                        <thead><tr><th scope="col">Method</th><th scope="col">Deposit</th><th scope="col">Withdrawal</th><th scope="col">Good to know</th></tr></thead>
                        <tbody>
                            <tr><td>Crypto (BTC, ETH, LTC, USDT)</td><td>Instant</td><td>Usually 1–2 hours</td><td>Fastest option we tested. Network fees apply, and coin prices move.</td></tr>
                            <tr><td>Visa / Mastercard debit</td><td>Instant</td><td>1–3 business days</td><td>Some Australian banks decline gambling payments, so keep a second method ready.</td></tr>
                            <tr><td>E-wallets (Skrill, Neteller, MuchBetter)</td><td>Instant</td><td>Within 24 hours</td><td>Only offered at some sites. Check fees for moving money back to your bank.</td></tr>
                            <tr><td>PayID / bank transfer</td><td>Minutes to 1 day</td><td>1–5 business days</td><td>Higher minimum withdrawals are common, around AU$50–100.</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="callout callout--teal">
                    <h4>Before your first withdrawal</h4>
                    <p>Almost every casino asks for ID and proof of address before it releases a payout. Upload them early so your first cashout isn't held up. Check the per-transaction limits as well: minimums are often AU$10–20, and maximums can be AU$5,000–10,000.</p>
                </div>
            </section>

            <section class="section" id="legal">
                <div class="section__head">
                    <span class="eyebrow">The law</span>
                    <h2>What Australian law says about online casinos</h2>
                </div>
                <p>The <strong>Interactive Gambling Act 2001</strong> bans operators from offering real-money online casino games, including pokies, roulette, blackjack and similar games, to people in Australia. That applies to companies based overseas too. Only online sports and race wagering can be licensed here.</p>
                <p>The Act targets operators, not players, so using an offshore casino is not a crime for you. It does leave you without the protections that come with a local licence:</p>
                <ul>
                    <li>No Australian regulator or ombudsman can step in if a casino refuses to pay.</li>
                    <li>ACMA regularly blocks offshore casino sites, so a site you use today may become unreachable.</li>
                    <li>BetStop, the national self-exclusion register, does not cover these sites.</li>
                    <li>Gambling winnings are generally not taxed for recreational players.</li>
                </ul>
                <div class="callout callout--coral">
                    <h4>Our position</h4>
                    <p>All the casinos on this page are offshore and hold overseas licences such as Curaçao. None is licensed in Australia, and listing one here does not make it legal or risk-free. You can check whether a provider is licensed on <a href="https://www.acma.gov.au/check-if-gambling-operator-legal" rel="noopener">ACMA's register</a>.</p>
                </div>
            </section>

            <section class="section" id="safer">
                <div class="section__head">
                    <span class="eyebrow">Safer play</span>
                    <h2>Staying in control</h2>
                </div>
                <div class="grid-2">
                    <div class="card"><h3>Budget first</h3><p>Pick a spending limit before you log in and treat it as money already spent on entertainment.</p></div>
                    <div class="card"><h3>Use the limits</h3><p>Set deposit, loss and session limits in your account settings on day one, not after a bad night.</p></div>
                    <div class="card"><h3>Don't chase</h3><p>Upping your bets to win back losses is the quickest way to lose control. Stop when the budget is gone.</p></div>
                    <div class="card"><h3>Block it at the bank</h3><p>Most Australian banks can block gambling transactions on your cards. Ask yours if you need a hard stop.</p></div>
                </div>
                <div class="helplines">
                    <a class="helpline" href="tel:1800858858"><strong>National Gambling Helpline</strong><span class="num">1800 858 858</span>Free, confidential, 24/7</a>
                    <a class="helpline" href="https://www.gamblinghelponline.org.au/" rel="noopener"><strong>Gambling Help Online</strong><span class="num">Chat &amp; email</span>Counselling at any hour</a>
                    <a class="helpline" href="tel:131114"><strong>Lifeline</strong><span class="num">13 11 14</span>24-hour crisis support</a>
                    <a class="helpline" href="https://gaaustralia.org.au/" rel="noopener"><strong>Gamblers Anonymous</strong><span class="num">Meetings</span>Peer support groups</a>
                </div>
                <p style="margin-top:20px"><a href="{c.page("responsible-gambling/")}">More on warning signs, self-exclusion and support &rarr;</a></p>
            </section>

            <section class="section" id="verdict">
                <div class="verdict">
                    <div>
                        <span class="eyebrow">Verdict</span>
                        <h2>Lucky 7 is our pick for 2026</h2>
                        <p>Across more than 50 casinos and 120+ hours of play, Lucky 7 did the most things well:</p>
                        <ul>
                            <li>Quickest crypto payout we recorded</li>
                            <li>4,000+ games from top studios</li>
                            <li>35x wagering, the lowest of the big welcome deals</li>
                            <li>Smooth on both iPhone and Android</li>
                        </ul>
                        <p>Want something different? Goldenbet suits people who dislike wagering, Wild Tokyo suits spin hunters, and Fortuneplay suits live table regulars.</p>
                    </div>
                    <div class="verdict__cta">
                        <span class="logo-box"><img src="{a}images/{img(lead[2])}" alt="Lucky 7 logo"></span>
                        {cta("Lucky 7", "Visit Lucky 7", "btn btn--coral btn--block")}
                        <p class="fine">18+. T&amp;Cs apply. Gamble responsibly.</p>
                    </div>
                </div>
            </section>

            <section class="section" id="faq">
                <div class="section__head">
                    <span class="eyebrow">FAQ</span>
                    <h2>Common questions</h2>
                </div>
                <div class="faq">{faqs}</div>
            </section>

            </div>
    </div>
    </main>
'''
    html += footer(c)
    return html


# ---------------------------------------------------------------- inner pages

def build_about(c):
    html = head(c, "How We Test Online Casinos | Aussie Casinos",
                "How Aussie Casinos reviews online casinos: real-money deposits and withdrawals, six scoring criteria, quarterly re-checks and an editorial process kept separate from affiliate deals.")
    html += header(c, "about/")
    html += '<main id="main">' + page_hero(c, "How we test", "How we test and rank casinos",
                                            "We don't rank sites from their marketing pages. Every casino on our list has been funded, played and cashed out by our own team.")
    html += f'''
    <div class="wrap layout">
            {toc([("process", "The process"), ("criteria", "Scoring criteria"), ("independence", "Independence"),
                  ("updates", "Keeping it current"), ("safety", "Player safety"), ("contact", "Get in touch")])}
            <div class="content prose">
            {byline(c, "Written by", "Updated")}

            <section class="section" id="process">
                <h2>The process</h2>
                <p>Each review follows the same cycle. We open an account as an ordinary player, deposit Australian dollars, claim the welcome offer and play across pokies, live tables, table games and crash games. Then we withdraw, and time how long the money takes to arrive.</p>
                <p>A review typically covers about 30 days and around 2,500 rounds of play. If a casino stalls a payout, hides a bonus condition or falls over on mobile during that window, it doesn't make the list.</p>
                <div class="grid-2" style="margin-top:24px">
                    <div class="card"><span class="card__kicker">Step 1</span><h3>Sign up and verify</h3><p>We note how long KYC takes and whether the terms are clear before any money goes in.</p></div>
                    <div class="card"><span class="card__kicker">Step 2</span><h3>Deposit and claim</h3><p>We check that the bonus lands as advertised and the cashier matches the published terms.</p></div>
                    <div class="card"><span class="card__kicker">Step 3</span><h3>Play</h3><p>Load times, stability and game range on desktop, iPhone and Android.</p></div>
                    <div class="card"><span class="card__kicker">Step 4</span><h3>Withdraw</h3><p>We time the payout from request to arrival and record any fees or extra checks.</p></div>
                </div>
            </section>

            <section class="section" id="criteria">
                <h2>Scoring criteria</h2>
                <ol class="criteria">
                    <li><h3>Payout speed</h3><p>Timed real withdrawals by every method offered. Top marks go to crypto under two hours and fiat under 24.</p></li>
                    <li><h3>Bonus value</h3><p>Value after wagering, game weighting, stake caps, withdrawal caps and expiry. Offers above 50x are flagged.</p></li>
                    <li><h3>Fairness</h3><p>Published RTPs, third-party audits and provably fair verification where available. We also read the terms line by line.</p></li>
                    <li><h3>Mobile</h3><p>Lobby navigation, game loading and the full cashier flow on phone browsers. Bugs that break games drop a site down the list.</p></li>
                    <li><h3>Security</h3><p>Licence checked with the issuer, encryption confirmed, KYC and data handling reviewed, complaint history searched.</p></li>
                    <li><h3>Fit for Australians</h3><p>Accepts Australian sign-ups, supports AUD or clear crypto conversion, and pays out to Australian accounts.</p></li>
                </ol>
            </section>

            <section class="section" id="independence">
                <h2>Independence and how we make money</h2>
                <p>The site earns affiliate commission when readers sign up through some of our links. That's how we pay for testing. Rankings come from the scoring above, and a commercial deal can't buy a better position or a softer review.</p>
                <p>If an operator asks for favourable coverage as a condition of working with us, we turn the deal down. Affiliate links are marked, and our disclosure sits in the footer of every page.</p>
            </section>

            <section class="section" id="updates">
                <h2>Keeping it current</h2>
                <p>Payout speeds and bonus terms change, so we re-check every listed casino at least once a quarter. Rankings move when performance does: a site at number one this quarter can drop if its withdrawals slow down.</p>
                <p>If a casino falls below our standards on a re-check, we take it off the list. The date at the top of each page shows when it was last reviewed.</p>
            </section>

            <section class="section" id="safety">
                <h2>Player safety</h2>
                <p>A casino has to offer working deposit limits, time-outs and self-exclusion to be listed. We also say plainly that none of these sites is licensed in Australia. Our <a href="{c.home("legal")}">legal notes</a> explain what that means for you.</p>
                <div class="callout callout--teal">
                    <h4>Need support?</h4>
                    <p>Call the National Gambling Helpline on <strong>1800 858 858</strong> or visit <a href="https://www.gamblinghelponline.org.au/" rel="noopener">Gambling Help Online</a>. For more options see our <a href="{c.page("responsible-gambling/")}">responsible gambling page</a>.</p>
                </div>
            </section>

            <section class="section" id="contact">
                <h2>Get in touch</h2>
                <p>Questions about our method, a problem with a listed casino, or a site you think we should test? Email <a href="mailto:{EMAIL}">{EMAIL}</a>. We aim to reply within two business days, and we check correction requests within seven.</p>
                <p><a href="{c.page("contact/")}">Full contact details &rarr;</a></p>
            </section>
            </div>
    </div>
    </main>
'''
    html += footer(c)
    return html


def build_author(c):
    html = head(c, "Benjamin Taylor, Lead Reviewer | Aussie Casinos",
                "Benjamin Taylor leads the Aussie Casinos review desk, testing online casinos for payout speed, bonus fairness, game quality and player safety.")
    html += header(c)
    hero = f'''
    <section class="page-hero">
        <div class="wrap">
            <nav class="crumbs" aria-label="Breadcrumb"><a href="{c.home()}">Home</a> / Our reviewer</nav>
            <div class="profile">
                <img src="{c.a}images/{img(AUTHOR_IMG)}" alt="{AUTHOR}" width="160" height="160">
                <div>
                    <span class="eyebrow">Lead reviewer</span>
                    <h1>{AUTHOR}</h1>
                    <p class="page-hero__lead">Benjamin runs our review desk. He decides how casinos are tested, carries out the hands-on reviews and signs off every change to the rankings.</p>
                    <ul class="chips"><li>8+ years reviewing casinos</li><li>50+ sites tested</li><li>Real-money testing</li></ul>
                </div>
            </div>
        </div>
    </section>
'''
    html += '<main id="main">' + hero
    html += f'''
    <div class="wrap layout">
            {toc([("focus", "What he looks at"), ("background", "Background"), ("checklist", "His checklist"), ("standards", "Standards")])}
            <div class="content prose">

            <section class="section" id="focus">
                <h2>What he looks at</h2>
                <div class="grid-2">
                    <div class="card"><h3>Withdrawals</h3><p>Real payout requests by crypto, card, bank and e-wallet, timed from request to arrival.</p></div>
                    <div class="card"><h3>Bonus terms</h3><p>Wagering, game weighting, stake caps, cashout limits, expiry and excluded games.</p></div>
                    <div class="card"><h3>Game libraries</h3><p>Pokies, live tables, crash and jackpots from studios like Pragmatic Play, Evolution, Hacksaw, NetEnt and Push Gaming.</p></div>
                    <div class="card"><h3>Mobile experience</h3><p>Lobby speed, cashier flow, verification steps and game launches on iOS and Android.</p></div>
                    <div class="card"><h3>Licensing and safety</h3><p>Licence details, encryption, KYC process and responsible gambling tools.</p></div>
                    <div class="card"><h3>Fit for Australians</h3><p>Whether a site takes Australian sign-ups, handles AUD sensibly and pays out to local accounts.</p></div>
                </div>
            </section>

            <section class="section" id="background">
                <h2>Background</h2>
                <ol class="timeline">
                    <li><time>2018–2020</time><h3>Product testing</h3><p>Started out auditing sign-up flows, bonus claiming, live chat and cashier reliability across offshore casinos.</p></li>
                    <li><time>2021–2023</time><h3>A stricter method</h3><p>Built a review process around real deposits, wagering checks and verified withdrawals, so scores reflect what players actually experience.</p></li>
                    <li><time>2024–present</time><h3>Aussie Casinos</h3><p>Leads our rankings, comparing casinos that accept Australians on payouts, bonus value, fairness, support and player protection.</p></li>
                </ol>
            </section>

            <section class="section" id="checklist">
                <h2>His checklist</h2>
                <ol class="criteria">
                    <li><h3>Open an account</h3><p>Registers as a normal player and notes verification demands and how clear the terms are.</p></li>
                    <li><h3>Deposit and claim</h3><p>Funds the account, claims the offer and confirms that the cashier matches the published terms.</p></li>
                    <li><h3>Play a full session</h3><p>Pokies, live tables, crash and table games, checking speed, stability and RTP disclosure.</p></li>
                    <li><h3>Cash out</h3><p>Requests a withdrawal and records the timing, fees and any extra checks along the way.</p></li>
                </ol>
            </section>

            <section class="section" id="standards">
                <h2>Standards</h2>
                <p>Benjamin doesn't score a bonus on its size. A huge package with steep wagering or a tight cashout cap can rank below a small, clean one.</p>
                <p>Responsible gambling tools count towards the score: limits, self-exclusion, clear age checks and links to support. Affiliate relationships play no part in his assessments.</p>
            </section>
            </div>
    </div>
    </main>
'''
    html += footer(c)
    return html


def build_contact(c):
    html = head(c, "Contact Us | Aussie Casinos",
                "Get in touch with the Aussie Casinos team about reviews, corrections or partnerships.")
    html += header(c)
    html += '<main id="main">' + page_hero(c, "Contact", "Contact us",
                                            "Questions, corrections and partnership enquiries all come to one inbox.")
    html += f'''
    <div class="wrap narrow prose">
            <div class="email-box">
                <div><span>Email</span><a class="addr" href="mailto:{EMAIL}">{EMAIL}</a></div>
                <a class="btn btn--coral btn--sm" href="mailto:{EMAIL}">Send an email</a>
            </div>
            <p>We aim to reply within two business days. Corrections that need checking can take up to seven.</p>

            <h2>Questions about a review</h2>
            <p>Tell us which page you're asking about and what you'd like to know. A link and a short quote help us answer quickly.</p>

            <h2>Corrections</h2>
            <p>If something on the site looks wrong or out of date, send the page link, the statement concerned and evidence we can check. We verify it independently and update the page if it needs changing.</p>

            <h2>Partnerships</h2>
            <p>Operators and agencies can use the same address. A commercial relationship doesn't guarantee a listing, a good review or a particular position.</p>

            <h2>Please don't send</h2>
            <p>Passwords, full card numbers, ID documents or casino login details. We don't run gambling accounts, handle payments or have access to any operator's systems.</p>

            <h2>Problems with a casino account</h2>
            <p>For deposits, withdrawals, verification or bonuses, contact the casino's own support team first, because we can't access or change your account. To report a gambling service you believe is operating illegally in Australia, use <a href="https://www.acma.gov.au/online-gambling-services" rel="noopener">ACMA's online gambling complaints form</a>.</p>

            <div class="callout callout--coral">
                <h4>Looking for help with gambling?</h4>
                <p>This inbox isn't a support service. Call the National Gambling Helpline on <strong>1800 858 858</strong> any time, or visit <a href="https://www.gamblinghelponline.org.au/" rel="noopener">Gambling Help Online</a>. If anyone is in immediate danger, call <strong>000</strong>.</p>
            </div>
    </div>
    </main>
'''
    html += footer(c)
    return html


def build_privacy(c):
    html = head(c, "Privacy Policy | Aussie Casinos",
                "What information Aussie Casinos collects, how it's used, and the choices you have.")
    html += header(c)
    html += '<main id="main">' + page_hero(c, "Privacy policy", "Privacy policy",
                                            "What we collect when you use this site, why we collect it, and what you can do about it.",
                                            f'<p class="updated">Effective {UPDATED_LONG}</p>')
    html += f'''
    <div class="wrap narrow prose">
            <h2>The short version</h2>
            <p>We collect as little as we can. We have no user accounts and take no payments. Most of what we see is anonymous traffic data used to understand which pages are useful.</p>

            <h2>What we collect</h2>
            <ul>
                <li><strong>Things you send us</strong>, such as your name and email address if you contact us.</li>
                <li><strong>Usage data</strong> collected automatically: browser and device type, referring page, pages viewed and similar statistics.</li>
            </ul>
            <p>We don't knowingly collect sensitive information, so please don't send it to us.</p>

            <h2>How we use it</h2>
            <p>To run and improve the site, answer messages, keep the site secure and understand which content readers find useful.</p>

            <h2>Cookies and analytics</h2>
            <p>We and our analytics providers may use cookies to measure traffic and remember preferences. You can block or delete cookies in your browser settings. The site will still work, though some features may not.</p>

            <h2>Affiliate links and other sites</h2>
            <p>Some links take you to casino operators, and we may earn a commission if you sign up. Once you leave this site, the other site's own privacy policy applies, and we aren't responsible for how it handles your data.</p>

            <h2>How long we keep it</h2>
            <p>Only as long as we need it: to answer you, run the site, meet legal obligations or resolve a dispute. After that it's deleted or anonymised.</p>

            <h2>Security</h2>
            <p>We take reasonable steps to protect what we hold. No internet transmission or storage is completely secure, so we can't promise absolute protection.</p>

            <h2>Your choices</h2>
            <p>You can turn off cookies, choose not to contact us, or ask what information we hold about you. Depending on where you live, you may have further rights under privacy law, including the Australian Privacy Principles.</p>

            <h2>Under-18s</h2>
            <p>This site is for adults only. We don't knowingly collect information from anyone under 18.</p>

            <h2>Changes</h2>
            <p>If this policy changes, we'll post the new version here with a new effective date.</p>

            <div class="callout">
                <p>Privacy questions: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
            </div>
    </div>
    </main>
'''
    html += footer(c)
    return html


def build_terms(c):
    html = head(c, "Terms of Use | Aussie Casinos",
                "The terms that apply when you use the Aussie Casinos website.")
    html += header(c)
    html += '<main id="main">' + page_hero(c, "Terms of use", "Terms of use",
                                            "The rules for using this site, and what you can and can't rely on.",
                                            f'<p class="updated">Effective {UPDATED_LONG}</p>')
    html += f'''
    <div class="wrap narrow prose">
            <h2>Using the site</h2>
            <p>By using this website you agree to these terms. Use it for lawful, personal, informational purposes. Don't try to disrupt it, scrape it or republish our content without permission.</p>

            <h2>Information only</h2>
            <p>Everything here is general information, not legal, financial or tax advice. We work to keep it accurate, but offers, terms, licences and availability change, often without notice. Check the details on the operator's own site before you sign up.</p>

            <h2>We're not a casino</h2>
            <p>We don't run gambling services, take bets or process payments. Anything you do at a third-party site, including registering, depositing or withdrawing, is between you and that operator under their terms. Our legal notes explain the position of these sites under Australian law.</p>

            <h2>Affiliate links</h2>
            <p>Some outbound links earn us a commission. You pay nothing extra, and commissions don't decide our rankings.</p>

            <h2>Age</h2>
            <p>You must be 18 or over to use this site.</p>

            <h2>Changes and severability</h2>
            <p>We may update these terms, and continuing to use the site means you accept the current version. If any part is found unenforceable, the rest still applies.</p>

            <p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
    </main>
'''
    html += footer(c)
    return html


def build_rg(c):
    html = head(c, "Responsible Gambling: Limits, Warning Signs & Support | Aussie Casinos",
                "Practical ways to keep gambling under control, warning signs of harm, how BetStop works and where Australians can get free, confidential help.")
    html += header(c)
    html += '<main id="main">' + page_hero(c, "Responsible gambling", "Responsible gambling",
                                            "How to keep gambling within limits, how to spot when it's slipping, and where to get free, confidential help in Australia.")
    html += f'''
    <div class="wrap layout">
            {toc([("basics", "The basics"), ("law", "Know the law"), ("control", "Staying in control"),
                  ("signs", "Warning signs"), ("betstop", "BetStop"), ("help", "Get help"),
                  ("steps", "Extra steps"), ("others", "Helping someone"), ("report", "Reporting")])}
            <div class="content prose">
            {byline(c, "Written and reviewed by", "Last reviewed")}

            <section class="section" id="basics">
                <h2>The basics</h2>
                <p>Gambling is something you pay for, like a night out. It isn't a way to earn money, clear debts or win back what you've lost. Every bet carries a real chance of losing, and no system changes that.</p>
                <p>This site is for adults 18 and over. If gambling is hurting your finances, relationships, work or health, stop and talk to someone. The services below are free.</p>
            </section>

            <section class="section" id="law">
                <h2>Know the law</h2>
                <p>Australian law treats licensed wagering, such as sports and racing bets, very differently from online casino games. Online pokies, roulette, blackjack and other casino-style games can't legally be offered to people in Australia, even if the website works here.</p>
                <p>Unlicensed operators may offer little protection: withdrawals can be delayed or refused, and some sites disappear with player balances. Check ACMA's <a href="https://www.acma.gov.au/check-if-gambling-operator-legal" rel="noopener">register of licensed providers</a> and its advice on <a href="https://www.acma.gov.au/protect-yourself-illegal-gambling-operators" rel="noopener">avoiding illegal operators</a>.</p>
                <div class="callout callout--teal">
                    <h4>The credit ban</h4>
                    <p>Licensed Australian online wagering providers can't accept credit cards or digital currency, and can't offer you credit. See ACMA's <a href="https://www.acma.gov.au/credit-ban" rel="noopener">credit ban guidance</a>. Whatever the payment method, only use money you can afford to lose.</p>
                </div>
            </section>

            <section class="section" id="control">
                <h2>Staying in control</h2>
                <div class="grid-2">
                    <div class="card"><h3>Set your limits first</h3><p>Decide on a money limit and a time limit before you start, and stop when you hit either one.</p></div>
                    <div class="card"><h3>Protect essentials</h3><p>Never gamble with rent, bills, food, health or savings money, and never borrow to gamble.</p></div>
                    <div class="card"><h3>Keep a record</h3><p>Track deposits, withdrawals and your total losses. The real figure is often a surprise.</p></div>
                    <div class="card"><h3>Mind your state</h3><p>Avoid gambling when you're stressed, upset, lonely or have been drinking.</p></div>
                </div>
                <h3>Also worth doing</h3>
                <ul>
                    <li>Use deposit limits, loss limits, session reminders and time-outs wherever they're offered.</li>
                    <li>Read the wagering, withdrawal and expiry rules before taking any bonus.</li>
                    <li>Turn off promotional emails and notifications that tempt you into unplanned bets.</li>
                    <li>Take regular breaks, and keep up the hobbies and friendships that have nothing to do with gambling.</li>
                    <li>Keep accounts, passwords and payment details to yourself, and never let anyone under 18 use them.</li>
                </ul>
            </section>

            <section class="section" id="signs">
                <h2>Warning signs</h2>
                <p>It may be time to stop and get support if you:</p>
                <ul class="checklist">
                    <li>Spend more time or money than you meant to</li>
                    <li>Keep trying to win back losses</li>
                    <li>Hide gambling or lie about how much you spend</li>
                    <li>Borrow money or fall behind on bills</li>
                    <li>Feel restless or irritable when you can't gamble</li>
                    <li>Gamble to escape stress or low mood</li>
                    <li>Need bigger bets to feel the same buzz</li>
                    <li>Have tried to cut back and couldn't</li>
                    <li>Argue with family or friends about it</li>
                </ul>
                <p>Anyone can be affected. Getting help early stops small problems turning into big ones.</p>
            </section>

            <section class="section" id="betstop">
                <h2>BetStop: the National Self-Exclusion Register</h2>
                <p><a href="https://www.betstop.gov.au/" rel="noopener">BetStop</a> is a free government service that lets you exclude yourself from every Australian-licensed online and phone wagering provider in one step. You can choose a period from three months to a lifetime.</p>
                <p>While you're registered, those providers must stop you betting, can't open new accounts for you and can't send you marketing. They must also close your existing accounts and refund any balance.</p>
                <div class="callout callout--coral">
                    <h4>What BetStop doesn't cover</h4>
                    <p>Offshore online casinos, land-based casinos, pub and club pokies, and some state-run products. For those, use venue self-exclusion, bank gambling blocks and blocking software.</p>
                </div>
                <p><a href="https://www.betstop.gov.au/signup/" rel="noopener">Register with BetStop</a> or call <strong>1800 238 786</strong>. You have to register yourself; no one else can do it on your behalf.</p>
            </section>

            <section class="section" id="help">
                <h2>Get help</h2>
                <div class="helplines">
                    <a class="helpline" href="tel:1800858858"><strong>National Gambling Helpline</strong><span class="num">1800 858 858</span>Free, confidential, 24/7</a>
                    <a class="helpline" href="https://www.gamblinghelponline.org.au/" rel="noopener"><strong>Gambling Help Online</strong><span class="num">Chat, email, tools</span>Counselling any time</a>
                    <a class="helpline" href="tel:131114"><strong>Lifeline</strong><span class="num">13 11 14</span>24-hour crisis support</a>
                    <a class="helpline" href="tel:000"><strong>Emergency</strong><span class="num">000</span>If anyone is in immediate danger</a>
                </div>
            </section>

            <section class="section" id="steps">
                <h2>Extra steps that help</h2>
                <ul>
                    <li>Ask your bank to block gambling transactions.</li>
                    <li>Delete gambling apps and saved card details.</li>
                    <li>Unsubscribe from gambling emails, texts and push alerts.</li>
                    <li>Install website or device blocking software.</li>
                    <li>Let someone you trust help manage money for a while.</li>
                    <li>Talk to a free financial counsellor about debts and bills.</li>
                    <li>Tell family or friends what you're doing so they can back you up.</li>
                    <li>Consider counselling before things reach a crisis.</li>
                </ul>
            </section>

            <section class="section" id="others">
                <h2>Helping someone else</h2>
                <ul>
                    <li>Pick a calm, private moment to talk.</li>
                    <li>Describe what you've noticed without blaming them.</li>
                    <li>Listen, and encourage them to get professional support.</li>
                    <li>Don't lend money for gambling or pay their debts without getting financial advice first.</li>
                    <li>Protect shared accounts and household money.</li>
                    <li>Look after yourself. The helplines above support family and friends too.</li>
                </ul>
            </section>

            <section class="section" id="report">
                <h2>Reporting and complaints</h2>
                <p>Report a possibly illegal online gambling service through <a href="https://www.acma.gov.au/online-gambling-services" rel="noopener">ACMA's online gambling complaints form</a>.</p>
                <p>If a licensed wagering provider lets a BetStop-registered person bet, open an account or receive marketing, complain through the <a href="https://www.betstop.gov.au/contact/" rel="noopener">BetStop contact page</a>.</p>
                <p><strong>Only gamble with money you can afford to lose. If it stops being fun, stop and reach out.</strong></p>
            </section>
            </div>
    </div>
    </main>
'''
    html += footer(c)
    return html


PAGES = {
    "": build_home,
    "about/": build_about,
    "author-benjamin-taylor/": build_author,
    "contact/": build_contact,
    "privacy-policy/": build_privacy,
    "terms-of-service/": build_terms,
    "responsible-gambling/": build_rg,
}

if __name__ == "__main__":
    for locale in ("", "en-au/"):
        for slug, fn in PAGES.items():
            out = Path(locale + slug + "index.html")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(fn(Ctx(locale, slug)), encoding="utf-8")
            print("wrote", out)
