#!/usr/bin/env python3
"""Vygeneruje statické HTML stránky webu BULDO (sdílená hlavička a patička).
Spuštění:  python3 tools/build.py   (z kořene repozitáře)
Výsledné .html soubory jsou hotové pro GitHub Pages, build není při nasazení potřeba."""
from pathlib import Path
import time
VER = time.strftime("%Y%m%d%H%M")  # mění adresu CSS/JS při každém buildu, aby prohlížeč nebral starou verzi z cache

ROOT = Path(__file__).resolve().parent.parent
REGISTER = "https://app.buldo.cz/register"

# ---------- ikony ----------
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="#FFB82F" d="M10 1.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 14.9l-5.2 2.8 1-5.9L1.5 7.7l5.9-.8z"/></svg>'
CHECK = '<img class="check" src="assets/svg/ikony/check.svg" alt="" width="22" height="22">'
CHEVRON = '<svg width="14" height="22" viewBox="0 0 14 22" aria-hidden="true"><path d="M3 3l8 8-8 8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def nico(path):
    return ('<svg class="notif-ico" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#FFB82F"/>'
            f'<g fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</g></svg>')

ICO_DENIK = '<img class="notif-ico" src="assets/svg/ikony/notif-denik.svg" alt="" width="32" height="32">'
ICO_VICE = '<img class="notif-ico" src="assets/svg/ikony/notif-viceprace.svg" alt="" width="32" height="32">'
ICO_FOTO = '<img class="notif-ico" src="assets/svg/ikony/notif-fotky.svg" alt="" width="32" height="32">'
ICO_OK = '<img class="notif-ico" src="assets/svg/ikony/notif-hotovo.svg" alt="" width="32" height="32">'

ICO = {
    "phone": '<svg viewBox="0 0 24 24"><path fill="#1D1D1F" d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><path fill="#1D1D1F" d="M3 5h18a1 1 0 011 1v12a1 1 0 01-1 1H3a1 1 0 01-1-1V6a1 1 0 011-1zm9 7.2L4 7.3V8l8 5 8-5v-.7z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24"><path fill="#1D1D1F" d="M12 2a10 10 0 110 20 10 10 0 010-20zm1 5h-2v6l5 3 1-1.7-4-2.3z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24"><path fill="#1D1D1F" d="M12 2a7 7 0 017 7c0 5-7 13-7 13S5 14 5 9a7 7 0 017-7zm0 4.5a2.5 2.5 0 100 5 2.5 2.5 0 000-5z"/></svg>',
    "user": '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="6" r="4" fill="#1D1D1F"/><path d="M2 18c0-4 3.6-6.5 8-6.5s8 2.5 8 6.5z" fill="#1D1D1F"/></svg>',
    "cal": '<svg viewBox="0 0 20 20" aria-hidden="true"><rect x="2" y="4" width="16" height="14" rx="2" fill="#1D1D1F"/><rect x="5" y="1.5" width="2" height="4" rx="1" fill="#1D1D1F"/><rect x="13" y="1.5" width="2" height="4" rx="1" fill="#1D1D1F"/><rect x="4" y="8" width="12" height="1.5" fill="#fff"/></svg>',
}
SOCIAL = {
    "Facebook": '<svg viewBox="0 0 27 27"><rect width="27" height="27" rx="3" fill="#fff"/><path fill="#1D1D1F" d="M18.6 27V16.6h3.4l.5-4h-3.9v-2.5c0-1.2.3-1.9 2-1.9h2.1V4.6a28 28 0 00-3-.2c-3 0-5.1 1.8-5.1 5.2v3H11v4h3.6V27z"/></svg>',
    "LinkedIn": '<svg viewBox="0 0 27 27"><rect width="27" height="27" rx="3" fill="#fff"/><path fill="#1D1D1F" d="M6 10.5h3.4V21H6zM7.7 5.5a2 2 0 110 4 2 2 0 010-4zM11.6 10.5h3.2v1.4h.1c.5-.9 1.6-1.7 3.3-1.7 3.5 0 4.1 2.3 4.1 5.2V21h-3.4v-5c0-1.2 0-2.7-1.7-2.7s-1.9 1.3-1.9 2.6V21h-3.4z"/></svg>',
    "Instagram": '<svg viewBox="0 0 27 27"><rect width="27" height="27" rx="5" fill="#fff"/><circle cx="13.5" cy="13.5" r="5" fill="none" stroke="#1D1D1F" stroke-width="2.6"/><circle cx="20" cy="7" r="1.5" fill="#1D1D1F"/></svg>',
}

