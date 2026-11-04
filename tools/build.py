#!/usr/bin/env python3
"""Erzeugt die statischen Prototyp-Seiten aus gemeinsamen Bausteinen.
Aufruf aus dem Repo-Root: python3 tools/build.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = ROOT / 'tools' / 'partials'
part = lambda n: (P / n).read_text(encoding='utf-8')

SITE = 'https://www.laudenberg-architektur.de/'
ARROW = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5" stroke="currentColor" stroke-width="1.3"/></svg>'
IG = ('<svg viewBox="0 0 256 256" fill="currentColor" aria-hidden="true"><path d="M128,82a46,46,0,1,0,46,46A46.06,46.06,0,0,0,128,82Zm0,80a34,34,0,1,1,34-34A34,34,0,0,1,128,162ZM176,26H80A54.06,54.06,0,0,0,26,80v96a54.06,54.06,0,0,0,54,54h96a54.06,54.06,0,0,0,54-54V80A54.06,54.06,0,0,0,176,26Zm42,150a42,42,0,0,1-42,42H80a42,42,0,0,1-42-42V80A42,42,0,0,1,80,38h96a42,42,0,0,1,42,42ZM190,76a10,10,0,1,1-10-10A10,10,0,0,1,190,76Z"/></svg>')
IG_URL = 'https://www.instagram.com/al_architektur/'
MARK = '<svg class="brand__mark" viewBox="0 0 480 480" aria-hidden="true"><rect width="480" height="480"/><path d="M62 350 177 85l113 263h140"/></svg>'
# Wortmarke: beide Zeilen per textLength exakt auf dieselbe Breite gesetzt (wie Originallogo)
WORDMARK = ('<svg class="brand__type" viewBox="0 0 240 45" aria-hidden="true">'
            '<text class="t1" x="0" y="12.2" textLength="240" lengthAdjust="spacing">ANNCATHRIN LAUDENBERG</text>'
            '<text class="t2" x="0" y="44.6" textLength="240" lengthAdjust="spacing">ARCHITEKTUR</text></svg>')

NAV = [('projekte.html', 'Projekte'), ('leistungen.html', 'Leistungen'), ('buero.html', 'Büro'), ('kontakt.html', 'Kontakt')]

LD_ORG = {
    "@context": "https://schema.org", "@type": "ProfessionalService",
    "additionalType": "https://schema.org/Architect",
    "name": "Anncathrin Laudenberg Architektur", "url": SITE,
    "image": SITE + "assets/img/hero-anncathrin-laudenberg-architektin-2400.webp",
    "telephone": "+49 157 89195072", "email": "info@laudenberg-architektur.de",
    "address": {"@type": "PostalAddress", "addressLocality": "Overath", "addressRegion": "NRW", "addressCountry": "DE"},
    "areaServed": ["Overath", "Rheinisch-Bergischer Kreis", "Rhein-Sieg-Kreis", "Köln", "Bonn", "Deutschland"],
    "founder": {"@type": "Person", "name": "Anncathrin Laudenberg", "jobTitle": "Architektin",
                "memberOf": {"@type": "Organization", "name": "Architektenkammer Nordrhein-Westfalen"}},
    "knowsAbout": ["Wohnungsbau", "Mehrfamilienhaus", "Projektentwicklung", "Bebauungskonzept", "Machbarkeitsstudie",
                   "Bauleitplanung", "Genehmigungsplanung", "Wohnraumförderung NRW"],
    "sameAs": [IG_URL],
}


def head(title, desc, path, extra=''):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{'' if path == 'index.html' else path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}assets/img/hero-anncathrin-laudenberg-architektin-2400.webp">
<meta name="theme-color" content="#f3f4f3">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add("js")</script>
<link rel="preload" href="assets/fonts/archivo-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
{extra}</head>
<body>

<a class="visually-hidden" href="#main">Zum Inhalt springen</a>
'''


def header(path):
    links = '\n'.join(
        f'        <li style="--i:{i}"><a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a></li>'
        for i, (h, t) in enumerate(NAV))
    return f'''
<header class="site-header" id="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Anncathrin Laudenberg Architektur, zur Startseite">
      {MARK}
      {WORDMARK}
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menü öffnen"><span class="burger" aria-hidden="true"><span></span><span></span></span></button>
    <nav class="nav" id="site-nav" aria-label="Hauptnavigation">
      <ul class="nav__links">
{links}
      </ul>
      <div class="nav__extra">
        <a href="mailto:info@laudenberg-architektur.de">info@laudenberg-architektur.de</a>
        <a href="tel:+4915789195072">0157 89195072</a>
        <a href="{IG_URL}" rel="noopener" target="_blank">{IG}Instagram</a>
      </div>
      <a class="nav__phone" href="tel:+4915789195072">0157 89195072</a>
      <a class="nav__ig" href="{IG_URL}" rel="noopener" target="_blank" aria-label="Instagram: al_architektur">{IG}</a>
      <a class="btn btn--solid" href="kontakt.html">Projekt anfragen</a>
    </nav>
  </div>
</header>
'''


def footer(path):
    def cur(h):
        return ' aria-current="page"' if h == path else ''
    return f'''
<footer class="site-footer">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Anncathrin Laudenberg Architektur, zur Startseite">
      {MARK}
      {WORDMARK}
    </a>
    <div class="footer__col">
      <h3>Kontakt</h3>
      <a href="mailto:info@laudenberg-architektur.de">E-Mail schreiben</a>
      <a href="tel:+4915789195072">0157 89195072</a>
    </div>
    <div class="footer__col">
      <h3>Seiten</h3>
      <a href="projekte.html"{cur('projekte.html')}>Projekte</a>
      <a href="leistungen.html"{cur('leistungen.html')}>Leistungen</a>
      <a href="buero.html"{cur('buero.html')}>Büro</a>
      <a href="kontakt.html"{cur('kontakt.html')}>Kontakt</a>
    </div>
    <div class="footer__col">
      <h3>Folgen</h3>
      <a href="{IG_URL}" rel="noopener" target="_blank">Instagram</a>
    </div>
    <div class="footer__legal">
      <span>© 2026 Anncathrin Laudenberg Architektur</span>
      <nav aria-label="Rechtliches"><a href="impressum.html"{cur('impressum.html')}>Impressum</a><a href="datenschutz.html"{cur('datenschutz.html')}>Datenschutz</a></nav>
    </div>
  </div>
</footer>

<script src="assets/site.js" defer></script>
</body>
</html>
'''


def page(path, title, desc, main, extra=''):
    html = head(title, desc, path, extra) + header(path) + '\n<main id="main">\n' + main + '\n</main>\n' + footer(path)
    (ROOT / path).write_text(html, encoding='utf-8')
    print('geschrieben:', path)


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>\n'


# ---------------------------------------------------------------- Startseite
ABOUT = f'''
  <section class="about" aria-labelledby="about-title">
    <div class="wrap grid">
      <figure class="about__portrait reveal-img">
        <img src="assets/img/anncathrin-laudenberg-architektin.webp" width="1200" height="1800" loading="lazy" alt="Porträt der Architektin Anncathrin Laudenberg">
      </figure>
      <div class="about__copy">
        <h2 id="about-title">Eine Ansprechpartnerin für Ihr Projekt</h2>
        <p>Ich bin Architektin, Mitglied der Architektenkammer Nordrhein-Westfalen und führe seit 2026 mein eigenes Büro in Overath.</p>
        <p>Nach meinem Master an der FH Aachen habe ich in einem Architekturbüro und einem ganzheitlichen Planungsbüro Projekte vom Entwurf bis zur Umsetzung begleitet. Heute plane ich selbst, kenne jedes Projekt im Detail und bin für meine Bauherren direkt erreichbar. Für größere Vorhaben arbeite ich mit festen freiberuflichen Mitarbeitern zusammen.</p>
        <div class="about__actions">
          <a class="link-arrow" href="buero.html">Mehr über das Büro
            {ARROW}
          </a>
        </div>
      </div>
    </div>
  </section>
'''

HERO = f'''
  <section class="hero" aria-labelledby="hero-title">
    <figure class="hero__media" aria-hidden="true">
      <img src="assets/img/hero-anncathrin-laudenberg-architektin-2400.webp" srcset="assets/img/hero-anncathrin-laudenberg-architektin-1200.webp 1200w, assets/img/hero-anncathrin-laudenberg-architektin-2400.webp 2400w" sizes="(max-width: 900px) 100vw, 64vw" width="2400" height="1600" alt="" fetchpriority="high">
    </figure>
    <div class="wrap grid">
      <div class="hero__copy">
        <h1 id="hero-title"><span class="line" style="--i:0"><span>Architektur beginnt</span></span> <span class="line" style="--i:1"><span>mit dem Potenzial</span></span> <span class="line" style="--i:2"><span>eines Ortes.</span></span></h1>
        <p class="lead soft" style="--d:560">Individuelle Konzepte für Wohnungsbau und Projektentwicklung – wirtschaftlich durchdacht, planungsrechtlich fundiert und architektonisch überzeugend.</p>
        <div class="hero__actions soft" style="--d:700">
          <a class="btn btn--solid" href="kontakt.html">Projekt anfragen
            {ARROW}
          </a>
          <a class="btn btn--ghost" href="projekte.html">Projekte ansehen</a>
        </div>
      </div>
    </div>
  </section>
'''

page('index.html',
     'Anncathrin Laudenberg Architektur | Architektin für Wohnungsbau und Projektentwicklung in Overath',
     'Architektin für Wohnungsbau und Projektentwicklung im Raum Köln, Bonn und Bergisches Land. Individuelle Konzepte, wirtschaftlich durchdacht und planungsrechtlich fundiert.',
     HERO + ABOUT,
     ld(LD_ORG) + '<link rel="preload" as="image" href="assets/img/hero-anncathrin-laudenberg-architektin-2400.webp" imagesrcset="assets/img/hero-anncathrin-laudenberg-architektin-1200.webp 1200w, assets/img/hero-anncathrin-laudenberg-architektin-2400.webp 2400w" imagesizes="(max-width: 900px) 100vw, 64vw">\n')

# ---------------------------------------------------------------- Projekte
LPH = 'Leistungsphasen 1 bis 4'
PROJECTS = [
    dict(id='eilenberg', name='Eilenberg', ort='Neustadt (Wied)', art='Mehrfamilienwohnhaus', umfang='6 Wohneinheiten',
         images=[dict(src='assets/img/projekt-eilenberg-neustadt-wied-skizze.webp', w=1232, h=864,
                      alt='Skizze eines Mehrfamilienwohnhauses mit Flachdach, Holzelementen und umlaufenden Balkonen in Hanglage, Projekt Eilenberg in Neustadt (Wied)',
                      note='Eigene Skizze, KI-nachbearbeitet')]),
    dict(id='goethestrasse', name='Goethestraße', ort='Siegburg', art='Mehrfamilienwohnhaus', umfang='4 Wohneinheiten',
         images=[dict(src='assets/img/projekt-goethestrasse-siegburg-visualisierung.webp', w=1201, h=908,
                      alt='Visualisierung eines weißen Mehrfamilienwohnhauses mit Staffelgeschoss an der Goethestraße in Siegburg',
                      note='KI-Visualisierung')]),
    dict(id='glockengiesserstrasse', name='Glockengießerstraße', ort='Overath', art='Mehrfamilienwohnhaus', umfang='10 Wohneinheiten',
         images=[dict(src='assets/img/projekt-glockengiesserstrasse-overath-skizze.webp', w=1262, h=848,
                      alt='Skizze eines Mehrfamilienwohnhauses mit Balkonen und Außentreppe an der Glockengießerstraße in Overath',
                      note='Visualisierung KI-unterstützt')]),
    dict(id='menden', name='Menden', ort='Sankt Augustin', art='Wohnbebauung Plangebiet',
         umfang='<abbr title="Einfamilienhäuser">25 EFH</abbr> und <abbr title="Mehrfamilienhaus">1 MFH</abbr> mit 4 Wohneinheiten',
         images=[dict(src='assets/img/projekt-menden-sankt-augustin-visualisierung.webp', w=1800, h=1012,
                      alt='Visualisierung des Plangebiets Menden in Sankt Augustin mit Einfamilienhäusern, Gärten und zentralem Spielplatz aus der Vogelperspektive',
                      note='KI-Visualisierung')]),
    dict(id='scherbusch', name='Scherbusch', ort='Hennef', art='Städtebauliche Konzeptplanung',
         umfang='<abbr title="Einfamilienhäuser">13 EFH</abbr>, <abbr title="Doppelhaushälften">10 DHH</abbr> und <abbr title="Mehrfamilienhäuser">4 MFH</abbr>',
         images=[dict(src='assets/img/projekt-scherbusch-hennef-visualisierung.webp', w=1800, h=1012,
                      alt='Visualisierung einer Wohnstraße mit weißen kubischen Häusern, städtebauliche Konzeptplanung Scherbusch in Hennef',
                      note='KI-Visualisierung')]),
]
tiles = '\n'.join(f'''        <li>
          <button class="tile" type="button" style="--i:{i % 3}" data-project="{i}" aria-haspopup="dialog">
            <span class="tile__media"><img src="{p['images'][0]['src']}" width="{p['images'][0]['w']}" height="{p['images'][0]['h']}" loading="{'eager' if i < 3 else 'lazy'}" alt="{p['images'][0]['alt']}"></span>
            <span class="tile__title"><span>{p['name']}</span></span>
            <span class="tile__meta">{p['art']}</span>
          </button>
        </li>''' for i, p in enumerate(PROJECTS))
pdata = [dict(id=p['id'], name=p['name'], images=p['images'],
              data=[['Ort', p['ort']], ['Projektart', p['art']], ['Umfang', p['umfang']], ['Leistungen', LPH]])
         for p in PROJECTS]
PROJ_MAIN = f'''
  <section class="page-head" aria-labelledby="page-title">
    <div class="wrap">
      <h1 id="page-title">Projekte</h1>
    </div>
  </section>
  <section class="page-body" aria-label="Projektübersicht">
    <div class="wrap">
      <ul class="project-grid">
{tiles}
      </ul>
    </div>
  </section>

  <dialog class="pd" id="pd" aria-labelledby="pd-title">
    <div class="pd__bar">
      <div class="wrap">
        <span class="pd__count" aria-live="polite"></span>
        <div class="pd__nav">
          <button class="icon-btn pd__prev" type="button" aria-label="Vorheriges Projekt"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M15 8H2M7 3 2 8l5 5" stroke="currentColor" stroke-width="1.3"/></svg></button>
          <button class="icon-btn pd__next" type="button" aria-label="Nächstes Projekt">{ARROW}</button>
          <button class="icon-btn pd__close" type="button" aria-label="Schließen" autofocus><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 2l12 12M14 2 2 14" stroke="currentColor" stroke-width="1.3"/></svg></button>
        </div>
      </div>
    </div>
    <div class="pd__body">
      <div class="wrap grid">
        <figure class="pd__media">
          <img src="" alt="">
          <figcaption></figcaption>
          <div class="pd__thumbs"></div>
        </figure>
        <div class="pd__info">
          <h2 id="pd-title"></h2>
          <dl class="pd__data"></dl>
          <div class="pd__cta">
            <a class="link-arrow" href="kontakt.html">Projekt anfragen
              {ARROW}
            </a>
          </div>
        </div>
      </div>
    </div>
  </dialog>
  <script type="application/json" id="projects-data">{json.dumps(pdata, ensure_ascii=False)}</script>
'''
page('projekte.html',
     'Projekte | Anncathrin Laudenberg Architektur',
     'Ausgewählte Projekte von Anncathrin Laudenberg Architektur: Mehrfamilienwohnhäuser, Wohnbebauung und städtebauliche Konzepte in Overath, Siegburg, Sankt Augustin, Hennef und Neustadt (Wied).',
     PROJ_MAIN)

# ---------------------------------------------------------------- Leistungen
services = part('services.html')
intro = re.search(r'<p class="services__intro">(.*?)</p>', services, re.S).group(1)
services = re.sub(r'\s*<h2 id="services-title">Leistungen</h2>\s*<p class="services__intro">.*?</p>', '', services, flags=re.S)
services = services.replace('<section class="services" id="leistungen" aria-labelledby="services-title">', '<section class="services" aria-label="Leistungsübersicht">')
faq = part('faq.html')
faq_ld = part('faq_ld.html')
LEIST_MAIN = f'''
  <section class="page-head" aria-labelledby="page-title">
    <div class="wrap">
      <h1 id="page-title">Leistungen</h1>
      <p>{intro}</p>
    </div>
  </section>
{services}
{faq}
'''
page('leistungen.html',
     'Leistungen: Objektplanung und Projektentwicklung | Anncathrin Laudenberg Architektur',
     'Objektplanung (LPH 1 bis 4), Projektentwicklung, Machbarkeitsstudien, städtebauliche Konzepte und Begleitung von Bauleitplanverfahren im Raum Köln, Bonn und Bergisches Land.',
     LEIST_MAIN, faq_ld)

# ---------------------------------------------------------------- Büro
TB = [('Name', 'Gyors'), ('Funktion', 'Bürohund'), ('Zuständigkeit', 'Gute Laune und die Einhaltung der täglichen Frischluftquote', 'wide'),
      ('Maßstab', '1:1'), ('Geprüft', 'A. Laudenberg')]
tb = '\n'.join(f'          <div{" class=\"wide\"" if len(t) > 2 else ""} style="--i:{i}"><dt>{t[0]}</dt><dd>{t[1]}</dd></div>' for i, t in enumerate(TB))
BUERO_MAIN = f'''
  <section class="page-head" aria-labelledby="page-title">
    <div class="wrap">
      <h1 id="page-title">Eine Ansprechpartnerin für Ihr Projekt</h1>
    </div>
  </section>
  <section class="office" aria-label="Über mich">
    <div class="wrap grid">
      <div class="office__intro">
        <p>Ich bin Architektin, Mitglied der Architektenkammer Nordrhein-Westfalen und führe seit 2026 mein eigenes Büro in Overath.</p>
        <p>Nach meinem Master an der FH Aachen habe ich in einem Architekturbüro und einem ganzheitlichen Planungsbüro Projekte vom Entwurf bis zur Umsetzung begleitet. Heute plane ich selbst, kenne jedes Projekt im Detail und bin für meine Bauherren direkt erreichbar.</p>
        <p>Für größere Vorhaben arbeite ich mit festen freiberuflichen Mitarbeitern zusammen. So bleibt die Verantwortung bei einer Person, und die Kapazität wächst mit dem Projekt.</p>
      </div>
      <figure class="office__img office__img--a reveal-img">
        <img src="assets/img/anncathrin-laudenberg-portrait.webp" width="1200" height="1800" loading="lazy" alt="Anncathrin Laudenberg im Büro">
      </figure>
      <figure class="office__img office__img--b reveal-img">
        <img src="assets/img/projektbesprechung-buero.webp" width="1800" height="1200" loading="lazy" alt="Anncathrin Laudenberg erläutert einen Entwurf am Bildschirm in einer Projektbesprechung">
      </figure>
      <div class="office__work">
        <h2>Persönlich und vor Ort</h2>
        <p>Abstimmungen finden direkt bei meinen Bauherren, auf dem Grundstück oder bei den Behörden statt. Kurze Wege, klare Entscheidungen.</p>
      </div>
    </div>
  </section>
  <section class="dog" aria-labelledby="dog-title">
    <div class="wrap grid">
      <figure class="dog__photo reveal-img">
        <img src="assets/img/gyors.webp" width="900" height="1200" loading="lazy" alt="Gyors, der Bürohund, sitzt in einer Blumenwiese">
      </figure>
      <div class="dog__copy">
        <h2 id="dog-title">Und dann ist da noch Gyors.</h2>
        <p>Er begleitet mich durch den Arbeitsalltag und sorgt dafür, dass zwischen zwei Plänen auch mal eine Runde an der frischen Luft drin ist.</p>
        <dl class="titleblock">
{tb}
        </dl>
      </div>
    </div>
  </section>
'''
page('buero.html',
     'Büro | Anncathrin Laudenberg Architektur, Overath',
     'Anncathrin Laudenberg, Architektin aus Overath: persönliche Zusammenarbeit, kurze Wege und eine feste Ansprechpartnerin für Wohnungsbau und Projektentwicklung.',
     BUERO_MAIN)

# ---------------------------------------------------------------- Kontakt
contact = part('contact.html')
contact = contact.replace('<section class="contact" id="kontakt" aria-labelledby="contact-title">', '<section class="contact contact--page" aria-labelledby="contact-title">')
contact = contact.replace('<h2 id="contact-title">Sie planen ein Wohnbauprojekt?</h2>', '<h1 id="contact-title">Sie planen ein Projekt?</h1>')
page('kontakt.html',
     'Kontakt | Anncathrin Laudenberg Architektur',
     'Projekt anfragen bei Anncathrin Laudenberg Architektur: per Formular, E-Mail an info@laudenberg-architektur.de oder telefonisch unter 0157 89195072.',
     contact)

# ---------------------------------------------------------------- Impressum, Datenschutz
rows = part('legal_rows.html')
page('impressum.html',
     'Impressum | Anncathrin Laudenberg Architektur',
     'Impressum von Anncathrin Laudenberg Architektur, Overath. Angaben nach § 5 DDG und berufsrechtliche Angaben.',
     f'''
  <section class="legal" aria-labelledby="legal-title">
    <div class="wrap grid">
      <h1 id="legal-title">Impressum</h1>
{rows}
    </div>
  </section>
''')
page('datenschutz.html',
     'Datenschutz | Anncathrin Laudenberg Architektur',
     'Datenschutzerklärung von Anncathrin Laudenberg Architektur.',
     '''
  <section class="legal" aria-labelledby="legal-title">
    <div class="wrap grid">
      <h1 id="legal-title">Datenschutz</h1>
      <dl class="legal__list">
        <div class="legal__row"><dt>Hinweis</dt><dd><p>Die Datenschutzerklärung wird mit dem finalen Hosting und Kontaktformular erstellt und vor dem Livegang eingefügt.</p></dd></div>
      </dl>
    </div>
  </section>
''')
