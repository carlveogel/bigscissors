#!/usr/bin/env python3
"""Generate the inner pages of the Aussie Casinos site (root + /en-au/ copies).

The homepage (index.html, en-au/index.html) is copied from 10onlinecasinos.com by tools/mirror.py.

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
AUTHOR = "Benjamin Taylor"
AUTHOR_IMG = "Benjamin Taylor.png"

def img(name):
    return quote(name)


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


NAV = [("", "Home"), ("about/", "How we test"), ("author-benjamin-taylor/", "Our reviewer"),
       ("responsible-gambling/", "Responsible gambling"), ("contact/", "Contact")]


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
</head>
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
        href = c.page(target) if target else c.home()
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
            <a href="{c.home()}" class="btn btn--coral btn--sm site-header__cta">Top casinos</a>
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
                    <h2>Casinos</h2>
                    <ul>
                        <li><a href="{c.home()}">Best online casinos</a></li>
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
                        <li><a href="{c.page("responsible-gambling/")}#law">Australian law</a></li>
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
                <p>A casino has to offer working deposit limits, time-outs and self-exclusion to be listed. We also say plainly that none of these sites is licensed in Australia. Our <a href="{c.page("responsible-gambling/")}#law">responsible gambling page</a> explains what that means for you.</p>
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
            <p>We don't run gambling services, take bets or process payments. Anything you do at a third-party site, including registering, depositing or withdrawing, is between you and that operator under their terms. Our responsible gambling page explains the position of these sites under Australian law.</p>

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
