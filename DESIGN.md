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

## Logo

Black square monogram (AL line, white stroke) as header mark, footer mark and favicon (favicon.svg). Path: M62 350 177 85l113 263h140 in a 480 box.

## Components

- Nutzungsschablone: 2-column definition grid, 1px ink borders, mono key over Archivo value.
- Baugrenze: dash-dot stroke (14 5 2 5), 1.25px, used for the hero Baufenster and as the hover outline on project tiles (marching).
- Project tile: 3:2 image, grayscale by default, colour on hover/focus (touch: colour when 75% in view), meta line in muted, title with underline grow.
- Planzeichen legend: 88px symbol box (text code, dashed line, dots, hatch, slope) plus heading and text.
- Maßkette: horizontal dimension line with ticks for process steps; draws on scroll; vertical on ≤1024px.
- Buttons: square, 52px, solid ink or ghost; one contact label everywhere: "Projekt anfragen".
- FAQ: details/summary with plus that rotates.
- Contact block: the only dark section (closing), underline inputs, chip radios, all fields optional.

## Layout and motion

12-column grid, max 1440px, gutter clamp(20px,4vw,56px), section spacing clamp(96px,12vw,176px). Square corners everywhere, lines instead of cards. Motion: hero rise on load, tile hover (grayscale to colour + Baugrenze), Maßkette draw, logo stroke draw on hover; all disabled under prefers-reduced-motion.