LOGOS = [f"logo-klient{s}.png" for s in ["", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-10", "-11"]]

def marquee():
    imgs = "".join(f'<img src="assets/img/{l}" alt="" loading="lazy">' for l in LOGOS)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{imgs * 4}</div></div>'

# ---------- společné části ----------
NAV = [("Hlavní funkce", "index.html#funkce", "funkce"), ("Ceník", "index.html#cenik", "cenik"),
       ("Články", "clanky.html", "clanky"), ("Poradna", "poradna.html", "poradna"), ("Kontakty", "kontakt.html", "kontakt")]

def header(dark, current):
    logo = "logo-white.svg" if dark else "logo-grey.svg"
    cls = "logo-white" if dark else ""
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if k == current else ""}>{t}</a></li>' for t, h, k in NAV)
    mlinks = "".join(f'<a href="{h}">{t}</a>' for t, h, _ in NAV)
    return f'''<header class="site-header {'header-dark' if dark else 'header-light'}">
  <nav class="nav" aria-label="Hlavní menu">
    <a class="nav-logo" href="index.html" aria-label="BULDO, úvodní stránka"><img class="{cls}" src="assets/svg/{logo}" alt="BULDO" width="110" height="27"></a>
    <ul class="nav-links">{links}</ul>
    <a class="btn btn-yellow" href="{REGISTER}">Vyzkoušet zdarma</a>
    <button class="nav-burger" type="button" aria-label="Otevřít menu" aria-expanded="false" aria-controls="mobile-menu"><span></span></button>
  </nav>
  <div class="mobile-menu" id="mobile-menu">{mlinks}<a class="btn btn-yellow" href="{REGISTER}">Vyzkoušet zdarma</a></div>
</header>'''

FOOTER = f'''<footer class="footer">
  <div class="footer-inner">
    <a class="footer-logo" href="index.html" aria-label="BULDO"><img src="assets/svg/logo-white.svg" alt="BULDO" width="228" height="56"></a>
    <div class="footer-grid">
      <div><h4>DIGITAL BUILD s.r.o.</h4><p>IČO: 06757642</p><p>Purkyňova 792, Velké Přílepy</p></div>
      <div class="nav-cols"><h4>Rychlá navigace</h4>
        <ul><li><a href="index.html">Homepage</a></li><li><a href="index.html#funkce">Hlavní funkce</a></li><li><a href="index.html#cenik">Ceník</a></li><li><a href="clanky.html">Články</a></li><li><a href="poradna.html">Poradna</a></li></ul>
        <ul><li><a href="#">Obchodní podmínky</a></li><li><a href="#">Ochrana osobních údajů</a></li><li><a href="kontakt.html">Kontakty</a></li></ul>
      </div>
      <div><h4>Kontakty</h4><p><a href="tel:+420737280800">+420 737 280 800</a></p><p><a href="mailto:info@buldo.cz">info@buldo.cz</a></p></div>
      <div><h4>Sociální sítě</h4><div class="socials">{"".join(f'<a href="#" aria-label="{n}">{s}</a>' for n, s in SOCIAL.items())}</div></div>
    </div>
  </div>
</footer>'''

TRIAL = f'''<section class="trial reveal" aria-labelledby="trial-title">
  <div>
    <h2 id="trial-title">Vyzkoušejte BULDO<br>na 14 dní zdarma</h2>
    <p>Založení účtu zabere pár minut. Po zkušební době si<br class="br-d"> vyberete tarif, nebo účet jednoduše necháte být.</p>
    <a class="btn btn-dark" href="{REGISTER}">Začít zdarma</a>
  </div>
  <div class="trial-img"><img src="assets/img/app-mockup.png" alt="Aplikace BULDO na notebooku a v mobilu" width="871" height="463" loading="lazy"></div>
</section>'''

FAQ_ITEMS = [
    ("Na jakých zařízeních můžu aplikaci používat?",
     "Na počítači, notebooku, tabletu i chytrém telefonu. BULDO je webová aplikace, takže nic nestahujete ani neinstalujete. Přihlášení je chráněné dvoufázovým ověřením."),
    ("Ceny v ceníku platí pro jednu stavbu za jednoho uživatele?",
     "Ne. U tarifů Basic, Standard a Profi platíte za aktivního uživatele, ne za stavbu. Počet staveb je ve všech tarifech neomezený. Profi+ má jednu cenu za celý účet pro 40 až 100 uživatelů."),
    ("Můžu si stavební deník stáhnout a vytisknout?",
     "Ano. Celý deník nebo jen jeho část vyexportujete do PDF a můžete ho vytisknout. Pod každým podepsaným zápisem je uvedeno, kdo ho podepsal: jméno, funkce a společnost. Postup najdete v Poradně v části Export a tisk stavebního deníku."),
    ("Jakým způsobem můžu archivovat elektronický stavební deník?",
     "Deník můžete vyexportovat do PDF, případně vytisknout a uložit v papírové podobě. Stavbu lze také přepnout do režimu Archivovat: data zůstanou v cloudu a stavbu můžete později znovu aktivovat. Tlačítko Archivovat stavbu je na profilu stavby vlevo dole pod mapou."),
    ("Můžu dát dalším uživatelům přístup jen k části informací?",
     "Ano. Každému uživateli stavby nastavíte konkrétní práva, takže vidí a upravuje jen to, co potřebuje. Postup je v Poradně v části Uživatelé stavby."),
]

def acc(items, cls=""):
    out = []
    for q, a in items:
        out.append(f'<details{cls}><summary>{q}<span class="plus" aria-hidden="true"></span></summary><div class="answer"><p>{a}</p></div></details>')
    return "\n".join(out)

FAQ = f'''<section class="faq" aria-labelledby="faq-title">
  <h2 class="h-section" id="faq-title">Nejčastěji kladené otázky</h2>
  <div class="acc">{acc(FAQ_ITEMS)}</div>
  <div class="faq-more"><p>Nenašli jste, co jste hledali?</p><a class="btn btn-yellow" href="poradna.html">Přejít do poradny</a></div>
</section>'''

ART = [("clanek-1.jpg", "Stavbyvedoucí a geodet na stavbě"), ("clanek-2.jpg", "Dělníci na stavbě v pohybu"), ("clanek-3.jpg", "Stavbyvedoucí s tabletem kontroluje měření")]

def acard(i, hidden=False):
    img, alt = ART[i % 3]
    return f'''<a class="acard{' is-hidden' if hidden else ''}" href="clanek.html">
  <div class="img"><img src="assets/img/{img}" alt="{alt}" width="458" height="275" loading="lazy"></div>
  <time datetime="2026-10-28">28. 10. 2026</time>
  <h3>Stavíte, rekonstruujete nebo teprve vybíráte pozemek?</h3>
  <p>Jak poznat, že je pozemek skutečně vhodný pro stavbu? Vyplatí se dřevostavba? Jaký zdroj vytápění zvolit?</p>
</a>'''

def page(title, desc, body, dark_header=False, current=""):
    return f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/svg/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css?v={VER}">
</head>
<body>
{header(dark_header, current) if not dark_header else ""}
{body}
{FOOTER}
<script src="assets/js/main.js?v={VER}" defer></script>
</body>
</html>
'''

# ---------- HOMEPAGE ----------
FEATURES = [
    ("Stavební deník", "<b>Stavební deník</b> s kvalifikovaným elektronickým podpisem přímo v aplikaci v souladu s legislativou ČR.", "stavebni-denik"),
    ("Vícepráce", "Evidence rozsahu a hodnoty <b>víceprací</b> s možností online potvrzení všech zúčastněných stran přímo v aplikaci.", "viceprace"),
    ("Timeline", "Online komunikace v rámci celé pracovní skupiny s možností fotopříloh tak, jak jste zvyklí na sociálních sítích.", "timeline"),
    ("Zaměstnanci", "Správa <b>zaměstnanců</b>, evidence docházky.", "zamestnanci"),
    ("Dokumenty", "Kompletní <b>dokumentace</b> stavby na jednom místě.", "dokumenty"),
    ("Práva v aplikaci", "Individuální nastavení <b>práv v aplikaci</b> pro jednotlivé interní i externí uživatele.", "prava-v-aplikaci"),
    ("Počasí", "Předpověď či historie <b>počasí</b> s automatickým zápisem do stavebního deníku.", "pocasi"),
    ("Stroje a nářadí", "Správa <b>strojů a nářadí</b>, zápis servisních prohlídek a datumů technických kontrol.", "stroje-a-naradi"),
]

def features():
    tabs, vids = [], []
    for i, (name, desc, slug) in enumerate(FEATURES):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<li><button class="feature-tab" type="button" role="tab" id="tab-{slug}" aria-selected="{sel}" aria-controls="video-{slug}" tabindex="{0 if i == 0 else -1}">'
                    f'<span class="name">{name}</span><span class="desc">{desc}</span></button></li>')
        src = f'src="assets/video/buldo-{slug}-macbook.mp4"' if i == 0 else f'data-src="assets/video/buldo-{slug}-macbook.mp4"'
        vids.append(f'<video id="video-{slug}" role="tabpanel" aria-labelledby="tab-{slug}" class="{"active" if i == 0 else ""}" {src} poster="assets/img/poster-{slug}.jpg" muted loop playsinline preload="{"auto" if i == 0 else "none"}"></video>')
    return f'''<div class="features-box">
      <div class="features-nav">
        <div class="features-arrows">
          <button type="button" class="f-prev" aria-label="Předchozí funkce"><svg width="14" height="14" viewBox="0 0 14 14"><path d="M2 9.5L7 4.5l5 5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <button type="button" class="f-next" aria-label="Další funkce"><svg width="14" height="14" viewBox="0 0 14 14"><path d="M2 4.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        </div>
        <ul class="features-list" role="tablist" aria-label="Hlavní funkce">{"".join(tabs)}</ul>
      </div>
      <div class="features-media">{"".join(vids)}</div>
    </div>'''

PLANS = [
    ("Basic", "Pro řemeslníky a malé firmy, které chtějí deník v telefonu.", (99, 149), "34", "za uživatele / měsíc", ["Online stavební deník", "Počasí", "Nastavení práv uživatelů", "Podpora"]),
    ("Standard", "Pro firmy, které řídí lidi, stroje a harmonogram.", (199, 249), "20", "za uživatele / měsíc", ["Vše z Basic", "Timeline", "Zaměstnanci a stroje", "Pracovní skupiny"]),
    ("Profi", "Pro stavební firmy, které řeší vícepráce a dokumentaci.", (245, 299), "18", "za uživatele / měsíc", ["Vše ze Standard", "Dokumenty", "Vícepráce", "Statistiky"]),
    ("Profi+", "Všechny funkce Profi jako paušál pro 40-100 uživatelů.", (9999, 11999), "17", "celkem / měsíc", ["Vše z Profi", "40-100 uživatelů", "Jedna cena pro celou firmu"]),
]

def kc(n):
    return f"{n:,}".replace(",", " ") + " Kč"

def plans():
    out = []
    for name, for_, (y, m), save, unit, items in PLANS:
        lis = "".join(f"<li>{CHECK}{t}</li>" for t in items)
        out.append(f'''<article class="plan">
  <h3>{name}</h3><p class="for">{for_}</p>
  <div class="price"><strong data-yearly="{kc(y)}" data-monthly="{kc(m)}">{kc(y)}</strong><span class="badge badge-soft save" data-yearly="Ušetříte {save}&nbsp;%">Ušetříte {save}&nbsp;%</span></div>
  <p class="price-unit">{unit}</p>
  <ul>{lis}</ul>
  <a class="btn btn-yellow btn-full" href="{REGISTER}">Vyzkoušet {name} zdarma</a>
</article>''')
    return "\n".join(out)

COMPARE = [
    ("Online stavební deník", "Denní zápisy, podpisy a export.", "1111"),
    ("Počasí", "Automaticky zapsané ke každému dni.", "1111"),
    ("Nastavení práv uživatelů", "Kdo smí co vidět a upravovat.", "1111"),
    ("Timeline", "Harmonogram a postup prací.", "0111"),
    ("Zaměstnanci", "Docházka a kdo je na které stavbě.", "0111"),
    ("Stroje", "Evidence techniky a nářadí.", "0111"),
    ("Pracovní skupiny", "Týmy a party na stavbách.", "0111"),
    ("Dokumenty", "Výkresy, smlouvy a protokoly.", "0011"),
    ("Vícepráce", "Evidence, ocenění a schválení.", "0011"),
    ("Statistiky", "Přehledy napříč stavbami.", "0011"),
    ("Podpora", "Odpověď do 1 pracovního dne.", "1111"),
]

def compare():
    rows = []
    for name, sub, flags in COMPARE:
        tds = "".join(f'<td>{CHECK if f == "1" else "<span class=\"dash\" aria-label=\"Není součástí\"></span>"}</td>' for f in flags)
        rows.append(f"<tr><th scope=\"row\"><b>{name}</b><small>{sub}</small></th>{tds}</tr>")
    y = "".join(f"<td>{kc(p[2][0])}</td>" for p in PLANS)
    m = "".join(f"<td>{kc(p[2][1])}</td>" for p in PLANS)
    return f'''<div class="compare reveal"><table>
  <thead><tr><th><span class="sr-only">Funkce</span></th><th scope="col">Basic</th><th scope="col">Standard</th><th scope="col">Profi</th><th scope="col">Profi+</th></tr></thead>
  <tbody>{"".join(rows)}</tbody>
  <tfoot><tr><th scope="row">Cena při roční platbě</th>{y}</tr><tr><th scope="row">Cena při měsíční platbě</th>{m}</tr></tfoot>
</table></div>'''

# papírky: x, y, šířka v souřadnicích 1440 × 880 (desktop) a v % (mobil)
CHAOS = [
    ("novezpravy.svg", "3 nové zprávy, stavbyvedoucí Klínovec", 310, 150, 305, (2, 10, 56), "0s"),
    ("vicepracelistek.svg", "Lísteček s poznámkami k vícepracím", 905, 30, 313, (58, 3, 40), "-2s"),
    ("stavebnidenikpapir.svg", "Papírový stavební deník s poznámkami", 125, 412, 356, (3, 63, 44), "-4s"),
    ("papirekzvaolatinvestorovi.svg", "Žlutý papírek: zavolat investorovi kvůli oknům", 775, 532, 282, (55, 60, 39), "-1s"),
    ("zmeskanehovoery.svg", "2 zmeškané hovory, stavbyvedoucí Vrchlabí", 960, 605, 311, (34, 83, 58), "-3s"),
]

def chaos_items():
    out = []
    for f, alt, x, y, w, (mx, my, mw), d in CHAOS:
        out.append(f'<div class="chaos-item" style="--x:{x};--y:{y};--w:{w};--mx:{mx};--my:{my};--mw:{mw};--d:{d}"><img src="assets/svg/{f}" alt="{alt}" loading="lazy"></div>')
    return "\n      ".join(out)

home_body = f'''<section class="hero" id="hero" aria-labelledby="hero-title">
  <video class="hero-video" src="assets/video/herovideo.mp4" poster="assets/img/hero-poster.jpg" autoplay muted loop playsinline aria-hidden="true"></video>
  {header(True, "")}
  <div class="hero-content">
    <div class="hero-rating"><span class="stars" aria-hidden="true">{STAR * 5}</span><span>5.0</span><span class="sr-only">hodnocení 5 z 5</span></div>
    <h1 id="hero-title">Celá stavba<br>v jedné aplikaci</h1>
    <p class="hero-lead">Celá stavba v telefonu. Deník, vícepráce, fotky i lidé na jednom místě.</p>
    <div class="hero-cta"><a class="btn btn-yellow" href="{REGISTER}">Vyzkoušet zdarma</a><a class="btn btn-outline-light" href="#funkce">Jak to funguje?</a></div>
  </div>
  <div class="hero-logos"><p>Firmy, které důvěřují aplikaci BULDO:</p>{marquee()}</div>
</section>

<section class="stats" aria-label="BULDO v číslech">
  <div class="stat"><strong data-count="730" data-suffix="+">730+</strong><span>zaregistrovaných firem</span></div>
  <div class="stat"><strong data-count="2500" data-suffix="+">2500+</strong><span>uživatelů každý den</span></div>
  <div class="stat"><strong data-count="5000" data-suffix="+">5000+</strong><span>založených staveb</span></div>
  <div class="stat"><strong data-count="100" data-suffix="%">100%</strong><span>dostupnost aplikace</span></div>
</section>

<section class="scene" id="scene" aria-label="Z chaosu jedna aplikace">
  <div class="scene-sticky">
    <div class="chaos">
      <h2 class="h-section scene-t1">Vypadá Váš stavební deník nějak takto?</h2>
      {chaos_items()}
    </div>
    <div class="control">
      <h2 class="h-section scene-t2">S BULDO máte vše<br>pod kontrolou.</h2>
      <div class="control-fit">
        <div class="control-stage">
          <img class="control-phone" src="assets/img/telefon.png" alt="Aplikace BULDO v mobilu, přehled staveb" width="263" height="535">
          <div class="notif n1" style="--i:0">{ICO_VICE}<div><strong>Vícepráce schválena</strong><span>Terasa · 42 000 Kč · 5 fotek</span></div></div>
          <div class="notif n2" style="--i:1">{ICO_DENIK}<div><strong>Stavební deník aktualizován</strong><span>Klínovec · Materiál dorazil na stavbu</span></div></div>
          <div class="notif n3" style="--i:2">{ICO_FOTO}<div><strong>Nové fotografie ze stavby</strong><span>Bylo přidáno 8 fotografií průběhu prací.</span></div></div>
          <div class="notif n4" style="--i:3">{ICO_OK}<div><strong>Úkol dokončen</strong><span>Montáž oken · Hotovo v termínu</span></div></div>
        </div>
      </div>
      <a class="btn btn-yellow scene-cta" href="{REGISTER}">Vyzkoušet zdarma</a>
    </div>
  </div>
</section>

<div class="dark">
  <section id="funkce" aria-labelledby="funkce-title">
    <h2 class="h-section light" id="funkce-title">Hlavní funkce</h2>
    {features()}
  </section>

  <section class="why" aria-labelledby="why-title">
    <h2 class="h-section light" id="why-title">Proč stavbu vést v BULDO?</h2>
    <div class="bento">
      <div class="bento-col">
        <article class="bcard bc-all reveal"><img src="assets/svg/karta-vse-na-jednom-miste.svg" alt="" loading="lazy"><h3>Vše na jednom místě</h3></article>
        <article class="bcard bc-photo bc-time reveal"><img class="bg" src="assets/img/rect-4146.png" alt="" loading="lazy"><h3>Šetří váš čas a peníze</h3><img class="time-card" src="assets/svg/karta-setri-cas.svg" alt="Papírový deník 8 hodin týdně, s BULDO 1 hodina. O 7 hodin méně papírování každý týden." loading="lazy"></article>
        <article class="bcard bc-lost reveal"><img src="assets/svg/karta-nic-neztrati.svg" alt="" loading="lazy"><h3>Už se vám nic neztratí</h3></article>
      </div>
      <div class="bento-col">
        <article class="bcard bc-24 reveal"><img src="assets/svg/karta-projekty-24h.svg" alt="" loading="lazy"><h3>Vaše projekty pod kontrolou<br>24 hodin denně</h3><p class="online">Online · 5 aktivních staveb</p></article>
        <article class="bcard bc-photo bc-tablet reveal"><img class="bg" src="assets/img/rect-4147.png" alt="" loading="lazy"><h3>Stačí jen telefon, tablet ať jste kdekoliv</h3>
          <div class="save-dialog" aria-hidden="true">
            <p class="t">Uložit zápis do deníku?</p>
            <div class="row site"><i></i><div><b>Stavba Klínovec</b><small>Stavební deník · 14. 10.</small></div></div>
            <div class="row">Betonáž základů dokončena. 14 °C, polojasno, 4 pracovníci. Přiloženo 6 fotek.</div>
            <div class="btns"><span>Zrušit</span><span class="y">Uložit zápis</span></div>
          </div>
        </article>
        <article class="bcard bc-paper reveal"><img src="assets/img/denik-3d.png" alt="" loading="lazy"><h3>Vše v elektronickém formátu bez papírových verzí</h3></article>
        <a class="why-link" href="{REGISTER}">Vyzkoušet na 14 dní zdarma {CHEVRON}</a>
      </div>
    </div>
  </section>
</div>

<section class="pricing" id="cenik" data-period="yearly" aria-labelledby="cenik-title">
  <h2 class="h-section" id="cenik-title">Ceník</h2>
  <div class="switch" role="group" aria-label="Způsob platby">
    <span class="knob" aria-hidden="true"></span>
    <button type="button" data-period="yearly" aria-pressed="true">Ročně <span class="badge">až -34&nbsp;%</span></button>
    <button type="button" data-period="monthly" aria-pressed="false">Měsíčně</button>
  </div>
  <div class="plans">{plans()}</div>
  <p class="price-note">Ceny jsou uvedeny bez DPH.</p>

  <h2 class="h-section compare-title">Který tarif vybrat?</h2>
  {compare()}

  <div class="help-bar reveal">
    <p><b>Nejste si jistí, který tarif zvolit?</b><span>Zavolejte nám, nebo nám napište, poradíme podle velikosti vaší firmy.</span></p>
    <a href="tel:+420737280800">+420 737 280 800</a>
    <a href="mailto:podpora@buldo.cz">podpora@buldo.cz</a>
  </div>
  <p class="compare-note">Ceny jsou uvedeny za uživatele za měsíc, Profi+ celkem za měsíc pro 40-100 uživatelů. Programování na míru 1000 Kč / hod.</p>
</section>

<section class="articles" aria-labelledby="clanky-title">
  <h2 class="h-section" id="clanky-title">Články ze světa BULDO</h2>
  <div class="article-grid">{"".join(acard(i) for i in range(3))}</div>
  <a class="btn btn-yellow" href="clanky.html">Všechny příspěvky</a>
</section>

{TRIAL}
{FAQ}'''

# ---------- ČLÁNKY ----------
clanky_body = f'''<main>
<section class="page-hero">
  <h1>Články o stavebnictví<br>a stavebním deníku</h1>
  <p>Na blogu Buldo najdete praktické informace o vedení stavebního deníku, stavební legislativě, dokumentaci a každodenním řízení stavebních projektů. Sdílíme také zkušenosti firem, které přešly z papírových záznamů na elektronický stavební deník.</p>
</section>
<section class="listing" aria-label="Seznam článků">
  <div class="article-grid">{"".join(acard(i, hidden=i >= 9) for i in range(12))}</div>
  <button class="btn btn-yellow more-btn" type="button" data-more>Načíst více</button>
</section>
{TRIAL}
{FAQ}
</main>'''

# ---------- ČLÁNEK ----------
clanek_body = f'''<main>
<article class="post">
  <h1>Stavíte, rekonstruujete nebo teprve vybíráte pozemek? STAVOTECH Olomouc nabídne odpovědi na jednom místě</h1>
  <div class="post-meta"><span>{ICO["user"]}Autor: Luci</span><span>{ICO["cal"]}<time datetime="2026-10-28">28. 10. 2026</time></span></div>
  <div class="post-body">
    <p>Jak poznat, že je pozemek skutečně vhodný pro stavbu? Vyplatí se dřevostavba? Jaký zdroj vytápění zvolit, kdy má smysl rekuperace a na co si dát pozor při výběru tepelného čerpadla? A kde do celého projektu zapadá technický dozor nebo aktuální dotační podpora?</p>
    <p>Od 5. do 7. listopadu 2026 se na Výstavišti Flora Olomouc uskuteční 68. pokračování stavebního a technického veletrhu STAVOTECH – Moderní dům Olomouc. Letošní program míří právě na otázky, které řeší lidé před stavbou, během realizace i při rekonstrukci domu.</p>
    <p>Podrobné informace o akci najdete také na oficiálním webu STAVOTECH – Moderní dům Olomouc. <a href="#">STAVOTECH – Moderní dům Olomouc 2026</a></p>
    <h2>Od prvního rozhodnutí až po provoz domu</h2>
    <p>Stavba domu není jedno velké rozhodnutí. Je to dlouhá řada menších voleb, které na sebe navazují – a chyba na začátku se může projevit až mnohem později.</p>
    <p>Už při výběru pozemku je potřeba řešit například inženýrské sítě, územní plán, věcná břemena, orientaci ke světovým stranám nebo svažitost terénu. Právě těmto prvním krokům se bude věnovat čtvrteční dvouhodinový pracovní seminář Máme pozemek – a jak dál?</p>
    <p>Pokud už je stavba o několik kroků dál, přichází na řadu způsob výstavby, volba dodavatelů, kontrola provedených prací nebo technické vybavení domu. Pátek proto nabídne mimo jiné přednášku o spolupráci investora s technickým dozorem stavebníka, praktický pohled na novostavbu a rekonstrukci nebo informace o tom, na co se zaměřit při výběru dodavatele dřevostavby.</p>
    <p>A právě výběr lidí, kteří budou váš projekt realizovat, není radno podcenit. Pokud už máte stavbu v přípravě, může se vám hodit také náš podrobný průvodce Jak vybrat stavební firmu a co ověřit před podpisem smlouvy. <a href="#">Jak vybrat stavební firmu a co ověřit před podpisem smlouvy</a></p>
    <p>Veletrh tak může být užitečný nejen pro člověka, který právě staví. Smysl dává i návštěvníkům, kteří jsou teprve ve fázi plánování a chtějí si některá zásadní rozhodnutí promyslet dřív, než podepíší smlouvu nebo začnou investovat.</p>
    <h2>Jak topit, větrat a neutratit zbytečně víc, než je nutné</h2>
    <p>Velkou část letošního programu tvoří energie a technické zařízení budov. Není divu. Právě způsob vytápění, kvalita izolace nebo větrání výrazně ovlivní nejen pořizovací cenu domu, ale také jeho budoucí provoz.</p>
    <p>Během tří dnů se proto bude mluvit například o:</p>
    <ul>
      <li>podlahovém vytápění a lokální rekuperaci,</li>
      <li>vytápění biomasou, krbovými kamny a zemním plynem,</li>
      <li>tepelných čerpadlech a ohřevu teplé vody,</li>
      <li>správném topení a péči o komíny,</li>
      <li>izolacích a tepelných ztrátách domu,</li>
      <li>rekuperaci a jejím využití v novostavbách i starších domech.</li>
      <li>Zajímavým bodem sobotního programu bude například přednáška zaměřená přímo na výběr tepelného čerpadla a riziko špatně zvoleného zařízení. Namísto jednoduchého „tepelné čerpadlo ano, nebo ne“ se tak návštěvníci mohou zaměřit na podstatnější otázku: jak poznat řešení, které skutečně odpovídá konkrétnímu domu a jeho provozu.</li>
    </ul>
    <p>Kompletní časy jednotlivých přednášek doporučujeme zkontrolovat v aktuálním doprovodném programu veletrhu. <a href="#">Doprovodný program STAVOTECH Olomouc 2026</a></p>
  </div>
</article>
<section class="articles" aria-labelledby="also-title">
  <h2 class="h-section" id="also-title">Také si přečtěte</h2>
  <div class="article-grid">{"".join(acard(i) for i in range(3))}</div>
  <a class="btn btn-yellow" href="clanky.html">Všechny příspěvky</a>
</section>
{TRIAL}
{FAQ}
</main>'''

# ---------- KONTAKT ----------
kontakt_body = f'''<main>
<section class="contact">
  <div>
    <h1>Máte zájem o Buldo nebo potřebujete poradit?</h1>
    <p class="contact-lead">Chcete se poradit, zda bude aplikace vyhovovat vašemu týmu? Potřebujete představit její možnosti nebo pomoci s výběrem vhodného tarifu? Zavolejte nám nebo nám pošlete zprávu prostřednictvím formuláře.</p>
    <div class="contact-info">
      <a href="tel:+420737280800"><img class="ci" src="assets/svg/ikony/kontakt-telefon.svg" alt="" width="32" height="32">+420 737 280 800</a>
      <span><img class="ci" src="assets/svg/ikony/kontakt-cas.svg" alt="" width="32" height="32">Po - Pá: 9:00 - 17:00</span>
      <a href="mailto:podpora@buldo.cz"><img class="ci" src="assets/svg/ikony/kontakt-email.svg" alt="" width="32" height="32">podpora@buldo.cz</a>
      <span><img class="ci" src="assets/svg/ikony/kontakt-adresa.svg" alt="" width="32" height="32">Kovárenská 233/2a, Praha 6</span>
    </div>
  </div>
  <form class="form" id="contact-form" novalidate>
    <div class="field"><label class="sr-only" for="f-firma">Firma</label><input id="f-firma" name="firma" placeholder="Firma" autocomplete="organization"></div>
    <div class="field"><label class="sr-only" for="f-jmeno">Jméno a příjmení</label><input id="f-jmeno" name="jmeno" placeholder="Jméno a příjmení" autocomplete="name" required></div>
    <div class="field"><label class="sr-only" for="f-tel">Tel. číslo</label><input id="f-tel" name="telefon" type="tel" placeholder="Tel. číslo" autocomplete="tel"></div>
    <div class="field"><label class="sr-only" for="f-email">Email</label><input id="f-email" name="email" type="email" placeholder="Email" autocomplete="email" required></div>
    <div class="field full"><label class="sr-only" for="f-zprava">Vaše zpráva</label><textarea id="f-zprava" name="zprava" placeholder="Vaše zpráva"></textarea></div>
    <label class="consent"><input type="checkbox" name="souhlas" required>Odesláním formuláře souhlasím se zpracováním svých osobních údajů v souladu s evropským nařízením GDPR.</label>
    <button class="btn btn-yellow" type="submit">Odeslat</button>
    <p class="form-msg" role="status"></p>
  </form>
</section>
<div class="contact-logos logos-on-light"><p>Firmy, které důvěřují aplikaci BULDO:</p>{marquee()}</div>
{TRIAL}
{FAQ}
</main>'''

# ---------- PORADNA ----------
HELP = [
    ("Úvod do používání aplikace BULDO", "uvod", ["Přihlášení do aplikace", "Nastavení účtu / profilu", "Změna hesla", "Změna jazykové mutace v aplikaci", "Vytvoření certifikovaného podpisu", "Pozvání nového člena do aplikace / účtu", "Předplatné aplikace Buldo", "Kontakty na podporu", "Odstranění účtu"]),
    ("Zaměstnanci", "zamestnanci", ["Přidání nového zaměstnance", "Úprava údajů zaměstnance", "Odstranění zaměstnance", "Vyhledávání a řazení zaměstnanců"]),
    ("Stroje a nářadí", "stroje", ["Přidání nového stroje / nářadí", "Úprava položky stroje / nářadí", "Odstranění stroje / nářadí ze seznamu"]),
    ("Pracovní skupiny", "skupiny", ["Vytvoření pracovní skupiny", "Úprava pracovní skupiny", "Odstranění pracovní skupiny"]),
    ("Management", "management", ["Profil účtu", "Členové", "Zabezpečení", "Vlastní logo"]),
    ("Stavby", "stavby", ["Přehled staveb", "Změna pořadí staveb", "Vytvoření nové stavby", "Kopírování údajů stavby"]),
    ("Stavební deník", "denik", 21), ("Pracovní skupiny na stavbě", "skupiny-stavba", 3), ("Osoby na stavbě", "osoby", 3),
    ("Stroje na stavbě", "stroje-stavba", 4), ("Statistiky", "statistiky", 3), ("Dokumenty", "dokumenty", 6),
    ("Vícepráce", "viceprace", 3), ("Uživatelé stavby", "uzivatele", 3), ("Profil stavby", "profil-stavby", 3),
]
HELP_ANSWER = "Text návodu doplníme z aktuální nápovědy BULDO."

def help_page():
    side, main = [], []
    for name, slug, items in HELP:
        n = len(items) if isinstance(items, list) else items
        side.append(f'<a href="#{slug}">{name} <span class="count">{n}</span></a>')
        if isinstance(items, list):
            rows = acc([(t, HELP_ANSWER) for t in items])
        else:
            rows = acc([(f"Návody v kategorii {name} ({n})", "Návody této kategorie doplníme z aktuální nápovědy BULDO.")])
        main.append(f'<section id="{slug}" data-help-section><h2>{name}</h2><div class="acc">{rows}</div></section>')
    return f'''<main>
<section class="page-hero">
  <h1>Podpora BULDO</h1>
  <form class="search" role="search" onsubmit="return false">
    <label class="sr-only" for="help-q">Hledat v poradně</label>
    <input id="help-q" type="search" placeholder="S čím potřebujete pomoci?" autocomplete="off">
    <button class="btn btn-yellow" type="submit">Vyhledat</button>
  </form>
</section>
<div class="help">
  <nav class="help-side" aria-label="Kategorie nápovědy">{"".join(side)}</nav>
  <div class="help-main">{"".join(main)}<p class="help-empty">Nic jsme nenašli. Zkuste jiné slovo, nebo nám <a href="kontakt.html"><u>napište</u></a>.</p></div>
</div>
<div style="height:120px"></div>
</main>'''

PAGES = {
    "index.html": ("BULDO | Elektronický stavební deník a správa staveb online", "Celá stavba v jedné aplikaci. Stavební deník s elektronickým podpisem, vícepráce, fotky i lidé na jednom místě. Vyzkoušejte BULDO 14 dní zdarma.", home_body, True, ""),
    "clanky.html": ("Články o stavebnictví a stavebním deníku | BULDO", "Praktické informace o vedení stavebního deníku, stavební legislativě a řízení stavebních projektů.", clanky_body, False, "clanky"),
    "clanek.html": ("STAVOTECH Olomouc nabídne odpovědi na jednom místě | BULDO", "Stavíte, rekonstruujete nebo teprve vybíráte pozemek? Program veletrhu STAVOTECH – Moderní dům Olomouc 2026.", clanek_body, False, "clanky"),
    "kontakt.html": ("Kontakty | BULDO", "Máte zájem o BULDO nebo potřebujete poradit? Zavolejte nám nebo napište.", kontakt_body, False, "kontakt"),
    "poradna.html": ("Podpora a návody | BULDO", "Návody k aplikaci BULDO: stavební deník, zaměstnanci, stroje, stavby a další.", help_page(), False, "poradna"),
}

for fn, (t, d, b, dark, cur) in PAGES.items():
    (ROOT / fn).write_text(page(t, d, b, dark, cur), encoding="utf-8")
    print("✓", fn)
