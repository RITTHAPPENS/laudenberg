# Design

Visual system of the Anncathrin Laudenberg Architektur website, documented from the built homepage (index.html). World: Bebauungsplan-Notation, consistently black and white.

## Tokens

| Token | Value | Use |
|---|---|---|
| --paper | #f3f4f3 | Page ground (cool, not cream) |
| --paper-raised | #fafbfa | Alternating section ground, table and legend cells |
| --ink | #141515 | Text, lines, buttons, contact block ground |
| --ink-soft | #2b2d2d | Body copy on paper |
| --muted | #5a5e5e | Meta text, labels (≥4.5:1 on paper) |
| --line | rgba(20,21,21,.14) | Hairline dividers |
| Accent | none | Colour comes only from project images on hover |

## Typography

- Archivo (variable, self-hosted, OFL): headings at font-stretch 112%, weight 500, tracking -0.025em to -0.035em; body 17px / 1.6, stretch 100%.
- Geist Mono (OFL): only for measurements and plan labels (Nutzungsschablone keys, Maßkette numbers, form labels, captions).
- Wordmark: caps, "ANNCATHRIN LAUDENBERG" weight 500 tracking .08em over "ARCHITEKTUR" weight 300.

## Type scale

One scale, used everywhere via tokens: --fs-label .75rem (mono labels), --fs-caption .8125rem, --fs-small .9375rem (nav, meta, step text), --fs-body 1.0625rem (all running text, 1rem mobile), --fs-lead (hero only), --fs-h3 1.25rem, --fs-h3-lg (service categories), --fs-h2, --fs-h2-xl (statement, contact), --fs-display (hero H1). No ad-hoc sizes outside the logo lockup.

## Logo

Black square monogram (AL line, white stroke) as header mark, footer mark and favicon (favicon.svg). Path: M62 350 177 85l113 263h140 in a 480 box.

## Components

- Nutzungsschablone: 2-column definition grid, 1px ink borders, mono key over Archivo value.
- Baugrenze: dash-dot stroke (14 5 2 5), 1.25px, used for the hero Baufenster and as the hover outline on project tiles (marching).
- Project tile: 3:2 image, grayscale by default, colour on hover/focus (touch: colour when 75% in view), meta line in muted, title with underline grow.
- Planzeichen legend: 88px symbol box (text code, dashed line, dots, hatch, slope) plus heading and text.
- Maßkette: horizontal dimension line with ticks for process steps; draws on scroll; vertical on ≤1024px.
- Projektliste (Startseite): große Projektnamen als Zeilen mit Projektart, Wohneinheiten, Status; beim Hover dimmen die anderen Zeilen, die aktive rückt ein, und ein Vorschaubild folgt der Maus (oberhalb des Cursors, öffnet per clip-path). Touch und mobil: Vorschaubild in der Zeile, farbig sobald im Blick. Die Kachel-Komponente bleibt für die Projektseite.
- Footer-Wortmarke: „LAUDENBERG“ randlos, per JS auf die Containerbreite eingepasst, Buchstaben steigen beim Erreichen nacheinander auf.
- Buttons: square, 52px, solid ink or ghost; one contact label everywhere: "Projekt anfragen".
- FAQ: details/summary with plus that rotates.
- Contact block: the only dark section (closing), underline inputs, chip radios, all fields optional.

## Layout and motion

12-column grid, max 1440px, gutter clamp(20px,4vw,56px), section spacing clamp(96px,12vw,176px). Square corners everywhere, lines instead of cards. Motion (ease-out cubic-bezier(.23,1,.32,1), ease-in-out cubic-bezier(.77,0,.175,1)):
- Focal moment, the Lageplan is drawn: H1 (her claim) rises out of line masks; beside it an illustrative site plan draws itself: context hatching, Flurstück outline, Baugrenze (dash-dot, revealed through an animated mask), two Mehrfamilienhäuser and six Reihenhäuser grow from their base, trees, labels, north arrow and a Nutzungsschablone (WA, III, 0,4, 1,2, o, FD) follow. Labelled "Beispiel". A five-cell facts strip closes the hero.
- Statement words ink in with scroll (scroll-driven timeline, plain ink fallback).
- Project images open as a plan cut (clip-path from bottom, slight zoom-out), staggered; Leistungen rules are drawn; legend symbols wipe in as a list; portrait uncovers.
- Feedback: buttons and chips press to .97, FAQ opens with height transition, burger morphs into a cross, mobile menu wipes down with staggered link reveal.
- Content stays visible without JS (.js gate); prefers-reduced-motion removes all movement.
