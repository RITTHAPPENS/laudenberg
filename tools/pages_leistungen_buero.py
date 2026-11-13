"""Erzeugt Leistungs- und Büro-Seite. Wird von build.py importiert und mit dessen Helfern aufgerufen."""
from content_leistungen import SERVICES, FAQ, OFFICE


def leistungen(page, ld):
    svc_blocks = []
    for sid, title, intro, items in SERVICES:
        lis = '\n'.join('            <li>' + li + '</li>' for li in items)
        svc_blocks.append(
            f'      <article class="svc" id="{sid}" aria-labelledby="{sid}-title">\n'
            f'        <div class="svc__head">\n'
            f'          <h2 id="{sid}-title">{title}</h2>\n'
            f'          <p>{intro}</p>\n'
            f'        </div>\n'
            f'        <div class="svc__list">\n'
            f'          <h3>Leistungsspektrum</h3>\n'
            f'          <ul>\n{lis}\n          </ul>\n'
            f'        </div>\n'
            f'      </article>')
    faq_items = '\n'.join(
        f'        <details>\n          <summary>{q}<span class="plus" aria-hidden="true"></span></summary>\n'
        f'          <p>{a}</p>\n        </details>' for q, a in FAQ)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    jump = '\n'.join(f'          <li><a href="#{sid}">{title}</a></li>' for sid, title, _, _ in SERVICES)
    main = f'''
  <section class="lhead" aria-labelledby="page-title">
    <div class="wrap">
      <div class="lhead__copy">
        <h1 id="page-title">Leistungen</h1>
        <ul class="lhead__jump">
{jump}
        </ul>
      </div>
      <figure class="lhead__media reveal-img">
        <img src="assets/img/zusammenarbeit-planbesprechung.webp" width="1200" height="1800" alt="Anncathrin Laudenberg erläutert einem Auftraggeber die ausgelegten Pläne am Besprechungstisch" fetchpriority="high">
      </figure>
    </div>
  </section>
  <section class="svcs" aria-label="Leistungsbereiche">
    <div class="wrap">
{chr(10).join(svc_blocks)}
    </div>
  </section>
  <section class="callout" aria-labelledby="callout-title">
    <div class="wrap">
      <div class="callout__inner">
        <div class="callout__copy">
          <h2 id="callout-title">Lassen Sie uns über Ihr Projekt sprechen.</h2>
          <p>Sie haben Fragen zu meinen Leistungen oder möchten ein konkretes Bauvorhaben besprechen? Rufen Sie mich gerne an oder schreiben Sie mir eine E-Mail. Ich freue mich darauf, von Ihnen zu hören.</p>
        </div>
        <div class="callout__actions">
          <a class="btn btn--solid" href="tel:+4915789195072">Jetzt anrufen</a>
          <a class="btn btn--ghost" href="mailto:info@laudenberg-architektur.de">E-Mail schreiben</a>
        </div>
      </div>
    </div>
  </section>
  <section class="faq" aria-labelledby="faq-title">
    <div class="wrap grid">
      <h2 id="faq-title">Häufige Fragen</h2>
      <div class="faq__list">
{faq_items}
      </div>
    </div>
  </section>
'''
    page('leistungen.html',
         'Leistungen: Projektentwicklung, Objektplanung und Beratung | Anncathrin Laudenberg Architektur',
         'Projektentwicklung und Konzeption, Architektur und Objektplanung (LPH 1 bis 4) sowie Beratung und ergänzende Leistungen. Architektin im Großraum Köln/Bonn, deutschlandweit tätig.',
         main, ld(faq_ld))


def buero(page):
    rows = []
    for i, (sid, label, title, paras, img) in enumerate(OFFICE):
        src, w, h, alt, pos = img
        side = 'left' if i % 2 == 0 else 'right'
        ps = '\n'.join('          <p>' + p + '</p>' for p in paras)
        rows.append(
            f'      <article class="orow orow--{side}" id="{sid}" aria-labelledby="{sid}-title">\n'
            f'        <figure class="orow__img reveal-img"><img src="{src}" width="{w}" height="{h}" loading="{"eager" if i == 0 else "lazy"}" alt="{alt}" style="object-position:{pos}"></figure>\n'
            f'        <div class="orow__copy">\n'
            f'          <p class="orow__label">{label}</p>\n'
            f'          <h2 id="{sid}-title">{title}</h2>\n{ps}\n'
            f'        </div>\n'
            f'      </article>')
    main = f'''
  <section class="page-head page-head--compact" aria-labelledby="page-title">
    <div class="wrap">
      <h1 id="page-title">Büro</h1>
    </div>
  </section>
  <section class="office" aria-label="Über das Büro">
    <div class="wrap">
{chr(10).join(rows)}
    </div>
  </section>
'''
    page('buero.html',
         'Büro | Anncathrin Laudenberg Architektur, Overath',
         'Anncathrin Laudenberg, Architektin: persönliche Betreuung, direkte Kommunikation und eine zentrale Ansprechpartnerin für Wohnungsbau und Projektentwicklung.',
         main)
